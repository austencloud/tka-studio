import { test, expect } from "@playwright/test";

test.describe("Beat Addition Performance", () => {
  test("should add beats without setTimeout violations", async ({ page }) => {
    // Navigate to the app
    await page.goto("http://localhost:5173");

    // Wait for app to load
    await page.waitForSelector('[data-testid="build-tab"]', { timeout: 10000 });

    // Collect console violations
    const violations: string[] = [];
    page.on("console", (msg) => {
      const text = msg.text();
      if (text.includes("[Violation]") && text.includes("setTimeout")) {
        violations.push(text);
        console.log("❌ VIOLATION:", text);
      }
    });

    // Select start position
    const startButton = page.locator(".start-tile").first();
    await startButton.click();

    // Wait for start position picker
    await page.waitForSelector('[data-testid="start-position-picker"]', {
      timeout: 5000,
    });

    // Select a start position (first available)
    const firstPosition = page.locator(".pictograph-button").first();
    await firstPosition.click();

    // Wait for option picker to appear
    await page.waitForSelector('[data-testid="option-viewer"]', {
      timeout: 5000,
    });

    // Add 10 beats rapidly
    console.log("🎯 Adding 10 beats...");
    for (let i = 0; i < 10; i++) {
      // Click the first available option
      const option = page.locator(".option-button").first();
      await option.click();

      // Wait a bit for the beat to be added
      await page.waitForTimeout(100);

      console.log(`✅ Added beat ${i + 1}`);
    }

    // Wait for any pending operations
    await page.waitForTimeout(1000);

    // Check for violations
    console.log(`\n📊 Total violations: ${violations.length}`);
    violations.forEach((v) => console.log(`  - ${v}`));

    // Assert no violations
    expect(violations.length).toBe(0);
  });

  test("measure beat addition timing", async ({ page }) => {
    // Navigate to the app
    await page.goto("http://localhost:5173");

    // Wait for app to load
    await page.waitForSelector('[data-testid="build-tab"]', { timeout: 10000 });

    // Inject performance measurement
    await page.evaluate(() => {
      (window as any).beatAdditionTimings = [];

      // Override console.log to capture timing
      const originalLog = console.log;
      console.log = function (...args) {
        const message = args.join(" ");
        if (message.includes("🎯 BuildTabEventService: Added beat")) {
          const timing = performance.now();
          (window as any).beatAdditionTimings.push(timing);
        }
        originalLog.apply(console, args);
      };
    });

    // Select start position
    const startButton = page.locator(".start-tile").first();
    await startButton.click();

    // Wait for start position picker
    await page.waitForSelector('[data-testid="start-position-picker"]', {
      timeout: 5000,
    });

    // Select a start position
    const firstPosition = page.locator(".pictograph-button").first();
    await firstPosition.click();

    // Wait for option picker
    await page.waitForSelector('[data-testid="option-viewer"]', {
      timeout: 5000,
    });

    // Add 10 beats and measure timing
    console.log("🎯 Measuring beat addition timing...");
    const startTime = await page.evaluate(() => performance.now());

    for (let i = 0; i < 10; i++) {
      const option = page.locator(".option-button").first();
      await option.click();
      await page.waitForTimeout(50);
    }

    const endTime = await page.evaluate(() => performance.now());
    const totalTime = endTime - startTime;
    const avgTime = totalTime / 10;

    console.log(`\n📊 Performance Metrics:`);
    console.log(`  Total time: ${totalTime.toFixed(2)}ms`);
    console.log(`  Average per beat: ${avgTime.toFixed(2)}ms`);
    console.log(`  Expected: <100ms per beat`);

    // Assert reasonable performance
    expect(avgTime).toBeLessThan(100);
  });
});
