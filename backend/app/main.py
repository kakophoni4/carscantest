import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.config import get_settings
from app.database import engine, AsyncSessionLocal, Base
from app.auth import ensure_admin_exists
from app.routers.auth_router import router as auth_router
from app.routers.cars_router import router as cars_router

settings = get_settings()
logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        await ensure_admin_exists(session)

    yield

    await engine.dispose()


app = FastAPI(
    title="CarScaner API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = (time.perf_counter() - start) * 1000
    logger.info(
        "%s %s -> %d (%.1fms)",
        request.method, request.url.path, response.status_code, elapsed,
    )
    response.headers["X-Response-Time"] = f"{elapsed:.1f}ms"
    return response


app.include_router(auth_router, prefix="/api")
app.include_router(cars_router, prefix="/api")


@app.get("/api/health")
async def health():
    return {"status": "ok"}
