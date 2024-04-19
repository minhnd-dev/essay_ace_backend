from datetime import datetime

from flask import Blueprint

from app.database import Session
from app.models.response import Response
from app.models.topic import Topic
from app.schema.topic import TopicSchema, DeleteSchema, CreateTopicSchema
from app.services.ai_model import AIModel
from app.services.jwt_service import jwt_required
from app.services.validation_service import validate_body

topic_bp = Blueprint("topic", __name__, url_prefix="/topic")


@topic_bp.route("/list", methods=["GET"])
@jwt_required
@validate_body(TopicSchema)
def get(body: TopicSchema, current_user):
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
                "response": topic.responses[0].content if topic.responses else None,
            }
            for topic in topics
        ],
        "total": query.count(),
    }


@topic_bp.route("/", methods=["DELETE"])
@validate_body(DeleteSchema)
def delete(body: DeleteSchema):
    session = Session()
    topic = session.query(Topic).filter(Topic.id == body.topic_id).first()
    if topic:
        session.delete(topic)
        session.commit()

        return {"message": "Topic deleted successfully"}, 200
    else:
        return {
            "message": "Topic not found or you don't have permission to delete it"
        }, 404


@topic_bp.route("/", methods=["POST"])
@jwt_required
@validate_body(CreateTopicSchema)
def create(body: CreateTopicSchema, current_user):
    session = Session()
    try:
        new_topic = Topic(
            user_id=current_user.id, content=body.content, created_at=datetime.now()
        )
        session.add(new_topic)
        session.commit()
        return {"message": "Topic created successfully"}, 201
    except Exception as e:
        session.rollback()
        return {"message": "Failed to create topic", "error": str(e)}, 500
    finally:
        session.close()


@topic_bp.route("/ai", methods=["GET"])
@jwt_required
def get_ai_generated_topic(current_user):
    ai = AIModel()
    return {
        "message": "Successfully generated topic",
        "data": ai.generate_topic(),
    }


@topic_bp.route("/<int:topic_id>", methods=["GET"])
@jwt_required
def get_topic_detail(current_user, topic_id):
    session = Session()
    topic = (
        session.query(Topic)
        .filter(Topic.id == topic_id, Topic.user_id == current_user.id)
        .first()
    )
    if not topic:
        return {
            "message": "Topic not found or you don't have permission to access it"
        }, 404

    return_data = {
        "id": topic.id,
        "created_at": topic.created_at,
        "content": topic.content,
    }
    response = session.query(Response).filter(Response.topic_id == topic_id).first()
    if response:
        return_data["response"] = {
            "content": response.content,
            "updated_at": response.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

        feedback = response.feedback
        if feedback:
            return_data["feedback"] = {"content": feedback[0].content}

    return {"message": "Successfully get topic detail", "data": return_data}
