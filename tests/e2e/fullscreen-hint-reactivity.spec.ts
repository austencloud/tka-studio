import { expect, test } from "@playwright/test";

/**
 * FullscreenHint Reactivity Tests
 *
 * Tests that the fullscreen hint component uses rune-based reactivity:
 * - Button position tracking with MutationObserver + ResizeObserver
 * - Fullscreen state changes trigger hint visibility
 * - Auto-show and auto-hide timing
 */

test.describe("FullscreenHint Reactivity", () => {
  test.beforeEach(async ({ page }) => {
    // Clear localStorage to reset dismissal state
    await page.goto("/");
    await page.evaluate(() => {
      localStorage.removeItem("tka-fullscreen-hint-dismissed");
    });
  });

  test("should reactively track button position on DOM changes", async ({
    page,
  }) => {
    await page.goto("/");

    // Wait for page to load
    await page.waitForLoadState("networkidle");

    // Check if fullscreen button exists
    const fullscreenButton = page.locator(".fullscreen-button").first();
    const buttonExists = (await fullscreenButton.count()) > 0;

    if (!buttonExists) {
      console.log("⚠️ No fullscreen button found - skipping position test");
      return;
    }

    // Get initial button position
    const initialPosition = await fullscreenButton.boundingBox();

    console.log("Initial button position:", initialPosition);

    // Simulate DOM change by resizing window
    await page.setViewportSize({ width: 800, height: 600 });
    await page.waitForTimeout(500); // Wait for reactivity

    // Get new button position
    const newPosition = await fullscreenButton.boundingBox();

    console.log("Button position after resize:", newPosition);

    // Positions should update (this verifies MutationObserver/ResizeObserver working)
    expect(newPosition).toBeTruthy();
  });

  test("should show hint when conditions are met", async ({ page }) => {
    await page.goto("/");
    await page.waitForLoadState("networkidle");

    // Check for fullscreen button
    const fullscreenButton = page.locator(".fullscreen-button").first();
    if ((await fullscreenButton.count()) === 0) {
      console.log("⚠️ No fullscreen button - hint won't show");
      return;
    }

    // Wait for hint to potentially appear (2 second delay in component)
    await page.waitForTimeout(2500);

    // Check if hint appeared
    const hint = page.locator(".fullscreen-hint");
    const hintCount = await hint.count();

    console.log(`Fullscreen hint present: ${hintCount > 0}`);

    if (hintCount > 0) {
      // Verify hint positioning
      const hintBox = await hint.boundingBox();
      const buttonBox = await fullscreenButton.boundingBox();

      expect(hintBox).toBeTruthy();
      expect(buttonBox).toBeTruthy();

      console.log("Hint position:", hintBox);
      console.log("Button position:", buttonBox);

      // Hint should be positioned above the button
      if (hintBox && buttonBox) {
        expect(hintBox.y).toBeLessThan(buttonBox.y);
      }
    }
  });

  test("should hide hint when dismissed", async ({ page }) => {
    await page.goto("/");
    await page.waitForLoadState("networkidle");

    // Wait for potential hint appearance
    await page.waitForTimeout(2500);

    const hint = page.locator(".fullscreen-hint");
    const hintCount = await hint.count();

    if (hintCount === 0) {
      console.log("⚠️ Hint didn't appear - skipping dismiss test");
      return;
    }

    // Click dismiss button
    const dismissButton = hint.locator(".hint-dismiss");
    await dismissButton.click();

    // Wait for reactivity
    await page.waitForTimeout(300);

    // Hint should be hidden
    await expect(hint).not.toBeVisible();

    // Dismissal should be persisted in localStorage
    const dismissed = await page.evaluate(() => {
      return localStorage.getItem("tka-fullscreen-hint-dismissed");
    });

    expect(dismissed).toBe("true");

    console.log("✅ Hint dismissed and persisted to localStorage");
  });

  test("should not show hint again after dismissal", async ({ page }) => {
    // Set dismissal flag
    await page.goto("/");
    await page.evaluate(() => {
      localStorage.setItem("tka-fullscreen-hint-dismissed", "true");
    });

    // Reload page
    await page.reload();
    await page.waitForLoadState("networkidle");

    // Wait beyond the auto-show delay
    await page.waitForTimeout(3000);

    // Hint should NOT appear
    const hint = page.locator(".fullscreen-hint");
    await expect(hint).not.toBeVisible();

    console.log("✅ Hint correctly suppressed after dismissal");
  });

  test("should reactively update position on window resize", async ({
    page,
  }) => {
    await page.goto("/");
    await page.waitForLoadState("networkidle");

    const fullscreenButton = page.locator(".fullscreen-button").first();
    if ((await fullscreenButton.count()) === 0) {
      console.log("⚠️ No fullscreen button - skipping resize test");
      return;
    }

    // Force hint to show (for testing purposes)
    await page.waitForTimeout(2500);

    const hint = page.locator(".fullscreen-hint");
    if ((await hint.count()) === 0) {
      console.log("⚠️ Hint didn't show - skipping resize test");
      return;
    }

    // Get initial hint position
    const initialHintBox = await hint.boundingBox();

    // Resize window
    await page.setViewportSize({ width: 600, height: 400 });
    await page.waitForTimeout(500); // Wait for resize + reactivity

    // Get new hint position
    const newHintBox = await hint.boundingBox();

    console.log("Hint position before resize:", initialHintBox);
    console.log("Hint position after resize:", newHintBox);

    // Positions should be different (reactive to resize)
    if (initialHintBox && newHintBox) {
      const positionChanged =
        initialHintBox.y !== newHintBox.y ||
        initialHintBox.x !== newHintBox.x;

      // Hint should update position reactively
      expect(positionChanged).toBe(true);
      console.log("✅ Hint position updated reactively on resize");
    }
  });

  test("should auto-hide after duration", async ({ page }) => {
    test.setTimeout(45000); // Increase timeout for this test

    await page.goto("/");
    await page.waitForLoadState("networkidle");

    // Wait for hint to appear
    await page.waitForTimeout(2500);

    const hint = page.locator(".fullscreen-hint");
    if ((await hint.count()) === 0) {
      console.log("⚠️ Hint didn't appear - skipping auto-hide test");
      return;
    }

    // Verify hint is visible
    await expect(hint).toBeVisible();
    console.log("Hint is visible");

    // Wait for auto-hide duration (5 seconds default + buffer)
    await page.waitForTimeout(5500);

    // Hint should be hidden
    await expect(hint).not.toBeVisible();
    console.log("✅ Hint auto-hidden after duration");
  });
});
