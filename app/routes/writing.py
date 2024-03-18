import os

import bcrypt
import jwt
from flask import Blueprint, request

from app.database import Session
from app.models.topic import Topic
from app.services.jwt_service import jwt_required

write_bp = Blueprint('write', __name__, url_prefix='/write')


@write_bp.route('/topic', methods=['POST'])
@jwt_required
def post_topics(current_user):
    session = Session()

    content = request.json.get("content")
    topic = Topic(content=content, user_id=current_user.id)
    session.add(topic)
    session.commit()
    return {
        "user_id": current_user.id,
        "content": topic.content
    }

