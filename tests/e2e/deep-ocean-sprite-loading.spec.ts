import { test, expect } from "@playwright/test";

test.describe("Deep Ocean Fish Sprite Loading", () => {
  test("should load fish sprites and display them correctly", async ({
    page,
  }) => {
    const consoleLogs: string[] = [];
    const consoleErrors: string[] = [];

    // Capture all console messages
    page.on("console", (msg) => {
      const text = msg.text();
      const type = msg.type();

      if (type === "error") {
        consoleErrors.push(`[ERROR] ${text}`);
      } else {
        consoleLogs.push(`[${type.toUpperCase()}] ${text}`);
      }

      // Print to test output in real-time
      console.log(`[${type.toUpperCase()}] ${text}`);
    });

    // Navigate to the app
    console.log("\n=== Navigating to app ===");
    await page.goto("/");

    // Wait for the page to load
    await page.waitForLoadState("networkidle");
    console.log("\n=== Page loaded ===");

    // Wait for initial setup
    await page.waitForTimeout(1000);

    // Open settings
    console.log("\n=== Opening settings ===");
    const settingsBtn = page
      .locator('button[aria-label*="Settings"], button:has-text("Settings")')
      .first();
    await settingsBtn.click();
    console.log("Clicked settings button");
    await page.waitForTimeout(1000);

    // Click Background tab
    console.log("\n=== Clicking Background tab ===");
    const backgroundTab = page.locator('button:has-text("Background")').first();
    await backgroundTab.click();
    await page.waitForTimeout(500);

    // Click the Deep Ocean card
    console.log("\n=== Clicking Deep Ocean card ===");
    const deepOceanCard = page.locator("text=Deep Ocean").first();
    await deepOceanCard.click();
    await page.waitForTimeout(500);

    // Click Apply Changes button
    console.log("\n=== Clicking Apply Changes ===");
    const applyButton = page
      .locator('button:has-text("Apply Changes")')
      .first();
    await applyButton.click();
    await page.waitForTimeout(1000);

    // Wait for sprites to load and render
    console.log("\n=== Waiting 3 seconds for sprite loading and rendering ===");
    await page.waitForTimeout(3000);

    // Filter and display relevant console logs
    console.log("\n\n=== FISH SPRITE LOADING LOGS ===");
    const fishLogs = consoleLogs.filter(
      (log) =>
        log.includes("🐟") ||
        log.includes("fish") ||
        log.includes("sprite") ||
        log.includes("Cache") ||
        log.includes("📥") ||
        log.includes("✅") ||
        log.includes("❌") ||
        log.includes("💾") ||
        log.includes("🔍") ||
        log.includes("⏰") ||
        log.includes("✨") ||
        log.includes("🔄") ||
        log.includes("Deep Ocean") ||
        log.includes("🌊")
    );

    fishLogs.forEach((log) => console.log(log));

    console.log("\n=== ALL CONSOLE ERRORS ===");
    consoleErrors.forEach((err) => console.log(err));

    console.log("\n=== ANALYSIS ===");

    // Check if Deep Ocean was initialized
    const deepOceanInit = consoleLogs.some((log) =>
      log.includes("Deep Ocean background initialized")
    );
    console.log(`Deep Ocean initialized: ${deepOceanInit}`);

    // Check if preload was called
    const preloadCalled = consoleLogs.some(
      (log) => log.includes("Preloading") && log.includes("fish sprites")
    );
    console.log(`Preload called: ${preloadCalled}`);

    // Check if any sprites loaded
    const spritesLoaded = consoleLogs.some((log) =>
      log.includes("Fish sprite loaded:")
    );
    console.log(`Sprites loaded: ${spritesLoaded}`);

    // Check cache state
    const cacheState = consoleLogs.filter((log) => log.includes("Cache state"));
    console.log(`Cache state logs: ${cacheState.length}`);

    // Check fish creation
    const fishCreated = consoleLogs.filter((log) =>
      log.includes("Creating fish")
    );
    console.log(`Fish created: ${fishCreated.length}`);

    // Check fish updates
    const fishUpdated = consoleLogs.filter((log) =>
      log.includes("Fish sprite updated to")
    );
    console.log(`Fish sprites updated: ${fishUpdated.length}`);

    // Check fallback rendering
    const fallbackRendering = consoleLogs.filter((log) =>
      log.includes("Fish fallback rendering")
    );
    console.log(`Fallback rendering logs: ${fallbackRendering.length}`);

    console.log("\n=== TEST COMPLETE ===\n");

    // Assertions
    expect(deepOceanInit, "Deep Ocean should be initialized").toBeTruthy();
    expect(preloadCalled, "Sprite preload should be called").toBeTruthy();
  });
});
