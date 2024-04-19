from datetime import datetime

from flask import Blueprint

from app.database import Session
from app.models.response import Response
from app.models.topic import Topic
from app.schema.response import ResponseSchema, SaveResponseSchema, ListWritingSchema
from app.services.jwt_service import jwt_required
from app.services.validation_service import validate_body

response_bp = Blueprint("response", __name__, url_prefix="/response")


@response_bp.route("", methods=["POST"])
@jwt_required
@validate_body(SaveResponseSchema)
def save(body: SaveResponseSchema, current_user):
    session = Session()

    topic = (
        session.query(Topic)
        .filter(Topic.id == body.topic_id, Topic.user_id == current_user.id)
        .first()
    )
    if not topic:
        topic = Topic(
            user_id=current_user.id,
            content=body.topic_content,
            type="TASK_2",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        session.add(topic)

    response = session.query(Response).filter(Response.topic_id == topic.id).first()
    if not response:
        response = Response(
            content=body.content,
            topic_id=topic.id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        session.add(response)
    else:
        response.content = body.content
        response.updated_at = datetime.now()

    session.commit()
    return {"message": "Content writing added successfully"}, 200


@response_bp.route("/detail", methods=["GET"])
@validate_body(ResponseSchema)
def detail(body: ResponseSchema):
    session = Session()
    response = session.query(Response).filter_by(topic_id=body.topic_id).first()
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


@response_bp.route("/list", methods=["PUT"])
def get(body: ListWritingSchema, current_user):
    session = Session()
    query = (
        session.query(Response)
        .filter_by(user_id=current_user.id)
        .order_by(Response.created_at.desc())
    )
    responses = query.limit(body.limit).offset(body.offset).all()
    return {
        "data": [
            {
                "id": response.id,
                "created_at": response.created_at,
                "content": response.content,
            }
            for response in responses
        ],
        "total": query.count(),
    }
