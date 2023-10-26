import datetime

from pydantic import BaseModel


class Token(BaseModel):
    user_id: str
    iat: str = datetime.datetime.utcnow()
    jti: str


class AccessTokens(Token):
    exp: str = datetime.datetime.utcnow() + datetime.timedelta(minutes=50)
    token_type: str = "access token"


class RefreshTokens(Token):
    exp: str = datetime.datetime.utcnow() + datetime.timedelta(minutes=100)
    token_type: str = "refresh token"
