import os
from my_wellness_connector.constants import (
    ACTIVITY_ID_ATTRIBUTE,
    CELL_DATE_ATTRIBUTE,
    DATA_POSITION_ATTRIBUTE,
    HREF_ATTRIBUTE,
    IDCR_ATTRIBUTE,
    MACHINE_TYPE_ATTRIBUTE,
)
from my_wellness_connector.my_whelness import MyWellness
from my_wellness_connector.logger import app_logger
import datetime

username: str = os.getenv("MYWELLNESS_USERNAME")
password: str = os.getenv("MYWELLNESS_PASSWORD")


my_wellness: MyWellness = MyWellness()


token, app_id = my_wellness.get_token_and_app_id(username=username, password=password)

start_date: datetime.date = datetime.date(2024, 8, 15)
end_date: datetime.date = datetime.date(2024, 8, 15)


movements_content: str = my_wellness._get_trainnings(
    token=token, app_id=app_id, start_date=start_date, end_date=end_date
)
with open("/Users/rbean/temp/trainings.html", "w") as file:
    file.write(movements_content)

training_urls: list[str]
training_id_crs: list[str]
training_dates: list[str]
data_positions: list[str]

trainning_sessions: list[dict] = my_wellness.get_trainning_sessions(
    token=token, app_id=app_id, start_date=start_date, end_date=end_date
)

with open("/Users/rbean/temp/trainings_urls.txt", "w") as file_url:
    for training_session in trainning_sessions:
        file_url.write(
            f"{training_session[HREF_ATTRIBUTE]},{training_session[IDCR_ATTRIBUTE]},{training_session[DATA_POSITION_ATTRIBUTE]}\n"
        )
        message_info: str = (
            f"Session: {training_session[CELL_DATE_ATTRIBUTE]} - {training_session[DATA_POSITION_ATTRIBUTE]} - {training_session[MACHINE_TYPE_ATTRIBUTE]} - {training_session[ACTIVITY_ID_ATTRIBUTE]}"
        )
        app_logger.info(message_info)
        session_exercices: str = my_wellness.get_session_exercice(
            href=training_session[HREF_ATTRIBUTE],
            id_cr=training_session[IDCR_ATTRIBUTE],
            position=training_session[DATA_POSITION_ATTRIBUTE],
            day_open_session=training_session[CELL_DATE_ATTRIBUTE],
            machine_type=training_session[MACHINE_TYPE_ATTRIBUTE],
            activity_id=training_session[ACTIVITY_ID_ATTRIBUTE],
        )
        with open(
            f"/Users/rbean/temp/session_{training_session[CELL_DATE_ATTRIBUTE]}_{training_session[DATA_POSITION_ATTRIBUTE]}.json",
            "w",
        ) as file_session:
            file_session.write(str(session_exercices))
