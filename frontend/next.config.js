/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '*.carsensor.net',
      },
    ],
  },
};

module.exports = nextConfig;
