'use client';

import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/auth';
import { useI18n, Lang } from '@/lib/i18n';
import { Car, LogOut } from 'lucide-react';

export default function Header() {
  const router = useRouter();
  const { logout } = useAuthStore();
  const { lang, setLang, t } = useI18n();

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14">
          <a href="/" className="flex items-center gap-2.5 text-primary-600 hover:text-primary-700 transition-colors">
            <div className="w-8 h-8 rounded-lg bg-primary-600 text-white flex items-center justify-center">
              <Car size={18} />
            </div>
            <span className="text-base font-bold text-gray-900">{t('appName')}</span>
          </a>

          <div className="flex items-center gap-2">
            <select
              value={lang}
              onChange={(e) => setLang(e.target.value as Lang)}
              className="text-xs border border-gray-200 rounded-lg px-2 py-1.5 bg-white text-gray-700 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 cursor-pointer"
            >
              <option value="en">🇬🇧 English</option>
              <option value="ru">🇷🇺 Русский</option>
            </select>
            <button
              onClick={handleLogout}
              className="flex items-center gap-1.5 px-2.5 py-1.5 text-xs text-gray-500 hover:text-gray-700 hover:bg-gray-50 rounded-lg transition-colors"
            >
              <LogOut size={14} />
              <span className="hidden sm:inline">{t('signOut')}</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
