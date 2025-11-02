# Floating Filter Button - Screen Size Test Plan

## Test Overview
Verify that the floating filter button appears/disappears appropriately when the grid becomes height-constrained with smooth transitions and no overlapping issues.

## Detection Mechanism
The grid sizing algorithm tries to maximize width first, but if that would cause vertical overflow, it shrinks to fit height. We detect this condition:

```typescript
widthPerItem = (availableWidth - gap * (columns - 1)) / columns
heightPerItem = (availableHeight - gap * (rows - 1)) / rows

isHeightConstrained = heightPerItem < widthPerItem

Floating button shows when: isHeightConstrained === true
```

**This means:** The floating button appears when the grid has been forced to shrink due to vertical space constraints, exactly when reclaiming header space would be most beneficial.

## Key Insight
- **Width-constrained:** Grid can expand to fill width → Header is fine
- **Height-constrained:** Grid shrunk to fit height → Use floating button to maximize vertical space

## Test Scenarios

### 1. **Desktop/Tablet - Large Container (500px+ height)**
**Expected:** Full header visible, no floating button
- [ ] Header appears at top with filter icon/chevron
- [ ] No floating button in top-left corner
- [ ] Header is fully interactive
- [ ] Smooth transitions when resizing

### 2. **Medium Container (300px - 500px height)**
**Expected:** Behavior depends on pictograph size
- [ ] With default 144px pictographs: Full header visible (300px > 244px threshold)
- [ ] Header remains interactive
- [ ] No floating button visible

### 3. **Small Container (200px - 300px height)**
**Expected:** Transitions based on exact height and pictograph size
- [ ] At 250px with 144px pictographs: Full header visible (250px > 244px)
- [ ] At 240px with 144px pictographs: Floating button appears (240px < 244px)
- [ ] Smooth fade transition between header and button (200ms)
- [ ] No overlap during transition

### 4. **Very Small Container (< 200px height)**
**Expected:** Floating button always visible
- [ ] Floating button appears in top-left (8px from edges)
- [ ] No header visible
- [ ] Button is fully interactive
- [ ] No layout shift or overlap

### 5. **Dynamic Pictograph Resizing**
**Expected:** Threshold adapts in real-time
- [ ] When pictographs shrink: threshold decreases, header may appear
- [ ] When pictographs grow: threshold increases, button may appear
- [ ] Smooth transitions during changes
- [ ] No visual glitches

### 6. **Transition States**
**Test the switch between header and floating button:**
- [ ] Fade duration is 200ms (feels smooth, not jarring)
- [ ] No overlap between header and floating button during transition
- [ ] Content below doesn't jump or shift
- [ ] Z-index is correct (floating button at z-index: 100)

### 7. **Filter Panel Interaction**
**With floating button:**
- [ ] Clicking floating button opens filter panel
- [ ] Button visual state changes when panel is open
- [ ] Filter indicator shows when continuous mode active
- [ ] Panel closes properly

**With header:**
- [ ] Clicking header opens filter panel
- [ ] Chevron rotates when panel is open
- [ ] All header interactions work normally

### 8. **Edge Cases**
- [ ] Container height exactly at threshold (e.g., 244px): behavior is consistent
- [ ] Rapid window resizing: no flickering or rapid switching
- [ ] Container height = 0: no floating button appears (safety check)
- [ ] Very wide but short containers (landscape mode): floating button appears correctly

## Device-Specific Tests

### iPhone SE (375x667, landscape: 667x375)
- **Portrait:** ~667px height → Header visible ✓
- **Landscape:** ~375px height → Depends on pictograph size, likely header visible

### iPhone 12/13 (390x844, landscape: 844x390)
- **Portrait:** ~844px height → Header visible ✓
- **Landscape:** ~390px height → Depends on pictograph size

### iPad (768x1024, landscape: 1024x768)
- **Both orientations:** Header visible ✓

### Galaxy Z Fold 6 (unfolded: 884x2208)
- **All orientations:** Header visible ✓

### Desktop (1920x1080)
- **All sizes:** Header visible ✓

## Visual Checklist

### Header Mode
- ✓ Header spans full width
- ✓ Header background has blur effect
- ✓ Center shows formatted section title
- ✓ Right shows chevron icon
- ✓ Clickable area covers entire header

### Floating Button Mode
- ✓ Button positioned at top-left (8px, 8px)
- ✓ Button size: 44x44px (touch-friendly)
- ✓ Button has glassmorphic style
- ✓ Filter indicator shows when continuous mode active
- ✓ Hover effects work (on desktop)
- ✓ No overlap with content

### Transition Quality
- ✓ 200ms fade feels smooth
- ✓ No "pop" or jarring changes
- ✓ Content area doesn't shift during transition
- ✓ Both elements never visible simultaneously

## Automated Test Commands

```bash
# Check TypeScript compilation
npx tsc --noEmit

# Run Svelte checks
npx svelte-check --threshold error

# Visual testing (manual)
npm run dev
# Then test with browser DevTools responsive mode
```

## Manual Testing Steps

1. **Open DevTools** (F12)
2. **Enable Responsive Design Mode** (Ctrl+Shift+M / Cmd+Shift+M)
3. **Test each dimension:**
   - Start at 1920x1080 (header visible)
   - Slowly decrease height to 500px (header still visible)
   - Continue to 300px (header still visible)
   - Continue to 244px (threshold - button should appear)
   - Continue to 200px (button visible)
   - Return to 300px (header should reappear)

4. **Watch for:**
   - Smooth 200ms fade transitions
   - No overlapping during transition
   - No content jumping
   - Correct interactive behavior

## Known Good States

✅ **Height > 244px (with 144px pictographs):** Header visible, no button
✅ **Height < 244px (with 144px pictographs):** Button visible, no header
✅ **Transition:** 200ms fade, no overlap
✅ **Z-index:** Floating button (100) above content

## Potential Issues to Watch For

⚠️ **Header and button both visible** → Check conditional logic
⚠️ **Flickering during resize** → May need debouncing (check if issue exists)
⚠️ **Content jumps when switching** → Check flex layout and spacing
⚠️ **Floating button behind content** → Check z-index values
⚠️ **Transition feels choppy** → May need to adjust duration

---

**Test Date:** _________
**Tester:** _________
**Browser/Device:** _________
**Result:** ☐ Pass ☐ Fail
**Notes:** _________
