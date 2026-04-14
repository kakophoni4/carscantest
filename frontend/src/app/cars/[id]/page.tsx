'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Image from 'next/image';
import { getCar, Car } from '@/lib/api';
import { useI18n, formatPriceMulti, formatMileageI18n } from '@/lib/i18n';
import AuthGuard from '@/components/AuthGuard';
import Header from '@/components/Header';
import {
  ArrowLeft, Calendar, Gauge, Wrench, MapPin, ExternalLink,
  ChevronLeft, ChevronRight, Fuel, Cog, Palette, Car as CarIcon, DoorOpen, Users
} from 'lucide-react';

function ImageGallery({ images, alt }: { images: string[]; alt: string }) {
  const [current, setCurrent] = useState(0);

  if (!images.length) {
    return (
      <div className="aspect-[16/10] bg-gray-100 rounded-xl flex items-center justify-center text-gray-300">
        <CarIcon size={48} />
      </div>
    );
  }

  return (
    <div className="space-y-2">
      <div className="relative aspect-[16/10] bg-gray-100 rounded-xl overflow-hidden">
        <Image
          src={images[current]}
          alt={`${alt} - ${current + 1}`}
          fill
          sizes="(max-width: 1024px) 100vw, 60vw"
          className="object-cover"
          priority={current === 0}
        />
        {images.length > 1 && (
          <>
            <button
              onClick={() => setCurrent((p) => (p > 0 ? p - 1 : images.length - 1))}
              className="absolute left-2 top-1/2 -translate-y-1/2 w-9 h-9 rounded-full bg-black/40 text-white flex items-center justify-center hover:bg-black/60 transition-colors z-10"
            >
              <ChevronLeft size={18} />
            </button>
            <button
              onClick={() => setCurrent((p) => (p < images.length - 1 ? p + 1 : 0))}
              className="absolute right-2 top-1/2 -translate-y-1/2 w-9 h-9 rounded-full bg-black/40 text-white flex items-center justify-center hover:bg-black/60 transition-colors z-10"
            >
              <ChevronRight size={18} />
            </button>
            <div className="absolute bottom-2 left-1/2 -translate-x-1/2 px-2.5 py-0.5 rounded-full bg-black/50 text-white text-[10px] z-10">
              {current + 1} / {images.length}
            </div>
          </>
        )}
      </div>

      {images.length > 1 && (
        <div className="flex gap-1.5 overflow-x-auto pb-1">
          {images.map((img, i) => (
            <button
              key={i}
              onClick={() => setCurrent(i)}
              className={`relative flex-shrink-0 w-16 h-12 rounded-lg overflow-hidden border-2 transition-colors ${
                i === current ? 'border-primary-500' : 'border-transparent hover:border-gray-300'
              }`}
            >
              <Image src={img} alt="" fill sizes="64px" className="object-cover" />
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

function CarDetailContent() {
  const { t, tv } = useI18n();
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const [car, setCar] = useState<Car | null>(null);
  const [loading, setLoading] = useState(true);

  const carId = params?.id;

  useEffect(() => {
    if (carId) {
      getCar(carId)
        .then(setCar)
        .catch(() => router.push('/'))
        .finally(() => setLoading(false));
    }
  }, [carId, router]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="flex items-center justify-center py-20">
          <div className="w-7 h-7 border-2 border-primary-600 border-t-transparent rounded-full animate-spin" />
        </div>
      </div>
    );
  }

  if (!car) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="text-center py-20">
          <h2 className="text-lg font-semibold text-gray-900">{t('carNotFound')}</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-6xl mx-auto px-3 sm:px-6 lg:px-8 py-4">
        <button
          onClick={() => router.back()}
          className="flex items-center gap-1.5 text-xs text-gray-500 hover:text-gray-700 mb-3 transition-colors"
        >
          <ArrowLeft size={14} />
          {t('backToListings')}
        </button>

        <div className="grid grid-cols-1 lg:grid-cols-5 gap-4">
          <div className="lg:col-span-3">
            <ImageGallery
              images={car.images || (car.thumbnail ? [car.thumbnail] : [])}
              alt={`${car.brand} ${car.model}`}
            />

            {car.description && (
              <div className="mt-4 bg-white rounded-xl border border-gray-100 shadow-sm p-4">
                <h3 className="font-semibold text-gray-900 text-sm mb-1.5">{t('description')}</h3>
                <p className="text-xs text-gray-600 leading-relaxed whitespace-pre-line">{car.description}</p>
              </div>
            )}
          </div>

          <div className="lg:col-span-2 space-y-3">
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-4">
              <div className="mb-0.5">
                <span className="text-[10px] font-medium text-primary-600 uppercase tracking-wide">{car.brand}</span>
              </div>
              <h1 className="text-lg font-bold text-gray-900 mb-0.5">{car.model}</h1>
              {car.grade && (
                <p className="text-xs text-gray-500 mb-3 line-clamp-2">{car.grade}</p>
              )}

              <div className="bg-primary-50 rounded-lg p-3 mb-3">
                <p className="text-xl font-bold text-primary-700">
                  ¥{car.price_jpy?.toLocaleString() || '—'}
                </p>
                {car.price_jpy && (
                  <p className="text-xs text-primary-500 mt-0.5">
                    {formatPriceMulti(car.price_jpy)}
                  </p>
                )}
                {car.price_man && (
                  <p className="text-[10px] text-primary-400 mt-0.5">{car.price_man}万円</p>
                )}
              </div>

              <a
                href={car.url}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-primary w-full flex items-center justify-center gap-2 text-xs"
              >
                <ExternalLink size={14} />
                {t('viewOnCarSensor')}
              </a>
            </div>

            <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-4">
              <h3 className="font-semibold text-gray-900 text-sm mb-2">{t('specifications')}</h3>
              <SpecRow icon={Calendar} label={t('year')} value={car.year?.toString()} />
              <SpecRow icon={Gauge} label={t('mileage')} value={car.mileage_km ? formatMileageI18n(car.mileage_km) : null} />
              <SpecRow icon={Cog} label={t('engine')} value={car.engine_cc ? `${car.engine_cc} cc` : null} />
              <SpecRow icon={Cog} label={t('transmission')} value={tv(car.transmission)} />
              <SpecRow icon={Fuel} label={t('fuel')} value={tv(car.fuel_type)} />
              <SpecRow icon={Cog} label={t('drive')} value={tv(car.drive_type)} />
              <SpecRow icon={CarIcon} label={t('body')} value={tv(car.body_type)} />
              <SpecRow icon={Palette} label={t('colorLabel')} value={tv(car.color)} />
              {car.color_jp && car.color !== car.color_jp && (
                <SpecRow icon={Palette} label={t('colorJp')} value={car.color_jp} />
              )}
              <SpecRow icon={DoorOpen} label={t('doors')} value={car.doors?.toString()} />
              <SpecRow icon={Users} label={t('seats')} value={car.seats?.toString()} />
              <SpecRow icon={Wrench} label={t('inspection')} value={car.inspection_date} />
              <SpecRow icon={Wrench} label={t('repairHistory')} value={tv(car.repair_history)} />
            </div>

            {(car.location || car.dealer_name) && (
              <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-4">
                <h3 className="font-semibold text-gray-900 text-sm mb-2">{t('dealer')}</h3>
                {car.dealer_name && (
                  <p className="text-xs font-medium text-gray-900">{car.dealer_name}</p>
                )}
                {car.location && (
                  <p className="text-xs text-gray-500 flex items-center gap-1 mt-1">
                    <MapPin size={12} />
                    {car.location}
                  </p>
                )}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

function SpecRow({ icon: Icon, label, value }: { icon: React.ElementType; label: string; value: string | null | undefined }) {
  if (!value) return null;
  return (
    <div className="flex items-center gap-2.5 py-2.5 border-b border-gray-50 last:border-0">
      <div className="w-7 h-7 rounded-lg bg-gray-50 flex items-center justify-center text-gray-400 flex-shrink-0">
        <Icon size={14} />
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-[10px] text-gray-400">{label}</p>
        <p className="text-xs font-medium text-gray-900 truncate">{value}</p>
      </div>
    </div>
  );
}

export default function CarDetailPage() {
  return (
    <AuthGuard>
      <CarDetailContent />
    </AuthGuard>
  );
}
