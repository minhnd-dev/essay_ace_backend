from pydantic import BaseModel


class TopicSchema(BaseModel):
    limit: int
    offset: int


class WritingSchema(BaseModel):
    content: str
    response_id: int


class UpdateWritingSchema(BaseModel):
    id: int
    content: str


class DeleteSchema(BaseModel):
    topic_id: int


class CreateTopicSchema(BaseModel):
    content: str


