import logging
import asyncio
from datetime import datetime, timezone
from bs4 import BeautifulSoup, Tag
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models import Car
from worker.translator import (
    translate_brand, translate_model, translate_body_type, translate_fuel,
    translate_transmission, translate_drive, translate_color, translate_repair,
    parse_mileage, parse_price_man, parse_engine_cc, parse_year,
)
from worker.auto_translate import translate_cars_batch

logger = logging.getLogger(__name__)

BASE_URL = "https://www.carsensor.net"
LISTING_URL = BASE_URL + "/usedcar/index{page}.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept-Language": "ja,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
REQUEST_DELAY = 1.5
DETAIL_DELAY = 1.0


def _text(el: Tag | None) -> str | None:
    if el is None:
        return None
    return el.get_text(strip=True) or None


def _extract_external_id(cassette: Tag) -> str | None:
    div_id = cassette.get("id", "")
    if "_cas" in div_id:
        return div_id.replace("_cas", "")
    return None


def _extract_images(cassette: Tag) -> tuple[str | None, list[str]]:
    thumbnail = None
    images = []

    main_img = cassette.select_one(".cassetteMain__mainImg img[data-original]")
    if main_img:
        src = main_img.get("data-original", "")
        if src:
            thumbnail = "https:" + src if src.startswith("//") else src
            images.append(thumbnail)

    noscript_img = cassette.select_one(".cassetteMain__mainImg noscript img")
    if noscript_img and not thumbnail:
        src = noscript_img.get("src", "")
        if src:
            thumbnail = "https:" + src if src.startswith("//") else src
            images.append(thumbnail)

    for sub in cassette.select(".cassetteMain__subImg img[data-original]"):
        src = sub.get("data-original", "")
        if src:
            url = "https:" + src if src.startswith("//") else src
            if url not in images:
                images.append(url)

    return thumbnail, images


def _extract_spec(cassette: Tag, title: str) -> str | None:
    for box in cassette.select(".specList__detailBox"):
        dt = box.select_one(".specList__title")
        if dt and title in _text(dt):
            dd = box.select_one(".specList__data")
            return _text(dd)
    return None


def _extract_year(cassette: Tag) -> int | None:
    for box in cassette.select(".specList__detailBox"):
        dt = box.select_one(".specList__title")
        if dt and "年式" in (_text(dt) or ""):
            emphasis = box.select_one(".specList__emphasisData")
            if emphasis:
                return parse_year(_text(emphasis))
    return None


def _extract_mileage(cassette: Tag) -> int | None:
    for box in cassette.select(".specList__detailBox"):
        dt = box.select_one(".specList__title")
        if dt and "走行距離" in (_text(dt) or ""):
            dd = box.select_one(".specList__data")
            return parse_mileage(_text(dd))
    return None


def _extract_price(cassette: Tag) -> tuple[float | None, int | None]:
    base_main = cassette.select_one(".basePrice__mainPriceNum")
    base_sub = cassette.select_one(".basePrice__subPriceNum")
    if base_main:
        price_str = _text(base_main)
        if base_sub:
            price_str += _text(base_sub) or ""
        price_str += "万円"
        return parse_price_man(price_str)
    return None, None


def _extract_body_color(cassette: Tag) -> tuple[str | None, str | None, str | None]:
    body_type_jp = None
    color_jp = None
    items = cassette.select(".carBodyInfoList__item")
    if len(items) >= 1:
        body_type_jp = _text(items[0])
    if len(items) >= 2:
        color_jp = _text(items[1])
        for tip in items[1].select(".cassetteColorTip"):
            tip.decompose()
        color_jp = _text(items[1]) or color_jp

    body_type = translate_body_type(body_type_jp)
    return body_type, color_jp, translate_color(color_jp)


def parse_cassette(cassette: Tag) -> dict | None:
    external_id = _extract_external_id(cassette)
    if not external_id:
        return None

    link_el = cassette.select_one(".cassetteMain__title a")
    url = ""
    title = ""
    if link_el:
        href = link_el.get("href", "")
        url = BASE_URL + href if href.startswith("/") else href
        title = _text(link_el) or ""

    brand_el = cassette.select_one(".cassetteMain__carInfoContainer > p")
    brand_jp = _text(brand_el)
    brand = translate_brand(brand_jp) or brand_jp or "Unknown"

    title_clean = title.replace("\xa0", " ").strip()
    model_jp = title_clean.split(" ")[0] if title_clean else ""
    model_en = translate_model(model_jp)
    grade = " ".join(title_clean.split(" ")[1:]) if " " in title_clean else None

    year = _extract_year(cassette)
    mileage_km = _extract_mileage(cassette)
    price_man, price_jpy = _extract_price(cassette)

    engine_text = _extract_spec(cassette, "排気量")
    engine_cc = parse_engine_cc(engine_text)

    transmission_jp = _extract_spec(cassette, "ミッション")
    transmission = translate_transmission(transmission_jp)

    repair_jp = _extract_spec(cassette, "修復歴")
    repair_history = translate_repair(repair_jp)

    inspection = _extract_spec(cassette, "車検")

    body_type, color_jp, color = _extract_body_color(cassette)

    thumbnail, images = _extract_images(cassette)

    location_parts = []
    area_div = cassette.select_one(".cassetteSub__area")
    if area_div:
        for p in area_div.select("p"):
            t = _text(p)
            if t:
                location_parts.append(t)
    location = " ".join(location_parts) if location_parts else None

    dealer_el = cassette.select_one(".cassetteSub__shop a")
    dealer_name = _text(dealer_el)

    description = _text(cassette.select_one(".cassetteMain__subText"))

    return {
        "external_id": external_id,
        "brand": brand,
        "brand_jp": brand_jp,
        "model": model_en or model_jp or brand,
        "model_jp": model_jp,
        "grade": grade,
        "year": year,
        "mileage_km": mileage_km,
        "price_jpy": price_jpy,
        "price_man": price_man,
        "engine_cc": engine_cc,
        "transmission": transmission,
        "fuel_type": None,
        "drive_type": None,
        "color": color,
        "color_jp": color_jp,
        "body_type": body_type,
        "doors": None,
        "seats": None,
        "inspection_date": inspection,
        "repair_history": repair_history,
        "location": location,
        "dealer_name": dealer_name,
        "url": url,
        "thumbnail": thumbnail,
        "images": images if images else None,
        "description": description,
    }


def _parse_drive_type(raw: str) -> str:
    raw_lower = raw.strip()
    if "4WD" in raw_lower or "四輪駆動" in raw:
        return "4WD"
    if "FF" in raw or "前輪駆動" in raw:
        return "FF"
    if "FR" in raw or "後輪駆動" in raw:
        return "FR"
    if "MR" in raw or "ミッドシップ" in raw:
        return "MR"
    if "RR" in raw:
        return "RR"
    if "2WD" in raw:
        return "2WD"
    return translate_drive(raw) or raw


async def fetch_detail(client: httpx.AsyncClient, url: str) -> dict:
    extra = {}
    try:
        resp = await client.get(url, headers=HEADERS, follow_redirects=True, timeout=30.0)
        resp.raise_for_status()
    except httpx.HTTPError as e:
        logger.warning("Failed to fetch detail %s: %s", url, e)
        return extra

    soup = BeautifulSoup(resp.text, "lxml")

    rows = soup.select("tr")
    for row in rows:
        ths = row.select("th.defaultTable__head")
        tds = row.select("td.defaultTable__description")
        for th, td in zip(ths, tds):
            label = _text(th) or ""
            value = _text(td)
            if not value:
                continue

            if "燃料" in label and "fuel_type" not in extra:
                extra["fuel_type"] = translate_fuel(value)
            elif "駆動" in label and "drive_type" not in extra:
                extra["drive_type"] = _parse_drive_type(value)
            elif "乗車定員" in label and "seats" not in extra:
                try:
                    extra["seats"] = int(value.replace("人", "").replace("名", "").strip())
                except (ValueError, TypeError):
                    pass
            elif "ドア" in label and "doors" not in extra:
                try:
                    extra["doors"] = int(value.replace("D", "").replace("ドア", "").strip())
                except (ValueError, TypeError):
                    pass

    return extra


async def fetch_page(client: httpx.AsyncClient, page: int) -> list[dict]:
    url = LISTING_URL.format(page=page)
    logger.info("Fetching page %d: %s", page, url)

    try:
        resp = await client.get(url, headers=HEADERS, follow_redirects=True, timeout=30.0)
        resp.raise_for_status()
    except httpx.HTTPError as e:
        logger.error("Failed to fetch page %d: %s", page, e)
        return []

    soup = BeautifulSoup(resp.text, "lxml")
    cassettes = soup.select(".cassette.js_listTableCassette")
    logger.info("Found %d cassettes on page %d", len(cassettes), page)

    cars = []
    for cass in cassettes:
        data = parse_cassette(cass)
        if data:
            cars.append(data)

    return cars


async def save_cars(session: AsyncSession, cars: list[dict]) -> tuple[int, int]:
    created = 0
    updated = 0
    seen_ids: set[str] = set()

    for car_data in cars:
        ext_id = car_data["external_id"]
        if ext_id in seen_ids:
            continue
        seen_ids.add(ext_id)

        result = await session.execute(
            select(Car).where(Car.external_id == ext_id)
        )
        existing = result.scalar_one_or_none()

        if not existing and car_data.get("url"):
            dup_by_url = await session.execute(
                select(Car).where(Car.url == car_data["url"])
            )
            existing = dup_by_url.scalar_one_or_none()

        if existing:
            for key, value in car_data.items():
                if key != "external_id" and value is not None:
                    setattr(existing, key, value)
            existing.updated_at = datetime.now(timezone.utc)
            updated += 1
        else:
            car = Car(**car_data)
            session.add(car)
            created += 1

    await session.commit()
    return created, updated


async def enrich_with_details(
    client: httpx.AsyncClient, cars: list[dict], batch_size: int = 5
) -> list[dict]:
    for i in range(0, len(cars), batch_size):
        batch = cars[i : i + batch_size]
        for car in batch:
            if not car.get("url"):
                continue
            try:
                detail = await fetch_detail(client, car["url"])
                for key, value in detail.items():
                    if car.get(key) is None and value is not None:
                        car[key] = value
                await asyncio.sleep(DETAIL_DELAY)
            except Exception as e:
                logger.warning("Detail enrichment failed for %s: %s", car.get("external_id"), e)
    return cars


async def run_scraper(max_pages: int = 5):
    logger.info("Starting CarSensor scraper, max_pages=%d", max_pages)
    total_created = 0
    total_updated = 0

    async with httpx.AsyncClient() as client:
        for page in range(1, max_pages + 1):
            try:
                cars = await fetch_page(client, page)
                if not cars:
                    logger.info("No cars found on page %d, stopping", page)
                    break

                cars = await enrich_with_details(client, cars)

                logger.info("Translating Japanese text for page %d...", page)
                cars = await translate_cars_batch(cars)

                async with AsyncSessionLocal() as session:
                    created, updated = await save_cars(session, cars)
                    total_created += created
                    total_updated += updated
                    logger.info(
                        "Page %d: %d created, %d updated (total: %d new, %d updated)",
                        page, created, updated, total_created, total_updated,
                    )

                await asyncio.sleep(REQUEST_DELAY)

            except Exception as e:
                logger.exception("Error processing page %d: %s", page, e)
                continue

    logger.info(
        "Scraper finished: %d new cars, %d updated",
        total_created, total_updated,
    )
    return total_created, total_updated
