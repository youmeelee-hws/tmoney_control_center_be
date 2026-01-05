import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "tmoney_control_center_backend"
    API_V1_PREFIX: str = "/api/v1"

    # MediaMTX 설정
    MEDIAMTX_HOST: str = "127.0.0.1"
    MEDIAMTX_WEBRTC_PORT: int = 8889
    MEDIAMTX_RTSP_PORT: int = 8554
    MEDIAMTX_HLS_PORT: int = 8888
    MEDIAMTX_PATH: str = "stitched"  # 예: "live" -> /live/{streamId}/whep

    APP_ENV: str = "local"
    DEV_AUTH_TOKEN: str = "" # TODO 삭제 예정

    class Config:
        # ENV 환경변수에 따라 다른 파일 로드
        env_file = f".env.{os.getenv('ENV', 'local')}"
        env_file_encoding = 'utf-8'

settings = Settings()