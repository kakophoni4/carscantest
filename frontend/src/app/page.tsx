'use client';

import { useState, useEffect, useCallback } from 'react';
import { getCars, CarListResponse, CarFilters } from '@/lib/api';
import { useI18n } from '@/lib/i18n';
import AuthGuard from '@/components/AuthGuard';
import Header from '@/components/Header';
import CarCard from '@/components/CarCard';
import Filters from '@/components/Filters';
import Pagination from '@/components/Pagination';
import { ArrowUpDown } from 'lucide-react';

function CardSkeleton() {
  return (
    <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
      <div className="aspect-[4/3] bg-gray-200 animate-pulse" />
      <div className="p-3 space-y-2">
        <div className="h-2.5 w-12 bg-gray-200 rounded animate-pulse" />
        <div className="h-3 w-3/4 bg-gray-200 rounded animate-pulse" />
        <div className="h-4 w-20 bg-gray-200 rounded animate-pulse" />
        <div className="grid grid-cols-2 gap-1.5">
          <div className="h-2.5 w-14 bg-gray-100 rounded animate-pulse" />
          <div className="h-2.5 w-16 bg-gray-100 rounded animate-pulse" />
        </div>
      </div>
    </div>
  );
}

function CarsPage() {
  const { t } = useI18n();
  const [data, setData] = useState<CarListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<CarFilters>({
    page: 1,
    page_size: 16,
    sort_by: 'created_at',
    sort_order: 'desc',
  });

  const fetchCars = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await getCars(filters);
      setData(result);
    } catch (err) {
      const msg = err instanceof Error ? err.message : t('failedToLoad');
      setError(msg);
    } finally {
      setLoading(false);
    }
  }, [filters, t]);

  useEffect(() => {
    fetchCars();
  }, [fetchCars]);

  const handleFiltersChange = (newFilters: CarFilters) => {
    setFilters(newFilters);
  };

  const handlePageChange = (page: number) => {
    setFilters((prev) => ({ ...prev, page }));
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 py-4">
        <div className="flex gap-5">
          <Filters filters={filters} onChange={handleFiltersChange} />

          <div className="flex-1 min-w-0">
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm px-3 py-2.5 mb-3 flex items-center justify-between">
              <p className="text-xs text-gray-500">
                {loading ? (
                  <span className="inline-block h-3.5 w-24 bg-gray-200 rounded animate-pulse align-middle" />
                ) : data ? (
                  <>
                    <span className="font-semibold text-gray-900">{data.total.toLocaleString()}</span>{' '}
                    {t('carsFound')}
                  </>
                ) : (
                  t('noData')
                )}
              </p>

              <div className="flex items-center gap-1.5">
                <ArrowUpDown size={12} className="text-gray-400" />
                <select
                  value={`${filters.sort_by}_${filters.sort_order}`}
                  onChange={(e) => {
                    const val = e.target.value;
                    const lastIdx = val.lastIndexOf('_');
                    const sortBy = val.slice(0, lastIdx);
                    const sortOrder = val.slice(lastIdx + 1);
                    setFilters((prev) => ({ ...prev, sort_by: sortBy, sort_order: sortOrder, page: 1 }));
                  }}
                  className="text-xs border-0 bg-transparent text-gray-700 font-medium focus:ring-0 cursor-pointer"
                >
                  <option value="created_at_desc">{t('newestFirst')}</option>
                  <option value="created_at_asc">{t('oldestFirst')}</option>
                  <option value="price_jpy_asc">{t('priceLowHigh')}</option>
                  <option value="price_jpy_desc">{t('priceHighLow')}</option>
                  <option value="year_desc">{t('yearNewest')}</option>
                  <option value="year_asc">{t('yearOldest')}</option>
                  <option value="mileage_km_asc">{t('mileageLowHigh')}</option>
                  <option value="mileage_km_desc">{t('mileageHighLow')}</option>
                </select>
              </div>
            </div>

            {error ? (
              <div className="text-center py-16">
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-red-100 text-red-500 mb-3">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                  </svg>
                </div>
                <h3 className="text-base font-medium text-gray-900 mb-1">{t('failedToLoad')}</h3>
                <p className="text-gray-500 text-xs mb-3">{error}</p>
                <button onClick={fetchCars} className="btn-primary text-xs px-4 py-2">
                  {t('tryAgain')}
                </button>
              </div>
            ) : loading ? (
              <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
                {Array.from({ length: 8 }).map((_, i) => (
                  <CardSkeleton key={i} />
                ))}
              </div>
            ) : data && data.items.length > 0 ? (
              <>
                <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
                  {data.items.map((car) => (
                    <CarCard key={car.id} car={car} />
                  ))}
                </div>
                <Pagination
                  page={data.page}
                  totalPages={data.total_pages}
                  onChange={handlePageChange}
                />
              </>
            ) : (
              <div className="text-center py-16">
                <div className="text-gray-300 mb-3">
                  <svg className="w-14 h-14 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 className="text-base font-medium text-gray-900 mb-1">{t('noCarsFound')}</h3>
                <p className="text-gray-500 text-xs">{t('noCarsHint')}</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default function Home() {
  return (
    <AuthGuard>
      <CarsPage />
    </AuthGuard>
  );
}
