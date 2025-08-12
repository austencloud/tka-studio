import { expect, test } from '@playwright/test';

test.describe('Browse Tab - All Sequences Filter Debug', () => {
	test('should show sequences when All Sequences filter is selected', async ({ page }) => {
		// Enable console logging
		page.on('console', (msg) => {
			if (msg.type() === 'log' || msg.type() === 'warning' || msg.type() === 'error') {
				console.log(`[${msg.type().toUpperCase()}] ${msg.text()}`);
			}
		});

		// Navigate to the browse tab
		await page.goto('/');
		await page.click('button:has-text("Browse")');

		// Wait for the browse tab to load
		await page.waitForSelector('.browse-tab');

		// Check if sequence-index.json loads successfully
		const response = await page.request.get('/sequence-index.json');
		expect(response.status()).toBe(200);

		const sequenceIndex = await response.json();
		console.log('Sequence index contains:', sequenceIndex.totalSequences, 'sequences');
		expect(sequenceIndex.sequences).toHaveLength(3);

		// Click "All Sequences" in quick access
		await page.click('button:has-text("📊 All Sequences")');

		// Wait a bit for the filter to be applied
		await page.waitForTimeout(2000);

		// Check if sequences are displayed
		const sequenceElements = await page
			.locator('.sequence-item, .sequence-card, .thumbnail')
			.count();
		console.log('Found sequence elements:', sequenceElements);

		// Check for "no sequences found" message
		const noSequencesText = await page.locator('text="No sequences found"').count();
		console.log('No sequences found messages:', noSequencesText);

		// If no sequences are shown, take a screenshot for debugging
		if (sequenceElements === 0 || noSequencesText > 0) {
			await page.screenshot({ path: 'debug-browse-tab.png', fullPage: true });
			console.log('Screenshot saved as debug-browse-tab.png');
		}

		// The test should pass if sequences are found
		expect(sequenceElements).toBeGreaterThan(0);
		expect(noSequencesText).toBe(0);
	});

	test('should load sequence data correctly from service', async ({ page }) => {
		// Test the service directly through the page context
		await page.goto('/');

		const sequenceData = await page.evaluate(async () => {
			// Access the browse service through the window (if exposed for debugging)
			// or create a new instance to test

			// Test fetch to sequence-index.json
			const response = await fetch('/sequence-index.json');
			const data = await response.json();

			return {
				fetchSuccess: response.ok,
				totalSequences: data.totalSequences,
				sequencesLength: data.sequences?.length || 0,
				firstSequence: data.sequences?.[0] || null,
			};
		});

		console.log('Service test results:', sequenceData);

		expect(sequenceData.fetchSuccess).toBe(true);
		expect(sequenceData.totalSequences).toBe(3);
		expect(sequenceData.sequencesLength).toBe(3);
		expect(sequenceData.firstSequence).not.toBeNull();
	});
});
