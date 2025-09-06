// import { PRIMARY_DOMAIN } from "$config/domains";
const PRIMARY_DOMAIN = "localhost:5173"; // Temporary fallback
import type { RequestHandler } from "./$types";

const pages = [
  // Main Application Pages (High Priority)
  {
    url: "",
    priority: "1.0",
    changefreq: "weekly",
    description: "TKA - The Kinetic Constructor | Home",
  },
  {
    url: "about",
    priority: "0.9",
    changefreq: "monthly",
    description: "About TKA - Revolutionary Flow Arts Tool",
  },
  {
    url: "constructor",
    priority: "0.9",
    changefreq: "weekly",
    description: "Flow Arts Constructor - Sequence Builder",
  },
  {
    url: "browse",
    priority: "0.8",
    changefreq: "weekly",
    description: "Browse Flow Arts Gallery - Sequence Library",
  },
  {
    url: "learn",
    priority: "0.8",
    changefreq: "weekly",
    description: "Learn Flow Arts - Comprehensive Tutorials",
  },

  // Secondary Pages (Medium Priority)
  {
    url: "features",
    priority: "0.7",
    changefreq: "monthly",
    description: "TKA Features - Advanced Animation Tools",
  },
  {
    url: "getting-started",
    priority: "0.7",
    changefreq: "monthly",
    description: "Getting Started with TKA - Tutorial",
  },
  {
    url: "word-card",
    priority: "0.6",
    changefreq: "monthly",
    description: "Sequence Cards - Movement Notation",
  },
  {
    url: "write",
    priority: "0.6",
    changefreq: "monthly",
    description: "Flow Arts Composer - Advanced Editor",
  },

  // Development Tools (Lower Priority - but still indexed)
  {
    url: "animator",
    priority: "0.3",
    changefreq: "monthly",
    description: "Animator - Development Tool",
  },

  {
    url: "metadata-tester",
    priority: "0.3",
    changefreq: "monthly",
    description: "Metadata Tester - Development Tool",
  },
];

export const GET: RequestHandler = async () => {
  const domain = PRIMARY_DOMAIN;
  const now = new Date().toISOString().split("T")[0];

  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  ${pages
    .map(
      (page) => `
  <url>
    <loc>${domain}/${page.url}</loc>
    <lastmod>${now}</lastmod>
    <changefreq>${page.changefreq}</changefreq>
    <priority>${page.priority}</priority>
  </url>`
    )
    .join("")}
</urlset>`;

  return new Response(sitemap, {
    headers: {
      "Content-Type": "application/xml",
      "Cache-Control": "public, max-age=3600",
    },
  });
};
