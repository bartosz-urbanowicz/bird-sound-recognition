from flask import Blueprint, request

users_blueprint = Blueprint("users", __name__)

@users_blueprint.route('/login', methods=['POST'])
def log_in_route():
        return  201

@users_blueprint.route('/register', methods=['POST'])
def create_user_route():
        return 201
