// @ts-nocheck
const puppeteer = require('puppeteer');

async function testOptionPicker() {
	console.log('🚀 Starting OptionPicker test...');

	let browser;
	try {
		// Use the Chrome we just installed
		browser = await puppeteer.launch({
			headless: false, // Show browser for better debugging
			args: ['--no-sandbox', '--disable-setuid-sandbox'],
		});

		const page = await browser.newPage();

		// Enable console logging from the browser
		page.on('console', (msg) => {
			console.log('BROWSER:', msg.text());
		});

		console.log('📱 Navigating to test page...');
		await page.goto('http://localhost:5174/test-option-flow', {
			waitUntil: 'networkidle0',
			timeout: 30000,
		});

		console.log('⏱️ Waiting for page to load...');
		await page.waitForTimeout(3000);

		// Take screenshot of initial state
		console.log('📸 Taking initial screenshot...');
		await page.screenshot({ path: 'initial-state.png' });

		// Look for start position buttons
		console.log('🔍 Looking for start position buttons...');
		const startPositionButtons = await page.$$('[data-testid*="start-position"]');
		console.log(`Found ${startPositionButtons.length} start position buttons`);

		if (startPositionButtons.length > 0) {
			console.log('✅ Clicking first start position (Alpha)...');
			await startPositionButtons[0].click();

			// Wait for options to load
			console.log('⏱️ Waiting for options to load...');
			await page.waitForTimeout(2000);

			// Check if options are visible
			const optionElements = await page.$$('[data-testid*="option"]');
			console.log(`📋 Found ${optionElements.length} option elements`);

			// Take screenshot after clicking
			await page.screenshot({ path: 'after-click.png' });

			if (optionElements.length > 0) {
				console.log('🎉 SUCCESS: Options are loading correctly!');

				// Get the text content of first few options
				for (let i = 0; i < Math.min(3, optionElements.length); i++) {
					const optionText = await optionElements[i].textContent();
					console.log(`📝 Option ${i + 1}: ${optionText}`);
				}
			} else {
				console.log('❌ FAILURE: No options found after clicking start position');
			}
		} else {
			console.log('❌ FAILURE: No start position buttons found');
		}

		// Let's also check the console for any error messages
		await page.evaluate(() => {
			return window.console._logs || [];
		});

		console.log('📋 Final test report:');
		console.log(`- Start position buttons: ${startPositionButtons.length}`);
		console.log(
			`- Option elements after click: ${(await page.$$('[data-testid*="option"]')).length}`
		);
	} catch (error) {
		console.error('❌ Test failed:', error.message);
	} finally {
		if (browser) {
			await browser.close();
		}
	}
}

testOptionPicker();
