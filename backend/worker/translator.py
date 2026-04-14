import re

BRAND_MAP: dict[str, str] = {
    "トヨタ": "Toyota",
    "ホンダ": "Honda",
    "日産": "Nissan",
    "マツダ": "Mazda",
    "スバル": "Subaru",
    "三菱": "Mitsubishi",
    "スズキ": "Suzuki",
    "ダイハツ": "Daihatsu",
    "レクサス": "Lexus",
    "いすゞ": "Isuzu",
    "光岡": "Mitsuoka",
    "日野": "Hino",
    "AMG": "AMG",
    "BMW": "BMW",
    "BMWアルピナ": "BMW Alpina",
    "メルセデス・ベンツ": "Mercedes-Benz",
    "メルセデスAMG": "Mercedes-AMG",
    "メルセデス・マイバッハ": "Mercedes-Maybach",
    "フォルクスワーゲン": "Volkswagen",
    "アウディ": "Audi",
    "ポルシェ": "Porsche",
    "ミニ": "MINI",
    "ボルボ": "Volvo",
    "プジョー": "Peugeot",
    "シトロエン": "Citroen",
    "ルノー": "Renault",
    "フィアット": "Fiat",
    "アルファロメオ": "Alfa Romeo",
    "アルファ　ロメオ": "Alfa Romeo",
    "アルファ ロメオ": "Alfa Romeo",
    "マセラティ": "Maserati",
    "フェラーリ": "Ferrari",
    "ランボルギーニ": "Lamborghini",
    "ロールスロイス": "Rolls-Royce",
    "ベントレー": "Bentley",
    "ジャガー": "Jaguar",
    "ランドローバー": "Land Rover",
    "アストンマーティン": "Aston Martin",
    "マクラーレン": "McLaren",
    "ロータス": "Lotus",
    "テスラ": "Tesla",
    "キャデラック": "Cadillac",
    "シボレー": "Chevrolet",
    "フォード": "Ford",
    "ジープ": "Jeep",
    "クライスラー": "Chrysler",
    "ダッジ": "Dodge",
    "リンカーン": "Lincoln",
    "ハマー": "Hummer",
    "ヒョンデ": "Hyundai",
    "起亜": "Kia",
    "BYD": "BYD",
    "ＢＭＷ": "BMW",
    "スマート": "Smart",
    "ＢＭＷＭ": "BMW M",
    "アバルト": "Abarth",
}

MODEL_MAP: dict[str, str] = {
    # Toyota
    "プリウス": "Prius",
    "アクア": "Aqua",
    "カローラ": "Corolla",
    "カローラアクシオ": "Corolla Axio",
    "カローラフィールダー": "Corolla Fielder",
    "カローラツーリング": "Corolla Touring",
    "カローラスポーツ": "Corolla Sport",
    "カローラクロス": "Corolla Cross",
    "カムリ": "Camry",
    "クラウン": "Crown",
    "クラウンアスリート": "Crown Athlete",
    "クラウンロイヤル": "Crown Royal",
    "クラウンマジェスタ": "Crown Majesta",
    "クラウンクロスオーバー": "Crown Crossover",
    "ヤリス": "Yaris",
    "ヤリスクロス": "Yaris Cross",
    "GRヤリス": "GR Yaris",
    "ヴィッツ": "Vitz",
    "シエンタ": "Sienta",
    "ルーミー": "Roomy",
    "ライズ": "Raize",
    "ハリアー": "Harrier",
    "RAV4": "RAV4",
    "ランドクルーザー": "Land Cruiser",
    "ランドクルーザー250": "Land Cruiser 250",
    "ランドクルーザープラド": "Land Cruiser Prado",
    "ランドクルーザー300": "Land Cruiser 300",
    "ヴェルファイア": "Vellfire",
    "アルファード": "Alphard",
    "ヴォクシー": "Voxy",
    "ノア": "Noah",
    "エスクァイア": "Esquire",
    "エスティマ": "Estima",
    "ハイエースバン": "HiAce Van",
    "ハイエース": "HiAce",
    "ハイラックス": "Hilux",
    "86": "86",
    "スープラ": "Supra",
    "C-HR": "C-HR",
    "bZ4X": "bZ4X",
    "パッソ": "Passo",
    "マークX": "Mark X",
    "センチュリー": "Century",
    "タンク": "Tank",
    "ポルテ": "Porte",
    "スペイド": "Spade",
    "ウィッシュ": "Wish",
    "アイシス": "Isis",
    "サクシード": "Succeed",
    "プロボックス": "Probox",
    # Honda
    "フィット": "Fit",
    "ヴェゼル": "Vezel",
    "フリード": "Freed",
    "ステップワゴン": "Step WGN",
    "オデッセイ": "Odyssey",
    "シビック": "Civic",
    "アコード": "Accord",
    "CR-V": "CR-V",
    "N-BOX": "N-BOX",
    "N-WGN": "N-WGN",
    "N-ONE": "N-ONE",
    "N-VAN": "N-VAN",
    "WR-V": "WR-V",
    "ZR-V": "ZR-V",
    "S660": "S660",
    "インサイト": "Insight",
    "グレイス": "Grace",
    "シャトル": "Shuttle",
    "ジェイド": "Jade",
    # Nissan
    "ノート": "Note",
    "ノートオーラ": "Note Aura",
    "セレナ": "Serena",
    "エクストレイル": "X-Trail",
    "キックス": "Kicks",
    "ジューク": "Juke",
    "リーフ": "Leaf",
    "スカイライン": "Skyline",
    "フェアレディZ": "Fairlady Z",
    "GT-R": "GT-R",
    "マーチ": "March",
    "デイズ": "Dayz",
    "デイズルークス": "Dayz Roox",
    "ルークス": "Roox",
    "モコ": "Moco",
    "エルグランド": "Elgrand",
    "ティアナ": "Teana",
    "フーガ": "Fuga",
    "シーマ": "Cima",
    "キャラバン": "Caravan",
    "NV350キャラバン": "NV350 Caravan",
    "アリア": "Ariya",
    "サクラ": "Sakura",
    # Mazda
    "デミオ": "Demio",
    "アクセラ": "Axela",
    "アクセラスポーツ": "Axela Sport",
    "アテンザ": "Atenza",
    "CX-3": "CX-3",
    "CX-30": "CX-30",
    "CX-5": "CX-5",
    "CX-8": "CX-8",
    "CX-60": "CX-60",
    "MAZDA2": "Mazda2",
    "MAZDA3": "Mazda3",
    "MAZDA6": "Mazda6",
    "ロードスター": "Roadster",
    "MX-30": "MX-30",
    # Subaru
    "インプレッサ": "Impreza",
    "インプレッサXV": "Impreza XV",
    "インプレッサスポーツ": "Impreza Sport",
    "XV": "XV",
    "フォレスター": "Forester",
    "レガシィ": "Legacy",
    "レガシィアウトバック": "Legacy Outback",
    "レガシィB4": "Legacy B4",
    "レヴォーグ": "Levorg",
    "WRX": "WRX",
    "BRZ": "BRZ",
    "クロストレック": "Crosstrek",
    "ソルテラ": "Solterra",
    # Suzuki
    "ジムニー": "Jimny",
    "ジムニーシエラ": "Jimny Sierra",
    "スイフト": "Swift",
    "スイフトスポーツ": "Swift Sport",
    "ハスラー": "Hustler",
    "スペーシア": "Spacia",
    "スペーシアカスタム": "Spacia Custom",
    "ワゴンR": "Wagon R",
    "アルト": "Alto",
    "アルトラパン": "Alto Lapin",
    "ソリオ": "Solio",
    "クロスビー": "Xbee",
    "エスクード": "Escudo",
    "エブリイ": "Every",
    "エブリイワゴン": "Every Wagon",
    # Daihatsu
    "タント": "Tanto",
    "タントカスタム": "Tanto Custom",
    "ムーヴ": "Move",
    "ムーヴカスタム": "Move Custom",
    "ムーヴキャンバス": "Move Canbus",
    "ミラ": "Mira",
    "ミライース": "Mira e:S",
    "ミラトコット": "Mira Tocot",
    "キャスト": "Cast",
    "コペン": "Copen",
    "ロッキー": "Rocky",
    "トール": "Thor",
    "ウェイク": "Wake",
    "アトレー": "Atrai",
    "ハイゼットカーゴ": "Hijet Cargo",
    "ハイゼットトラック": "Hijet Truck",
    # Mitsubishi
    "デリカD5": "Delica D:5",
    "デリカD:5": "Delica D:5",
    "アウトランダー": "Outlander",
    "エクリプスクロス": "Eclipse Cross",
    "RVR": "RVR",
    "eKワゴン": "eK Wagon",
    "eKクロス": "eK X",
    "eKスペース": "eK Space",
    "パジェロ": "Pajero",
    "パジェロミニ": "Pajero Mini",
    "ランサーエボリューション": "Lancer Evolution",
    # Lexus
    "IS": "IS",
    "ES": "ES",
    "LS": "LS",
    "NX": "NX",
    "RX": "RX",
    "UX": "UX",
    "LX": "LX",
    "LC": "LC",
    "RC": "RC",
    "CT": "CT",
    "GS": "GS",
    "GSハイブリッド": "GS Hybrid",
    "ISハイブリッド": "IS Hybrid",
    "RXハイブリッド": "RX Hybrid",
    "NXハイブリッド": "NX Hybrid",
    "LBX": "LBX",
    # Mercedes-Benz
    "Aクラス": "A-Class",
    "Bクラス": "B-Class",
    "Cクラス": "C-Class",
    "Eクラス": "E-Class",
    "Sクラス": "S-Class",
    "Gクラス": "G-Class",
    "CLAクラス": "CLA-Class",
    "CLSクラス": "CLS-Class",
    "GLAクラス": "GLA-Class",
    "GLBクラス": "GLB-Class",
    "GLCクラス": "GLC-Class",
    "GLEクラス": "GLE-Class",
    "GLSクラス": "GLS-Class",
    "GLC": "GLC",
    "GLE": "GLE",
    "GLA": "GLA",
    "GLB": "GLB",
    # BMW
    "1シリーズ": "1 Series",
    "2シリーズ": "2 Series",
    "2シリーズアクティブツアラー": "2 Series Active Tourer",
    "2シリーズグランツアラー": "2 Series Gran Tourer",
    "3シリーズ": "3 Series",
    "4シリーズ": "4 Series",
    "5シリーズ": "5 Series",
    "7シリーズ": "7 Series",
    "8シリーズ": "8 Series",
    "X1": "X1",
    "X2": "X2",
    "X3": "X3",
    "X4": "X4",
    "X5": "X5",
    "X6": "X6",
    "X7": "X7",
    "iX": "iX",
    "i3": "i3",
    "i4": "i4",
    # MINI
    "ミニ": "Mini",
    "ミニクラブマン": "Mini Clubman",
    "ミニクロスオーバー": "Mini Crossover",
    "ミニコンバーチブル": "Mini Convertible",
    # Volkswagen
    "ゴルフ": "Golf",
    "ポロ": "Polo",
    "ティグアン": "Tiguan",
    "パサート": "Passat",
    "トゥアレグ": "Touareg",
    "T-Roc": "T-Roc",
    "T-Cross": "T-Cross",
    "ID.4": "ID.4",
    # Volvo
    "XC40": "XC40",
    "XC60": "XC60",
    "XC90": "XC90",
    "V40": "V40",
    "V60": "V60",
    "V90": "V90",
    "S60": "S60",
    "S90": "S90",
    # Peugeot
    "208": "208",
    "308": "308",
    "2008": "2008",
    "3008": "3008",
    "5008": "5008",
    # Audi
    "A1": "A1",
    "A3": "A3",
    "A4": "A4",
    "A5": "A5",
    "A6": "A6",
    "A7": "A7",
    "A8": "A8",
    "Q2": "Q2",
    "Q3": "Q3",
    "Q5": "Q5",
    "Q7": "Q7",
    "Q8": "Q8",
    "e-tron": "e-tron",
    # Smart
    "フォーツー": "Fortwo",
    "フォーフォー": "Forfour",
    # Alfa Romeo
    "ジュリア": "Giulia",
    "ステルヴィオ": "Stelvio",
    "トナーレ": "Tonale",
    "ジュリエッタ": "Giulietta",
    "A7スポーツバック": "A7 Sportback",
    "NV200バネットバン": "NV200 Vanette Van",
    "イグニス": "Ignis",
    "エクシーガクロスオーバー7": "Exiga Crossover 7",
    "タフト": "Taft",
    "バモス": "Vamos",
    "フーガハイブリッド": "Fuga Hybrid",
    "ラフェスタハイウェイスター": "Lafesta Highway Star",
    "SAI": "SAI",
    "プレミオ": "Premio",
    "アリオン": "Allion",
    "ハイエースワゴン": "HiAce Wagon",
    "レジアスエース": "Regius Ace",
    "タウンエース": "Townace",
    "スペイド": "Spade",
    "エスクァイア": "Esquire",
    "マークII": "Mark II",
    "チェイサー": "Chaser",
    "ランドクルーザー70": "Land Cruiser 70",
    "ランドクルーザー80": "Land Cruiser 80",
    "ランドクルーザー100": "Land Cruiser 100",
    "ランドクルーザー200": "Land Cruiser 200",
    "FJクルーザー": "FJ Cruiser",
    "ピクシス": "Pixis",
    "アベンシス": "Avensis",
    "イスト": "Ist",
    "オーリス": "Auris",
    "カルディナ": "Caldina",
    "クルーガー": "Kluger",
    "ベルタ": "Belta",
    "ラクティス": "Ractis",
    "ヴァンガード": "Vanguard",
    "CR-Z": "CR-Z",
    "エリシオン": "Elysion",
    "エレメント": "Element",
    "クロスロード": "Crossroad",
    "ストリーム": "Stream",
    "ゼスト": "Zest",
    "ライフ": "Life",
    "ウイングロード": "Wingroad",
    "キューブ": "Cube",
    "ティーダ": "Tiida",
    "プレサージュ": "Presage",
    "ブルーバード": "Bluebird",
    "ムラーノ": "Murano",
    "ラティオ": "Latio",
    "デリカD3": "Delica D:3",
    "デリカD2": "Delica D:2",
    "アイ": "i",
    "コルト": "Colt",
    "ギャランフォルティス": "Galant Fortis",
    "AZワゴン": "AZ-Wagon",
    "フレア": "Flair",
    "フレアワゴン": "Flair Wagon",
    "プレマシー": "Premacy",
    "ビアンテ": "Biante",
    "MPV": "MPV",
    "R1": "R1",
    "R2": "R2",
    "ステラ": "Stella",
    "トレジア": "Trezia",
    "プレオ": "Pleo",
    "サンバー": "Sambar",
    "キャリイ": "Carry",
    "セルボ": "Cervo",
    "パレット": "Palette",
    "ラパン": "Lapin",
    "ランディ": "Landy",
    "MRワゴン": "MR Wagon",
    "コンテ": "Conte",
    "ブーン": "Boon",
    "MAX": "MAX",
    "テリオスキッド": "Terios Kid",
    "ムーヴラテ": "Move Latte",
    "SUV": "SUV",
}


def translate_model(jp: str | None) -> str | None:
    return translate(jp, MODEL_MAP)


BODY_TYPE_MAP: dict[str, str] = {
    "セダン": "Sedan",
    "ハッチバック": "Hatchback",
    "クーペ": "Coupe",
    "オープン": "Convertible",
    "ステーションワゴン": "Station Wagon",
    "ミニバン": "Minivan",
    "SUV・クロカン": "SUV",
    "クロカン・ＳＵＶ": "SUV",
    "クロカン・SUV": "SUV",
    "コンパクトカー": "Compact",
    "軽自動車": "Kei Car",
    "ピックアップトラック": "Pickup Truck",
    "バン": "Van",
    "バス": "Bus",
    "トラック": "Truck",
    "キャンピングカー": "Camper",
    "福祉車両": "Welfare Vehicle",
    "商用車": "Commercial",
}

FUEL_TYPE_MAP: dict[str, str] = {
    "ガソリン": "Gasoline",
    "レギュラー": "Gasoline",
    "ハイオク": "Premium Gasoline",
    "軽油": "Diesel",
    "ハイブリッド": "Hybrid",
    "電気": "Electric",
    "LPG": "LPG",
    "CNG": "CNG",
    "その他": "Other",
    "プラグインハイブリッド": "Plug-in Hybrid",
}

TRANSMISSION_MAP: dict[str, str] = {
    "AT": "Automatic",
    "CVT": "CVT",
    "MT": "Manual",
    "AT/CVT": "Automatic/CVT",
    "セミAT": "Semi-Automatic",
    "その他": "Other",
}

DRIVE_TYPE_MAP: dict[str, str] = {
    "2WD": "2WD",
    "4WD": "4WD",
    "FF": "FF",
    "FR": "FR",
    "MR": "MR",
    "RR": "RR",
}

COLOR_MAP: dict[str, str] = {
    "ホワイト": "White",
    "ブラック": "Black",
    "シルバー": "Silver",
    "グレー": "Gray",
    "レッド": "Red",
    "ブルー": "Blue",
    "グリーン": "Green",
    "イエロー": "Yellow",
    "オレンジ": "Orange",
    "ブラウン": "Brown",
    "ゴールド": "Gold",
    "ベージュ": "Beige",
    "パープル": "Purple",
    "ピンク": "Pink",
    "ワインレッド": "Wine Red",
    "ガンメタリック": "Gunmetal",
    "ダークブルー": "Dark Blue",
    "ライトブルー": "Light Blue",
    "パール": "Pearl",
    "ホワイトパール": "White Pearl",
    "ブラックメタリック": "Black Metallic",
    "シルバーメタリック": "Silver Metallic",
    "白": "White",
    "黒": "Black",
    "赤": "Red",
    "青": "Blue",
    "緑": "Green",
    "黄": "Yellow",
    "茶": "Brown",
    "紫": "Purple",
    "灰": "Gray",
    "真珠白": "Pearl White",
    "白真珠": "Pearl White",
    "真珠黒": "Pearl Black",
    "黒真珠": "Pearl Black",
    "真珠Ｍ": "Pearl Metallic",
    "真珠": "Pearl",
    "白黒": "White/Black",
    "白黒II": "White/Black II",
    "黒Ｍ": "Black Metallic",
    "銀Ｍ": "Silver Metallic",
    "灰Ｍ": "Gray Metallic",
    "銀": "Silver",
    "濃黒": "Dark Black",
    "灰黒II": "Charcoal II",
    "青Ｍ": "Blue Metallic",
    "青真珠": "Pearl Blue",
    "青黒II": "Blue Black II",
    "赤Ｍ": "Red Metallic",
    "赤灰II": "Red Gray II",
    "緑Ｍ": "Green Metallic",
    "深緑Ｍ": "Dark Green Metallic",
    "茶Ｍ": "Brown Metallic",
    "茶真珠": "Pearl Brown",
    "茶黒II": "Brown Black II",
    "薄茶": "Light Brown",
    "薄茶白": "Light Brown White",
    "薄茶Ｍ": "Light Brown Metallic",
    "薄銀": "Light Silver",
    "薄銀Ｍ": "Light Silver Metallic",
    "薄青II": "Light Blue II",
    "薄青Ｍ": "Light Blue Metallic",
    "紫Ｍ": "Purple Metallic",
    "紺真珠": "Pearl Navy",
    "桃": "Pink",
    "黄真珠": "Pearl Yellow",
    "黄黒": "Yellow/Black",
    "黒赤": "Black/Red",
}

REPAIR_HISTORY_MAP: dict[str, str] = {
    "なし": "None",
    "あり": "Yes",
    "修復歴あり": "Yes",
    "修復歴なし": "None",
}


def translate(value: str | None, mapping: dict[str, str]) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return mapping.get(value, value)


def translate_brand(jp: str | None) -> str | None:
    return translate(jp, BRAND_MAP)


def translate_body_type(jp: str | None) -> str | None:
    return translate(jp, BODY_TYPE_MAP)


def translate_fuel(jp: str | None) -> str | None:
    return translate(jp, FUEL_TYPE_MAP)


def translate_transmission(jp: str | None) -> str | None:
    if not jp:
        return None
    jp = jp.strip()
    exact = TRANSMISSION_MAP.get(jp)
    if exact:
        return exact
    if "セミAT" in jp or "セミオート" in jp:
        return "Semi-Automatic"
    if "CVT" in jp:
        return "CVT"
    if re.search(r'\dAT', jp):
        return "Automatic"
    if re.search(r'\dMT', jp):
        return "Manual"
    if "AT" in jp:
        return "Automatic"
    if "MT" in jp:
        return "Manual"
    return jp


def translate_drive(jp: str | None) -> str | None:
    return translate(jp, DRIVE_TYPE_MAP)


def translate_color(jp: str | None) -> str | None:
    return translate(jp, COLOR_MAP)


def translate_repair(jp: str | None) -> str | None:
    return translate(jp, REPAIR_HISTORY_MAP)


def parse_mileage(text: str | None) -> int | None:
    if not text:
        return None
    text = text.replace(",", "").replace(" ", "").strip()
    try:
        if "万" in text:
            num = float(text.replace("万km", "").replace("万", ""))
            return int(num * 10000)
        elif "km" in text:
            return int(text.replace("km", ""))
    except (ValueError, TypeError):
        pass
    return None


def parse_price_man(text: str | None) -> tuple[float | None, int | None]:
    if not text:
        return None, None
    text = text.replace(",", "").replace(" ", "").replace("　", "").strip()
    try:
        if "万円" in text:
            man = float(text.replace("万円", ""))
            return man, int(man * 10000)
        elif "億" in text:
            text = text.replace("億", "").replace("円", "")
            oku = float(text)
            return oku * 10000, int(oku * 100000000)
    except (ValueError, TypeError):
        pass
    return None, None


def parse_engine_cc(text: str | None) -> int | None:
    if not text:
        return None
    text = text.replace(",", "").replace("cc", "").replace("CC", "").strip()
    try:
        return int(text)
    except (ValueError, TypeError):
        return None


def parse_year(text: str | None) -> int | None:
    if not text:
        return None
    text = text.strip()
    try:
        if "年" in text:
            text = text.split("年")[0].strip()

        if text.startswith("令和"):
            era_year = int(text.replace("令和", "").strip())
            return 2018 + era_year
        elif text.startswith("平成"):
            era_year = int(text.replace("平成", "").strip())
            return 1988 + era_year
        elif text.startswith("昭和"):
            era_year = int(text.replace("昭和", "").strip())
            return 1925 + era_year

        year = int(text)
        if 1900 <= year <= 2100:
            return year
    except (ValueError, TypeError):
        pass
    return None
