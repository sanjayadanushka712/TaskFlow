from app import Taskflow
import pytest

# test 1
def test_create_task():
    obj = Taskflow()

    task = obj.create_task(1,"Learn Docker")

    assert task == {
        "id": 1,
        "title": "Learn Docker",
        "completed": False
    }

# test2 
def test_check_task_id():
    obj = Taskflow()
    obj.create_task(1,"Learn Docker") 
    assert obj.find_task( 1) == {'id': 1, 'title': 'Learn Docker', 'completed': False}

      
# test 3
def test_duplicate_task_id():
    obj = Taskflow()
    obj.create_task(1,"Learn Python")
    with pytest.raises(ValueError):
         obj.create_task(1,"Learn Python")      

# test 4
def test_create_task_with_not_int_id():
    obj = Taskflow()
    with pytest.raises(TypeError):
         obj.create_task("Learn Python", "test")    

# test 5
def test_completed_task():
    obj = Taskflow()
    obj.create_task(1,"Learn Python")
    assert obj.complete_task(1) == True
    assert obj.find_task(1) == {'id': 1, 'title': 'Learn Python', 'completed': True}
        
# test 6
def test_complete_missing_task():
    obj = Taskflow()
    assert obj.complete_task(99) == False

# test 7
def test_delete_task():
    obj = Taskflow()
    obj.create_task(1,"Learn Python")
    obj.create_task(2,"Learn Docker")

    assert obj.delete_task(1) == True


# test 8
def test_delete_task_if_not_Exists():
    obj = Taskflow()
    obj.create_task(1,"Learn Python")
    obj.create_task(2,"Learn Docker")

    assert obj.delete_task(99) == False

# test 9
def test_delete_task_second_task():
    obj = Taskflow()
    obj.create_task(1,"Learn Python")
    obj.create_task(2,"Learn Docker")

    assert obj.delete_task(2) == True

# test 10
def test_Update_task_normal():
    obj = Taskflow()
    obj.create_task(1,"Learn Python")
    obj.create_task(2,"Learn Docker")

    assert obj.update_task(2,"Learn django") == {'id': 2, 'title': 'Learn django', 'completed': False}

# test 11
def test_update_task_wrong_id():
    obj = Taskflow()
    with pytest.raises(ValueError):
             obj.update_task("Learn Python", "") 

# test 12
def test_update_task_null_title():
    obj = Taskflow()
    obj.create_task(1,"Learn Python")
    obj.create_task(2,"Learn Docker")

    assert obj.update_task(99,"Learn Docker") == False

# test13
def test_update_completed_task():
    obj = Taskflow()

    obj.create_task(1,"Learn Python")
    obj.complete_task(1)

    updated = obj.update_task(1, "Learn Advanced Python")

    assert updated == {
        "id": 1,
        "title": "Learn Advanced Python",
        "completed": True
    }