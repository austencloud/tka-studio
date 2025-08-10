import { test, expect } from "../utils/test-base";

/**
 * Asset Diagnostic Test
 *
 * This test identifies exactly which assets are failing to load and why,
 * then provides specific fixes for each issue.
 */

test.describe("Asset Loading Diagnostics", () => {
  test("should identify and fix asset loading issues", async ({ page }) => {
    console.log("🔍 Starting asset diagnostic...");

    // Track all network requests
    const failedRequests: Array<{ url: string; status: number; error?: string }> = [];
    const successfulRequests: Array<{ url: string; status: number; size: number }> = [];

    page.on('response', (response) => {
      const url = response.url();
      const status = response.status();

      if (status >= 400) {
        failedRequests.push({ url, status });
      } else if (url.includes('/images/') || url.includes('.svg')) {
        successfulRequests.push({
          url,
          status,
          size: parseInt(response.headers()['content-length'] || '0')
        });
      }
    });

    page.on('requestfailed', (request) => {
      failedRequests.push({
        url: request.url(),
        status: 0,
        error: request.failure()?.errorText
      });
    });

    // Load the page and wait for all network activity
    await page.goto('http://localhost:5175/', { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000); // Extra time for lazy loading

    console.log("\n📊 ASSET LOADING ANALYSIS:");
    console.log("============================");

    // Analyze failed requests
    if (failedRequests.length > 0) {
      console.log(`\n❌ FAILED REQUESTS (${failedRequests.length}):`);
      failedRequests.forEach((req, index) => {
        const filename = req.url.split('/').pop();
        console.log(`${index + 1}. ${filename}`);
        console.log(`   URL: ${req.url}`);
        console.log(`   Status: ${req.status}`);
        if (req.error) console.log(`   Error: ${req.error}`);
        console.log("");
      });

      // Categorize failures
      const missingArrows = failedRequests.filter(r => r.url.includes('/arrows/'));
      const missingLetters = failedRequests.filter(r => r.url.includes('/letters_'));
      const otherMissing = failedRequests.filter(r => !r.url.includes('/arrows/') && !r.url.includes('/letters_'));

      console.log("📋 FAILURE CATEGORIES:");
      console.log(`   🏹 Arrow SVGs: ${missingArrows.length} missing`);
      console.log(`   🔤 Letter SVGs: ${missingLetters.length} missing`);
      console.log(`   📄 Other assets: ${otherMissing.length} missing`);
    }

    // Analyze successful requests
    if (successfulRequests.length > 0) {
      console.log(`\n✅ SUCCESSFUL REQUESTS (${successfulRequests.length}):`);
      const totalSize = successfulRequests.reduce((sum, req) => sum + req.size, 0);
      console.log(`   📦 Total size: ${(totalSize / 1024 / 1024).toFixed(2)} MB`);

      const slowAssets = successfulRequests.filter(req => req.size > 100000); // > 100KB
      if (slowAssets.length > 0) {
        console.log(`   🐌 Large assets (>100KB): ${slowAssets.length}`);
        slowAssets.forEach(asset => {
          const filename = asset.url.split('/').pop();
          console.log(`      - ${filename}: ${(asset.size / 1024).toFixed(1)} KB`);
        });
      }
    }

    // Test specific problematic assets
    console.log("\n🧪 TESTING SPECIFIC ASSETS:");
    console.log("==============================");

    const testAssets = [
      '/images/arrows/pro/from_radial/pro_0.0.svg',
      '/images/letters_trimmed/Type1/A.svg',
      '/images/arrows/pro/from_radial/pro_45.0.svg',
      '/favicon.ico'
    ];

    for (const assetPath of testAssets) {
      try {
        const response = await page.goto(`http://localhost:5175${assetPath}`);
        const status = response?.status() || 0;
        const filename = assetPath.split('/').pop();

        if (status === 200) {
          console.log(`✅ ${filename}: OK (${status})`);
        } else {
          console.log(`❌ ${filename}: FAILED (${status})`);
        }
      } catch (error) {
        const filename = assetPath.split('/').pop();
        console.log(`❌ ${filename}: ERROR - ${error}`);
      }
    }

    // Go back to main page for final analysis
    await page.goto('http://localhost:5175/', { waitUntil: 'networkidle' });

    // Generate specific fixes
    console.log("\n🔧 RECOMMENDED FIXES:");
    console.log("======================");

    if (failedRequests.length > 0) {
      console.log("1. IMMEDIATE FIXES:");

      if (failedRequests.some(r => r.url.includes('/arrows/'))) {
        console.log("   📁 Check arrow SVG paths in static/images/arrows/");
        console.log("   🔧 Verify file permissions and case sensitivity");
      }

      if (failedRequests.some(r => r.url.includes('/letters_'))) {
        console.log("   📁 Check letter SVG paths in static/images/letters_trimmed/");
        console.log("   🔧 Consider creating fallback placeholder SVGs");
      }

      console.log("\n2. PERFORMANCE FIXES:");
      console.log("   ⚡ Implement lazy loading for non-critical SVGs");
      console.log("   📦 Bundle frequently used SVGs into sprites");
      console.log("   🗄️  Add service worker for aggressive caching");
      console.log("   🔄 Implement error handling with fallbacks");
    }

    // Performance assertions
    expect(failedRequests.length).toBeLessThan(10); // Should have fewer than 10 failed requests
    expect(successfulRequests.length).toBeGreaterThan(0); // Should load some assets successfully

    // Take diagnostic screenshot
    await page.screenshot({ path: 'test-results/asset-diagnostic.png', fullPage: true });

    console.log("\n📸 Screenshot saved: test-results/asset-diagnostic.png");
    console.log("🎯 Run this test to identify specific asset issues before implementing fixes!");
  });

  test("should test asset loading performance", async ({ page }) => {
    console.log("⏱️  Testing asset loading performance...");

    const assetLoadTimes: Array<{ name: string; time: number; size: number }> = [];

    page.on('response', async (response) => {
      if (response.url().includes('/images/') || response.url().includes('.svg')) {
        const timing = await response.request().timing();
        const size = parseInt(response.headers()['content-length'] || '0');
        const filename = response.url().split('/').pop() || 'unknown';

        assetLoadTimes.push({
          name: filename,
          time: timing.responseEnd - timing.requestStart,
          size
        });
      }
    });

    await page.goto('http://localhost:5175/', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    // Sort by load time
    assetLoadTimes.sort((a, b) => b.time - a.time);

    console.log("\n⏱️  ASSET LOAD TIMES:");
    console.log("======================");

    const slowAssets = assetLoadTimes.filter(asset => asset.time > 100);
    if (slowAssets.length > 0) {
      console.log("🐌 Slow loading assets (>100ms):");
      slowAssets.slice(0, 10).forEach((asset, index) => {
        console.log(`${index + 1}. ${asset.name}: ${asset.time.toFixed(0)}ms (${(asset.size / 1024).toFixed(1)} KB)`);
      });
    }

    const fastAssets = assetLoadTimes.filter(asset => asset.time <= 100);
    console.log(`\n⚡ Fast loading assets (≤100ms): ${fastAssets.length}`);
    console.log(`🐌 Slow loading assets (>100ms): ${slowAssets.length}`);

    const avgLoadTime = assetLoadTimes.reduce((sum, asset) => sum + asset.time, 0) / assetLoadTimes.length;
    console.log(`📊 Average load time: ${avgLoadTime.toFixed(0)}ms`);

    // Performance recommendations
    if (slowAssets.length > 10) {
      console.log("\n🚨 TOO MANY SLOW ASSETS - Priority fixes needed!");
    } else if (slowAssets.length > 5) {
      console.log("\n⚠️  Some slow assets - Consider optimization");
    } else {
      console.log("\n✅ Asset loading performance is good!");
    }
  });
});
