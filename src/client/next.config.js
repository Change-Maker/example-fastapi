/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  rewrites: async () => {
    return [
      {
        source: '/:path*',
        destination:
          process.env.NODE_ENV === 'development'
            ? 'http://localhost:3001/:path*'
            : 'http://fastapi-app:3001/:path*',
      },
      {
        source: '/docs',
        destination:
          process.env.NODE_ENV === 'development'
            ? 'http://localhost:3001/docs'
            : 'http://fastapi-app:3001/docs',
      },
      {
        source: '/openapi.json',
        destination:
          process.env.NODE_ENV === 'development'
            ? 'http://localhost:3001/openapi.json'
            : 'http://fastapi-app:3001/openapi.json',
      },
    ];
  },
};

module.exports = nextConfig;
