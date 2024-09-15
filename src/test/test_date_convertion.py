from my_wellness_connector.model import convert_utc_to_db_datetime
import datetime


def test_date_convertion():
    print(convert_utc_to_db_datetime(datetime.datetime.now(datetime.timezone.utc)))


test_date_convertion()
