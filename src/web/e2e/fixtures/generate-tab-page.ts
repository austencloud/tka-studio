import { Page, Locator } from "@playwright/test";

/**
 * Page object for the Generate Tab
 *
 * Encapsulates selectors and actions for interacting with the Generate Tab
 * and its sequence generation functionality.
 */
export class GenerateTabPage {
  readonly page: Page;

  // Generate Tab elements
  readonly generateTab: Locator;
  readonly workbenchPanel: Locator;
  readonly controlsPanel: Locator;
  readonly toggleContainer: Locator;
  readonly generateButton: Locator;
  readonly sequenceOutput: Locator;
  readonly progressBar: Locator;

  // Generator settings
  readonly numBeatsInput: Locator;
  readonly turnIntensityButtons: Locator;
  readonly propContinuityToggle: Locator;
  readonly capButtons: Locator;

  constructor(page: Page) {
    this.page = page;

    // Main tab selectors based on our DOM exploration
    this.generateTab = page.locator(".generate-tab").first();
    this.workbenchPanel = page.locator(".sequence-workbench, .workbench-panel");
    this.controlsPanel = page.locator(".controls-panel");

    // Generator controls
    this.toggleContainer = page.locator(".toggle-container");
    this.generateButton = page.locator(".generate-button");
    this.sequenceOutput = page.locator(".sequence-output, .beat-frame");
    this.progressBar = page.locator(".progress-bar, .progress-indicator");

    // Generator settings - based on actual UI
    this.numBeatsInput = page.locator(".beat-input");
    this.turnIntensityButtons = page.locator(".intensity-button");
    this.propContinuityToggle = page.locator("#prop-continuity-toggle");
    this.capButtons = page.locator(".cap-button");
  }

  /**
   * Navigate to the Generate Tab
   */
  async navigateTo() {
    console.log("Navigating to Generate tab");

    // Try multiple approaches to navigate to the Generate tab
    try {
      // Approach 1: Use JavaScript to click the button
      const clicked = await this.page.evaluate(() => {
        // Try to find the Generate tab button using multiple selectors
        const possibleButtons = [
          // By text content
          ...Array.from(document.querySelectorAll("button")).filter(
            (b) => b.textContent?.toLowerCase().includes("generate"),
          ),
          // By class
          ...Array.from(
            document.querySelectorAll(".generate-button, .generate-tab-button"),
          ),
          // By data attribute
          ...Array.from(document.querySelectorAll('[data-tab="generate"]')),
        ];

        // Click the first button found
        if (possibleButtons.length > 0) {
          console.log(
            `Found ${possibleButtons.length} possible buttons for Generate tab`,
          );
          (possibleButtons[0] as HTMLElement).click();
          return true;
        }

        return false;
      });

      if (clicked) {
        console.log("Clicked Generate tab button using JavaScript evaluation");
      } else {
        // Approach 2: Try using Playwright's locator
        console.log(
          "Could not click Generate tab button using JavaScript, trying Playwright locator",
        );

        // Try multiple selectors
        const selectors = [
          'button:has-text("Generate")',
          '.nav-button:has-text("Generate")',
          '[data-tab="generate"]',
          "button.generate-tab-button",
          ".generate-button",
        ];

        let selectorClicked = false;
        for (const selector of selectors) {
          try {
            const count = await this.page.locator(selector).count();
            if (count > 0) {
              await this.page.locator(selector).first().click();
              selectorClicked = true;
              console.log(
                `Clicked Generate tab button using selector: ${selector}`,
              );
              break;
            }
          } catch (e) {
            console.log(`Error clicking with selector ${selector}:`, e);
          }
        }

        if (!selectorClicked) {
          console.log("Could not click Generate tab button with any selector");

          // Take a screenshot to debug
          await this.page.screenshot({
            path: "test-results/generate-tab-navigation-failed.png",
          });

          // Try one more approach - use the app-page fixture's navigateToTab method
          try {
            // Import the AppPage class
            const { AppPage } = require("./app-page");
            const appPage = new AppPage(this.page);
            await appPage.navigateToTab("generate");
            console.log("Used AppPage.navigateToTab as fallback");
          } catch (e) {
            console.log("Error using AppPage.navigateToTab:", e);
            throw new Error("Failed to navigate to Generate tab");
          }
        }
      }
    } catch (e) {
      console.log("Error navigating to Generate tab:", e);
      throw e;
    }

    // Wait for the Generate tab content to be visible with a longer timeout
    try {
      await this.generateTab.waitFor({ state: "visible", timeout: 15000 });
      console.log("Generate tab content is visible");
    } catch (e) {
      console.log(
        "Could not find Generate tab content, trying alternative approaches",
      );

      // Try to verify the tab has loaded using JavaScript
      const tabLoaded = await this.page.evaluate(() => {
        // Check for any visible content that might indicate the tab is loaded
        const possibleContent = [
          document.querySelector(".generate-tab"),
          document.querySelector(".generate-content"),
          document.querySelector('[data-tab-content="generate"]'),
          document.querySelector(".sequence-workbench"),
          document.querySelector(".controls-panel"),
        ];

        for (const content of possibleContent) {
          if (content && window.getComputedStyle(content).display !== "none") {
            console.log("Found visible content for Generate tab");
            return true;
          }
        }

        return false;
      });

      if (!tabLoaded) {
        console.log(
          "Could not verify Generate tab has loaded, continuing anyway",
        );

        // Take a screenshot to debug
        await this.page.screenshot({
          path: "test-results/generate-tab-content-not-found.png",
        });
      }
    }

    // Add a longer delay to ensure the tab content is fully loaded
    await this.page.waitForTimeout(2000);
    console.log("Navigation to Generate tab completed");
  }

  /**
   * Select a generator type (circular or freeform)
   */
  async selectGeneratorType(type: "circular" | "freeform") {
    // Find the generator type option and click it based on text content
    const typeText = type === "circular" ? "Circular" : "Freeform";
    await this.page.locator(`.toggle-option:has-text("${typeText}")`).click();
  }

  /**
   * Set the number of beats for sequence generation
   */
  async setNumBeats(value: number) {
    await this.numBeatsInput.fill(value.toString());
  }

  /**
   * Set the turn intensity for sequence generation
   */
  async setTurnIntensity(value: number) {
    // Find the intensity button with the specified value
    await this.turnIntensityButtons.nth(value - 1).click();
  }

  /**
   * Set the prop continuity for sequence generation
   */
  async setPropContinuity(value: "continuous" | "discontinuous") {
    // Get the current state
    const isSelected = await this.page
      .locator(".toggle-label.selected")
      .textContent();
    const currentValue = isSelected?.toLowerCase().includes("continuous")
      ? "continuous"
      : "discontinuous";

    // Only toggle if the current value is different from the desired value
    if (currentValue !== value) {
      await this.propContinuityToggle.click();
    }
  }

  /**
   * Set the cap type for sequence generation
   */
  async setCapType(value: "mirrored" | "matched" | "random") {
    // Map the value to the actual button text
    const buttonTextMap = {
      mirrored: "Mirrored",
      matched: "Rotated",
      random: "Swapped Complementary",
    };

    // Click the appropriate CAP button
    await this.page
      .locator(`.cap-button:has-text("${buttonTextMap[value]}")`)
      .first()
      .click();
  }

  /**
   * Generate a sequence with the current settings
   */
  async generateSequence() {
    // First scroll to the generate button to make it visible
    await this.page.evaluate(() => {
      // Find the generate button
      const button = document.querySelector(".generate-button") as HTMLElement;
      if (button) {
        // Scroll to the button
        button.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    });

    // Wait a moment for the scroll to complete
    await this.page.waitForTimeout(1000);

    // Click the generate button using JavaScript
    await this.page.evaluate(() => {
      const button = document.querySelector(
        ".generate-button",
      ) as HTMLButtonElement;
      if (button) {
        button.click();
      }
    });

    // Wait for a moment to ensure the generation process has started
    await this.page.waitForTimeout(1000);

    // Wait for generation to complete
    try {
      // Wait for the "Ready" indicator to appear
      await this.page.locator('.indicator-label:has-text("Ready")').waitFor({
        state: "visible",
        timeout: 30000,
      });
    } catch (e) {
      console.log(
        'Could not detect "Ready" indicator, waiting for sequence output instead',
      );

      // Wait for the sequence output to be visible
      await this.sequenceOutput.waitFor({ state: "visible", timeout: 30000 });
    }

    // Add a small delay to ensure the sequence is fully loaded
    await this.page.waitForTimeout(1000);
  }

  /**
   * Get the generated sequence beats
   */
  async getGeneratedSequenceBeats() {
    // Look for beat elements in the sequence
    const beats = this.page.locator(".beat");
    return await beats.count();
  }

  /**
   * Drag a generated sequence to the Write Tab
   */
  async dragSequenceToWriteTab() {
    try {
      console.log("Starting sequence drag operation");

      // First navigate to the Write tab to ensure it's initialized
      console.log("Navigating to Write tab");
      await this.page.locator('button:has-text("Write")').click();
      await this.page.waitForTimeout(1000); // Add a small delay
      await this.page
        .locator(".write-tab")
        .waitFor({ state: "visible", timeout: 15000 });
      console.log("Write tab visible");

      // Then navigate back to Generate tab
      console.log("Navigating back to Generate tab");
      await this.page.locator('button.nav-button:has-text("Generate")').click();
      await this.page.waitForTimeout(1000); // Add a small delay
      await this.generateTab.waitFor({ state: "visible", timeout: 15000 });
      console.log("Generate tab visible");

      // Wait for any animations to complete
      await this.page.waitForTimeout(2000);

      // Make sure sequence is visible before clicking
      console.log("Waiting for sequence to be visible");
      const beatFrame = this.page.locator(".beat-frame").first();
      await beatFrame.waitFor({ state: "visible", timeout: 15000 });

      // Take a screenshot before clicking
      await this.page.screenshot({
        path: "test-results/before-sequence-click.png",
      });

      // Try a more reliable approach using JavaScript
      console.log("Selecting sequence");
      try {
        // First try normal click
        await beatFrame.click({ timeout: 15000, force: true });
        console.log("Clicked sequence using Playwright click");
      } catch (e) {
        console.log("Error clicking sequence, trying JavaScript approach:", e);
        // Fall back to JavaScript click
        await this.page.evaluate(() => {
          const beatFrame = document.querySelector(".beat-frame");
          if (beatFrame) {
            // Cast to HTMLElement to access click method
            (beatFrame as HTMLElement).click();
            return true;
          }
          return false;
        });
        console.log("Clicked sequence using JavaScript");
      }

      // Wait a moment for the click to register
      await this.page.waitForTimeout(1000);

      // Copy the sequence
      console.log("Copying sequence");
      await this.page.keyboard.press("Control+C");
      await this.page.waitForTimeout(1000); // Wait for copy operation

      // Navigate to Write tab again
      console.log("Navigating to Write tab again");
      await this.page.locator('button:has-text("Write")').click();
      await this.page.waitForTimeout(1000); // Add a small delay
      await this.page
        .locator(".write-tab")
        .waitFor({ state: "visible", timeout: 15000 });
      console.log("Write tab visible again");

      // Wait for any animations to complete
      await this.page.waitForTimeout(2000);

      // Paste the sequence
      console.log("Pasting sequence");
      await this.page.keyboard.press("Control+V");
      console.log("Sequence drag operation completed");
    } catch (e) {
      console.error("Error in dragSequenceToWriteTab:", e);
      // Take a screenshot to help debug the issue
      await this.page.screenshot({
        path: "test-results/drag-sequence-error.png",
      });
      throw e;
    }
  }
}
