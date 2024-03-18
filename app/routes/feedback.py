import os

import bcrypt
import jwt
from flask import Blueprint, request

from app.database import Session
from app.models.feedback import Feedback
from app.models.topic import Topic
from app.services.jwt_service import jwt_required

feedback_bp = Blueprint("feedback", __name__, url_prefix="/feedback")


@feedback_bp.route("/post_feedback", methods=["POST"])
@jwt_required
def post_feedbacks(current_user):
    session = Session()
    content = request.json.get("content")
    rewrite = request.json.get("rewrite")
    feedback = Feedback(content=content, rewrite=rewrite, user_id=current_user.id)

    session.add(feedback, rewrite)
    session.commit()
    return {
        "content": feedback.content,
        "rewrite": feedback.rewrite,
        "user_id": current_user.id,
    }
