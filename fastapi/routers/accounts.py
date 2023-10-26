from uuid import uuid4

from fastapi import APIRouter, HTTPException, Depends, status

from db.mongodb import get_db
from schemas.tokens import AccessTokens, RefreshTokens
from schemas.users import CreateUser, UserInfo, UserLogin
from utils.token_utils import create_access_token, create_refresh_token, decode_token
from utils.user_utils import get_password_hash, verify_password

routers = APIRouter()


@routers.post("/register/")
async def register_user(user: CreateUser, db=Depends(get_db)):
    users = db["accounts"]
    result = await users.find_one({"email": user.email})

    if result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    if user.password != user.confirmed_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords don't match")

    hashed_password = get_password_hash(user.password)
    data = {"email": user.email, "password_hash": hashed_password}
    result = await users.insert_one(data)
    _id = str(result.inserted_id)

    user_info = UserInfo(id=_id, email=user.email)

    return user_info


@routers.post("/login/")
async def login(user: UserLogin, db=Depends(get_db)):
    users = db["accounts"]
    result = await users.find_one({"email": user.email})

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is wrong")
    if not verify_password(user.password, result["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is wrong")

    user_id = str(result["_id"])

    jti = uuid4().hex
    access_token = AccessTokens(user_id=user_id, jti=jti)
    refresh_token = RefreshTokens(user_id=user_id, jti=jti)

    access_token = create_access_token(access_token)
    refresh_token = create_refresh_token(refresh_token)

    data = {"access_token": access_token, "refresh_token": refresh_token}
    token = db["token"]
    await token.insert_one(data)

    return {"access_token": access_token, "refresh_token": refresh_token}


@routers.get("/profile/")
async def profile(token: str, db=Depends(get_db)):
    decode_token(token)