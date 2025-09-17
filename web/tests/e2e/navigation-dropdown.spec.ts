import { test, expect } from '@playwright/test';

test.describe('Navigation Dropdown', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    // Wait for the app to load
    await page.waitForSelector('.app-navigation-bar');
  });

  test('should show Build dropdown on hover/click', async ({ page }) => {
    // Find the Build tab container
    const buildTabContainer = page.locator('.nav-tab-container').filter({ hasText: 'Build' });
    await expect(buildTabContainer).toBeVisible();

    // Find the dropdown trigger
    const dropdownTrigger = buildTabContainer.locator('.dropdown-trigger');
    await expect(dropdownTrigger).toBeVisible();

    // Click the dropdown trigger
    await dropdownTrigger.click();

    // Check if dropdown menu appears
    const dropdownMenu = page.locator('.dropdown-menu');
    await expect(dropdownMenu).toBeVisible();

    // Check if all build modes are present
    await expect(dropdownMenu.locator('.dropdown-item').filter({ hasText: 'Construct' })).toBeVisible();
    await expect(dropdownMenu.locator('.dropdown-item').filter({ hasText: 'Generate' })).toBeVisible();
    await expect(dropdownMenu.locator('.dropdown-item').filter({ hasText: 'Edit' })).toBeVisible();
    await expect(dropdownMenu.locator('.dropdown-item').filter({ hasText: 'Export' })).toBeVisible();
  });

  test('should switch build modes when dropdown item is clicked', async ({ page }) => {
    // Open the Build dropdown
    const buildTabContainer = page.locator('.nav-tab-container').filter({ hasText: 'Build' });
    const dropdownTrigger = buildTabContainer.locator('.dropdown-trigger');
    await dropdownTrigger.click();

    // Click on Generate mode
    const generateItem = page.locator('.dropdown-item').filter({ hasText: 'Generate' });
    await generateItem.click();

    // Check if the current mode indicator shows Generate
    const currentModeIndicator = buildTabContainer.locator('.current-mode');
    await expect(currentModeIndicator).toContainText('Generate');

    // Check if dropdown closes after selection
    const dropdownMenu = page.locator('.dropdown-menu');
    await expect(dropdownMenu).not.toBeVisible();
  });

  test('should close dropdown when clicking outside', async ({ page }) => {
    // Open the Build dropdown
    const buildTabContainer = page.locator('.nav-tab-container').filter({ hasText: 'Build' });
    const dropdownTrigger = buildTabContainer.locator('.dropdown-trigger');
    await dropdownTrigger.click();

    // Verify dropdown is open
    const dropdownMenu = page.locator('.dropdown-menu');
    await expect(dropdownMenu).toBeVisible();

    // Click outside the dropdown
    await page.click('body', { position: { x: 10, y: 10 } });

    // Check if dropdown closes
    await expect(dropdownMenu).not.toBeVisible();
  });

  test('should handle keyboard navigation', async ({ page }) => {
    // Open the Build dropdown
    const buildTabContainer = page.locator('.nav-tab-container').filter({ hasText: 'Build' });
    const dropdownTrigger = buildTabContainer.locator('.dropdown-trigger');
    await dropdownTrigger.click();

    // Press Escape to close dropdown
    await page.keyboard.press('Escape');

    // Check if dropdown closes
    const dropdownMenu = page.locator('.dropdown-menu');
    await expect(dropdownMenu).not.toBeVisible();
  });
});
