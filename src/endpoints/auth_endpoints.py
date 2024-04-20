from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from src.domain.features.authentication.models.authentication.token import JWToken
from src.domain.features.authentication.models.authentication.user import User
from src.domain.features.authentication.services.authentication_service import authenticate_user, fake_users_db, \
    get_current_active_user, get_password_hash, generate_token
from src.domain.infrastructure.settings import Settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> JWToken:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = user.username
    access_token_expires = timedelta(minutes=Settings.access_token_expire_minutes())

    return await generate_token(access_token_expires, username)


@router.get("/user/", response_model=User)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.get("/hashpassword/")
async def get_hash_password(password: str):
    return {"hashed_password": get_password_hash(password)}


@router.get("/user/items/")
async def read_own_items(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
