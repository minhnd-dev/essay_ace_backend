import json
import os
import openai
import bcrypt
import jwt
from flask import Blueprint, request, jsonify
from openai import OpenAI

from app.database import Session
from app.models.topic import Topic
from app.schema.auth import AuthSchema
from app.schema.topic import TopicSchema, WritingSchema
from app.services.jwt_service import jwt_required
from app.services.validation_service import validate_body

write_bp = Blueprint('write', __name__, url_prefix='/write')

client = OpenAI()


@write_bp.route('/topic', methods=['POST'])
@jwt_required
@validate_body(WritingSchema)
def post_topics(body: AuthSchema, current_user):
    session = Session()
    topic = Topic(content=body.content, user_id=current_user.id)
    session.add(topic)
    session.commit()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[

            {"role": "system", "content": f"Given this text: '{body.content}'  Give me feed back on the content this "
                                          f"text with the following questions: I'm interested in your feedback on "
                                          f"this writing. What's your evaluation?, Can you provide feedback on "
                                          f"grammar and language usage?Please evaluate based on IELTS scoring "
                                          f"criteria. I want the result to be in JSON format"},
        ]
    )
    generated_review = completion.choices[-1].message.json()
    response_data = {
        "user_id": current_user.id,
        "content": body.content,
        "generated_review": json.loads(json.loads(generated_review)["content"])
    }

    return response_data
