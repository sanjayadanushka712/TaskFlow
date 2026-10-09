import pytest

from database import engine
from sqlalchemy import inspect
from database import SessionLocal
from models import Task
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()

    session = SessionLocal(
        bind=connection,
        join_transaction_mode="create_savepoint"
    )

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# check database connection
def test_database_connection():
    with engine.connect() as connection:
        result = connection.exec_driver_sql("SELECT 1")
        assert result.scalar() == 1

# check table exists
def test_tasks_table_exists():
    inspector = inspect(engine)

    assert inspector.has_table("tasks")


def test_read_task_from_database(db_session):

    task = Task(
        id=201,
        title="Test PostgreSQL",
        completed=False
    )

    db_session.add(task)
    db_session.commit()

    result = db_session.get(Task, 201)

    assert result is not None
    assert result.id == 201
    assert result.title == "Test PostgreSQL"
    assert result.completed is False

# update task from database
def test_update_task_in_database(db_session):
        task = Task(
            id=202,
            title="Learn PostgreSQL",
            completed=False
        )

        db_session.add(task)
        db_session.commit()

        task.title = "update task"
        db_session.commit()

        result = db_session.get(Task, 202)

        assert result.title == "update task"  # type: ignore

def test_delete_task_from_database(db_session):
        task = Task(
            id=203,
            title="delete Task",
            completed=False
        )

        db_session.add(task)
        db_session.commit()

        db_session.delete(task)
        db_session.commit()

        result = db_session.get(Task, 203)

        assert result is None

# complete task from database
def test_complete_task_in_database(db_session):
        task = Task(
            id=204,
            title="complete Task",
            completed=False
        )

        db_session.add(task)
        db_session.commit()

        task.completed = True
        db_session.commit()

        result = db_session.get(Task, 204)

        assert result.completed  == True # type: ignore      

# database duplicate id
def test_duplicate_id_in_database(db_session):
        task = Task(
            id=205,
            title="duplicate Task",
            completed=False
        )
        db_session.add(task)
        db_session.commit()

        with pytest.raises(IntegrityError):
            task = Task(
                            id=205,
                            title="duplicate Task",
                            completed=False
                        )
            db_session.add(task)
            db_session.commit()


# database check multi tasks update
def test_multi_tasks_update_one_not_exists(db_session):
        task1 = Task(
            id=206,
            title="Multitask 1",
            completed=False
        )

        db_session.add(task1)
        db_session.commit()

        task_206 = db_session.get(Task, 206)
        task_207 = db_session.get(Task, 207)

        with pytest.raises(AttributeError):


            task_206.title = "Learn Python" # type: ignore
            task_207.title = "Learn SQLAlchemy" # type: ignore
