import { expect, test } from "@playwright/test";

/**
 * E2E Test: Clear Sequence Navigation
 *
 * Tests that clearing a sequence from the Animate tab returns the user
 * to the last content tab they were on (Construct or Generate).
 *
 * This replaces the unit test that used mocks - now we test the real user experience.
 */

test.describe("Clear Sequence Navigation from Animate Tab", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
    await page.waitForSelector(".app-navigation-bar");
  });

  test("returns to Construct when clearing from Animate after Construct", async ({
    page,
  }) => {
    // 1. Navigate to Build module
    const buildTab = page
      .locator(".nav-tab-container")
      .filter({ hasText: "Build" });
    await buildTab.click();

    // 2. Wait for Construct tab to be active (default)
    await expect(
      page.locator('[data-testid="construct-tab-content"]')
    ).toBeVisible();

    // 3. Create a sequence by selecting a start position
    const startPositionPicker = page.locator(
      '[data-testid="start-position-picker"]'
    );
    if (await startPositionPicker.isVisible()) {
      // Click first available start position
      const firstPosition = startPositionPicker
        .locator(".position-option")
        .first();
      await firstPosition.click();
      await page.waitForTimeout(500); // Wait for transition
    }

    // 4. Add at least one beat to the sequence
    const optionViewer = page.locator('[data-testid="option-viewer"]');
    await expect(optionViewer).toBeVisible();
    const firstOption = optionViewer.locator(".option-card").first();
    await firstOption.click();
    await page.waitForTimeout(500); // Wait for beat to be added

    // 5. Navigate to Animate tab
    const animateButton = page
      .locator(".main-tab-btn")
      .filter({ hasText: "Animate" });
    await animateButton.click();
    await page.waitForTimeout(500); // Wait for tab transition

    // 6. Verify we're on Animate tab
    await expect(page.locator('[data-testid="animation-panel"]')).toBeVisible();

    // 7. Clear the sequence using the Clear button
    const clearButton = page.locator("button").filter({ hasText: /clear/i });
    await clearButton.click();
    await page.waitForTimeout(500); // Wait for clear and navigation

    // 8. Verify we're back on Construct tab
    await expect(
      page.locator('[data-testid="construct-tab-content"]')
    ).toBeVisible();
    await expect(
      page.locator('[data-testid="start-position-picker"]')
    ).toBeVisible();
  });

  test("returns to Generate when clearing from Animate after Generate", async ({
    page,
  }) => {
    // 1. Navigate to Build module
    const buildTab = page
      .locator(".nav-tab-container")
      .filter({ hasText: "Build" });
    await buildTab.click();

    // 2. Navigate to Generate tab
    const generateButton = page
      .locator(".main-tab-btn")
      .filter({ hasText: "Generate" });
    await generateButton.click();
    await page.waitForTimeout(500);

    // 3. Verify we're on Generate tab
    await expect(page.locator('[data-testid="generate-panel"]')).toBeVisible();

    // 4. Generate a sequence (click generate button)
    const generateSequenceButton = page
      .locator("button")
      .filter({ hasText: /generate/i })
      .first();
    await generateSequenceButton.click();
    await page.waitForTimeout(1000); // Wait for sequence generation

    // 5. Navigate to Animate tab
    const animateButton = page
      .locator(".main-tab-btn")
      .filter({ hasText: "Animate" });
    await animateButton.click();
    await page.waitForTimeout(500);

    // 6. Verify we're on Animate tab
    await expect(page.locator('[data-testid="animation-panel"]')).toBeVisible();

    // 7. Clear the sequence
    const clearButton = page.locator("button").filter({ hasText: /clear/i });
    await clearButton.click();
    await page.waitForTimeout(500);

    // 8. Verify we're back on Generate tab (not Construct)
    await expect(page.locator('[data-testid="generate-panel"]')).toBeVisible();
  });

  test("handles complex navigation: Construct -> Generate -> Animate -> Clear", async ({
    page,
  }) => {
    // 1. Navigate to Build module
    const buildTab = page
      .locator(".nav-tab-container")
      .filter({ hasText: "Build" });
    await buildTab.click();

    // 2. Start on Construct tab and create a sequence
    await expect(
      page.locator('[data-testid="construct-tab-content"]')
    ).toBeVisible();

    const startPositionPicker = page.locator(
      '[data-testid="start-position-picker"]'
    );
    if (await startPositionPicker.isVisible()) {
      const firstPosition = startPositionPicker
        .locator(".position-option")
        .first();
      await firstPosition.click();
      await page.waitForTimeout(500);
    }

    const optionViewer = page.locator('[data-testid="option-viewer"]');
    const firstOption = optionViewer.locator(".option-card").first();
    await firstOption.click();
    await page.waitForTimeout(500);

    // 3. Navigate to Generate tab (this becomes the "last content tab")
    const generateButton = page
      .locator(".main-tab-btn")
      .filter({ hasText: "Generate" });
    await generateButton.click();
    await page.waitForTimeout(500);
    await expect(page.locator('[data-testid="generate-panel"]')).toBeVisible();

    // 4. Navigate to Animate tab
    const animateButton = page
      .locator(".main-tab-btn")
      .filter({ hasText: "Animate" });
    await animateButton.click();
    await page.waitForTimeout(500);
    await expect(page.locator('[data-testid="animation-panel"]')).toBeVisible();

    // 5. Clear the sequence
    const clearButton = page.locator("button").filter({ hasText: /clear/i });
    await clearButton.click();
    await page.waitForTimeout(500);

    // 6. Verify we're back on Generate tab (the last content tab we visited)
    await expect(page.locator('[data-testid="generate-panel"]')).toBeVisible();
  });

  test("clearing from Construct tab stays on Construct", async ({ page }) => {
    // 1. Navigate to Build module
    const buildTab = page
      .locator(".nav-tab-container")
      .filter({ hasText: "Build" });
    await buildTab.click();

    // 2. Create a sequence on Construct tab
    await expect(
      page.locator('[data-testid="construct-tab-content"]')
    ).toBeVisible();

    const startPositionPicker = page.locator(
      '[data-testid="start-position-picker"]'
    );
    if (await startPositionPicker.isVisible()) {
      const firstPosition = startPositionPicker
        .locator(".position-option")
        .first();
      await firstPosition.click();
      await page.waitForTimeout(500);
    }

    const optionViewer = page.locator('[data-testid="option-viewer"]');
    const firstOption = optionViewer.locator(".option-card").first();
    await firstOption.click();
    await page.waitForTimeout(500);

    // 3. Clear the sequence while still on Construct tab
    const clearButton = page.locator("button").filter({ hasText: /clear/i });
    await clearButton.click();
    await page.waitForTimeout(500);

    // 4. Verify we're still on Construct tab
    await expect(
      page.locator('[data-testid="construct-tab-content"]')
    ).toBeVisible();
    await expect(
      page.locator('[data-testid="start-position-picker"]')
    ).toBeVisible();
  });

  test("clearing from Generate tab stays on Generate", async ({ page }) => {
    // 1. Navigate to Build module
    const buildTab = page
      .locator(".nav-tab-container")
      .filter({ hasText: "Build" });
    await buildTab.click();

    // 2. Navigate to Generate tab
    const generateButton = page
      .locator(".main-tab-btn")
      .filter({ hasText: "Generate" });
    await generateButton.click();
    await page.waitForTimeout(500);
    await expect(page.locator('[data-testid="generate-panel"]')).toBeVisible();

    // 3. Generate a sequence
    const generateSequenceButton = page
      .locator("button")
      .filter({ hasText: /generate/i })
      .first();
    await generateSequenceButton.click();
    await page.waitForTimeout(1000);

    // 4. Clear the sequence while still on Generate tab
    const clearButton = page.locator("button").filter({ hasText: /clear/i });
    await clearButton.click();
    await page.waitForTimeout(500);

    // 5. Verify we're still on Generate tab
    await expect(page.locator('[data-testid="generate-panel"]')).toBeVisible();
  });
});
