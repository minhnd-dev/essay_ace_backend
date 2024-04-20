from pydantic import BaseModel, field_validator
from pydantic import validator


class AuthSchema(BaseModel):
    user_name: str
    password: str

    @field_validator("user_name")
    @classmethod
    def username_validator(cls, v: str) -> str:
        min_length = 4
        max_length = 256
        if len(v) < min_length:
            raise ValueError(f"Username must be at least {min_length} characters long")
        elif len(v) > max_length:
            raise ValueError(f"Username must be at most {min_length} characters long")

        return v.title()

    @field_validator("password")
    @classmethod
    def password_validator(cls, v: str) -> str:
        min_length = 8
        if len(v) < min_length:
            raise ValueError(f"Password must be at least {min_length} characters long")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c in "!@#$%^&*()-_+=<>,.?/:;{}[]" for c in v):
            raise ValueError("Password must contain at least one special character")

        return v.title()


class ChangePasswordSchema(BaseModel):
    password: str
    new_password: str
