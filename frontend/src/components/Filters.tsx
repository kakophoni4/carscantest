'use client';

import { useState, useEffect, useCallback } from 'react';
import { getFilters, FiltersResponse, CarFilters } from '@/lib/api';
import { useI18n } from '@/lib/i18n';
import { Search, SlidersHorizontal, X } from 'lucide-react';

interface Props {
  filters: CarFilters;
  onChange: (filters: CarFilters) => void;
}

export default function Filters({ filters, onChange }: Props) {
  const { t, tv } = useI18n();
  const [availableFilters, setAvailableFilters] = useState<FiltersResponse | null>(null);
  const [showMobile, setShowMobile] = useState(false);
  const [searchInput, setSearchInput] = useState(filters.search || '');

  useEffect(() => {
    getFilters().then(setAvailableFilters).catch(console.error);
  }, []);

  const update = useCallback(
    (key: keyof CarFilters, value: string | number | undefined) => {
      onChange({ ...filters, [key]: value || undefined, page: 1 });
    },
    [filters, onChange]
  );

  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchInput !== (filters.search || '')) {
        update('search', searchInput || undefined);
      }
    }, 400);
    return () => clearTimeout(timer);
  }, [searchInput, filters.search, update]);

  const clearAll = () => {
    setSearchInput('');
    onChange({ page: 1, page_size: filters.page_size, sort_by: filters.sort_by, sort_order: filters.sort_order });
  };

  const hasActiveFilters = filters.brand || filters.body_type || filters.transmission ||
    filters.fuel_type || filters.drive_type || filters.color || filters.dealer_name ||
    filters.year_min || filters.year_max || filters.price_min || filters.price_max ||
    filters.mileage_max || filters.engine_min || filters.engine_max || filters.search;

  const filterContent = (
    <div className="space-y-3">
      <div className="relative">
        <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          placeholder={t('search')}
          className="input-field pl-9 text-sm"
        />
      </div>

      <div>
        <label className="block text-[11px] font-medium text-gray-500 mb-1">{t('brand')}</label>
        <select value={filters.brand || ''} onChange={(e) => update('brand', e.target.value)} className="select-field text-sm">
          <option value="">{t('allBrands')}</option>
          {availableFilters?.brands.map((b) => <option key={b} value={b}>{b}</option>)}
        </select>
      </div>

      <div>
        <label className="block text-[11px] font-medium text-gray-500 mb-1">{t('bodyType')}</label>
        <select value={filters.body_type || ''} onChange={(e) => update('body_type', e.target.value)} className="select-field text-sm">
          <option value="">{t('allTypes')}</option>
          {availableFilters?.body_types.map((b) => <option key={b} value={b}>{tv(b)}</option>)}
        </select>
      </div>

      <div>
        <label className="block text-[11px] font-medium text-gray-500 mb-1">{t('transmission')}</label>
        <select value={filters.transmission || ''} onChange={(e) => update('transmission', e.target.value)} className="select-field text-sm">
          <option value="">{t('allTransmissions')}</option>
          {availableFilters?.transmissions.map((v) => <option key={v} value={v}>{tv(v)}</option>)}
        </select>
      </div>

      <div>
        <label className="block text-[11px] font-medium text-gray-500 mb-1">{t('fuelType')}</label>
        <select value={filters.fuel_type || ''} onChange={(e) => update('fuel_type', e.target.value)} className="select-field text-sm">
          <option value="">{t('allFuelTypes')}</option>
          {availableFilters?.fuel_types.map((f) => <option key={f} value={f}>{tv(f)}</option>)}
        </select>
      </div>

      <div>
        <label className="block text-[11px] font-medium text-gray-500 mb-1">{t('driveType')}</label>
        <select value={filters.drive_type || ''} onChange={(e) => update('drive_type', e.target.value)} className="select-field text-sm">
          <option value="">{t('allDriveTypes')}</option>
          {availableFilters?.drive_types.map((d) => <option key={d} value={d}>{tv(d)}</option>)}
        </select>
      </div>

      <div>
        <label className="block text-[11px] font-medium text-gray-500 mb-1">{t('color')}</label>
        <select value={filters.color || ''} onChange={(e) => update('color', e.target.value)} className="select-field text-sm">
          <option value="">{t('allColors')}</option>
          {availableFilters?.colors.map((c) => <option key={c} value={c}>{tv(c)}</option>)}
        </select>
      </div>

      <div>
        <label className="block text-[11px] font-medium text-gray-500 mb-1">{t('dealerFilter')}</label>
        <select value={filters.dealer_name || ''} onChange={(e) => update('dealer_name', e.target.value)} className="select-field text-sm">
          <option value="">{t('allDealers')}</option>
          {availableFilters?.dealers.map((d) => <option key={d} value={d}>{d}</option>)}
        </select>
      </div>

      <div className="grid grid-cols-2 gap-2">
        <div>
          <label className="block text-[11px] font-medium text-gray-500 mb-1">{t('yearFrom')}</label>
          <input type="number" min={1990} max={2027} value={filters.year_min || ''} onChange={(e) => update('year_min', e.target.value ? Number(e.target.value) : undefined)} placeholder={t('min')} className="input-field text-sm" />
        </div>
        <div>
          <label className="block text-[11px] font-medium text-gray-500 mb-1">{t('yearTo')}</label>
          <input type="number" min={1990} max={2027} value={filters.year_max || ''} onChange={(e) => update('year_max', e.target.value ? Number(e.target.value) : undefined)} placeholder={t('max')} className="input-field text-sm" />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-2">
        <div>
          <label className="block text-[11px] font-medium text-gray-500 mb-1">{t('priceFrom')}</label>
          <input type="number" step={100000} value={filters.price_min || ''} onChange={(e) => update('price_min', e.target.value ? Number(e.target.value) : undefined)} placeholder={t('min')} className="input-field text-sm" />
        </div>
        <div>
          <label className="block text-[11px] font-medium text-gray-500 mb-1">{t('priceTo')}</label>
          <input type="number" step={100000} value={filters.price_max || ''} onChange={(e) => update('price_max', e.target.value ? Number(e.target.value) : undefined)} placeholder={t('max')} className="input-field text-sm" />
        </div>
      </div>

      <div>
        <label className="block text-[11px] font-medium text-gray-500 mb-1">{t('maxMileage')}</label>
        <input type="number" step={10000} value={filters.mileage_max || ''} onChange={(e) => update('mileage_max', e.target.value ? Number(e.target.value) : undefined)} placeholder="100000" className="input-field text-sm" />
      </div>

      <div className="grid grid-cols-2 gap-2">
        <div>
          <label className="block text-[11px] font-medium text-gray-500 mb-1">{t('engineFrom')}</label>
          <input type="number" step={100} value={filters.engine_min || ''} onChange={(e) => update('engine_min', e.target.value ? Number(e.target.value) : undefined)} placeholder={t('min')} className="input-field text-sm" />
        </div>
        <div>
          <label className="block text-[11px] font-medium text-gray-500 mb-1">{t('engineTo')}</label>
          <input type="number" step={100} value={filters.engine_max || ''} onChange={(e) => update('engine_max', e.target.value ? Number(e.target.value) : undefined)} placeholder={t('max')} className="input-field text-sm" />
        </div>
      </div>

      {hasActiveFilters && (
        <button onClick={clearAll} className="btn-secondary w-full text-xs flex items-center justify-center gap-1.5 py-2">
          <X size={12} />
          {t('clearAll')}
        </button>
      )}
    </div>
  );

  return (
    <>
      <aside className="hidden lg:block w-60 flex-shrink-0">
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-3.5 sticky top-16 max-h-[calc(100vh-5rem)] overflow-y-auto">
          <h2 className="text-sm font-semibold text-gray-900 mb-3 flex items-center gap-2">
            <SlidersHorizontal size={14} />
            {t('filters')}
          </h2>
          {filterContent}
        </div>
      </aside>

      <div className="lg:hidden fixed bottom-4 right-4 z-50">
        <button
          onClick={() => setShowMobile(true)}
          className="btn-primary rounded-full w-12 h-12 flex items-center justify-center shadow-lg"
        >
          <SlidersHorizontal size={20} />
        </button>
      </div>

      {showMobile && (
        <div className="lg:hidden fixed inset-0 z-50">
          <div className="absolute inset-0 bg-black/40" onClick={() => setShowMobile(false)} />
          <div className="absolute right-0 top-0 bottom-0 w-80 max-w-[90vw] bg-white shadow-xl overflow-y-auto p-4">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-semibold text-gray-900 flex items-center gap-2">
                <SlidersHorizontal size={14} />
                {t('filters')}
              </h2>
              <button onClick={() => setShowMobile(false)} className="p-1 hover:bg-gray-100 rounded-lg">
                <X size={18} />
              </button>
            </div>
            {filterContent}
          </div>
        </div>
      )}
    </>
  );
}
