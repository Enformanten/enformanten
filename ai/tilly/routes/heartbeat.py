from fastapi import APIRouter, Request

from tilly.config import GIT_METADATA


router = APIRouter()


@router.get("/heartbeat/")
def heartbeat(_: Request):
    """Heartbeat endpoint"""
    return {"version": GIT_METADATA}
