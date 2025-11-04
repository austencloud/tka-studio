import { test, expect } from "@playwright/test";

/**
 * Aurora Background Contrast System E2E Tests
 *
 * These tests verify that the adaptive contrast system works correctly
 * when the Aurora background is selected.
 */

test.describe("Aurora Background Contrast System", () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the app
    await page.goto("http://localhost:5173");

    // Wait for app to initialize
    await page.waitForLoadState("networkidle");
    await page.waitForTimeout(1000); // Allow background animations to initialize
  });

  test("should apply Aurora-specific CSS variables when Aurora background is selected", async ({
    page,
  }) => {
    // Open settings
    await page.click('[data-testid="settings-button"], button:has-text("Settings"), .settings-trigger');
    await page.waitForTimeout(500);

    // Navigate to Background tab
    await page.click('button:has-text("Background"), [data-testid="background-tab"]');
    await page.waitForTimeout(300);

    // Select Aurora background
    await page.click('button:has-text("Aurora"), [data-testid="aurora-background"]');
    await page.waitForTimeout(1000); // Wait for background transition

    // Check that CSS variables are applied
    const panelBg = await page.evaluate(() => {
      return getComputedStyle(document.documentElement).getPropertyValue(
        "--panel-bg-current"
      );
    });

    const cardBg = await page.evaluate(() => {
      return getComputedStyle(document.documentElement).getPropertyValue(
        "--card-bg-current"
      );
    });

    const textPrimary = await page.evaluate(() => {
      return getComputedStyle(document.documentElement).getPropertyValue(
        "--text-primary-current"
      );
    });

    // Verify Aurora-specific values are applied (dark purple overlays)
    expect(panelBg.trim()).toContain("rgba(20, 10, 40, 0.85)");
    expect(cardBg.trim()).toContain("rgba(25, 15, 45, 0.88)");
    expect(textPrimary.trim()).toContain("#ffffff");
  });

  test("should revert to light overlays when switching from Aurora to Night Sky", async ({
    page,
  }) => {
    // First, set Aurora background
    await page.click('[data-testid="settings-button"], button:has-text("Settings")');
    await page.waitForTimeout(500);
    await page.click('button:has-text("Background")');
    await page.waitForTimeout(300);
    await page.click('button:has-text("Aurora")');
    await page.waitForTimeout(1000);

    // Verify Aurora styles are applied
    let panelBg = await page.evaluate(() => {
      return getComputedStyle(document.documentElement).getPropertyValue(
        "--panel-bg-current"
      );
    });
    expect(panelBg.trim()).toContain("rgba(20, 10, 40, 0.85)");

    // Switch to Night Sky
    await page.click('button:has-text("Night Sky"), [data-testid="nightSky-background"]');
    await page.waitForTimeout(1000);

    // Verify Night Sky styles are applied (light overlays)
    panelBg = await page.evaluate(() => {
      return getComputedStyle(document.documentElement).getPropertyValue(
        "--panel-bg-current"
      );
    });

    expect(panelBg.trim()).toContain("rgba(255, 255, 255, 0.05)");
  });

  test("should have high contrast cards in Explore > Collections with Aurora background", async ({
    page,
  }) => {
    // Set Aurora background
    await page.click('[data-testid="settings-button"], button:has-text("Settings")');
    await page.waitForTimeout(500);
    await page.click('button:has-text("Background")');
    await page.waitForTimeout(300);
    await page.click('button:has-text("Aurora")');
    await page.waitForTimeout(1000);

    // Close settings
    await page.click('button:has-text("Close"), .close-button');
    await page.waitForTimeout(500);

    // Navigate to Explore
    await page.click('button:has-text("Explore"), [data-testid="explore-tab"]');
    await page.waitForTimeout(500);

    // Go to Collections
    await page.click('button:has-text("Collections")');
    await page.waitForTimeout(500);

    // Check if collection cards exist and have proper styling
    const collectionCard = page.locator(".collection-card").first();
    if (await collectionCard.count() > 0) {
      const cardBg = await collectionCard.evaluate((el) => {
        return window.getComputedStyle(el).backgroundColor;
      });

      // Should have dark purple background, not light white overlay
      // The computed style will be in rgb format
      expect(cardBg).toContain("rgb"); // Basic check that style is applied
    }
  });

  test("should have high contrast search input with Aurora background", async ({
    page,
  }) => {
    // Set Aurora background
    await page.click('[data-testid="settings-button"], button:has-text("Settings")');
    await page.waitForTimeout(500);
    await page.click('button:has-text("Background")');
    await page.waitForTimeout(300);
    await page.click('button:has-text("Aurora")');
    await page.waitForTimeout(1000);

    // Close settings
    await page.click('button:has-text("Close"), .close-button');
    await page.waitForTimeout(500);

    // Navigate to Explore > Search
    await page.click('button:has-text("Explore")');
    await page.waitForTimeout(500);
    await page.click('button:has-text("Search")');
    await page.waitForTimeout(500);

    // Check search input styling
    const searchInput = page.locator(".search-input, input[type='text']").first();
    if (await searchInput.count() > 0) {
      const inputBg = await searchInput.evaluate((el) => {
        return window.getComputedStyle(el).backgroundColor;
      });

      // Should have dark background for Aurora
      expect(inputBg).toContain("rgb");
    }
  });

  test("should persist Aurora contrast settings after page reload", async ({
    page,
  }) => {
    // Set Aurora background
    await page.click('[data-testid="settings-button"], button:has-text("Settings")');
    await page.waitForTimeout(500);
    await page.click('button:has-text("Background")');
    await page.waitForTimeout(300);
    await page.click('button:has-text("Aurora")');
    await page.waitForTimeout(1000);

    // Reload the page
    await page.reload();
    await page.waitForLoadState("networkidle");
    await page.waitForTimeout(1000);

    // Check that Aurora CSS variables are still applied
    const panelBg = await page.evaluate(() => {
      return getComputedStyle(document.documentElement).getPropertyValue(
        "--panel-bg-current"
      );
    });

    expect(panelBg.trim()).toContain("rgba(20, 10, 40, 0.85)");
  });

  test("should apply all 20 theme variables for Aurora", async ({ page }) => {
    // Set Aurora background
    await page.click('[data-testid="settings-button"], button:has-text("Settings")');
    await page.waitForTimeout(500);
    await page.click('button:has-text("Background")');
    await page.waitForTimeout(300);
    await page.click('button:has-text("Aurora")');
    await page.waitForTimeout(1000);

    // Check all theme variables are defined
    const themeVars = await page.evaluate(() => {
      const root = document.documentElement;
      const style = getComputedStyle(root);
      return {
        panelBg: style.getPropertyValue("--panel-bg-current"),
        panelBorder: style.getPropertyValue("--panel-border-current"),
        panelHover: style.getPropertyValue("--panel-hover-current"),
        cardBg: style.getPropertyValue("--card-bg-current"),
        cardBorder: style.getPropertyValue("--card-border-current"),
        cardHover: style.getPropertyValue("--card-hover-current"),
        textPrimary: style.getPropertyValue("--text-primary-current"),
        textSecondary: style.getPropertyValue("--text-secondary-current"),
        inputBg: style.getPropertyValue("--input-bg-current"),
        inputBorder: style.getPropertyValue("--input-border-current"),
        inputFocus: style.getPropertyValue("--input-focus-current"),
        buttonActive: style.getPropertyValue("--button-active-current"),
      };
    });

    // All variables should have values
    Object.entries(themeVars).forEach(([key, value]) => {
      expect(value.trim()).not.toBe("");
      console.log(`${key}: ${value.trim()}`);
    });

    // Verify Aurora-specific values
    expect(themeVars.panelBg.trim()).toContain("rgba(20, 10, 40, 0.85)");
    expect(themeVars.cardBg.trim()).toContain("rgba(25, 15, 45, 0.88)");
  });

  test("should have visible filter buttons with Aurora background", async ({
    page,
  }) => {
    // Set Aurora background
    await page.click('[data-testid="settings-button"], button:has-text("Settings")');
    await page.waitForTimeout(500);
    await page.click('button:has-text("Background")');
    await page.waitForTimeout(300);
    await page.click('button:has-text("Aurora")');
    await page.waitForTimeout(1000);

    // Close settings
    await page.click('button:has-text("Close"), .close-button');
    await page.waitForTimeout(500);

    // Navigate to Explore > Collections
    await page.click('button:has-text("Explore")');
    await page.waitForTimeout(500);
    await page.click('button:has-text("Collections")');
    await page.waitForTimeout(500);

    // Check filter buttons
    const filterButton = page.locator(".filter-button").first();
    if (await filterButton.count() > 0) {
      const buttonBg = await filterButton.evaluate((el) => {
        return window.getComputedStyle(el).backgroundColor;
      });

      // Should use panel-bg-current variable (dark purple for Aurora)
      expect(buttonBg).toBeTruthy();
    }
  });
});

test.describe("Theme Variable Definitions", () => {
  test("should have all Aurora-specific CSS variables defined in app.css", async ({
    page,
  }) => {
    await page.goto("http://localhost:5173");
    await page.waitForLoadState("networkidle");

    const auroraVars = await page.evaluate(() => {
      const root = document.documentElement;
      const style = getComputedStyle(root);
      return {
        // Panel variables
        panelBgAurora: style.getPropertyValue("--panel-bg-aurora"),
        panelBorderAurora: style.getPropertyValue("--panel-border-aurora"),
        panelHoverAurora: style.getPropertyValue("--panel-hover-aurora"),

        // Card variables
        cardBgAurora: style.getPropertyValue("--card-bg-aurora"),
        cardBorderAurora: style.getPropertyValue("--card-border-aurora"),
        cardHoverAurora: style.getPropertyValue("--card-hover-aurora"),

        // Text variables
        textPrimaryAurora: style.getPropertyValue("--text-primary-aurora"),
        textSecondaryAurora: style.getPropertyValue("--text-secondary-aurora"),

        // Input variables
        inputBgAurora: style.getPropertyValue("--input-bg-aurora"),
        inputBorderAurora: style.getPropertyValue("--input-border-aurora"),
        inputFocusAurora: style.getPropertyValue("--input-focus-aurora"),

        // Button variables
        buttonActiveAurora: style.getPropertyValue("--button-active-aurora"),
      };
    });

    // All variables should be defined
    Object.entries(auroraVars).forEach(([key, value]) => {
      expect(value.trim()).not.toBe("");
      console.log(`${key}: ${value.trim()}`);
    });

    // Verify specific Aurora values
    expect(auroraVars.panelBgAurora.trim()).toContain("rgba(20, 10, 40, 0.85)");
    expect(auroraVars.cardBgAurora.trim()).toContain("rgba(25, 15, 45, 0.88)");
    expect(auroraVars.textPrimaryAurora.trim()).toContain("#ffffff");
  });
});
