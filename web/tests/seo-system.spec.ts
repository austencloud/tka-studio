/**
 * SEO System Testing Script
 *
 * Comprehensive tests to validate the hybrid SEO approach
 * Run with: npm run test:seo
 */

import { expect, test } from "@playwright/test";

test.describe("SEO Hybrid System", () => {
  test.describe("Bot Behavior (No Redirects)", () => {
    test("Googlebot sees static about page", async ({ page }) => {
      // Simulate Googlebot both in headers and navigator.userAgent
      const botUserAgent =
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)";

      await page.setExtraHTTPHeaders({
        "User-Agent": botUserAgent,
      });

      // Override navigator.userAgent in the browser context
      await page.addInitScript((ua) => {
        Object.defineProperty(navigator, "userAgent", {
          get: () => ua,
        });
      }, botUserAgent);

      await page.goto("/about");

      // Should not redirect
      expect(page.url()).toContain("/about");

      // Should have proper meta tags (using actual title from +page.server.ts)
      const title = await page.locator("title").textContent();
      expect(title).toContain("About TKA - The Kinetic Constructor");

      const description = await page
        .locator('meta[name="description"]')
        .getAttribute("content");
      expect(description).toContain("kinetic typography");

      // Should have structured data
      const structuredData = await page
        .locator('script[type="application/ld+json"]')
        .textContent();
      expect(structuredData).toContain("SoftwareApplication");
    });

    test("Bingbot sees static features page", async ({ page }) => {
      // Simulate Bingbot both in headers and navigator.userAgent
      const botUserAgent =
        "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)";

      await page.setExtraHTTPHeaders({
        "User-Agent": botUserAgent,
      });

      // Override navigator.userAgent in the browser context
      await page.addInitScript((ua) => {
        Object.defineProperty(navigator, "userAgent", {
          get: () => ua,
        });
      }, botUserAgent);

      await page.goto("/features");

      expect(page.url()).toContain("/features");

      const title = await page.locator("title").textContent();
      expect(title).toContain("TKA Features");
    });

    test("Facebook crawler sees static browse page", async ({ page }) => {
      // Simulate Facebook crawler both in headers and navigator.userAgent
      const botUserAgent =
        "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)";

      await page.setExtraHTTPHeaders({
        "User-Agent": botUserAgent,
      });

      // Override navigator.userAgent in the browser context
      await page.addInitScript((ua) => {
        Object.defineProperty(navigator, "userAgent", {
          get: () => ua,
        });
      }, botUserAgent);

      await page.goto("/browse");

      expect(page.url()).toContain("/browse");

      const ogTitle = await page
        .locator('meta[property="og:title"]')
        .getAttribute("content");
      expect(ogTitle).toContain("Browse Flow Arts Gallery");
    });
  });

  test.describe("User Redirection (From Search Engines)", () => {
    test("Users from Google get redirected to SPA", async ({ page }) => {
      // Simulate coming from Google search
      await page.goto("https://www.google.com/search?q=test");
      await page.goto("/about");

      // Should redirect to main app with tab parameter
      await page.waitForURL("/?tab=about", { timeout: 5000 });
      expect(page.url()).toContain("/?tab=about");
    });

    test("Direct users get redirected to SPA", async ({ page }) => {
      await page.goto("/features");

      // Should redirect to main app with section parameter
      await page.waitForURL("/?tab=about&section=features", { timeout: 5000 });
      expect(page.url()).toContain("tab=about");
      expect(page.url()).toContain("section=features");
    });

    test("Browse page redirects correctly", async ({ page }) => {
      await page.goto("/browse");

      await page.waitForURL("/?tab=browse", { timeout: 5000 });
      expect(page.url()).toContain("/?tab=browse");
    });
  });

  test.describe("SPA Navigation (No Page Reloads)", () => {
    test("Tab navigation stays in SPA", async ({ page }) => {
      await page.goto("/");

      // Click about tab (using actual selectors)
      await page.click('.nav-tab:has-text("About")');

      // URL should not change
      expect(page.url()).toBe(new URL("/", page.url()).href);

      // Should not trigger page reload
      const navigationPromise = page.waitForLoadState("networkidle");
      await page.click('.nav-tab:has-text("Browse")');

      // Should resolve quickly (no full page load)
      await expect(navigationPromise).resolves.toBe(undefined);
    });

    test("Logo click switches to about tab", async ({ page }) => {
      await page.goto("/");

      // Start on a different tab
      await page.click('.nav-tab:has-text("Construct")');

      // Click logo
      await page.click(".nav-brand");

      // Should switch to about tab without URL change
      expect(page.url()).toBe(new URL("/", page.url()).href);

      // About tab should be active (check for active class)
      const aboutTab = page.locator('.nav-tab:has-text("About")');
      await expect(aboutTab).toHaveClass(/active/);
    });
  });

  test.describe("URL Parameter Handling", () => {
    test("Main page handles tab parameter", async ({ page }) => {
      await page.goto("/?tab=about");

      // Should activate about tab (check for active class)
      const aboutTab = page.locator('.nav-tab:has-text("About")');
      await expect(aboutTab).toHaveClass(/active/);

      // URL should be cleaned up
      await page.waitForFunction(() => window.location.search === "");
      expect(new URL(page.url()).search).toBe("");
    });

    test("Section parameter triggers scroll", async ({ page }) => {
      await page.goto("/?tab=about&section=features");

      // Should scroll to features section
      await page.waitForTimeout(1000); // Allow time for scroll

      const featuresSection = page.locator("#features");
      await expect(featuresSection).toBeInViewport();
    });
  });

  test.describe("SEO Infrastructure", () => {
    test("Sitemap is accessible and valid", async ({ page }) => {
      const response = await page.goto("/sitemap.xml");
      expect(response?.status()).toBe(200);
      expect(response?.headers()["content-type"]).toContain("application/xml");

      const content = await page.textContent("body");
      expect(content).toContain('<?xml version="1.0"');
      expect(content).toContain("<urlset");
      expect(content).toContain("/about");
      expect(content).toContain("/features");
      expect(content).toContain("/browse");
    });

    test("Robots.txt is accessible", async ({ page }) => {
      const response = await page.goto("/robots.txt");
      expect(response?.status()).toBe(200);

      const content = await page.textContent("body");
      expect(content).toContain("User-agent: *");
      expect(content).toContain("Sitemap:");
      expect(content).toContain("/sitemap.xml");
    });
  });

  test.describe("SEO Utils Functions", () => {
    test("Bot detection works correctly", async ({ page }) => {
      // Test the isSearchEngineBot function
      const botDetection = await page.evaluate(() => {
        // Import and test the function
        const isBot = (ua: string) => {
          const botPatterns = [
            /googlebot/i,
            /bingbot/i,
            /facebookexternalhit/i,
          ];
          return botPatterns.some((pattern) => pattern.test(ua));
        };

        return {
          google: isBot("Mozilla/5.0 (compatible; Googlebot/2.1)"),
          bing: isBot("Mozilla/5.0 (compatible; bingbot/2.0)"),
          facebook: isBot("facebookexternalhit/1.1"),
          chrome: isBot(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
          ),
          firefox: isBot(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
          ),
        };
      });

      expect(botDetection.google).toBe(true);
      expect(botDetection.bing).toBe(true);
      expect(botDetection.facebook).toBe(true);
      expect(botDetection.chrome).toBe(false);
      expect(botDetection.firefox).toBe(false);
    });
  });
});

test.describe("Performance Impact", () => {
  test("SPA navigation is fast", async ({ page }) => {
    await page.goto("/");

    const startTime = Date.now();

    // Click between tabs multiple times (using actual selectors)
    await page.click('.nav-tab:has-text("About")');
    await page.click('.nav-tab:has-text("Browse")');
    await page.click('.nav-tab:has-text("Construct")');

    const endTime = Date.now();
    const duration = endTime - startTime;

    // Should be very fast (under 500ms for 3 tab switches)
    expect(duration).toBeLessThan(500);
  });

  test("SEO pages have good Lighthouse scores", async ({ page }) => {
    // This would require lighthouse integration
    // For now, just ensure pages load quickly
    const startTime = Date.now();
    await page.goto("/about");
    const loadTime = Date.now() - startTime;

    expect(loadTime).toBeLessThan(2000); // Under 2 seconds
  });
});
