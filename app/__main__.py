import logging

import uvicorn
from fastapi import FastAPI

from app import config
from app.Task1.config import prefix_task1
from app.Task1.router import router as router_task1
from app.Task2.config import prefix_task2
from app.Task2.router import router as router_task2
from app.Task1.models import Base

app = FastAPI(
    title="Bewise",
    description="Description",
    version="1.0.0",
    openapi_url=config.openapi_url,
    docs_url=config.docs_url,
)

app.include_router(
    router_task1,
    prefix=prefix_task1,
    tags=["Task1"],
)

app.include_router(
    router_task2,
    prefix=prefix_task2,
    tags=["Task2"],
)

logging.basicConfig(
    format="{asctime} : {levelname} : {name} : {message}",
    style="{",
    level=logging.INFO,
)

log: logging.Logger = logging.getLogger("main")


@app.on_event("startup")
async def startup_event() -> None:
    pass


@app.on_event("shutdown")
async def shutdown_event() -> None:
    pass


if __name__ == "__main__":
    uvicorn.run(
        "__main__:app",
        host=config.host,
        port=config.port,
        reload=config.reload,
        log_config=None,
    )
