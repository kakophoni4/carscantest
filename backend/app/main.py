import os
import time
import asyncio
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

_scraper_task = None


async def _scraper_loop():
    from worker.scraper import run_scraper
    await asyncio.sleep(5)
    while True:
        try:
            logger.info("Scraper started")
            await run_scraper(max_pages=settings.SCRAPER_MAX_PAGES)
            logger.info("Scraper finished, next run in %d min", settings.SCRAPER_INTERVAL_MINUTES)
        except Exception as e:
            logger.exception("Scraper failed: %s", e)
        await asyncio.sleep(settings.SCRAPER_INTERVAL_MINUTES * 60)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _scraper_task
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        await ensure_admin_exists(session)

    run_worker = os.environ.get("RUN_WORKER", "false").lower() in ("1", "true", "yes")
    if run_worker:
        _scraper_task = asyncio.create_task(_scraper_loop())

    yield

    if _scraper_task:
        _scraper_task.cancel()
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
