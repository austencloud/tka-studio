/**
 * Sequence Actions Panel E2E Test
 * 
 * Tests the bug where swiping away the Sequence Actions panel
 * prevents it from being reopened.
 */

import { test, expect } from '@playwright/test';

test.describe('Sequence Actions Panel', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the app
    await page.goto('http://localhost:5173');
    
    // Wait for app to be ready
    await page.waitForLoadState('networkidle');
    
    // Wait for create module to be visible
    await page.waitForSelector('.create-tab', { timeout: 10000 });
  });

  test('should open and close via button click', async ({ page }) => {
    // Find and click the sequence actions button
    // The button might be in a toolbar or button panel
    const sequenceActionsButton = page.locator('button').filter({ 
      hasText: /actions|sequence actions|transform/i 
    }).first();
    
    // Click to open
    await sequenceActionsButton.click();
    await page.waitForTimeout(500); // Wait for animation
    
    // Verify panel is visible
    const actionsPanel = page.locator('.actions-panel, [role="dialog"]').filter({
      hasText: /mirror|rotate|color swap/i
    });
    await expect(actionsPanel).toBeVisible();
    
    // Close via close button
    const closeButton = actionsPanel.locator('button[aria-label*="close" i], button .fa-times').first();
    await closeButton.click();
    await page.waitForTimeout(500); // Wait for animation
    
    // Verify panel is closed
    await expect(actionsPanel).not.toBeVisible();
    
    // Try to reopen
    await sequenceActionsButton.click();
    await page.waitForTimeout(500);
    
    // Verify panel opens again
    await expect(actionsPanel).toBeVisible();
  });

  test('should reopen after swipe gesture close', async ({ page }) => {
    console.log('🧪 Starting swipe gesture test');
    
    // Find sequence actions button - try multiple possible selectors
    const possibleButtons = [
      'button:has-text("Actions")',
      'button:has-text("Sequence")',
      'button[aria-label*="action" i]',
      'button[aria-label*="sequence" i]',
      '.button-panel button',
      '.tool-panel button'
    ];
    
    let sequenceActionsButton = null;
    for (const selector of possibleButtons) {
      const btn = page.locator(selector).first();
      if (await btn.count() > 0) {
        sequenceActionsButton = btn;
        console.log(`✅ Found button with selector: ${selector}`);
        break;
      }
    }
    
    if (!sequenceActionsButton) {
      console.log('⚠️ Could not find sequence actions button, trying generic approach');
      // Take screenshot to see what's available
      await page.screenshot({ path: 'test-screenshots/button-not-found.png' });
      
      // Get all buttons and log them
      const allButtons = await page.locator('button').all();
      console.log(`Found ${allButtons.length} buttons on page`);
      for (let i = 0; i < Math.min(allButtons.length, 10); i++) {
        const button = allButtons[i];
        if (button) {
          const text = await button.textContent();
          const ariaLabel = await button.getAttribute('aria-label');
          console.log(`Button ${i}: text="${text}" aria-label="${ariaLabel}"`);
        }
      }
      
      // Skip test if button not found
      test.skip();
      return;
    }
    
    // Click to open panel
    console.log('🖱️ Clicking sequence actions button');
    await sequenceActionsButton.click();
    await page.waitForTimeout(500);
    
    // Check console logs
    const logs: string[] = [];
    page.on('console', msg => {
      const text = msg.text();
      logs.push(text);
      if (text.includes('🟢') || text.includes('📊') || text.includes('🔴')) {
        console.log('Browser log:', text);
      }
    });
    
    // Find the panel
    const actionsPanel = page.locator('.actions-panel').first();
    await expect(actionsPanel).toBeVisible({ timeout: 5000 });
    console.log('✅ Panel is visible');
    
    // Take screenshot before swipe
    await page.screenshot({ path: 'test-screenshots/before-swipe.png' });
    
    // Get panel bounding box for swipe gesture
    const panelBox = await actionsPanel.boundingBox();
    if (!panelBox) {
      throw new Error('Could not get panel bounding box');
    }
    
    // Perform swipe down gesture (simulating drawer close)
    console.log('👆 Performing swipe down gesture');
    const startX = panelBox.x + panelBox.width / 2;
    const startY = panelBox.y + 20; // Near top of panel
    const endY = panelBox.y + panelBox.height + 100; // Swipe down
    
    await page.mouse.move(startX, startY);
    await page.mouse.down();
    await page.mouse.move(startX, endY, { steps: 10 });
    await page.mouse.up();
    await page.waitForTimeout(1000); // Wait for close animation
    
    // Take screenshot after swipe
    await page.screenshot({ path: 'test-screenshots/after-swipe.png' });
    
    // Verify panel is closed
    console.log('🔍 Checking if panel is closed');
    await expect(actionsPanel).not.toBeVisible({ timeout: 5000 });
    console.log('✅ Panel is closed');
    
    // Check console logs for close handler
    const closeLog = logs.find(log => log.includes('🔴 handleClose'));
    if (closeLog) {
      console.log('✅ Close handler was called:', closeLog);
    } else {
      console.log('⚠️ Close handler was NOT called in logs');
    }
    
    // Wait a moment
    await page.waitForTimeout(500);
    
    // 🔴 THIS IS THE BUG: Try to reopen the panel
    console.log('🖱️ Attempting to reopen panel (THIS IS WHERE THE BUG OCCURS)');
    await sequenceActionsButton.click();
    await page.waitForTimeout(1000);
    
    // Take screenshot of attempted reopen
    await page.screenshot({ path: 'test-screenshots/after-reopen-attempt.png' });
    
    // Check if panel reopened
    const isVisible = await actionsPanel.isVisible();
    console.log(`🔍 Panel visible after reopen attempt: ${isVisible}`);
    
    // Check console logs for open handler
    const openLog = logs.find(log => log.includes('🟢 handleOpenSequenceActions'));
    if (openLog) {
      console.log('✅ Open handler was called:', openLog);
    } else {
      console.log('⚠️ Open handler was NOT called in logs');
    }
    
    // Print all relevant logs
    console.log('\n📋 All relevant console logs:');
    logs.forEach(log => {
      if (log.includes('🟢') || log.includes('📊') || log.includes('🔴')) {
        console.log(log);
      }
    });
    
    // ❌ THIS ASSERTION SHOULD FAIL, demonstrating the bug
    await expect(actionsPanel).toBeVisible({ timeout: 5000 });
  });

  test('should track state changes in console', async ({ page }) => {
    // Collect console logs
    const logs: string[] = [];
    page.on('console', msg => {
      const text = msg.text();
      logs.push(text);
      console.log('Browser:', text);
    });
    
    // Find and click sequence actions button
    const sequenceActionsButton = page.locator('button').filter({ 
      hasText: /actions|sequence/i 
    }).first();
    
    // Open panel
    await sequenceActionsButton.click();
    await page.waitForTimeout(500);
    
    // Verify we see state change logs
    expect(logs.some(log => log.includes('📊') || log.includes('🟢'))).toBe(true);
    
    // Close panel via button
    const closeButton = page.locator('.actions-panel button[aria-label*="close" i]').first();
    await closeButton.click();
    await page.waitForTimeout(500);
    
    // Verify we see close logs
    expect(logs.some(log => log.includes('🔴'))).toBe(true);
    
    // Print summary
    console.log('\n📊 State Change Summary:');
    console.log(`Total logs captured: ${logs.length}`);
    console.log(`Open logs (🟢): ${logs.filter(l => l.includes('🟢')).length}`);
    console.log(`State change logs (📊): ${logs.filter(l => l.includes('📊')).length}`);
    console.log(`Close logs (🔴): ${logs.filter(l => l.includes('🔴')).length}`);
  });
});
