from fastapi import APIRouter
from log_state import logs

router = APIRouter()

@router.get("/logs")
async def get_logs():
    return {"logs": logs}
