/** @type {import('next').NextConfig} */
const nextConfig = {
  // Disable strict mode for development
  reactStrictMode: true,
  // Ensure proper handling of trailing slashes
  trailingSlash: false,
  // Image optimization configuration
  images: {
    domains: [],
    remotePatterns: [],
  },
  // Use Webpack instead of Turbopack for stability
  // Turbopack can be enabled via CLI flag: next dev --turbo
}

module.exports = nextConfig
