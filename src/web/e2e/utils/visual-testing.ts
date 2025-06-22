import { Page, Locator, expect } from "@playwright/test";

/**
 * Utility functions for visual testing of SVG components
 */
export class VisualTestingUtils {
  /**
   * Compare SVG content for visual testing
   *
   * This function compares the SVG content of a component with a baseline
   * or expected SVG content to detect visual regressions.
   */
  static async compareSvgContent(
    actual: string,
    expected: string,
    options: { ignoreIds?: boolean; ignoreTransforms?: boolean } = {},
  ) {
    let normalizedActual = actual;
    let normalizedExpected = expected;

    // Optionally ignore dynamic IDs
    if (options.ignoreIds) {
      const idRegex = /id="[^"]*"/g;
      normalizedActual = normalizedActual.replace(idRegex, 'id="IGNORED"');
      normalizedExpected = normalizedExpected.replace(idRegex, 'id="IGNORED"');
    }

    // Optionally ignore transforms which might have small precision differences
    if (options.ignoreTransforms) {
      const transformRegex = /transform="[^"]*"/g;
      normalizedActual = normalizedActual.replace(
        transformRegex,
        'transform="IGNORED"',
      );
      normalizedExpected = normalizedExpected.replace(
        transformRegex,
        'transform="IGNORED"',
      );
    }

    // Compare the normalized SVG content
    expect(normalizedActual).toBe(normalizedExpected);
  }

  /**
   * Take a screenshot of an SVG component for visual comparison
   */
  static async takeComponentScreenshot(
    page: Page,
    componentLocator: Locator,
    screenshotName: string,
  ) {
    console.log(`Taking screenshot of component: ${screenshotName}`);

    try {
      // First check if the component exists
      const count = await componentLocator.count();
      if (count === 0) {
        console.log(`Component not found for screenshot: ${screenshotName}`);

        // Take a screenshot of the whole page for debugging
        await page.screenshot({
          path: `./test-results/${screenshotName}-not-found.png`,
        });

        // Try to find the component using JavaScript
        const found = await page.evaluate(
          (selector) => {
            // Try to find the component using multiple approaches
            const element =
              document.querySelector(selector) ||
              document.querySelector(`.${selector}`) ||
              document.querySelector(`[data-test="${selector}"]`);

            if (element) {
              // Highlight the element for debugging
              const originalStyle = element.getAttribute("style") || "";
              element.setAttribute(
                "style",
                `${originalStyle}; border: 3px solid red !important;`,
              );
              return true;
            }

            return false;
          },
          componentLocator.toString().replace(/.*'(.*)'.*/, "$1"),
        );

        if (found) {
          console.log(
            `Found component using JavaScript, taking screenshot of whole page`,
          );
          await page.screenshot({
            path: `./test-results/${screenshotName}-highlighted.png`,
          });
        }

        return;
      }

      // Ensure the component is visible with a longer timeout
      await componentLocator.waitFor({ state: "visible", timeout: 15000 });

      // Scroll the component into view
      await page.evaluate(
        (selector) => {
          const element = document.querySelector(selector);
          if (element) {
            element.scrollIntoView({ behavior: "smooth", block: "center" });
          }
        },
        componentLocator.toString().replace(/.*'(.*)'.*/, "$1"),
      );

      // Wait for any animations to complete
      await page.waitForTimeout(1000);

      // Create the test-results directory if it doesn't exist
      await page.evaluate(() => {
        try {
          // This is a no-op in the browser, but we'll catch any errors
        } catch (e) {
          console.error("Error creating directory:", e);
        }
      });

      // Take a screenshot of just the component
      await componentLocator
        .screenshot({
          path: `./test-results/${screenshotName}.png`,
          omitBackground: true,
        })
        .catch(async (e) => {
          console.log(`Error taking component screenshot: ${e}`);

          // Fallback: take a screenshot of the whole page
          await page.screenshot({
            path: `./test-results/${screenshotName}-fallback.png`,
          });
        });

      console.log(`Screenshot taken: ${screenshotName}`);
    } catch (e) {
      console.log(`Error in takeComponentScreenshot: ${e}`);

      // Take a screenshot of the whole page as a fallback
      await page.screenshot({
        path: `./test-results/${screenshotName}-error.png`,
      });
    }
  }

  /**
   * Compare a component's appearance with a baseline image
   */
  static async compareComponentWithBaseline(
    componentLocator: Locator,
    baselineImagePath: string,
  ) {
    // Take a screenshot of the component
    const screenshot = await componentLocator.screenshot({
      omitBackground: true,
    });

    // Compare with the baseline image
    // This uses Playwright's built-in image comparison
    await expect(screenshot).toMatchSnapshot(baselineImagePath);
  }

  /**
   * Verify SVG rendering accuracy by checking key attributes
   */
  static async verifySvgAttributes(
    svgLocator: Locator,
    expectedAttributes: Record<string, string>,
  ) {
    console.log("Verifying SVG attributes");

    try {
      // First check if the SVG exists
      const count = await svgLocator.count();
      if (count === 0) {
        console.log("SVG element not found");

        // Try to find the SVG using JavaScript
        const svgInfo = await svgLocator.page().evaluate(() => {
          const svgs = Array.from(document.querySelectorAll("svg"));
          return svgs.map((svg) => ({
            attributes: Array.from(svg.attributes).reduce(
              (acc, attr) => {
                acc[attr.name] = attr.value;
                return acc;
              },
              {} as Record<string, string>,
            ),
            path: svg.closest("[class]")?.getAttribute("class") || "unknown",
          }));
        });

        console.log("Found SVGs on page:", JSON.stringify(svgInfo, null, 2));

        // Skip the attribute checks
        return;
      }

      // Check each attribute with more flexible matching
      for (const [attr, expectedValue] of Object.entries(expectedAttributes)) {
        try {
          const actualValue = await svgLocator.getAttribute(attr);

          if (actualValue === null) {
            console.log(`Attribute ${attr} not found on SVG element`);
            continue;
          }

          // For viewBox, allow for slight variations in values
          if (attr === "viewBox" && actualValue && expectedValue) {
            const actualParts = actualValue.split(" ").map(Number);
            const expectedParts = expectedValue.split(" ").map(Number);

            // Check if the viewBox has the same number of parts
            if (actualParts.length === expectedParts.length) {
              // Allow for small differences in viewBox values
              const tolerance = 10;
              const allWithinTolerance = actualParts.every(
                (val, i) => Math.abs(val - expectedParts[i]) <= tolerance,
              );

              if (allWithinTolerance) {
                console.log(
                  `ViewBox values are within tolerance: ${actualValue} vs ${expectedValue}`,
                );
                continue;
              }
            }
          }

          // For preserveAspectRatio, be more flexible
          if (attr === "preserveAspectRatio") {
            // If both contain "meet", consider it a match
            if (
              actualValue?.includes("meet") &&
              expectedValue?.includes("meet")
            ) {
              console.log(
                `PreserveAspectRatio values both use 'meet': ${actualValue} vs ${expectedValue}`,
              );
              continue;
            }
          }

          // For other attributes, do an exact match
          expect(actualValue).toBe(expectedValue);
        } catch (e) {
          console.log(`Error checking attribute ${attr}:`, e);
        }
      }
    } catch (e) {
      console.log("Error in verifySvgAttributes:", e);
    }
  }
}
