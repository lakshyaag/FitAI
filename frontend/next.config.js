/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config) => {
    config.externals = ["chrome-aws-lambda"];

    return config;
  },
};

module.exports = nextConfig;
