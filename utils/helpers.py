def validate_task_input(data):
    if not data.get("title"):
        return False
    return True
