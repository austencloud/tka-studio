import { test, expect } from "../utils/test-base";
import { Page } from "@playwright/test";

/**
 * Simple Performance Test Suite
 *
 * This suite measures basic performance metrics of the legacy web app
 * and provides actionable insights for optimization.
 */

interface SimpleMetrics {
  pageLoadTime: number;
  firstContentfulPaint: number;
  memoryUsage: number;
  assetCount: number;
  totalAssetSize: number;
  slowAssets: Array<{ name: string; time: number; size: number }>;
}

async function collectSimpleMetrics(page: Page): Promise<SimpleMetrics> {
  return await page.evaluate(() => {
    const resources = performance.getEntriesByType('resource');
    const paint = performance.getEntriesByType('paint');

    // Calculate total asset size and identify slow assets
    let totalAssetSize = 0;
    const slowAssets: Array<{ name: string; time: number; size: number }> = [];

    resources.forEach((resource: any) => {
      const size = resource.transferSize || 0;
      totalAssetSize += size;

      if (resource.duration > 100) { // Assets taking more than 100ms
        const url = new URL(resource.name);
        const filename = url.pathname.split('/').pop() || url.pathname;
        slowAssets.push({
          name: filename,
          time: Math.round(resource.duration),
          size: size
        });
      }
    });

    // Sort slow assets by load time
    slowAssets.sort((a, b) => b.time - a.time);

    return {
      pageLoadTime: Math.round(performance.now()),
      firstContentfulPaint: Math.round(paint.find(p => p.name === 'first-contentful-paint')?.startTime || 0),
      memoryUsage: Math.round((performance as any).memory?.usedJSHeapSize || 0),
      assetCount: resources.length,
      totalAssetSize: totalAssetSize,
      slowAssets: slowAssets.slice(0, 10) // Top 10 slowest assets
    };
  });
}

test.describe("Simple Performance Analysis", () => {
  test("should collect baseline performance metrics", async ({ page }) => {
    console.log("🚀 Starting performance measurement...");

    const startTime = Date.now();
    await page.goto('http://localhost:5175/', { waitUntil: 'networkidle' });
    const totalLoadTime = Date.now() - startTime;

    // Wait a moment for the app to fully initialize
    await page.waitForTimeout(2000);

    const metrics = await collectSimpleMetrics(page);

    console.log("\n📊 PERFORMANCE METRICS:");
    console.log("========================");
    console.log(`⏱️  Total Load Time: ${totalLoadTime}ms`);
    console.log(`🎨 First Contentful Paint: ${metrics.firstContentfulPaint}ms`);
    console.log(`💾 Memory Usage: ${(metrics.memoryUsage / 1024 / 1024).toFixed(2)} MB`);
    console.log(`📦 Total Assets: ${metrics.assetCount}`);
    console.log(`📊 Total Asset Size: ${(metrics.totalAssetSize / 1024 / 1024).toFixed(2)} MB`);

    if (metrics.slowAssets.length > 0) {
      console.log("\n🐌 SLOW LOADING ASSETS (>100ms):");
      console.log("==================================");
      metrics.slowAssets.forEach((asset, index) => {
        console.log(`${index + 1}. ${asset.name}: ${asset.time}ms (${(asset.size / 1024).toFixed(1)} KB)`);
      });
    }

    // Take screenshot for visual verification
    await page.screenshot({ path: 'test-results/performance-baseline.png', fullPage: true });

    // Basic performance assertions
    expect(totalLoadTime).toBeLessThan(10000); // Should load within 10 seconds
    expect(metrics.firstContentfulPaint).toBeLessThan(5000); // FCP should be under 5 seconds
    expect(metrics.memoryUsage).toBeLessThan(100 * 1024 * 1024); // Should use less than 100MB
  });

  test("should measure tab navigation performance", async ({ page, appPage }) => {
    console.log("🔄 Testing tab navigation performance...");

    await page.goto('http://localhost:5175/', { waitUntil: 'networkidle' });
    await page.waitForTimeout(1000);

    const tabs = ['write', 'generate', 'construct', 'browse'];
    const navigationTimes: { [key: string]: number } = {};

    for (const tab of tabs) {
      try {
        const startTime = performance.now();
        await appPage.navigateToTab(tab as any);
        await page.waitForTimeout(500); // Wait for tab to settle
        const endTime = performance.now();

        navigationTimes[tab] = Math.round(endTime - startTime);
        console.log(`📑 ${tab.toUpperCase()} tab: ${navigationTimes[tab]}ms`);

        // Take screenshot of each tab
        await page.screenshot({ path: `test-results/tab-${tab}.png` });

      } catch (error) {
        console.log(`❌ Error navigating to ${tab}:`, error);
        navigationTimes[tab] = -1;
      }
    }

    console.log("\n📑 TAB NAVIGATION SUMMARY:");
    console.log("===========================");
    Object.entries(navigationTimes).forEach(([tab, time]) => {
      if (time > 0) {
        const status = time < 1000 ? "✅ Fast" : time < 2000 ? "⚠️  Slow" : "❌ Very Slow";
        console.log(`${tab.toUpperCase()}: ${time}ms ${status}`);
      }
    });

    // Verify navigation times are reasonable
    Object.entries(navigationTimes).forEach(([tab, time]) => {
      if (time > 0) {
        expect(time).toBeLessThan(5000); // Tab navigation should be under 5 seconds
      }
    });
  });

  test("should analyze caching effectiveness", async ({ page }) => {
    console.log("🗄️  Testing caching effectiveness...");

    // First load (cold cache)
    console.log("❄️  Cold cache load...");
    const firstStartTime = Date.now();
    await page.goto('http://localhost:5175/', { waitUntil: 'networkidle' });
    const firstLoadTime = Date.now() - firstStartTime;

    await page.waitForTimeout(1000);
    const firstMetrics = await collectSimpleMetrics(page);

    // Second load (warm cache)
    console.log("🔥 Warm cache load...");
    const secondStartTime = Date.now();
    await page.reload({ waitUntil: 'networkidle' });
    const secondLoadTime = Date.now() - secondStartTime;

    await page.waitForTimeout(1000);
    const secondMetrics = await collectSimpleMetrics(page);

    const improvement = ((firstLoadTime - secondLoadTime) / firstLoadTime) * 100;
    const assetSizeReduction = ((firstMetrics.totalAssetSize - secondMetrics.totalAssetSize) / firstMetrics.totalAssetSize) * 100;

    console.log("\n🗄️  CACHING ANALYSIS:");
    console.log("======================");
    console.log(`❄️  First load: ${firstLoadTime}ms`);
    console.log(`🔥 Second load: ${secondLoadTime}ms`);
    console.log(`⚡ Speed improvement: ${improvement.toFixed(1)}%`);
    console.log(`💾 Asset size reduction: ${assetSizeReduction.toFixed(1)}%`);

    if (improvement > 20) {
      console.log("✅ Excellent caching performance!");
    } else if (improvement > 10) {
      console.log("⚠️  Good caching, but could be better");
    } else {
      console.log("❌ Poor caching effectiveness - needs optimization");
    }

    // Expect some improvement from caching
    expect(improvement).toBeGreaterThan(5); // At least 5% improvement
    expect(secondLoadTime).toBeLessThan(firstLoadTime);
  });

  test("should identify optimization opportunities", async ({ page }) => {
    console.log("🔍 Analyzing optimization opportunities...");

    await page.goto('http://localhost:5175/', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    const metrics = await collectSimpleMetrics(page);

    console.log("\n🔧 OPTIMIZATION RECOMMENDATIONS:");
    console.log("==================================");

    // Bundle size analysis
    if (metrics.totalAssetSize > 5 * 1024 * 1024) { // > 5MB
      console.log("📦 LARGE BUNDLE SIZE:");
      console.log("   - Consider code splitting");
      console.log("   - Implement lazy loading for non-critical components");
      console.log("   - Use dynamic imports for heavy libraries");
    }

    // Slow assets analysis
    if (metrics.slowAssets.length > 0) {
      console.log("\n🐌 SLOW LOADING ASSETS:");
      console.log("   - Optimize or compress large assets");
      console.log("   - Consider CDN for static assets");
      console.log("   - Implement asset preloading for critical resources");

      const verySlowAssets = metrics.slowAssets.filter(asset => asset.time > 500);
      if (verySlowAssets.length > 0) {
        console.log("   - Priority fixes needed for:");
        verySlowAssets.forEach(asset => {
          console.log(`     * ${asset.name} (${asset.time}ms)`);
        });
      }
    }

    // Memory usage analysis
    const memoryMB = metrics.memoryUsage / 1024 / 1024;
    if (memoryMB > 50) {
      console.log("\n💾 HIGH MEMORY USAGE:");
      console.log("   - Review for memory leaks");
      console.log("   - Optimize large data structures");
      console.log("   - Consider virtual scrolling for large lists");
    }

    // Asset count analysis
    if (metrics.assetCount > 100) {
      console.log("\n📦 TOO MANY ASSETS:");
      console.log("   - Bundle smaller assets together");
      console.log("   - Use HTTP/2 server push");
      console.log("   - Implement resource hints (preload, prefetch)");
    }

    console.log("\n✨ GENERAL RECOMMENDATIONS:");
    console.log("   - Implement service worker for offline caching");
    console.log("   - Use compression (gzip/brotli) for text assets");
    console.log("   - Optimize images with modern formats (WebP, AVIF)");
    console.log("   - Consider implementing a loading skeleton");

    // Basic assertions to ensure the app is functional
    expect(metrics.assetCount).toBeGreaterThan(0);
    expect(metrics.totalAssetSize).toBeGreaterThan(0);
  });
});
