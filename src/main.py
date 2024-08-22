#!/usr/bin/env python
from sqlalchemy import Engine
from sqlalchemy.dialects.mysql import insert as mysql_insert
from sqlalchemy.orm import Session
from my_wellness_connector.constants import (
    ACTIVITY_ID_ATTRIBUTE,
    CELL_DATE_ATTRIBUTE,
    MACHINE_TYPE_ATTRIBUTE,
)
from my_wellness_connector.my_whelness import MyWellness
from my_wellness_connector.logger import app_logger
from my_wellness_connector.model import ExerciseType, MachineType, SessionExercise
import datetime
import os

from my_wellness_connector.db import get_db_engine, get_db_url
from sqlalchemy import select
from my_wellness_connector.model import (
    EXERCISE_TYPE_AEROBIC,
    MACHINE_TYPE_GROUP_CYCLING,
    EXERCISE_TYPE_RESISTANCE,
    EXERCISE_TYPE_BALANCE,
    EXERCISE_TYPE_FLEXIBILITY,
    MACHINE_TYPE_RUN_ARTIS,
    MACHINE_TYPE_SYNCRO_ARTIS,
    MACHINE_TYPE_CHEST_PRESS_BIO,
    MACHINE_TYPE_RUN_ARTIS_CHEST,
    ExerciseType,
    MachineType,
)


engine: Engine = get_db_engine(get_db_url())
my_wellness: MyWellness = MyWellness()


def insert_exercise_type(session: Session, exercise_type: str):
    stmt_check = select(ExerciseType).where(ExerciseType.name == exercise_type)
    result = session.execute(stmt_check)
    exists = result.fetchone() is not None
    if not exists:
        exercise_type: ExerciseType = ExerciseType(name=exercise_type)
        session.add(exercise_type)
        session.commit()
        session.flush()


def insert_machine_type(session: Session, machine_type: str, exercise_type: str):
    stmt_check = select(MachineType).where(MachineType.name == machine_type)
    result = session.execute(stmt_check)
    exists = result.fetchone() is not None
    if not exists:
        machine_type: MachineType = MachineType(name=machine_type)
        machine_type.exercise_type_uuid = ExerciseType.get_by_name(
            session, exercise_type
        ).uuid
        session.add(machine_type)
        session.commit()
        session.flush()


def insert_machine_types(session: Session):
    insert_machine_type(session, MACHINE_TYPE_GROUP_CYCLING, EXERCISE_TYPE_AEROBIC)
    insert_machine_type(session, MACHINE_TYPE_RUN_ARTIS, EXERCISE_TYPE_AEROBIC)
    insert_machine_type(session, MACHINE_TYPE_SYNCRO_ARTIS, EXERCISE_TYPE_AEROBIC)
    insert_machine_type(session, MACHINE_TYPE_CHEST_PRESS_BIO, EXERCISE_TYPE_RESISTANCE)
    insert_machine_type(session, MACHINE_TYPE_RUN_ARTIS_CHEST, EXERCISE_TYPE_RESISTANCE)


def sync_master_data():
    with Session(engine) as session:
        insert_exercise_types(session)
        insert_machine_types(session)


def insert_exercise_types(session):
    insert_exercise_type(session, EXERCISE_TYPE_AEROBIC)
    insert_exercise_type(session, EXERCISE_TYPE_RESISTANCE)
    insert_exercise_type(session, EXERCISE_TYPE_BALANCE)
    insert_exercise_type(session, EXERCISE_TYPE_FLEXIBILITY)


def sync_sessions(days_back: int):
    start_date: datetime.date = datetime.date.today() - datetime.timedelta(
        days=days_back
    )
    end_date: datetime.date = datetime.date.today()
    trainning_sessions: list[dict] = my_wellness.get_trainning_sessions(
        start_date=start_date, end_date=end_date
    )
    with Session(engine, autocommit=False, autoflush=False) as session:
        for training_session in trainning_sessions:
            session_execise: SessionExercise = SessionExercise.get_by_activity_uuid(
                session, training_session[ACTIVITY_ID_ATTRIBUTE]
            )
            session_exercise: dict[str, str] = my_wellness.get_session_exercice(
                training_session=training_session
            )
            if not session_execise:
                try:
                    machine_type: MachineType = MachineType.get_by_name(
                        session=session, name=training_session[MACHINE_TYPE_ATTRIBUTE]
                    )
                    session_execise = SessionExercise(
                        activity_uuid=training_session[ACTIVITY_ID_ATTRIBUTE],
                        session_date=training_session[CELL_DATE_ATTRIBUTE],
                        fc_avg=my_wellness.get_int_attribute_from_session(
                            session_exercise, "FC media"
                        ),
                        fc_max=my_wellness.get_int_attribute_from_session(
                            session_exercise, "FC Máx."
                        ),
                        machine_type_uuid=MachineType.get_by_name(
                            session=session,
                            name=machine_type.name,
                        ).uuid,
                        exercise_type_uuid=machine_type.exercise_type_uuid,
                    )
                    session.add(session_execise)
                    session.flush()
                    session.commit()

                except Exception as e:
                    app_logger.error(f"Error: {e}")

            app_logger.info(
                "Processing session: %s %s",
                training_session[ACTIVITY_ID_ATTRIBUTE],
                session_execise,
            )


if __name__ == "__main__":

    sync_master_data()
    days_back: int = int(os.getenv("DAYS_BACK")) if os.getenv("DAYS_BACK") else 7

    sync_sessions(days_back=days_back)
