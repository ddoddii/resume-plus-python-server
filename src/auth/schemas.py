from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    username: str
    name: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserLoginRequest(BaseModel):
    username: str
    password: str
