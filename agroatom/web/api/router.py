from fastapi.routing import APIRouter

from agroatom.web.api import container, echo, grain_culture, monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(container.router, prefix="/containers", tags=["container"])
api_router.include_router(grain_culture.router, prefix="/cultures", tags=["culture"])
