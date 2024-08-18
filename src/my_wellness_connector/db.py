from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
import os


def user_name():
    return os.getenv("DB_USERNAME")


def password():
    return os.getenv("DB_PASSWORD")


def host():
    return os.getenv("DB_HOST")


def db_name():
    return os.getenv("DB_NAME")


def get_db_url():
    ret_connection_string: str = (
        f"mysql+pymysql://{user_name()}:{password()}@{host()}/{db_name()}"
    )
    return ret_connection_string


def get_deb_engine(url: str) -> Engine:
    return create_engine(url)
