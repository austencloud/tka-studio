import { expect, test } from "@playwright/test";

/**
 * Desktop Sidebar Collapsed Expansion Behavior Test
 *
 * Tests that when clicking a module from collapsed state:
 * 1. The sidebar expands
 * 2. Only the clicked module expands
 * 3. Other modules (including current module) remain collapsed
 */

const DESKTOP_SIZE = { width: 1400, height: 900 };

test.describe("Desktop Sidebar - Collapsed Module Click", () => {
  test("clicking module from collapsed sidebar expands only that module", async ({
    page,
  }) => {
    // Set desktop viewport to trigger desktop sidebar
    await page.setViewportSize(DESKTOP_SIZE);
    await page.goto("/");

    // Wait for desktop sidebar to appear
    const sidebar = page.locator(".desktop-navigation-sidebar");
    await expect(sidebar).toBeVisible({ timeout: 10000 });

    // Wait for initial load to complete
    await page.waitForTimeout(1000);

    // Collapse the sidebar
    const collapseButton = page.locator(".collapse-toggle");
    await collapseButton.click();
    await page.waitForTimeout(300); // Wait for collapse animation

    // Verify sidebar is collapsed
    await expect(sidebar).toHaveClass(/collapsed/);

    // Get all module buttons
    const moduleButtons = page.locator(".module-button");
    const moduleCount = await moduleButtons.count();

    console.log(`Found ${moduleCount} modules`);

    if (moduleCount > 1) {
      // Click the second module (assuming first might be current)
      const secondModule = moduleButtons.nth(1);
      const moduleLabel = await secondModule.getAttribute("aria-label");
      console.log(`Clicking module: ${moduleLabel}`);

      await secondModule.click();
      await page.waitForTimeout(400); // Wait for expand animation

      // Verify sidebar is now expanded
      await expect(sidebar).not.toHaveClass(/collapsed/);

      // Check which modules are expanded
      const expandedModules = page.locator(".module-button.expanded");
      const expandedCount = await expandedModules.count();

      console.log(`Expanded modules after click: ${expandedCount}`);

      // Get all module labels to see which ones are expanded
      for (let i = 0; i < expandedCount; i++) {
        const label = await expandedModules.nth(i).getAttribute("aria-label");
        const ariaExpanded = await expandedModules.nth(i).getAttribute("aria-expanded");
        console.log(`  - ${label} (aria-expanded: ${ariaExpanded})`);
      }

      // EXPECTED: Only 1 module should be expanded (the one we clicked)
      expect(expandedCount).toBe(1);

      // Verify it's the module we clicked
      const expandedModule = expandedModules.first();
      const expandedLabel = await expandedModule.getAttribute("aria-label");
      expect(expandedLabel).toBe(moduleLabel);

      // Verify the clicked module shows its sections
      const sectionsVisible = await page.locator(".sections-list").isVisible();
      expect(sectionsVisible).toBe(true);
    } else {
      console.log("⚠️ Not enough modules to test");
    }
  });

  test("verify expandedModules state using page evaluation", async ({ page }) => {
    // Set desktop viewport
    await page.setViewportSize(DESKTOP_SIZE);
    await page.goto("/");

    // Wait for sidebar
    await expect(page.locator(".desktop-navigation-sidebar")).toBeVisible({
      timeout: 10000,
    });
    await page.waitForTimeout(1000);

    // Get current module from page state
    const initialState = await page.evaluate(() => {
      const sidebar = document.querySelector(".desktop-navigation-sidebar");
      const moduleButtons = sidebar?.querySelectorAll(".module-button");

      const expandedModules: string[] = [];
      moduleButtons?.forEach((btn) => {
        if (btn.classList.contains("expanded")) {
          expandedModules.push(btn.getAttribute("aria-label") || "unknown");
        }
      });

      return {
        expandedModules,
        isCollapsed: sidebar?.classList.contains("collapsed"),
      };
    });

    console.log("Initial state:", initialState);

    // Collapse sidebar
    await page.locator(".collapse-toggle").click();
    await page.waitForTimeout(300);

    // Get module count
    const moduleCount = await page.locator(".module-button").count();
    console.log(`Total modules: ${moduleCount}`);

    if (moduleCount > 1) {
      // Click second module
      const secondModuleLabel = await page
        .locator(".module-button")
        .nth(1)
        .getAttribute("aria-label");

      console.log(`Clicking: ${secondModuleLabel}`);
      await page.locator(".module-button").nth(1).click();
      await page.waitForTimeout(400);

      // Check final state
      const finalState = await page.evaluate(() => {
        const sidebar = document.querySelector(".desktop-navigation-sidebar");
        const moduleButtons = sidebar?.querySelectorAll(".module-button");

        const expandedModules: string[] = [];
        moduleButtons?.forEach((btn) => {
          if (btn.classList.contains("expanded")) {
            expandedModules.push(btn.getAttribute("aria-label") || "unknown");
          }
        });

        return {
          expandedModules,
          expandedCount: expandedModules.length,
          isCollapsed: sidebar?.classList.contains("collapsed"),
        };
      });

      console.log("Final state:", finalState);

      // EXPECTED: sidebar is expanded, only 1 module expanded
      expect(finalState.isCollapsed).toBe(false);
      expect(finalState.expandedCount).toBe(1);
      expect(finalState.expandedModules[0]).toBe(secondModuleLabel);
    }
  });

  test("verify multiple collapse/expand cycles", async ({ page }) => {
    await page.setViewportSize(DESKTOP_SIZE);
    await page.goto("/");

    await expect(page.locator(".desktop-navigation-sidebar")).toBeVisible({
      timeout: 10000,
    });
    await page.waitForTimeout(1000);

    const moduleCount = await page.locator(".module-button").count();

    if (moduleCount < 2) {
      console.log("⚠️ Not enough modules for this test");
      return;
    }

    // Test 3 cycles
    for (let cycle = 1; cycle <= 3; cycle++) {
      console.log(`\n=== Cycle ${cycle} ===`);

      // Collapse
      await page.locator(".collapse-toggle").click();
      await page.waitForTimeout(300);

      // Click a module (alternate between first and second)
      const moduleIndex = cycle % 2;
      const moduleLabel = await page
        .locator(".module-button")
        .nth(moduleIndex)
        .getAttribute("aria-label");

      console.log(`  Clicking: ${moduleLabel}`);
      await page.locator(".module-button").nth(moduleIndex).click();
      await page.waitForTimeout(400);

      // Check result
      const state = await page.evaluate(() => {
        const expandedButtons = document.querySelectorAll(".module-button.expanded");
        return {
          expandedCount: expandedButtons.length,
          expandedLabels: Array.from(expandedButtons).map(
            (btn) => btn.getAttribute("aria-label") || "unknown"
          ),
        };
      });

      console.log(`  Result: ${state.expandedCount} expanded`);
      console.log(`  Expanded: ${state.expandedLabels.join(", ")}`);

      expect(state.expandedCount).toBe(1);
      expect(state.expandedLabels[0]).toBe(moduleLabel);
    }
  });
});
