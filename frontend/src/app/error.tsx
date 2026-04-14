'use client';

import { useEffect } from 'react';
import { useI18n } from '@/lib/i18n';
import { AlertTriangle, RefreshCw } from 'lucide-react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  const { t } = useI18n();

  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="text-center max-w-md">
        <div className="inline-flex items-center justify-center w-14 h-14 rounded-full bg-red-100 text-red-500 mb-5">
          <AlertTriangle size={28} />
        </div>
        <h2 className="text-lg font-bold text-gray-900 mb-2">{t('somethingWrong')}</h2>
        <p className="text-gray-500 text-sm mb-5">{t('errorHint')}</p>
        <button onClick={reset} className="btn-primary inline-flex items-center gap-2 text-sm">
          <RefreshCw size={14} />
          {t('tryAgain')}
        </button>
      </div>
    </div>
  );
}
