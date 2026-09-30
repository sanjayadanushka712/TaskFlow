from app import Taskflow
import pytest

# test 1
def test_create_task():
    obj = Taskflow()

    task = obj.create_task("Learn Docker", 1)

    assert task == {
        "id": 1,
        "title": "Learn Docker",
        "completed": False
    }

# test3 
def test_check_task_id():
    obj = Taskflow()
    obj.create_task("Learn Docker", 1) 
    assert obj.find_task( 1) == {'id': 1, 'title': 'Learn Docker', 'completed': False}

      
# test 4
def test_duplicate_task_id():
    obj = Taskflow()
    obj.create_task("Learn Python", 1)
    with pytest.raises(ValueError):
         obj.create_task("Learn Python", 1)
        

# test 5
def test_completed_task():
    obj = Taskflow()
    obj.create_task("Learn Python", 1)
    assert obj.complete_task(1) == True
    assert obj.find_task(1) == {'id': 1, 'title': 'Learn Python', 'completed': True}
        
# test 6
def test_complete_missing_task():
    obj = Taskflow()
    assert obj.complete_task(99) == False