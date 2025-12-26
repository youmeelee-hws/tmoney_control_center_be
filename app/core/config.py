import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "tmoney_control_center_backend"
    API_V1_PREFIX: str = "/api/v1"

    # 나중에 MediaMTX 붙일 때 사용할 자리 (지금은 더미)
    MEDIAMTX_BASE_URL: str = "http://localhost:8889"
    # 예: WebRTC WHEP endpoint, HLS endpoint 등도 추후 여기에 추가

    APP_ENV: str = "local"
    DEV_AUTH_TOKEN: str = ""

    class Config:
        # ENV 환경변수에 따라 다른 파일 로드
        env_file = f".env.{os.getenv('ENV', 'local')}"
        env_file_encoding = 'utf-8'

settings = Settings()