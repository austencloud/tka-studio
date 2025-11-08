import { test, expect } from "@playwright/test";

test.describe("Settings Miscellaneous Tab - Mobile Layout", () => {
  test("should fit content without scrolling on iPhone SE viewport", async ({
    page,
  }) => {
    // Set iPhone SE viewport size
    await page.setViewportSize({ width: 375, height: 667 });

    // Navigate to the app
    await page.goto("http://localhost:5173");

    // Wait for the page to load
    await page.waitForLoadState("networkidle");

    // Click the Settings button
    await page.getByRole("button", { name: /settings/i }).click();

    // Wait for settings dialog to open
    await page.waitForSelector('[role="dialog"]', { state: "visible" });

    // Click on Miscellaneous tab
    await page.getByRole("button", { name: /miscellaneous/i }).click();

    // Wait a moment for content to render
    await page.waitForTimeout(500);

    // Get the content area
    const content = page.locator(".settings-sheet__content");

    // Check if content is scrollable
    const scrollInfo = await content.evaluate((el) => ({
      scrollHeight: el.scrollHeight,
      clientHeight: el.clientHeight,
      isScrollable: el.scrollHeight > el.clientHeight,
      overflow: el.scrollHeight - el.clientHeight,
    }));

    console.log("Scroll Info:", scrollInfo);

    // Take a screenshot
    await page.screenshot({
      path: "tests/screenshots/miscellaneous-mobile.png",
      fullPage: false,
    });

    // Assert that content is not scrollable
    expect(scrollInfo.isScrollable).toBe(false);

    // Additional check: content should fit with some buffer (allow 5px tolerance)
    expect(scrollInfo.overflow).toBeLessThanOrEqual(5);
  });

  test("should have all interactive elements accessible on mobile", async ({
    page,
  }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto("http://localhost:5173");
    await page.waitForLoadState("networkidle");

    // Open settings and navigate to Miscellaneous
    await page.getByRole("button", { name: /settings/i }).click();
    await page.getByRole("button", { name: /miscellaneous/i }).click();
    await page.waitForTimeout(500);

    // Check that all toggle switches are visible and clickable
    const toggles = page.locator(".toggle-switch input");
    const toggleCount = await toggles.count();

    expect(toggleCount).toBeGreaterThanOrEqual(2); // At least Haptic and Motion

    // Check that Clear Cache button is visible and clickable
    const clearButton = page.getByRole("button", { name: /clear/i });
    await expect(clearButton).toBeVisible();

    // Verify buttons meet minimum touch target size (44x44px per WCAG)
    const buttonBox = await clearButton.boundingBox();
    expect(buttonBox?.height).toBeGreaterThanOrEqual(44);
  });
});
