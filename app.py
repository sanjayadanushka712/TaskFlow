from models import Task
from sqlalchemy import select


class Taskflow():
    def __init__(self, session):
        self.session = session

    def _get_task_obj(self,task_id):
        """Helper to fetch the raw database object inside an active session"""
        return self.session.get(Task, task_id)


    def create_task(self, task_id,title):
        """ensure function title is not empty
        and task id greater than 0 and add to tasks"""

        if not isinstance(task_id, int):
            raise TypeError("task_id must be an integer")
        if not title or not title.strip():
            raise ValueError("title must not be empty")
        if task_id<= 0:
            raise ValueError("task_id must be a positive integer")
        if self._get_task_obj( task_id):
            raise ValueError("task_id Already exist")
            
        task = Task(
            id=task_id,
            title=title,
            completed=False
            )
        self.session.add(task)
        self.session.flush()
        return {
                "id": task.id, 
                "title": task.title, 
                "completed": task.completed 
        }


    def get_all_task(self):
        """Fetch every task from the database"""

        # 1. Query all records from the Task table
        statement = select(Task).order_by(Task.id) 
        tasks = self.session.scalars(statement).all()
        
        # 2. Convert the list of database objects into a list of dictionaries
        return [
            {
                "id": task.id,
                "title": task.title,
                "completed": task.completed
            }
            for task in tasks
        ]



    def find_task(self, task_id):
        """find the task with given id"""

        task =  self._get_task_obj(task_id)
        if  task is None:
            return None
        return {
                "id": task.id, 
                "title": task.title, 
                "completed": task.completed 
                }

    def complete_task(self, task_id):
        """complete the task with given id"""

        task = self._get_task_obj( task_id)
        if task:
            task.completed = True 
            self.session.flush()
            return True
        return False       

    def delete_task(self, task_id):
        """delete the task with given id"""

        task = self._get_task_obj( task_id)
        if task:
                self.session.delete(task)
                self.session.flush()
                return True
        return False   

    def update_task(self,task_id, title):
        """ update the task title with given id"""
        if not title or not title.strip():
                     raise ValueError("title must not be empty")
        task = self._get_task_obj( task_id)
        if task:
                task.title= title.strip()
                self.session.flush()
                return {
                "id": task.id, 
                "title": task.title, 
                "completed": task.completed 
                }

        return False 

