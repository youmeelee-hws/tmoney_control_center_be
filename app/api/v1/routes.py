from fastapi import APIRouter
from app.api.v1.endpoints import ping, streams

api_router = APIRouter()

# 테스트
api_router.include_router(ping.router)

# 스트리밍 관리
api_router.include_router(streams.router)