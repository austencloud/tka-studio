import { test, expect } from '@playwright/test';

test.describe('SequenceActionsSheet Reopen Issue', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the create module
    await page.goto('http://localhost:5173/create', { 
      waitUntil: 'load',
      timeout: 60000 
    });
    
    // Wait for the canvas/pictograph area to load
    await page.waitForSelector('canvas, .pictograph-container, .beat-frame', { 
      timeout: 30000 
    });
    
    // The sequence actions button should appear once we have a sequence loaded
    // Give it some time to render
    await page.waitForTimeout(3000);
    
    // Try to find the sequence actions button
    const buttonExists = await page.locator('[data-testid="sequence-actions-button"]').count();
    if (buttonExists === 0) {
      console.log('⚠️ Sequence actions button not visible - test may fail');
    }
  });

  test('should reopen SequenceActionsSheet after swiping it away', async ({ page, browserName }) => {
    // Listen to console logs to capture our debug output
    const consoleLogs: string[] = [];
    page.on('console', msg => {
      const text = msg.text();
      if (text.includes('🟢') || text.includes('📊') || text.includes('🔴')) {
        consoleLogs.push(text);
      }
    });

    // Check if button is visible
    const button = page.locator('[data-testid="sequence-actions-button"]');
    const isVisible = await button.isVisible().catch(() => false);
    
    if (!isVisible) {
      console.log('⚠️ SKIPPING TEST: Sequence actions button not visible (likely no sequence loaded)');
      test.skip();
      return;
    }

    // Step 1: Click the sequence actions button to open the sheet
    console.log('Step 1: Opening SequenceActionsSheet...');
    await button.click();
    
    // Wait for sheet to appear
    await page.waitForSelector('[data-testid="sequence-actions-sheet"]', { 
      state: 'visible',
      timeout: 5000 
    });
    
    // Verify sheet is open
    const sheetVisible = await page.isVisible('[data-testid="sequence-actions-sheet"]');
    expect(sheetVisible).toBe(true);
    console.log('✅ Sheet opened successfully');
    
    // Log what we captured
    console.log('Console logs after opening:', consoleLogs);
    
    // Step 2: Swipe the sheet away (simulate gesture)
    console.log('Step 2: Swiping sheet away...');
    const sheet = page.locator('[data-testid="sequence-actions-sheet"]');
    
    // Get the sheet's bounding box
    const box = await sheet.boundingBox();
    if (!box) throw new Error('Sheet not found');
    
    // Perform swipe down gesture (works across browsers)
    await page.mouse.move(box.x + box.width / 2, box.y + 50);
    await page.mouse.down();
    await page.mouse.move(box.x + box.width / 2, box.y + box.height + 100, { steps: 10 });
    await page.mouse.up();
    
    // Wait for sheet to close
    await page.waitForSelector('[data-testid="sequence-actions-sheet"]', { 
      state: 'hidden',
      timeout: 5000 
    });
    
    console.log('✅ Sheet closed via swipe');
    console.log('Console logs after swiping:', consoleLogs);
    
    // Step 3: Try to reopen the sheet
    console.log('Step 3: Attempting to reopen SequenceActionsSheet...');
    consoleLogs.length = 0; // Clear previous logs
    
    await button.click();
    
    // Wait a moment for any state changes
    await page.waitForTimeout(1000);
    
    // Check if sheet reopened
    const sheetReopened = await page.isVisible('[data-testid="sequence-actions-sheet"]');
    
    console.log('Console logs after reopen attempt:', consoleLogs);
    
    // This is the failing assertion - documenting the bug
    if (!sheetReopened) {
      console.error('❌ BUG CONFIRMED: Sheet did not reopen after swipe!');
      console.error('Final console logs:', consoleLogs);
    }
    
    expect(sheetReopened).toBe(true);
  });

  test('should reopen SequenceActionsSheet after clicking close button', async ({ page }) => {
    // This test verifies the close button works correctly (baseline)
    const consoleLogs: string[] = [];
    page.on('console', msg => {
      const text = msg.text();
      if (text.includes('🟢') || text.includes('📊') || text.includes('🔴')) {
        consoleLogs.push(text);
      }
    });

    // Check if button is visible
    const button = page.locator('[data-testid="sequence-actions-button"]');
    const isVisible = await button.isVisible().catch(() => false);
    
    if (!isVisible) {
      console.log('⚠️ SKIPPING TEST: Sequence actions button not visible (likely no sequence loaded)');
      test.skip();
      return;
    }

    // Open sheet
    await button.click();
    await page.waitForSelector('[data-testid="sequence-actions-sheet"]', { state: 'visible' });
    
    // Close via close button
    await page.click('[data-testid="close-sequence-actions"]');
    await page.waitForSelector('[data-testid="sequence-actions-sheet"]', { state: 'hidden' });
    
    console.log('Console logs after close button:', consoleLogs);
    
    // Try to reopen
    consoleLogs.length = 0;
    await button.click();
    await page.waitForTimeout(500);
    
    const sheetReopened = await page.isVisible('[data-testid="sequence-actions-sheet"]');
    console.log('Console logs after reopen:', consoleLogs);
    
    expect(sheetReopened).toBe(true);
  });
});
