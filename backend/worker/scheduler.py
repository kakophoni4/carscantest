import asyncio
import logging
import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.config import get_settings
from app.database import engine, AsyncSessionLocal, Base
from app.auth import ensure_admin_exists
from worker.scraper import run_scraper

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)
settings = get_settings()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        await ensure_admin_exists(session)
    logger.info("Database initialized")


async def scraper_job():
    logger.info("Scheduled scraper job triggered")
    try:
        created, updated = await run_scraper(max_pages=settings.SCRAPER_MAX_PAGES)
        logger.info("Job complete: %d new, %d updated", created, updated)
    except Exception as e:
        logger.exception("Scraper job failed: %s", e)


async def main():
    await init_db()

    logger.info("Running initial scrape...")
    await scraper_job()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        scraper_job,
        "interval",
        minutes=settings.SCRAPER_INTERVAL_MINUTES,
        id="carsensor_scraper",
        replace_existing=True,
    )
    scheduler.start()
    logger.info(
        "Scheduler started, scraping every %d minutes",
        settings.SCRAPER_INTERVAL_MINUTES,
    )

    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler stopped")


if __name__ == "__main__":
    asyncio.run(main())
