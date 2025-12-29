from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timedelta
import secrets
from app.core.config import settings

router = APIRouter(tags=["auth"])

class TokenResponse(BaseModel):
    token: str

@router.post("/token", response_model=TokenResponse)
def issue_token() -> TokenResponse:
    # TODO(나중): 로그인/권한 확인 + 짧은 토큰 발급 로직으로 교체
    return TokenResponse(token=settings.DEV_AUTH_TOKEN)