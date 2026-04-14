import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="text-center max-w-md">
        <p className="text-6xl font-bold text-primary-600 mb-3">404</p>
        <h2 className="text-lg font-bold text-gray-900 mb-2">Page not found</h2>
        <p className="text-gray-500 text-sm mb-5">
          The page you are looking for does not exist.
        </p>
        <Link href="/" className="btn-primary inline-block text-sm">
          Back to home
        </Link>
      </div>
    </div>
  );
}
