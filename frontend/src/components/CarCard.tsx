'use client';

import Link from 'next/link';
import Image from 'next/image';
import { Car } from '@/lib/api';
import { useI18n, formatPriceMulti, formatMileageI18n } from '@/lib/i18n';
import { Calendar, Gauge, Cog, MapPin } from 'lucide-react';

export default function CarCard({ car }: { car: Car }) {
  const { tv } = useI18n();

  return (
    <Link href={`/cars/${car.id}`} className="card group block">
      <div className="relative aspect-[4/3] bg-gray-100 overflow-hidden">
        {car.thumbnail ? (
          <Image
            src={car.thumbnail}
            alt={`${car.brand} ${car.model}`}
            fill
            sizes="(max-width: 640px) 50vw, (max-width: 1280px) 33vw, 25vw"
            className="object-cover group-hover:scale-105 transition-transform duration-300"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-300">
            <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        )}
        {car.body_type && (
          <span className="absolute top-1.5 left-1.5 px-1.5 py-0.5 text-[10px] font-medium bg-black/60 text-white rounded backdrop-blur-sm z-10">
            {tv(car.body_type)}
          </span>
        )}
      </div>

      <div className="p-2.5 sm:p-3">
        <div className="mb-0.5">
          <span className="text-[10px] font-medium text-primary-600 uppercase tracking-wide">{car.brand}</span>
        </div>
        <h3 className="font-semibold text-gray-900 text-xs leading-tight line-clamp-1 mb-1 group-hover:text-primary-600 transition-colors">
          {car.model}
        </h3>

        <div className="text-sm font-bold text-primary-600 leading-tight">
          ¥{car.price_jpy?.toLocaleString() || '—'}
        </div>
        {car.price_jpy && (
          <p className="text-[10px] text-gray-400 mb-1.5">
            {formatPriceMulti(car.price_jpy)}
          </p>
        )}

        <div className="grid grid-cols-2 gap-1 text-[10px] text-gray-500">
          {car.year && (
            <div className="flex items-center gap-0.5">
              <Calendar size={9} />
              <span>{car.year}</span>
            </div>
          )}
          {car.mileage_km !== null && (
            <div className="flex items-center gap-0.5">
              <Gauge size={9} />
              <span>{formatMileageI18n(car.mileage_km)}</span>
            </div>
          )}
          {car.transmission && (
            <div className="flex items-center gap-0.5">
              <Cog size={9} />
              <span>{tv(car.transmission)}</span>
            </div>
          )}
          {car.location && (
            <div className="flex items-center gap-0.5">
              <MapPin size={9} />
              <span className="truncate">{car.location}</span>
            </div>
          )}
        </div>
      </div>
    </Link>
  );
}
