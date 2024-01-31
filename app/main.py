import logging
import os
import time

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.hash.router import router as hash_router
from app.api.sys.router import router as sys_router
from app.api.sys.router import get_server_version
from app.core.errors import GenericError

logger = logging.getLogger(__name__)

if os.getenv("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        traces_sample_rate=1.0,
    )


app = FastAPI(docs_url="/short-url/docs", openapi_url="/short-url/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex="https://.*\.icanpe\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["Server-Timing"] = f"total;dur={process_time*1000}"
    response.headers["X-Canpe-Service"] = f"short-url:{get_server_version()}"
    return response


@app.exception_handler(GenericError)
async def generic_error_handler(request: Request, exc: GenericError):
    status, code, message, data = exc.get_error_params()
    return JSONResponse(
        status_code=status,
        content={"detail": {"code": code, "message": message, "data": data}},
    )


app.include_router(hash_router)
app.include_router(sys_router)
