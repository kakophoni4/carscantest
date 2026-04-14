import re
import logging
import asyncio
from functools import lru_cache

logger = logging.getLogger(__name__)

PREFECTURE_MAP: dict[str, str] = {
    "北海道": "Hokkaido",
    "青森県": "Aomori", "青森": "Aomori",
    "岩手県": "Iwate", "岩手": "Iwate",
    "宮城県": "Miyagi", "宮城": "Miyagi",
    "秋田県": "Akita", "秋田": "Akita",
    "山形県": "Yamagata", "山形": "Yamagata",
    "福島県": "Fukushima", "福島": "Fukushima",
    "茨城県": "Ibaraki", "茨城": "Ibaraki",
    "栃木県": "Tochigi", "栃木": "Tochigi",
    "群馬県": "Gunma", "群馬": "Gunma",
    "埼玉県": "Saitama", "埼玉": "Saitama",
    "千葉県": "Chiba", "千葉": "Chiba",
    "東京都": "Tokyo", "東京": "Tokyo",
    "神奈川県": "Kanagawa", "神奈川": "Kanagawa",
    "新潟県": "Niigata", "新潟": "Niigata",
    "富山県": "Toyama", "富山": "Toyama",
    "石川県": "Ishikawa", "石川": "Ishikawa",
    "福井県": "Fukui", "福井": "Fukui",
    "山梨県": "Yamanashi", "山梨": "Yamanashi",
    "長野県": "Nagano", "長野": "Nagano",
    "岐阜県": "Gifu", "岐阜": "Gifu",
    "静岡県": "Shizuoka", "静岡": "Shizuoka",
    "愛知県": "Aichi", "愛知": "Aichi",
    "三重県": "Mie", "三重": "Mie",
    "滋賀県": "Shiga", "滋賀": "Shiga",
    "京都府": "Kyoto", "京都": "Kyoto",
    "大阪府": "Osaka", "大阪": "Osaka",
    "兵庫県": "Hyogo", "兵庫": "Hyogo",
    "奈良県": "Nara", "奈良": "Nara",
    "和歌山県": "Wakayama", "和歌山": "Wakayama",
    "鳥取県": "Tottori", "鳥取": "Tottori",
    "島根県": "Shimane", "島根": "Shimane",
    "岡山県": "Okayama", "岡山": "Okayama",
    "広島県": "Hiroshima", "広島": "Hiroshima",
    "山口県": "Yamaguchi", "山口": "Yamaguchi",
    "徳島県": "Tokushima", "徳島": "Tokushima",
    "香川県": "Kagawa", "香川": "Kagawa",
    "愛媛県": "Ehime", "愛媛": "Ehime",
    "高知県": "Kochi", "高知": "Kochi",
    "福岡県": "Fukuoka", "福岡": "Fukuoka",
    "佐賀県": "Saga", "佐賀": "Saga",
    "長崎県": "Nagasaki", "長崎": "Nagasaki",
    "熊本県": "Kumamoto", "熊本": "Kumamoto",
    "大分県": "Oita", "大分": "Oita",
    "宮崎県": "Miyazaki", "宮崎": "Miyazaki",
    "鹿児島県": "Kagoshima", "鹿児島": "Kagoshima",
    "沖縄県": "Okinawa", "沖縄": "Okinawa",
}

COMMON_WORDS: dict[str, str] = {
    "中古車": "used car",
    "販売": "sales",
    "店": "shop",
    "本店": "main shop",
    "支店": "branch",
    "営業所": "office",
    "自動車": "automobile",
    "モータース": "motors",
    "カーズ": "cars",
    "カーセンター": "car center",
    "カーサービス": "car service",
    "ネッツ": "Netz",
    "カローラ": "Corolla",
    "株式会社": "Co., Ltd.",
    "(株)": "Co.",
    "（株）": "Co.",
    "有限会社": "Ltd.",
    "(有)": "Ltd.",
    "（有）": "Ltd.",
    "万km": "0km",
    "年式": "year",
    "走行距離": "mileage",
    "修復歴なし": "No repair history",
    "修復歴あり": "Repair history: Yes",
    "ワンオーナー": "One owner",
    "禁煙車": "Non-smoking",
    "記録簿": "Service records available",
    "保証付": "With warranty",
    "保証あり": "With warranty",
    "保証なし": "No warranty",
    "法定整備付": "With statutory maintenance",
    "法定整備別": "Statutory maintenance separate",
    "法定整備無": "No statutory maintenance",
    "整備込": "Maintenance included",
    "車検整備付": "Inspection maintenance included",
    "車検整備別": "Inspection maintenance separate",
    "車検整備無": "No inspection maintenance",
    "車検なし": "No inspection",
    "車検": "Inspection",
    "新車保証継承": "New car warranty transfer",
    "純正": "Genuine/OEM",
    "社外": "Aftermarket",
    "ナビ": "Navigation",
    "カーナビ": "Car navigation",
    "バックカメラ": "Rear camera",
    "ETC": "ETC",
    "ドライブレコーダー": "Dashcam",
    "ドラレコ": "Dashcam",
    "アルミホイール": "Alloy wheels",
    "スマートキー": "Smart key",
    "キーレス": "Keyless entry",
    "パワーシート": "Power seats",
    "シートヒーター": "Seat heater",
    "エアコン": "A/C",
    "オートエアコン": "Auto A/C",
    "クルーズコントロール": "Cruise control",
    "アダプティブクルーズ": "Adaptive cruise",
    "衝突被害軽減ブレーキ": "Collision mitigation braking",
    "衝突軽減": "Collision mitigation",
    "安全装備": "Safety equipment",
    "横滑り防止": "Stability control",
    "レーンアシスト": "Lane assist",
    "駐車支援": "Parking assist",
    "オートライト": "Auto lights",
    "LEDヘッドライト": "LED headlights",
    "LED": "LED",
    "フォグランプ": "Fog lights",
    "サンルーフ": "Sunroof",
    "ルーフレール": "Roof rails",
    "電動スライドドア": "Power sliding door",
    "両側電動スライドドア": "Both-side power sliding doors",
    "片側電動スライドドア": "One-side power sliding door",
    "Bluetooth": "Bluetooth",
    "USB": "USB",
    "フルセグ": "Full-seg TV",
    "地デジ": "Digital TV",
    "DVD": "DVD",
    "CD": "CD",
    "ミュージックサーバー": "Music server",
    "アイドリングストップ": "Idling stop",
    "エコカー減税": "Eco-car tax break",
    "ターボ": "Turbo",
    "スーパーチャージャー": "Supercharger",
    "4WD": "4WD",
    "AWD": "AWD",
    "2WD": "2WD",
}

_JP_CHAR_RE = re.compile(r'[\u3000-\u303F\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\uFF00-\uFFEF]')
_translation_cache: dict[str, str] = {}
_translator = None


def _has_japanese(text: str) -> bool:
    return bool(_JP_CHAR_RE.search(text))


def _get_translator():
    global _translator
    if _translator is None:
        try:
            from deep_translator import GoogleTranslator
            _translator = GoogleTranslator(source='ja', target='en')
        except Exception as e:
            logger.warning("Failed to init GoogleTranslator: %s", e)
    return _translator


def translate_location(text: str | None) -> str | None:
    if not text:
        return None
    result = text
    for jp, en in PREFECTURE_MAP.items():
        result = result.replace(jp, en)
    if not _has_japanese(result):
        return result.strip()
    parts = result.split()
    translated_parts = []
    for part in parts:
        if _has_japanese(part):
            t = _translate_text_cached(part)
            translated_parts.append(t if t else part)
        else:
            translated_parts.append(part)
    return " ".join(translated_parts).strip()


def translate_inspection(text: str | None) -> str | None:
    if not text:
        return None
    text = text.strip()
    m = re.match(r'(\d{4})\s*[\(（][A-Za-z]\d+[\)）]\s*年?\s*(\d{1,2})月?', text)
    if m:
        return f"{m.group(1)}/{m.group(2).zfill(2)}"
    m2 = re.match(r'(\d{4})\s*年?\s*(\d{1,2})月?', text)
    if m2:
        return f"{m2.group(1)}/{m2.group(2).zfill(2)}"
    if _has_japanese(text):
        return _translate_text_cached(text) or text
    return text


def translate_free_text(text: str | None) -> str | None:
    if not text or not _has_japanese(text):
        return text
    result = text
    for jp, en in COMMON_WORDS.items():
        result = result.replace(jp, en)
    if not _has_japanese(result):
        return result.strip()
    return _translate_text_cached(result) or text


def _translate_text_cached(text: str) -> str | None:
    if not text or not text.strip():
        return text
    text = text.strip()
    if text in _translation_cache:
        return _translation_cache[text]
    translator = _get_translator()
    if not translator:
        return None
    try:
        result = translator.translate(text)
        if result:
            _translation_cache[text] = result
            return result
    except Exception as e:
        logger.debug("Translation failed for '%s': %s", text[:50], e)
    return None


async def translate_car_fields(car: dict) -> dict:
    loop = asyncio.get_event_loop()

    if car.get("model") and _has_japanese(car["model"]):
        car["model"] = await loop.run_in_executor(
            None, translate_free_text, car["model"]
        ) or car["model"]

    if car.get("description") and _has_japanese(car["description"]):
        car["description"] = await loop.run_in_executor(
            None, translate_free_text, car["description"]
        )

    if car.get("grade") and _has_japanese(car["grade"]):
        car["grade"] = await loop.run_in_executor(
            None, translate_free_text, car["grade"]
        )

    if car.get("dealer_name") and _has_japanese(car["dealer_name"]):
        car["dealer_name"] = await loop.run_in_executor(
            None, translate_free_text, car["dealer_name"]
        )

    if car.get("location") and _has_japanese(car["location"]):
        car["location"] = await loop.run_in_executor(
            None, translate_location, car["location"]
        )

    if car.get("inspection_date") and _has_japanese(car["inspection_date"]):
        car["inspection_date"] = translate_inspection(car["inspection_date"])

    return car


async def translate_cars_batch(cars: list[dict]) -> list[dict]:
    for car in cars:
        try:
            await translate_car_fields(car)
            await asyncio.sleep(0.1)
        except Exception as e:
            logger.warning("Translation failed for car %s: %s", car.get("external_id"), e)
    return cars
