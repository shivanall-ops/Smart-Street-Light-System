def main():
    tasks = []
    
    while True:
        print("\n=== TO-DO LIST ===")
        print("1. Add task")
        print("2. View tasks")
        print("3. Delete task")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            task = input("Enter task: ")
            if task.strip():
                tasks.append(task)
                print(f"Task '{task}' added successfully!")
            else:
                print("Task cannot be empty!")
        
        elif choice == "2":
            if not tasks:
                print("\nNo tasks in the list.")
            else:
                print("\n=== YOUR TASKS ===")
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task}")
        
        elif choice == "3":
            if not tasks:
                print("\nNo tasks to delete.")
            else:
                print("\n=== YOUR TASKS ===")
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task}")
                
                try:
                    task_num = int(input("\nEnter task number to delete: "))
                    if 1 <= task_num <= len(tasks):
                        deleted_task = tasks.pop(task_num - 1)
                        print(f"Task '{deleted_task}' deleted successfully!")
                    else:
                        print("Invalid task number!")
                except ValueError:
                    print("Please enter a valid number!")
        
        elif choice == "4":
            print("\nGoodbye!")
            break
        
        else:
            print("Invalid choice! Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
