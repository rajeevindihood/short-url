import logging

from fastapi import FastAPI, Request
import time

from app.core.dbpool import dbHdlr

logging.config.fileConfig("./app/logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

from app.api.auth.router import router as auth_router
from app.api.hash.router import router as hashRouter

app=FastAPI(docs_url="/short-url/docs",openapi_url="/short-url/openapi.json")

from fastapi.middleware.cors import CORSMiddleware
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
    return response

app.include_router(auth_router)
app.include_router(hashRouter)

@app.on_event("startup")
async def on_startup():
    dbHdlr()

@app.on_event("shutdown")
async def on_shutdown():
    dbHdlr().close()
