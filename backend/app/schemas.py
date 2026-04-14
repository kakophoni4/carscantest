from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: UUID
    username: str

    class Config:
        from_attributes = True


class CarResponse(BaseModel):
    id: UUID
    external_id: str
    brand: str
    brand_jp: str | None = None
    model: str
    model_jp: str | None = None
    grade: str | None = None
    year: int | None = None
    mileage_km: int | None = None
    price_jpy: int | None = None
    price_man: float | None = None
    engine_cc: int | None = None
    transmission: str | None = None
    drive_type: str | None = None
    fuel_type: str | None = None
    color: str | None = None
    color_jp: str | None = None
    body_type: str | None = None
    doors: int | None = None
    seats: int | None = None
    inspection_date: str | None = None
    repair_history: str | None = None
    location: str | None = None
    dealer_name: str | None = None
    url: str
    thumbnail: str | None = None
    images: list[str] | None = None
    description: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CarListResponse(BaseModel):
    items: list[CarResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class FiltersResponse(BaseModel):
    brands: list[str]
    body_types: list[str]
    fuel_types: list[str]
    transmissions: list[str]
    drive_types: list[str]
    colors: list[str]
    dealers: list[str]
    year_min: int | None = None
    year_max: int | None = None
    price_min: int | None = None
    price_max: int | None = None
    engine_min: int | None = None
    engine_max: int | None = None
