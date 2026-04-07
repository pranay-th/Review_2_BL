class Task:
    def __init__(self, task_id, title, priority="Medium", status="Pending"):
        self.id = task_id
        self.title = title
        self.priority = priority
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        return Task(
            task_id=data["id"],
            title=data["title"],
            priority=data.get("priority", "Medium"),
            status=data.get("status", "Pending")
        )

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title!r}, priority={self.priority}, status={self.status})"
