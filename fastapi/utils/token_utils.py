from fastapi import HTTPException, status
from jose import JWTError, jwt

from schemas.tokens import AccessTokens, RefreshTokens

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


def create_access_token(access_token: AccessTokens):
    payload = access_token.model_dump()
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return access_token


def create_refresh_token(refresh_token: RefreshTokens):
    payload = refresh_token.model_dump()
    refresh_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return refresh_token


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


