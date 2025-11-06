import { test, expect } from "@playwright/test";

test.describe("Edit Panel Deselection Test", () => {
  test("should properly deselect pictograph when clicking outside edit panel", async ({
    page,
  }) => {
    // Navigate to the app
    await page.goto("http://localhost:5173/");
    console.log("🏠 Navigated to app");

    // Wait for the app to load
    await page.waitForLoadState("networkidle");
    await page.waitForTimeout(1000);

    // Navigate to Build tab
    const buildTab = page.locator('button:has-text("Build")').first();
    await buildTab.waitFor({ state: "visible", timeout: 5000 });
    await buildTab.click();
    console.log("🏗️ Clicked Build tab");
    await page.waitForTimeout(500);

    // Navigate to Construct mode
    const constructButton = page
      .locator('button:has-text("Construct")')
      .first();
    if (await constructButton.isVisible()) {
      await constructButton.click();
      console.log("🔨 Clicked Construct");
      await page.waitForTimeout(1000);
    }

    // Select a start position
    const startPositions = page
      .locator('[data-testid="start-position-option"]')
      .or(page.locator('button:has-text("α")'));

    const startPositionCount = await startPositions.count();
    if (startPositionCount > 0) {
      await startPositions.first().click();
      console.log("📍 Selected start position");
      await page.waitForTimeout(500);
    } else {
      console.log("⚠️ No start positions found, test may fail");
    }

    // Look for option tiles to add a beat
    const optionTiles = page.locator('[role="button"]').filter({
      has: page.locator('svg'),
    });

    const optionCount = await optionTiles.count();
    if (optionCount > 0) {
      // Click the first option to add a beat
      await optionTiles.first().click();
      console.log("✅ Added first beat to sequence");
      await page.waitForTimeout(1000);
    } else {
      console.log("⚠️ No option tiles found");
    }

    // Find the beat cell in the workspace
    const beatCell = page.locator('.beat-cell').first();
    await beatCell.waitFor({ state: "visible", timeout: 5000 });
    console.log("🎯 Found beat cell");

    // Click on the beat to open edit panel
    await beatCell.click();
    console.log("🖱️ Clicked beat cell");
    await page.waitForTimeout(500);

    // Verify edit panel is open (look for edit panel container)
    const editPanel = page.locator('.edit-panel').or(
      page.locator('[class*="edit"]').filter({ hasText: /Edit|Orientation|Turns/ })
    );
    await expect(editPanel.first()).toBeVisible({ timeout: 3000 });
    console.log("✅ Edit panel is open");

    // Verify beat is selected (has selected class)
    await expect(beatCell).toHaveClass(/selected/, { timeout: 2000 });
    console.log("✅ Beat is selected (has selected class)");

    // Get the beat's bounding box to click outside of it
    const beatBox = await beatCell.boundingBox();

    // Click on an empty area of the workspace (not on the beat, not on the panel)
    // Click to the left of the beat, in the workspace area
    const clickX = beatBox ? beatBox.x - 100 : 100;
    const clickY = beatBox ? beatBox.y : 300;

    console.log(`🖱️ Clicking outside edit panel at (${clickX}, ${clickY})`);
    await page.mouse.click(clickX, clickY);
    await page.waitForTimeout(500);

    // Verify edit panel is closed
    await expect(editPanel.first()).not.toBeVisible({ timeout: 3000 });
    console.log("✅ Edit panel is closed");

    // Verify beat is no longer selected (doesn't have selected class)
    await expect(beatCell).not.toHaveClass(/selected/, { timeout: 2000 });
    console.log("✅ Beat is deselected (no longer has selected class)");

    // Verify subsequent selections work - click the beat again
    await beatCell.click();
    console.log("🖱️ Clicked beat cell again to test re-selection");
    await page.waitForTimeout(500);

    // Verify edit panel opens again
    await expect(editPanel.first()).toBeVisible({ timeout: 3000 });
    console.log("✅ Edit panel opened again");

    // Verify beat is selected again
    await expect(beatCell).toHaveClass(/selected/, { timeout: 2000 });
    console.log("✅ Beat is selected again (subsequent selection works)");

    console.log("🎉 Test passed: Edit panel properly deselects pictograph on outside click");
  });

  test("should not deselect when clicking on another beat", async ({ page }) => {
    // Navigate to the app
    await page.goto("http://localhost:5173/");
    console.log("🏠 Navigated to app");

    await page.waitForLoadState("networkidle");
    await page.waitForTimeout(1000);

    // Navigate to Build > Construct
    const buildTab = page.locator('button:has-text("Build")').first();
    await buildTab.waitFor({ state: "visible", timeout: 5000 });
    await buildTab.click();
    await page.waitForTimeout(500);

    const constructButton = page
      .locator('button:has-text("Construct")')
      .first();
    if (await constructButton.isVisible()) {
      await constructButton.click();
      await page.waitForTimeout(1000);
    }

    // Select start position
    const startPositions = page
      .locator('[data-testid="start-position-option"]')
      .or(page.locator('button:has-text("α")'));

    if ((await startPositions.count()) > 0) {
      await startPositions.first().click();
      await page.waitForTimeout(500);
    }

    // Add two beats to the sequence
    const optionTiles = page.locator('[role="button"]').filter({
      has: page.locator('svg'),
    });

    if ((await optionTiles.count()) >= 2) {
      // Add first beat
      await optionTiles.nth(0).click();
      await page.waitForTimeout(500);

      // Add second beat
      await optionTiles.nth(1).click();
      await page.waitForTimeout(1000);
      console.log("✅ Added two beats to sequence");
    }

    // Find both beat cells
    const beatCells = page.locator('.beat-cell');
    await expect(beatCells).toHaveCount(2, { timeout: 5000 });

    const firstBeat = beatCells.nth(0);
    const secondBeat = beatCells.nth(1);

    // Click first beat to select it
    await firstBeat.click();
    await page.waitForTimeout(500);
    console.log("🖱️ Clicked first beat");

    // Verify first beat is selected
    await expect(firstBeat).toHaveClass(/selected/, { timeout: 2000 });
    console.log("✅ First beat is selected");

    // Click second beat - panel should switch to editing second beat
    await secondBeat.click();
    await page.waitForTimeout(500);
    console.log("🖱️ Clicked second beat");

    // Verify second beat is now selected
    await expect(secondBeat).toHaveClass(/selected/, { timeout: 2000 });
    console.log("✅ Second beat is now selected");

    // Verify first beat is no longer selected
    await expect(firstBeat).not.toHaveClass(/selected/, { timeout: 2000 });
    console.log("✅ First beat is no longer selected");

    // Edit panel should still be open
    const editPanel = page.locator('.edit-panel').or(
      page.locator('[class*="edit"]').filter({ hasText: /Edit|Orientation|Turns/ })
    );
    await expect(editPanel.first()).toBeVisible({ timeout: 3000 });
    console.log("✅ Edit panel remains open when switching between beats");

    console.log("🎉 Test passed: Beat selection switching works correctly");
  });
});
