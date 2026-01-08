from fastapi import APIRouter
from app.api.v1.endpoints import ping, streams, auth, error_logs

api_router = APIRouter()

# 테스트
api_router.include_router(ping.router)

# 인증
api_router.include_router(auth.router)

# 스트리밍 관리
api_router.include_router(streams.router)

# 오류 로그
api_router.include_router(error_logs.router)