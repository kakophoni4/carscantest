from worker.translator import (
    translate_brand, translate_body_type, translate_fuel,
    translate_color, translate_repair,
    parse_mileage, parse_price_man, parse_engine_cc, parse_year,
)


def test_translate_brand_known():
    assert translate_brand("トヨタ") == "Toyota"
    assert translate_brand("ホンダ") == "Honda"
    assert translate_brand("マツダ") == "Mazda"
    assert translate_brand("メルセデス・ベンツ") == "Mercedes-Benz"


def test_translate_brand_unknown():
    assert translate_brand("何か") == "何か"


def test_translate_brand_none():
    assert translate_brand(None) is None


def test_translate_body_type():
    assert translate_body_type("セダン") == "Sedan"
    assert translate_body_type("SUV・クロカン") == "SUV"
    assert translate_body_type("軽自動車") == "Kei Car"


def test_translate_fuel():
    assert translate_fuel("ガソリン") == "Gasoline"
    assert translate_fuel("軽油") == "Diesel"
    assert translate_fuel("ハイブリッド") == "Hybrid"


def test_translate_color():
    assert translate_color("白") == "White"
    assert translate_color("黒") == "Black"
    assert translate_color("ホワイトパール") == "White Pearl"


def test_translate_repair():
    assert translate_repair("なし") == "None"
    assert translate_repair("あり") == "Yes"


def test_parse_mileage():
    assert parse_mileage("5.2万km") == 52000
    assert parse_mileage("1000km") == 1000
    assert parse_mileage(None) is None
    assert parse_mileage("") is None


def test_parse_price_man():
    man, jpy = parse_price_man("150万円")
    assert man == 150.0
    assert jpy == 1500000

    man, jpy = parse_price_man("29.8万円")
    assert man == 29.8
    assert jpy == 298000

    man, jpy = parse_price_man(None)
    assert man is None
    assert jpy is None


def test_parse_engine_cc():
    assert parse_engine_cc("2000cc") == 2000
    assert parse_engine_cc("660CC") == 660
    assert parse_engine_cc("1,500cc") == 1500
    assert parse_engine_cc(None) is None


def test_parse_year_western():
    assert parse_year("2024") == 2024
    assert parse_year("2020年") == 2020


def test_parse_year_japanese_era():
    assert parse_year("令和6") == 2024
    assert parse_year("令和1") == 2019
    assert parse_year("平成30") == 2018
    assert parse_year("平成1") == 1989


def test_parse_year_none():
    assert parse_year(None) is None
    assert parse_year("") is None
