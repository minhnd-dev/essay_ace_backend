import os

import bcrypt
import jwt
from flask import Blueprint, request

from app.database import Session
from app.models.response import Response
from app.models.topic import Topic
from app.schema.auth import AuthSchema
from app.schema.response import ResponseSchema
from app.services.jwt_service import jwt_required
from app.services.validation_service import validate_body

response_bp = Blueprint("response", __name__, url_prefix="/response")


@response_bp.route("/detail", methods=["GET"])
@jwt_required
@validate_body(ResponseSchema)
def detail(current_user, body: AuthSchema):
    session = Session()
    response = session.query(Response).filter_by(topic_id=body.topic_id).first()
    if not response:
        return {"message": "Not found topic"}
    else:
        return {
            "data": {
                "id": response.id,
                "content": response.content,
                "feedback": response.feedback,
            }
        }
