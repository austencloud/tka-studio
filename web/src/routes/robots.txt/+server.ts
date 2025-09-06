// import { PRIMARY_DOMAIN } from "$config/domains";
const PRIMARY_DOMAIN = "localhost:5173"; // Temporary fallback
import type { RequestHandler } from "./$types";

export const GET: RequestHandler = async () => {
  const robots = `User-agent: *
Allow: /

# Sitemap
Sitemap: ${PRIMARY_DOMAIN}/sitemap.xml

# Main application pages - high priority for indexing
Allow: /
Allow: /about
Allow: /constructor
Allow: /browse
Allow: /learn
Allow: /features
Allow: /getting-started

# Secondary pages
Allow: /word-card
Allow: /write

# Development tools - lower priority but still allowed
Allow: /metadata-tester
Allow: /animator

# Block irrelevant paths
Disallow: /api/
Disallow: /_app/
Disallow: /static/
Disallow: /.svelte-kit/
Disallow: /node_modules/

# Crawl delay for respectful crawling
Crawl-delay: 1

# Cache instruction
Cache-control: max-age=86400`;

  return new Response(robots, {
    headers: {
      "Content-Type": "text/plain",
      "Cache-Control": "public, max-age=86400",
    },
  });
};
