import { test, expect } from "@playwright/test";

/**
 * Flow #2: Generate Flow - Basic Auto-Creation
 * Tests: navigate to generate → toggle settings → generate → view animation → regenerate
 */
test("Generate Flow - Basic Auto-Creation", async ({ page }) => {
  // Navigate to app
  await page.goto("/");
  await page.waitForSelector(".app-navigation-bar");

  // Navigate to Build module
  const buildTab = page
    .locator(".nav-tab-container")
    .filter({ hasText: "Build" });
  await buildTab.click();

  // Switch to Generate tab
  const generateButton = page
    .locator(".main-tab-btn")
    .filter({ hasText: "Generate" });
  await generateButton.click();
  await page.waitForTimeout(500);

  // Verify we're on Generate tab
  await expect(page.locator('[data-testid="generate-panel"]')).toBeVisible();
  await page.waitForSelector(".card-settings-container");

  // Step 1: Toggle Grid Mode (click on grid card)
  const gridModeCard = page.locator(".toggle-card").filter({
    has: page.locator('.card-title:has-text("Grid")'),
  });
  await gridModeCard.click();
  await page.waitForTimeout(300);

  // Step 2: Toggle Prop Continuity
  const continuityCard = page.locator(".toggle-card").filter({
    has: page.locator('.card-title:has-text("Continuity")'),
  });
  await continuityCard.click();
  await page.waitForTimeout(300);

  // Step 3: Toggle Generation Mode to Circular
  const genModeCard = page.locator(".toggle-card").filter({
    has: page.locator('.card-title:has-text("Generation")'),
  });

  // Check if Circular is already active
  const circularOption = genModeCard
    .locator(".toggle-option")
    .filter({ hasText: "Circular" });
  const isCircularActive = await circularOption.evaluate((el) =>
    el.classList.contains("active")
  );

  if (!isCircularActive) {
    await genModeCard.click();
    await page.waitForTimeout(500);
  }

  // Step 4: Generate sequence
  const generateSequenceButton = page
    .locator("button")
    .filter({ hasText: /generate/i })
    .first();
  await generateSequenceButton.click();
  await page.waitForTimeout(1500);

  // Step 5: Play the generated sequence
  const animateButton = page
    .locator(".main-tab-btn")
    .filter({ hasText: "Animate" });
  await animateButton.click();
  await page.waitForTimeout(500);

  await expect(page.locator('[data-testid="animation-panel"]')).toBeVisible();
  await page.waitForTimeout(2000);

  // Step 6: Go back to Generate and regenerate with different settings
  await generateButton.click();
  await page.waitForTimeout(500);

  // Change difficulty level
  const levelCard = page.locator(".stepper-card").filter({
    has: page.locator('.card-title:has-text("Level")'),
  });
  const incrementZone = levelCard.locator(".increment-zone");
  await incrementZone.click();
  await page.waitForTimeout(300);

  // Generate again
  await generateSequenceButton.click();
  await page.waitForTimeout(1500);

  console.log("✅ Flow #2: Generate Flow - PASSED");
});
