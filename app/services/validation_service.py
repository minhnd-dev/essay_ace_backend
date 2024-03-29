import json

from flask import request, jsonify
from pydantic import BaseModel, ValidationError


def validate_body(schema: type[BaseModel]) -> callable:
    def decorator(function: callable):
        def inner_function(*args, **kwargs):
            try:
                body = schema(**request.get_json())
                return function(body, *args, **kwargs)
            except ValidationError as e:
                return jsonify({"error": json.loads(e.json())}), 400

        inner_function.__name__ = function.__name__
        return inner_function

    return decorator


def validate_params(schema: type[BaseModel]) -> callable:
    def decorator(function: callable):
        def inner_function(*args, **kwargs):
            try:
                params = schema(**request.args.to_dict())
                return function(params, *args, **kwargs)
            except ValidationError as e:
                return jsonify({"error": json.loads(e.json())}), 400

        return inner_function

    return decorator
