/**
 * Simple Start Position Picker Test
 *
 * A basic test to check if both applications are running and compare
 * the 3 start position pictographs between legacy and modern versions.
 */

import { chromium } from 'playwright';

async function runSimpleTest() {
  console.log('🚀 Starting simple start position comparison test...');

  const browser = await chromium.launch({ headless: false });

  try {
    // Test legacy app
    console.log('\n📱 Testing Legacy App...');
    const legacyContext = await browser.newContext();
    const legacyPage = await legacyContext.newPage();

    try {
      await legacyPage.goto('http://localhost:5173', { timeout: 10000 });
      console.log('✅ Legacy app is accessible');

      // Look for start position picker
      const legacyStartPicker = await legacyPage.locator('.start-pos-picker, [data-component="start-position-picker"]').first();
      if (await legacyStartPicker.isVisible({ timeout: 5000 })) {
        console.log('✅ Legacy start position picker found');

        // Count pictographs
        const legacyPictographs = await legacyPage.locator('.pictograph-container, .pictograph-wrapper').count();
        console.log(`📊 Legacy pictographs found: ${legacyPictographs}`);

        // Take screenshot
        await legacyPage.screenshot({ path: './test-results/legacy-start-positions.png', fullPage: true });
        console.log('📸 Legacy screenshot saved');

      } else {
        console.log('⚠️ Legacy start position picker not found');
      }

    } catch (error) {
      console.log('❌ Legacy app error:', error.message);
    }

    await legacyContext.close();

    // Test modern app
    console.log('\n📱 Testing Modern App...');
    const modernContext = await browser.newContext();
    const modernPage = await modernContext.newPage();

    try {
      await modernPage.goto('http://localhost:5177', { timeout: 10000 });
      console.log('✅ Modern app is accessible');

      // Look for start position picker
      const modernStartPicker = await modernPage.locator('.start-pos-picker, [data-component="start-position-picker"]').first();
      if (await modernStartPicker.isVisible({ timeout: 5000 })) {
        console.log('✅ Modern start position picker found');

        // Count pictographs
        const modernPictographs = await modernPage.locator('.pictograph-container, .pictograph-wrapper').count();
        console.log(`📊 Modern pictographs found: ${modernPictographs}`);

        // Take screenshot
        await modernPage.screenshot({ path: './test-results/modern-start-positions.png', fullPage: true });
        console.log('📸 Modern screenshot saved');

      } else {
        console.log('⚠️ Modern start position picker not found');
      }

    } catch (error) {
      console.log('❌ Modern app error:', error.message);
    }

    await modernContext.close();

    // Simple coordinate extraction test
    console.log('\n🔍 Attempting coordinate extraction...');

    const testContext = await browser.newContext();
    const testPage = await testContext.newPage();

    try {
      await testPage.goto('http://localhost:5173');

      // Look for any props or positioning elements
      const props = await testPage.evaluate(() => {
        const propElements = document.querySelectorAll('[data-prop-color], .prop, circle[data-color]');
        const results = [];

        propElements.forEach((el, index) => {
          const rect = el.getBoundingClientRect();
          const transform = window.getComputedStyle(el).transform;
          const color = el.getAttribute('data-prop-color') || el.getAttribute('data-color') || 'unknown';

          results.push({
            index,
            color,
            x: rect.x,
            y: rect.y,
            width: rect.width,
            height: rect.height,
            transform
          });
        });

        return results;
      });

      console.log('📍 Found props:', props.length);
      props.forEach(prop => {
        console.log(`   ${prop.color}: (${prop.x.toFixed(1)}, ${prop.y.toFixed(1)})`);
      });

    } catch (error) {
      console.log('❌ Coordinate extraction error:', error.message);
    }

    await testContext.close();

  } finally {
    await browser.close();
  }

  console.log('\n✅ Simple test completed');
}

// Create test-results directory if it doesn't exist
import fs from 'fs';
if (!fs.existsSync('./test-results')) {
  fs.mkdirSync('./test-results', { recursive: true });
}

// Run the test
runSimpleTest().catch(console.error);
