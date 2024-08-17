from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class ExerciseType(Base):
    __tablename__ = "exercise_type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)


class SessionExercise(Base):
    __tablename__ = "session_exercise"
    id = Column(Integer, primary_key=True, autoincrement=True)
    exercise_type_id: Column = Column(Integer)
    machine_type: Column = Column(String)
    activity_id: Column = Column(String)
    session_date: Column = Column(DateTime)
    fc_max: Column = Column(Integer)
    fc_avg: Column = Column(Integer)
    duration_minutes: Column = Column(Integer)
