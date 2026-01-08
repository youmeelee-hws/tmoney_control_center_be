# MediaMTX 오류 로깅 시스템

## 개요

MediaMTX 서버가 다운되거나 연결 오류가 발생했을 때 **자동으로** 오류 로그를 파일로 저장하는 시스템입니다.

## 구현 내용

### 1. 백엔드 (FastAPI)

**새로운 API 엔드포인트:**

- `POST /api/v1/error-logs/mediamtx` - MediaMTX 오류 로그 저장
- `GET /api/v1/error-logs/mediamtx/latest?limit=50` - 최근 오류 로그 조회

**로그 파일 저장 위치:**

```
tmoney_control_center_be/logs/mediamtx_errors/YYYY-MM-DD.jsonl
```

**파일 형식:** JSON Lines (`.jsonl`)

- 한 줄에 하나의 JSON 객체
- 날짜별로 파일 생성
- 예: `2026-01-08.jsonl`

### 2. 프론트엔드 (React + TypeScript)

**수정된 파일:**

- `src/api/errorLogs.ts` - 오류 로그 API 클라이언트
- `src/hooks/useWebRTCPlayer.ts` - WebRTC 연결 오류 감지 및 자동 로그 전송
- `src/components/PlayerSlot.tsx` - streamId 전달
- `src/components/TestPlayerSlot.tsx` - streamId 전달

**오류 감지 시점:**

1. **WHEP POST 실패** - MediaMTX 서버가 응답하지 않거나 HTTP 오류 반환
2. **Fetch 오류** - 네트워크 연결 실패 (서버 다운, 타임아웃 등)
3. **WebRTC 연결 실패/종료** - 연결이 'failed' 또는 'closed' 상태로 변경

## 로그 데이터 구조

```json
{
  "timestamp": "2026-01-08T12:34:56.789Z",
  "streamId": "stream-001",
  "errorType": "whep_post_failed",
  "errorMessage": "WHEP POST failed: 502 Bad Gateway",
  "statusCode": 502,
  "whepUrl": "http://192.168.0.10:8889/stitched/whep",
  "userAgent": "Mozilla/5.0...",
  "clientInfo": {
    "browserName": "Chrome",
    "browserVersion": "120.0",
    "os": "Linux x86_64",
    "screenResolution": "1920x1080"
  }
}
```

## 테스트 방법

### 1. 정상 동작 확인

백엔드와 프론트엔드를 실행한 상태에서:

```bash
# 백엔드 실행
cd /root/tmoney_control_center_be
source venv/bin/activate  # 가상환경이 있는 경우
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 프론트엔드 실행 (다른 터미널)
cd /root/tmoney_control_center
npm run dev
```

### 2. MediaMTX 서버 다운 시뮬레이션

**방법 1: MediaMTX 서버 중지**

```bash
# MediaMTX가 실행 중이면 중지
pkill mediamtx
```

**방법 2: 잘못된 URL 설정**

- 프론트엔드에서 존재하지 않는 스트림에 연결 시도
- 백엔드 환경변수에서 잘못된 MediaMTX 호스트 설정

### 3. 로그 파일 확인

```bash
# 오늘 날짜의 로그 파일 확인
cd /root/tmoney_control_center_be/logs/mediamtx_errors
cat $(date +%Y-%m-%d).jsonl

# 또는 최근 로그를 보기 좋게 포맷팅
cat $(date +%Y-%m-%d).jsonl | jq '.'
```

**또는 API로 조회:**

```bash
curl http://localhost:8000/api/v1/error-logs/mediamtx/latest?limit=10
```

### 4. 예상 결과

MediaMTX 서버가 다운되면:

1. **프론트엔드:**

   - 브라우저 콘솔에 오류 메시지 출력
   - UI에 오류 상태 표시
   - 백엔드로 오류 로그 자동 전송

2. **백엔드:**

   - `/logs/mediamtx_errors/YYYY-MM-DD.jsonl` 파일에 로그 기록
   - 각 오류마다 한 줄씩 추가

3. **로그 내용:**
   - 발생 시간 (timestamp)
   - 어떤 스트림에서 발생했는지 (streamId)
   - 오류 유형 (errorType)
   - 상세 오류 메시지 (errorMessage)
   - HTTP 상태 코드 (있으면)
   - 클라이언트 정보 (브라우저, OS 등)

## 오류 유형 (errorType)

- `fetch_error` - 네트워크 연결 실패 (서버 다운, 타임아웃)
- `whep_post_failed` - WHEP POST 요청이 HTTP 오류 반환 (404, 500, 502 등)
- `connection_closed` - WebRTC 연결이 실패하거나 닫힘
- `connection_failed` - WebRTC 연결 실패
- `unknown` - 기타 알 수 없는 오류

## 주의사항

1. **로그 파일 용량 관리**

   - 오래된 로그 파일은 주기적으로 삭제하거나 아카이빙 필요
   - logrotate 등의 도구 사용 권장

2. **로그 전송 실패**

   - 로그 전송이 실패해도 사용자 경험에는 영향 없음
   - 콘솔에 경고 메시지만 출력

3. **개인정보**
   - User-Agent 등 클라이언트 정보가 포함됨
   - 필요에 따라 수집 항목 조정 가능

## 향후 개선 사항

- [ ] 로그 파일 자동 로테이션
- [ ] 오류 알림 (이메일, Slack 등)
- [ ] 대시보드를 통한 오류 통계 시각화
- [ ] 오류 패턴 분석 및 자동 복구
