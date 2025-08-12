import type { RequestHandler } from "./$types";

const site = "https://thekineticalphabet.com"; // Replace with your actual domain

export const GET: RequestHandler = async () => {
  const robots = `User-agent: *
Allow: /

# Sitemap
Sitemap: ${site}/sitemap.xml

# Crawl-delay for respectful crawling
Crawl-delay: 1`;

  return new Response(robots, {
    headers: {
      "Content-Type": "text/plain",
      "Cache-Control": "max-age=86400",
    },
  });
};
