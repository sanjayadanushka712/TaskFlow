from fastapi import FastAPI, HTTPException
from app import Taskflow
from pydantic import BaseModel,Field

taskflow = Taskflow()
app = FastAPI()

class TaskCreate(BaseModel):
    task_id: int = Field(gt=0)
    title: str = Field(min_length=1)

class TaskUpdate(BaseModel):
    title: str = Field(min_length=1)

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
    "/create",
    status_code=201,
    response_model=TaskResponse,
    responses={409: {"description": "Task ID already exists"}}
)

def create_task(data: TaskCreate):
    try:
        task = taskflow.create_task(data.task_id, data.title)
        return task
    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )

# find task
@app.get(
    "/find/{task_id}",
    responses={404: {"description": "Task not found"}}
)
def find_task(task_id: int):
    task = taskflow.find_task(task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task

# complete task
@app.patch("/complete/{task_id}")
def complete_task(task_id: int):
    """Mark a task as completed."""
    success = taskflow.complete_task(task_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {"message": "Task completed successfully"}


# delete task
@app.delete("/delete/{task_id}")
def delete_task(task_id: int):
    """Delete a task by its ID."""
    success = taskflow.delete_task(task_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {"message": "Task deleted successfully"}

# update tasks
@app.put("/tasks/{task_id}")
def update_task(task_id: int, data: TaskUpdate):
    """Update a task title."""
    task = taskflow.update_task(task_id, data.title)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task