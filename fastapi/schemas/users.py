from pydantic import BaseModel


class BaseUser(BaseModel):
    email: str


class CreateUser(BaseUser):
    password: str
    confirmed_password: str


class UserLogin(BaseUser):
    password: str


class UserInfo(BaseUser):
    id: str
