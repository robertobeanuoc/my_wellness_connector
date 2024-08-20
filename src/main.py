#!/usr/bin/env python
from sqlalchemy import Engine, insert
from sqlalchemy.dialects.mysql import insert as mysql_insert
from sqlalchemy.orm import Session
import sys

from my_wellness_connector.db import get_db_engine, get_db_url
from sqlalchemy import select
from my_wellness_connector.model import (
    AEROBIC_EXERCISE_TYPE,
    RESISTANCE_EXERCISE_TYPE,
    BALANCE_EXERCISE_TYPE,
    FLEXIBILITY_EXERCISE_TYPE,
    ExerciseType,
)


engine: Engine = get_db_engine(get_db_url())


def insert_exercise_type(session: Session, exercise_type: str):
    stmt_check = select(ExerciseType).where(ExerciseType.name == exercise_type)
    result = session.execute(stmt_check)
    exists = result.fetchone() is not None
    if not exists:
        exercise_type: ExerciseType = ExerciseType(name=exercise_type)
        session.add(exercise_type)
        session.commit()
        session.flush()


def sync_master_data():
    with Session(engine) as session:
        insert_exercise_type(session, AEROBIC_EXERCISE_TYPE)
        insert_exercise_type(session, RESISTANCE_EXERCISE_TYPE)
        insert_exercise_type(session, BALANCE_EXERCISE_TYPE)
        insert_exercise_type(session, FLEXIBILITY_EXERCISE_TYPE)


if __name__ == "__main__":
    sync_master_data()
