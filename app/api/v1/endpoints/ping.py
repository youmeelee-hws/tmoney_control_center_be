from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["debug"])

class PingResponse(BaseModel):
    ok: bool
    message: str

@router.get("/ping", response_model=PingResponse)
def ping() -> PingResponse:
    return PingResponse(ok=True, message="pong")
