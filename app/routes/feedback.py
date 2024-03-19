import os

import bcrypt
import jwt
from flask import Blueprint, request

from app.database import Session
from app.models.feedback import Feedback
from app.models.topic import Topic
from app.schema.auth import AuthSchema
from app.schema.feedback import FeedbackSchema
from app.services.jwt_service import jwt_required
from app.services.validation_service import validate_body

feedback_bp = Blueprint("feedback", __name__, url_prefix="/feedback")


@feedback_bp.route("/post_feedback", methods=["POST"])
@jwt_required
@validate_body(FeedbackSchema)
def post_feedbacks(body: AuthSchema, current_user):
    session = Session()
    feedback = Feedback(content=body.content, rewrite=body.rewrite, user_id=current_user.id)

    session.add(feedback)
    session.commit()
    return {
        "content": feedback.content,
        "rewrite": feedback.rewrite,
        "user_id": current_user.id,
    }
