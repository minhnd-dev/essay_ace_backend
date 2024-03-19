import os

import bcrypt
import jwt
from flask import Blueprint, request

from app.database import Session
from app.models.topic import Topic
from app.schema.auth import AuthSchema
from app.schema.topic import TopicSchema
from app.services.jwt_service import jwt_required
from app.services.validation_service import validate_body

write_bp = Blueprint('write', __name__, url_prefix='/write')


@write_bp.route('/topic', methods=['POST'])
@jwt_required
@validate_body(TopicSchema)
def post_topics(current_user, body: AuthSchema):
    session = Session()
    topic = Topic(content=body.content, user_id=current_user.id)
    session.add(topic)
    session.commit()
    return {
        "user_id": current_user.id,
        "content": topic.content
    }

