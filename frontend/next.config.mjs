import { readFileSync } from "node:fs";

const { rewrites } = JSON.parse(
  readFileSync(new URL("./vercel.json", import.meta.url), "utf8")
);

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Use the same proxy routes locally and on Vercel.
  async rewrites() {
    return rewrites;
  },
};

export default nextConfig;
