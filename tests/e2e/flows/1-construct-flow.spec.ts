import { test, expect } from "@playwright/test";

/**
 * Flow #1: Complete Construct Flow
 * Tests: start position → add beats → play → edit → clear
 */
test("Complete Construct Flow", async ({ page }) => {
  // Navigate to app
  await page.goto("/");
  await page.waitForSelector(".app-navigation-bar");

  // Navigate to Build module (should default to Construct)
  const buildTab = page
    .locator(".nav-tab-container")
    .filter({ hasText: "Build" });
  await buildTab.click();
  await page.waitForTimeout(500);

  // Verify we're on Construct tab
  await expect(
    page.locator('[data-testid="construct-tab-content"]')
  ).toBeVisible();

  // Step 1: Select a start position
  const startPositionPicker = page.locator(
    '[data-testid="start-position-picker"]'
  );
  await expect(startPositionPicker).toBeVisible();

  const firstPosition = startPositionPicker.locator(".position-option").first();
  await firstPosition.click();
  await page.waitForTimeout(500);

  // Step 2: Add 3-4 motion beats by clicking options
  const optionViewer = page.locator('[data-testid="option-viewer"]');
  await expect(optionViewer).toBeVisible();

  for (let i = 0; i < 4; i++) {
    const optionCard = optionViewer.locator(".option-card").first();
    await optionCard.click();
    await page.waitForTimeout(400);
  }

  // Step 3: Play/animate the sequence
  const animateButton = page
    .locator(".main-tab-btn")
    .filter({ hasText: "Animate" });
  await animateButton.click();
  await page.waitForTimeout(500);

  // Verify animation panel opened
  await expect(page.locator('[data-testid="animation-panel"]')).toBeVisible();

  // Watch animation play
  await page.waitForTimeout(2000);

  // Step 4: Go back to construct
  const constructButton = page
    .locator(".main-tab-btn")
    .filter({ hasText: "Construct" });
  await constructButton.click();
  await page.waitForTimeout(500);

  // Step 5: Clear sequence
  const clearButton = page.locator("button").filter({ hasText: /clear/i });
  await clearButton.click();
  await page.waitForTimeout(500);

  // Verify sequence cleared (start position picker should be visible again)
  await expect(
    page.locator('[data-testid="start-position-picker"]')
  ).toBeVisible();

  console.log("✅ Flow #1: Complete Construct Flow - PASSED");
});
