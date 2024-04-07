import json

from flask import Blueprint
from openai import OpenAI

from app.database import Session
from app.models.feedback import Feedback
from app.models.response import Response
from app.schema.feedback import FeedbackSchema, RewriteSchema
from app.services.jwt_service import jwt_required
from app.services.validation_service import validate_body

feedback_bp = Blueprint("feedback", __name__, url_prefix="/feedback")

client = OpenAI()


@feedback_bp.route("/detail", methods=["GET"])
@jwt_required
@validate_body(FeedbackSchema)
def detail(body: FeedbackSchema, current_user):
    session = Session()
    feedback = session.query(Feedback).filter_by(id=body.id).first()
    return {
        "content": feedback.content,
        "rewrite": feedback.rewrite,
        "user_id": current_user.id,
    }


@feedback_bp.route("/rewrite", methods=["POST"])
@jwt_required
@validate_body(RewriteSchema)
def rewrite_writing(body: RewriteSchema, current_user):
    session = Session()
    response_id = body.response_id
    response_content = session.query(Response).filter_by(id=response_id).first().content
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": f"Given this text: '{response_content}'  Give me a better article on this content "
             },
        ]
    )
    generated_rewrite = completion.choices[-1].message.json()
    new_content = json.loads(generated_rewrite)["content"]
    feedback = Feedback(response_id=response_id, rewrite=new_content)
    session.add(feedback)
    session.commit()
    response_data = {
        "id": current_user.id,
        "response_id": response_id,
        "rewrite": new_content
    }
    return response_data
