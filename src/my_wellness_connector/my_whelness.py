import requests
import re
import datetime
import typing
from lxml import html
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


class MyWellness:
    def __init__(self) -> None:
        self.session = requests.Session()

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

    def get_token_and_app_id(
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
        token: str,
        app_id: str,
        start_date: datetime.date,
        end_date: datetime.date,
    ) -> list[str]:
        header_info: dict = {
            "token": token,
            "fromDate": start_date.strftime("%d/%m/%Y)"),
            "toDate": end_date.strftime("%d/%m/%Y)"),
            "appId": app_id,
            "_c": "es_ES",
        }
        response: requests.Request = self.session.get(
            DATE_RANGE_URL, headers=header_info
        )
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

    def get_trainning_sessions(
        self,
        token: str,
        app_id: str,
        start_date: datetime.date,
        end_date: datetime.date,
    ) -> list[dict]:

        ret_trainings: list[dict] = []

        response_text: str = self._get_trainnings(
            token=token, app_id=app_id, start_date=start_date, end_date=end_date
        )
        html_doc = html.fromstring(response_text)
        row_ods = html_doc.xpath('//div[@class="row odd"]')
        for row in row_ods:
            for session in row.xpath('.//div[@class="single-item clearfix even"]/a'):
                notes: list[str] = list(
                    map(
                        lambda note: note.text_content(),
                        row.xpath('.//span[@class="note"]'),
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
        self,
        href: str,
        id_cr: str,
        position: int,
        day_open_session: str,
        machine_type: str,
        activity_id: str,
    ) -> dict[str, str]:

        exercise_content: str = self._get_training_exeercices_content(
            url=href, id_cr=id_cr, position=position, day_open_session=day_open_session
        )
        ret_exercice_atributes: dict = self.get_attributes_session_content(
            session_exercice_content=exercise_content
        )
        ret_exercice_atributes[MACHINE_TYPE_ATTRIBUTE] = machine_type
        ret_exercice_atributes[ACTIVITY_ID_ATTRIBUTE] = activity_id

        return ret_exercice_atributes

    def get_attributes_session_content(
        self, session_exercice_content: str
    ) -> dict[str, str]:
        training_parsed: dict = html.fromstring(session_exercice_content)
        table: dict = training_parsed.xpath('//table[@class="exercise-table"]')
        ret_training: dict[str, str] = {}
        if table:
            rows = table[0].xpath(".//tr")
            for row in rows:
                th_elements = row.xpath(".//th")
                td_elements = row.xpath(".//td")
                # ret_training[th.text_content()] = td.text_content()
                ret_training[th_elements[0].text_content()] = td_elements[
                    0
                ].text_content()
                # th_values.extend([th.text_content() for th in th_elements])
                # td_values.extend([td.text_content() for td in td_elements])
        else:
            raise Exception("Table not found")

        return ret_training
