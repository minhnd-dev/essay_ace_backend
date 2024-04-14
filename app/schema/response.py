from pydantic import BaseModel


class ResponseSchema(BaseModel):
    topic_id: int


class SaveWritingSchema(BaseModel):
    content: str


class ListWritingSchema(BaseModel):
    limit: int
    offset: int