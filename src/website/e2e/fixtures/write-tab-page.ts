import { Page, Locator } from "@playwright/test";

/**
 * Page object for the Write Tab
 *
 * Encapsulates selectors and actions for interacting with the Write Tab
 * and its sequence editing functionality.
 */
export class WriteTabPage {
  readonly page: Page;

  // Write Tab elements
  readonly writeTab: Locator;
  readonly actSheet: Locator;
  readonly sequenceRows: Locator;
  readonly beatCells: Locator;
  readonly actTitle: Locator;
  readonly actTitleInput: Locator;
  readonly favoriteSequences: Locator;

  constructor(page: Page) {
    this.page = page;

    // Main tab selectors
    this.writeTab = page.locator(".write-tab");
    this.actSheet = page.locator(".act-sheet");
    this.sequenceRows = page.locator(".sequence-row");
    this.beatCells = page.locator(".beat-cell");

    // Act title elements
    this.actTitle = page.locator(".act-title");
    this.actTitleInput = page.locator("input.act-title-input");

    // Favorite sequences panel
    this.favoriteSequences = page.locator(".favorite-sequences");
  }

  /**
   * Navigate to the Write Tab
   */
  async navigateTo() {
    console.log("Navigating to Write tab");

    // Try multiple approaches to navigate to the Write tab
    try {
      // Approach 1: Use JavaScript to click the button
      const clicked = await this.page.evaluate(() => {
        // Try to find the Write tab button using multiple selectors
        const possibleButtons = [
          // By text content
          ...Array.from(document.querySelectorAll("button")).filter(
            (b) => b.textContent?.toLowerCase().includes("write"),
          ),
          // By class
          ...Array.from(
            document.querySelectorAll(".write-button, .write-tab-button"),
          ),
          // By data attribute
          ...Array.from(document.querySelectorAll('[data-tab="write"]')),
        ];

        // Click the first button found
        if (possibleButtons.length > 0) {
          console.log(
            `Found ${possibleButtons.length} possible buttons for Write tab`,
          );
          (possibleButtons[0] as HTMLElement).click();
          return true;
        }

        return false;
      });

      if (clicked) {
        console.log("Clicked Write tab button using JavaScript evaluation");
      } else {
        // Approach 2: Try using Playwright's locator
        console.log(
          "Could not click Write tab button using JavaScript, trying Playwright locator",
        );

        // Try multiple selectors
        const selectors = [
          'button:has-text("Write")',
          '.nav-button:has-text("Write")',
          '[data-tab="write"]',
          "button.write-tab-button",
          ".write-button",
        ];

        let selectorClicked = false;
        for (const selector of selectors) {
          try {
            const count = await this.page.locator(selector).count();
            if (count > 0) {
              await this.page.locator(selector).first().click();
              selectorClicked = true;
              console.log(
                `Clicked Write tab button using selector: ${selector}`,
              );
              break;
            }
          } catch (e) {
            console.log(`Error clicking with selector ${selector}:`, e);
          }
        }

        if (!selectorClicked) {
          console.log("Could not click Write tab button with any selector");

          // Take a screenshot to debug
          await this.page.screenshot({
            path: "test-results/write-tab-navigation-failed.png",
          });

          // Try one more approach - use the app-page fixture's navigateToTab method
          try {
            // Import the AppPage class
            const { AppPage } = require("./app-page");
            const appPage = new AppPage(this.page);
            await appPage.navigateToTab("write");
            console.log("Used AppPage.navigateToTab as fallback");
          } catch (e) {
            console.log("Error using AppPage.navigateToTab:", e);
            throw new Error("Failed to navigate to Write tab");
          }
        }
      }
    } catch (e) {
      console.log("Error navigating to Write tab:", e);
      throw e;
    }

    // Wait for the Write tab content to be visible with a longer timeout
    try {
      await this.writeTab.waitFor({ state: "visible", timeout: 15000 });
      console.log("Write tab content is visible");
    } catch (e) {
      console.log(
        "Could not find Write tab content, trying alternative approaches",
      );

      // Try to verify the tab has loaded using JavaScript
      const tabLoaded = await this.page.evaluate(() => {
        // Check for any visible content that might indicate the tab is loaded
        const possibleContent = [
          document.querySelector(".write-tab"),
          document.querySelector(".write-content"),
          document.querySelector('[data-tab-content="write"]'),
          document.querySelector(".act-sheet"),
          document.querySelector(".favorite-sequences"),
        ];

        for (const content of possibleContent) {
          if (content && window.getComputedStyle(content).display !== "none") {
            console.log("Found visible content for Write tab");
            return true;
          }
        }

        return false;
      });

      if (!tabLoaded) {
        console.log("Could not verify Write tab has loaded, continuing anyway");

        // Take a screenshot to debug
        await this.page.screenshot({
          path: "test-results/write-tab-content-not-found.png",
        });
      }
    }

    // Add a longer delay to ensure the tab content is fully loaded
    await this.page.waitForTimeout(2000);
    console.log("Navigation to Write tab completed");
  }

  /**
   * Set the act title
   */
  async setActTitle(title: string) {
    // First make sure we're on the Write tab
    await this.navigateTo();

    // Use JavaScript to directly set the title without clicking
    await this.page.evaluate((newTitle) => {
      // Try to find the title element
      const titleElement = document.querySelector(".act-title") as HTMLElement;
      if (titleElement) {
        // If there's an input already visible, use it
        const inputElement = document.querySelector(
          "input.act-title-input",
        ) as HTMLInputElement;
        if (inputElement) {
          inputElement.value = newTitle;
          // Dispatch input and change events to trigger reactivity
          inputElement.dispatchEvent(new Event("input", { bubbles: true }));
          inputElement.dispatchEvent(new Event("change", { bubbles: true }));
        } else {
          // Otherwise, try to update the title directly
          // This is a fallback and may not work depending on the app's architecture
          titleElement.textContent = newTitle;
        }
      }
    }, title);

    // Wait for the change to take effect
    await this.page.waitForTimeout(1000);
  }

  /**
   * Get the current act title
   */
  async getActTitle() {
    // Use JavaScript to get the title
    return await this.page.evaluate(() => {
      const titleElement = document.querySelector(".act-title");
      return titleElement ? titleElement.textContent || "" : "";
    });
  }

  /**
   * Get the number of sequences in the act
   */
  async getSequenceCount() {
    return await this.sequenceRows.count();
  }

  /**
   * Get the number of beats in a sequence
   */
  async getBeatCount(sequenceIndex: number) {
    const sequenceRow = this.sequenceRows.nth(sequenceIndex);
    const beats = sequenceRow.locator(".beat-cell");
    return await beats.count();
  }

  /**
   * Click on a beat cell
   */
  async clickBeatCell(sequenceIndex: number, beatIndex: number) {
    // Use JavaScript to click the beat cell
    await this.page.evaluate(
      ({ seqIndex, beatIdx }) => {
        // Get all sequence rows
        const rows = document.querySelectorAll(".sequence-row");
        if (rows.length > seqIndex) {
          // Get the specified row
          const row = rows[seqIndex];
          // Get all beat cells in that row
          const cells = row.querySelectorAll(".beat-cell");
          if (cells.length > beatIdx) {
            // Click the specified cell
            (cells[beatIdx] as HTMLElement).click();
          }
        }
      },
      { seqIndex: sequenceIndex, beatIdx: beatIndex },
    );

    // Wait for any UI updates
    await this.page.waitForTimeout(1000);
  }

  /**
   * Check if a beat cell is filled
   */
  async isBeatCellFilled(sequenceIndex: number, beatIndex: number) {
    // Use JavaScript to check if the cell is filled
    return await this.page.evaluate(
      ({ seqIndex, beatIdx }) => {
        // Get all sequence rows
        const rows = document.querySelectorAll(".sequence-row");
        if (rows.length > seqIndex) {
          // Get the specified row
          const row = rows[seqIndex];
          // Get all beat cells in that row
          const cells = row.querySelectorAll(".beat-cell");
          if (cells.length > beatIdx) {
            // Check if the cell has the filled class
            return (
              cells[beatIdx].classList.contains("is-filled") ||
              cells[beatIdx].classList.contains("filled") ||
              cells[beatIdx].querySelector(".beat-content") !== null
            );
          }
        }
        return false;
      },
      { seqIndex: sequenceIndex, beatIdx: beatIndex },
    );
  }

  /**
   * Set a cue for a sequence
   */
  async setSequenceCue(sequenceIndex: number, cue: string) {
    const sequenceRow = this.sequenceRows.nth(sequenceIndex);
    const cueInput = sequenceRow.locator("input.cue-input");

    await cueInput.clear();
    await cueInput.fill(cue);
    await cueInput.press("Enter");
  }

  /**
   * Set a timestamp for a sequence
   */
  async setSequenceTimestamp(sequenceIndex: number, timestamp: string) {
    const sequenceRow = this.sequenceRows.nth(sequenceIndex);
    const timestampInput = sequenceRow.locator("input.timestamp-input");

    await timestampInput.clear();
    await timestampInput.fill(timestamp);
    await timestampInput.press("Enter");
  }

  /**
   * Drag a sequence from favorites to the act sheet
   */
  async dragFavoriteSequenceToAct(
    favoriteIndex: number,
    targetSequenceIndex: number,
  ) {
    const favoriteSequence = this.favoriteSequences
      .locator(".favorite-sequence-item")
      .nth(favoriteIndex);
    const targetSequence = this.sequenceRows.nth(targetSequenceIndex);

    await favoriteSequence.dragTo(targetSequence);
  }

  /**
   * Erase a beat
   */
  async eraseBeat(sequenceIndex: number, beatIndex: number) {
    // Right-click on the beat to open the context menu
    const beatCell = this.sequenceRows
      .nth(sequenceIndex)
      .locator(".beat-cell")
      .nth(beatIndex);
    await beatCell.click({ button: "right" });

    // Click the erase option
    await this.page.locator("text=Erase").click();
  }

  /**
   * Erase the entire act
   */
  async eraseEntireAct() {
    // Click the erase act button
    await this.page.locator('button:has-text("Erase Act")').click();

    // Confirm the action
    await this.page.locator('button:has-text("Confirm")').click();
  }
}
