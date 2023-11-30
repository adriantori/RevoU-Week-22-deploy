from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from datetime import datetime

from db import db
from todo.model import Todo
from auth.model import User, UserRole

bcrypt = Bcrypt()

todo_blueprint = Blueprint('todo', __name__)

@todo_blueprint.route('/create', methods=['POST'])
@jwt_required()
def create_todo():
    data = request.get_json()
    todo_task = data.get("todoTask")
    todo_priority = data.get("todoPriority")
    todo_due = data.get("todoDue")

    user_id = get_jwt_identity()

    try:
        todo = Todo(
            task=todo_task,
            priority=todo_priority,
            due=datetime.strptime(todo_due, '%d/%m/%Y'),
            user_id=user_id
        )

        db.session.add(todo)
        db.session.commit()

        return jsonify({
            'message': 'ToDo created successfully',
            'data': {
                'id': todo.id,
                'task': todo.task,
                'priority': todo.priority.value,
                'due': todo.due.strftime('%d/%m/%Y'),
            }
        }), 201
    except Exception as error:
        return jsonify({'error_message': f'Error creating ToDo: {str(error)}'}), 500

@todo_blueprint.route('/retrieve', methods=['GET'])
@jwt_required()
def get_todo():
    user_id = get_jwt_identity()

    try:
        user = User.query.filter_by(id=user_id).first()

        if not user:
            return jsonify({'error_message': 'User not found'}), 404

        if user.role == UserRole.USER:
            todos = Todo.query.filter_by(user_id=user_id, is_deleted=False).all()
        elif user.role == UserRole.ADMIN:
            todos = Todo.query.filter_by(is_deleted=False).all()
        else:
            return jsonify({'error_message': 'Invalid role'}), 400

        todos_data = [
            {
                'id': todo.id,
                'task': todo.task,
                'priority': todo.priority.value,
                'due': todo.due.strftime('%d/%m/%Y'),
                'user_id': todo.user_id,
            } for todo in todos
        ]

        return jsonify({'message': 'ToDos retrieved successfully', 'data': todos_data}), 200
    except Exception as error:
        return jsonify({'error_message': f'Error retrieving ToDos: {str(error)}'}), 500


@todo_blueprint.route('/update/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    data = request.get_json()
    todo_task = data.get("todoTask")
    todo_priority = data.get("todoPriority")
    todo_due = data.get("todoDue")

    user_id = get_jwt_identity()
    print("User ID:", user_id)


    try:
        todo = Todo.query.filter_by(id=todo_id).first()

        if not todo:
            return jsonify({'error_message': 'ToDo not found'}), 404

        if todo.user_id != user_id:
            return jsonify({'error_message': 'You are not authorized to update this ToDo'}), 403

        todo.task = todo_task
        todo.priority = todo_priority
        todo.due = datetime.strptime(todo_due, '%d/%m/%Y')

        db.session.commit()

        return jsonify({
            'message': 'ToDo updated successfully',
            'data': {
                'id': todo.id,
                'task': todo.task,
                'priority': todo.priority.value,
                'due': todo.due,
            }
        }), 200
    except Exception as error:
        return jsonify({'error_message': f'Error updating ToDo: {str(error)}'}), 500

@todo_blueprint.route('/delete/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    user_id = get_jwt_identity()

    try:
        todo = Todo.query.filter_by(id=todo_id).first()

        if not todo:
            return jsonify({'error_message': 'ToDo not found'}), 404

        if todo.user_id != user_id:
            return jsonify({'error_message': 'You are not authorized to delete this ToDo'}), 403

        if todo.is_deleted:
            return jsonify({'error_message': 'ToDo already deleted'}), 400

        todo.is_deleted = True
        db.session.commit()

        return jsonify({
            'message': 'ToDo deleted successfully',
            'data': {
                'id': todo.id,
                'task': todo.task,
                'priority': todo.priority.value,
                'due': todo.due,
            }
        }), 200
    except Exception as error:
        return jsonify({'error_message': f'Error deleting ToDo: {str(error)}'}), 500
