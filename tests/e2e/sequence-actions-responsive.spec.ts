/**
 * Sequence Actions Panel - Responsive Layout Tests
 *
 * Tests the intelligent container query-based responsive layout system
 * to ensure action cards adapt properly to different container sizes
 * and aspect ratios without overflow or unwieldy sizing.
 */

import { test, expect, type Page } from "@playwright/test";

// Common viewport configurations to test
const viewports = {
  mobile: { width: 375, height: 667 }, // iPhone SE
  mobileLandscape: { width: 667, height: 375 }, // iPhone SE landscape
  tablet: { width: 768, height: 1024 }, // iPad Mini
  tabletLandscape: { width: 1024, height: 768 }, // iPad Mini landscape
  desktop: { width: 1280, height: 720 }, // Standard desktop
  wide: { width: 1920, height: 1080 }, // Full HD
  ultraWide: { width: 2560, height: 1440 }, // 2K
};

test.describe("Sequence Actions - Responsive Layout", () => {
  // Helper function to open sequence actions panel
  async function openSequenceActionsPanel(page: Page) {
    // Wait for app to be ready
    await page.waitForLoadState("networkidle");
    await page.waitForSelector(".create-tab", { timeout: 10000 });

    // Find sequence actions button
    const sequenceActionsButton = page
      .locator("button")
      .filter({
        hasText: /actions|sequence/i,
      })
      .first();

    // Open panel
    await sequenceActionsButton.click();
    await page.waitForTimeout(500); // Wait for animation

    // Verify panel is visible
    const panel = page.locator('[data-testid="sequence-actions-sheet"]');
    await expect(panel).toBeVisible({ timeout: 5000 });

    return panel;
  }

  // Helper function to get grid layout info
  async function getGridLayoutInfo(page: Page) {
    return await page.evaluate(() => {
      const grid = document.querySelector(".actions-grid");
      if (!grid) return null;

      const styles = window.getComputedStyle(grid);
      const gridTemplateColumns = styles.gridTemplateColumns;
      const gap = styles.gap;

      // Count columns by parsing grid-template-columns
      const columnCount = gridTemplateColumns.split(" ").length;

      return {
        columns: columnCount,
        gap: gap,
        width: grid.clientWidth,
        height: grid.clientHeight,
      };
    });
  }

  // Helper function to check button sizes
  async function getButtonSizes(page: Page) {
    return await page.evaluate(() => {
      const buttons = Array.from(document.querySelectorAll(".action-button"));
      return buttons.map((button) => ({
        width: button.clientWidth,
        height: button.clientHeight,
      }));
    });
  }

  // Helper function to check for overflow
  async function checkForOverflow(page: Page) {
    return await page.evaluate(() => {
      const panel = document.querySelector(".actions-panel__content");
      const grid = document.querySelector(".actions-grid");

      if (!panel || !grid) return { hasOverflow: false };

      const panelWidth = panel.clientWidth;
      const gridWidth = grid.scrollWidth;
      const hasHorizontalOverflow = gridWidth > panelWidth;

      return {
        hasOverflow: hasHorizontalOverflow,
        panelWidth,
        gridWidth,
        overflow: gridWidth - panelWidth,
      };
    });
  }

  test.describe("Mobile Portrait (375x667)", () => {
    test.use({ viewport: viewports.mobile });

    test("should display in 2-column layout", async ({ page }) => {
      await page.goto("http://localhost:5173");
      await openSequenceActionsPanel(page);

      const layoutInfo = await getGridLayoutInfo(page);
      expect(layoutInfo).not.toBeNull();
      expect(layoutInfo!.columns).toBe(2);

      // Take screenshot for visual verification
      await page.screenshot({
        path: "test-screenshots/responsive/mobile-portrait.png",
        fullPage: true,
      });
    });

    test("should not have horizontal overflow", async ({ page }) => {
      await page.goto("http://localhost:5173");
      await openSequenceActionsPanel(page);

      const overflow = await checkForOverflow(page);
      expect(overflow.hasOverflow).toBe(false);
    });

    test("should have reasonably sized buttons", async ({ page }) => {
      await page.goto("http://localhost:5173");
      await openSequenceActionsPanel(page);

      const buttonSizes = await getButtonSizes(page);

      // All buttons should be between 70-160px height
      buttonSizes.forEach((size: { width: number; height: number }) => {
        expect(size.height).toBeGreaterThanOrEqual(70);
        expect(size.height).toBeLessThanOrEqual(160);
      });
    });
  });

  test.describe("Mobile Landscape (667x375)", () => {
    test.use({ viewport: viewports.mobileLandscape });

    test("should adapt to landscape layout", async ({ page }) => {
      await page.goto("http://localhost:5173");
      await openSequenceActionsPanel(page);

      const layoutInfo = await getGridLayoutInfo(page);
      expect(layoutInfo).not.toBeNull();

      // Should use horizontal layout in landscape
      expect(layoutInfo!.columns).toBeGreaterThanOrEqual(2);

      await page.screenshot({
        path: "test-screenshots/responsive/mobile-landscape.png",
        fullPage: true,
      });
    });

    test("should not have overflow in landscape", async ({ page }) => {
      await page.goto("http://localhost:5173");
      await openSequenceActionsPanel(page);

      const overflow = await checkForOverflow(page);
      expect(overflow.hasOverflow).toBe(false);
    });
  });

  test.describe("Tablet Portrait (768x1024)", () => {
    test.use({ viewport: viewports.tablet });

    test("should display in appropriate layout for tablet", async ({
      page,
    }) => {
      await page.goto("http://localhost:5173");
      await openSequenceActionsPanel(page);

      const layoutInfo = await getGridLayoutInfo(page);
      expect(layoutInfo).not.toBeNull();

      // Tablet should have 2 or 4 columns depending on aspect ratio
      expect([2, 4]).toContain(layoutInfo!.columns);

      await page.screenshot({
        path: "test-screenshots/responsive/tablet-portrait.png",
        fullPage: true,
      });
    });
  });

  test.describe("Tablet Landscape (1024x768)", () => {
    test.use({ viewport: viewports.tabletLandscape });

    test("should use wide layout in tablet landscape", async ({ page }) => {
      await page.goto("http://localhost:5173");
      await openSequenceActionsPanel(page);

      const layoutInfo = await getGridLayoutInfo(page);
      expect(layoutInfo).not.toBeNull();

      // Landscape should favor more columns
      expect(layoutInfo!.columns).toBeGreaterThanOrEqual(4);

      await page.screenshot({
        path: "test-screenshots/responsive/tablet-landscape.png",
        fullPage: true,
      });
    });

    test("buttons should not be unwieldy in landscape", async ({ page }) => {
      await page.goto("http://localhost:5173");
      await openSequenceActionsPanel(page);

      const buttonSizes = await getButtonSizes(page);

      // Buttons should be constrained even in wide layout
      buttonSizes.forEach((size: { width: number; height: number }) => {
        expect(size.width).toBeLessThanOrEqual(200);
        expect(size.height).toBeLessThanOrEqual(160);
      });
    });
  });

  test.describe("Desktop (1280x720)", () => {
    test.use({ viewport: viewports.desktop });

    test("should display in 4-column grid", async ({ page }) => {
      await page.goto("http://localhost:5173");
      await openSequenceActionsPanel(page);

      const layoutInfo = await getGridLayoutInfo(page);
      expect(layoutInfo).not.toBeNull();
      expect(layoutInfo!.columns).toBeGreaterThanOrEqual(4);

      await page.screenshot({
        path: "test-screenshots/responsive/desktop.png",
        fullPage: true,
      });
    });
  });

  test.describe("Wide Desktop (1920x1080)", () => {
    test.use({ viewport: viewports.wide });

    test("should handle wide layout without overflow", async ({ page }) => {
      await page.goto("http://localhost:5173");
      await openSequenceActionsPanel(page);

      const overflow = await checkForOverflow(page);
      expect(overflow.hasOverflow).toBe(false);

      await page.screenshot({
        path: "test-screenshots/responsive/wide-desktop.png",
        fullPage: true,
      });
    });

    test("should constrain button sizes on wide screens", async ({ page }) => {
      await page.goto("http://localhost:5173");
      await openSequenceActionsPanel(page);

      const buttonSizes = await getButtonSizes(page);

      // On very wide screens, buttons should be constrained to max-width
      buttonSizes.forEach((size: { width: number; height: number }) => {
        expect(size.width).toBeLessThanOrEqual(180); // Allow some margin
        expect(size.height).toBeLessThanOrEqual(160);
      });
    });
  });

  test.describe("Ultra-Wide (2560x1440)", () => {
    test.use({ viewport: viewports.ultraWide });

    test("should center content and not stretch buttons unwieldily", async ({
      page,
    }) => {
      await page.goto("http://localhost:5173");
      await openSequenceActionsPanel(page);

      const buttonSizes = await getButtonSizes(page);

      // Even on ultra-wide, buttons should be reasonable
      buttonSizes.forEach((size: { width: number; height: number }) => {
        expect(size.width).toBeLessThanOrEqual(180);
        expect(size.height).toBeLessThanOrEqual(160);
      });

      const layoutInfo = await getGridLayoutInfo(page);
      // Should show 5 items in a row on ultra-wide
      expect(layoutInfo!.columns).toBe(5);

      await page.screenshot({
        path: "test-screenshots/responsive/ultra-wide.png",
        fullPage: true,
      });
    });
  });

  test.describe("Edge Cases", () => {
    test("very narrow viewport (320px)", async ({ page }) => {
      await page.setViewportSize({ width: 320, height: 568 });
      await page.goto("http://localhost:5173");
      await openSequenceActionsPanel(page);

      const layoutInfo = await getGridLayoutInfo(page);
      expect(layoutInfo).not.toBeNull();

      // Should handle very narrow screens gracefully
      expect(layoutInfo!.columns).toBeGreaterThanOrEqual(1);

      const overflow = await checkForOverflow(page);
      expect(overflow.hasOverflow).toBe(false);

      await page.screenshot({
        path: "test-screenshots/responsive/very-narrow.png",
        fullPage: true,
      });
    });

    test("square viewport (800x800)", async ({ page }) => {
      await page.setViewportSize({ width: 800, height: 800 });
      await page.goto("http://localhost:5173");
      await openSequenceActionsPanel(page);

      const layoutInfo = await getGridLayoutInfo(page);
      expect(layoutInfo).not.toBeNull();

      const overflow = await checkForOverflow(page);
      expect(overflow.hasOverflow).toBe(false);

      await page.screenshot({
        path: "test-screenshots/responsive/square.png",
        fullPage: true,
      });
    });
  });

  test.describe("Container Resize Behavior", () => {
    test("should adapt layout when container is resized", async ({ page }) => {
      await page.setViewportSize(viewports.mobile);
      await page.goto("http://localhost:5173");
      await openSequenceActionsPanel(page);

      // Get initial layout
      const initialLayout = await getGridLayoutInfo(page);

      // Resize to desktop
      await page.setViewportSize(viewports.desktop);
      await page.waitForTimeout(500); // Wait for layout to update

      // Get new layout
      const newLayout = await getGridLayoutInfo(page);

      // Layout should have changed
      expect(newLayout!.columns).not.toBe(initialLayout!.columns);
      expect(newLayout!.columns).toBeGreaterThan(initialLayout!.columns);
    });
  });

  test.describe("Accessibility", () => {
    test.use({ viewport: viewports.mobile });

    test("buttons should maintain minimum tap target size", async ({
      page,
    }) => {
      await page.goto("http://localhost:5173");
      await openSequenceActionsPanel(page);

      const buttonSizes = await getButtonSizes(page);

      // All buttons should be at least 44x44 for touch accessibility
      buttonSizes.forEach((size: { width: number; height: number }) => {
        expect(size.width).toBeGreaterThanOrEqual(44);
        expect(size.height).toBeGreaterThanOrEqual(44);
      });
    });

    test("buttons should be keyboard navigable at all sizes", async ({
      page,
    }) => {
      await page.goto("http://localhost:5173");
      await openSequenceActionsPanel(page);

      // Tab through buttons
      await page.keyboard.press("Tab");
      await page.keyboard.press("Tab");

      // Check that a button has focus
      const focusedElement = await page.evaluate(() => {
        const activeEl = document.activeElement;
        return activeEl?.classList.contains("action-button");
      });

      expect(focusedElement).toBe(true);
    });
  });

  test.describe("Visual Regression", () => {
    // These tests create screenshots for visual comparison

    test("all viewports should render consistently", async ({ page }) => {
      for (const [name, viewport] of Object.entries(viewports)) {
        await page.setViewportSize(viewport);
        await page.goto("http://localhost:5173");
        await openSequenceActionsPanel(page);

        await page.screenshot({
          path: `test-screenshots/responsive/visual-${name}.png`,
          fullPage: true,
        });
      }
    });
  });
});
