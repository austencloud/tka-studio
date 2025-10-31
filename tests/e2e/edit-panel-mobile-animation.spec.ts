import { test, expect } from "@playwright/test";

test.describe("Edit Panel Mobile Animation Test", () => {
  test("should observe edit panel animation at Z Fold 5 viewport (344x882)", async ({
    page,
  }) => {
    // Set viewport to Z Fold 5 folded size
    await page.setViewportSize({ width: 344, height: 882 });

    // Navigate to the app
    await page.goto("/");
    console.log("📱 Set viewport to 344x882 (Z Fold 5 folded)");

    // Wait for the app to load
    await page.waitForLoadState("networkidle");
    await page.waitForTimeout(1000);

    // Navigate to Build tab
    const buildTab = page.locator('button:has-text("Build")').first();
    await buildTab.waitFor({ state: "visible", timeout: 5000 });
    await buildTab.click();
    console.log("🏗️ Clicked Build tab");
    await page.waitForTimeout(500);

    // Navigate to Construct
    const constructButton = page
      .locator('button:has-text("Construct")')
      .first();
    if (await constructButton.isVisible()) {
      await constructButton.click();
      console.log("🔨 Clicked Construct");
      await page.waitForTimeout(1000);
    }

    // Click on a start position to get into the flow
    const startPositions = page
      .locator('[data-testid="start-position-option"]')
      .or(page.locator('button:has-text("α")'));
    if (
      await startPositions
        .first()
        .isVisible({ timeout: 3000 })
        .catch(() => false)
    ) {
      await startPositions.first().click();
      console.log("📍 Selected start position");
      await page.waitForTimeout(500);
    }

    // Look for any existing beats or the ability to add beats
    // Check for the variations button which appears after start position is selected
    const variationsButton = page.locator('button:has-text("Variations")');
    if (
      await variationsButton.isVisible({ timeout: 3000 }).catch(() => false)
    ) {
      await variationsButton.click();
      console.log("⚡ Clicked Variations");
      await page.waitForTimeout(500);

      // Click on the first variation to add a beat
      const firstVariation = page.locator("[data-beat-id]").first();
      if (
        await firstVariation.isVisible({ timeout: 3000 }).catch(() => false)
      ) {
        await firstVariation.click();
        console.log("✅ Added first beat");
        await page.waitForTimeout(500);
      }
    }

    // Now look for beats in the sequence display
    await page.waitForTimeout(500);
    const beats = page.locator("[data-beat-id]");
    const beatCount = await beats.count();
    console.log(`📊 Found ${beatCount} beats in sequence`);

    if (beatCount > 0) {
      // Look for an Edit button on the first beat
      const editButton = page.locator('button[aria-label*="Edit"]').first();

      if (await editButton.isVisible()) {
        console.log("🎯 Edit button found, preparing to observe animation...");

        // Get initial panel state
        const editPanel = page.locator(".edit-panel-overlay").first();
        const panelVisibleBefore = await editPanel
          .isVisible()
          .catch(() => false);
        console.log(`📋 Edit panel visible before: ${panelVisibleBefore}`);

        // Take screenshot before clicking
        await page.screenshot({
          path: "before-edit-panel.png",
          fullPage: true,
        });
        console.log("📸 Screenshot saved: before-edit-panel.png");

        // Click the edit button and observe
        console.log("🖱️ Clicking edit button...");
        await editButton.click();

        // Wait a bit for animation to start
        await page.waitForTimeout(100);

        // Take screenshot during animation
        await page.screenshot({
          path: "during-edit-panel-animation.png",
          fullPage: true,
        });
        console.log("📸 Screenshot saved: during-edit-panel-animation.png");

        // Wait for panel to be visible
        await editPanel.waitFor({ state: "visible", timeout: 5000 });
        console.log("✅ Edit panel is now visible");

        // Wait for animation to complete
        await page.waitForTimeout(500);

        // Take screenshot after animation
        await page.screenshot({ path: "after-edit-panel.png", fullPage: true });
        console.log("📸 Screenshot saved: after-edit-panel.png");

        // Get panel position and dimensions
        const panelBounds = await editPanel.boundingBox();
        if (panelBounds) {
          console.log("📐 Panel position and size:");
          console.log(`   - X: ${panelBounds.x}`);
          console.log(`   - Y: ${panelBounds.y}`);
          console.log(`   - Width: ${panelBounds.width}`);
          console.log(`   - Height: ${panelBounds.height}`);
          console.log(`   - Right edge: ${panelBounds.x + panelBounds.width}`);
          console.log(
            `   - Bottom edge: ${panelBounds.y + panelBounds.height}`
          );
        }

        // Check computed styles
        const panelStyles = await editPanel.evaluate((el) => {
          const styles = window.getComputedStyle(el);
          return {
            position: styles.position,
            top: styles.top,
            right: styles.right,
            bottom: styles.bottom,
            left: styles.left,
            transform: styles.transform,
            width: styles.width,
            height: styles.height,
            justifyContent: styles.justifyContent,
            alignItems: styles.alignItems,
            flexDirection: styles.flexDirection,
          };
        });
        console.log("🎨 Panel computed styles:", panelStyles);

        // Check if panel has mobile class
        const panelClasses = await editPanel.getAttribute("class");
        console.log("📝 Panel classes:", panelClasses);
        console.log(
          `🔍 Has 'mobile' class: ${panelClasses?.includes("mobile")}`
        );

        // Get viewport dimensions for comparison
        const viewport = page.viewportSize();
        console.log(`📱 Viewport: ${viewport?.width}x${viewport?.height}`);

        // Analyze animation direction
        if (panelBounds) {
          const isFullWidth =
            Math.abs(panelBounds.width - (viewport?.width || 0)) < 10;
          const isFullHeight =
            Math.abs(panelBounds.height - (viewport?.height || 0)) < 10;
          const isAtRight =
            panelBounds.x + panelBounds.width >= (viewport?.width || 0) - 5;
          const isAtBottom =
            panelBounds.y + panelBounds.height >= (viewport?.height || 0) - 5;

          console.log("\n🔍 ANIMATION ANALYSIS:");
          console.log(`   - Panel is full width: ${isFullWidth}`);
          console.log(`   - Panel is full height: ${isFullHeight}`);
          console.log(`   - Panel is at right edge: ${isAtRight}`);
          console.log(`   - Panel is at bottom edge: ${isAtBottom}`);

          if (isFullHeight && isAtRight) {
            console.log(
              "   ⚠️ DETECTED: Panel slides from RIGHT (current behavior)"
            );
          } else if (isFullWidth && isAtBottom) {
            console.log(
              "   ✅ DETECTED: Panel slides from BOTTOM (desired behavior)"
            );
          }
        }

        console.log("\n📋 SUMMARY:");
        console.log(
          "   The edit panel is currently sliding in from the right side."
        );
        console.log(
          "   For mobile devices (344x882), it should slide up from the bottom."
        );
      } else {
        console.log("⚠️ No edit button found on beats");
      }
    } else {
      console.log("⚠️ No beats found in sequence - cannot test edit panel");
    }
  });
});
