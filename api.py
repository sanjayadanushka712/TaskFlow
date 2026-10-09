from fastapi import FastAPI, HTTPException,Depends
from app import Taskflow
from pydantic import BaseModel,Field,field_validator
from database import SessionLocal
from sqlalchemy.exc import IntegrityError

    
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

app = FastAPI()

def validate_title(value: str) -> str:
    cleaned_value = value.strip()

    if not cleaned_value:
        raise ValueError("Title cannot be empty")

    return cleaned_value

class TaskCreate(BaseModel):
    task_id: int = Field(gt=0)
    title: str = Field(min_length=1)


    @field_validator("title")
    @classmethod
    def check_title(cls, value: str) -> str:
        return validate_title(value)


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1)


    @field_validator("title")
    @classmethod
    def check_title(cls, value: str) -> str:
        return validate_title(value)



class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool


# check connection
@app.get("/")
def home():
    return {"message": "TaskFlow API is running"}

# create tasks
@app.post(
    "/tasks",
    status_code=201,
    response_model=TaskResponse,
    responses={409: {"description": "Task ID already exists"}}
)

def create_task(data: TaskCreate,session = Depends(get_session)):
    taskflow = Taskflow(session)
    try:
        task = taskflow.create_task(data.task_id, data.title)
        session.commit()
        return task
    except ValueError as error:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Task ID conflicts with existing data"
        )

# find task
@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    responses={404: {"description": "Task not found"}}
)
def find_task(task_id: int,session = Depends(get_session)):
    taskflow = Taskflow(session)
    task = taskflow.find_task(task_id)
    if not task: 
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task

# complete task
@app.patch(
    "/tasks/{task_id}/complete",
    responses={404: {"description": "Task not found"}}
)
def complete_task(task_id: int,session = Depends(get_session)):
    """Mark a task as completed."""
    taskflow = Taskflow(session)
    success = taskflow.complete_task(task_id)
    if not success:
        session.rollback()
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    session.commit()
    return {"message": "Task completed successfully"}


# delete task
@app.delete("/tasks/{task_id}",
            responses={404: {"description": "Task not found"}}
)
def delete_task(task_id: int,session = Depends(get_session)):
    """Delete a task by its ID."""
    taskflow = Taskflow(session)
    success = taskflow.delete_task(task_id)
    if not success:
        session.rollback()
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    session.commit()
    return {"message": "Task deleted successfully"}

# update tasks
@app.put("/tasks/{task_id}",
         responses={404: {"description": "Task not found"}}
)
def update_task(task_id: int, data: TaskUpdate,session = Depends(get_session)):
    """Update a task title."""
    taskflow = Taskflow(session)
    task = taskflow.update_task(task_id, data.title)
    if not task:
        session.rollback()
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    session.commit()
    return task
# get all tasks
@app.get("/tasks",
         response_model=list[TaskResponse]
)
def all_tasks(session = Depends(get_session)):
    """Get all tasks."""
    taskflow = Taskflow(session)
    return taskflow.get_all_task()
