import { Page, Locator } from "@playwright/test";

/**
 * Page object for Pictograph components
 *
 * Encapsulates selectors and actions for interacting with Pictograph
 * components throughout the application.
 */
export class PictographPage {
  readonly page: Page;

  // Pictograph elements
  readonly pictographWrapper: Locator;
  readonly grid: Locator;
  readonly props: Locator;
  readonly arrows: Locator;

  constructor(page: Page) {
    this.page = page;

    // Based on our exploration of the DOM structure
    this.pictographWrapper = page.locator(".pictograph-wrapper");
    this.grid = page.locator(".tka-glyph"); // The grid appears to be part of the tka-glyph
    this.props = page.locator(".tka-dot"); // Props appear to be represented by tka-dot elements
    this.arrows = page.locator(".tka-dash"); // Arrows appear to be represented by tka-dash elements
  }

  /**
   * Wait for a pictograph to be fully loaded in the specified tab
   * @param tabName - The name of the tab containing the pictograph
   * @param timeout - Optional timeout in milliseconds (default: 10000)
   */
  async waitForPictographLoaded(tabName = "construct", timeout = 10000) {
    // First wait for the tab to be visible
    await this.page
      .locator(`.${tabName}-tab`)
      .waitFor({ state: "visible", timeout });

    // Then look for pictograph elements within this tab using multiple possible selectors
    try {
      // Try the primary selector first
      const tabPictograph = this.page
        .locator(`.${tabName}-tab .pictograph-wrapper`)
        .first();
      await tabPictograph.waitFor({ state: "visible", timeout });
    } catch (e) {
      console.log(
        `Could not find pictograph with primary selector in ${tabName} tab, trying alternatives`,
      );

      // Try alternative selectors
      const alternativeSelectors = [
        `.${tabName}-tab .tka-glyph`,
        `.${tabName}-tab .pictograph`,
        `.${tabName}-tab .svg-container`,
      ];

      let found = false;
      for (const selector of alternativeSelectors) {
        const count = await this.page.locator(selector).count();
        if (count > 0) {
          console.log(`Found pictograph with selector: ${selector}`);
          await this.page
            .locator(selector)
            .first()
            .waitFor({ state: "visible", timeout });
          found = true;
          break;
        }
      }

      if (!found) {
        console.log(
          `Could not find pictograph in ${tabName} tab with any selector`,
        );
        // Take a screenshot to debug
        await this.page.screenshot({
          path: `test-results/pictograph-not-found-${tabName}.png`,
        });
      }
    }

    // Check if there's a grid component using multiple possible selectors
    try {
      const gridSelectors = [
        `.${tabName}-tab .grid-component`,
        `.${tabName}-tab .tka-grid`,
        `.${tabName}-tab .grid-svg`,
      ];

      for (const selector of gridSelectors) {
        const gridCount = await this.page.locator(selector).count();
        if (gridCount > 0) {
          const tabGrid = this.page.locator(selector).first();
          await tabGrid.waitFor({ state: "visible", timeout });
          console.log(`Found grid with selector: ${selector}`);
          break;
        }
      }
    } catch (e) {
      console.log(`Error waiting for grid in ${tabName} tab:`, e);
    }

    // Wait a moment for any animations to complete
    await this.page.waitForTimeout(500);
  }

  /**
   * Get the letter attribute of the pictograph
   */
  async getPictographLetter() {
    return await this.pictographWrapper.getAttribute("data-letter");
  }

  /**
   * Get the grid mode of the pictograph
   */
  async getGridMode() {
    return await this.grid.getAttribute("data-grid-mode");
  }

  /**
   * Check if the pictograph has props
   */
  async hasProps() {
    const propsCount = await this.props.count();
    return propsCount > 0;
  }

  /**
   * Check if the pictograph has arrows
   */
  async hasArrows() {
    const arrowsCount = await this.arrows.count();
    return arrowsCount > 0;
  }

  /**
   * Take a screenshot of the pictograph for visual testing
   */
  async takeScreenshot(name: string) {
    await this.pictographWrapper.screenshot({
      path: `./test-results/pictograph-${name}.png`,
    });
  }

  /**
   * Get the SVG content of the pictograph for comparison
   */
  async getSvgContent() {
    const svg = this.pictographWrapper.locator("svg").first();
    return await svg.evaluate((el) => el.outerHTML);
  }

  /**
   * Click on a specific point in the grid
   */
  async clickGridPoint(pointName: string) {
    const gridPoint = this.grid.locator(`[data-point-name="${pointName}"]`);
    await gridPoint.click();
  }
}
