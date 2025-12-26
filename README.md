# T-Money Control Center Backend

FastAPI 기반의 T-Money Control Center 백엔드 서버입니다.

## 📋 프로젝트 개요

스트리밍 관리 및 제어를 위한 백엔드 API 서버로, MediaMTX와 연동하여 실시간 스트리밍 서비스를 제공합니다.

## 🛠 기술 스택

- **Python**: 3.10+ (tested on 3.12.3)
- **Framework**: FastAPI 0.127.0
- **ASGI Server**: Uvicorn 0.40.0
- **설정 관리**: Pydantic Settings 2.12.0
- **환경 변수**: python-dotenv 1.2.1

## 📁 프로젝트 구조

```
tmoney_control_center_be/
├── app/
│   ├── main.py                 # FastAPI 애플리케이션 엔트리포인트
│   ├── core/
│   │   └── config.py           # 환경 설정 관리
│   └── api/
│       └── v1/
│           ├── routes.py       # API 라우터 등록
│           └── endpoints/
│               ├── ping.py     # 헬스체크 엔드포인트
│               └── streams.py  # 스트리밍 관리 엔드포인트
├── requirements.txt            # Python 의존성 목록
├── .env.local                  # 로컬 환경 변수 (git ignored)
├── .env.dev                    # 개발 환경 변수 (git ignored)
├── .env.staging                # 스테이징 환경 변수 (git ignored)
├── .env.prod                   # 프로덕션 환경 변수 (git ignored)
├── .gitignore
└── README.md
```

## 🚀 설치 및 실행

### 1. 사전 요구사항

- Python 3.10 이상 (tested on 3.12.3)
- pip
- virtualenv (권장)

### 2. Python 및 pip 설치 (필요시)

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

### 3. 가상환경 생성 및 활성화

```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate  # Linux/WSL
# Windows: venv\Scripts\activate
```

### 4. 의존성 설치

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. 환경 변수 설정

프로젝트는 환경별로 분리된 설정 파일을 사용합니다:

- `.env.local` - 로컬 개발 환경
- `.env.dev` - 개발 서버 환경
- `.env.staging` - 스테이징 환경
- `.env.prod` - 프로덕션 환경

각 환경에 맞는 `.env` 파일을 생성하세요:

```bash
# .env.local 예시
APP_NAME=tmoney_control_center_backend
API_V1_PREFIX=/api/v1
APP_ENV=local
MEDIAMTX_BASE_URL=http://localhost:8889
```

```bash
# .env.prod 예시
APP_NAME=tmoney_control_center_backend
API_V1_PREFIX=/api/v1
APP_ENV=prod
MEDIAMTX_BASE_URL=http://production-mediamtx-server:8889
```

### 6. 서버 실행

환경에 따라 `ENV` 환경변수를 설정하여 실행합니다:

#### 로컬 개발 모드 (Hot Reload)

```bash
ENV=local uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 개발 서버

```bash
ENV=dev uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 스테이징 서버

```bash
ENV=staging uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### 프로덕션 모드

```bash
ENV=prod uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

> **참고**: `ENV` 환경변수를 지정하지 않으면 기본적으로 `local` 환경으로 실행됩니다.

서버가 시작되면 다음 URL에서 접근 가능합니다:

- API 서버: http://localhost:8000
- API 문서 (Swagger): http://localhost:8000/docs
- API 문서 (ReDoc): http://localhost:8000/redoc

## 📡 API 엔드포인트

### 기본 엔드포인트

#### `GET /`

서버 상태 확인

```json
{
  "name": "tmoney_control_center_backend",
  "status": "running"
}
```

### 헬스체크

#### `GET /api/v1/ping`

서버 헬스체크

```json
{
  "ok": true,
  "message": "pong"
}
```

### 스트리밍 관리

#### `POST /api/v1/streams/{stream_id}/play-ticket`

스트림 재생 티켓 발급

**요청:**

- Path Parameter: `stream_id` (string)

**응답:**

```json
{
  "stream_id": "stream123",
  "token": "temporary_token_here",
  "expires_at": "2024-12-26T12:34:56.789Z"
}
```

## ⚙️ 설정

### CORS 설정

현재 개발 모드에서는 `http://localhost:5173` (Vite 기본 포트)에서의 요청을 허용합니다.
프로덕션 환경에서는 `app/main.py`의 `allow_origins`를 수정하여 적절히 제한해야 합니다.

### 환경 변수

#### 환경 파일 설정

프로젝트는 `ENV` 환경변수를 통해 다른 설정 파일을 로드합니다:

```bash
ENV=local   → .env.local 파일 로드
ENV=dev     → .env.dev 파일 로드
ENV=staging → .env.staging 파일 로드
ENV=prod    → .env.prod 파일 로드
```

#### 사용 가능한 환경 변수

| 변수명              | 기본값                          | 설명                               |
| ------------------- | ------------------------------- | ---------------------------------- |
| `ENV`               | `local`                         | 실행 환경 (시스템 환경변수로 설정) |
| `APP_NAME`          | `tmoney_control_center_backend` | 애플리케이션 이름                  |
| `API_V1_PREFIX`     | `/api/v1`                       | API v1 경로 prefix                 |
| `APP_ENV`           | `local`                         | 애플리케이션 환경 표시             |
| `MEDIAMTX_BASE_URL` | `http://localhost:8889`         | MediaMTX 서버 URL                  |

## 🔧 개발

### 의존성 추가

새로운 패키지 설치 후 requirements.txt 업데이트:

```bash
pip install <package-name>
pip freeze > requirements.txt
```

### 코드 포맷팅 (권장)

```bash
pip install black isort
black app/
isort app/
```

### 타입 체크 (권장)

```bash
pip install mypy
mypy app/
```

## 🐛 트러블슈팅

### Import 오류

가상환경이 활성화되어 있는지 확인:

```bash
which python  # venv 경로가 표시되어야 함
```

### 포트 충돌

8000번 포트가 이미 사용 중인 경우 다른 포트 사용:

```bash
uvicorn app.main:app --reload --port 8001
```

## 📝 TODO

- [ ] LLM 엔드포인트 구현 (현재 routes.py에 import되어 있으나 파일 미존재)
- [ ] MediaMTX 실제 연동
- [ ] 인증/권한 시스템 구현
- [ ] 로깅 시스템 개선
- [ ] 테스트 코드 작성
- [ ] Docker 컨테이너화

## 📄 라이선스

(프로젝트 라이선스를 여기에 명시)

## 👥 기여

(기여 가이드라인을 여기에 명시)
