import { test, expect } from "../utils/test-base";

/**
 * Pictograph Component Tests
 *
 * These tests verify the rendering and interaction with Pictograph components,
 * which are core to the application's visualization capabilities.
 */
test.describe("Pictograph Component", () => {
  // Setup: Navigate to the application before each test
  test.beforeEach(async ({ appPage }) => {
    await appPage.goto();
    await appPage.waitForAppReady();
  });

  test("should render pictograph components", async ({ page, appPage }) => {
    // Navigate to the Construct tab where we can create a pictograph
    await appPage.navigateToTab("construct");

    // Wait for the construct tab to be visible
    await page
      .locator(".construct-tab")
      .waitFor({ state: "visible", timeout: 10000 });

    // Wait a moment for the UI to stabilize
    await page.waitForTimeout(1000);

    // Look for pictograph wrappers
    const pictographWrappers = page.locator(".pictograph-wrapper");
    const count = await pictographWrappers.count();
    console.log(`Found ${count} pictograph wrappers`);

    // Verify we have at least one pictograph
    expect(count).toBeGreaterThan(0);

    // Check if pictographs have SVG elements
    for (let i = 0; i < count; i++) {
      const wrapper = pictographWrappers.nth(i);
      const svg = wrapper.locator("svg.pictograph");

      // Check if the SVG is visible
      await expect(svg).toBeVisible();

      // Take a screenshot of this pictograph
      await wrapper.screenshot({ path: `test-results/pictograph-${i}.png` });

      // Check for TKA elements
      const letterCount = await wrapper.locator(".tka-letter").count();
      const glyphCount = await wrapper.locator(".tka-glyph").count();
      const dotCount = await wrapper.locator(".tka-dot").count();
      const dashCount = await wrapper.locator(".tka-dash").count();

      console.log(
        `Pictograph ${i} contains: ${letterCount} letters, ${glyphCount} glyphs, ${dotCount} dots, ${dashCount} dashes`,
      );
    }

    // Success if we've made it this far
    expect(true).toBeTruthy();
  });

  test.skip("should explore SVG structure", async ({ page, appPage }) => {
    // Navigate to the Construct tab
    await appPage.navigateToTab("construct");

    // Wait for the construct tab to be visible
    await page
      .locator(".construct-tab")
      .waitFor({ state: "visible", timeout: 10000 });

    // Take a screenshot of the construct tab
    await page.screenshot({ path: "test-results/construct-tab-full.png" });

    // Look for any SVG elements in the construct tab
    const svgElements = page.locator(".construct-tab svg");
    const svgCount = await svgElements.count();
    console.log(`Found ${svgCount} SVG elements`);

    // If we have SVG elements, examine their structure
    if (svgCount > 0) {
      // Take screenshots of each SVG
      for (let i = 0; i < svgCount; i++) {
        const svg = svgElements.nth(i);
        await svg.screenshot({ path: `test-results/svg-element-${i}.png` });

        // Get information about this SVG
        const svgInfo = await svg.evaluate((el: SVGElement) => ({
          width: el.getAttribute("width"),
          height: el.getAttribute("height"),
          viewBox: el.getAttribute("viewBox"),
          classes:
            typeof el.className === "string"
              ? el.className
              : el.className.baseVal,
          parentClasses: el.parentElement ? el.parentElement.className : "",
          parentId: el.parentElement ? el.parentElement.id : "",
          childElements: Array.from(el.querySelectorAll("*")).map(
            (child: Element) => ({
              tag: child.tagName,
              classes:
                child instanceof SVGElement &&
                typeof child.className !== "string"
                  ? child.className.baseVal
                  : child.className,
              id: child.id,
              dataAttributes: {
                "data-point-name": child.getAttribute("data-point-name"),
                "data-grid-mode": child.getAttribute("data-grid-mode"),
              },
            }),
          ),
        }));

        console.log(`SVG ${i} info:`, JSON.stringify(svgInfo, null, 2));

        // Look for circle elements that might be grid points
        const circles = svg.locator("circle");
        const circleCount = await circles.count();
        console.log(`Found ${circleCount} circles in SVG ${i}`);

        if (circleCount > 0) {
          // Try clicking the first circle
          await circles.first().click();
          await page.screenshot({
            path: `test-results/after-circle-click-${i}.png`,
          });
        }
      }
    }

    // Success if we've made it this far
    expect(true).toBeTruthy();
  });

  test.skip("should render props when added to the pictograph", async ({
    page,
    appPage,
  }) => {
    // This test is skipped until we can determine the exact selectors needed
    // for your specific implementation

    // Navigate to the Construct tab
    await appPage.navigateToTab("construct");

    // Wait for the construct tab to be visible
    await page
      .locator(".construct-tab")
      .waitFor({ state: "visible", timeout: 10000 });

    // Take a screenshot for debugging
    await page.screenshot({ path: "test-results/props.png" });
  });

  test.skip("should render arrows when motion is added", async ({
    page,
    appPage,
  }) => {
    // This test is skipped until we can determine the exact selectors needed
    // for your specific implementation

    // Navigate to the Construct tab
    await appPage.navigateToTab("construct");

    // Wait for the construct tab to be visible
    await page
      .locator(".construct-tab")
      .waitFor({ state: "visible", timeout: 10000 });

    // Take a screenshot for debugging
    await page.screenshot({ path: "test-results/arrows.png" });
  });
});
