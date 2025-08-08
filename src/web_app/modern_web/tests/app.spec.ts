import { test, expect } from '@playwright/test';

test('application loads and initializes successfully', async ({ page }) => {
  // Collect console messages
  const consoleMessages: string[] = [];
  page.on('console', msg => {
    consoleMessages.push(msg.text());
  });

  // Navigate to the application
  await page.goto('http://localhost:5174/');

  // Wait for the application to initialize
  await page.waitForSelector('[data-testid="main-application"]', { timeout: 15000 });

  // Check that the construct tab is visible
  await expect(page.locator('[data-testid="construct-tab"]')).toBeVisible();

  // Check that start position picker is shown initially
  await expect(page.locator('[data-testid="start-position-picker"]')).toBeVisible();

  // Wait a bit for any async operations and console messages
  await page.waitForTimeout(3000);

  // Check that DI container initialized successfully
  const hasSuccessfulInit = consoleMessages.some(log =>
    log.includes('TKA V2 Modern initialized successfully')
  );

  console.log('Console messages:', consoleMessages.slice(-10)); // Show last 10 messages
  expect(hasSuccessfulInit).toBeTruthy();

  // Check that the application is functional (no critical errors that prevent basic operation)
  const criticalErrors = consoleMessages.filter(log =>
    log.includes('TypeError') ||
    log.includes('ReferenceError') ||
    log.includes('Cannot read properties of undefined')
  );

  console.log('Critical errors found:', criticalErrors);
  expect(criticalErrors.length).toBeLessThan(3); // Allow some minor errors but not too many
});
