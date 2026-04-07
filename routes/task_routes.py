from flask import Blueprint, request, jsonify
from models.APIClient import TaskManager
from models.FileHandler import FileHandler
from utils.helpers import validate_task_input
from config import JSON_FILE_PATH, CSV_FILE_PATH

task_bp = Blueprint("tasks", __name__)

file_handler = FileHandler(JSON_FILE_PATH, CSV_FILE_PATH)
manager = TaskManager(file_handler)
manager.load_tasks()


@task_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not validate_task_input(data):
        return jsonify({"error": "Title is required"}), 400
    task = manager.add_task(data["title"], data.get("priority", "Medium"))
    return jsonify(task), 201


@task_bp.route("/tasks", methods=["GET"])
def get_all_tasks():
    return jsonify(manager.get_all_tasks()), 200


@task_bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = manager.get_task_by_id(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200


@task_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    task = manager.update_task(task_id, data)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200


@task_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    deleted = manager.delete_task(task_id)
    if not deleted:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task deleted"}), 200
