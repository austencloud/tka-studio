import { test, expect } from "@playwright/test";

test("Debug animation sequence data", async ({ page }) => {
  // Capture console messages
  const consoleLogs: any[] = [];

  page.on("console", (msg) => {
    const text = msg.text();
    // Only capture our diagnostic logs
    if (
      text.includes("🎯 EndpointCalculator") ||
      text.includes("🔍 Beat") ||
      text.includes("⚠️")
    ) {
      consoleLogs.push({
        type: msg.type(),
        text: text,
      });
    }
  });

  // Navigate to the app
  await page.goto("http://localhost:5173");
  await page.waitForTimeout(2000); // Wait for app to load

  // Click Animate tab
  const animateButton = page.locator("button", { hasText: "Animate" });
  await animateButton.click();
  await page.waitForTimeout(1000);

  // Clear previous logs
  consoleLogs.length = 0;

  // Click play button
  const playButton = page.locator('button[aria-label="Play"]');
  await playButton.click();

  // Let animation run for 3 beats
  await page.waitForTimeout(3000);

  // Stop animation
  const pauseButton = page.locator('button[aria-label="Pause animation"]');
  if (await pauseButton.isVisible()) {
    await pauseButton.click();
  }

  // Print first 20 diagnostic logs
  console.log("\n=== ANIMATION DIAGNOSTIC LOGS ===\n");
  consoleLogs.slice(0, 30).forEach((log, i) => {
    console.log(`${i + 1}. ${log.text}`);
  });

  // Look for any warnings
  const warnings = consoleLogs.filter((log) => log.text.includes("⚠️"));
  if (warnings.length > 0) {
    console.log("\n=== WARNINGS FOUND ===\n");
    warnings.forEach((w) => console.log(w.text));
  }

  // Evaluate to get full motion data for first beat
  const firstBeatData = await page.evaluate(() => {
    // Try to access the animation state if possible
    return {
      note: "Attempting to access beat data via console capture",
    };
  });

  console.log("\n=== FIRST BEAT DATA ===");
  console.log(JSON.stringify(firstBeatData, null, 2));

  expect(consoleLogs.length).toBeGreaterThan(0);
});
