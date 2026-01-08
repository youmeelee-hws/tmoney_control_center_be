from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import os
import json
from pathlib import Path

router = APIRouter(tags=["error_logs"])

# 로그 저장 디렉토리
LOG_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent / "logs" / "mediamtx_errors"

class MediaMTXErrorLog(BaseModel):
    """MediaMTX 서버 오류 로그 모델"""
    streamId: str
    errorType: str  # 'connection_failed', 'whep_post_failed', 'connection_closed', etc.
    errorMessage: str
    statusCode: Optional[int] = None
    whepUrl: Optional[str] = None
    timestamp: str  # ISO 8601 format
    userAgent: Optional[str] = None
    clientInfo: Optional[dict] = None

class ErrorLogResponse(BaseModel):
    success: bool
    logFile: str
    message: str

@router.post("/error-logs/mediamtx", response_model=ErrorLogResponse)
def log_mediamtx_error(log_data: MediaMTXErrorLog) -> ErrorLogResponse:
    """
    MediaMTX 서버 다운 또는 연결 오류 발생 시 로그를 파일에 저장
    
    로그 파일 형식: logs/mediamtx_errors/YYYY-MM-DD.jsonl
    각 라인은 JSON 객체 (JSON Lines 형식)
    """
    try:
        # 로그 디렉토리 생성 (없으면)
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        
        # 날짜별 로그 파일명 생성
        log_date = datetime.fromisoformat(log_data.timestamp.replace('Z', '+00:00'))
        log_filename = f"{log_date.strftime('%Y-%m-%d')}.jsonl"
        log_filepath = LOG_DIR / log_filename
        
        # 로그 데이터 준비
        log_entry = {
            "timestamp": log_data.timestamp,
            "streamId": log_data.streamId,
            "errorType": log_data.errorType,
            "errorMessage": log_data.errorMessage,
            "statusCode": log_data.statusCode,
            "whepUrl": log_data.whepUrl,
            "userAgent": log_data.userAgent,
            "clientInfo": log_data.clientInfo,
        }
        
        # JSON Lines 형식으로 추가 (한 줄에 하나의 JSON)
        with open(log_filepath, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        
        return ErrorLogResponse(
            success=True,
            logFile=str(log_filepath),
            message=f"Error logged successfully to {log_filename}"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to write error log: {str(e)}"
        )

@router.get("/error-logs/mediamtx/latest")
def get_latest_logs(limit: int = 50):
    """
    최근 MediaMTX 오류 로그 조회 (디버깅용)
    """
    try:
        if not LOG_DIR.exists():
            return {"logs": [], "message": "No log directory found"}
        
        # 최신 로그 파일부터 읽기
        log_files = sorted(LOG_DIR.glob("*.jsonl"), reverse=True)
        
        logs = []
        for log_file in log_files:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        logs.append(json.loads(line))
                        if len(logs) >= limit:
                            break
            if len(logs) >= limit:
                break
        
        return {
            "logs": logs[:limit],
            "count": len(logs),
            "message": f"Retrieved {len(logs)} most recent error logs"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to read error logs: {str(e)}"
        )
