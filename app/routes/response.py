import os

import bcrypt
import jwt
from flask import Blueprint, request

from app.database import Session
from app.models.response import Response
from app.models.topic import Topic
from app.services.jwt_service import jwt_required

response_bp = Blueprint("response", __name__, url_prefix="/response")


@response_bp.route("/detail", methods=["GET"])
@jwt_required
def detail(current_user):
    session = Session()
    topic_id = request.json.get("topic_id")
    response = session.query(Response).filter_by(topic_id=topic_id).first()
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
