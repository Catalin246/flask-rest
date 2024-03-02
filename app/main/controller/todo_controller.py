from flask import request
from flask_restx import Resource

from app.main.util.decorator import user_logged
from app.main.util.dto import TodoDto
from app.main.service.todo_service import TodoService
from typing import Dict, Tuple

api = TodoDto.api
_todo = TodoDto.todo


@api.route('/')
class UserTodoList(Resource):
    @api.doc('get todos of the logged-in user')
    @user_logged
    @api.marshal_list_with(_todo, envelope='data')
    def get(self, user_id):
        """Get all todos of the logged-in user"""
        return TodoService.get_user_todos(user_id)

    @api.doc('create a todo for the logged-in user')
    @user_logged
    @api.expect(_todo, validate=True)
    @api.response(201, 'Todo successfully created.')
    def post(self, user_id):
        """Create a new todo for the logged-in user"""
        data = request.json
        return TodoService.create_todo(user_id, data['description'])

@api.route('/<int:todo_id>')
class UserTodo(Resource):
    @api.doc('update a todo of the logged-in user')
    @user_logged
    @api.expect(_todo, validate=True)
    @api.response(200, 'Todo successfully updated.')
    def put(self, user, todo_id):
        """Update a todo of the logged-in user"""
        data = request.json
        return TodoService.update_todo(user.id, todo_id, data['description'])

    @api.doc('delete a todo of the logged-in user')
    @user_logged
    @api.response(204, 'Todo successfully deleted.')
    def delete(self, user, todo_id):
        """Delete a todo of the logged-in user"""
        return TodoService.delete_todo(user.id, todo_id)


@api.route('/todos')
class AdminTodoList(Resource):
    @api.doc('get all todos (admin only)')
    #@admin_token_required
    @api.marshal_list_with(_todo, envelope='data')
    def get(self):
        """Get all todos"""
        return TodoService.get_all_todos()
