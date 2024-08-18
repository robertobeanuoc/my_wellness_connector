from typing import List
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, event
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
import datetime
import uuid

ID_STRING_LENGTH: int = 64
NAME_STRING_LENGTH: int = 100
AEROBIC_EXERCISE_TYPE: str = "Aerobic"
RESISTANCE_EXERCISE_TYPE: str = "Resistance"


class Base(DeclarativeBase):
    uuid: Mapped[String] = mapped_column(String(ID_STRING_LENGTH), primary_key=True)
    row_created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.datetime.now(datetime.UTC)
    )

    row_updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=True,
        default=None,
    )


@event.listens_for(Base, "before_insert")
def before_insert(mapper, connection, target):
    target.row_created_at = datetime.datetime.now(datetime.UTC)
    target.uuid = uuid.uuid4()


@event.listens_for(Base, "before_update")
def before_update(mapper, connection, target):
    target.row_updated_at = datetime.datetime.now(datetime.UTC)


class ExerciseType(Base):
    __tablename__ = "exercise_type"
    name = Column(String(10), unique=True)
    machine_types: Mapped[List["MachineType"]] = relationship(back_populates="user")


class MachineType(Base):
    __tablename__ = "machine_type"
    name: Column = Column(String(NAME_STRING_LENGTH), unique=True)
    exercise_type_uuid: Column = Column(
        String(ID_STRING_LENGTH), ForeignKey("exercise_type.uuid")
    )
    exercise_type: Mapped[List["ExerciseType"]] = relationship(
        back_populates="machine_types"
    )


class SessionExercise(Base):
    __tablename__ = "session_exercise"
    exercise_type_id: Column = Column(
        String(ID_STRING_LENGTH), ForeignKey("exercise_type.uuid")
    )
    machine_type: Column = Column(String(NAME_STRING_LENGTH))
    activity_uuid: Column = Column(String(ID_STRING_LENGTH))
    session_date: Column = Column(DateTime)
    fc_max: Column = Column(Integer)
    fc_avg: Column = Column(Integer)
    duration_minutes: Column = Column(Integer)
