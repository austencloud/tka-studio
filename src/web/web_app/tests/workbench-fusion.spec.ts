import { expect, test } from '@playwright/test';

test.describe('Workbench Fusion Tests', () => {
	test.beforeEach(async ({ page }) => {
		// Navigate to the application
		await page.goto('http://localhost:5175/');

		// Wait for the application to initialize
		await page.waitForSelector('[data-testid="main-application"]', { timeout: 15000 });

		// Wait for construct tab to be visible
		await expect(page.locator('[data-testid="construct-tab"]')).toBeVisible();
	});

	test('workbench has correct fusion layout', async ({ page }) => {
		// Check that workbench components exist
		const workbench = page.locator('.workbench');
		await expect(workbench).toBeVisible();

		// Check for the new grid layout structure
		const mainLayout = page.locator('.main-layout');
		await expect(mainLayout).toBeVisible();

		// Verify left side has sequence content
		const leftVbox = page.locator('.left-vbox');
		await expect(leftVbox).toBeVisible();

		// Verify right side has button panel (inside workbench)
		const workbenchButtonPanel = page.locator('.workbench-button-panel');
		await expect(workbenchButtonPanel).toBeVisible();

		// Check that button panel is inside the workbench (not in separate right panel)
		const buttonPanel = page.locator('.button-panel');
		await expect(buttonPanel).toBeVisible();

		// Verify button panel contains expected buttons
		await expect(buttonPanel.locator('button[title="Add to Dictionary"]')).toBeVisible();
		await expect(buttonPanel.locator('button[title="Fullscreen"]')).toBeVisible();
		await expect(buttonPanel.locator('button[title="Mirror Sequence"]')).toBeVisible();
		await expect(buttonPanel.locator('button[title="Swap Colors"]')).toBeVisible();
		await expect(buttonPanel.locator('button[title="Rotate Sequence"]')).toBeVisible();
		await expect(buttonPanel.locator('button[title="Copy JSON"]')).toBeVisible();
		await expect(buttonPanel.locator('button[title="Delete Beat"]')).toBeVisible();
		await expect(buttonPanel.locator('button[title="Clear Sequence"]')).toBeVisible();
	});

	test('sequence content displays correctly', async ({ page }) => {
		// Check for sequence content wrapper
		const sequenceContainer = page.locator('.sequence-container');
		await expect(sequenceContainer).toBeVisible();

		// Check for label area
		const currentWordLabel = page.locator('.current-word-label');
		await expect(currentWordLabel).toBeVisible();

		// Check for beat frame wrapper
		const beatFrameWrapper = page.locator('.beat-frame-wrapper');
		await expect(beatFrameWrapper).toBeVisible();

		// Check for beat frame container
		const beatFrameContainer = page.locator('.beat-frame-container');
		await expect(beatFrameContainer).toBeVisible();
	});

	test('beat frame shows start tile when no sequence loaded', async ({ page }) => {
		// Look for start tile
		const startTile = page.locator('.start-tile');
		await expect(startTile).toBeVisible();

		// Verify start tile text
		await expect(startTile.locator('.start-label')).toHaveText('START');
	});

	test('button panel interactions work', async ({ page }) => {
		const buttonPanel = page.locator('.button-panel');

		// Test that delete beat button is initially disabled (no selection)
		const deleteBeatBtn = buttonPanel.locator('button[title="Delete Beat"]');
		await expect(deleteBeatBtn).toBeDisabled();

		// Test that other buttons are enabled
		const clearSequenceBtn = buttonPanel.locator('button[title="Clear Sequence"]');
		await expect(clearSequenceBtn).toBeEnabled();

		const fullscreenBtn = buttonPanel.locator('button[title="Fullscreen"]');
		await expect(fullscreenBtn).toBeEnabled();
	});

	test('button panel visual styling matches legacy', async ({ page }) => {
		const buttonPanel = page.locator('.button-panel');

		// Check layout is vertical column
		const computedStyle = await buttonPanel.evaluate((el) => {
			const style = window.getComputedStyle(el);
			return {
				display: style.display,
				flexDirection: style.flexDirection,
				alignItems: style.alignItems,
				gap: style.gap,
			};
		});

		expect(computedStyle.display).toBe('flex');
		expect(computedStyle.flexDirection).toBe('column');
		expect(computedStyle.alignItems).toBe('center');

		// Check button styling
		const firstButton = buttonPanel.locator('button').first();
		const buttonStyle = await firstButton.evaluate((el) => {
			const style = window.getComputedStyle(el);
			return {
				width: style.width,
				height: style.height,
				borderRadius: style.borderRadius,
				display: style.display,
				alignItems: style.alignItems,
				justifyContent: style.justifyContent,
			};
		});

		expect(buttonStyle.width).toBe('48px');
		expect(buttonStyle.height).toBe('48px');
		expect(buttonStyle.borderRadius).toBe('10px');
		expect(buttonStyle.display).toBe('flex');
		expect(buttonStyle.alignItems).toBe('center');
		expect(buttonStyle.justifyContent).toBe('center');
	});

	test('beat view styling matches legacy (minimal design)', async ({ page }) => {
		// Look for any beat views that might be rendered
		const beatViews = page.locator('.beat-view');

		if ((await beatViews.count()) > 0) {
			const firstBeat = beatViews.first();

			// Check for minimal border styling (no heavy shadows/gradients)
			const beatStyle = await firstBeat.evaluate((el) => {
				const style = window.getComputedStyle(el);
				return {
					border: style.border,
					borderRadius: style.borderRadius,
					background: style.background,
					boxShadow: style.boxShadow,
					transition: style.transition,
				};
			});

			// Verify minimal styling approach
			expect(beatStyle.border).toContain('1px solid');
			expect(beatStyle.borderRadius).toBe('6px');
			expect(beatStyle.background).not.toContain('gradient'); // No gradients

			// Should not have heavy box shadows (minimal design)
			if (beatStyle.boxShadow && beatStyle.boxShadow !== 'none') {
				expect(beatStyle.boxShadow).not.toContain('8px'); // No heavy shadows
			}
		}
	});

	test('workbench layout is responsive', async ({ page }) => {
		// Test different viewport sizes
		await page.setViewportSize({ width: 1200, height: 800 });

		const mainLayout = page.locator('.main-layout');
		await expect(mainLayout).toBeVisible();

		// Check that grid layout is maintained
		const layoutStyle = await mainLayout.evaluate((el) => {
			const style = window.getComputedStyle(el);
			return {
				display: style.display,
				gridTemplateColumns: style.gridTemplateColumns,
				width: style.width,
				height: style.height,
			};
		});

		expect(layoutStyle.display).toBe('grid');
		expect(layoutStyle.gridTemplateColumns).toContain('1fr auto'); // Left fills, right auto
		expect(layoutStyle.width).toBe('100%');
		expect(layoutStyle.height).toBe('100%');

		// Test smaller viewport
		await page.setViewportSize({ width: 800, height: 600 });
		await expect(mainLayout).toBeVisible();

		// Button panel should still be visible and functional
		const buttonPanel = page.locator('.workbench-button-panel .button-panel');
		await expect(buttonPanel).toBeVisible();
	});

	test('scroll mode activates correctly', async ({ page }) => {
		// This test would require a sequence with many beats to trigger scroll mode
		// For now, just verify the CSS classes exist for scroll mode
		const beatFrameContainer = page.locator('.beat-frame-container');
		await expect(beatFrameContainer).toBeVisible();

		// Check that scroll mode classes are available in CSS
		const hasScrollableClass = await page.evaluate(() => {
			const style = document.createElement('style');
			document.head.appendChild(style);

			// Look for scrollable-active class in stylesheets
			for (let i = 0; i < document.styleSheets.length; i++) {
				try {
					const styleSheet = document.styleSheets[i];
					const rules = styleSheet?.cssRules || styleSheet?.rules;
					if (rules) {
						for (let j = 0; j < rules.length; j++) {
							const rule = rules[j] as any;
							if (
								rule.selectorText &&
								rule.selectorText.includes('scrollable-active')
							) {
								return true;
							}
						}
					}
				} catch (e) {
					// Cross-origin or other access issues
				}
			}
			return false;
		});

		expect(hasScrollableClass).toBeTruthy();
	});
});
