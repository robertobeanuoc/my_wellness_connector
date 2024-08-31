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


my_wellness: MyWellness = MyWellness()


start_date: datetime.date = datetime.date(2024, 8, 15)
end_date: datetime.date = datetime.date(2024, 8, 15)


movements_content: str = my_wellness._get_trainnings(
    start_date=start_date, end_date=end_date
)
with open("/Users/rbean/temp/trainings.html", "w") as file:
    file.write(movements_content)

training_urls: list[str]
training_id_crs: list[str]
training_dates: list[str]
data_positions: list[str]

trainning_sessions: list[dict] = my_wellness.get_trainning_sessions(
    start_date=start_date, end_date=end_date
)

with open("/Users/rbean/temp/trainings_urls.txt", "w") as file_url:
    for training_session in trainning_sessions:
        file_url.write(
            f"{training_session[HREF_ATTRIBUTE]},{training_session[IDCR_ATTRIBUTE]},{training_session[DATA_POSITION_ATTRIBUTE]},{training_session[MACHINE_TYPE_ATTRIBUTE]}\n"
        )
        message_info: str = (
            f"Session: {training_session[CELL_DATE_ATTRIBUTE]} - {training_session[DATA_POSITION_ATTRIBUTE]} - {training_session[MACHINE_TYPE_ATTRIBUTE]} - {training_session[ACTIVITY_ID_ATTRIBUTE]}"
        )
        try:
            app_logger.info(message_info)
            session_exercice: str = my_wellness.get_session_exercice(
                training_session=training_session
            )
            with open(
                f"/Users/rbean/temp/session_{training_session[CELL_DATE_ATTRIBUTE]}_{training_session[DATA_POSITION_ATTRIBUTE]}.json",
                "w",
            ) as file_session:
                file_session.write(str(session_exercice))
        except Exception as e:
            app_logger.error(f"Error: {e}")
