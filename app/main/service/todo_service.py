from app.main import db
from app.main.model.todo import Todo
from app.main.model.user import User
from typing import Dict, Tuple
import datetime
import uuid


class TodoService:
    @staticmethod
    def get_all_todos() -> Tuple[Dict[str, any], int]:
        todos = Todo.query.all()
        if not todos:
            response_object = {
                'status': 'success',
                'message': 'No todos found.'
            }
            return response_object, 404

        todos_data = [{
            'id': todo.id,
            'user_id': todo.user_id,
            'description': todo.description,
            'created_at': todo.created_at
        } for todo in todos]

        response_object = {
            'status': 'success',
            'todos': todos_data
        }
        return response_object, 200

    @staticmethod
    def get_user_todos(user_id: int) -> Tuple[Dict[str, str], int]:
        user = User.query.get(user_id)
        if not user:
            response_object = {
                'status': 'fail',
                'message': 'User not found.'
            }
            return response_object, 404

        todos = [{'id': todo.id, 'user_id': todo.user_id, 'description': todo.description, 'created_at': todo.created_at}
                 for todo in user.todos]
        
        response_object = {
            'status': 'success',
            'todos': todos
        }
        return response_object, 200

    @staticmethod
    def create_todo(user_id: int, description: str) -> Tuple[Dict[str, str], int]:
        new_todo = Todo(
            user_id=user_id,
            description=description,
            created_at=datetime.datetime.utcnow()
        )
        TodoService._save_changes(new_todo)
        
        response_object = {
            'status': 'success',
            'message': 'Todo created successfully.',
            'todo': {
                'id': new_todo.id,
                'user_id': new_todo.user_id,
                'description': new_todo.description,
                'created_at': new_todo.created_at
            }
        }
        return response_object, 201

    @staticmethod
    def update_todo(user_id: int, todo_id: int, new_description: str) -> Tuple[Dict[str, str], int]:
        todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
        if not todo:
            response_object = {
                'status': 'fail',
                'message': 'Todo not found for the user.'
            }
            return response_object, 404
        
        todo.description = new_description
        TodoService._save_changes(todo)
        
        response_object = {
            'status': 'success',
            'message': 'Todo updated successfully.',
            'todo': {
                'id': todo.id,
                'user_id': todo.user_id,
                'description': todo.description,
                'created_at': todo.created_at
            }
        }
        return response_object, 200

    @staticmethod
    def delete_todo(user_id: int, todo_id: int) -> Tuple[Dict[str, str], int]:
        todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
        if not todo:
            response_object = {
                'status': 'fail',
                'message': 'Todo not found for the user.'
            }
            return response_object, 404
        
        db.session.delete(todo)
        db.session.commit()
        
        response_object = {
            'status': 'success',
            'message': 'Todo deleted successfully.'
        }
        return response_object, 200

    @staticmethod
    def _save_changes(data: Todo) -> None:
        db.session.add(data)
        db.session.commit()
