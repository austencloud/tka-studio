import { test, expect } from "@playwright/test";

// Configure browser with touch support
test.use({
  hasTouch: true,
  isMobile: true,
  viewport: { width: 375, height: 667 },
});

test.describe("Settings Button - Swipe State Bug", () => {
  test("should clear active state when settings panel is swiped closed", async ({
    page,
  }) => {
    // Viewport already set via test.use above

    // Navigate to the app
    await page.goto("http://localhost:5173");

    // Wait for the page to load
    await page.waitForLoadState("networkidle");

    // Find the settings button
    const settingsButton = page.locator(".settings-button");
    await expect(settingsButton).toBeVisible();

    // Verify initial state - button should not be active
    let hasActiveClass = await settingsButton.evaluate((el) =>
      el.classList.contains("active")
    );
    expect(hasActiveClass).toBe(false);

    // Click the Settings button to open the panel
    await settingsButton.click();

    // Wait for settings dialog to open
    await page.waitForSelector('[role="dialog"]', { state: "visible" });

    // Verify button is now active (highlighted)
    hasActiveClass = await settingsButton.evaluate((el) =>
      el.classList.contains("active")
    );
    expect(hasActiveClass).toBe(true);

    // Simulate swipe down gesture to close the panel
    const drawer = page.locator('[role="dialog"]');
    const drawerBox = await drawer.boundingBox();

    if (!drawerBox) {
      throw new Error("Could not find drawer bounding box");
    }

    // Perform swipe gesture using Playwright's touchscreen API
    const startX = drawerBox.x + drawerBox.width / 2;
    const startY = drawerBox.y + 20;
    const endY = drawerBox.y + 200;

    // Touch start
    await page.touchscreen.tap(startX, startY);
    await page.waitForTimeout(50);

    // Swipe down
    await page.mouse.move(startX, startY);
    await page.mouse.down();
    await page.mouse.move(startX, endY, { steps: 10 });
    await page.mouse.up();

    // Wait for animation to complete
    await page.waitForTimeout(500);

    // Verify the drawer is closed
    await expect(drawer).not.toBeVisible();

    // CRITICAL CHECK: Verify button is no longer active after swipe
    hasActiveClass = await settingsButton.evaluate((el) =>
      el.classList.contains("active")
    );
    expect(hasActiveClass).toBe(false);

    // Additional verification: button should be clickable again immediately
    await settingsButton.click();
    await page.waitForTimeout(300);

    // Verify settings panel reopens
    await expect(drawer).toBeVisible();

    // Verify button is active again
    hasActiveClass = await settingsButton.evaluate((el) =>
      el.classList.contains("active")
    );
    expect(hasActiveClass).toBe(true);
  });

  test("should clear active state when settings panel is closed via close button", async ({
    page,
  }) => {
    // Viewport already set via test.use above

    // Navigate to the app
    await page.goto("http://localhost:5173");
    await page.waitForLoadState("networkidle");

    // Find the settings button
    const settingsButton = page.locator(".settings-button");

    // Click to open settings
    await settingsButton.click();
    await page.waitForSelector('[role="dialog"]', { state: "visible" });

    // Verify button is active
    let hasActiveClass = await settingsButton.evaluate((el) =>
      el.classList.contains("active")
    );
    expect(hasActiveClass).toBe(true);

    // Click the close button in the header
    const closeButton = page.locator(".settings-sheet__close");
    await closeButton.click();

    // Wait for panel to close
    await page.waitForTimeout(500);

    // Verify button is no longer active
    hasActiveClass = await settingsButton.evaluate((el) =>
      el.classList.contains("active")
    );
    expect(hasActiveClass).toBe(false);
  });

  test("should clear active state when settings panel backdrop is clicked", async ({
    page,
  }) => {
    // Viewport already set via test.use above

    // Navigate to the app
    await page.goto("http://localhost:5173");
    await page.waitForLoadState("networkidle");

    // Find the settings button
    const settingsButton = page.locator(".settings-button");

    // Click to open settings
    await settingsButton.click();
    await page.waitForSelector('[role="dialog"]', { state: "visible" });

    // Verify button is active
    let hasActiveClass = await settingsButton.evaluate((el) =>
      el.classList.contains("active")
    );
    expect(hasActiveClass).toBe(true);

    // Click the backdrop (overlay)
    const backdrop = page.locator(".drawer-overlay");
    await backdrop.click({ position: { x: 10, y: 10 } });

    // Wait for panel to close
    await page.waitForTimeout(500);

    // Verify button is no longer active
    hasActiveClass = await settingsButton.evaluate((el) =>
      el.classList.contains("active")
    );
    expect(hasActiveClass).toBe(false);
  });
});
