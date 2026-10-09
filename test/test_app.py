from app import Taskflow
from database import SessionLocal,engine

import pytest

@pytest.fixture
def session():
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
# get all tasks
# def test_get_all_tasks_empty(session):
#     obj = Taskflow(session)

#     assert obj.get_all_task() == []


# get all tasks
def test_get_all_tasks_normal(session):
    obj = Taskflow(session)
    obj.create_task(16,"Learn Python")
    obj.create_task(17,"Learn Docker")

    assert obj.get_all_task() == [{'id': 16, 'title': 'Learn Python', 'completed': False}, {'id': 17, 'title': 'Learn Docker', 'completed': False}]



# create task
def test_create_task(session):
    obj = Taskflow(session)

    task = obj.create_task(1,"Learn Docker")

    assert task == {
        "id": 1,
        "title": "Learn Docker",
        "completed": False
    }


def test_check_task_id(session):
    obj = Taskflow(session)
    obj.create_task(2,"Learn Docker") 
    assert obj.find_task( 2) == {'id': 2, 'title': 'Learn Docker', 'completed': False}

      

def test_duplicate_task_id(session):
    obj = Taskflow(session)
    obj.create_task(3,"Learn Python")
    with pytest.raises(ValueError):
         obj.create_task(3,"Learn Python")      


def test_create_task_with_not_int_id(session):
    obj = Taskflow(session)
    with pytest.raises(TypeError):
         obj.create_task("Learn Python", "test")    

def test_create_taskId_with_empty_space(session):
    obj = Taskflow(session)
    with pytest.raises(TypeError):
         obj.create_task("  ","Learn Python")   



# complete task
def test_completed_task(session):
    obj = Taskflow(session)
    obj.create_task(4,"Learn Python")
    assert obj.complete_task(4) == True
    assert obj.find_task(4) == {'id': 4, 'title': 'Learn Python', 'completed': True}
        

def test_complete_missing_task(session):
    obj = Taskflow(session)
    assert obj.complete_task(99) == False


# delete task
def test_delete_task(session):
    obj = Taskflow(session)
    obj.create_task(5,"Learn Python")
    obj.create_task(6,"Learn Docker")

    assert obj.delete_task(5) == True


def test_delete_task_if_not_Exists(session):
    obj = Taskflow(session)
    obj.create_task(7,"Learn Python")
    obj.create_task(8,"Learn Docker")

    assert obj.delete_task(99) == False


def test_delete_task_second_task(session):
    obj = Taskflow(session)
    obj.create_task(9,"Learn Python")
    obj.create_task(10,"Learn Docker")

    assert obj.delete_task(10) == True


# update task
def test_Update_task_normal(session):
    obj = Taskflow(session)
    obj.create_task(11,"Learn Python")
    obj.create_task(12,"Learn Docker")

    assert obj.update_task(12,"Learn django") == {'id': 12, 'title': 'Learn django', 'completed': False}


def test_update_task_wrong_id(session):
    obj = Taskflow(session)
    with pytest.raises(ValueError):
             obj.update_task(1, "") 


def test_update_task_null_title(session):
    obj = Taskflow(session)
    obj.create_task(13,"Learn Python")
    obj.create_task(14,"Learn Docker")

    assert obj.update_task(99,"Learn Docker") == False


def test_update_completed_task(session):
    obj = Taskflow(session)

    obj.create_task(15,"Learn Python")
    obj.complete_task(15)

    updated = obj.update_task(15, "Learn Advanced Python")

    assert updated == {
        "id": 15,
        "title": "Learn Advanced Python",
        "completed": True
    }



