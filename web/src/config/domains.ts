/**
 * Domain Config for TKA
 *
 * Handles multiple domains and SEO settings
 */

// Primary domain (canonical)
export const PRIMARY_DOMAIN = "https://thekineticalphabet.com";

// Secondary domains (will redirect to primary)
export const SECONDARY_DOMAINS = [
  "https://kineticalphabet.com",
  "https://www.thekineticalphabet.com",
  "https://www.kineticalphabet.com",
];

// All valid domains
export const ALL_DOMAINS = [PRIMARY_DOMAIN, ...SECONDARY_DOMAINS];

/**
 * Get the canonical URL for a given path
 */
export function getCanonicalURL(path: string): string {
  // Remove leading slash if present to avoid double slashes
  const cleanPath = path.startsWith("/") ? path.slice(1) : path;
  return `${PRIMARY_DOMAIN}/${cleanPath}`;
}

/**
 * Check if current domain should redirect to primary
 */
export function shouldRedirectToPrimary(currentOrigin: string): boolean {
  return SECONDARY_DOMAINS.some(
    (domain) => currentOrigin === new URL(domain).origin
  );
}

/**
 * Get redirect URL for domain consolidation
 */
export function getRedirectURL(currentURL: string): string {
  const url = new URL(currentURL);
  return `${PRIMARY_DOMAIN}${url.pathname}${url.search}${url.hash}`;
}

/**
 * Domain-specific meta tags
 */
export const SEO_CONFIG = {
  siteName: "TKA - The Kinetic Alphabet",
  description:
    "Revolutionary browser-based tool for creating flow arts sequences",
  keywords: "flow arts, notation, vtg, tka",
  author: "Austen Cloud",
  language: "en",
  type: "website",
};
