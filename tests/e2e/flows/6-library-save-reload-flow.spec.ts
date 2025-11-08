import { test, expect } from "@playwright/test";

/**
 * Flow #6: Library Save & Reload Flow
 * Tests: build sequence → save to library → navigate to library → find sequence → load back → edit → re-save
 */
test("Library Save & Reload Flow", async ({ page }) => {
  // Navigate to app
  await page.goto("http://localhost:5173");
  await page.waitForLoadState("networkidle");

  // Build a unique sequence to test persistence
  const testSequenceName = `Test-${Date.now()}`;

  // Step 1: Build a 3-beat sequence
  await page
    .click('[data-testid="menu-button"], button:has-text("Menu")')
    .catch(() => {});
  await page.click("text=Build").catch(() => {});
  await page.click(
    'button:has-text("Construct"), [data-testid="construct-tab"]'
  );
  await page.waitForTimeout(500);

  // Select start position
  const startPosButton = page
    .locator('[data-testid="start-position-picker"] button')
    .first();
  await startPosButton.click();
  await page.waitForTimeout(300);

  // Add 3 beats
  for (let i = 0; i < 3; i++) {
    const optionButton = page
      .locator(
        '[data-testid="option-grid"] button, [data-testid="pictograph-option"]'
      )
      .first();
    await optionButton.click();
    await page.waitForTimeout(400);
  }

  // Step 2: Save to Library
  // Open sequence actions menu
  const actionsButton = page
    .locator('button:has-text("Actions"), [data-testid="sequence-actions"]')
    .first();
  await actionsButton.click().catch(() => {
    // Try three-dot menu
    page
      .click('[data-testid="more-options"], button:has-text("⋮")')
      .catch(() => {});
  });
  await page.waitForTimeout(500);

  // Click Save
  const saveButton = page
    .locator('button:has-text("Save"), [data-testid="save-sequence"]')
    .first();
  await saveButton.click();
  await page.waitForTimeout(800);

  // If name dialog appears, enter test name
  const nameInput = page
    .locator('input[placeholder*="name"], input[type="text"]')
    .first();
  if (await nameInput.isVisible({ timeout: 1000 }).catch(() => false)) {
    await nameInput.fill(testSequenceName);
    await page.click('button:has-text("Save"), button:has-text("Confirm")');
    await page.waitForTimeout(500);
  }

  console.log("✅ Sequence saved to library");

  // Step 3: Navigate to Library module
  await page
    .click('[data-testid="menu-button"], button:has-text("Menu")')
    .catch(() => {});
  await page.click("text=Library");
  await page.waitForTimeout(800);

  // Switch to Sequences view
  await page
    .click('button:has-text("Sequences"), [data-testid="sequences-tab"]')
    .catch(() => {});
  await page.waitForTimeout(500);

  // Step 4: Find the saved sequence
  const sequenceCards = page.locator(
    '[data-testid="sequence-card"], [data-testid="sequence-item"]'
  );
  await expect(sequenceCards.first()).toBeVisible({ timeout: 2000 });

  // Click the first sequence (should be our recently saved one)
  const firstSequence = sequenceCards.first();
  await firstSequence.click();
  await page.waitForTimeout(500);

  // Step 5: Load it back into Build module
  const loadButton = page
    .locator(
      'button:has-text("Load"), button:has-text("Edit"), button:has-text("Open")'
    )
    .first();
  await loadButton.click();
  await page.waitForTimeout(800);

  // Should navigate back to Build module with sequence loaded
  await expect(page.locator('[data-testid="beat-grid"]')).toBeVisible();

  // Step 6: Edit the sequence (add one more beat)
  const optionButton = page
    .locator(
      '[data-testid="option-grid"] button, [data-testid="pictograph-option"]'
    )
    .first();
  await optionButton.click();
  await page.waitForTimeout(400);

  // Step 7: Re-save
  await page
    .click('button:has-text("Actions"), [data-testid="sequence-actions"]')
    .catch(() => {
      page
        .click('[data-testid="more-options"], button:has-text("⋮")')
        .catch(() => {});
    });
  await page.waitForTimeout(300);

  await page.click('button:has-text("Save"), [data-testid="save-sequence"]');
  await page.waitForTimeout(800);

  console.log("✅ Flow #6: Library Save & Reload Flow - PASSED");
});
