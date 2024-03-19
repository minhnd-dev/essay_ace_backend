import os

import bcrypt
import jwt
from flask import Blueprint, request

from app.database import Session
from app.models.feedback import Feedback
from app.models.topic import Topic
from app.schema.auth import AuthSchema
from app.schema.topic import TopicSchema
from app.services.jwt_service import jwt_required
from app.services.validation_service import validate_body

topic_bp = Blueprint("topic", __name__, url_prefix="/topic")


@topic_bp.route("/list", methods=["GET"])
@jwt_required
@validate_body(TopicSchema)
def get_topics(current_user, body: AuthSchema):
    session = Session()
    query = (
        session.query(Topic)
        .filter_by(user_id=current_user.id)
        .order_by(Topic.created_at.desc())
    )
    topics = query.limit(body.limit).offset(body.offset).all()
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
