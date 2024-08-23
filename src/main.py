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
from my_wellness_connector.model import (
    MACHINE_TYPE_SYNCRO_ARTIS_2019,
    ExerciseType,
    MachineClass,
    MachineType,
    SessionExercise,
)
import datetime
import os

from my_wellness_connector.db import get_db_engine, get_db_url
from sqlalchemy import select
from my_wellness_connector.model import (
    EXERCISE_TYPE_AEROBIC,
    MACHINE_TYPE_GROUP_CYCLING,
    EXERCISE_TYPE_STRENGTH,
    EXERCISE_TYPE_BALANCE,
    EXERCISE_TYPE_FLEXIBILITY,
    MACHINE_TYPE_RUN_ARTIS,
    MACHINE_TYPE_SYNCRO_ARTIS,
    MACHINE_TYPE_CHEST_PRESS_BIO,
    MACHINE_TYPE_RUN_ARTIS_CHEST,
    MACHINE_CLASS_GROUP_CYCLING,
    MACHINE_CLASS_RUNNING,
    MACHINE_CLASS_STRENGTH,
    ExerciseType,
    MachineType,
)


engine: Engine = get_db_engine(get_db_url())
my_wellness: MyWellness = MyWellness()


def insert_machine_class(session: Session, machine_class: str):
    stmt_check = select(MachineClass).where(MachineClass.name == machine_class)
    result = session.execute(stmt_check)
    exists = result.fetchone() is not None
    if not exists:
        machine_class: MachineClass = MachineClass(name=machine_class)
        session.add(machine_class)
        session.commit()
        session.flush()


def insert_exercise_type(session: Session, exercise_type: str):
    stmt_check = select(ExerciseType).where(ExerciseType.name == exercise_type)
    result = session.execute(stmt_check)
    exists = result.fetchone() is not None
    if not exists:
        exercise_type: ExerciseType = ExerciseType(name=exercise_type)
        session.add(exercise_type)
        session.commit()
        session.flush()


def insert_machine_classes(session: Session):
    insert_machine_class(session, MACHINE_CLASS_GROUP_CYCLING)
    insert_machine_class(session, MACHINE_CLASS_RUNNING)
    insert_machine_class(session, MACHINE_CLASS_STRENGTH)


def insert_machine_type(
    session: Session, machine_type: str, exercise_type: str, machine_class: str
):
    stmt_check = select(MachineType).where(MachineType.name == machine_type)
    result = session.execute(stmt_check)
    exists = result.fetchone() is not None
    if not exists:
        machine_type: MachineType = MachineType(name=machine_type)
        machine_type.exercise_type_uuid = ExerciseType.get_by_name(
            session, exercise_type
        ).uuid
        machine_type.machine_class_uuid = MachineClass.get_by_name(
            session=session, name=machine_class
        ).uuid
        session.add(machine_type)
        session.commit()
        session.flush()


def insert_machine_types(session: Session):
    insert_machine_type(
        session=session,
        machine_type=MACHINE_TYPE_GROUP_CYCLING,
        exercise_type=EXERCISE_TYPE_AEROBIC,
        machine_class=MACHINE_CLASS_GROUP_CYCLING,
    )
    insert_machine_type(
        session=session,
        machine_type=MACHINE_TYPE_RUN_ARTIS,
        exercise_type=EXERCISE_TYPE_AEROBIC,
        machine_class=MACHINE_CLASS_RUNNING,
    )
    insert_machine_type(
        session=session,
        machine_type=MACHINE_TYPE_SYNCRO_ARTIS,
        exercise_type=EXERCISE_TYPE_AEROBIC,
        machine_class=MACHINE_CLASS_RUNNING,
    )
    insert_machine_type(
        session=session,
        machine_type=MACHINE_TYPE_SYNCRO_ARTIS_2019,
        exercise_type=EXERCISE_TYPE_AEROBIC,
        machine_class=MACHINE_CLASS_RUNNING,
    )

    insert_machine_type(
        session=session,
        machine_type=MACHINE_TYPE_CHEST_PRESS_BIO,
        exercise_type=EXERCISE_TYPE_STRENGTH,
        machine_class=MACHINE_CLASS_STRENGTH,
    )
    insert_machine_type(
        session=session,
        machine_type=MACHINE_TYPE_RUN_ARTIS_CHEST,
        exercise_type=EXERCISE_TYPE_STRENGTH,
        machine_class=MACHINE_CLASS_STRENGTH,
    )


def sync_master_data():
    with Session(engine) as session:
        insert_machine_classes(session)
        insert_exercise_types(session)
        insert_machine_types(session)


def insert_exercise_types(session):
    insert_exercise_type(session, EXERCISE_TYPE_AEROBIC)
    insert_exercise_type(session, EXERCISE_TYPE_STRENGTH)
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
            machine_type: MachineType = MachineType.get_by_name(
                session=session, name=training_session[MACHINE_TYPE_ATTRIBUTE]
            )
            session_execise: SessionExercise = SessionExercise.get_by_activity_uuid(
                session, training_session[ACTIVITY_ID_ATTRIBUTE]
            )
            session_exercise: dict[str, str] = my_wellness.get_session_exercice(
                training_session=training_session,
                machine_class=machine_type.machine_class.name,
            )
            app_logger.info(
                "Processing session: %s %s",
                training_session[ACTIVITY_ID_ATTRIBUTE],
                session_execise,
            )
            if not session_execise:
                try:
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
                        power_avg=my_wellness.get_int_attribute_from_session(
                            session_exercise, "POTENCIA MEDIA"
                        ),
                        moves=my_wellness.get_int_attribute_from_session(
                            session_exercise, "MOVEs"
                        ),
                        weight=my_wellness.get_int_attribute_from_session(
                            session_exercise, "Carga levantada total"
                        ),
                    )
                    session.add(session_execise)
                    session.flush()
                    session.commit()

                except Exception as e:
                    app_logger.error(f"Error: {e}")


if __name__ == "__main__":

    sync_master_data()
    days_back: int = int(os.getenv("DAYS_BACK")) if os.getenv("DAYS_BACK") else 7

    sync_sessions(days_back=days_back)
