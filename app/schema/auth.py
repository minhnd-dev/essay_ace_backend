from pydantic import BaseModel


class AuthSchema(BaseModel):
    user_name: str
    password: str
