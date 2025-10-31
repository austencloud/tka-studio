import { expect, test } from "@playwright/test";

/**
 * E2E Test: Animation Panel Slide Animation
 *
 * Tests that the inline animation panel slides up smoothly without jank
 * when the play button is clicked. This test visually captures the animation
 * to verify smooth transitions.
 */

test.describe("Animation Panel Slide Animation", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
    // Wait for any navigation to be ready
    await page.waitForTimeout(2000);
  });

  test("should slide up smoothly when play button is clicked", async ({
    page,
  }) => {
    // 1. Navigate to Build module
    const buildTab = page
      .locator(".nav-tab-container")
      .filter({ hasText: "Build" });
    await buildTab.click();
    await page.waitForTimeout(500);

    // 2. Create a sequence by selecting a start position
    const firstPosition = page.locator(".pictograph-container").first();
    await firstPosition.click();
    await page.waitForTimeout(500);

    // 3. Add at least one beat to the sequence
    const firstOption = page.locator(".option-card").first();
    await firstOption.click();
    await page.waitForTimeout(500);

    // 4. Verify play button is visible
    const playButton = page.locator('button[aria-label="Play animation"]');
    await expect(playButton).toBeVisible();

    // 5. Take screenshot before clicking play
    await page.screenshot({
      path: "test-results/before-play.png",
      fullPage: false,
    });

    // 6. Start recording animation frames
    const frameCount = 10;
    const recordingPromise = (async () => {
      for (let i = 0; i < frameCount; i++) {
        await page.waitForTimeout(30); // 30ms intervals = ~33fps
        await page.screenshot({ path: `test-results/frame-${i}.png` });
      }
    })();

    // 7. Click play button - this should trigger the slide animation
    await playButton.click();

    // Wait for recording to complete
    await recordingPromise;

    // 8. Take screenshot after animation should be complete
    await page.waitForTimeout(400); // Wait for 320ms delay + some buffer
    await page.screenshot({
      path: "test-results/after-play.png",
      fullPage: false,
    });

    // 9. Verify the animation panel is now visible
    const animatorPanel = page.locator(".inline-animator-panel");
    await expect(animatorPanel).toBeVisible({ timeout: 1000 });

    // 10. Check if BottomSheet has the expected transition
    const bottomSheet = page.locator(".bottom-sheet.inline-animator-container");
    await expect(bottomSheet).toBeVisible();

    // 11. Verify the panel has content (not just an empty div)
    const canvasContainer = page.locator(".canvas-container");
    await expect(canvasContainer).toBeVisible({ timeout: 2000 });

    console.log(`✅ Captured ${frameCount} animation frames`);
    console.log(
      "📊 Animation test complete - check screenshots in test-results/"
    );
  });

  test("sequence actions sheet should slide up smoothly for comparison", async ({
    page,
  }) => {
    // 1. Navigate to Build module
    const buildTab = page
      .locator(".nav-tab-container")
      .filter({ hasText: "Build" });
    await buildTab.click();
    await page.waitForTimeout(500);

    // 2. Create a sequence
    const firstPosition = page.locator(".pictograph-container").first();
    await firstPosition.click();
    await page.waitForTimeout(500);

    const firstOption = page.locator(".option-card").first();
    await firstOption.click();
    await page.waitForTimeout(500);

    // 3. Click sequence actions button
    const actionsButton = page.locator('button[aria-label="Sequence actions"]');
    await expect(actionsButton).toBeVisible();

    await page.screenshot({
      path: "test-results/before-actions.png",
      fullPage: false,
    });

    await actionsButton.click();

    await page.waitForTimeout(400);
    await page.screenshot({
      path: "test-results/after-actions.png",
      fullPage: false,
    });

    // 4. Verify actions sheet is visible
    const actionsSheet = page.locator(".actions-sheet");
    await expect(actionsSheet).toBeVisible({ timeout: 1000 });

    console.log("✅ Sequence actions sheet animation test complete");
  });
});
