from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timedelta
import secrets

router = APIRouter(tags=["streams"])

class PlayTicketResponse(BaseModel):
    stream_id: str
    token: str
    expires_at: str  # ISO string (지금은 더미)

@router.post("/streams/{stream_id}/play-ticket", response_model=PlayTicketResponse)
def issue_play_ticket(stream_id: str) -> PlayTicketResponse:
    # TODO(나중): 로그인/권한 확인 + 짧은 토큰 발급 로직으로 교체
    token = secrets.token_urlsafe(24)
    expires_at = (datetime.utcnow() + timedelta(minutes=5)).isoformat() + "Z"
    return PlayTicketResponse(stream_id=stream_id, token=token, expires_at=expires_at)
