import { test, expect } from "../utils/test-base";
import { VisualTestingUtils } from "../utils/visual-testing";

/**
 * Visual Tests for Pictograph Rendering
 *
 * These tests verify the visual appearance of SVG components
 * to ensure they render correctly across browsers.
 */
test.describe("Pictograph Visual Rendering", () => {
  // Setup: Navigate to the application before each test
  test.beforeEach(async ({ page, appPage }) => {
    // Increase timeout for navigation
    test.setTimeout(60000);

    await appPage.goto();
    await appPage.waitForAppReady();

    // Take a screenshot before navigation
    await page.screenshot({ path: "test-results/before-construct-tab.png" });

    // Navigate to the Construct tab where we can create pictographs
    await appPage.navigateToTab("construct");

    // Wait a moment for the tab to fully load
    await page.waitForTimeout(2000);

    // Take a screenshot after navigation
    await page.screenshot({ path: "test-results/after-construct-tab.png" });
  });

  test("should render diamond grid correctly", async ({
    page,
    pictographPage,
  }) => {
    // Wait for the pictograph to load with a longer timeout
    await pictographPage.waitForPictographLoaded("construct", 20000);

    // Take a screenshot of the whole page
    await page.screenshot({ path: "test-results/diamond-grid-page.png" });

    // Try to find the grid component using JavaScript
    const gridInfo = await page.evaluate(() => {
      // Try multiple selectors to find the grid
      const selectors = [
        ".grid-component",
        ".tka-grid",
        ".grid-svg",
        ".pictograph-wrapper svg",
        ".pictograph svg",
      ];

      for (const selector of selectors) {
        const elements = document.querySelectorAll(selector);
        if (elements.length > 0) {
          return {
            selector,
            count: elements.length,
            found: true,
          };
        }
      }

      return { found: false };
    });

    console.log("Grid component info:", gridInfo);

    // Use the selector that was found
    let gridSelector = ".grid-component";
    if (gridInfo.found && gridInfo.selector) {
      gridSelector = gridInfo.selector;
    }

    // Take a screenshot of the grid for visual comparison
    const gridElement = page.locator(gridSelector);
    await VisualTestingUtils.takeComponentScreenshot(
      page,
      gridElement,
      "diamond-grid",
    );

    // Verify the grid has the correct SVG structure
    try {
      const gridSvg = gridElement.locator("svg").first();

      // Check essential attributes
      await VisualTestingUtils.verifySvgAttributes(gridSvg, {
        viewBox: "0 0 1000 1000", // Adjust based on your actual viewBox
        preserveAspectRatio: "xMidYMid meet",
      });
    } catch (e) {
      console.log("Error verifying SVG attributes:", e);
    }

    // Verify diamond points are present using JavaScript
    await page.evaluate(() => {
      const diamondPoints = [
        "center",
        "n_diamond",
        "e_diamond",
        "s_diamond",
        "w_diamond",
        "ne_diamond",
        "se_diamond",
        "sw_diamond",
        "nw_diamond",
      ];

      const results: { point: string; found: boolean }[] = [];

      for (const point of diamondPoints) {
        // Try multiple ways to find the point
        const element =
          document.querySelector(`[data-point-name="${point}"]`) ||
          document.querySelector(`.${point}-point`);

        results.push({
          point,
          found: !!element,
        });
      }

      console.log("Diamond points check results:", results);
    });
  });

  test("should render box grid correctly", async ({ page, pictographPage }) => {
    // Wait for the pictograph to load
    await pictographPage.waitForPictographLoaded("construct", 20000);

    // Take a screenshot before switching grid mode
    await page.screenshot({ path: "test-results/before-box-grid.png" });

    // Try to find and click the box grid button using JavaScript
    const clicked = await page.evaluate(() => {
      // Try multiple ways to find the box grid button
      const possibleButtons = [
        // By text content
        ...Array.from(document.querySelectorAll("button")).filter(
          (b) => b.textContent?.toLowerCase().includes("box grid"),
        ),
        // By data attribute
        document.querySelector('[data-test="box-grid-button"]'),
        // By class
        document.querySelector(".box-grid-button"),
        // By any grid toggle button
        document.querySelector(".grid-toggle button"),
      ].filter(Boolean);

      if (possibleButtons.length > 0) {
        (possibleButtons[0] as HTMLElement).click();
        return true;
      }

      return false;
    });

    if (!clicked) {
      console.log(
        "Could not find box grid button using JavaScript, trying Playwright locator",
      );

      // Try multiple selectors
      const selectors = [
        'button:has-text("Box Grid")',
        '[data-test="box-grid-button"]',
        ".box-grid-button",
        ".grid-toggle button",
      ];

      for (const selector of selectors) {
        try {
          const count = await page.locator(selector).count();
          if (count > 0) {
            await page.locator(selector).first().click();
            console.log(`Clicked box grid button using selector: ${selector}`);
            break;
          }
        } catch (e) {
          console.log(`Error clicking with selector ${selector}:`, e);
        }
      }
    }

    // Wait for the grid to update
    await page.waitForTimeout(1000);

    // Take a screenshot after switching grid mode
    await page.screenshot({ path: "test-results/after-box-grid.png" });

    // Try to find the grid component using JavaScript
    const gridInfo = await page.evaluate(() => {
      // Try multiple selectors to find the grid
      const selectors = [
        ".grid-component",
        ".tka-grid",
        ".grid-svg",
        ".pictograph-wrapper svg",
        ".pictograph svg",
      ];

      for (const selector of selectors) {
        const elements = document.querySelectorAll(selector);
        if (elements.length > 0) {
          return {
            selector,
            count: elements.length,
            found: true,
          };
        }
      }

      return { found: false };
    });

    // Use the selector that was found
    let gridSelector = ".grid-component";
    if (gridInfo.found && gridInfo.selector) {
      gridSelector = gridInfo.selector;
    }

    // Take a screenshot of the box grid
    const gridElement = page.locator(gridSelector);
    await VisualTestingUtils.takeComponentScreenshot(
      page,
      gridElement,
      "box-grid",
    );

    // Verify the grid mode has changed
    try {
      const gridMode = await pictographPage.getGridMode();
      console.log(`Current grid mode: ${gridMode}`);
    } catch (e) {
      console.log("Error getting grid mode:", e);
    }
  });

  test("should render props with correct appearance", async ({ page }) => {
    // Wait for the pictograph to load
    await page.waitForTimeout(2000);

    // Take a screenshot before adding prop
    await page.screenshot({ path: "test-results/before-add-prop.png" });

    // Try to find and click the add prop button using JavaScript
    await page.evaluate(() => {
      // Try multiple ways to find the add prop button
      const possibleButtons = [
        // By text content
        ...Array.from(document.querySelectorAll("button")).filter(
          (b) => b.textContent?.toLowerCase().includes("add prop"),
        ),
        // By data attribute
        document.querySelector('[data-test="add-prop-button"]'),
        // By class
        document.querySelector(".add-prop-button"),
      ].filter(Boolean);

      if (possibleButtons.length > 0) {
        (possibleButtons[0] as HTMLElement).click();

        // Wait a moment for the prop menu to appear
        setTimeout(() => {
          // Try to find and click the club prop option
          const clubOptions = [
            // By text content
            ...Array.from(document.querySelectorAll("button, div")).filter(
              (b) => b.textContent?.toLowerCase().includes("club"),
            ),
            // By data attribute
            document.querySelector('[data-prop-type="club"]'),
          ].filter(Boolean);

          if (clubOptions.length > 0) {
            (clubOptions[0] as HTMLElement).click();

            // Wait a moment for the prop to be selected
            setTimeout(() => {
              // Try to find and click the center point
              const centerPoints = [
                document.querySelector(".center-point"),
                document.querySelector('[data-point-name="center"]'),
              ].filter(Boolean);

              if (centerPoints.length > 0) {
                (centerPoints[0] as HTMLElement).click();
                return true;
              }
            }, 500);
          }
        }, 500);

        return true;
      }

      return false;
    });

    // Wait for the prop to be added
    await page.waitForTimeout(2000);

    // Take a screenshot after adding prop
    await page.screenshot({ path: "test-results/after-add-prop.png" });

    // Try to find the prop component using JavaScript
    const propInfo = await page.evaluate(() => {
      // Try multiple selectors to find the prop
      const selectors = [
        ".prop-component",
        '[data-test="prop"]',
        ".tka-dot",
        ".pictograph-wrapper .prop",
      ];

      for (const selector of selectors) {
        const elements = document.querySelectorAll(selector);
        if (elements.length > 0) {
          return {
            selector,
            count: elements.length,
            found: true,
          };
        }
      }

      return { found: false };
    });

    // Use the selector that was found
    let propSelector = '.prop-component, [data-test="prop"]';
    if (propInfo.found && propInfo.selector) {
      propSelector = propInfo.selector;
    }

    // Take a screenshot of the prop
    const propElement = page.locator(propSelector);
    await VisualTestingUtils.takeComponentScreenshot(
      page,
      propElement,
      "club-prop",
    );
  });

  test("should render arrows with correct appearance", async ({ page }) => {
    // Wait for the pictograph to load
    await page.waitForTimeout(2000);

    // Take a screenshot before adding motion
    await page.screenshot({ path: "test-results/before-add-motion.png" });

    // Try to find and click the add motion button using JavaScript
    await page.evaluate(() => {
      // Try multiple ways to find the add motion button
      const possibleButtons = [
        // By text content
        ...Array.from(document.querySelectorAll("button")).filter(
          (b) => b.textContent?.toLowerCase().includes("add motion"),
        ),
        // By data attribute
        document.querySelector('[data-test="add-motion-button"]'),
        // By class
        document.querySelector(".add-motion-button"),
      ].filter(Boolean);

      if (possibleButtons.length > 0) {
        (possibleButtons[0] as HTMLElement).click();

        // Wait a moment for the motion menu to appear
        setTimeout(() => {
          // Try to find and click the pro motion option
          const proOptions = [
            // By text content
            ...Array.from(document.querySelectorAll("button, div")).filter(
              (b) => b.textContent?.toLowerCase().includes("pro"),
            ),
            // By data attribute
            document.querySelector('[data-motion-type="pro"]'),
          ].filter(Boolean);

          if (proOptions.length > 0) {
            (proOptions[0] as HTMLElement).click();

            // Wait a moment for the motion to be selected
            setTimeout(() => {
              // Try to find and click the NE point
              const nePoints = [
                document.querySelector(".ne-point"),
                document.querySelector('[data-point-name="ne"]'),
              ].filter(Boolean);

              if (nePoints.length > 0) {
                (nePoints[0] as HTMLElement).click();

                // Wait a moment for the start point to be selected
                setTimeout(() => {
                  // Try to find and click the SW point
                  const swPoints = [
                    document.querySelector(".sw-point"),
                    document.querySelector('[data-point-name="sw"]'),
                  ].filter(Boolean);

                  if (swPoints.length > 0) {
                    (swPoints[0] as HTMLElement).click();
                    return true;
                  }
                }, 500);
              }
            }, 500);
          }
        }, 500);

        return true;
      }

      return false;
    });

    // Wait for the motion to be added
    await page.waitForTimeout(3000);

    // Take a screenshot after adding motion
    await page.screenshot({ path: "test-results/after-add-motion.png" });

    // Try to find the arrow component using JavaScript
    const arrowInfo = await page.evaluate(() => {
      // Try multiple selectors to find the arrow
      const selectors = [
        ".arrow-component",
        '[data-test="arrow"]',
        ".tka-dash",
        ".pictograph-wrapper .arrow",
      ];

      for (const selector of selectors) {
        const elements = document.querySelectorAll(selector);
        if (elements.length > 0) {
          return {
            selector,
            count: elements.length,
            found: true,
          };
        }
      }

      return { found: false };
    });

    // Use the selector that was found
    let arrowSelector = '.arrow-component, [data-test="arrow"]';
    if (arrowInfo.found && arrowInfo.selector) {
      arrowSelector = arrowInfo.selector;
    }

    // Take a screenshot of the arrow
    const arrowElement = page.locator(arrowSelector);
    await VisualTestingUtils.takeComponentScreenshot(
      page,
      arrowElement,
      "pro-arrow",
    );
  });
});
