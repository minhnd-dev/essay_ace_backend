import os

import bcrypt
import jwt
from flask import Blueprint, request

from app.database import Session
from app.models.feedback import Feedback
from app.models.topic import Topic
from app.services.jwt_service import jwt_required

topic_bp = Blueprint("topic", __name__, url_prefix="/topic")


@topic_bp.route("/list", methods=["GET"])
@jwt_required
def get_topics(current_user):
    session = Session()
    limit = request.json.get("limit")
    offset = request.json.get("offset")
    query = (
        session.query(Topic)
        .filter_by(user_id=current_user.id)
        .order_by(Topic.created_at.desc())
    )
    topics = query.limit(limit).offset(offset).all()
    return {
        "data": [
            {
                "id": topic.id,
                "created_at": topic.created_at,
                "content": topic.content,
            }
            for topic in topics
        ],
        "total": query.count(),
    }
