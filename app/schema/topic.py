from pydantic import BaseModel


class TopicSchema(BaseModel):
    limit: int
    offset: int


class WritingSchema(BaseModel):
    content: str
