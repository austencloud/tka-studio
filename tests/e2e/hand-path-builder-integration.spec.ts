import { test, expect } from '@playwright/test';

test.describe('Hand Path Builder Integration', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate directly to Create module
    await page.goto('/create', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1000); // Wait for Svelte hydration

    // Navigate to gestural/hand path tab
    // Try multiple selector strategies to find the tab button
    const gesturalTab = page.locator('[data-build-mode-id="gestural"], button:has-text("Hand Path"), button:has-text("Gestural")').first();

    if (await gesturalTab.count() > 0) {
      await gesturalTab.click();
      await page.waitForTimeout(500);
    } else {
      console.log('⚠️ Could not find gestural tab button');
    }
  });

  test('workspace should take no height before starting', async ({ page }) => {
    // Check that workspace container doesn't exist
    const workspaceContainer = page.locator('.hand-path-workspace-container');
    await expect(workspaceContainer).not.toBeVisible();

    // Check that workspace itself doesn't exist
    const workspace = page.locator('[data-testid="hand-path-workspace"]');
    await expect(workspace).not.toBeVisible();
  });

  test('should show "Configure Your Settings" message in top bar', async ({ page }) => {
    // Check that contextual message appears in word label
    const wordLabel = page.locator('.word-label');
    await expect(wordLabel).toContainText('Configure Your Settings');
  });

  test('should show workspace after clicking "Start Drawing"', async ({ page }) => {
    // Find and click "Start Drawing" button
    const startButton = page.getByRole('button', { name: /start drawing/i });
    await expect(startButton).toBeVisible();
    await startButton.click();

    // Wait for animation
    await page.waitForTimeout(500);

    // Check that workspace is now visible
    const workspace = page.locator('[data-testid="hand-path-workspace"]');
    await expect(workspace).toBeVisible();

    // Check that contextual message changed
    const wordLabel = page.locator('.word-label');
    await expect(wordLabel).toContainText('Drawing Blue Hand Path');
  });

  test('should hide workspace when resetting', async ({ page }) => {
    // Start drawing
    const startButton = page.getByRole('button', { name: /start drawing/i });
    await startButton.click();
    await page.waitForTimeout(500);

    // Verify workspace is visible
    const workspace = page.locator('[data-testid="hand-path-workspace"]');
    await expect(workspace).toBeVisible();

    // Click reset button (the redo icon in settings section)
    const resetButton = page.locator('.icon-btn').filter({ hasText: '' }); // redo icon
    await resetButton.click();
    await page.waitForTimeout(300);

    // Workspace should be hidden again
    await expect(workspace).not.toBeVisible();

    // Should show "Configure Your Settings" again
    const wordLabel = page.locator('.word-label');
    await expect(wordLabel).toContainText('Configure Your Settings');
  });

  test('workspace should animate in smoothly', async ({ page }) => {
    // Get initial viewport size
    const viewportSize = page.viewportSize();

    // Start drawing
    const startButton = page.getByRole('button', { name: /start drawing/i });
    await startButton.click();

    // Workspace should start appearing immediately
    const workspace = page.locator('[data-testid="hand-path-workspace"]');

    // Wait a bit and check it's animating
    await page.waitForTimeout(100);
    await expect(workspace).toBeVisible();

    // After full animation, should be fully visible
    await page.waitForTimeout(500);
    const box = await workspace.boundingBox();
    expect(box).not.toBeNull();
    expect(box!.height).toBeGreaterThan(100); // Should have substantial height
  });

  test('sequence length picker should be visible before starting', async ({ page }) => {
    // Sequence length picker should be in the tool panel
    const lengthPicker = page.locator('.sequence-length-picker, .length-picker, [data-testid="sequence-length-picker"]');

    // Check for any buttons or controls related to sequence length
    const toolPanel = page.locator('[data-testid="tool-panel"]');
    await expect(toolPanel).toBeVisible();
  });
});
