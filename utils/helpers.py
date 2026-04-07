def generate_id(tasks):
    if not tasks:
        return 1
    return max(t.id for t in tasks) + 1


def validate_task_input(data):
    if not data.get("title"):
        return False
    return True
