import os

import bcrypt
import jwt
from flask import Blueprint, request

from app.database import Session
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    session = Session()

    user_name = request.json.get("user_name", None)
    password = request.json.get("password", None)
    if not user_name:
        return "Missing user_name", 400
    if not password:
        return "Missing password", 400

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user = User(user_name=user_name, password=hashed)

    session.add(user)
    session.commit()
    return {
        "user_id": user.id,
        "user_name": user.user_name
    }


@auth_bp.route('/login', methods=['POST'])
def login():
    session = Session()

    user_name = request.json.get("user_name", None)
    password = request.json.get("password", None)
    if not user_name:
        return "Missing user_name", 400
    if not password:
        return "Missing password", 400

    user = session.query(User).filter_by(user_name=user_name).first()

    if not user:
        return {
            "message": "User not found"
        }, 401

    if bcrypt.checkpw(password.encode('utf-8'), user.password):
        token = jwt.encode(
            {
                "user_name": user.user_name,
            },
            os.getenv("SECRET_KEY"),
            algorithm="HS256"
        )
        return {
            "user_id": user.id,
            "user_name": user.user_name,
            "token": token
        }
    else:
        return {
            "message": "Wrong password",
        }, 401
