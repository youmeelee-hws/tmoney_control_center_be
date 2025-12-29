FROM python:3.12-slim

# 파이썬 출력 버퍼 제거(로그 바로 보이게)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# (선택) 빌드에 필요한 최소 패키지
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

# 의존성 먼저 설치(캐시 효율)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 복사
COPY . .

# 기본 포트
EXPOSE 8000

# 기본 실행: uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
