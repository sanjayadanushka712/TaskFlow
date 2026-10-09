from database import SessionLocal 
from app import Taskflow

def get_task_id():
    while True:
        try:
            return int(input("Please enter the task ID: "))
        except ValueError:
            print("Error: Please enter a valid whole number.")


def task_create_cli():
        """Create a new task by collecting inputs and relying on Taskflow for validation."""
        while True:           
                task_id = get_task_id()

                task_title = input("Please enter the title: ")

                try:
                    task = obj.create_task(task_id,task_title)
                    if task :
                        obj.session.commit() 
                        print("Task created successfully!")
                        display_task(task)   
                        break
                except ValueError as e:
                    print(f"Error: {e}")

def task_find_cli():
        """find task and return if exists"""

        task_id = get_task_id()

        task = obj.find_task(task_id)
        if task: 
            print(" Task found successfully!")
            display_task(task)               
        else:
            print("cannot Found Task")



def task_complete_cli():
        """change task complete state to true"""

        task_id = get_task_id()

        task = obj.complete_task(task_id)
        if task:
            print("Task completed successfully!")
            obj.session.commit()
        else:
            print("Task Completed Failed.")


def task_update_cli():
        """update task"""

        task_id = get_task_id()

        task_title = input("Please enter the title: ")

        task = obj.update_task(task_id,task_title)
        if task: 
            display_task(task)
            obj.session.commit()
        else:
            print("Task Update Failed.")  
             

def task_delete_cli():
        """delete task"""

        task_id = get_task_id()

        task = obj.delete_task(task_id)
        if task: 
            print("Task delete successfully!")
            obj.session.commit()
        else:
            print("Task Delete Failed.")  

def task_show_tasks_cli():
    """Get and display all tasks in a clean table format.""" 
    tasks = obj.get_all_task()  
    if not tasks: 
        print("\n--- No tasks found. ---")
        return
    display_tasks(tasks)


def display_task(task):
    status = "Done" if task.get('completed') else "Pending"

    print("-" * 35)
    print(f"{'Task ID:':<12} {task.get('id')}")
    print(f"{'Title:':<12} {task.get('title')}")
    print(f"{'Status:':<12} {status}")
    print("-" * 35 + "\n")

def display_tasks(tasks):
    print(f"\n{'ID':<5} | {'Title':<20} | {'Status':<10}")
    print("-" * 40)

    for task in tasks:
        status = "Done" if task['completed'] else "Pending"
        print(f"{task['id']:<5} | {task['title']:<20} | {status:<10}")

    print()

def main():
       
        task_menu = ["Create task","Show tasks","Find task","Complete task","Update task","Delete task","Exit"]

        while True:
            print("===== TaskFlow =====")

            for index,item in enumerate(task_menu,start=1):
                print(f"{index}. {item}")
            
            choice = input("choose: ")

            try:
                choice = int(choice)
            except ValueError:
                print("Invalid choice! Please enter a number.")
                continue


            match choice:
                case 1:
                    print("Executing: Create task...")
                    task_create_cli()
                
                case 2:
                    print("Executing: Show tasks...")
                    task_show_tasks_cli()
                
                case 3:
                    print("Executing: Find task...")
                    task_find_cli()
                    
                case 4:
                    print("Executing: Complete task...")
                    task_complete_cli()
                    
                case 5:
                    print("Executing: Update task...")
                    task_update_cli()
                    
                case 6:
                    print("Executing: Delete task...")
                    task_delete_cli()
                    
                case 7:
                    print("Goodbye!")
                    break  # Exit the while loop
                    
                case _:  # The wildcard case (acts like 'default' or 'else')
                    print("Invalid choice! Please enter a number between 1 and 7.")

if __name__ == "__main__":
    with SessionLocal() as session:
        obj = Taskflow(session)
        main()


