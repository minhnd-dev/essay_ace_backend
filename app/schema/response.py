from pydantic import BaseModel


class ResponseSchema(BaseModel):
    topic_id: int


class SaveResponseSchema(BaseModel):
    topic_id: int | None = None
    topic_content: str
    response_id: int | None = None
    content: str


class ListWritingSchema(BaseModel):
    limit: int
    offset: int
