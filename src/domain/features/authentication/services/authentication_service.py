from datetime import timedelta, datetime, timezone
from http.client import HTTPException
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from jose import jwt, JWTError
from passlib.context import CryptContext

from src.domain.features.authentication.models.authentication.token import JWToken
from src.domain.features.authentication.models.authentication.token_data import TokenData
from src.domain.features.authentication.models.authentication.user import User
from src.domain.features.authentication.models.authentication.user_in_db import UserInDB

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

# PW Folsom_800
fake_users_db = {
    "chuckconway": {
        "username": "chuckconway",
        "full_name": "Chuck Conway",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$3w7fNpnWWZDvIzNCpcydRuMnn3g49A6SOSDNZXJFt5lvDwaFJqX4a",
        "disabled": False,
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def generate_token(access_token_expires: timedelta, username: str, scope: str = None) -> JWToken:
    """
    Generates a JWT Token
    :param access_token_expires: This takes a timedelta object.
    :param username: The username of the user requesting the token
    :param scope: Optional. The scope of the token. Format it as application:read (ex. api:read)
    :return: JWToken object
    """

    dict_data = {"sub": username}

    if scope:
        dict_data["scope"] = scope

    access_token = create_access_token(
        data=dict_data, expires_delta=access_token_expires
    )

    return JWToken(access_token=access_token, token_type="bearer")


def get_password_hash(password):
    hashed_password = pwd_context.hash(password)
    return hashed_password


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
