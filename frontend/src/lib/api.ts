import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && typeof window !== 'undefined') {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface Car {
  id: string;
  external_id: string;
  brand: string;
  brand_jp: string | null;
  model: string;
  model_jp: string | null;
  grade: string | null;
  year: number | null;
  mileage_km: number | null;
  price_jpy: number | null;
  price_man: number | null;
  engine_cc: number | null;
  transmission: string | null;
  drive_type: string | null;
  fuel_type: string | null;
  color: string | null;
  color_jp: string | null;
  body_type: string | null;
  doors: number | null;
  seats: number | null;
  inspection_date: string | null;
  repair_history: string | null;
  location: string | null;
  dealer_name: string | null;
  url: string;
  thumbnail: string | null;
  images: string[] | null;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface CarListResponse {
  items: Car[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface FiltersResponse {
  brands: string[];
  body_types: string[];
  fuel_types: string[];
  transmissions: string[];
  drive_types: string[];
  colors: string[];
  dealers: string[];
  year_min: number | null;
  year_max: number | null;
  price_min: number | null;
  price_max: number | null;
  engine_min: number | null;
  engine_max: number | null;
}

export interface CarFilters {
  page?: number;
  page_size?: number;
  brand?: string;
  body_type?: string;
  fuel_type?: string;
  transmission?: string;
  drive_type?: string;
  color?: string;
  dealer_name?: string;
  year_min?: number;
  year_max?: number;
  price_min?: number;
  price_max?: number;
  mileage_max?: number;
  engine_min?: number;
  engine_max?: number;
  search?: string;
  sort_by?: string;
  sort_order?: string;
}

export async function login(username: string, password: string): Promise<string> {
  const { data } = await api.post('/auth/login', { username, password });
  return data.access_token;
}

export async function getMe() {
  const { data } = await api.get('/auth/me');
  return data;
}

export async function getCars(filters: CarFilters = {}): Promise<CarListResponse> {
  const params = Object.fromEntries(
    Object.entries(filters).filter(([, v]) => v !== undefined && v !== '' && v !== null)
  );
  const { data } = await api.get('/cars', { params });
  return data;
}

export async function getCar(id: string): Promise<Car> {
  const { data } = await api.get(`/cars/${id}`);
  return data;
}

export async function getFilters(): Promise<FiltersResponse> {
  const { data } = await api.get('/cars/filters');
  return data;
}

export default api;
