from pydantic import BaseModel


class ResponseSchema(BaseModel):
    topic_id: int
