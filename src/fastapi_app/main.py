import asyncio
import os
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger

from routers import example, home
from utils import config_util, logger_util

WORKING_DIR = os.path.realpath(os.path.dirname(__file__))
CLIENT_DIR = os.path.realpath(os.path.join(WORKING_DIR, "../client/build"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Before FastAPI app start.
    logger.debug("Before FastAPI app start.")
    yield
    # Before FastAPI app shutdown.
    logger.debug("Before FastAPI app shutdown.")


app = FastAPI(lifespan=lifespan)
app.include_router(home.router)
app.include_router(example.router)

if os.environ.get("MODE") == "dev":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    # Serve static files.
    app.mount("/", StaticFiles(directory=CLIENT_DIR, html=True), name="client")


async def main():
    uvicorn_config = uvicorn.Config(
        APP,
        cfg.uvicorn.host,
        cfg.uvicorn.port,
        log_level=cfg.uvicorn.log_level,
    )
    logger_util.override_uvicorn_logger()
    server = uvicorn.Server(uvicorn_config)
    await server.serve()


if __name__ == "__main__":
    APP = "main:app"
    cfg = config_util.get_config(
        os.path.join(WORKING_DIR, "./configs/settings.json"),
    )

    if cfg is None:
        sys.exit(1)

    if cfg.logger is not None:
        logger_util.init_logger(cfg.logger)

    if os.environ.get("MODE") == "dev":
        logger.info("In development mode.")
        uvicorn.run(
            APP,
            host=cfg.uvicorn.host,
            port=cfg.uvicorn.port,
            reload=True,
            log_level=cfg.uvicorn.log_level,
        )
    else:
        asyncio.run(main())
