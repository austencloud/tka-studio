import { test } from '@playwright/test';

test('Browse Tab - Manual Navigation Debug', async ({ page }) => {
	// Enable console logging
	page.on('console', (msg) => {
		if (msg.type() === 'log' || msg.type() === 'warning' || msg.type() === 'error') {
			console.log(`[${msg.type().toUpperCase()}] ${msg.text()}`);
		}
	});

	// Navigate to the browse tab
	await page.goto('/');

	// Wait for the page to load
	await page.waitForTimeout(3000);

	// Click browse tab
	await page.click('button:has-text("Browse")');

	// Wait for browse tab to load
	await page.waitForTimeout(2000);

	// Take screenshot to see what's currently visible
	await page.screenshot({ path: 'manual-debug-browse.png', fullPage: true });

	// Get the text content of the browse tab to see what's rendered
	const browseTabContent = await page.locator('.browse-tab').textContent();
	console.log('Browse tab content:', browseTabContent);

	// Check if SequenceBrowserPanel is rendered
	const browserPanel = await page.locator('.sequence-browser-panel').count();
	console.log('SequenceBrowserPanel elements found:', browserPanel);

	// Click "All Sequences" if possible
	const allSequencesButton = await page.locator('button:has-text("📊 All Sequences")').count();
	console.log('All Sequences button found:', allSequencesButton);

	if (allSequencesButton > 0) {
		await page.click('button:has-text("📊 All Sequences")');
		await page.waitForTimeout(2000);

		// Take another screenshot after clicking
		await page.screenshot({ path: 'manual-debug-after-click.png', fullPage: true });

		// Check what's in the browser panel now
		const afterClickContent = await page.locator('.sequence-browser-panel').textContent();
		console.log('Browser panel content after click:', afterClickContent);
	}
});
