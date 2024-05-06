from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.api import board, post, user
from app.config import settings
from app.containers import Container
from app.middlewares.request import base_http_middleware
from app.schemas.base import ResponseBase

container = Container()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=base_http_middleware)

app.container = container  # type: ignore

app.include_router(user.router, prefix="/api/v1")
app.include_router(board.router, prefix="/api/v1")
app.include_router(post.router, prefix="/api/v1")


@app.on_event("startup")
async def startup() -> None:
    pass


@app.on_event("shutdown")
async def shutdown() -> None:
    db = container.db()
    await db.disconnect()


@app.get(
    "/health",
    response_model=ResponseBase,
    responses={
        200: {"description": "Server Alive"},
    },
    status_code=status.HTTP_200_OK,
    description="Health Check API",
    summary="Health Check",
)
async def health_check() -> ResponseBase:
    return ResponseBase(
        code=status.HTTP_200_OK,
        message="Server Alive",
        data={"status": "alive"},
    )
