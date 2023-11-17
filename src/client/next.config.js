/** @type {import('next').NextConfig} */
const nextConfig = {
  rewrites: async () => {
    return [
      {
        source: '/:path*',
        destination: 'http://localhost:3001/:path*',
          // process.env.NODE_ENV === 'development'
          //   ? 'http://localhost:3001/:path*'
          //   : '/',
      },
      {
        source: '/docs',
        destination: 'http://localhost:3001/docs',
          // process.env.NODE_ENV === 'development'
          //   ? 'http://localhost:3001/docs'
          //   : '/docs',
      },
      {
        source: '/openapi.json',
        destination: 'http://localhost:3001/openapi.json',
          // process.env.NODE_ENV === 'development'
          //   ? 'http://localhost:3001/openapi.json'
          //   : '/openapi.json',
      },
    ];
  },
};

module.exports = nextConfig;
