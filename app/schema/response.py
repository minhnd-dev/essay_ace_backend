from pydantic import BaseModel


class ResponseSchema(BaseModel):
    topic_id: int


class SaveWritingSchema(BaseModel):
    content: str
