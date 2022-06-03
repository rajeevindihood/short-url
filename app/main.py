import logging

from fastapi import FastAPI, Request
import time

from app.core.dbpool import dbHdlr

logging.config.fileConfig("./app/logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

from app.api.hash import router as hashRouter

app=FastAPI(docs_url="/short-url/docs",openapi_url="/short-url/openapi.json")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.include_router(hashRouter)

@app.on_event("startup")
async def on_startup():
    dbHdlr()

@app.on_event("shutdown")
async def on_shutdown():
    dbHdlr().close()
