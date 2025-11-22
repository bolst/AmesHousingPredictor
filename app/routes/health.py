from fastapi import APIRouter

health_router = APIRouter(prefix="/api", tags=["api_v1"])

@health_router.get("/health", response_model=dict[str, str])
def healthcheck() -> dict[str, str]:
    """
    Healthcheck endpoint to verify that the service is running.
    """
    return {"status": "ok"}