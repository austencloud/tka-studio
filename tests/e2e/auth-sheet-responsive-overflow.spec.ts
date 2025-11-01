import { expect, test } from "@playwright/test";

/**
 * Auth Sheet Responsive Overflow Detection Test
 *
 * Verifies that the authentication sheet fits properly on all screen sizes
 * without overflow, especially on small devices like iPhone SE.
 *
 * Tests both sign-in and sign-up modes across multiple viewport sizes.
 */

test.describe("Auth Sheet Responsive Layout", () => {
  /**
   * Helper function to open the auth sheet
   */
  async function openAuthSheet(page: any) {
    // Wait for page to be fully loaded
    await page.waitForLoadState("networkidle");
    await page.waitForTimeout(2000); // Give extra time for app initialization

    // Click the profile button - it has class "profile-button"
    const profileButton = page.locator('.profile-button').first();

    // Wait for it to be visible with longer timeout
    await profileButton.waitFor({ state: 'visible', timeout: 15000 });

    // Click the profile button
    await profileButton.click();

    // Wait a bit for profile settings sheet to animate
    await page.waitForTimeout(800);

    // Now we need to click the "Sign In" button in the profile settings sheet
    const signInButton = page.locator('button:has-text("Sign In")').first();
    await signInButton.waitFor({ state: 'visible', timeout: 15000 });
    await signInButton.click();

    // Wait a bit for auth sheet to animate
    await page.waitForTimeout(800);

    // Wait for auth sheet to be visible
    await page.waitForSelector('.auth-sheet__container', { timeout: 15000 });
  }

  /**
   * Helper function to measure overflow in the auth sheet
   */
  async function measureAuthSheetOverflow(page: any) {
    const container = page.locator('.auth-sheet__container');
    const content = page.locator('.auth-sheet__content');
    const header = page.locator('.auth-sheet__header');
    const footer = page.locator('.auth-sheet__footer');

    // Get measurements
    const measurements = await container.evaluate((el) => {
      const containerRect = el.getBoundingClientRect();
      const contentEl = el.querySelector('.auth-sheet__content') as HTMLElement;
      const headerEl = el.querySelector('.auth-sheet__header') as HTMLElement;
      const footerEl = el.querySelector('.auth-sheet__footer') as HTMLElement;

      const contentRect = contentEl?.getBoundingClientRect();
      const headerRect = headerEl?.getBoundingClientRect();
      const footerRect = footerEl?.getBoundingClientRect();

      return {
        container: {
          height: containerRect.height,
          scrollHeight: el.scrollHeight,
          clientHeight: el.clientHeight,
          hasVerticalOverflow: el.scrollHeight > el.clientHeight,
          top: containerRect.top,
          bottom: containerRect.bottom,
        },
        content: contentEl ? {
          height: contentRect.height,
          scrollHeight: contentEl.scrollHeight,
          clientHeight: contentEl.clientHeight,
          hasVerticalOverflow: contentEl.scrollHeight > contentEl.clientHeight,
          isScrollable: contentEl.scrollHeight > contentEl.clientHeight,
        } : null,
        header: headerEl ? {
          height: headerRect.height,
          isVisible: headerEl.offsetParent !== null,
        } : null,
        footer: footerEl ? {
          height: footerRect.height,
          isVisible: footerEl.offsetParent !== null,
          display: window.getComputedStyle(footerEl).display,
        } : null,
        viewport: {
          width: window.innerWidth,
          height: window.innerHeight,
        },
      };
    });

    // Check if elements fit within viewport
    const elementsInBounds = await container.evaluate((el) => {
      const containerRect = el.getBoundingClientRect();
      const viewportHeight = window.innerHeight;

      return {
        fitsInViewport: containerRect.bottom <= viewportHeight && containerRect.top >= 0,
        bottomOverflow: containerRect.bottom - viewportHeight,
        topOverflow: 0 - containerRect.top,
      };
    });

    return { ...measurements, bounds: elementsInBounds };
  }

  /**
   * Helper function to switch between sign-in and sign-up modes
   */
  async function toggleAuthMode(page: any, targetMode: 'signin' | 'signup') {
    const toggleButton = page.locator('.toggle-button');

    if (await toggleButton.count() > 0) {
      const buttonText = await toggleButton.textContent();

      // Click if we need to switch modes
      if (
        (targetMode === 'signup' && buttonText?.includes('Sign up')) ||
        (targetMode === 'signin' && buttonText?.includes('Sign in'))
      ) {
        await toggleButton.click();
        await page.waitForTimeout(400); // Wait for animation
      }
    }
  }

  /**
   * Test device configurations
   */
  const testDevices = [
    {
      name: "Desktop (1920x1080)",
      width: 1920,
      height: 1080,
      expectFooterVisible: true,
      expectSubtitleVisible: true,
    },
    {
      name: "iPad Pro (1024x1366)",
      width: 1024,
      height: 1366,
      expectFooterVisible: true,
      expectSubtitleVisible: true,
    },
    {
      name: "iPhone 14 Pro (393x852)",
      width: 393,
      height: 852,
      expectFooterVisible: true,
      expectSubtitleVisible: true,
    },
    {
      name: "iPhone SE 2/3 (375x667)",
      width: 375,
      height: 667,
      expectFooterVisible: false, // Footer should be hidden
      expectSubtitleVisible: true,
    },
    {
      name: "iPhone SE 1 (320x568)",
      width: 320,
      height: 568,
      expectFooterVisible: false, // Footer should be hidden
      expectSubtitleVisible: false, // Subtitle should be hidden
    },
  ];

  for (const device of testDevices) {
    test(`${device.name} - Sign In mode should fit without overflow`, async ({ page }) => {
      // Set viewport
      await page.setViewportSize({ width: device.width, height: device.height });
      await page.goto("/");

      // Open auth sheet
      await openAuthSheet(page);

      // Ensure we're in sign-in mode
      await toggleAuthMode(page, 'signin');

      // Measure overflow
      const measurements = await measureAuthSheetOverflow(page);

      console.log(`\n📱 ${device.name} - Sign In Mode:`);
      console.log(`  Viewport: ${measurements.viewport.width}x${measurements.viewport.height}px`);
      console.log(`  Container height: ${measurements.container.height.toFixed(0)}px`);
      console.log(`  Container scroll height: ${measurements.container.scrollHeight}px`);
      console.log(`  Container has overflow: ${measurements.container.hasVerticalOverflow}`);
      console.log(`  Content scrollable: ${measurements.content?.isScrollable}`);
      console.log(`  Fits in viewport: ${measurements.bounds.fitsInViewport}`);
      console.log(`  Header height: ${measurements.header?.height.toFixed(0)}px`);
      console.log(`  Footer visible: ${measurements.footer?.isVisible}`);
      console.log(`  Footer display: ${measurements.footer?.display}`);

      if (!measurements.bounds.fitsInViewport) {
        console.log(`  ⚠️ Bottom overflow: ${measurements.bounds.bottomOverflow.toFixed(0)}px`);
      }

      // ASSERTIONS

      // 1. Container should fit within viewport
      expect(measurements.bounds.fitsInViewport).toBe(true);

      // 2. Container itself should not overflow (content area should handle scrolling)
      expect(measurements.container.hasVerticalOverflow).toBe(false);

      // 3. Footer visibility based on device
      if (device.expectFooterVisible) {
        expect(measurements.footer?.isVisible).toBe(true);
        expect(measurements.footer?.display).not.toBe('none');
      } else {
        // On small screens, footer should be hidden
        expect(measurements.footer?.display).toBe('none');
      }

      // 4. Subtitle visibility based on device
      const subtitle = page.locator('.auth-sheet__subtitle');
      if (device.expectSubtitleVisible) {
        await expect(subtitle).toBeVisible();
      } else {
        // On very small screens, subtitle should be hidden
        const subtitleDisplay = await subtitle.evaluate((el) =>
          window.getComputedStyle(el).display
        );
        expect(subtitleDisplay).toBe('none');
      }

      // 5. Content area should be scrollable if needed (this is OK)
      console.log(`  Content area scrollable: ${measurements.content?.isScrollable ? '✓ (expected)' : '✓ (no scroll needed)'}`);

      // 6. No element should overflow the bottom of viewport
      if (measurements.bounds.bottomOverflow > 0) {
        console.log(`  ❌ OVERFLOW: ${measurements.bounds.bottomOverflow.toFixed(0)}px extends beyond viewport`);
      }
      expect(measurements.bounds.bottomOverflow).toBeLessThanOrEqual(0);

      console.log(`  ✅ Layout fits correctly`);
    });

    test(`${device.name} - Sign Up mode should fit without overflow`, async ({ page }) => {
      // Set viewport
      await page.setViewportSize({ width: device.width, height: device.height });
      await page.goto("/");

      // Open auth sheet
      await openAuthSheet(page);

      // Switch to sign-up mode
      await toggleAuthMode(page, 'signup');

      // Measure overflow
      const measurements = await measureAuthSheetOverflow(page);

      console.log(`\n📱 ${device.name} - Sign Up Mode:`);
      console.log(`  Viewport: ${measurements.viewport.width}x${measurements.viewport.height}px`);
      console.log(`  Container height: ${measurements.container.height.toFixed(0)}px`);
      console.log(`  Container scroll height: ${measurements.container.scrollHeight}px`);
      console.log(`  Container has overflow: ${measurements.container.hasVerticalOverflow}`);
      console.log(`  Content scrollable: ${measurements.content?.isScrollable}`);
      console.log(`  Fits in viewport: ${measurements.bounds.fitsInViewport}`);
      console.log(`  Footer visible: ${measurements.footer?.isVisible}`);

      if (!measurements.bounds.fitsInViewport) {
        console.log(`  ⚠️ Bottom overflow: ${measurements.bounds.bottomOverflow.toFixed(0)}px`);
      }

      // ASSERTIONS

      // 1. Container should fit within viewport
      expect(measurements.bounds.fitsInViewport).toBe(true);

      // 2. Container should not overflow
      expect(measurements.container.hasVerticalOverflow).toBe(false);

      // 3. Footer visibility
      if (device.expectFooterVisible) {
        expect(measurements.footer?.isVisible).toBe(true);
      } else {
        expect(measurements.footer?.display).toBe('none');
      }

      // 4. Name field should be visible in sign-up mode
      const nameField = page.locator('input#name');
      await expect(nameField).toBeVisible();

      // 5. No bottom overflow
      expect(measurements.bounds.bottomOverflow).toBeLessThanOrEqual(0);

      console.log(`  ✅ Sign-up layout fits correctly`);
    });
  }

  test("OAuth buttons visible in both sign-in and sign-up modes", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE 2/3
    await page.goto("/");

    await openAuthSheet(page);

    // In sign-in mode, compact social buttons should be visible
    const compactSocialLinks = page.locator('.auth-sheet__social-compact');
    await expect(compactSocialLinks).toBeVisible();

    // Check individual buttons
    const googleButton = page.locator('.social-compact-button--google');
    const facebookButton = page.locator('.social-compact-button--facebook');
    await expect(googleButton).toBeVisible();
    await expect(facebookButton).toBeVisible();

    // Switch to sign-up mode
    await toggleAuthMode(page, 'signup');

    // OAuth buttons should still be visible
    await expect(compactSocialLinks).toBeVisible();
    await expect(googleButton).toBeVisible();
    await expect(facebookButton).toBeVisible();

    console.log('✅ OAuth buttons consistently visible in both modes');
  });

  test("Touch targets meet WCAG minimum size on smallest device", async ({ page }) => {
    await page.setViewportSize({ width: 320, height: 568 }); // iPhone SE 1
    await page.goto("/");

    await openAuthSheet(page);

    // Check button sizes
    const buttons = page.locator('.submit-button, .toggle-button, .password-toggle, .auth-sheet__close');
    const buttonCount = await buttons.count();

    console.log(`\n🎯 Checking ${buttonCount} touch targets on iPhone SE 1:`);

    for (let i = 0; i < buttonCount; i++) {
      const button = buttons.nth(i);
      const size = await button.evaluate((el) => {
        const rect = el.getBoundingClientRect();
        return {
          width: rect.width,
          height: rect.height,
          className: el.className,
        };
      });

      console.log(`  ${size.className}: ${size.width.toFixed(0)}x${size.height.toFixed(0)}px`);

      // WCAG 2.1 AA minimum: 44x44px
      expect(size.width).toBeGreaterThanOrEqual(44);
      expect(size.height).toBeGreaterThanOrEqual(44);
    }

    console.log('✅ All touch targets meet WCAG 2.1 AA minimum (44x44px)');
  });

  test("Content remains accessible when scrolling is needed", async ({ page }) => {
    await page.setViewportSize({ width: 320, height: 568 }); // Smallest device
    await page.goto("/");

    await openAuthSheet(page);
    await toggleAuthMode(page, 'signup'); // More content in sign-up mode

    // Get all form elements
    const emailInput = page.locator('input#email');
    const passwordInput = page.locator('input#password');
    const nameInput = page.locator('input#name');
    const submitButton = page.locator('.submit-button');

    // All should be in the DOM
    await expect(emailInput).toBeAttached();
    await expect(passwordInput).toBeAttached();
    await expect(nameInput).toBeAttached();
    await expect(submitButton).toBeAttached();

    // Check if content area is scrollable
    const contentScrollable = await page.locator('.auth-sheet__content').evaluate((el) => {
      return el.scrollHeight > el.clientHeight;
    });

    if (contentScrollable) {
      console.log('✓ Content area is scrollable (expected on small screens)');

      // Try scrolling to bottom element
      await submitButton.scrollIntoViewIfNeeded();
      await expect(submitButton).toBeInViewport();

      console.log('✅ Elements remain accessible via scrolling');
    } else {
      console.log('✅ All content fits without scrolling');
    }
  });

  test("Dynamic viewport height (dvh) adapts to keyboard on mobile", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE 2/3
    await page.goto("/");

    await openAuthSheet(page);

    // Get initial container height
    const initialHeight = await page.locator('.auth-sheet__container').evaluate((el) => {
      const styles = window.getComputedStyle(el);
      return {
        maxHeight: styles.maxHeight,
        computedHeight: el.getBoundingClientRect().height,
      };
    });

    console.log(`\n📐 Container using dvh units:`);
    console.log(`  max-height: ${initialHeight.maxHeight}`);
    console.log(`  computed height: ${initialHeight.computedHeight.toFixed(0)}px`);

    // Verify dvh is being used
    expect(initialHeight.maxHeight).toContain('dvh');

    console.log('✅ Using dvh units for better mobile keyboard handling');
  });

  test("Mode transitions don't cause layout overflow", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE 2/3
    await page.goto("/");

    await openAuthSheet(page);

    // Measure in sign-in mode
    const signInMeasurements = await measureAuthSheetOverflow(page);
    expect(signInMeasurements.bounds.fitsInViewport).toBe(true);

    // Switch to sign-up mode
    await toggleAuthMode(page, 'signup');
    await page.waitForTimeout(400); // Wait for animation

    // Measure in sign-up mode
    const signUpMeasurements = await measureAuthSheetOverflow(page);
    expect(signUpMeasurements.bounds.fitsInViewport).toBe(true);

    // Switch back to sign-in
    await toggleAuthMode(page, 'signin');
    await page.waitForTimeout(400);

    // Measure again
    const backToSignInMeasurements = await measureAuthSheetOverflow(page);
    expect(backToSignInMeasurements.bounds.fitsInViewport).toBe(true);

    console.log('✅ No overflow during mode transitions');
  });
});
