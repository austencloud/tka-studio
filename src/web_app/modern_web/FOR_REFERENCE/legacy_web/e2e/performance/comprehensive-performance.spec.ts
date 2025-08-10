import { test, expect } from "../utils/test-base";
import { Page } from "@playwright/test";

/**
 * Comprehensive Performance Test Suite
 *
 * This suite measures various performance aspects of the legacy web app:
 * - Page load times
 * - Asset loading performance
 * - Memory usage patterns
 * - Interaction responsiveness
 * - Caching effectiveness
 */

interface PerformanceMetrics {
  loadTime: number;
  domContentLoaded: number;
  firstContentfulPaint: number;
  largestContentfulPaint: number;
  cumulativeLayoutShift: number;
  firstInputDelay: number;
  totalBlockingTime: number;
  memoryUsage?: number;
  assetLoadTimes: { [key: string]: number };
}

async function collectPerformanceMetrics(page: Page): Promise<PerformanceMetrics> {
  return await page.evaluate(() => {
    const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
    const paint = performance.getEntriesByType('paint');
    const resources = performance.getEntriesByType('resource');

    // Calculate asset load times
    const assetLoadTimes: { [key: string]: number } = {};
    resources.forEach((resource: any) => {
      const url = new URL(resource.name);
      const filename = url.pathname.split('/').pop() || url.pathname;
      assetLoadTimes[filename] = resource.duration;
    });

    // Get Web Vitals if available
    let lcp = 0;
    let cls = 0;
    let fid = 0;
    let tbt = 0;

    // Try to get LCP from PerformanceObserver if available
    try {
      const lcpEntries = performance.getEntriesByType('largest-contentful-paint');
      if (lcpEntries.length > 0) {
        lcp = (lcpEntries[lcpEntries.length - 1] as any).startTime;
      }
    } catch (e) {
      console.log('LCP not available');
    }

    return {
      loadTime: navigation.loadEventEnd - navigation.navigationStart,
      domContentLoaded: navigation.domContentLoadedEventEnd - navigation.navigationStart,
      firstContentfulPaint: paint.find(p => p.name === 'first-contentful-paint')?.startTime || 0,
      largestContentfulPaint: lcp,
      cumulativeLayoutShift: cls,
      firstInputDelay: fid,
      totalBlockingTime: tbt,
      memoryUsage: (performance as any).memory?.usedJSHeapSize || 0,
      assetLoadTimes
    };
  });
}

async function measureInteractionTime(page: Page, selector: string, action: () => Promise<void>): Promise<number> {
  const startTime = await page.evaluate(() => performance.now());
  await action();
  const endTime = await page.evaluate(() => performance.now());
  return endTime - startTime;
}

test.describe("Comprehensive Performance Analysis", () => {
  let baselineMetrics: PerformanceMetrics;

  test.beforeAll(async ({ browser }) => {
    // Collect baseline metrics on a fresh page load
    const context = await browser.newContext();
    const page = await context.newPage();

    await page.goto('http://localhost:5175/');
    await page.waitForLoadState('networkidle');

    baselineMetrics = await collectPerformanceMetrics(page);
    console.log('Baseline metrics collected:', baselineMetrics);

    await context.close();
  });

  test("should measure initial page load performance", async ({ page }) => {
    // Clear cache to simulate first-time visitor
    await page.context().clearCookies();

    const startTime = Date.now();
    await page.goto('http://localhost:5175/', { waitUntil: 'networkidle' });
    const loadTime = Date.now() - startTime;

    const metrics = await collectPerformanceMetrics(page);

    console.log('Page Load Metrics:', {
      totalLoadTime: loadTime,
      domContentLoaded: metrics.domContentLoaded,
      firstContentfulPaint: metrics.firstContentfulPaint,
      memoryUsage: metrics.memoryUsage
    });

    // Performance assertions
    expect(loadTime).toBeLessThan(5000); // Should load within 5 seconds
    expect(metrics.domContentLoaded).toBeLessThan(3000); // DOM should be ready within 3 seconds
    expect(metrics.firstContentfulPaint).toBeLessThan(2000); // FCP should be under 2 seconds

    // Take screenshot for visual verification
    await page.screenshot({ path: 'test-results/initial-load.png', fullPage: true });
  });

  test("should measure asset loading performance", async ({ page }) => {
    await page.goto('http://localhost:5175/');
    await page.waitForLoadState('networkidle');

    const metrics = await collectPerformanceMetrics(page);

    console.log('Asset Load Times:', metrics.assetLoadTimes);

    // Identify slow-loading assets
    const slowAssets = Object.entries(metrics.assetLoadTimes)
      .filter(([_, time]) => time > 1000)
      .sort(([_, a], [__, b]) => b - a);

    console.log('Slow loading assets (>1s):', slowAssets);

    // Check for excessively slow assets
    const criticalAssets = ['app.js', 'app.css', 'index.html'];
    criticalAssets.forEach(asset => {
      const loadTime = metrics.assetLoadTimes[asset];
      if (loadTime) {
        expect(loadTime).toBeLessThan(2000); // Critical assets should load within 2 seconds
      }
    });
  });

  test("should measure tab navigation performance", async ({ page, appPage }) => {
    await page.goto('http://localhost:5175/');
    await page.waitForLoadState('networkidle');

    const tabs = ['write', 'generate', 'construct', 'browse', 'learn'];
    const navigationTimes: { [key: string]: number } = {};

    for (const tab of tabs) {
      const startTime = await page.evaluate(() => performance.now());

      try {
        await appPage.navigateToTab(tab as any);
        await page.waitForTimeout(500); // Wait for tab to settle

        const endTime = await page.evaluate(() => performance.now());
        navigationTimes[tab] = endTime - startTime;

        console.log(`${tab} tab navigation time: ${navigationTimes[tab]}ms`);

        // Take screenshot of each tab
        await page.screenshot({ path: `test-results/tab-${tab}.png` });

      } catch (error) {
        console.log(`Error navigating to ${tab}:`, error);
        navigationTimes[tab] = -1; // Mark as failed
      }
    }

    // Verify navigation times are reasonable
    Object.entries(navigationTimes).forEach(([tab, time]) => {
      if (time > 0) {
        expect(time).toBeLessThan(3000); // Tab navigation should be under 3 seconds
      }
    });

    console.log('All navigation times:', navigationTimes);
  });

  test("should measure memory usage patterns", async ({ page, appPage }) => {
    await page.goto('http://localhost:5175/');
    await page.waitForLoadState('networkidle');

    const memorySnapshots: { [key: string]: number } = {};

    // Initial memory usage
    const initialMemory = await page.evaluate(() => (performance as any).memory?.usedJSHeapSize || 0);
    memorySnapshots['initial'] = initialMemory;

    // Navigate through tabs and measure memory
    const tabs = ['write', 'generate', 'construct', 'browse'];
    for (const tab of tabs) {
      try {
        await appPage.navigateToTab(tab as any);
        await page.waitForTimeout(1000);

        const memory = await page.evaluate(() => (performance as any).memory?.usedJSHeapSize || 0);
        memorySnapshots[tab] = memory;

        console.log(`Memory usage after ${tab} tab: ${(memory / 1024 / 1024).toFixed(2)} MB`);
      } catch (error) {
        console.log(`Error measuring memory for ${tab}:`, error);
      }
    }

    // Check for memory leaks (significant increases)
    const memoryIncrease = memorySnapshots['browse'] - memorySnapshots['initial'];
    const memoryIncreasePercent = (memoryIncrease / memorySnapshots['initial']) * 100;

    console.log(`Memory increase: ${(memoryIncrease / 1024 / 1024).toFixed(2)} MB (${memoryIncreasePercent.toFixed(1)}%)`);

    // Memory should not increase by more than 50MB or 100% during normal navigation
    expect(memoryIncrease).toBeLessThan(50 * 1024 * 1024); // 50MB
    expect(memoryIncreasePercent).toBeLessThan(100); // 100%
  });

  test("should measure caching effectiveness", async ({ page }) => {
    // First load (cold cache)
    await page.goto('http://localhost:5175/');
    await page.waitForLoadState('networkidle');
    const firstLoadMetrics = await collectPerformanceMetrics(page);

    // Second load (warm cache)
    await page.reload({ waitUntil: 'networkidle' });
    const secondLoadMetrics = await collectPerformanceMetrics(page);

    console.log('First load time:', firstLoadMetrics.loadTime);
    console.log('Second load time:', secondLoadMetrics.loadTime);

    // Second load should be faster due to caching
    const improvement = ((firstLoadMetrics.loadTime - secondLoadMetrics.loadTime) / firstLoadMetrics.loadTime) * 100;
    console.log(`Cache improvement: ${improvement.toFixed(1)}%`);

    // Expect at least 10% improvement from caching
    expect(improvement).toBeGreaterThan(10);
    expect(secondLoadMetrics.loadTime).toBeLessThan(firstLoadMetrics.loadTime);
  });

  test("should measure interaction responsiveness", async ({ page, appPage, generateTabPage }) => {
    await page.goto('http://localhost:5175/');
    await page.waitForLoadState('networkidle');

    const interactionTimes: { [key: string]: number } = {};

    // Measure button click responsiveness
    try {
      await appPage.navigateToTab('generate');
      await page.waitForTimeout(1000);

      // Measure generate button click time
      const generateClickTime = await measureInteractionTime(page, '.generate-button', async () => {
        try {
          await generateTabPage.generateSequence();
        } catch (error) {
          // Fallback: try to click any generate button
          await page.click('button:has-text("Generate")', { timeout: 5000 });
        }
      });

      interactionTimes['generateButton'] = generateClickTime;
      console.log(`Generate button response time: ${generateClickTime}ms`);

    } catch (error) {
      console.log('Error measuring generate button:', error);
    }

    // Measure tab switching responsiveness
    const tabSwitchTime = await measureInteractionTime(page, '[data-tab="write"]', async () => {
      await appPage.navigateToTab('write');
    });

    interactionTimes['tabSwitch'] = tabSwitchTime;
    console.log(`Tab switch response time: ${tabSwitchTime}ms`);

    // Verify interaction times are acceptable
    Object.entries(interactionTimes).forEach(([interaction, time]) => {
      expect(time).toBeLessThan(1000); // All interactions should respond within 1 second
    });

    console.log('All interaction times:', interactionTimes);
  });

  test("should analyze bundle size and loading patterns", async ({ page }) => {
    await page.goto('http://localhost:5175/');
    await page.waitForLoadState('networkidle');

    const bundleAnalysis = await page.evaluate(() => {
      const resources = performance.getEntriesByType('resource');
      const jsFiles = resources.filter((r: any) => r.name.endsWith('.js'));
      const cssFiles = resources.filter((r: any) => r.name.endsWith('.css'));
      const imageFiles = resources.filter((r: any) =>
        r.name.match(/\.(png|jpg|jpeg|gif|svg|webp)$/i)
      );

      const totalJSSize = jsFiles.reduce((sum: number, file: any) => sum + (file.transferSize || 0), 0);
      const totalCSSSize = cssFiles.reduce((sum: number, file: any) => sum + (file.transferSize || 0), 0);
      const totalImageSize = imageFiles.reduce((sum: number, file: any) => sum + (file.transferSize || 0), 0);

      return {
        jsFileCount: jsFiles.length,
        cssFileCount: cssFiles.length,
        imageFileCount: imageFiles.length,
        totalJSSize,
        totalCSSSize,
        totalImageSize,
        largestJSFile: jsFiles.reduce((largest: any, current: any) =>
          (current.transferSize || 0) > (largest.transferSize || 0) ? current : largest, {}
        ),
        largestImageFile: imageFiles.reduce((largest: any, current: any) =>
          (current.transferSize || 0) > (largest.transferSize || 0) ? current : largest, {}
        )
      };
    });

    console.log('Bundle Analysis:', {
      ...bundleAnalysis,
      totalJSSizeMB: (bundleAnalysis.totalJSSize / 1024 / 1024).toFixed(2),
      totalCSSSizeMB: (bundleAnalysis.totalCSSSize / 1024 / 1024).toFixed(2),
      totalImageSizeMB: (bundleAnalysis.totalImageSize / 1024 / 1024).toFixed(2)
    });

    // Performance assertions for bundle sizes
    expect(bundleAnalysis.totalJSSize).toBeLessThan(5 * 1024 * 1024); // JS should be under 5MB
    expect(bundleAnalysis.totalCSSSize).toBeLessThan(1 * 1024 * 1024); // CSS should be under 1MB
    expect(bundleAnalysis.jsFileCount).toBeLessThan(20); // Should not have too many JS files
  });
});
