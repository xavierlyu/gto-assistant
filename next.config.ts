import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true
  },
  assetPrefix: process.env.NODE_ENV === 'production' ? '/gto-assistant' : '',
  basePath: process.env.NODE_ENV === 'production' ? '/gto-assistant' : '',
};

export default nextConfig;
