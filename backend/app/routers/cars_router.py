from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, asc
from app.database import get_db
from app.models import Car, User
from app.schemas import CarResponse, CarListResponse, FiltersResponse
from app.auth import get_current_user

router = APIRouter(prefix="/cars", tags=["cars"])


@router.get("", response_model=CarListResponse)
async def list_cars(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    brand: str | None = None,
    body_type: str | None = None,
    fuel_type: str | None = None,
    transmission: str | None = None,
    drive_type: str | None = None,
    color: str | None = None,
    dealer_name: str | None = None,
    year_min: int | None = None,
    year_max: int | None = None,
    price_min: int | None = None,
    price_max: int | None = None,
    mileage_max: int | None = None,
    engine_min: int | None = None,
    engine_max: int | None = None,
    search: str | None = None,
    sort_by: str = Query("created_at", pattern="^(price_jpy|year|mileage_km|created_at)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    query = select(Car)
    count_query = select(func.count(Car.id))

    if brand:
        query = query.where(Car.brand == brand)
        count_query = count_query.where(Car.brand == brand)
    if body_type:
        query = query.where(Car.body_type == body_type)
        count_query = count_query.where(Car.body_type == body_type)
    if fuel_type:
        query = query.where(Car.fuel_type == fuel_type)
        count_query = count_query.where(Car.fuel_type == fuel_type)
    if transmission:
        query = query.where(Car.transmission == transmission)
        count_query = count_query.where(Car.transmission == transmission)
    if drive_type:
        query = query.where(Car.drive_type == drive_type)
        count_query = count_query.where(Car.drive_type == drive_type)
    if color:
        query = query.where(Car.color == color)
        count_query = count_query.where(Car.color == color)
    if dealer_name:
        query = query.where(Car.dealer_name == dealer_name)
        count_query = count_query.where(Car.dealer_name == dealer_name)
    if year_min is not None:
        query = query.where(Car.year >= year_min)
        count_query = count_query.where(Car.year >= year_min)
    if year_max is not None:
        query = query.where(Car.year <= year_max)
        count_query = count_query.where(Car.year <= year_max)
    if price_min is not None:
        query = query.where(Car.price_jpy >= price_min)
        count_query = count_query.where(Car.price_jpy >= price_min)
    if price_max is not None:
        query = query.where(Car.price_jpy <= price_max)
        count_query = count_query.where(Car.price_jpy <= price_max)
    if mileage_max is not None:
        query = query.where(Car.mileage_km <= mileage_max)
        count_query = count_query.where(Car.mileage_km <= mileage_max)
    if engine_min is not None:
        query = query.where(Car.engine_cc >= engine_min)
        count_query = count_query.where(Car.engine_cc >= engine_min)
    if engine_max is not None:
        query = query.where(Car.engine_cc <= engine_max)
        count_query = count_query.where(Car.engine_cc <= engine_max)
    if search:
        pattern = f"%{search}%"
        query = query.where(
            (Car.brand.ilike(pattern)) | (Car.model.ilike(pattern)) | (Car.grade.ilike(pattern))
        )
        count_query = count_query.where(
            (Car.brand.ilike(pattern)) | (Car.model.ilike(pattern)) | (Car.grade.ilike(pattern))
        )

    sort_column = {
        "price_jpy": Car.price_jpy,
        "year": Car.year,
        "mileage_km": Car.mileage_km,
        "created_at": Car.created_at,
    }[sort_by]

    order_func = desc if sort_order == "desc" else asc
    query = query.order_by(order_func(sort_column).nulls_last())

    total_result = await db.execute(count_query)
    total = total_result.scalar()

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)
    cars = result.scalars().all()

    total_pages = (total + page_size - 1) // page_size if total > 0 else 0

    return CarListResponse(
        items=[CarResponse.model_validate(c) for c in cars],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/filters", response_model=FiltersResponse)
async def get_filters(
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    brands = (await db.execute(
        select(Car.brand).distinct().where(Car.brand.isnot(None)).order_by(Car.brand)
    )).scalars().all()

    body_types = (await db.execute(
        select(Car.body_type).distinct().where(Car.body_type.isnot(None)).order_by(Car.body_type)
    )).scalars().all()

    fuel_types = (await db.execute(
        select(Car.fuel_type).distinct().where(Car.fuel_type.isnot(None)).order_by(Car.fuel_type)
    )).scalars().all()

    transmissions = (await db.execute(
        select(Car.transmission).distinct().where(Car.transmission.isnot(None)).order_by(Car.transmission)
    )).scalars().all()

    drive_types = (await db.execute(
        select(Car.drive_type).distinct().where(Car.drive_type.isnot(None)).order_by(Car.drive_type)
    )).scalars().all()

    colors = (await db.execute(
        select(Car.color).distinct().where(Car.color.isnot(None)).order_by(Car.color)
    )).scalars().all()

    dealers = (await db.execute(
        select(Car.dealer_name).distinct().where(Car.dealer_name.isnot(None)).order_by(Car.dealer_name)
    )).scalars().all()

    year_range = (await db.execute(
        select(func.min(Car.year), func.max(Car.year))
    )).one()

    price_range = (await db.execute(
        select(func.min(Car.price_jpy), func.max(Car.price_jpy))
    )).one()

    engine_range = (await db.execute(
        select(func.min(Car.engine_cc), func.max(Car.engine_cc))
    )).one()

    return FiltersResponse(
        brands=brands,
        body_types=body_types,
        fuel_types=fuel_types,
        transmissions=transmissions,
        drive_types=drive_types,
        colors=colors,
        dealers=dealers,
        year_min=year_range[0],
        year_max=year_range[1],
        price_min=price_range[0],
        price_max=price_range[1],
        engine_min=engine_range[0],
        engine_max=engine_range[1],
    )


@router.get("/{car_id}", response_model=CarResponse)
async def get_car(
    car_id: UUID,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    result = await db.execute(select(Car).where(Car.id == car_id))
    car = result.scalar_one_or_none()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return CarResponse.model_validate(car)
