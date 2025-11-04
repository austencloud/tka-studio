/**
 * Aurora Contrast System Validation Script
 *
 * Run this in your browser console while the app is running to validate
 * that the Aurora contrast system is working correctly.
 *
 * Usage:
 * 1. Open the app (localhost:5173)
 * 2. Open browser DevTools (F12)
 * 3. Copy and paste this entire file into the Console
 * 4. Press Enter
 *
 * The script will output a detailed report of all checks.
 */

(function() {
  console.clear();
  console.log('%c🎨 Aurora Contrast System Validation', 'font-size: 20px; font-weight: bold; color: #a855f7;');
  console.log('%c══════════════════════════════════════════', 'color: #a855f7;');
  console.log('');

  const results = {
    passed: 0,
    failed: 0,
    warnings: 0,
    tests: []
  };

  function test(name, condition, expected, actual) {
    const passed = condition;
    results.tests.push({ name, passed, expected, actual });
    if (passed) {
      results.passed++;
      console.log(`%c✅ PASS%c ${name}`, 'color: #22c55e; font-weight: bold;', 'color: inherit;');
      if (actual) console.log(`   ${actual}`);
    } else {
      results.failed++;
      console.log(`%c❌ FAIL%c ${name}`, 'color: #ef4444; font-weight: bold;', 'color: inherit;');
      console.log(`   Expected: ${expected}`);
      console.log(`   Actual: ${actual || 'undefined'}`);
    }
  }

  function warn(message) {
    results.warnings++;
    console.log(`%c⚠️  WARN%c ${message}`, 'color: #f59e0b; font-weight: bold;', 'color: inherit;');
  }

  console.log('%c📋 Running Tests...', 'font-size: 16px; font-weight: bold; color: #3b82f6;');
  console.log('');

  // Get current theme
  const root = document.documentElement;
  const style = getComputedStyle(root);
  let currentTheme = 'unknown';

  try {
    const settings = JSON.parse(localStorage.getItem('tka-modern-web-settings'));
    currentTheme = settings?.backgroundType || 'nightSky';
  } catch (e) {
    warn('Could not read current theme from localStorage');
  }

  console.log(`Current theme: %c${currentTheme}`, 'font-weight: bold; color: #a855f7;');
  console.log('');

  // Test 1: Check if Aurora-specific variables are defined
  console.log('%c1️⃣  Aurora Variable Definitions', 'font-weight: bold;');
  const auroraVars = {
    panelBg: style.getPropertyValue('--panel-bg-aurora').trim(),
    panelBorder: style.getPropertyValue('--panel-border-aurora').trim(),
    panelHover: style.getPropertyValue('--panel-hover-aurora').trim(),
    cardBg: style.getPropertyValue('--card-bg-aurora').trim(),
    cardBorder: style.getPropertyValue('--card-border-aurora').trim(),
    cardHover: style.getPropertyValue('--card-hover-aurora').trim(),
    textPrimary: style.getPropertyValue('--text-primary-aurora').trim(),
    textSecondary: style.getPropertyValue('--text-secondary-aurora').trim(),
    inputBg: style.getPropertyValue('--input-bg-aurora').trim(),
    inputBorder: style.getPropertyValue('--input-border-aurora').trim(),
    inputFocus: style.getPropertyValue('--input-focus-aurora').trim(),
    buttonActive: style.getPropertyValue('--button-active-aurora').trim(),
  };

  test(
    'Panel background variable defined',
    auroraVars.panelBg !== '',
    'rgba(20, 10, 40, 0.85)',
    auroraVars.panelBg
  );

  test(
    'Card background variable defined',
    auroraVars.cardBg !== '',
    'rgba(25, 15, 45, 0.88)',
    auroraVars.cardBg
  );

  test(
    'All 12 Aurora variables defined',
    Object.values(auroraVars).every(v => v !== ''),
    '12 variables with values',
    `${Object.values(auroraVars).filter(v => v !== '').length} defined`
  );

  console.log('');

  // Test 2: Check current theme variables
  console.log('%c2️⃣  Current Theme Variables', 'font-weight: bold;');
  const currentVars = {
    panelBg: style.getPropertyValue('--panel-bg-current').trim(),
    cardBg: style.getPropertyValue('--card-bg-current').trim(),
    textPrimary: style.getPropertyValue('--text-primary-current').trim(),
    inputBg: style.getPropertyValue('--input-bg-current').trim(),
    buttonActive: style.getPropertyValue('--button-active-current').trim(),
  };

  test(
    'Current panel background defined',
    currentVars.panelBg !== '',
    'Non-empty value',
    currentVars.panelBg
  );

  if (currentTheme === 'aurora') {
    test(
      'Current variables match Aurora theme',
      currentVars.panelBg.includes('20, 10, 40') && currentVars.cardBg.includes('25, 15, 45'),
      'Aurora-specific dark purple values',
      `Panel: ${currentVars.panelBg}, Card: ${currentVars.cardBg}`
    );
  } else {
    console.log(`   ℹ️  Skipped Aurora match test (current theme is ${currentTheme})`);
  }

  console.log('');

  // Test 3: Check ThemeService functionality
  console.log('%c3️⃣  ThemeService Functionality', 'font-weight: bold;');

  // Check if localStorage has settings
  const hasSettings = localStorage.getItem('tka-modern-web-settings') !== null;
  test(
    'Settings stored in localStorage',
    hasSettings,
    'Settings object present',
    hasSettings ? 'Found' : 'Not found'
  );

  console.log('');

  // Test 4: Component Integration
  console.log('%c4️⃣  Component Integration', 'font-weight: bold;');

  // Check if collection cards exist and use variables
  const collectionCard = document.querySelector('.collection-card');
  if (collectionCard) {
    const cardStyle = window.getComputedStyle(collectionCard);
    const cardBg = cardStyle.backgroundColor;
    test(
      'Collection card has background color',
      cardBg !== 'rgba(0, 0, 0, 0)' && cardBg !== 'transparent',
      'Non-transparent background',
      cardBg
    );
  } else {
    warn('No collection cards found in DOM (may need to navigate to Collections)');
  }

  // Check if search input exists and uses variables
  const searchInput = document.querySelector('.search-input, input[type="text"]');
  if (searchInput) {
    const inputStyle = window.getComputedStyle(searchInput);
    const inputBg = inputStyle.backgroundColor;
    test(
      'Search input has background color',
      inputBg !== 'rgba(0, 0, 0, 0)' && inputBg !== 'transparent',
      'Non-transparent background',
      inputBg
    );
  } else {
    warn('No search input found in DOM (may need to navigate to Search)');
  }

  console.log('');

  // Test 5: Dropdown/Header variables
  console.log('%c5️⃣  Dropdown & Header Variables', 'font-weight: bold;');
  const dropdownVars = {
    dropdownBg: style.getPropertyValue('--dropdown-bg-current').trim(),
    dropdownText: style.getPropertyValue('--dropdown-text-current').trim(),
    headerBg: style.getPropertyValue('--header-bg-current').trim(),
  };

  test(
    'Dropdown background defined',
    dropdownVars.dropdownBg !== '',
    'Non-empty value',
    dropdownVars.dropdownBg
  );

  test(
    'All dropdown/header variables defined',
    Object.values(dropdownVars).every(v => v !== ''),
    '3 variables with values',
    `${Object.values(dropdownVars).filter(v => v !== '').length} defined`
  );

  console.log('');

  // Summary
  console.log('%c══════════════════════════════════════════', 'color: #a855f7;');
  console.log('%c📊 Test Summary', 'font-size: 16px; font-weight: bold; color: #3b82f6;');
  console.log('');
  console.log(`%c✅ Passed: ${results.passed}`, 'color: #22c55e; font-weight: bold;');
  console.log(`%c❌ Failed: ${results.failed}`, results.failed > 0 ? 'color: #ef4444; font-weight: bold;' : 'color: #6b7280;');
  console.log(`%c⚠️  Warnings: ${results.warnings}`, results.warnings > 0 ? 'color: #f59e0b; font-weight: bold;' : 'color: #6b7280;');
  console.log('');

  if (results.failed === 0 && results.warnings === 0) {
    console.log('%c🎉 All tests passed! Aurora contrast system is working correctly.', 'font-size: 14px; color: #22c55e; font-weight: bold; padding: 8px; background: #dcfce7; border-radius: 4px;');
  } else if (results.failed === 0) {
    console.log('%c✓ All tests passed with some warnings.', 'font-size: 14px; color: #f59e0b; font-weight: bold;');
  } else {
    console.log('%c❌ Some tests failed. Review the output above for details.', 'font-size: 14px; color: #ef4444; font-weight: bold; padding: 8px; background: #fee2e2; border-radius: 4px;');
  }

  console.log('');
  console.log('%c💡 Tips:', 'font-weight: bold;');
  console.log('   • Navigate to Explore > Collections to test collection cards');
  console.log('   • Navigate to Explore > Search to test search input');
  console.log('   • Change background in Settings > Background to test theme switching');
  console.log('');

  // Return results for programmatic access
  return results;
})();
