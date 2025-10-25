/**
 * Direct Background Change Test
 *
 * Tests the background change mechanism by directly calling the update functions
 * in the browser console, bypassing the UI.
 */

import { expect, test } from '@playwright/test';

test.describe('Direct Background Change Test', () => {
  test('should change background when directly calling updateBodyBackground', async ({ page }) => {
    // Capture console logs
    const logs: string[] = [];
    page.on('console', (msg) => {
      const text = msg.text();
      logs.push(text);
      if (
        text.includes('updateBodyBackground') ||
        text.includes('🎨') ||
        text.includes('🔍') ||
        text.includes('✅')
      ) {
        console.log('[APP]', text);
      }
    });

    console.log('\n🔬 TEST: Direct background update via browser console\n');

    // Navigate to the app
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);

    console.log('1️⃣ Getting initial background state...');
    const initialState = await page.evaluate(() => {
      return {
        gradientCosmic: document.documentElement.style.getPropertyValue('--gradient-cosmic'),
        gradientNext: document.documentElement.style.getPropertyValue('--gradient-next'),
        bodyClasses: document.body.className,
      };
    });

    console.log('   Initial --gradient-cosmic:', initialState.gradientCosmic || 'none');
    console.log('   Initial body classes:', initialState.bodyClasses);

    console.log('\n2️⃣ Importing and calling updateBodyBackground directly...');

    // Import the background module and call updateBodyBackground directly
    const result = await page.evaluate(async () => {
      try {
        // Import the module
        const { updateBodyBackground, BackgroundType } = await import('$lib/shared/background');

        console.log('🧪 TEST: Successfully imported background module');
        console.log('🧪 TEST: Available BackgroundType values:', Object.keys(BackgroundType));

        // Call updateBodyBackground with Aurora
        console.log('🧪 TEST: Calling updateBodyBackground with AURORA');
        updateBodyBackground(BackgroundType.AURORA);

        // Return success
        return {
          success: true,
          backgroundType: BackgroundType.AURORA,
        };
      } catch (error) {
        console.error('🧪 TEST ERROR:', error);
        return {
          success: false,
          error: error instanceof Error ? error.message : String(error),
        };
      }
    });

    console.log('   Import result:', result);

    if (!result.success) {
      console.log('   ❌ Failed to import/call updateBodyBackground');
      console.log('   Error:', result.error);
      throw new Error(`Failed to call updateBodyBackground: ${result.error}`);
    }

    console.log('\n3️⃣ Waiting for transition...');
    await page.waitForTimeout(2000);

    console.log('\n4️⃣ Checking final state...');
    const finalState = await page.evaluate(() => {
      return {
        gradientCosmic: document.documentElement.style.getPropertyValue('--gradient-cosmic'),
        gradientNext: document.documentElement.style.getPropertyValue('--gradient-next'),
        bodyClasses: document.body.className,
        bodyHasTransitioningClass: document.body.classList.contains('background-transitioning'),
      };
    });

    console.log('   Final --gradient-cosmic:', finalState.gradientCosmic || 'none');
    console.log('   Final --gradient-next:', finalState.gradientNext || 'none');
    console.log('   Final body classes:', finalState.bodyClasses);
    console.log('   Has transitioning class:', finalState.bodyHasTransitioningClass);

    console.log('\n5️⃣ Analyzing results...');
    console.log('   ════════════════════════════════════════════════════════════');

    const auroraGradient = 'linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%)';
    const gradientChanged = finalState.gradientCosmic.includes('#667eea') ||
                           finalState.gradientNext.includes('#667eea');
    const hasAuroraClass = finalState.bodyClasses.includes('aurora-flow');

    console.log('   Gradient contains Aurora colors:', gradientChanged);
    console.log('   Body has aurora-flow class:', hasAuroraClass);

    // Check for relevant log messages
    const relevantLogs = logs.filter(log =>
      log.includes('updateBodyBackground') ||
      log.includes('Starting background transition') ||
      log.includes('Body element:') ||
      log.includes('Adding background-transitioning')
    );

    console.log('\n   Relevant console logs captured:', relevantLogs.length);
    if (relevantLogs.length > 0) {
      console.log('   Latest logs:');
      relevantLogs.slice(-5).forEach(log => console.log('      ', log));
    }

    console.log('   ════════════════════════════════════════════════════════════');

    // Final verdict
    if (gradientChanged && hasAuroraClass) {
      console.log('\n✅ SUCCESS: Background changed to Aurora!');
      console.log('   - Gradient updated:', gradientChanged);
      console.log('   - Animation class updated:', hasAuroraClass);
    } else {
      console.log('\n❌ FAILURE: Background did NOT change properly');
      console.log('   - Gradient updated:', gradientChanged);
      console.log('   - Animation class updated:', hasAuroraClass);

      // This will fail the test
      expect(gradientChanged, 'Gradient should contain Aurora colors').toBe(true);
      expect(hasAuroraClass, 'Body should have aurora-flow class').toBe(true);
    }
  });
});
