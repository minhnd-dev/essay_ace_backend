from datetime import datetime

from flask import Blueprint

from app.database import Session
from app.models.response import Response
from app.schema.response import ResponseSchema, SaveWritingSchema, ListWritingSchema
from app.services.validation_service import validate_body

response_bp = Blueprint("response", __name__, url_prefix="/response")


@response_bp.route('/save', methods=['POST'])
@validate_body(SaveWritingSchema)
def save(body: SaveWritingSchema):
    session = Session()
    response = Response(content=body.content, created_at=datetime.now())
    session.add(response)
    session.commit()
    if response:
        return {"message": "Content writing added successfully"}, 200
    else:
        return {"message": "Added fail"}, 404


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
