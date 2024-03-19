from pydantic import BaseModel


class FeedbackSchema(BaseModel):
    content: str
    rewrite: str
