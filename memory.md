<!-- # what i learned
So we should also test the boundary value 0:

def test_create_task_zero_id():
    with pytest.raises(ValueError):
        create_task("Learn Python", 0)

That's a useful testing habit:

Requirement: ID > 0

-1  → invalid
 0  → invalid   ← boundary
 1  → valid     ← boundary

This is called boundary-value testing. You'll use this kind of thinking constantly in real software. -->

<!-- self .task -->


<!-- class Taskflow():
    def __init__(self):
        self.tasks = []

    def create_task(self,title, task_id):
        """ensure function title is not empty
        and task id greater than 0 and add to tasks"""
    
        if not title or not title.strip():
             raise ValueError("title must not be empty")
        if task_id<= 0:
            raise ValueError("task_id must be a positive integer")

        self.tasks.append({ "id": task_id,"title": title, "completed": False})

    def find_task(self, task_id):
        """find the task with given id"""
        for task in self.tasks:
            if task["id"] == task_id:
             return task
        return None

    def complete_task(self, task_id):
        """complete the task with given id"""
        task = self.find_task(task_id)
        if task:
            task["completed"] = True

obj = Taskflow()
obj.create_task("Learn Docker ",1)
# print(obj.tasks)
findTask = obj.find_task(1)
print(findTask)

obj.complete_task(1)
print(obj.tasks) -->
