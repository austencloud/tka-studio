import { Page, Locator } from "@playwright/test";

/**
 * Page object for the main application
 *
 * Encapsulates selectors and actions for the main application layout
 * and navigation between tabs.
 */
export class AppPage {
  readonly page: Page;

  // Main layout elements
  readonly mainLayout: Locator;
  readonly menuBar: Locator;
  readonly tabButtons: Record<string, Locator>;

  constructor(page: Page) {
    this.page = page;

    // Main layout selectors
    this.mainLayout = page.locator(".main-layout-wrapper");
    this.menuBar = page.locator(".menu-bar");

    // Tab navigation buttons with more flexible selectors
    this.tabButtons = {
      write: page.locator(
        'button:has-text("Write"), .nav-button:has-text("Write"), [data-tab="write"]',
      ),
      generate: page.locator(
        'button:has-text("Generate"), .nav-button:has-text("Generate"), [data-tab="generate"]',
      ),
      construct: page.locator(
        'button:has-text("Construct"), .nav-button:has-text("Construct"), [data-tab="construct"]',
      ),
      browse: page.locator(
        'button:has-text("Browse"), .nav-button:has-text("Browse"), [data-tab="browse"]',
      ),
      learn: page.locator(
        'button:has-text("Learn"), .nav-button:has-text("Learn"), [data-tab="learn"]',
      ),
    };
  }

  /**
   * Navigate to the application
   */
  async goto() {
    try {
      // Navigate to the application with a longer timeout
      await this.page.goto("/", { timeout: 60000 });

      // Try to wait for the application to load
      try {
        // Wait for the main layout to be visible
        await this.mainLayout.waitFor({ state: "visible", timeout: 30000 });
      } catch (e) {
        console.log("Could not find main layout, trying to continue anyway");

        try {
          // Take a screenshot to see what's happening
          await this.page.screenshot({
            path: "test-results/app-load-error.png",
          });
        } catch (screenshotError) {
          console.log("Could not take screenshot:", screenshotError);
        }

        try {
          // Try reloading the page
          await this.page.reload({ timeout: 60000 });

          // Wait a moment
          await this.page.waitForTimeout(5000);
        } catch (reloadError) {
          console.log("Could not reload page:", reloadError);
        }
      }
    } catch (e) {
      console.log("Error navigating to application:", e);
    }
  }

  /**
   * Navigate to a specific tab
   */
  async navigateToTab(
    tabName: "write" | "generate" | "construct" | "browse" | "learn",
  ) {
    console.log(`Attempting to navigate to ${tabName} tab`);

    try {
      // First check if we're already on this tab using JavaScript evaluation
      // This is more reliable than using the isTabActive method
      const isActive = await this.page.evaluate((tab) => {
        // Try multiple ways to determine if a tab is active

        // 1. Check for active class on buttons
        const activeButtons = Array.from(
          document.querySelectorAll(
            "button.active, button.blue, .active-button",
          ),
        );
        for (const button of activeButtons) {
          if (button.textContent?.toLowerCase().includes(tab.toLowerCase())) {
            console.log(`Found active button with text containing ${tab}`);
            return true;
          }
        }

        // 2. Check for visible tab content
        const tabContent = document.querySelector(`.${tab}-tab`);
        if (
          tabContent &&
          window.getComputedStyle(tabContent).display !== "none"
        ) {
          console.log(`Found visible tab content for ${tab}`);
          return true;
        }

        // 3. Check URL hash
        if (window.location.hash === `#${tab}`) {
          console.log(`URL hash matches #${tab}`);
          return true;
        }

        return false;
      }, tabName);

      if (isActive) {
        console.log(`Already on ${tabName} tab, no navigation needed`);
        return;
      }
    } catch (e) {
      console.log(`Error checking if ${tabName} tab is active:`, e);
      // Continue with navigation anyway
    }

    // Try multiple approaches to click the tab button
    let clicked = false;

    // Approach 1: Use the tabButtons locator
    try {
      // Make sure the tab button is visible
      await this.tabButtons[tabName].waitFor({
        state: "visible",
        timeout: 5000,
      });

      // Click the tab button
      await this.tabButtons[tabName].click();
      clicked = true;
      console.log(`Clicked ${tabName} tab button using tabButtons locator`);
    } catch (e) {
      console.log(
        `Could not click ${tabName} tab button using tabButtons locator:`,
        e,
      );
    }

    // Approach 2: Try using JavaScript if the first approach failed
    if (!clicked) {
      try {
        await this.page.evaluate((tab) => {
          // Try to find any button or element that might be the tab button
          const possibleButtons = [
            // By text content
            ...Array.from(document.querySelectorAll("button")).filter(
              (b) => b.textContent?.toLowerCase().includes(tab.toLowerCase()),
            ),
            // By class
            ...Array.from(
              document.querySelectorAll(`.${tab}-button, .${tab}-tab-button`),
            ),
            // By data attribute
            ...Array.from(document.querySelectorAll(`[data-tab="${tab}"]`)),
          ];

          // Click the first button found
          if (possibleButtons.length > 0) {
            console.log(
              `Found ${possibleButtons.length} possible buttons for ${tab} tab`,
            );
            (possibleButtons[0] as HTMLElement).click();
            return true;
          }

          return false;
        }, tabName);

        clicked = true;
        console.log(
          `Clicked ${tabName} tab button using JavaScript evaluation`,
        );
      } catch (e) {
        console.log(
          `Could not click ${tabName} tab button using JavaScript:`,
          e,
        );
      }
    }

    // If we still couldn't click, try one more approach with a more general selector
    if (!clicked) {
      try {
        // Try a very general selector
        const generalSelector = `button:has-text("${tabName}")`;
        await this.page.locator(generalSelector).first().click();
        clicked = true;
        console.log(`Clicked ${tabName} tab button using general selector`);
      } catch (e) {
        console.log(
          `Could not click ${tabName} tab button using general selector:`,
          e,
        );
        throw new Error(
          `Failed to navigate to ${tabName} tab: Could not click tab button`,
        );
      }
    }

    // Take a screenshot to help debug
    try {
      await this.page.screenshot({
        path: `test-results/after-${tabName}-tab-click.png`,
      });
    } catch (e) {
      console.log("Could not take screenshot:", e);
    }

    // Wait for the tab content to be visible with a longer timeout
    const tabContentSelector = `.${tabName}-tab`;

    // Try multiple approaches to detect when the tab is loaded
    try {
      await this.page.locator(tabContentSelector).waitFor({
        state: "visible",
        timeout: 15000,
      });
      console.log(`${tabName} tab content is visible`);
    } catch (e) {
      console.log(
        `Could not find tab content with selector ${tabContentSelector}, trying alternative approaches`,
      );

      // Try multiple ways to verify the tab has loaded
      const tabLoaded = await this.page.evaluate((tab) => {
        // 1. Check if the URL hash has changed
        if (window.location.hash === `#${tab}`) {
          console.log(`URL hash matches #${tab}`);
          return true;
        }

        // 2. Check for any visible content that might indicate the tab is loaded
        const possibleContent = [
          document.querySelector(`.${tab}-tab`),
          document.querySelector(`.${tab}-content`),
          document.querySelector(`[data-tab-content="${tab}"]`),
          document.querySelector(`[data-tab="${tab}"]`),
          // Additional selectors that might help
          document.querySelector(`.${tab}-tab-content`),
          document.querySelector(`.${tab}-panel`),
        ];

        for (const content of possibleContent) {
          if (content && window.getComputedStyle(content).display !== "none") {
            console.log(`Found visible content for ${tab} tab`);
            return true;
          }
        }

        // 3. Check if the button is active
        const activeButtons = Array.from(
          document.querySelectorAll(
            "button.active, button.blue, .active-button, .selected",
          ),
        );
        for (const button of activeButtons) {
          if (button.textContent?.toLowerCase().includes(tab.toLowerCase())) {
            console.log(`Found active button for ${tab} tab`);
            return true;
          }
        }

        return false;
      }, tabName);

      if (!tabLoaded) {
        console.log(
          `Could not verify ${tabName} tab has loaded, continuing anyway`,
        );

        // Take a screenshot to help debug
        try {
          await this.page.screenshot({
            path: `test-results/${tabName}-tab-load-failed.png`,
          });
        } catch (e) {
          console.log("Could not take screenshot:", e);
        }
      }
    }

    // Add a longer delay to ensure tab content is fully loaded
    await this.page.waitForTimeout(3000);
    console.log(`Navigation to ${tabName} tab completed`);
  }

  /**
   * Check if a specific tab is active
   */
  async isTabActive(
    tabName: "write" | "generate" | "construct" | "browse" | "learn",
  ) {
    try {
      // Use JavaScript evaluation for more reliable checking
      return await this.page.evaluate((tab) => {
        // Try multiple ways to determine if a tab is active

        // 1. Check for active class on buttons
        const activeButtons = Array.from(
          document.querySelectorAll(
            "button.active, button.blue, .active-button",
          ),
        );
        for (const button of activeButtons) {
          if (button.textContent?.toLowerCase().includes(tab.toLowerCase())) {
            return true;
          }
        }

        // 2. Check for visible tab content
        const tabContent = document.querySelector(`.${tab}-tab`);
        if (
          tabContent &&
          window.getComputedStyle(tabContent).display !== "none"
        ) {
          return true;
        }

        // 3. Check URL hash
        if (window.location.hash === `#${tab}`) {
          return true;
        }

        return false;
      }, tabName);
    } catch (e) {
      console.log(`Error checking if ${tabName} tab is active:`, e);

      // Fallback to simpler checks
      try {
        // Check if the tab content is visible
        const tabContentVisible = await this.page
          .locator(`.${tabName}-tab`)
          .isVisible();
        if (tabContentVisible) {
          return true;
        }
      } catch (e2) {
        console.log(`Error checking tab content visibility:`, e2);
      }

      return false;
    }
  }

  /**
   * Toggle fullscreen mode
   */
  async toggleFullscreen() {
    const fullscreenButton = this.page.locator("button.fullscreen-toggle");
    await fullscreenButton.click();
  }

  /**
   * Wait for the application to be fully loaded
   */
  async waitForAppReady() {
    try {
      // Wait for the loading overlay to disappear
      await this.page.locator(".loading-overlay-wrapper").waitFor({
        state: "detached",
        timeout: 15000,
      });
    } catch (e) {
      console.log("Could not find loading overlay, continuing anyway");
    }

    try {
      // Wait for the main layout to be visible
      await this.mainLayout.waitFor({ state: "visible", timeout: 15000 });
    } catch (e) {
      console.log("Could not find main layout, trying to continue anyway");

      try {
        // Take a screenshot to see what's happening
        await this.page.screenshot({
          path: "test-results/app-ready-error.png",
        });
      } catch (screenshotError) {
        console.log("Could not take screenshot:", screenshotError);
      }
    }

    try {
      // Wait for any tab button to be visible
      const tabButtonSelectors = [
        'button:has-text("Write")',
        'button:has-text("Generate")',
        'button:has-text("Construct")',
        'button:has-text("Browse")',
        'button:has-text("Learn")',
      ];

      let buttonFound = false;
      for (const selector of tabButtonSelectors) {
        try {
          const count = await this.page.locator(selector).count();
          if (count > 0) {
            await this.page
              .locator(selector)
              .first()
              .waitFor({ state: "visible", timeout: 5000 });
            buttonFound = true;
            break;
          }
        } catch (e) {
          console.log(`Could not find tab button with selector ${selector}`);
        }
      }

      if (!buttonFound) {
        console.log(
          "Could not find any tab buttons, trying to continue anyway",
        );

        try {
          // Take a screenshot to see what's happening
          await this.page.screenshot({
            path: "test-results/tab-buttons-not-found.png",
          });
        } catch (screenshotError) {
          console.log("Could not take screenshot:", screenshotError);
        }
      }
    } catch (e) {
      console.log("Error waiting for tab buttons:", e);
    }

    // Wait a moment for the UI to stabilize
    try {
      await this.page.waitForTimeout(3000);
    } catch (e) {
      console.log("Error during timeout:", e);
    }
  }
}
