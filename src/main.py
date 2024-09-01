#!/usr/bin/env python
from asyncio import sleep
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
    MACHINE_TYPE_SYNCRO_ARTIS_2019,
    MACHINE_DATA_HORIZONTAL,
    MACHINE_DATA_VERTICAL,
    ExerciseType,
    MachineType,
)


engine: Engine = get_db_engine(get_db_url())
my_wellness: MyWellness = MyWellness()


def insert_machine_data(session: Session, machine_data: str):
    stmt_check = select(MachineClass).where(MachineClass.name == machine_data)
    result = session.execute(stmt_check)
    exists = result.fetchone() is not None
    if not exists:
        machine_data: MachineClass = MachineClass(name=machine_data)
        session.add(machine_data)
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


def insert_machine_dataes(session: Session):
    insert_machine_data(session, MACHINE_DATA_HORIZONTAL)
    insert_machine_data(session, MACHINE_DATA_VERTICAL)


def insert_machine_type(
    session: Session, machine_type: str, exercise_type: str, machine_data: str
):
    stmt_check = select(MachineType).where(MachineType.name == machine_type)
    result = session.execute(stmt_check)
    exists = result.fetchone() is not None
    if not exists:
        machine_type: MachineType = MachineType(name=machine_type)
        machine_type.exercise_type_uuid = ExerciseType.get_by_name(
            session, exercise_type
        ).uuid
        machine_type.machine_data_uuid = MachineClass.get_by_name(
            session=session, name=machine_data
        ).uuid
        session.add(machine_type)
        session.commit()
        session.flush()


def insert_machine_types(session: Session):
    insert_machine_type(
        session=session,
        machine_type=MACHINE_TYPE_GROUP_CYCLING,
        exercise_type=EXERCISE_TYPE_AEROBIC,
        machine_data=MACHINE_DATA_VERTICAL,
    )
    insert_machine_type(
        session=session,
        machine_type=MACHINE_TYPE_RUN_ARTIS,
        exercise_type=EXERCISE_TYPE_AEROBIC,
        machine_data=MACHINE_DATA_VERTICAL,
    )
    insert_machine_type(
        session=session,
        machine_type=MACHINE_TYPE_SYNCRO_ARTIS,
        exercise_type=EXERCISE_TYPE_AEROBIC,
        machine_data=MACHINE_DATA_VERTICAL,
    )
    insert_machine_type(
        session=session,
        machine_type=MACHINE_TYPE_SYNCRO_ARTIS_2019,
        exercise_type=EXERCISE_TYPE_AEROBIC,
        machine_data=MACHINE_DATA_VERTICAL,
    )

    insert_machine_type(
        session=session,
        machine_type=MACHINE_TYPE_CHEST_PRESS_BIO,
        exercise_type=EXERCISE_TYPE_STRENGTH,
        machine_data=MACHINE_DATA_VERTICAL,
    )
    insert_machine_type(
        session=session,
        machine_type=MACHINE_TYPE_RUN_ARTIS_CHEST,
        exercise_type=EXERCISE_TYPE_STRENGTH,
        machine_data=MACHINE_DATA_HORIZONTAL,
    )


def sync_master_data():
    with Session(engine) as session:
        insert_machine_dataes(session)
        insert_exercise_types(session)
        insert_machine_types(session)


def insert_exercise_types(session):
    insert_exercise_type(session, EXERCISE_TYPE_AEROBIC)
    insert_exercise_type(session, EXERCISE_TYPE_STRENGTH)
    insert_exercise_type(session, EXERCISE_TYPE_BALANCE)
    insert_exercise_type(session, EXERCISE_TYPE_FLEXIBILITY)


def sync_sessions(start_date: datetime.date, end_date: datetime.date):
    trainning_sessions: list[dict] = my_wellness.get_trainning_sessions(
        start_date=start_date, end_date=end_date
    )
    with Session(engine, autocommit=False, autoflush=False) as session:
        for training_session in trainning_sessions:
            machine_type: MachineType = MachineType.get_by_name(
                session=session, name=training_session[MACHINE_TYPE_ATTRIBUTE]
            )
            session_execise_db: SessionExercise = SessionExercise.get_by_activity_uuid(
                session, training_session[ACTIVITY_ID_ATTRIBUTE]
            )
            session_exercise_attributes: dict[str, str] = (
                my_wellness.get_session_exercice(
                    training_session=training_session,
                    machine_data=machine_type.machine_data.name,
                )
            )
            app_logger.info(
                "Processing session: %s session exercise atributes %s",
                training_session[ACTIVITY_ID_ATTRIBUTE],
                session_exercise_attributes,
            )
            if not session_execise_db:
                try:
                    session_execise = SessionExercise(
                        activity_uuid=training_session[ACTIVITY_ID_ATTRIBUTE],
                        session_date=training_session[CELL_DATE_ATTRIBUTE],
                        fc_avg=my_wellness.get_int_attribute_from_session(
                            session_exercise_attributes, "FC media"
                        ),
                        fc_max=my_wellness.get_int_attribute_from_session(
                            session_exercise_attributes, "FC Máx."
                        ),
                        machine_type_uuid=MachineType.get_by_name(
                            session=session,
                            name=machine_type.name,
                        ).uuid,
                        power_avg=my_wellness.get_int_attribute_from_session(
                            session_exercise_attributes, "Potencia media"
                        ),
                        moves=my_wellness.get_int_attribute_from_session(
                            session_exercise_attributes, "MOVEs"
                        )
                        + my_wellness.get_int_attribute_from_session(
                            session_exercise_attributes, "Repeticiones [rep] hecho"
                        ),
                        weight=my_wellness.get_int_attribute_from_session(
                            session_exercise_attributes, "Carga levantada total"
                        )
                        + my_wellness.get_int_attribute_from_session(
                            session_exercise_attributes, "Carga [kg] hecho"
                        ),
                        duration_minutes=my_wellness.get_minutes_from_time_attribute_from_session(
                            session_exercise_attributes, "Duración [min]"
                        )
                        + my_wellness.get_minutes_from_time_attribute_from_session(
                            session_exercise_attributes, "Duración"
                        ),
                        calories=my_wellness.get_int_attribute_from_session(
                            session_exercise_attributes, "Calorías"
                        ),
                    )
                    session.add(session_execise)
                    session.flush()
                    session.commit()

                except Exception as e:
                    app_logger.error(f"Error: {e}")


if __name__ == "__main__":
    start_date: datetime.date = datetime.date.today()
    end_date: datetime.date = datetime.date.today() + datetime.timedelta(
        days=int(os.getenv("DAYS_BACK")) if os.getenv("DAYS_BACK") else 7
    )
    if os.getenv("START_DATE"):
        start_date: datetime.date = datetime.datetime.strptime(
            os.getenv("START_DATE"), "%Y-%m-%d"
        ).date()
        end_date: datetime.date = datetime.datetime.strptime(
            os.getenv("END_DATE"), "%Y-%m-%d"
        ).date()
    sync_master_data()
    sync_sessions(start_date=start_date, end_date=end_date)
