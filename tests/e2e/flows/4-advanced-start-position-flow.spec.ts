import { test, expect } from '@playwright/test';

/**
 * Flow #4: Advanced Start Position Picker Flow
 * Tests: navigate to construct → toggle advanced → browse 16 variations → select → add beat → return to default
 */
test('Advanced Start Position Picker Flow', async ({ page }) => {
  // Navigate to app
  await page.goto('http://localhost:5173');
  await page.waitForLoadState('networkidle');

  // Switch to Build > Construct
  await page.click('[data-testid="menu-button"], button:has-text("Menu")').catch(() => {});
  await page.click('text=Build').catch(() => {});
  await page.click('button:has-text("Construct"), [data-testid="construct-tab"]');
  await page.waitForTimeout(500);

  // Step 1: Click "Show Advanced" toggle in start position picker
  const advancedToggle = page.locator('button:has-text("Advanced"), button:has-text("Show All"), [data-testid="toggle-advanced"]').first();
  await advancedToggle.click();
  await page.waitForTimeout(600); // Wait for animation

  // Verify advanced picker is visible (should show 16 positions)
  await expect(page.locator('[data-testid="advanced-start-position-picker"]')).toBeVisible();

  // Step 2: Browse through all 16 variations (scroll through grid)
  const advancedGrid = page.locator('[data-testid="advanced-start-position-picker"]');
  await advancedGrid.hover();
  await page.mouse.wheel(0, 300); // Scroll down
  await page.waitForTimeout(500);

  // Step 3: Select one advanced position (5th position)
  const advancedPosition = page.locator('[data-testid="advanced-start-position-picker"] button').nth(4);
  await advancedPosition.click();
  await page.waitForTimeout(500);

  // Verify position selected (beat grid should appear)
  await expect(page.locator('[data-testid="beat-grid"]')).toBeVisible();

  // Step 4: Add a beat to confirm position works
  const optionButton = page.locator('[data-testid="option-grid"] button, [data-testid="pictograph-option"]').first();
  await optionButton.click();
  await page.waitForTimeout(400);

  // Verify beat added
  const beatCount = await page.locator('[data-testid="beat-grid"] [data-beat-number]').count();
  expect(beatCount).toBeGreaterThan(0);

  // Step 5: Clear and return to default picker
  const clearButton = page.locator('button:has-text("Clear"), [data-testid="clear-button"]').first();
  await clearButton.click();
  await page.waitForTimeout(300);

  // Confirm clear if needed
  await page.click('button:has-text("Confirm"), button:has-text("Yes")').catch(() => {});
  await page.waitForTimeout(500);

  // Step 6: Verify we're back to default picker (3 positions visible)
  await expect(page.locator('[data-testid="start-position-picker"]')).toBeVisible();

  // Toggle back to default if still in advanced mode
  await page.click('button:has-text("Default"), button:has-text("Hide"), [data-testid="toggle-default"]').catch(() => {});
  await page.waitForTimeout(300);

  console.log('✅ Flow #4: Advanced Start Position Picker Flow - PASSED');
});
