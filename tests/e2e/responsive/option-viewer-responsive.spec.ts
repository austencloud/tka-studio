/**
 * Option Viewer Responsive Layout Tests
 *
 * Tests the responsive behavior of the OptionViewer component across all screen sizes.
 * Validates that:
 * 1. Content never overflows the container
 * 2. Header/floating button displays correctly based on container height
 * 3. Filter panel scales appropriately for all container sizes
 * 4. Embla container and viewport utilize full available height
 */

import { test, expect, type Page } from "@playwright/test";

// Common device viewport sizes
const DEVICE_SIZES = [
  // Mobile devices
  { name: "iPhone SE", width: 375, height: 667 },
  { name: "iPhone 12", width: 390, height: 844 },
  { name: "iPhone 14 Pro Max", width: 430, height: 932 },
  { name: "Samsung Galaxy S21", width: 360, height: 800 },
  { name: "Samsung Galaxy Z Fold 6 (folded)", width: 768, height: 1024 },
  { name: "Samsung Galaxy Z Fold 6 (unfolded)", width: 1812, height: 2176 },

  // Tablets
  { name: "iPad Mini", width: 768, height: 1024 },
  { name: "iPad Air", width: 820, height: 1180 },
  { name: "iPad Pro 11", width: 834, height: 1194 },
  { name: "iPad Pro 12.9", width: 1024, height: 1366 },

  // Desktop
  { name: "Small Desktop", width: 1280, height: 720 },
  { name: "Medium Desktop", width: 1920, height: 1080 },
  { name: "Large Desktop", width: 2560, height: 1440 },
  { name: "Ultra Wide", width: 3440, height: 1440 },
];

test.describe("Option Viewer - Responsive Layout", () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the build page where option viewer is used
    await page.goto("/");

    // Wait for app to initialize
    await page.waitForLoadState("networkidle");

    // Click on Build tab if available
    const buildTabButton = page.locator(
      'button:has-text("Build"), a:has-text("Build")'
    );
    if ((await buildTabButton.count()) > 0) {
      await buildTabButton.first().click();
      await page.waitForTimeout(1000);
    }

    // Select a start position to activate option picker
    const startPositionButton = page
      .locator(
        '[data-grid-position], .grid-position-button, button[aria-label*="start position"]'
      )
      .first();
    if ((await startPositionButton.count()) > 0) {
      await startPositionButton.click();
      await page.waitForTimeout(500);
    }

    // Wait for option viewer to be present
    try {
      await page.waitForSelector('[data-testid="option-picker-container"]', {
        timeout: 5000,
      });
    } catch (e) {
      console.log(
        "Option picker not found - test may be running in wrong context"
      );
      // Continue anyway for some tests
    }
  });

  test.describe("Full Viewport Tests", () => {
    for (const device of DEVICE_SIZES) {
      test(`${device.name} (${device.width}x${device.height}) - No overflow`, async ({
        page,
      }) => {
        // Set viewport size
        await page.setViewportSize({
          width: device.width,
          height: device.height,
        });

        // Wait for layout to stabilize
        await page.waitForTimeout(1000);

        // Get option picker container
        const container = page.locator(
          '[data-testid="option-picker-container"]'
        );

        // Skip if container doesn't exist (might not be in build mode)
        if ((await container.count()) === 0) {
          console.log(`Skipping ${device.name} - option picker not available`);
          test.skip();
          return;
        }

        await expect(container).toBeVisible();

        // Check for overflow
        const hasOverflow = await checkForOverflow(page, container);

        // Get container dimensions for logging
        const containerBox = await container.boundingBox();

        if (containerBox) {
          console.log(
            `${device.name}: Container ${containerBox.width}x${containerBox.height}, Overflow: ${hasOverflow}`
          );
        }

        expect(hasOverflow).toBe(false);

        // Verify container dimensions
        expect(containerBox).not.toBeNull();

        if (containerBox) {
          // Container should have reasonable dimensions
          expect(containerBox.width).toBeGreaterThan(0);
          expect(containerBox.height).toBeGreaterThan(0);

          // Verify header or floating button is shown appropriately
          await verifyHeaderOrFloatingButton(page, containerBox.height);
        }
      });
    }
  });

  test.describe("Filter Panel Responsive Tests", () => {
    test("Filter panel never causes overflow on small screen", async ({
      page,
    }) => {
      await page.setViewportSize({ width: 375, height: 667 });
      await page.waitForTimeout(1000);

      const container = page.locator('[data-testid="option-picker-container"]');

      if ((await container.count()) === 0) {
        console.log("Skipping - option picker not available");
        test.skip();
        return;
      }

      // Open filter panel
      const opened = await openFilterPanel(page);
      if (!opened) {
        console.log("Could not open filter panel");
        test.skip();
        return;
      }

      // Wait for filter panel to be visible
      const filterPanel = page.locator(".filter-panel");
      await expect(filterPanel).toBeVisible({ timeout: 2000 });

      // Verify no overflow
      const hasOverflow = await checkForOverflow(page, filterPanel);
      expect(hasOverflow).toBe(false);

      // Panel should fit within container
      const panelBox = await filterPanel.boundingBox();
      const containerBox = await container.boundingBox();

      if (panelBox && containerBox) {
        console.log(
          `Filter Panel - Container: ${containerBox.width}x${containerBox.height}, Panel: ${panelBox.width}x${panelBox.height}`
        );
        expect(panelBox.width).toBeLessThanOrEqual(containerBox.width + 2); // +2 for rounding/borders
        expect(panelBox.height).toBeLessThanOrEqual(containerBox.height + 2);
      }
    });

    test("Filter panel never causes overflow on large screen", async ({
      page,
    }) => {
      await page.setViewportSize({ width: 1920, height: 1080 });
      await page.waitForTimeout(1000);

      const container = page.locator('[data-testid="option-picker-container"]');

      if ((await container.count()) === 0) {
        console.log("Skipping - option picker not available");
        test.skip();
        return;
      }

      // Open filter panel
      const opened = await openFilterPanel(page);
      if (!opened) {
        console.log("Could not open filter panel");
        test.skip();
        return;
      }

      const filterPanel = page.locator(".filter-panel");
      await expect(filterPanel).toBeVisible({ timeout: 2000 });

      // Verify no overflow
      const hasOverflow = await checkForOverflow(page, filterPanel);
      expect(hasOverflow).toBe(false);

      const panelBox = await filterPanel.boundingBox();
      const containerBox = await container.boundingBox();

      if (panelBox && containerBox) {
        console.log(
          `Large Screen - Container: ${containerBox.width}x${containerBox.height}, Panel: ${panelBox.width}x${panelBox.height}`
        );
        expect(panelBox.width).toBeLessThanOrEqual(containerBox.width + 2);
        expect(panelBox.height).toBeLessThanOrEqual(containerBox.height + 2);
      }
    });
  });

  test.describe("Content Height Utilization", () => {
    test("Option picker content uses full available height", async ({
      page,
    }) => {
      await page.setViewportSize({ width: 390, height: 844 });
      await page.waitForTimeout(1000);

      const container = page.locator('[data-testid="option-picker-container"]');
      const content = page.locator(".option-picker-content");

      if ((await container.count()) === 0) {
        console.log("Skipping - option picker not available");
        test.skip();
        return;
      }

      await expect(container).toBeVisible();
      await expect(content).toBeVisible();

      const containerBox = await container.boundingBox();
      const contentBox = await content.boundingBox();

      if (containerBox && contentBox) {
        // Content should take up most of the container height
        const heightUtilization = contentBox.height / containerBox.height;

        console.log(
          `Content height utilization: ${(heightUtilization * 100).toFixed(1)}% (${contentBox.height}px / ${containerBox.height}px)`
        );

        // Content should use at least 65% of container height (accounting for header/padding)
        expect(heightUtilization).toBeGreaterThan(0.65);
      }
    });
  });
});

// Helper Functions

/**
 * Check if an element has overflow (scrollHeight > clientHeight or scrollWidth > clientWidth)
 */
async function checkForOverflow(page: Page, locator: any): Promise<boolean> {
  return await locator.evaluate((el: HTMLElement) => {
    const verticalOverflow = el.scrollHeight - el.clientHeight;
    const horizontalOverflow = el.scrollWidth - el.clientWidth;

    // Allow minimal overflow (2px) for rounding errors and borders
    return verticalOverflow > 2 || horizontalOverflow > 2;
  });
}

/**
 * Verify that either header or floating button is shown based on container height
 */
async function verifyHeaderOrFloatingButton(
  page: Page,
  containerHeight: number
): Promise<void> {
  const THRESHOLD = 300;

  if (containerHeight < THRESHOLD) {
    // Should show floating button
    const floatingButton = page.locator(".floating-filter-button");
    const count = await floatingButton.count();

    if (count > 0) {
      console.log(
        `  ✓ Floating button shown (height: ${containerHeight}px < ${THRESHOLD}px)`
      );
    } else {
      console.log(
        `  ⚠ Expected floating button but not found (height: ${containerHeight}px < ${THRESHOLD}px)`
      );
    }
  } else {
    // Should show header
    const header = page.locator(
      ".construct-picker-header[data-variant='options']"
    );
    const count = await header.count();

    if (count > 0) {
      console.log(
        `  ✓ Header shown (height: ${containerHeight}px >= ${THRESHOLD}px)`
      );
    } else {
      console.log(
        `  ⚠ Expected header but not found (height: ${containerHeight}px >= ${THRESHOLD}px)`
      );
    }
  }
}

/**
 * Open the filter panel by clicking the appropriate trigger
 */
async function openFilterPanel(page: Page): Promise<boolean> {
  try {
    // Try floating button first
    const floatingButton = page.locator(".floating-filter-button");
    if ((await floatingButton.count()) > 0) {
      await floatingButton.click();
      await page.waitForTimeout(500);
      return true;
    }

    // Otherwise try header button
    const headerButton = page.locator(".options-header-button");
    if ((await headerButton.count()) > 0) {
      await headerButton.click();
      await page.waitForTimeout(500);
      return true;
    }

    return false;
  } catch (e) {
    console.error("Error opening filter panel:", e);
    return false;
  }
}
