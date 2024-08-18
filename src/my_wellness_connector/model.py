from typing import List
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, event
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
import datetime


class Base(DeclarativeBase):
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


@event.listens_for(Base, "before_update")
def before_update(mapper, connection, target):
    target.row_updated_at = datetime.datetime.now(datetime.UTC)


class ExerciseType(Base):
    __tablename__ = "exercise_type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10))
    machine_types: Mapped[List["MachineType"]] = relationship(back_populates="user")


class SessionExercise(Base):
    __tablename__ = "session_exercise"
    id = Column(Integer, primary_key=True, autoincrement=True)
    exercise_type_id: Column = Column(Integer)
    machine_type: Column = Column(String(100))
    activity_id: Column = Column(String(64))
    session_date: Column = Column(DateTime)
    fc_max: Column = Column(Integer)
    fc_avg: Column = Column(Integer)
    duration_minutes: Column = Column(Integer)


class MachineType(Base):
    __tablename__ = "machine_type"
    id: Column = Column(Integer, primary_key=True, autoincrement=True)
    name: Column = Column(String(100))
    exercise_type_id: Column = Column(Integer, ForeignKey("exercise_type.id"))
    exercise_type: Mapped[List["ExerciseType"]] = relationship(
        back_populates="machine_types"
    )
