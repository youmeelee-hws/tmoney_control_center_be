from __future__ import annotations

from typing import Optional
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

try:
    # 선택: JWT 서명 검증 모드
    from jose import jwt, JWTError
except Exception:  # pragma: no cover
    jwt = None
    JWTError = Exception

from app.core.config import settings

PUBLIC_PATHS = {
    "/api/v1/ping",
    "/api/v1/token",
    "/api/v1/openapi.json",
    "/docs",
    "/redoc",
    "/api/v1/error-logs/mediamtx",  # MediaMTX 오류 로그 (인증 불필요)
    "/api/v1/error-logs/mediamtx/latest",  # 최근 오류 로그 조회
}


def _get_bearer_token(request: Request) -> Optional[str]:
    auth = request.headers.get("Authorization", "")
    if not auth:
        return None
    parts = auth.split(" ", 1)
    if len(parts) != 2:
        return None
    scheme, token = parts[0], parts[1].strip()
    if scheme.lower() != "bearer" or not token:
        return None
    return token


class ApiV1AuthMiddleware(BaseHTTPMiddleware):
    """
    - /api/v1/ping, /api/v1/token 등 PUBLIC_PATHS는 통과
    - 그 외 /api/v1/** 는 Authorization: Bearer <token> 필수
    - 검증 방식:
        1) JWT_SECRET이 설정되어 있고 python-jose 사용 가능하면 서명 검증
        2) 아니면 DEV_JWT와 문자열 완전 일치로 검증
    """

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # /api/v1 경로가 아니면 무시 (필요에 따라 전체 보호로 바꿔도 됨)
        if not path.startswith("/api/v1"):
            return await call_next(request)

        # Public allowlist
        if path in PUBLIC_PATHS:
            return await call_next(request)

        token = _get_bearer_token(request)
        if not token:
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing Authorization Bearer token"},
            )

        dev_jwt = settings.DEV_AUTH_TOKEN
        # jwt_secret = os.getenv("JWT_SECRET", "").strip()
        # jwt_alg = os.getenv("JWT_ALG", "HS256")

        # (A) JWT 서명 검증 모드
        # if jwt_secret and jwt is not None:
        #     try:
        #         payload = jwt.decode(token, jwt_secret, algorithms=[jwt_alg])
        #         # 필요하면 여기서 payload의 role/user_id 등을 request.state에 저장
        #         request.state.user = payload
        #     except JWTError:
        #         return JSONResponse(
        #             status_code=401,
        #             content={"detail": "Invalid or expired token"},
        #         )
        #     return await call_next(request)

        # (B) DEV_JWT 완전 일치 모드 (프로토타입 추천)
        if dev_jwt and token == dev_jwt:
            # request.state.user = {"sub": "dev-user", "role": "ADMIN"}
            return await call_next(request)

        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid token"},
        )
