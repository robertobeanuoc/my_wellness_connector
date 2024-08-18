from sqlalchemy import Engine, insert
from sqlalchemy.orm import Session
from my_wellness_connector.db import get_db_engine, get_db_url
from my_wellness_connector.model import ExerciseType, MachineType


engine: Engine = get_db_engine(get_db_url())


def sync_master_data():
    with Session(engine) as session:
        stmt = (
            insert(ExerciseType)
            .values(name="Aerobic")
            .on_conflict_do_update(index_elements=["name"], set_=dict(name="Aerobic"))
        )
        session.execute(stmt)


if __name__ == "__main__":
    sync_master_data()
