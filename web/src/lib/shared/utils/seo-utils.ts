/**
 * SEO Link Utilities
 *
 * Utilities for creating special SEO links that bypass the normal
 * SPA behavior when needed (e.g., for sharing, email campaigns, etc.)
 */

interface SEOLinkOptions {
  tab?: string;
  section?: string;
  seoMode?: boolean;
}

/**
 * Generate a special SEO link that will redirect users to the SPA
 * but still provide SEO benefits
 */
export function createSEOLink(
  path: string,
  options: SEOLinkOptions = {}
): string {
  const { tab, section, seoMode = false } = options;

  if (seoMode) {
    // Return direct SEO page URL for bots/special cases
    return `/${path}`;
  }

  // Return main app URL with parameters for user redirection
  const params = new URLSearchParams();
  if (tab) params.set("tab", tab);
  if (section) params.set("section", section);

  const queryString = params.toString();
  return queryString ? `/?${queryString}` : "/";
}

/**
 * Create shareable links for different sections
 */
export const seoLinks = {
  about: () => createSEOLink("about", { tab: "about" }),
  features: () =>
    createSEOLink("features", { tab: "about", section: "features" }),
  gettingStarted: () =>
    createSEOLink("getting-started", {
      tab: "about",
      section: "getting-started",
    }),
  browse: () => createSEOLink("browse", { tab: "browse" }),
  constructor: () => createSEOLink("constructor", { tab: "construct" }),

  // SEO-only versions (for bots)
  aboutSEO: () => createSEOLink("about", { seoMode: true }),
  featuresSEO: () => createSEOLink("features", { seoMode: true }),
  gettingStartedSEO: () => createSEOLink("getting-started", { seoMode: true }),
  browseSEO: () => createSEOLink("browse", { seoMode: true }),
};

/**
 * Check if current request is from a search engine bot
 */
export function isSearchEngineBot(userAgent?: string): boolean {
  if (!userAgent) {
    userAgent = typeof navigator !== "undefined" ? navigator.userAgent : "";
  }

  const botPatterns = [
    /googlebot/i,
    /bingbot/i,
    /slurp/i,
    /duckduckbot/i,
    /baiduspider/i,
    /yandexbot/i,
    /facebookexternalhit/i,
    /twitterbot/i,
    /linkedinbot/i,
    /whatsapp/i,
    /telegrambot/i,
  ];

  return botPatterns.some((pattern) => pattern.test(userAgent));
}

/**
 * Enhanced redirect logic for SEO pages
 */
export function handleSEORedirect(
  targetTab: string,
  targetSection?: string
): void {
  if (typeof window === "undefined") return;

  // Check if this is a bot (don't redirect bots)
  if (isSearchEngineBot()) {
    return;
  }

  // Check referrer to see if user came from search engine
  const referrer = document.referrer;
  const fromSearchEngine =
    referrer.includes("google.") ||
    referrer.includes("bing.") ||
    referrer.includes("duckduckgo.") ||
    referrer === "";

  // Small delay to allow SEO crawlers to see content, then redirect users
  const delay = fromSearchEngine ? 200 : 100;

  setTimeout(() => {
    const params = new URLSearchParams();
    params.set("tab", targetTab);
    if (targetSection) params.set("section", targetSection);

    window.location.href = `/?${params.toString()}`;
  }, delay);
}
