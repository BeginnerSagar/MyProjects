import json
import datetime
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

class Task:
    def __init__(self, title, description, due_date, priority, completed=False):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = completed
        self.creation_date = datetime.datetime.now()

class TodoList:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def edit_task(self, task, new_title, new_description, new_due_date, new_priority):
        task.title = new_title
        task.description = new_description
        task.due_date = new_due_date
        task.priority = new_priority

    def mark_task_completed(self, task):
        task.completed = True

    def mark_task_incomplete(self, task):
        task.completed = False

    def sort_tasks(self, key):
        self.tasks.sort(key=key)

    def filter_tasks(self, condition):
        return list(filter(condition, self.tasks))

    def export_to_json(self):
        data = {
            "name": self.name,
            "tasks": [
                {
                    "title": task.title,
                    "description": task.description,
                    "due_date": task.due_date.strftime("%Y-%m-%d") if task.due_date else None,
                    "priority": task.priority,
                    "completed": task.completed,
                    "creation_date": task.creation_date.strftime("%Y-%m-%d %H:%M:%S")
                }
                for task in self.tasks
            ]
        }
        return json.dumps(data, indent=2)

    def import_from_json(self, json_data):
        data = json.loads(json_data)
        self.name = data["name"]
        self.tasks = []
        for task_data in data["tasks"]:
            due_date = datetime.datetime.strptime(task_data["due_date"], "%Y-%m-%d") if task_data["due_date"] else None
            creation_date = datetime.datetime.strptime(task_data["creation_date"], "%Y-%m-%d %H:%M:%S")
            task = Task(
                title=task_data["title"],
                description=task_data["description"],
                due_date=due_date,
                priority=task_data["priority"],
                completed=task_data["completed"]
            )
            task.creation_date = creation_date
            self.tasks.append(task)

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List App")

        # Adding a bit of color
        self.root.configure(bg='#f0f0f0')  # Background color

        self.style = ttk.Style()
        self.style.configure('TButton', foreground='black', background='#4A766E')  # Metallic green color

        self.todo_list = TodoList("My Todo List")

        self.task_tree = ttk.Treeview(
            root,
            columns=("Title", "Due Date", "Priority", "Completed"),
            show="headings",
            selectmode="browse"
        )

        # Header colors
        self.task_tree.heading("Title", text="Title", anchor="w")
        self.task_tree.heading("Due Date", text="Due Date", anchor="w")
        self.task_tree.heading("Priority", text="Priority", anchor="w")
        self.task_tree.heading("Completed", text="Completed", anchor="w")

        # Column colors
        self.task_tree.column("Title", width=200, anchor="w")
        self.task_tree.column("Due Date", width=100, anchor="w")
        self.task_tree.column("Priority", width=100, anchor="w")
        self.task_tree.column("Completed", width=100, anchor="w")

        self.load_tasks()

        self.task_tree.pack(pady=10)

        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10)

        add_btn = ttk.Button(btn_frame, text="Add Task", command=self.add_task, style='TButton')
        remove_btn = ttk.Button(btn_frame, text="Remove Task", command=self.remove_task, style='TButton')
        edit_btn = ttk.Button(btn_frame, text="Edit Task", command=self.edit_task, style='TButton')
        complete_btn = ttk.Button(btn_frame, text="Mark Complete", command=self.mark_complete, style='TButton')
        incomplete_btn = ttk.Button(btn_frame, text="Mark Incomplete", command=self.mark_incomplete, style='TButton')
        save_btn = ttk.Button(btn_frame, text="Save to JSON", command=self.save_to_json, style='TButton')
        load_btn = ttk.Button(btn_frame, text="Load from JSON", command=self.load_from_json, style='TButton')

        add_btn.grid(row=0, column=0, padx=5)
        remove_btn.grid(row=0, column=1, padx=5)
        edit_btn.grid(row=0, column=2, padx=5)
        complete_btn.grid(row=0, column=3, padx=5)
        incomplete_btn.grid(row=0, column=4, padx=5)
        save_btn.grid(row=0, column=5, padx=5)
        load_btn.grid(row=0, column=6, padx=5)

    def add_task(self):
        title = self.get_input("Enter task title")
        if title is not None:  # Check if the user canceled the input
            description = self.get_input("Enter task description")
            due_date = self.get_input("Enter due date (YYYY-MM-DD)")
            priority = self.get_input("Enter priority (1: Low, 2: Medium, 3: High)")

            # Check if the user canceled the input for priority
            if priority is not None:
                priority = int(priority)

            due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d") if due_date else None

            task = Task(title, description, due_date, priority)
            self.todo_list.add_task(task)

            self.update_task_tree()

    def remove_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            title = self.task_tree.item(selected_item, "values")[0]
            tasks_to_remove = [task for task in self.todo_list.tasks if task.title == title]
            for task in tasks_to_remove:
                self.todo_list.remove_task(task)

            self.update_task_tree()
        else:
            messagebox.showinfo("Error", "Select a task to remove.")

    def edit_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            title = self.task_tree.item(selected_item, "values")[0]
            task_to_edit = next((task for task in self.todo_list.tasks if task.title == title), None)

            if task_to_edit:
                new_title = self.get_input(f"Enter new title for '{task_to_edit.title}'")
                if new_title is not None:  # Check if the user canceled the input
                    new_description = self.get_input(f"Enter new description for '{task_to_edit.title}'")
                    new_due_date = self.get_input(f"Enter new due date for '{task_to_edit.title}' (YYYY-MM-DD)")
                    new_priority = self.get_input(f"Enter new priority for '{task_to_edit.title}' (1: Low, 2: Medium, 3: High)")

                    # Check if the user canceled the input for priority
                    if new_priority is not None:
                        new_priority = int(new_priority)

                    new_due_date = datetime.datetime.strptime(new_due_date, "%Y-%m-%d") if new_due_date else None

                    self.todo_list.edit_task(task_to_edit, new_title, new_description, new_due_date, new_priority)

                    self.update_task_tree()
            else:
                messagebox.showinfo("Error", f"No task found with title '{title}'.")
        else:
            messagebox.showinfo("Error", "Select a task to edit.")

    def mark_complete(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            title = self.task_tree.item(selected_item, "values")[0]
            tasks_to_mark_completed = [task for task in self.todo_list.tasks if task.title == title]
            for task in tasks_to_mark_completed:
                self.todo_list.mark_task_completed(task)

            self.update_task_tree()
        else:
            messagebox.showinfo("Error", "Select a task to mark as complete.")

    def mark_incomplete(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            title = self.task_tree.item(selected_item, "values")[0]
            tasks_to_mark_incomplete = [task for task in self.todo_list.tasks if task.title == title]
            for task in tasks_to_mark_incomplete:
                self.todo_list.mark_task_incomplete(task)

            self.update_task_tree()
        else:
            messagebox.showinfo("Error", "Select a task to mark as incomplete.")

    def save_to_json(self):
        json_data = self.todo_list.export_to_json()
        with open("todo_list.json", "w") as file:
            file.write(json_data)
        messagebox.showinfo("Info", "Todo list exported to 'todo_list.json'.")

    def load_from_json(self):
        try:
            with open("todo_list.json", "r") as file:
                json_data = file.read()
            self.todo_list.import_from_json(json_data)
            self.update_task_tree()
            messagebox.showinfo("Info", "Todo list imported from 'todo_list.json'.")
        except FileNotFoundError:
            messagebox.showinfo("Error", "No 'todo_list.json' file found.")

    def load_tasks(self):
        for task in self.todo_list.tasks:
            self.task_tree.insert("", "end", values=(task.title, task.due_date, task.priority, task.completed))

    def update_task_tree(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        self.load_tasks()

    def get_input(self, prompt):
        return simpledialog.askstring("Input", prompt)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()
