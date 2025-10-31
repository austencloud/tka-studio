/**
 * E2E Test: Background Change Verification
 *
 * This test demonstrates that selecting a background and clicking Apply
 * does NOT actually change the visible background in the application.
 */

import { test, expect, type Page } from "@playwright/test";

test.describe("Background Change Functionality", () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the app
    await page.goto("/");

    // Wait for app to initialize
    await page.waitForLoadState("networkidle");
    await page.waitForTimeout(2000);
  });

  test("should demonstrate that background does not change when selecting different background", async ({
    page,
  }) => {
    console.log("\n🔬 TEST: Verifying background change functionality\n");

    // Step 1: Get initial background state
    console.log("1️⃣ Checking initial background...");
    const initialGradient = await page.evaluate(() => {
      return document.documentElement.style.getPropertyValue(
        "--gradient-cosmic"
      );
    });
    const initialAnimation = await page.evaluate(() => {
      const classes = document.body.className;
      if (classes.includes("aurora-flow")) return "aurora-flow";
      if (classes.includes("snow-fall")) return "snow-fall";
      if (classes.includes("star-twinkle")) return "star-twinkle";
      if (classes.includes("deep-ocean-flow")) return "deep-ocean-flow";
      return "none";
    });

    console.log("   Initial gradient:", initialGradient || "none");
    console.log("   Initial animation:", initialAnimation);

    // Step 2: Open settings dialog
    console.log("\n2️⃣ Opening settings dialog...");
    await page.keyboard.press("Meta+,"); // Cmd/Ctrl + ,
    await page.waitForTimeout(500);

    // Verify settings dialog is open
    const settingsDialog = page.locator(".settings-dialog");
    await expect(settingsDialog).toBeVisible({ timeout: 5000 });
    console.log("   ✅ Settings dialog opened");

    // Step 3: Navigate to Background tab
    console.log("\n3️⃣ Navigating to Background tab...");
    const backgroundTab = page.locator("text=Background").first();
    await backgroundTab.click();
    await page.waitForTimeout(500);
    console.log("   ✅ Background tab clicked");

    // Step 4: Get available backgrounds
    console.log("\n4️⃣ Finding available backgrounds...");
    const backgroundThumbnails = page.locator(".background-thumbnail");
    const count = await backgroundThumbnails.count();
    console.log(`   Found ${count} background options`);

    // Log all available backgrounds
    for (let i = 0; i < count; i++) {
      const name = await backgroundThumbnails
        .nth(i)
        .locator(".background-name")
        .textContent();
      console.log(`   - Option ${i + 1}: ${name}`);
    }

    // Step 5: Select a different background (Aurora)
    console.log("\n5️⃣ Selecting Aurora background...");
    const auroraBackground = page.locator(
      '.background-thumbnail:has-text("Aurora")'
    );

    // Check if Aurora exists
    const auroraExists = (await auroraBackground.count()) > 0;
    if (!auroraExists) {
      console.log(
        "   ⚠️ Aurora background not found, trying first available option"
      );
      await backgroundThumbnails.first().click();
    } else {
      await auroraBackground.click();
      console.log("   ✅ Aurora background clicked");
    }

    await page.waitForTimeout(500);

    // Step 6: Click Apply button
    console.log("\n6️⃣ Clicking Apply button...");
    const applyButton = page.locator('button:has-text("Apply")');
    await applyButton.click();
    console.log("   ✅ Apply button clicked");

    // Wait for dialog to close and background to update
    await page.waitForTimeout(2000);

    // Step 7: Check if background changed
    console.log("\n7️⃣ Checking if background changed...");
    const newGradient = await page.evaluate(() => {
      return document.documentElement.style.getPropertyValue(
        "--gradient-cosmic"
      );
    });
    const newAnimation = await page.evaluate(() => {
      const classes = document.body.className;
      if (classes.includes("aurora-flow")) return "aurora-flow";
      if (classes.includes("snow-fall")) return "snow-fall";
      if (classes.includes("star-twinkle")) return "star-twinkle";
      if (classes.includes("deep-ocean-flow")) return "deep-ocean-flow";
      return "none";
    });

    console.log("   New gradient:", newGradient || "none");
    console.log("   New animation:", newAnimation);

    // Step 8: Compare results
    console.log("\n8️⃣ RESULTS:");
    console.log("   ────────────────────────────────────");
    console.log("   Initial gradient:", initialGradient || "none");
    console.log("   New gradient:    ", newGradient || "none");
    console.log("   Gradient changed:", initialGradient !== newGradient);
    console.log("   ────────────────────────────────────");
    console.log("   Initial animation:", initialAnimation);
    console.log("   New animation:    ", newAnimation);
    console.log("   Animation changed:", initialAnimation !== newAnimation);
    console.log("   ────────────────────────────────────");

    // The test will fail if background didn't change
    if (initialGradient === newGradient && initialAnimation === newAnimation) {
      console.log("\n❌ BUG CONFIRMED: Background did NOT change!");
      console.log("   User selected a different background and clicked Apply,");
      console.log("   but the background remained the same.");

      // Check localStorage to see if settings were saved
      const savedSettings = await page.evaluate(() => {
        const stored = localStorage.getItem("tka-modern-web-settings");
        return stored ? JSON.parse(stored) : null;
      });

      console.log("\n📦 Checking localStorage:");
      console.log(
        "   Saved backgroundType:",
        savedSettings?.backgroundType || "none"
      );
      console.log("   Settings were saved:", !!savedSettings);

      if (savedSettings?.backgroundType) {
        console.log("\n🔍 DIAGNOSIS:");
        console.log("   ✅ Settings ARE being saved to localStorage");
        console.log("   ❌ But background update is NOT being triggered");
        console.log(
          "   Problem: The reactive effect or updateBodyBackground is not working properly"
        );
      }

      // This assertion will fail and show the problem
      expect(newGradient).not.toBe(initialGradient);
    } else {
      console.log("\n✅ SUCCESS: Background changed successfully!");
    }
  });

  test("should log console messages to see what is being called", async ({
    page,
  }) => {
    console.log(
      "\n🔬 TEST: Monitoring console logs during background change\n"
    );

    // Capture console logs
    const logs: string[] = [];
    page.on("console", (msg) => {
      const text = msg.text();
      logs.push(text);
      if (
        text.includes("updateBodyBackground") ||
        text.includes("Settings applied") ||
        text.includes("SettingsState") ||
        text.includes("updateSettings") ||
        text.includes("Background") ||
        text.includes("🎨")
      ) {
        console.log("   [APP]", text);
      }
    });

    // Navigate and wait
    await page.goto("/");
    await page.waitForLoadState("networkidle");
    await page.waitForTimeout(1000);

    console.log("\n1️⃣ Opening settings...");
    await page.keyboard.press("Meta+,");
    await page.waitForTimeout(500);

    console.log("\n2️⃣ Clicking Background tab...");
    await page.locator("text=Background").first().click();
    await page.waitForTimeout(500);

    console.log("\n3️⃣ Selecting a different background...");
    const thumbnails = page.locator(".background-thumbnail");
    await thumbnails.first().click();
    await page.waitForTimeout(500);

    console.log("\n4️⃣ Clicking Apply...");
    await page.locator('button:has-text("Apply")').click();
    await page.waitForTimeout(2000);

    console.log("\n5️⃣ Relevant console logs:");
    const relevantLogs = logs.filter(
      (log) =>
        log.includes("updateBodyBackground") ||
        log.includes("Settings applied") ||
        log.includes("SettingsState") ||
        log.includes("updateSettings") ||
        log.includes("🎨")
    );

    if (relevantLogs.length === 0) {
      console.log("   ❌ NO relevant logs found!");
      console.log("   This means updateBodyBackground was never called");
    } else {
      relevantLogs.forEach((log) => console.log(`   ${log}`));
    }
  });
});
