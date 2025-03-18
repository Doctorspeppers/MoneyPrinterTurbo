from fastapi import APIRouter, Header, HTTPException, Depends
from app.config import config

API_KEY = config.app.get("api_key", "meu_super_secreto_token")

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

def new_router(require_auth: bool = True):
    router = APIRouter()
    router.tags = ["V1"]
    router.prefix = "/api/v1"
    
    if require_auth:
        router.dependencies = [Depends(verify_api_key)]
    
    return router
