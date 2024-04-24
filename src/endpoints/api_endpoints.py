import base64
from datetime import timedelta
from fastapi import Depends, HTTPException, status, APIRouter
from pydantic import BaseModel

from src.domain.features.authentication.services.authentication_service import authenticate_user, fake_users_db, \
    generate_token
from src.domain.features.parse_chatgpt_transcription.services.transcription_formatter import extract_title_and_summary
from src.domain.features.parse_chatgpt_transcription.title_summary import SummaryMetadata
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


class Item(BaseModel):
    transcription: str


@router.post("/transcription_formatter/")
def post_transcription_formatter(item: Item) -> SummaryMetadata:
    message_bytes = base64.b64decode(item.transcription)
    markdown = message_bytes.decode('utf-8')

    summary = extract_title_and_summary(markdown)

    return summary
