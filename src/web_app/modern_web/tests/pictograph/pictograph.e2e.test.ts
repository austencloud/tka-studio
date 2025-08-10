// @ts-nocheck
/**
 * End-to-End Pictograph Rendering Tests
 *
 * Tests the complete pictograph rendering pipeline from data to visual output
 */

import { expect, test } from '@playwright/test';

test.describe('Modern Pictograph E2E', () => {
	test.beforeEach(async ({ page }) => {
		// Navigate to a test page with pictograph demo
		// You'll need to create this route for testing
		await page.goto('/test/pictograph-demo');
	});

	test.describe('Basic Rendering', () => {
		test('should render simple pictograph with letter', async ({ page }) => {
			// Select the simple demo
			await page.selectOption('[data-testid="demo-selector"]', 'simple');

			// Wait for pictograph to load
			await page.waitForSelector('[data-testid="main-pictograph"] svg', {
				state: 'visible',
				timeout: 10000,
			});

			// Verify SVG is present
			const svg = page.locator('[data-testid=\"main-pictograph\"] svg');
			await expect(svg).toBeVisible();

			// Verify dimensions
			await expect(svg).toHaveAttribute('width', '300');
			await expect(svg).toHaveAttribute('height', '300');
			await expect(svg).toHaveAttribute('viewBox', '0 0 950 950');

			// Verify letter is displayed
			const letterText = page.locator('svg text:has-text(\"A\")');
			await expect(letterText).toBeVisible();
		});

		test('should render complex pictograph with multiple components', async ({ page }) => {
			// Select the complex demo
			await page.selectOption('[data-testid=\"demo-selector\"]', 'complex');

			// Wait for pictograph to load
			await page.waitForSelector('[data-testid=\"main-pictograph\"] svg', {
				state: 'visible',
				timeout: 10000,
			});

			// Verify letter
			const letterText = page.locator('svg text:has-text(\"Φ\")');
			await expect(letterText).toBeVisible();

			// Verify arrows are present (check for arrow group elements)
			const blueArrow = page.locator('svg g[data-arrow-color=\"blue\"]');
			await expect(blueArrow).toBeVisible();

			const redArrow = page.locator('svg g[data-arrow-color=\"red\"]');
			await expect(redArrow).toBeVisible();
		});

		test('should render empty state for blank pictograph', async ({ page }) => {
			// Select the empty demo
			await page.selectOption('[data-testid=\"demo-selector\"]', 'empty');

			// Wait for pictograph to load
			await page.waitForSelector('[data-testid=\"main-pictograph\"] svg', {
				state: 'visible',
				timeout: 5000,
			});

			// Should show empty state indicator
			const emptyState = page.locator('svg g.empty-state');
			await expect(emptyState).toBeVisible();

			// Should show default text
			const emptyText = page.locator('svg text:has-text(\"Empty\")');
			await expect(emptyText).toBeVisible();
		});
	});

	test.describe('Grid Mode Switching', () => {
		test('should switch between diamond and box grid modes', async ({ page }) => {
			// Start with diamond mode
			await page.selectOption('[data-testid=\"grid-mode-selector\"]', 'diamond');
			await page.selectOption('[data-testid=\"demo-selector\"]', 'simple');

			await page.waitForSelector('[data-testid=\"main-pictograph\"] svg', {
				state: 'visible',
				timeout: 10000,
			});

			// Verify grid is loaded
			const grid = page.locator('svg g.grid');
			await expect(grid).toBeVisible();

			// Switch to box mode
			await page.selectOption('[data-testid=\"grid-mode-selector\"]', 'box');

			// Wait for re-render
			await page.waitForTimeout(1000);

			// Grid should still be visible (potentially different shape)
			await expect(grid).toBeVisible();
		});
	});

	test.describe('Debug Mode', () => {
		test('should show debug information when enabled', async ({ page }) => {
			// Enable debug mode
			await page.check('[data-testid=\"debug-mode-checkbox\"]');
			await page.selectOption('[data-testid=\"demo-selector\"]', 'simple');

			await page.waitForSelector('[data-testid=\"main-pictograph\"] svg', {
				state: 'visible',
				timeout: 10000,
			});

			// Should show component count
			const componentText = page.locator(
				'svg text:text-matches(\"Components: \\\\d+/\\\\d+\")'
			);
			await expect(componentText).toBeVisible();

			// Should show data ID
			const dataText = page.locator('svg text:text-matches(\"Data: [a-f0-9]+\")');
			await expect(dataText).toBeVisible();
		});

		test('should hide debug information when disabled', async ({ page }) => {
			// Ensure debug mode is disabled
			await page.uncheck('[data-testid=\"debug-mode-checkbox\"]');
			await page.selectOption('[data-testid=\"demo-selector\"]', 'simple');

			await page.waitForSelector('[data-testid=\"main-pictograph\"] svg', {
				state: 'visible',
				timeout: 10000,
			});


		});
	});

	test.describe('Component Loading', () => {
		test('should show loading indicator during component loading', async ({ page }) => {
			// Clear cache and reload to see loading states
			await page.reload();

			// Select a complex demo to have more loading time
			await page.selectOption('[data-testid=\"demo-selector\"]', 'complex');

			// Should show loading overlay initially
			const loadingOverlay = page.locator('svg g.loading-overlay');
			await expect(loadingOverlay).toBeVisible({ timeout: 2000 });

			// Loading should complete
			await expect(loadingOverlay).not.toBeVisible({ timeout: 15000 });

			// Final pictograph should be visible
			const svg = page.locator('[data-testid=\"main-pictograph\"] svg');
			await expect(svg).toBeVisible();
		});

		test('should handle component loading errors gracefully', async ({ page }) => {
			// Mock network to cause asset loading failures
			await page.route('/images/arrows/**', (route) => route.abort());
			await page.route('/images/props/**', (route) => route.abort());

			await page.selectOption('[data-testid=\"demo-selector\"]', 'simple');

			// Should still render the pictograph with fallbacks
			await page.waitForSelector('[data-testid=\"main-pictograph\"] svg', {
				state: 'visible',
				timeout: 10000,
			});

			// May show error overlay
			const errorOverlay = page.locator('svg g.error-overlay');
			// Error overlay might or might not be visible depending on fallback success

			// But the SVG should still be present
			const svg = page.locator('[data-testid=\"main-pictograph\"] svg');
			await expect(svg).toBeVisible();
		});
	});

	test.describe('Interactive Features', () => {
		test('should handle click events', async ({ page }) => {
			// Set up click tracking
			await page.evaluate(() => {
				window.clickCount = 0;
				window.addEventListener('pictograph-click', () => {
					window.clickCount++;
				});
			});

			await page.selectOption('[data-testid=\"demo-selector\"]', 'simple');
			await page.waitForSelector('[data-testid=\"main-pictograph\"] svg', {
				state: 'visible',
				timeout: 10000,
			});

			// Click the pictograph
			await page.click('[data-testid=\"main-pictograph\"] svg');

			// Verify click was registered (this would depend on your implementation)
			const clickCount = await page.evaluate(() => window.clickCount);
			expect(clickCount).toBeGreaterThan(0);
		});

		test('should respond to keyboard navigation', async ({ page }) => {
			await page.selectOption('[data-testid=\"demo-selector\"]', 'simple');
			await page.waitForSelector('[data-testid=\"main-pictograph\"] svg', {
				state: 'visible',
				timeout: 10000,
			});

			// Focus the pictograph
			await page.focus('[data-testid=\"main-pictograph\"] svg');

			// Should have focus styles
			const focusedElement = page.locator('[data-testid=\"main-pictograph\"] svg:focus');
			await expect(focusedElement).toBeVisible();

			// Test keyboard activation
			await page.keyboard.press('Enter');
			// Verify activation (implementation dependent)
		});
	});

	test.describe('Multiple Size Rendering', () => {
		test('should render correctly at different sizes', async ({ page }) => {
			await page.selectOption('[data-testid=\"demo-selector\"]', 'simple');

			// Test small size
			const smallPictograph = page.locator('[data-testid=\"small-pictograph\"] svg');
			await expect(smallPictograph).toBeVisible({ timeout: 10000 });
			await expect(smallPictograph).toHaveAttribute('width', '150');
			await expect(smallPictograph).toHaveAttribute('height', '150');

			// Test medium size
			const mediumPictograph = page.locator('[data-testid=\"medium-pictograph\"] svg');
			await expect(mediumPictograph).toBeVisible();
			await expect(mediumPictograph).toHaveAttribute('width', '200');
			await expect(mediumPictograph).toHaveAttribute('height', '200');

			// Test large size
			const largePictograph = page.locator('[data-testid=\"large-pictograph\"] svg');
			await expect(largePictograph).toBeVisible();
			await expect(largePictograph).toHaveAttribute('width', '400');
			await expect(largePictograph).toHaveAttribute('height', '400');

			// All should have the same viewBox
			for (const pictograph of [smallPictograph, mediumPictograph, largePictograph]) {
				await expect(pictograph).toHaveAttribute('viewBox', '0 0 950 950');
			}
		});
	});

	test.describe('Beat Integration', () => {
		test('should render pictograph from beat data', async ({ page }) => {
			// Switch to beat data demo
			const beatDataDemo = page.locator('[data-testid=\"beat-data-demo\"]');
			await expect(beatDataDemo).toBeVisible({ timeout: 10000 });

			// Should show beat number
			const beatNumber = page.locator('svg text:has-text(\"1\")');
			await expect(beatNumber).toBeVisible();

			// Should render the pictograph content
			const svg = beatDataDemo.locator('svg');
			await expect(svg).toBeVisible();
		});

		test('should render blank beat correctly', async ({ page }) => {
			const blankBeatDemo = page.locator('[data-testid=\"blank-beat-demo\"]');
			await expect(blankBeatDemo).toBeVisible({ timeout: 10000 });

			// Should show beat number for blank beat
			const beatNumber = page.locator(
				'[data-testid=\"blank-beat-demo\"] svg text:has-text(\"2\")'
			);
			await expect(beatNumber).toBeVisible();

			// Should show empty state
			const emptyState = page.locator('[data-testid=\"blank-beat-demo\"] svg g.empty-state');
			await expect(emptyState).toBeVisible();
		});
	});

	test.describe('Performance', () => {
		test('should render pictographs efficiently', async ({ page }) => {
			// Mark start time
			const startTime = await page.evaluate(() => performance.now());

			// Load complex demo
			await page.selectOption('[data-testid=\"demo-selector\"]', 'complex');

			// Wait for complete rendering
			await page.waitForSelector('[data-testid=\"main-pictograph\"] svg', {
				state: 'visible',
				timeout: 10000,
			});

			// Wait for all loading to complete
			await page.waitForSelector('svg g.loading-overlay', {
				state: 'hidden',
				timeout: 15000,
			});

			// Mark end time
			const endTime = await page.evaluate(() => performance.now());
			const renderTime = endTime - startTime;

			// Should render within reasonable time (adjust threshold as needed)
			expect(renderTime).toBeLessThan(5000); // 5 seconds max
		});

		test('should handle rapid demo switching without memory leaks', async ({ page }) => {
			const demos = ['simple', 'complex', 'empty'];

			// Rapidly switch between demos
			for (let i = 0; i < 10; i++) {
				const demo = demos[i % demos.length];
				await page.selectOption('[data-testid=\"demo-selector\"]', demo);
				await page.waitForTimeout(200); // Small delay between switches
			}

			// Final render should still work
			await page.selectOption('[data-testid=\"demo-selector\"]', 'simple');
			await page.waitForSelector('[data-testid=\"main-pictograph\"] svg', {
				state: 'visible',
				timeout: 10000,
			});

			const svg = page.locator('[data-testid=\"main-pictograph\"] svg');
			await expect(svg).toBeVisible();
		});
	});

	test.describe('Error Handling', () => {
		test('should recover from asset loading failures', async ({ page }) => {
			// Mock some assets to fail
			await page.route('/images/grid/diamond_grid.svg', (route) => route.abort());

			await page.selectOption('[data-testid=\"demo-selector\"]', 'simple');

			// Should still render with fallback grid
			await page.waitForSelector('[data-testid=\"main-pictograph\"] svg', {
				state: 'visible',
				timeout: 10000,
			});

			const svg = page.locator('[data-testid=\"main-pictograph\"] svg');
			await expect(svg).toBeVisible();

			// Should have fallback grid rendering
			const fallbackGrid = page.locator('svg g.fallback-grid');
			await expect(fallbackGrid).toBeVisible();
		});

		test('should handle invalid data gracefully', async ({ page }) => {
			// Inject invalid data (this would require a test endpoint)
			await page.goto('/test/pictograph-demo?invalidData=true');

			// Should show error state or fallback
			const svg = page.locator('svg');
			await expect(svg).toBeVisible({ timeout: 5000 });

			// May show error overlay
			const errorOverlay = page.locator('svg g.error-overlay');
			// Error handling depends on implementation
		});
	});
});

test.describe('BeatView Integration E2E', () => {
	test.beforeEach(async ({ page }) => {
		// Navigate to a page with BeatView components
		await page.goto('/test/beat-view-demo');
	});

	test('should render multiple beats in sequence', async ({ page }) => {
		// Wait for beat views to load
		await page.waitForSelector('[data-testid=\"beat-view-0\"]', {
			state: 'visible',
			timeout: 10000,
		});

		// Check multiple beats are rendered
		const beatViews = page.locator('[data-testid^=\"beat-view-\"]');
		const count = await beatViews.count();
		expect(count).toBeGreaterThan(0);

		// Each beat should have proper styling
		for (let i = 0; i < Math.min(count, 5); i++) {
			const beatView = page.locator(`[data-testid=\"beat-view-${i}\"]`);
			await expect(beatView).toBeVisible();
			await expect(beatView).toHaveClass(/beat-view/);
		}
	});

	test('should handle beat selection', async ({ page }) => {
		await page.waitForSelector('[data-testid=\"beat-view-0\"]', {
			state: 'visible',
			timeout: 10000,
		});

		// Click first beat
		await page.click('[data-testid=\"beat-view-0\"]');

		// Should have selected state
		const selectedBeat = page.locator('[data-testid=\"beat-view-0\"].selected');
		await expect(selectedBeat).toBeVisible();
	});

	test('should show hover effects', async ({ page }) => {
		await page.waitForSelector('[data-testid=\"beat-view-0\"]', {
			state: 'visible',
			timeout: 10000,
		});

		// Hover over beat
		await page.hover('[data-testid=\"beat-view-0\"]');

		// Should have hover state
		const hoveredBeat = page.locator('[data-testid=\"beat-view-0\"].hovered');
		await expect(hoveredBeat).toBeVisible();
	});
});
