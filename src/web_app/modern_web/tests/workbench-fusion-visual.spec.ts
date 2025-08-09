import { test, expect } from '@playwright/test';

test.describe('Workbench Fusion Visual Tests', () => {
	test.beforeEach(async ({ page }) => {
		// Navigate to the application
		await page.goto('http://localhost:5175/');

		// Wait for the application to initialize
		await page.waitForSelector('[data-testid="main-application"]', { timeout: 15000 });

		// Wait for construct tab to be visible
		await expect(page.locator('[data-testid="construct-tab"]')).toBeVisible();
	});

	test('capture workbench fusion layout screenshot', async ({ page }) => {
		// Wait for workbench to be fully loaded
		const workbench = page.locator('.workbench');
		await expect(workbench).toBeVisible();

		// Wait for button panel to be visible
		const buttonPanel = page.locator('.button-panel');
		await expect(buttonPanel).toBeVisible();

		// Wait for beat frame to be visible
		const beatFrame = page.locator('.beat-frame-container');
		await expect(beatFrame).toBeVisible();

		// Take a screenshot of the entire workbench area
		await workbench.screenshot({ path: 'workbench-fusion-layout.png' });

		// Take a screenshot of the main application for context
		await page.screenshot({ path: 'workbench-fusion-full-app.png', fullPage: true });

		// Verify the fusion layout structure
		const mainLayout = page.locator('.main-layout');
		await expect(mainLayout).toBeVisible();

		// Check the layout has correct grid structure
		const layoutStyle = await mainLayout.evaluate((el) => {
			const style = window.getComputedStyle(el);
			return {
				display: style.display,
				gridTemplateColumns: style.gridTemplateColumns,
				gap: style.gap,
			};
		});

		console.log('Layout Style:', layoutStyle);
		expect(layoutStyle.display).toBe('grid');
		// Grid template columns should expand to actual pixel values
		expect(layoutStyle.gridTemplateColumns).toMatch(/^\d+px \d+px$/);
		expect(layoutStyle.gap).toBe('0px');

		// Verify button panel is positioned correctly within workbench
		const workbenchButtonPanel = page.locator('.workbench-button-panel');
		await expect(workbenchButtonPanel).toBeVisible();

		// Verify button panel contains all expected buttons
		const buttons = [
			'Add to Dictionary',
			'Fullscreen',
			'Mirror Sequence',
			'Swap Colors',
			'Rotate Sequence',
			'Copy JSON',
			'Delete Beat',
			'Clear Sequence',
		];

		for (const buttonTitle of buttons) {
			await expect(buttonPanel.locator(`button[title="${buttonTitle}"]`)).toBeVisible();
		}

		// Verify Delete Beat button is disabled (no selection)
		await expect(buttonPanel.locator('button[title="Delete Beat"]')).toBeDisabled();

		// Verify other buttons are enabled
		await expect(buttonPanel.locator('button[title="Clear Sequence"]')).toBeEnabled();
		await expect(buttonPanel.locator('button[title="Fullscreen"]')).toBeEnabled();
	});

	test('test button interactions and visual feedback', async ({ page }) => {
		const buttonPanel = page.locator('.button-panel');
		await expect(buttonPanel).toBeVisible();

		// Test hover effects on buttons
		const fullscreenBtn = buttonPanel.locator('button[title="Fullscreen"]');
		await fullscreenBtn.hover();

		// Take a screenshot showing button hover state
		await buttonPanel.screenshot({ path: 'button-panel-hover.png' });

		// Test button click (should show console log)
		await fullscreenBtn.click();

		// Test mirror button
		const mirrorBtn = buttonPanel.locator('button[title="Mirror Sequence"]');
		await mirrorBtn.click();

		// Test copy JSON button
		const copyJsonBtn = buttonPanel.locator('button[title="Copy JSON"]');
		await copyJsonBtn.click();

		// Take final screenshot after interactions
		await page.screenshot({ path: 'workbench-fusion-after-interactions.png' });
	});

	test('verify beat frame layout and start tile', async ({ page }) => {
		// Check for beat frame
		const beatFrameContainer = page.locator('.beat-frame-container');
		await expect(beatFrameContainer).toBeVisible();

		// Check for start tile
		const startTile = page.locator('.start-tile');
		await expect(startTile).toBeVisible();
		await expect(startTile.locator('.start-label')).toHaveText('START');

		// Take screenshot of beat frame area
		await beatFrameContainer.screenshot({ path: 'beat-frame-with-start-tile.png' });

		// Verify beat frame has minimal styling (legacy parity)
		const frameStyle = await beatFrameContainer.evaluate((el) => {
			const style = window.getComputedStyle(el);
			return {
				background: style.background,
				borderRadius: style.borderRadius,
				border: style.border,
				overflow: style.overflow,
			};
		});

		console.log('Beat Frame Style:', frameStyle);
		expect(frameStyle.background).toContain('transparent');
		expect(frameStyle.borderRadius).toBe('12px');
		expect(frameStyle.border).toContain('1px solid');
		expect(frameStyle.overflow).toBe('hidden');
	});

	test('verify sequence content label area', async ({ page }) => {
		// Check for sequence content
		const sequenceContainer = page.locator('.sequence-container');
		await expect(sequenceContainer).toBeVisible();

		// Check for current word label
		const currentWordLabel = page.locator('.current-word-label');
		await expect(currentWordLabel).toBeVisible();

		// Take screenshot of sequence content area
		await sequenceContainer.screenshot({ path: 'sequence-content-area.png' });

		// Verify label styling
		const labelStyle = await currentWordLabel.evaluate((el) => {
			const style = window.getComputedStyle(el);
			return {
				fontSize: style.fontSize,
				fontWeight: style.fontWeight,
				color: style.color,
				textAlign: style.textAlign,
				padding: style.padding,
			};
		});

		console.log('Label Style:', labelStyle);
		expect(labelStyle.fontSize).toBe('14px');
		expect(labelStyle.fontWeight).toBe('600');
		expect(labelStyle.textAlign).toBe('center');
	});
});
