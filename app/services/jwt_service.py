import os

from dotenv import load_dotenv
from flask import request
import jwt

from app.database import Session
from app.models.user import User

load_dotenv()


def jwt_required(function):
    def inner_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Token is missing",
            }, 401
        
        try:
            data = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
            current_user = Session().query(User).where(User.user_name == data['user_name']).first()
            if not current_user:
                return {
                    "message": "User not found",
                }, 401
        except jwt.ExpiredSignatureError:
            return {
                "message": "Token is expired",
            }, 401
        except jwt.InvalidTokenError:
            return {
                "message": "Token is invalid",
            }, 401
        return function(current_user, *args, **kwargs)
    inner_function.__name__ = function.__name__
    return inner_function
