from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt

from auth.model import User, UserRole
from db import db

bcrypt = Bcrypt()

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "USER")

    if not username or not password:
        return {
            'error_message': 'username dan password tidak boleh kosong'
        }, 400

    try:
        # Check if the username is already taken
        existing_user = db.session.query(User).filter_by(username=username).first()
        if existing_user:
            return {
                'error_message': 'username sudah digunakan'
            }, 400

        new_user = User(username=username, role=UserRole[role])
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return {
            'user_id': new_user.id,
            'username': new_user.username,
            'role': new_user.role.value
        }

    except Exception as error:
        return {
            'error_message': str(error)
        }, 500

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {
            'error_message': 'username atau password tidak boleh kosong'
        }, 400

    try:
        user = db.session.query(User).filter_by(username=username).first()

        if user and user.check_password(password):
            # Use Flask-JWT-Extended to generate a token
            access_token = create_access_token(identity=user.id)
            return {
                'token': access_token,
                'username': user.username,
                'role': user.role.value
            }, 200
        else:
            return {
                'error_message': 'username atau password tidak tepat'
            }, 401

    except Exception as error:
        return {
            'error_message': str(error)
        }, 500
