import { test as base } from "@playwright/test";
import { AppPage } from "../fixtures/app-page";
import { PictographPage } from "../fixtures/pictograph-page";
import { GenerateTabPage } from "../fixtures/generate-tab-page";
import { WriteTabPage } from "../fixtures/write-tab-page";

/**
 * Extended test fixture with custom page objects for The Kinetic Constructor
 *
 * This provides strongly-typed access to page objects that encapsulate
 * application-specific functionality and selectors.
 */
export const test = base.extend<{
  appPage: AppPage;
  pictographPage: PictographPage;
  generateTabPage: GenerateTabPage;
  writeTabPage: WriteTabPage;
}>({
  // Define the app page fixture
  appPage: async ({ page }, use) => {
    const appPage = new AppPage(page);
    await use(appPage);
  },

  // Define the pictograph page fixture
  pictographPage: async ({ page }, use) => {
    const pictographPage = new PictographPage(page);
    await use(pictographPage);
  },

  // Define the generate tab page fixture
  generateTabPage: async ({ page }, use) => {
    const generateTabPage = new GenerateTabPage(page);
    await use(generateTabPage);
  },

  // Define the write tab page fixture
  writeTabPage: async ({ page }, use) => {
    const writeTabPage = new WriteTabPage(page);
    await use(writeTabPage);
  },
});

// Re-export expect
export { expect } from "@playwright/test";
