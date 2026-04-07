from models.Task import Task


class TaskManager:
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.tasks = []

    def load_tasks(self):
        data = self.file_handler.read_json()
        self.tasks = [Task.from_dict(item) for item in data]

    def get_all_tasks(self):
        return [task.to_dict() for task in self.tasks]

    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task.to_dict()
        return None

    def add_task(self, title, priority="Medium"):
        new_id = max((t.id for t in self.tasks), default=0) + 1
        task = Task(task_id=new_id, title=title, priority=priority)
        self.tasks.append(task)
        self.save_tasks()
        return task.to_dict()

    def update_task(self, task_id, updates):
        for task in self.tasks:
            if task.id == task_id:
                if "title" in updates:
                    task.title = updates["title"]
                if "priority" in updates:
                    task.priority = updates["priority"]
                if "status" in updates:
                    task.status = updates["status"]
                self.save_tasks()
                return task.to_dict()
        return None

    def delete_task(self, task_id):
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks.pop(i)
                self.save_tasks()
                return True
        return False

    def save_tasks(self):
        self.file_handler.write_json(self.tasks)
        self.file_handler.write_csv(self.tasks)

    def filter_completed_tasks(self):
        return [task.to_dict() for task in self.tasks if task.status == "Completed"]
