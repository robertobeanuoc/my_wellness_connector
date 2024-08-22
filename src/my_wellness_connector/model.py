from typing import List
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, event
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
import datetime
import uuid

ID_STRING_LENGTH: int = 64
NAME_STRING_LENGTH: int = 100

# Exercise Types
EXERCISE_TYPE_AEROBIC: str = "Aerobic"
EXERCISE_TYPE_RESISTANCE: str = "Resistance"
EXERCISE_TYPE_FLEXIBILITY: str = "Flexibility"
EXERCISE_TYPE_BALANCE: str = "Balance"

# Machine Types
MACHINE_TYPE_GROUP_CYCLING: str = "Group Cycle Connect"
MACHINE_TYPE_RUN_ARTIS: str = "Run Artis"
MACHINE_TYPE_SYNCRO_ARTIS: str = "Synchro Artis"
MACHINE_TYPE_CHEST_PRESS_BIO: str = "Chest Press Biostrength"
MACHINE_TYPE_RUN_ARTIS_CHEST: str = "Chest Press Artis"


class Base(DeclarativeBase):
    uuid: Mapped[String] = mapped_column(
        String(ID_STRING_LENGTH), primary_key=True, default=str(uuid.uuid4())
    )
    row_created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.datetime.now(datetime.UTC)
    )
    row_updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=True,
        default=None,
    )


class ExerciseType(Base):
    __tablename__ = "exercise_type"
    name: Column = Column(String(NAME_STRING_LENGTH), unique=True)

    @staticmethod
    def get_by_name(session, name: str):
        return session.query(ExerciseType).filter_by(name=name).first()


@event.listens_for(ExerciseType, "before_insert")
def before_insert(mapper, connection, target):
    target.row_created_at = datetime.datetime.now(datetime.UTC)
    target.uuid = str(uuid.uuid4())


@event.listens_for(ExerciseType, "before_update")
def before_update(mapper, connection, target):
    target.row_updated_at = datetime.datetime.now(datetime.UTC)


class MachineType(Base):
    __tablename__ = "machine_type"
    exercise_type_uuid: Column = Column(
        String(ID_STRING_LENGTH), ForeignKey("exercise_type.uuid")
    )
    name: Column = Column(String(NAME_STRING_LENGTH), unique=True)

    @staticmethod
    def get_by_name(session, name: str):
        return session.query(MachineType).filter_by(name=name).first()


@event.listens_for(MachineType, "before_insert")
def before_insert(mapper, connection, target):
    target.row_created_at = datetime.datetime.now(datetime.UTC)
    target.uuid = str(uuid.uuid4())


@event.listens_for(MachineType, "before_update")
def before_update(mapper, connection, target):
    target.row_updated_at = datetime.datetime.now(datetime.UTC)


class SessionExercise(Base):
    __tablename__ = "session_exercise"
    exercise_type_uuid: Column = Column(
        String(ID_STRING_LENGTH), ForeignKey("exercise_type.uuid")
    )
    machine_type_uuid: Column = Column(
        String(NAME_STRING_LENGTH), ForeignKey("machine_type.uuid")
    )
    activity_uuid: Column = Column(String(ID_STRING_LENGTH), unique=True)
    session_date: Column = Column(DateTime)
    fc_max: Column = Column(Integer)
    fc_avg: Column = Column(Integer)
    duration_minutes: Column = Column(Integer)

    @staticmethod
    def get_by_activity_uuid(session, activity_uuid: str):
        return (
            session.query(SessionExercise)
            .filter_by(activity_uuid=activity_uuid)
            .first()
        )


@event.listens_for(SessionExercise, "before_insert")
def before_insert(mapper, connection, target):
    target.row_created_at = datetime.datetime.now(datetime.UTC)
    target.uuid = str(uuid.uuid4())


@event.listens_for(SessionExercise, "before_update")
def before_update(mapper, connection, target):
    target.row_updated_at = datetime.datetime.now(datetime.UTC)
