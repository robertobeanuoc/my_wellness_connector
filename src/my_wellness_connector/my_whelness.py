import requests
import re
import datetime
import typing
import os
from lxml import html
import urllib
from my_wellness_connector.constants import (
    ACTIVITY_ID_ATTRIBUTE,
    CELL_DATE_ATTRIBUTE,
    DATA_POSITION_ATTRIBUTE,
    HREF_ATTRIBUTE,
    IDCR_ATTRIBUTE,
    MACHINE_TYPE_ATTRIBUTE,
    REGULAR_EXPRESSION_ACTIVITY_ID,
    TOKEN_URL,
    DATE_RANGE_URL,
    REGULAR_EXPRESION_TOKEN,
    REGULAR_EXPRESION_ID,
    REGULAR_EXPRESION_ID_CR,
    REGULAR_EXPRESION_DATE,
    REGULAR_EXPRESSION_DATA_POSITION,
)
from my_wellness_connector.logger import app_logger
from my_wellness_connector.model import MACHINE_DATA_VERTICAL


class MyWellness:
    token: str = ""
    app_id: str = ""

    def __init__(self) -> None:
        self.session = requests.Session()
        self.login()

    def _get_token(self, response_text: str) -> str:
        match: re.Match = re.search(REGULAR_EXPRESION_TOKEN, response_text)
        if not match:
            raise Exception("Token not found")
        else:
            ret_token = match.group(1)
        return ret_token

    def _get_app_id(self, response_text: str) -> str:
        match: re.Match = re.search(REGULAR_EXPRESION_ID, response_text)
        if not match:
            raise Exception("App Id not found")
        else:
            ret_app_id = match.group(1)

        return ret_app_id

    def login(self):
        username: str = os.getenv("MYWELLNESS_USERNAME")
        password: str = os.getenv("MYWELLNESS_PASSWORD")
        self.token, self.app_id = self._get_token_and_app_id(username, password)

    def _get_token_and_app_id(
        self, username: str, password: str
    ) -> typing.Tuple[str, str]:
        header_info: dict = {
            "UserBinder.Username": username,
            "UserBinder.Password": password,
            "UserBinder.IsFromLogin": True,
            "UserBinder.KeepMeLogged": False,
        }
        response: requests.Request = self.session.post(TOKEN_URL, data=header_info)
        ret_token: str = self._get_token(response.text)
        ret_app_id: str = self._get_app_id(response.text)

        return ret_token, ret_app_id

    def _get_trainnings(
        self,
        start_date: datetime.date,
        end_date: datetime.date,
    ) -> list[str]:
        params: dict = {
            "token": self.token,
            "fromDate": start_date.strftime("%d/%m/%Y"),
            "toDate": end_date.strftime("%d/%m/%Y"),
            "appId": self.app_id,
            "_c": "es_ES",
        }
        encoded_params = urllib.parse.urlencode(params)
        full_url: str = f"{DATE_RANGE_URL}?{encoded_params}"
        response: requests.Request = self.session.get(full_url)
        return response.text

    def _getids_cr(self, response_text: str) -> list[str]:
        ret_idr_crs: list[str] = re.findall(REGULAR_EXPRESION_ID_CR, response_text)
        return ret_idr_crs

    def _get_dates(self, response_text: str) -> list[str]:
        ret_dates: list[str] = list(
            set(re.findall(REGULAR_EXPRESION_DATE, response_text))
        )

        return ret_dates

    def _get_data_position(self, response_text: str) -> list[str]:
        ret_positions: list[str] = re.findall(
            REGULAR_EXPRESSION_DATA_POSITION, response_text
        )
        return ret_positions

    def _get_physical_activity_id(self, url: str) -> str:
        ret_activity_id: str = re.findall(REGULAR_EXPRESSION_ACTIVITY_ID, url)[0]
        return ret_activity_id

    def _machine_type_has_vertical_data(self, machine_type: str) -> bool:
        ret_has_vertical_data: bool = False
        if "vertical" in machine_type.lower():
            return True

    def get_trainning_sessions(
        self,
        start_date: datetime.date,
        end_date: datetime.date,
    ) -> list[dict]:

        ret_trainings: list[dict] = []

        response_text: str = self._get_trainnings(
            start_date=start_date,
            end_date=end_date,
        )
        html_doc = html.fromstring(response_text)
        row_ods = html_doc.xpath('//div[@class="row odd"]')
        for row in row_ods:
            for session in row.xpath('.//div[@class="single-item clearfix even"]/a'):
                notes: list[str] = list(
                    map(
                        lambda note: note.text_content(),
                        session.xpath('.//span[@class="note"]'),
                    )
                )
                machine_type: str = " ".join(notes)
                session_attrib: dict = {
                    CELL_DATE_ATTRIBUTE: row.xpath('.//div[@class="cell date"]')[
                        0
                    ].text_content(),
                    IDCR_ATTRIBUTE: row.xpath('.//input[@name="hdSessionIdCR"]')[
                        0
                    ].attrib["id"],
                    HREF_ATTRIBUTE: session.attrib["href"],
                    DATA_POSITION_ATTRIBUTE: int(session.attrib["data-position"]),
                    MACHINE_TYPE_ATTRIBUTE: machine_type,
                    ACTIVITY_ID_ATTRIBUTE: self._get_physical_activity_id(
                        url=session.attrib["href"]
                    ),
                }
                if session_attrib[MACHINE_TYPE_ATTRIBUTE] == "Run Artis":
                    i = 10
                ret_trainings.append(session_attrib)

        return ret_trainings

    def _get_training_exeercices_content(
        self, url: str, id_cr: str, position: int, day_open_session: str
    ) -> str:
        header_info: dict = {
            "idCR": id_cr,
            "position": position,
            "dayOpenSession": day_open_session,
            "singleView": True,
        }
        response: requests.Request = self.session.get(url, data=header_info)
        return response.text

    def get_session_exercice(
        self, training_session: dict[str, str], machine_data: str
    ) -> dict[str, str]:

        exercise_content: str = self._get_training_exeercices_content(
            url=training_session[HREF_ATTRIBUTE],
            id_cr=training_session[IDCR_ATTRIBUTE],
            position=training_session[DATA_POSITION_ATTRIBUTE],
            day_open_session=training_session[CELL_DATE_ATTRIBUTE],
        )
        ret_exercice_atributes: dict = self.get_attributes_session_content(
            session_exercice_content=exercise_content, machine_data=machine_data
        )
        ret_exercice_atributes[MACHINE_TYPE_ATTRIBUTE] = (
            training_session[MACHINE_TYPE_ATTRIBUTE],
        )
        ret_exercice_atributes[ACTIVITY_ID_ATTRIBUTE] = (
            training_session[ACTIVITY_ID_ATTRIBUTE],
        )

        return ret_exercice_atributes

    def get_attributes_session_content(
        self, session_exercice_content: str, machine_data: str
    ) -> dict[str, str]:
        training_parsed: dict = html.fromstring(session_exercice_content)
        session_exercise_content_fixed: str = html.tostring(
            training_parsed, pretty_print=True
        ).decode()
        training_parsed: dict = html.fromstring(session_exercise_content_fixed)
        table: dict = training_parsed.xpath('//table[@class="exercise-table"]')
        ret_training: dict[str, str] = {}
        if table:
            if machine_data == MACHINE_DATA_VERTICAL:
                table_rows = table[0].xpath(".//tbody//tr")
                for table_row in table_rows:
                    td_elements = table_row.xpath(".//td")
                    th_elements = table_row.xpath(".//th")
                    if th_elements and td_elements:
                        ret_training[th_elements[0].text_content()] = td_elements[
                            0
                        ].text_content()
            else:
                training_properties: list[str] = []
                table_headers = table[0].xpath(".//tbody//th")
                for table_header in table_headers:
                    training_properties.append(table_header.text_content())
                table_rows = table[0].xpath(".//tbody//tr")
                for table_row in table_rows:
                    td_elements = table_row.xpath(".//td")
                    for i in range(len(td_elements)):
                        if training_properties[i] in ret_training.keys():
                            ret_training[training_properties[i]] += (
                                "," + td_elements[i].text_content()
                            )
                        else:
                            ret_training[training_properties[i]] = td_elements[
                                i
                            ].text_content()
        else:
            raise Exception("Table not found")

        return ret_training

    @staticmethod
    def get_int_attribute_from_session(
        session_exercise: dict[str, str], attribute: str
    ) -> int:
        ret_attribute: int = 0
        if attribute in session_exercise:
            for match in re.findall(r"[0-9]+", session_exercise[attribute]):
                ret_attribute = int(match)
        return ret_attribute

    @staticmethod
    def get_minutes_from_time_attribute_from_session(
        session_exercise: dict[str, str], attribute: str
    ) -> float:
        ret_attribute: float = 0
        if attribute in session_exercise:
            for match in re.findall(
                r"[0-9][0-9]?:[0-9][0-9]", session_exercise[attribute]
            ):
                minutes, seconds = match.split(":")
                ret_attribute = float(minutes) + float(seconds) / 60
        return ret_attribute
