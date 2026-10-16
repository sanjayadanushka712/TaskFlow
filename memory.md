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



<!-- Lesson 3: HTTP methods have different responsibilities
One important concept in API engineering is idempotency.
An operation is idempotent if repeating the same request produces the same intended final state as making it once.
Method Usually idempotent? Example
GET Yes Reading task 10 repeatedly doesn't change it.
POST No Repeating a creation request might create duplicates or return a conflict.
PUT Yes Setting a task's title to "Learn Python" repeatedly leaves the same title.
PATCH Depends Setting completed = true repeatedly leaves it true.
DELETE Yes, in terms of final state After repeated deletion requests, the task remains absent, although responses may differ.
Notice that PATCH is not automatically non-idempotent. It depends on the operation. Your complete_task() sets a Boolean to True, so repeating it leaves the same final state. -->



<!-- 200

OK
The request succeeded. For example, retrieving an existing task.

201

Created
A resource was created successfully. Your POST /tasks endpoint uses this.

404

Not Found
The requested resource doesn't exist. Your API returns this when a task ID cannot be found.

409

Conflict
The request conflicts with existing data, such as attempting to create a task with a duplicate ID.

422

Unprocessable Content
The request reached FastAPI, but its data failed validation. For example, submitting a title containing only spaces. -->

<!-- Lesson: What is a race condition?
Imagine two requests arrive with the same idempotency key, task-create-001, almost simultaneously.
Request A

Request B

Both look up the same key.
Neither finds a record yet.

Request A creates task and record.

Request B also tries to create them.

The conflict
PostgreSQL's unique constraint prevents both requests from inserting the same idempotency key. But your application must handle that conflict and return the correct response instead of an unexpected server error. -->

<!-- 
First, distinguish these three concepts

Concurrency
Multiple tasks make progress during overlapping periods. Their execution may be interleaved rather than occurring strictly one after another.

Parallelism
Multiple tasks execute at the same instant, such as on separate CPU cores.

Synchronization
Mechanisms that coordinate competing tasks so shared state remains correct. -->



<!-- Lesson 1 — 7 terminal tricks worth remembering

1. Repeat a previous command
!!

Runs your last command again. Useful when you mistype something, but check what the command does before repeating it.

1. Search command history
Press Ctrl + R, then type part of a previous command, such as pytest. Press Enter to run the selected command.

2. Autocomplete paths and commands
Type pyte and press Tab. Your shell may complete it to pytest if the command is available. If there are multiple matches, press Tab again to see options.

3. Jump to the previous directory
cd -

Switches back to the previous working directory.

1. Go straight home
cd ~

Or simply run cd with no arguments.

1. Show readable file sizes
ls -lh

The -h option displays sizes in units like KB and MB, rather than just bytes.

1. Check your Git changes quickly
git status --short

In your TaskFlow repo, this shows modified and untracked files without a long explanation. -->
