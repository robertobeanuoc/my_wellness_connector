from sqlalchemy import create_engine
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
        f"mysql://{user_name()}:{password()}@{host()}/{db_name()}"
    )
    return ret_connection_string
