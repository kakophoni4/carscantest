import pytest
from httpx import AsyncClient
from app.models import Car


@pytest.mark.asyncio
async def test_list_cars_unauthorized(client: AsyncClient):
    resp = await client.get("/api/cars")
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_list_cars(client: AsyncClient, auth_headers: dict, sample_cars: list[Car]):
    resp = await client.get("/api/cars", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 5
    assert len(data["items"]) == 5
    assert data["page"] == 1
    assert data["total_pages"] == 1


@pytest.mark.asyncio
async def test_list_cars_pagination(client: AsyncClient, auth_headers: dict, sample_cars: list[Car]):
    resp = await client.get("/api/cars", headers=auth_headers, params={
        "page_size": 2, "page": 1,
    })
    data = resp.json()
    assert len(data["items"]) == 2
    assert data["total"] == 5
    assert data["total_pages"] == 3


@pytest.mark.asyncio
async def test_filter_by_brand(client: AsyncClient, auth_headers: dict, sample_cars: list[Car]):
    resp = await client.get("/api/cars", headers=auth_headers, params={"brand": "Toyota"})
    data = resp.json()
    assert data["total"] == 3
    for item in data["items"]:
        assert item["brand"] == "Toyota"


@pytest.mark.asyncio
async def test_filter_by_year_range(client: AsyncClient, auth_headers: dict, sample_cars: list[Car]):
    resp = await client.get("/api/cars", headers=auth_headers, params={
        "year_min": 2022, "year_max": 2024,
    })
    data = resp.json()
    for item in data["items"]:
        assert 2022 <= item["year"] <= 2024


@pytest.mark.asyncio
async def test_filter_by_price_range(client: AsyncClient, auth_headers: dict, sample_cars: list[Car]):
    resp = await client.get("/api/cars", headers=auth_headers, params={
        "price_min": 1000000, "price_max": 1500000,
    })
    data = resp.json()
    for item in data["items"]:
        assert 1000000 <= item["price_jpy"] <= 1500000


@pytest.mark.asyncio
async def test_filter_by_mileage(client: AsyncClient, auth_headers: dict, sample_cars: list[Car]):
    resp = await client.get("/api/cars", headers=auth_headers, params={
        "mileage_max": 20000,
    })
    data = resp.json()
    for item in data["items"]:
        assert item["mileage_km"] <= 20000


@pytest.mark.asyncio
async def test_search(client: AsyncClient, auth_headers: dict, sample_cars: list[Car]):
    resp = await client.get("/api/cars", headers=auth_headers, params={"search": "Civic"})
    data = resp.json()
    assert data["total"] == 2
    for item in data["items"]:
        assert item["model"] == "Civic"


@pytest.mark.asyncio
async def test_sort_price_asc(client: AsyncClient, auth_headers: dict, sample_cars: list[Car]):
    resp = await client.get("/api/cars", headers=auth_headers, params={
        "sort_by": "price_jpy", "sort_order": "asc",
    })
    data = resp.json()
    prices = [item["price_jpy"] for item in data["items"]]
    assert prices == sorted(prices)


@pytest.mark.asyncio
async def test_sort_year_desc(client: AsyncClient, auth_headers: dict, sample_cars: list[Car]):
    resp = await client.get("/api/cars", headers=auth_headers, params={
        "sort_by": "year", "sort_order": "desc",
    })
    data = resp.json()
    years = [item["year"] for item in data["items"]]
    assert years == sorted(years, reverse=True)


@pytest.mark.asyncio
async def test_get_car_by_id(client: AsyncClient, auth_headers: dict, sample_cars: list[Car]):
    car_id = str(sample_cars[0].id)
    resp = await client.get(f"/api/cars/{car_id}", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["external_id"] == "test_0"


@pytest.mark.asyncio
async def test_get_car_not_found(client: AsyncClient, auth_headers: dict, sample_cars: list[Car]):
    resp = await client.get(
        "/api/cars/00000000-0000-0000-0000-000000000000",
        headers=auth_headers,
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_filters(client: AsyncClient, auth_headers: dict, sample_cars: list[Car]):
    resp = await client.get("/api/cars/filters", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "Toyota" in data["brands"]
    assert "Honda" in data["brands"]
    assert "Sedan" in data["body_types"]
    assert data["year_min"] == 2020
    assert data["year_max"] == 2024


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    resp = await client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
