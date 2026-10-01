from app import Taskflow


def task_create_cli():
        """Create a new task by collecting inputs and relying on Taskflow for validation."""
        while True:
                try:
                    task_id = int(input("Please enter the task ID: "))
                except ValueError:
                    print("Error: Please enter a valid whole number.")
                    continue

                task_title = input("Please enter the title: ")

                try:
                    obj.create_task( task_id,task_title)
                    print("Task created successfully!")
                    print("Current tasks:", obj.tasks)
                    break
                except ValueError as e:
                    print(f"Error: {e}")

def task_find_cli():
        """find task and return if exists"""
        while True:
                try:
                    task_id = int(input("Please enter the task ID: "))
                except ValueError:
                    print("Error: Please enter a valid whole number.")
                    continue

                try:
                    task = obj.find_task(task_id)
                    if task : 
                         print("Task Found successfully!")
                         print(task)
                         
                    else:
                         print("cannot Found Task")
                    break
                except ValueError as e:
                    print(f"Error: {e}")

def task_complete_cli():
        """change task complete state to true"""
        while True:
                try:
                    task_id = int(input("Please enter the task ID: "))
                except ValueError:
                    print("Error: Please enter a valid whole number.")
                    continue

                try:
                    if obj.complete_task(task_id):
                         print("Task completed successfully!")
                    else:
                          print("Task Completed Failed.")
                    
                    break
                except ValueError as e:
                    print(f"Error: {e}")

def task_update_cli():
        """update task"""
        while True:
                try:
                    task_id = int(input("Please enter the task ID: "))
                except ValueError:
                    print("Error: Please enter a valid whole number.")
                    continue
                task_title = input("Please enter the title: ")

                try:
                    task = obj.update_task(task_id,task_title)
                    if task : 
                        print("Task updated successfully!")
                        print(task)
                    else:
                          print("Task Update Failed.")                 
                    break
                except ValueError as e:
                    print(f"Error: {e}")

def task_delete_cli():
        """delete task"""
        while True:
                try:
                    task_id = int(input("Please enter the task ID: "))
                except ValueError:
                    print("Error: Please enter a valid whole number.")
                    continue
                try:
                    task = obj.delete_task(task_id)
                    if task : 
                        print("Task delete successfully!")
                    else:
                          print("Task Delete Failed.")                 
                    break
                except ValueError as e:
                    print(f"Error: {e}")



obj = Taskflow()
print("===== TaskFlow =====")
task_menu = ["Create task","Find task","Complete task","Update task","Delete task","Exit"]
for index,item in enumerate(task_menu,start=1):
        print(f"{index}. {item}")
while True:
    choice = input("choose: ")

    match choice:
        case "1":
            print("Executing: Create task...")
            task_create_cli()
            
        case "2":
            print("Executing: Find task...")
            task_find_cli()
            
        case "3":
            print("Executing: Complete task...")
            task_complete_cli()
            # Call obj.complete_task() here
            
        case "4":
            print("Executing: Update task...")
            task_update_cli()
            
        case "5":
            print("Executing: Delete task...")
            task_delete_cli()
            
        case "6":
            print("Goodbye!")
            break  # Exit the while loop
            
        case _:  # The wildcard case (acts like 'default' or 'else')
            print("Invalid choice! Please enter a number between 1 and 6.")