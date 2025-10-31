/**
 * SeoService Tests
 *
 * Comprehensive test suite for the SeoService.
 * Tests SEO link generation, meta tag creation, bot detection, and redirect handling.
 */

import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { SeoService } from "../../../src/lib/shared/foundation/services/implementations/SeoService";

describe("SeoService", () => {
  let service: SeoService;

  beforeEach(() => {
    service = new SeoService();
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.useRealTimers();
  });

  // ============================================================================
  // SEO LINK GENERATION TESTS
  // ============================================================================

  describe("createSEOLink", () => {
    it("should create basic SEO link without options", () => {
      const link = service.createSEOLink("about");
      expect(link).toBe("/");
    });

    it("should create link with tab parameter", () => {
      const link = service.createSEOLink("about", { tab: "learn" });
      expect(link).toBe("/?tab=learn");
    });

    it("should create link with section parameter", () => {
      const link = service.createSEOLink("about", { section: "tutorial" });
      expect(link).toBe("/?section=tutorial");
    });

    it("should create link with both tab and section", () => {
      const link = service.createSEOLink("about", {
        tab: "learn",
        section: "tutorial",
      });
      expect(link).toBe("/?tab=learn&section=tutorial");
    });

    it("should return direct path in SEO mode", () => {
      const link = service.createSEOLink("about", { seoMode: true });
      expect(link).toBe("/about");
    });

    it("should ignore tab/section in SEO mode", () => {
      const link = service.createSEOLink("about", {
        tab: "learn",
        section: "tutorial",
        seoMode: true,
      });
      expect(link).toBe("/about");
    });

    it("should handle empty path", () => {
      const link = service.createSEOLink("");
      expect(link).toBe("/");
    });

    it("should handle path with leading slash", () => {
      const link = service.createSEOLink("/about", { seoMode: true });
      expect(link).toBe("//about");
    });
  });

  // ============================================================================
  // META TAG GENERATION TESTS
  // ============================================================================

  describe("generateMetaTags", () => {
    it("should generate default meta tags", () => {
      const tags = service.generateMetaTags({});

      expect(tags.title).toBe("TKA Constructor - The Kinetic Alphabet");
      expect(tags.description).toBe(
        "Create visual movement sequences with The Kinetic Alphabet"
      );
      expect(tags["og:title"]).toBe("TKA Constructor - The Kinetic Alphabet");
      expect(tags["og:description"]).toBe(
        "Create visual movement sequences with The Kinetic Alphabet"
      );
      expect(tags["og:type"]).toBe("website");
      expect(tags["twitter:card"]).toBe("summary_large_image");
    });

    it("should use custom title", () => {
      const tags = service.generateMetaTags({
        title: "Custom Title",
      });

      expect(tags.title).toBe("Custom Title");
      expect(tags["og:title"]).toBe("Custom Title");
      expect(tags["twitter:title"]).toBe("Custom Title");
    });

    it("should use custom description", () => {
      const tags = service.generateMetaTags({
        description: "Custom description",
      });

      expect(tags.description).toBe("Custom description");
      expect(tags["og:description"]).toBe("Custom description");
      expect(tags["twitter:description"]).toBe("Custom description");
    });

    it("should include keywords when provided", () => {
      const tags = service.generateMetaTags({
        keywords: ["flow arts", "notation", "tka"],
      });

      expect(tags.keywords).toBe("flow arts, notation, tka");
    });

    it("should not include keywords when empty", () => {
      const tags = service.generateMetaTags({
        keywords: [],
      });

      expect(tags.keywords).toBeUndefined();
    });

    it("should include og:image when provided", () => {
      const tags = service.generateMetaTags({
        ogImage: "https://example.com/image.png",
      });

      expect(tags["og:image"]).toBe("https://example.com/image.png");
      expect(tags["twitter:image"]).toBe("https://example.com/image.png");
    });

    it("should include canonical URL when provided", () => {
      const tags = service.generateMetaTags({
        canonicalUrl: "https://example.com/page",
      });

      expect(tags["canonical"]).toBe("https://example.com/page");
    });

    it("should generate complete meta tags with all options", () => {
      const tags = service.generateMetaTags({
        title: "Test Page",
        description: "Test description",
        keywords: ["test", "page"],
        ogImage: "https://example.com/image.png",
        canonicalUrl: "https://example.com/test",
      });

      expect(tags.title).toBe("Test Page");
      expect(tags.description).toBe("Test description");
      expect(tags.keywords).toBe("test, page");
      expect(tags["og:image"]).toBe("https://example.com/image.png");
      expect(tags["canonical"]).toBe("https://example.com/test");
    });
  });

  // ============================================================================
  // BOT DETECTION TESTS
  // ============================================================================

  describe("isBotRequest", () => {
    it("should detect all search engine and social media bots", () => {
      const bots = [
        "Mozilla/5.0 (compatible; Googlebot/2.1)",
        "Mozilla/5.0 (compatible; bingbot/2.0)",
        "Mozilla/5.0 (compatible; Yahoo! Slurp)",
        "DuckDuckBot/1.0",
        "Mozilla/5.0 (compatible; Baiduspider/2.0)",
        "Mozilla/5.0 (compatible; YandexBot/3.0)",
        "facebookexternalhit/1.1",
        "Twitterbot/1.0",
        "LinkedInBot/1.0",
        "Pinterest/0.2",
      ];
      bots.forEach((bot) => {
        expect(service.isBotRequest(bot)).toBe(true);
      });
    });

    it("should not detect regular browsers", () => {
      expect(
        service.isBotRequest(
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0"
        )
      ).toBe(false);
    });

    it("should not detect mobile browsers", () => {
      expect(
        service.isBotRequest(
          "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0) Safari/604.1"
        )
      ).toBe(false);
    });

    it("should be case insensitive", () => {
      expect(service.isBotRequest("GOOGLEBOT/2.1")).toBe(true);
      expect(service.isBotRequest("googlebot/2.1")).toBe(true);
    });

    it("should return false for empty user agent", () => {
      expect(service.isBotRequest("")).toBe(false);
    });

    it("should return false for undefined user agent", () => {
      expect(service.isBotRequest(undefined)).toBe(false);
    });

    it("should use navigator.userAgent when no argument provided", () => {
      // Mock navigator
      Object.defineProperty(global.navigator, "userAgent", {
        value: "Mozilla/5.0 (compatible; Googlebot/2.1)",
        writable: true,
        configurable: true,
      });

      expect(service.isBotRequest()).toBe(true);
    });
  });

  // ============================================================================
  // SEO REDIRECT HANDLING TESTS
  // ============================================================================

  describe("handleSEORedirect", () => {
    beforeEach(() => {
      // Mock window.location with a writable href property
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      delete (window as any).location;
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (window as any).location = {
        href: "",
      };

      // Mock document.referrer
      Object.defineProperty(document, "referrer", {
        value: "",
        writable: true,
        configurable: true,
      });
    });

    afterEach(() => {
      // Clean up mocked location
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      delete (window as any).location;
      // Restore to jsdom's default location
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (window as any).location = new URL("http://localhost:3000");
    });

    it("should not redirect bots", () => {
      Object.defineProperty(global.navigator, "userAgent", {
        value: "Googlebot/2.1",
        writable: true,
        configurable: true,
      });

      service.handleSEORedirect("learn");
      vi.runAllTimers();

      expect(window.location.href).toBe("");
    });

    it("should redirect users to tab", () => {
      Object.defineProperty(global.navigator, "userAgent", {
        value: "Mozilla/5.0 Chrome/91.0",
        writable: true,
        configurable: true,
      });

      service.handleSEORedirect("learn");
      vi.runAllTimers();

      expect(window.location.href).toBe("/?tab=learn");
    });

    it("should redirect with tab and section", () => {
      Object.defineProperty(global.navigator, "userAgent", {
        value: "Mozilla/5.0 Chrome/91.0",
        writable: true,
        configurable: true,
      });

      service.handleSEORedirect("learn", "tutorial");
      vi.runAllTimers();

      expect(window.location.href).toBe("/?tab=learn&section=tutorial");
    });

    it("should use longer delay for search engine referrers", () => {
      Object.defineProperty(global.navigator, "userAgent", {
        value: "Mozilla/5.0 Chrome/91.0",
        writable: true,
        configurable: true,
      });
      Object.defineProperty(document, "referrer", {
        value: "https://www.google.com/search",
        writable: true,
        configurable: true,
      });

      service.handleSEORedirect("learn");

      // Should not redirect before 200ms
      vi.advanceTimersByTime(100);
      expect(window.location.href).toBe("");

      // Should redirect after 200ms
      vi.advanceTimersByTime(100);
      expect(window.location.href).toBe("/?tab=learn");
    });
  });
});
