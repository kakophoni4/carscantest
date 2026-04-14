'use client';

import { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';

export type Lang = 'en' | 'ru';

const translations = {
  en: {
    appName: 'CarScaner',
    appSubtitle: 'Japanese Used Cars Database',
    signIn: 'Sign In',
    signOut: 'Sign Out',
    username: 'Username',
    password: 'Password',
    enterUsername: 'Enter username',
    enterPassword: 'Enter password',
    invalidCredentials: 'Invalid username or password',
    backToListings: 'Back to listings',
    viewOnCarSensor: 'View on CarSensor',
    specifications: 'Specifications',
    dealer: 'Dealer',
    description: 'Description',
    carsFound: 'cars found',
    noData: 'No data',
    noCarsFound: 'No cars found',
    noCarsHint: 'Try adjusting your filters or check back later',
    carNotFound: 'Car not found',
    priceOnRequest: 'Price on request',
    tryAgain: 'Try again',
    failedToLoad: 'Failed to load cars',
    somethingWrong: 'Something went wrong',
    errorHint: 'An unexpected error occurred. Please try again.',
    pageNotFound: 'Page not found',
    pageNotFoundHint: 'The page you are looking for does not exist.',
    backToHome: 'Back to home',
    filters: 'Filters',
    clearAll: 'Clear all',
    search: 'Search brand, model...',
    brand: 'Brand',
    allBrands: 'All brands',
    bodyType: 'Body type',
    allTypes: 'All types',
    transmission: 'Transmission',
    allTransmissions: 'All',
    fuelType: 'Fuel type',
    allFuelTypes: 'All',
    driveType: 'Drive',
    allDriveTypes: 'All',
    color: 'Color',
    allColors: 'All colors',
    dealerFilter: 'Dealer',
    allDealers: 'All dealers',
    yearFrom: 'Year from',
    yearTo: 'Year to',
    priceFrom: 'Price from (¥)',
    priceTo: 'Price to (¥)',
    maxMileage: 'Max mileage (km)',
    engineFrom: 'Engine from (cc)',
    engineTo: 'Engine to (cc)',
    newestFirst: 'Newest first',
    oldestFirst: 'Oldest first',
    priceLowHigh: 'Price ↑',
    priceHighLow: 'Price ↓',
    yearNewest: 'Year ↓',
    yearOldest: 'Year ↑',
    mileageLowHigh: 'Mileage ↑',
    mileageHighLow: 'Mileage ↓',
    year: 'Year',
    mileage: 'Mileage',
    engine: 'Engine',
    fuel: 'Fuel',
    drive: 'Drive',
    body: 'Body type',
    colorLabel: 'Color',
    colorJp: 'Color (JP)',
    inspection: 'Inspection',
    repairHistory: 'Repair history',
    doors: 'Doors',
    seats: 'Seats',
    min: 'Min',
    max: 'Max',
    langName: 'English',
  },
  ru: {
    appName: 'CarScaner',
    appSubtitle: 'База б/у авто из Японии',
    signIn: 'Войти',
    signOut: 'Выйти',
    username: 'Логин',
    password: 'Пароль',
    enterUsername: 'Введите логин',
    enterPassword: 'Введите пароль',
    invalidCredentials: 'Неверный логин или пароль',
    backToListings: 'Назад к списку',
    viewOnCarSensor: 'Смотреть на CarSensor',
    specifications: 'Характеристики',
    dealer: 'Дилер',
    description: 'Описание',
    carsFound: 'авто найдено',
    noData: 'Нет данных',
    noCarsFound: 'Ничего не найдено',
    noCarsHint: 'Попробуйте изменить фильтры или зайдите позже',
    carNotFound: 'Автомобиль не найден',
    priceOnRequest: 'Цена по запросу',
    tryAgain: 'Попробовать снова',
    failedToLoad: 'Не удалось загрузить',
    somethingWrong: 'Что-то пошло не так',
    errorHint: 'Произошла ошибка. Попробуйте снова.',
    pageNotFound: 'Страница не найдена',
    pageNotFoundHint: 'Такой страницы не существует.',
    backToHome: 'На главную',
    filters: 'Фильтры',
    clearAll: 'Сбросить',
    search: 'Марка, модель...',
    brand: 'Марка',
    allBrands: 'Все марки',
    bodyType: 'Кузов',
    allTypes: 'Все типы',
    transmission: 'КПП',
    allTransmissions: 'Все',
    fuelType: 'Топливо',
    allFuelTypes: 'Все',
    driveType: 'Привод',
    allDriveTypes: 'Все',
    color: 'Цвет',
    allColors: 'Все цвета',
    dealerFilter: 'Дилер',
    allDealers: 'Все дилеры',
    yearFrom: 'Год от',
    yearTo: 'Год до',
    priceFrom: 'Цена от (¥)',
    priceTo: 'Цена до (¥)',
    maxMileage: 'Макс. пробег (км)',
    engineFrom: 'Двигатель от (cc)',
    engineTo: 'Двигатель до (cc)',
    newestFirst: 'Сначала новые',
    oldestFirst: 'Сначала старые',
    priceLowHigh: 'Цена ↑',
    priceHighLow: 'Цена ↓',
    yearNewest: 'Год ↓',
    yearOldest: 'Год ↑',
    mileageLowHigh: 'Пробег ↑',
    mileageHighLow: 'Пробег ↓',
    year: 'Год',
    mileage: 'Пробег',
    engine: 'Двигатель',
    fuel: 'Топливо',
    drive: 'Привод',
    body: 'Кузов',
    colorLabel: 'Цвет',
    colorJp: 'Цвет (яп.)',
    inspection: 'Техосмотр',
    repairHistory: 'Ремонт',
    doors: 'Двери',
    seats: 'Мест',
    min: 'Мин',
    max: 'Макс',
    langName: 'Русский',
  },
} as const;

export type TranslationKey = keyof typeof translations.en;

const valueTranslationsRu: Record<string, string> = {
  'Automatic': 'Автомат',
  'Manual': 'Механика',
  'CVT': 'Вариатор',
  'Semi-Automatic': 'Полуавтомат',
  'Sedan': 'Седан',
  'Hatchback': 'Хэтчбек',
  'Coupe': 'Купе',
  'Convertible': 'Кабриолет',
  'Station Wagon': 'Универсал',
  'Minivan': 'Минивэн',
  'SUV': 'Внедорожник',
  'Compact': 'Компакт',
  'Kei Car': 'Кей-кар',
  'Pickup Truck': 'Пикап',
  'Van': 'Фургон',
  'Bus': 'Автобус',
  'Truck': 'Грузовик',
  'Camper': 'Кемпер',
  'Commercial': 'Коммерческий',
  'Gasoline': 'Бензин',
  'Premium Gasoline': 'Бензин (премиум)',
  'Diesel': 'Дизель',
  'Hybrid': 'Гибрид',
  'Electric': 'Электро',
  'Plug-in Hybrid': 'Плагин-гибрид',
  'LPG': 'Газ (LPG)',
  '2WD': 'Передний (2WD)',
  '4WD': 'Полный (4WD)',
  'FF': 'Передний (FF)',
  'FR': 'Задний (FR)',
  'MR': 'Средний (MR)',
  'White': 'Белый',
  'Black': 'Чёрный',
  'Silver': 'Серебристый',
  'Gray': 'Серый',
  'Red': 'Красный',
  'Blue': 'Синий',
  'Green': 'Зелёный',
  'Yellow': 'Жёлтый',
  'Orange': 'Оранжевый',
  'Brown': 'Коричневый',
  'Gold': 'Золотой',
  'Beige': 'Бежевый',
  'Purple': 'Фиолетовый',
  'Pink': 'Розовый',
  'Pearl White': 'Перламутровый белый',
  'Pearl Blue': 'Перламутровый синий',
  'Black Metallic': 'Чёрный металлик',
  'Silver Metallic': 'Серебристый металлик',
  'Gray Metallic': 'Серый металлик',
  'Blue Metallic': 'Синий металлик',
  'Red Metallic': 'Красный металлик',
  'Green Metallic': 'Зелёный металлик',
  'Brown Metallic': 'Коричневый металлик',
  'Dark Green Metallic': 'Тёмно-зелёный металлик',
  'Light Silver': 'Светло-серебристый',
  'Light Brown Metallic': 'Светло-коричневый металлик',
  'Light Blue Metallic': 'Голубой металлик',
  'Wine Red': 'Бордо',
  'Gunmetal': 'Тёмно-серый',
  'Pearl': 'Перламутровый',
  'None': 'Нет',
  'Yes': 'Да',
  'Other': 'Другое',
  'Welfare Vehicle': 'Спецтранспорт',
  'White Pearl': 'Белый перламутр',
  'Pearl Black': 'Чёрный перламутр',
  'Pearl Metallic': 'Перламутровый металлик',
  'White/Black': 'Белый/Чёрный',
  'White/Black II': 'Белый/Чёрный II',
  'Dark Black': 'Тёмно-чёрный',
  'Charcoal II': 'Тёмно-серый II',
  'Pearl Brown': 'Коричневый перламутр',
  'Brown Black II': 'Коричнево-чёрный II',
  'Light Brown': 'Светло-коричневый',
  'Light Brown White': 'Светло-коричнево-белый',
  'Light Silver Metallic': 'Светло-серебристый металлик',
  'Light Blue II': 'Голубой II',
  'Purple Metallic': 'Фиолетовый металлик',
  'Pearl Navy': 'Тёмно-синий перламутр',
  'Pearl Yellow': 'Жёлтый перламутр',
  'Yellow/Black': 'Жёлтый/Чёрный',
  'Black/Red': 'Чёрный/Красный',
  'Dark Blue': 'Тёмно-синий',
  'Light Blue': 'Голубой',
  'Blue Black II': 'Сине-чёрный II',
  'Red Gray II': 'Красно-серый II',
};

interface I18nContextType {
  lang: Lang;
  setLang: (lang: Lang) => void;
  t: (key: TranslationKey) => string;
  tv: (value: string | null | undefined) => string;
}

const I18nContext = createContext<I18nContextType | null>(null);

export function I18nProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>('en');

  useEffect(() => {
    const saved = localStorage.getItem('lang') as Lang | null;
    if (saved === 'en' || saved === 'ru') {
      setLangState(saved);
    }
  }, []);

  const setLang = useCallback((newLang: Lang) => {
    setLangState(newLang);
    localStorage.setItem('lang', newLang);
  }, []);

  const t = useCallback((key: TranslationKey): string => {
    return translations[lang][key] || translations.en[key] || key;
  }, [lang]);

  const tv = useCallback((value: string | null | undefined): string => {
    if (!value) return '';
    if (lang === 'ru' && valueTranslationsRu[value]) {
      return valueTranslationsRu[value];
    }
    return value;
  }, [lang]);

  return (
    <I18nContext.Provider value={{ lang, setLang, t, tv }}>
      {children}
    </I18nContext.Provider>
  );
}

export function useI18n() {
  const ctx = useContext(I18nContext);
  if (!ctx) throw new Error('useI18n must be used within I18nProvider');
  return ctx;
}

const JPY_TO_USD = 0.0067;
const JPY_TO_RUB = 0.58;

export function formatPriceMulti(priceJpy: number | null): string {
  if (!priceJpy) return '';
  const usd = Math.round(priceJpy * JPY_TO_USD).toLocaleString();
  const rub = Math.round(priceJpy * JPY_TO_RUB).toLocaleString();
  return `~$${usd} / ~₽${rub}`;
}

export function formatMileageI18n(km: number | null): string {
  if (!km) return '—';
  return `${km.toLocaleString()} km`;
}
