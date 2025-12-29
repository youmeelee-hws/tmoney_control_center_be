from fastapi import APIRouter
from app.api.v1.endpoints import ping, streams, auth

api_router = APIRouter()

# 테스트
api_router.include_router(ping.router)

# 인증
api_router.include_router(auth.router)

# 스트리밍 관리
api_router.include_router(streams.router)