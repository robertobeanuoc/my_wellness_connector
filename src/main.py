#!/usr/bin/env python
from sqlalchemy import Engine, insert
from sqlalchemy.orm import Session
import sys

print(sys.path)
from my_wellness_connector.db import get_db_engine, get_db_url
from my_wellness_connector.model import (
    AEROBIC_EXERCISE_TYPE,
    RESISTANCE_EXERCISE_TYPE,
    ExerciseType,
)


engine: Engine = get_db_engine(get_db_url())


def sync_master_data():
    with Session(engine) as session:
        stmt_aerobic = (
            insert(ExerciseType)
            .values(name=AEROBIC_EXERCISE_TYPE)
            .on_conflict_do_update(
                index_elements=["name"], set_=dict(name=AEROBIC_EXERCISE_TYPE)
            )
        )
        session.execute(stmt_aerobic)
        stmt_resitance = (
            insert(ExerciseType)
            .values(name=RESISTANCE_EXERCISE_TYPE)
            .on_conflict_do_update(
                index_elements=["name"], set_=dict(name=RESISTANCE_EXERCISE_TYPE)
            )
        )

        session.execute(stmt_resitance)


if __name__ == "__main__":
    sync_master_data()
