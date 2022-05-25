from fastapi import APIRouter

from core import settings
from database.mappings.base import Mapping

router = APIRouter()


class HealthRunning(Mapping):
    service: str
    running: bool


@router.get("/running", response_model=HealthRunning, include_in_schema=False)
async def health_running() -> HealthRunning:
    return HealthRunning(service=settings.PROJECT_TITLE, running=True)
