# Aurora Contrast System - Manual Testing Guide

This guide provides step-by-step instructions to manually verify that the Aurora contrast system is working correctly.

## Prerequisites

1. Start the development server: `npm run dev`
2. Open the app in your browser: `http://localhost:5173`
3. Have Chrome DevTools open (F12) with the Console and Elements tabs visible

## Test 1: Verify CSS Variables are Defined

**Purpose**: Confirm all Aurora-specific CSS variables exist in the stylesheet.

### Steps:
1. Open DevTools Console
2. Paste and run this code:

```javascript
const root = document.documentElement;
const style = getComputedStyle(root);

const auroraVars = {
  // Panel variables
  panelBgAurora: style.getPropertyValue('--panel-bg-aurora'),
  panelBorderAurora: style.getPropertyValue('--panel-border-aurora'),
  panelHoverAurora: style.getPropertyValue('--panel-hover-aurora'),

  // Card variables
  cardBgAurora: style.getPropertyValue('--card-bg-aurora'),
  cardBorderAurora: style.getPropertyValue('--card-border-aurora'),
  cardHoverAurora: style.getPropertyValue('--card-hover-aurora'),

  // Text variables
  textPrimaryAurora: style.getPropertyValue('--text-primary-aurora'),
  textSecondaryAurora: style.getPropertyValue('--text-secondary-aurora'),

  // Input variables
  inputBgAurora: style.getPropertyValue('--input-bg-aurora'),
  inputBorderAurora: style.getPropertyValue('--input-border-aurora'),
  inputFocusAurora: style.getPropertyValue('--input-focus-aurora'),

  // Button variables
  buttonActiveAurora: style.getPropertyValue('--button-active-aurora'),
};

console.table(auroraVars);
```

### Expected Results:
All variables should have values displayed. Key values to verify:
- `panelBgAurora`: `rgba(20, 10, 40, 0.85)`
- `cardBgAurora`: `rgba(25, 15, 45, 0.88)`
- `textPrimaryAurora`: `#ffffff`

✅ **PASS**: All variables have values
❌ **FAIL**: Any variable is empty or undefined

---

## Test 2: Switch to Aurora Background

**Purpose**: Verify the Aurora background applies correctly and theme variables update.

### Steps:
1. Click the **Settings** button (gear icon or profile icon)
2. Click the **Background** tab
3. Click **Animated** category (if not already selected)
4. Click the **Aurora** background option
5. Wait 2 seconds for the transition

### Expected Results:
- Background should transition to vibrant purple/pink/blue gradient
- Settings panel should become noticeably darker
- Text should remain crisp and readable

### Visual Inspection:
Look at the Settings panel itself:
- Background should be **dark purple/translucent** (not barely visible white)
- Text should be **bright white** and highly legible
- Any cards or buttons should have **strong contrast**

✅ **PASS**: Dark purple overlays visible, text is readable
❌ **FAIL**: Panels are barely visible, text is hard to read

---

## Test 3: Verify CSS Variables Update Dynamically

**Purpose**: Confirm that `--*-current` variables switch to Aurora values.

### Steps:
1. With Aurora background active, open DevTools Console
2. Paste and run this code:

```javascript
const root = document.documentElement;
const style = getComputedStyle(root);

const currentVars = {
  panelBgCurrent: style.getPropertyValue('--panel-bg-current'),
  cardBgCurrent: style.getPropertyValue('--card-bg-current'),
  textPrimaryCurrent: style.getPropertyValue('--text-primary-current'),
  inputBgCurrent: style.getPropertyValue('--input-bg-current'),
  buttonActiveCurrent: style.getPropertyValue('--button-active-current'),
};

console.table(currentVars);

// Verify they match Aurora values
console.log('✅ Match Aurora values:',
  currentVars.panelBgCurrent.includes('rgba(20, 10, 40, 0.85)') &&
  currentVars.cardBgCurrent.includes('rgba(25, 15, 45, 0.88)')
);
```

### Expected Results:
- Console should show Aurora-specific values
- Final line should print: `✅ Match Aurora values: true`

✅ **PASS**: Variables match Aurora values
❌ **FAIL**: Variables still show default values

---

## Test 4: Test Collections Panel Contrast

**Purpose**: Verify collection cards are visible with Aurora background.

### Steps:
1. Ensure Aurora background is active
2. Close Settings
3. Click **Explore** tab in the navigation
4. Click **Collections** subtab
5. Observe collection cards (if any exist, or look at filter buttons)

### Expected Results:
- Filter buttons at the top should have **dark purple backgrounds**
- If collection cards exist, they should have **dark purple backgrounds**
- All text should be **bright and readable**
- Hover effects should make cards slightly lighter purple

### Visual Inspection:
- Cards should **NOT** be barely visible white/transparent
- Cards should be **clearly distinguishable** from the background
- Borders should have a **purple tint**

✅ **PASS**: Cards are dark and clearly visible
❌ **FAIL**: Cards blend into background

---

## Test 5: Test Search Panel Contrast

**Purpose**: Verify search inputs and result cards are visible.

### Steps:
1. Ensure Aurora background is active
2. Navigate to **Explore > Search**
3. Look at the search input field
4. Look at suggestion chips below the search bar
5. Type something in the search box

### Expected Results:
- Search input should have **dark purple background** `rgba(30, 20, 50, 0.75)`
- Suggestion chips should have **dark backgrounds**
- All text should be **bright white** and readable
- Purple borders should be visible

### Visual Inspection:
- Search field should be **clearly visible** against the Aurora background
- When focused, should become slightly darker
- Suggestion chips should be **distinct cards** with good contrast

✅ **PASS**: Search input and chips are highly visible
❌ **FAIL**: Search field is hard to see

---

## Test 6: Switch Back to Night Sky

**Purpose**: Verify theme reverts correctly when switching backgrounds.

### Steps:
1. Open Settings > Background
2. Click **Night Sky** background
3. Wait 2 seconds for transition
4. Open DevTools Console and run:

```javascript
const root = document.documentElement;
const style = getComputedStyle(root);
const panelBg = style.getPropertyValue('--panel-bg-current');

console.log('Current panel background:', panelBg);
console.log('✅ Reverted to Night Sky:',
  panelBg.includes('rgba(255, 255, 255, 0.05)')
);
```

### Expected Results:
- Background should transition to dark blue gradient
- Panels should become **lighter/more transparent** again
- Console should show: `✅ Reverted to Night Sky: true`

✅ **PASS**: Variables revert to Night Sky values
❌ **FAIL**: Still showing Aurora values

---

## Test 7: Persistence After Page Reload

**Purpose**: Verify Aurora contrast settings persist after reload.

### Steps:
1. Set Aurora background (Settings > Background > Aurora)
2. Close Settings
3. Navigate around the app (Explore, Create, etc.)
4. **Reload the page** (Ctrl+R or F5)
5. Wait for page to fully load
6. Observe the UI immediately after load

### Expected Results:
- Aurora background should still be active
- UI elements should have **dark purple overlays** immediately
- No flash of light/incorrect styling

### Console Verification:
```javascript
const style = getComputedStyle(document.documentElement);
console.log('Panel BG:', style.getPropertyValue('--panel-bg-current'));
console.log('✅ Aurora persisted:',
  style.getPropertyValue('--panel-bg-current').includes('rgba(20, 10, 40, 0.85)')
);
```

✅ **PASS**: Aurora theme persists after reload
❌ **FAIL**: Reverts to default or shows incorrect styling

---

## Test 8: Component Integration Test

**Purpose**: Verify migrated components actually use the new variables.

### Steps:
1. Set Aurora background
2. Navigate to Explore > Collections
3. Open DevTools, select Elements tab
4. Click the "Select element" tool (Ctrl+Shift+C)
5. Click on a collection card or filter button
6. Look at the Styles panel on the right

### Expected Results:
In the Styles panel, you should see:
```css
.collection-card {
  background: var(--card-bg-current);
  border: var(--card-border-current);
}
```

### Computed Tab Verification:
1. Click the "Computed" tab next to "Styles"
2. Search for "background-color"
3. Should show a computed value of `rgba(25, 15, 45, 0.88)` or similar purple

✅ **PASS**: Components use CSS variables, computed values are correct
❌ **FAIL**: Still using hard-coded rgba values

---

## Test 9: Hover State Verification

**Purpose**: Verify hover effects work with Aurora theme.

### Steps:
1. Set Aurora background
2. Navigate to Explore > Collections
3. Hover over filter buttons at the top
4. Hover over collection cards (if available)

### Expected Results:
- Buttons should get **slightly lighter purple** on hover
- Cards should get **slightly lighter purple** on hover
- Text should remain readable
- Transition should be smooth (0.2s)

✅ **PASS**: Hover effects work smoothly and are visible
❌ **FAIL**: No hover effect or broken styling

---

## Test 10: All Four Backgrounds Comparison

**Purpose**: Compare contrast across all backgrounds.

### Steps:
1. Test each background in sequence:
   - Night Sky
   - Aurora
   - Snowfall
   - Deep Ocean

2. For each background:
   - Go to Settings > Background
   - Select the background
   - Navigate to Explore > Collections
   - Observe card/panel visibility

3. Run this comparison script in Console for each background:

```javascript
const root = document.documentElement;
const style = getComputedStyle(root);
const settings = JSON.parse(localStorage.getItem('tka-modern-web-settings'));

console.log('Current Background:', settings.backgroundType);
console.log('Panel BG:', style.getPropertyValue('--panel-bg-current').trim());
console.log('Card BG:', style.getPropertyValue('--card-bg-current').trim());
console.log('---');
```

### Expected Results:

| Background | Panel BG | Card BG | Visibility |
|------------|----------|---------|------------|
| Night Sky | `rgba(255, 255, 255, 0.05)` | `rgba(255, 255, 255, 0.05)` | Good (dark bg) |
| **Aurora** | `rgba(20, 10, 40, 0.85)` | `rgba(25, 15, 45, 0.88)` | **Excellent (high contrast)** |
| Snowfall | `rgba(255, 255, 255, 0.05)` | `rgba(255, 255, 255, 0.05)` | Good (dark bg) |
| Deep Ocean | `rgba(255, 255, 255, 0.05)` | `rgba(25, 15, 45, 0.88)` | Good (very dark bg) |

✅ **PASS**: Aurora has significantly higher opacity values
❌ **FAIL**: All backgrounds have the same values

---

## Quick Smoke Test (5 minutes)

If you're short on time, run this abbreviated test:

1. **Set Aurora background** (Settings > Background > Aurora)
2. **Visual check**: Are UI panels noticeably darker? ✅/❌
3. **Console check**:
   ```javascript
   getComputedStyle(document.documentElement)
     .getPropertyValue('--panel-bg-current')
     .includes('rgba(20, 10, 40, 0.85)')
   ```
   Should return `true` ✅/❌
4. **Switch back to Night Sky**
5. **Console check**: Panel bg should be `rgba(255, 255, 255, 0.05)` ✅/❌
6. **Reload page** with Aurora active - does it persist? ✅/❌

All checks pass? **System is working correctly!** ✅

---

## Troubleshooting

### Issue: CSS variables are undefined
- **Solution**: Check that `app.css` has been loaded. Hard refresh (Ctrl+Shift+R)

### Issue: Variables don't update when switching backgrounds
- **Solution**: Check that ThemeService.updateTheme() is being called in MainApplication.svelte

### Issue: Components still use hard-coded colors
- **Solution**: Component hasn't been migrated yet. Check AURORA_CONTRAST_SYSTEM.md for migration guide

### Issue: Aurora background loads but contrast is still poor
- **Solution**: CSS variables might not be defined correctly. Inspect app.css:257-343

---

## Test Results Template

Copy this template and fill in your results:

```
# Aurora Contrast System Test Results
Date: ___________
Tester: ___________
Browser: ___________

Test 1 - CSS Variables Defined: ✅/❌
Test 2 - Aurora Background Switch: ✅/❌
Test 3 - Variables Update Dynamically: ✅/❌
Test 4 - Collections Panel Contrast: ✅/❌
Test 5 - Search Panel Contrast: ✅/❌
Test 6 - Switch Back to Night Sky: ✅/❌
Test 7 - Persistence After Reload: ✅/❌
Test 8 - Component Integration: ✅/❌
Test 9 - Hover State Verification: ✅/❌
Test 10 - All Backgrounds Comparison: ✅/❌

Overall Result: PASS / FAIL
Notes: ___________
```

---

## Automated Test Commands

After manual verification, you can also run:

```bash
# Unit tests
npm run test tests/unit/ThemeService.test.ts

# E2E tests (requires dev server running)
npm run test:e2e tests/e2e/aurora-contrast.spec.ts
```
