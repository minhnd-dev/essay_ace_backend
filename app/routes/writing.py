import json
from datetime import datetime

from flask import Blueprint
from openai import OpenAI

from app.database import Session
from app.models.feedback import Feedback
from app.models.response import Response
from app.schema.topic import WritingSchema, UpdateWritingSchema
from app.services.jwt_service import jwt_required
from app.services.validation_service import validate_body

write_bp = Blueprint('writing', __name__, url_prefix='/writing')

client = OpenAI()


@write_bp.route('/feedback', methods=['POST'])
@jwt_required
@validate_body(WritingSchema)
def feedback(body: WritingSchema, current_user):
    session = Session()
    writing_content = body.content
    response_id = body.response_id
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[

            {"role": "system",
             "content": f"Given this text: '{writing_content}'  Give me feed back on the content this "
                        f"text with the following questions: I'm interested in your feedback on "
                        f"this writing. What's your evaluation?, Can you provide feedback on "
                        f"grammar and language usage?Please evaluate based on IELTS scoring "
                        f"criteria. I want the result to be in JSON format"},
        ]
    )
    generated_review = completion.choices[-1].message.json()
    feedback_content = json.loads(generated_review)["content"]
    feedback = session.query(Feedback).filter_by(response_id=response_id).first()
    feedback.created_at = datetime.now()
    session.add(feedback)
    session.commit()
    feedback_data = {
        "user_id": current_user.id,
        "response_id": feedback.response_id,
        "content": json.loads(feedback_content),
    }
    return feedback_data


@write_bp.route("/update", methods=["PUT"])
@validate_body(UpdateWritingSchema)
def update(body: UpdateWritingSchema):
    session = Session()
    response_id = body.id
    new_content = body.content
    response = session.query(Response).filter_by(id=response_id).first()
    response.content = new_content
    response.updated_at = datetime.now()
    session.commit()
    return {"message": "Updated writing successfully"}, 200
