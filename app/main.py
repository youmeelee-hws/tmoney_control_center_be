from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.routes import api_router

print(f"ENV = {settings.APP_ENV}")

app = FastAPI(title=settings.APP_NAME)

# 개발 편의용 (운영에서는 origin 제한 권장)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    return {"name": settings.APP_NAME, "status": "running"}
