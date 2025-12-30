from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timedelta
import secrets

router = APIRouter(tags=["streams"])

"""
{
  "streams": [
    {
      "id": "cam-001",
      "name": "Gate 1",
      "status": "unknown",
      "capabilities": {
        "live": true,
        "record": false
      }
    },
    ...
  ]
}
"""
class StreamResponse(BaseModel):
    id: str
    name: str
    status: str

class StreamListResponse(BaseModel):
    streams: List[StreamResponse]

@router.get("/streams", response_model=StreamListResponse)
def get_stream_list() -> StreamListResponse:
    # 토큰 체크 # TODO 나중에 인증 구현 후 JWT 토큰 유효성 검증으로 대치
    
    streams = [
        StreamResponse(id="cam-001", name="Gate-01", status="unknown"),
        StreamResponse(id="cam-002", name="Gate-02", status="unknown"),
        StreamResponse(id="cam-003", name="Gate-03", status="unknown"),
        StreamResponse(id="cam-004", name="Gate-04", status="unknown"),
    ]

    return StreamListResponse(streams=streams)

"""
{
  "streamId": "cam-001",
  "playTicket": "ptk_abc123",
  "expiresAt": "2025-12-26T11:30:00+09:00",
  "whepUrl": "https://media.example.local/whep/cam-001"
}
"""
class PlayTicketResponse(BaseModel):
    streamId: str
    playTicket: str
    expiresAt: str  # ISO string (지금은 더미)
    whepUrl: str

@router.post("/streams/{streamId}/play-ticket", response_model=PlayTicketResponse)
def issue_play_ticket(streamId: str) -> PlayTicketResponse:
    expiresAt = (datetime.utcnow() + timedelta(minutes=30)).isoformat() + "Z"
    playTicket="ptk_abc123" # TODO 나중에 실제 티켓 발급 로직으로 대치
    whepUrl="https://media.stub.local/whep/" + streamId # TODO 나중에 실제 미디어 서버 URL로 대치
    return PlayTicketResponse(streamId=streamId, playTicket=playTicket, expiresAt=expiresAt, whepUrl=whepUrl)