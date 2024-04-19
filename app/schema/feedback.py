from datetime import datetime

from pydantic import BaseModel


class FeedbackSchema(BaseModel):
    id: int


class RewriteSchema(BaseModel):
    content: str
    response_id: int


class CreateFeedbackSchema(BaseModel):
    response_id: int
