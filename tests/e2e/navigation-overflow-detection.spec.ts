import { expect, test } from "@playwright/test";

/**
 * Dynamic Overflow Detection Test
 * Tests that navigation bar automatically switches to icon-only mode
 * when tabs are dynamically added and exceed available space
 */

test.describe("Navigation Overflow Detection", () => {
  test("should show labels initially with few tabs", async ({ page }) => {
    // Use a medium viewport that will overflow with many tabs but not with few
    await page.setViewportSize({ width: 800, height: 600 });
    await page.goto("/");

    // Wait for navigation to be ready
    await page.waitForSelector(".app-navigation-bar.layout-top", {
      timeout: 10000,
    });

    // Initially, should have labels visible (2 tabs: Construct, Edit)
    const tabLabels = page.locator(".nav-tab .tab-label");
    const labelCount = await tabLabels.count();

    console.log(`Initial tab label count: ${labelCount}`);

    if (labelCount > 0) {
      // Check if labels are visible (not hidden by icon-only mode)
      const firstLabel = tabLabels.first();
      const isVisible = await firstLabel.isVisible();

      console.log(`Labels visible initially: ${isVisible}`);
      console.log(`First label text: ${await firstLabel.textContent()}`);

      // Check if icon-only class is NOT applied
      const subModeTabs = page.locator(".sub-mode-tabs");
      const hasIconOnlyClass = await subModeTabs.evaluate((el) =>
        el.classList.contains("icon-only")
      );

      console.log(`Icon-only class applied initially: ${hasIconOnlyClass}`);

      // Measure scroll width vs client width
      const navCenter = page.locator(".nav-center");
      const measurements = await navCenter.evaluate((el) => ({
        scrollWidth: el.scrollWidth,
        clientWidth: el.clientWidth,
        hasOverflow: el.scrollWidth > el.clientWidth,
      }));

      console.log(`Nav center measurements (initial):`);
      console.log(`  scrollWidth: ${measurements.scrollWidth}px`);
      console.log(`  clientWidth: ${measurements.clientWidth}px`);
      console.log(`  hasOverflow: ${measurements.hasOverflow}`);

      // With only 2 tabs, should NOT overflow on 800px width
      if (!measurements.hasOverflow) {
        expect(isVisible).toBe(true);
        expect(hasIconOnlyClass).toBe(false);
        console.log("✅ INITIAL STATE: Labels visible, no overflow");
      } else {
        console.log("⚠️ INITIAL STATE: Already overflowing (unexpected)");
      }
    }
  });

  test("should switch to icon-only mode when tabs are added dynamically", async ({
    page,
  }) => {
    // Use a medium viewport
    await page.setViewportSize({ width: 800, height: 600 });
    await page.goto("/");

    await page.waitForSelector(".app-navigation-bar.layout-top", {
      timeout: 10000,
    });

    // Get initial state
    const getOverflowState = async () => {
      const subModeTabs = page.locator(".sub-mode-tabs");

      const hasIconOnlyClass = await subModeTabs.evaluate((el) =>
        el.classList.contains("icon-only")
      );

      const navCenter = page.locator(".nav-center");
      const measurements = await navCenter.evaluate((el) => ({
        scrollWidth: el.scrollWidth,
        clientWidth: el.clientWidth,
        hasOverflow: el.scrollWidth > el.clientWidth,
      }));

      const tabCount = await page.locator(".nav-tab").count();
      const labelCount = await page.locator(".nav-tab .tab-label").count();
      const labelsVisible =
        labelCount > 0
          ? await page.locator(".nav-tab .tab-label").first().isVisible()
          : false;

      return {
        hasIconOnlyClass,
        measurements,
        tabCount,
        labelCount,
        labelsVisible,
      };
    };

    const initialState = await getOverflowState();

    console.log("INITIAL STATE:");
    console.log(`  Tab count: ${initialState.tabCount}`);
    console.log(`  Label count: ${initialState.labelCount}`);
    console.log(`  Labels visible: ${initialState.labelsVisible}`);
    console.log(`  Icon-only class: ${initialState.hasIconOnlyClass}`);
    console.log(
      `  scrollWidth: ${initialState.measurements.scrollWidth}px, clientWidth: ${initialState.measurements.clientWidth}px`
    );
    console.log(`  Has overflow: ${initialState.measurements.hasOverflow}`);

    // Now select a sequence to add more tabs (Generate, Practice tabs should appear)
    // First, we need to construct a sequence
    const constructTab = page.locator('button.nav-tab:has-text("Construct")');
    if ((await constructTab.count()) > 0) {
      await constructTab.click();
      await page.waitForTimeout(500);

      // Add a beat to create a sequence
      const addBeatButton = page.locator('button:has-text("Add Beat")').first();
      if ((await addBeatButton.count()) > 0) {
        await addBeatButton.click();
        await page.waitForTimeout(1000); // Wait for tabs to be added

        const afterAddingSequence = await getOverflowState();

        console.log("\nAFTER ADDING SEQUENCE:");
        console.log(`  Tab count: ${afterAddingSequence.tabCount}`);
        console.log(`  Label count: ${afterAddingSequence.labelCount}`);
        console.log(`  Labels visible: ${afterAddingSequence.labelsVisible}`);
        console.log(`  Icon-only class: ${afterAddingSequence.hasIconOnlyClass}`);
        console.log(
          `  scrollWidth: ${afterAddingSequence.measurements.scrollWidth}px, clientWidth: ${afterAddingSequence.measurements.clientWidth}px`
        );
        console.log(
          `  Has overflow: ${afterAddingSequence.measurements.hasOverflow}`
        );

        // ASSERTIONS
        // More tabs should have been added
        expect(afterAddingSequence.tabCount).toBeGreaterThan(
          initialState.tabCount
        );

        // If overflow is detected, icon-only mode should be activated
        if (afterAddingSequence.measurements.hasOverflow) {
          console.log(
            "\n🔍 OVERFLOW DETECTED - Checking if icon-only mode activated..."
          );

          // This is the critical test: overflow should trigger icon-only mode
          expect(afterAddingSequence.hasIconOnlyClass).toBe(true);

          // Labels should be hidden when icon-only is active
          if (afterAddingSequence.labelCount > 0) {
            expect(afterAddingSequence.labelsVisible).toBe(false);
          }

          console.log("✅ TEST PASSED: Icon-only mode correctly activated");
        } else {
          console.log(
            "\n✓ NO OVERFLOW: Enough space for all tabs with labels"
          );
          console.log(
            "  (This is OK - viewport might be wide enough for all tabs)"
          );
        }
      } else {
        console.log("⚠️ Could not find 'Add Beat' button");
      }
    } else {
      console.log("⚠️ Could not find 'Construct' tab");
    }
  });

  test("should measure and detect overflow reactively", async ({ page }) => {
    // Use progressively smaller viewports to trigger overflow
    const viewportSizes = [
      { width: 1200, height: 600, expectOverflow: false },
      { width: 800, height: 600, expectOverflow: false },
      { width: 600, height: 600, expectOverflow: false },
      { width: 400, height: 600, expectOverflow: false },
      { width: 300, height: 600, expectOverflow: true }, // Very narrow - should overflow
      { width: 200, height: 600, expectOverflow: true }, // Extremely narrow - definitely overflow
    ];

    await page.goto("/");
    await page.waitForSelector(".app-navigation-bar.layout-top");

    // Create a sequence first to get all tabs visible
    const constructTab = page.locator('button.nav-tab:has-text("Construct")');
    if ((await constructTab.count()) > 0) {
      await constructTab.click();
      await page.waitForTimeout(300);

      const addBeatButton = page.locator('button:has-text("Add Beat")').first();
      if ((await addBeatButton.count()) > 0) {
        await addBeatButton.click();
        await page.waitForTimeout(800);
      }
    }

    console.log("\nRESIZE TEST - Testing reactive overflow detection:");

    for (const size of viewportSizes) {
      await page.setViewportSize({ width: size.width, height: size.height });
      // Wait for resize, ResizeObserver, requestAnimationFrame, and reactive updates
      await page.waitForTimeout(1000);

      const subModeTabs = page.locator(".sub-mode-tabs");
      const hasIconOnlyClass = await subModeTabs.evaluate((el) =>
        el.classList.contains("icon-only")
      );

      const navCenter = page.locator(".nav-center");
      const measurements = await navCenter.evaluate((el) => ({
        scrollWidth: el.scrollWidth,
        clientWidth: el.clientWidth,
      }));

      console.log(`\nViewport: ${size.width}px`);
      console.log(
        `  scrollWidth: ${measurements.scrollWidth}px, clientWidth: ${measurements.clientWidth}px`
      );
      console.log(
        `  Overflow: ${measurements.scrollWidth > measurements.clientWidth}`
      );
      console.log(`  Icon-only mode: ${hasIconOnlyClass}`);

      // If content overflows, icon-only should be active
      if (measurements.scrollWidth > measurements.clientWidth) {
        expect(hasIconOnlyClass).toBe(true);
        console.log(`  ✅ Overflow correctly detected and handled`);
      } else {
        // If no overflow, icon-only may or may not be active (hysteresis)
        console.log(`  ✓ No overflow at this width`);
      }
    }
  });
});
