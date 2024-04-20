from datetime import timedelta
from fastapi import Depends, HTTPException, status, APIRouter
from src.domain.features.authentication.services.authentication_service import authenticate_user, fake_users_db, \
    generate_token
from src.domain.infrastructure.settings import Settings

router = APIRouter(prefix="/api", tags=["api"])


@router.post("/generate-jwt/")
async def get_generate_jwt(username: str, password: str):
    user = authenticate_user(fake_users_db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = user.username
    access_token_expires = timedelta(weeks=Settings.jwt_expire_weeks())

    return await generate_token(access_token_expires, username)

@router.post("/transcription_formatter/")
async def get_generate_jwt(username: str, password: str):
    user = authenticate_user(fake_users_db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = user.username
    access_token_expires = timedelta(weeks=Settings.jwt_expire_weeks())

    return await generate_token(access_token_expires, username)
