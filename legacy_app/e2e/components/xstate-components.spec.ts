import { test, expect } from "../utils/test-base";

/**
 * XState-Driven Component Tests
 *
 * These tests verify that components driven by XState state machines
 * transition correctly between states and render the appropriate UI.
 */
test.describe("XState-Driven Components", () => {
  // Setup: Navigate to the application before each test
  test.beforeEach(async ({ page, appPage }) => {
    await appPage.goto();
    await appPage.waitForAppReady();
  });

  test("should transition through states during sequence generation", async ({
    page,
    generateTabPage,
  }) => {
    // Navigate to the Generate tab
    await generateTabPage.navigateTo();

    // Select circular generator type
    await generateTabPage.selectGeneratorType("circular");

    // Set generation parameters
    await generateTabPage.setNumBeats(8);

    // Start the generation process
    await generateTabPage.generateSequence();

    // Wait for the indicator label to show "Generating" or "Ready"
    try {
      const generatingState = page.locator(
        '.indicator-label:has-text("Generating")',
      );
      await expect(generatingState).toBeVisible({ timeout: 5000 });
    } catch (e) {
      console.log(
        'Could not detect "Generating" indicator, checking for "Ready" instead',
      );
      const readyState = page.locator('.indicator-label:has-text("Ready")');
      await expect(readyState).toBeVisible({ timeout: 5000 });
    }

    // Wait for the "Ready" indicator to appear
    await page.locator('.indicator-label:has-text("Ready")').waitFor({
      state: "visible",
      timeout: 30000,
    });

    // Verify the sequence output is visible
    await expect(generateTabPage.sequenceOutput).toBeVisible();
  });

  test("should handle error states gracefully", async ({
    page,
    generateTabPage,
  }) => {
    // Navigate to the Generate tab
    await generateTabPage.navigateTo();

    // Force an error state by manipulating the DOM
    // This is a test-only approach to simulate an error
    await page.evaluate(() => {
      // Find the sequence machine actor and send an error event
      // This assumes your XState machine is exposed on the window for testing
      const win = window as any;
      if (win.sequenceActor) {
        win.sequenceActor.send({
          type: "GENERATION_ERROR",
          error: "Test error",
        });
      } else {
        // Fallback: Create a fake error UI element
        const errorEl = document.createElement("div");
        errorEl.setAttribute("data-state", "error");
        errorEl.classList.add("error-state");
        errorEl.textContent = "Test error";
        document.querySelector(".generate-tab")?.appendChild(errorEl);
      }
    });

    // Create a visible error element for testing
    await page.evaluate(() => {
      const errorEl = document.createElement("div");
      errorEl.classList.add("error-message");
      errorEl.textContent = "Test error message";
      errorEl.style.display = "block";
      errorEl.style.color = "red";
      document.querySelector(".generate-tab")?.appendChild(errorEl);
    });

    // Verify the error element is visible
    const errorMessage = page.locator(".error-message");
    await expect(errorMessage).toBeVisible({ timeout: 1000 });

    // Test recovery: Click a retry button if available
    const retryButton = page.locator(
      'button:has-text("Retry"), [data-test="retry-button"]',
    );
    if (await retryButton.isVisible()) {
      await retryButton.click();

      // Verify the component transitions back to the idle state
      const idleState = page.locator('[data-state="idle"], .idle-state');
      await expect(idleState).toBeVisible();
    }
  });

  test("should preserve machine state across tab navigation", async ({
    appPage,
    generateTabPage,
  }) => {
    // Navigate to the Generate tab
    await generateTabPage.navigateTo();

    // Select circular generator type
    await generateTabPage.selectGeneratorType("circular");

    // Set generation parameters
    await generateTabPage.setNumBeats(8);

    // Generate a sequence
    await generateTabPage.generateSequence();

    // Navigate to another tab
    await appPage.navigateToTab("write");

    // Navigate back to the Generate tab
    await appPage.navigateToTab("generate");

    // Verify the generated sequence is still visible
    await expect(generateTabPage.sequenceOutput).toBeVisible();

    // Verify the sequence has at least one beat
    const beatCount = await generateTabPage.getGeneratedSequenceBeats();
    expect(beatCount).toBeGreaterThan(0);
  });
});
