from Task import Task

class Course:
    """
    A class to represent a course
    """
    name: str
    tasks: list[Task]

    def __init__(self, name: str):
        self.name = name
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def get_tasks(self):
        return self.tasks

    def get_name(self):
        return self.name

    def get_tasks_by_date(self, date: str):
        return [task for task in self.tasks if task.get_date() == date]

    def get_tasks_by_label(self, label: str):
        return [task for task in self.tasks if label in task.get_labels()]
    
    def get_tasks_by_priority(self, priority: str):
        return [task for task in self.tasks if task.get_priority() == priority]
    
    def get_tasks_by_status(self, status: str):
        return [task for task in self.tasks if task.get_status() == status]