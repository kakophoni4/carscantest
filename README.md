# CarScaner

Парсер и каталог б/у авто с carsensor.net.

Скрапер ходит на сайт раз в час, собирает машины (марка, модель, год, пробег, цена, фото, тип топлива, привод и т.д.), переводит японские термины на английский через словарь + автоперевод (Google Translate) и складывает в PostgreSQL. Для каждой машины дополнительно парсится детальная страница для получения расширенных характеристик. Поверх этого стоит API на FastAPI и фронт на Next.js с поддержкой EN/RU.

## Как запустить

Нужен Docker.

```bash
docker compose up -d
```

Подождать пару минут, пока воркер прогонит первый скрейп (парсит 15 страниц + детали каждой машины + автоперевод).

- Фронт: http://localhost:3000
- API: http://localhost:8000/api
- Swagger: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

Логин: `admin` / `admin123`

## Запуск тестов

```bash
cd backend
pip install -r requirements.txt
pytest -v
```

Тесты покрывают авторизацию, фильтрацию, пагинацию, сортировку и переводчик.

## Что внутри

```
backend/
  app/             FastAPI приложение (роутеры, модели, авторизация)
  worker/          скрапер + планировщик + словарь JP->EN + автоперевод
  alembic/         миграции БД
  tests/           pytest тесты
frontend/          Next.js 14, Tailwind, zustand, i18n (EN/RU)
render.yaml        конфиг для деплоя на Render.com
docker-compose.yml
```

## Стек

- Python 3.12, FastAPI, SQLAlchemy 2 (async), asyncpg
- PostgreSQL 16
- httpx + BeautifulSoup4 (парсинг), lxml
- deep-translator (автоперевод JP->EN через Google Translate)
- APScheduler (расписание)
- Alembic (миграции)
- Next.js 14 (App Router), Tailwind CSS, next/image
- JWT авторизация (python-jose + bcrypt)
- Docker + Docker Compose

## Фичи

- Скрапинг ~450 авто (15 страниц) каждый час
- Детальный парсинг: тип топлива, привод, двери, места
- Перевод японского: словарь (~700 терминов) + автоперевод через Google Translate
- Японского текста на сайте < 1%
- Фильтры: марка, кузов, КПП, топливо, привод, цвет, дилер, год, цена, пробег, объем двигателя
- Сортировка по цене, году, пробегу, дате добавления
- Поиск по марке/модели
- Пагинация (16 на страницу)
- Цены в иенах + приблизительно в долларах и рублях
- Локализация EN/RU (переключатель в хедере)
- Перевод значений фильтров (Automatic -> Автомат, Sedan -> Седан и т.д.)
- Адаптивная верстка: 2 колонки на мобильных, 3-4 на десктопе
- Мобильные фильтры через выдвижную панель
- Скелетоны при загрузке, обработка ошибок
- Защита от дублей в скрапере (по external_id + url)
- GZip сжатие, логирование запросов

## API

`POST /api/auth/login` - получить токен, тело `{"username": "admin", "password": "admin123"}`

`GET /api/auth/me` - текущий юзер (нужен Bearer токен)

`GET /api/cars` - список авто, поддерживает query-параметры:
- `page`, `page_size` - пагинация
- `brand`, `body_type`, `fuel_type`, `transmission`, `drive_type`, `color`, `dealer_name` - фильтры
- `year_min`, `year_max`, `price_min`, `price_max`, `mileage_max`, `engine_min`, `engine_max` - диапазоны
- `search` - поиск по бренду/модели
- `sort_by` (price_jpy, year, mileage_km, created_at), `sort_order` (asc, desc)

`GET /api/cars/filters` - доступные значения фильтров из БД

`GET /api/cars/{id}` - одна машина по uuid

`GET /api/health` - healthcheck

Все эндпоинты кроме login и health требуют `Authorization: Bearer <token>`.

## Скрапер

Парсит carsensor.net/usedcar, вытаскивает из HTML карточки машин. Для каждой дополнительно заходит на детальную страницу за расширенными данными. После парсинга все японские тексты (описания, дилеры, локации, комплектации) автоматически переводятся на английский через Google Translate с кешированием.

Словарь в `worker/translator.py` покрывает бренды, модели (~200+), типы кузова, топливо, КПП, привод, цвета, историю ремонта. Автоперевод в `worker/auto_translate.py` дополнительно переводит свободный текст и содержит словарь 47 префектур Японии + ~90 автомобильных терминов.

Настраивается через env `SCRAPER_MAX_PAGES` и `SCRAPER_INTERVAL_MINUTES`.

## Деплой

Проект готов к деплою на Render.com через `render.yaml` (Blueprint). Достаточно подключить репозиторий и нажать deploy.

Для других платформ используйте `docker-compose.yml`, не забудьте задать env переменные.

## Env переменные

- `DATABASE_URL` - строка подключения к постгресу
- `JWT_SECRET` - секрет для подписи токенов
- `SCRAPER_MAX_PAGES` - сколько страниц парсить (по умолчанию 15)
- `SCRAPER_INTERVAL_MINUTES` - интервал между запусками (по умолчанию 60)
- `CORS_ORIGINS` - разрешённые origins для CORS
