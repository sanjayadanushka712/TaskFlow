class Taskflow():
    def __init__(self):
        self.tasks = []

    def create_task(self, task_id,title):
        """ensure function title is not empty
        and task id greater than 0 and add to tasks"""

        if not isinstance(task_id, int):
            raise TypeError("task_id must be an integer")
        if not title or not title.strip():
             raise ValueError("title must not be empty")
        if task_id<= 0:
            raise ValueError("task_id must be a positive integer")
        if self.find_task(task_id): #check if task_id
            raise ValueError("task_id Already exist")
            
        task = { "id": task_id,"title": title, "completed": False}
        self.tasks.append(task)
        return task


    def find_task(self, task_id):
        """find the task with given id"""
        for task in self.tasks:
            if task["id"] == task_id:
             return task
        return False

    def complete_task(self, task_id):
        """complete the task with given id"""
        task = self.find_task(task_id)
        if task:
            task["completed"] = True
            return True
        return False

    def delete_task(self, task_id):
        """delete the task with given id"""
        task = self.find_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        
        return False

    def update_task(self,task_id, title):
        """ update the task title with given id"""
        if not title or not title.strip():
                     raise ValueError("title must not be empty")
        task = self.find_task(task_id)
        if task:
             task["title"] = title.strip()
             return task
        return False
       

        

                 


