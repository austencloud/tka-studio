# Floating Filter Button Logic Explained

## The Problem
We want to maximize vertical screen space by showing a compact floating button instead of the full header, but only when it actually helps.

## The Solution
Show the floating button when **BOTH** conditions are true:
1. **Pictographs are too small** (< 80px) - user needs help clicking
2. **Height is the constraining factor** - removing header will actually help

If pictographs are small due to width constraints, showing the floating button won't help.

## How It Works

### Grid Sizing Algorithm (from OptionSizer)

The grid calculates two potential sizes:

1. **Width-based size:** How big can pictographs be based on horizontal space?
   ```
   widthPerItem = (availableWidth - gap × (columns - 1)) / columns
   ```

2. **Height-based size:** How big can pictographs be based on vertical space?
   ```
   heightPerItem = (availableHeight - gap × (rows - 1)) / rows
   ```

3. **Final size:** Use the **smaller** of the two (the limiting constraint)
   ```
   actualSize = Math.min(widthPerItem, heightPerItem)
   ```

### Detection Logic

```typescript
// Step 1: Check if pictographs are too small
const arePictographsTooSmall = pictographSize < 80;

if (!arePictographsTooSmall) {
  // Pictographs are fine, no need to help
  showFloatingButton = false
}

// Step 2: Check if height is the constraint
if (heightPerItem < widthPerItem) {
  // Grid is HEIGHT-CONSTRAINED
  // The grid wanted to be bigger based on width,
  // but was forced to shrink to fit height
  // → Use floating button to reclaim vertical space
  showFloatingButton = true
} else {
  // Grid is WIDTH-CONSTRAINED
  // Floating button won't help (need more width, not height)
  showFloatingButton = false
}

// Final: Both conditions must be true
showFloatingButton = arePictographsTooSmall && isHeightConstrained
```

## Visual Examples

### Scenario 1: Wide & Tall Container (Desktop)
```
Container: 800px wide × 600px tall
Columns: 8, Rows: 2 (16 items)
Padding: 12px each side

availableWidth = 800 - 24 = 776px
availableHeight = 600 - 24 = 576px

widthPerItem = (776 - 2×7) / 8 = 95.25px
heightPerItem = (576 - 2×1) / 2 = 287px

actualSize = min(95.25, 287) = 95.25px
isHeightConstrained = 287 < 95.25 = FALSE

Result: ✅ Header visible (width is the constraint)
```

### Scenario 2: Wide & Short Container (Landscape Phone)
```
Container: 800px wide × 250px tall
Columns: 8, Rows: 2 (16 items)
Padding: 12px each side

availableWidth = 800 - 24 = 776px
availableHeight = 250 - 24 = 226px

widthPerItem = (776 - 2×7) / 8 = 95.25px
heightPerItem = (226 - 2×1) / 2 = 112px

actualSize = min(95.25, 112) = 95.25px
isHeightConstrained = 112 > 95.25 = FALSE

Result: ✅ Header visible (width is still the constraint)
```

### Scenario 3: Narrow & Tall Container (Portrait Phone)
```
Container: 400px wide × 600px tall
Columns: 4, Rows: 4 (16 items)
Padding: 12px each side

availableWidth = 400 - 24 = 376px
availableHeight = 600 - 24 = 576px

widthPerItem = (376 - 2×3) / 4 = 92.5px
heightPerItem = (576 - 2×3) / 4 = 142.5px

actualSize = min(92.5, 142.5) = 92.5px
isHeightConstrained = 142.5 > 92.5 = FALSE

Result: ✅ Header visible (width is the constraint)
```

### Scenario 4: Narrow & SHORT Container (Cramped Layout)
```
Container: 400px wide × 300px tall
Columns: 4, Rows: 4 (16 items)
Padding: 12px each side

availableWidth = 400 - 24 = 376px
availableHeight = 300 - 24 = 276px

widthPerItem = (376 - 2×3) / 4 = 92.5px
heightPerItem = (276 - 2×3) / 4 = 67.5px

actualSize = min(92.5, 67.5) = 67.5px
isHeightConstrained = 67.5 < 92.5 = TRUE ✓

Result: 🎯 FLOATING BUTTON (height is the constraint!)
```

### Scenario 5: Your Screenshot (298px × 572px)
```
Container: 298px wide × 572px tall
Columns: 4, Rows: 4 (16 items assumed)
Padding: 12px each side

availableWidth = 298 - 24 = 274px
availableHeight = 572 - 24 = 548px

widthPerItem = (274 - 2×3) / 4 = 67px
heightPerItem = (548 - 2×3) / 4 = 135.5px

actualSize = min(67, 135.5) = 67px

Check 1: arePictographsTooSmall = 67 < 80 = TRUE ✓
Check 2: isHeightConstrained = 135.5 < 67 = FALSE ✗

Result: ✅ Header visible (width-constrained, floating button won't help)
Why: Even though pictographs are small (67px), they're small due to
      width constraint. Removing header won't make them bigger.
```

### Scenario 6: Small Pictographs + Height-Constrained (300px × 250px)
```
Container: 300px wide × 250px tall
Columns: 4, Rows: 4 (16 items)
Padding: 12px each side

availableWidth = 300 - 24 = 276px
availableHeight = 250 - 24 = 226px

widthPerItem = (276 - 2×3) / 4 = 67.5px
heightPerItem = (226 - 2×3) / 4 = 55px

actualSize = min(67.5, 55) = 55px

Check 1: arePictographsTooSmall = 55 < 80 = TRUE ✓
Check 2: isHeightConstrained = 55 < 67.5 = TRUE ✓

Result: 🎯 FLOATING BUTTON! (Both conditions met)
Why: Pictographs are small (55px) AND height is the limiting factor.
     Removing the ~52px header will give us ~302px total height,
     which could increase pictographs to ~65px - a 18% improvement!
```

### Scenario 7: Large Pictographs + Height-Constrained (800px × 300px)
```
Container: 800px wide × 300px tall
Columns: 8, Rows: 2 (16 items)
Padding: 12px each side

availableWidth = 800 - 24 = 776px
availableHeight = 300 - 24 = 276px

widthPerItem = (776 - 2×7) / 8 = 95.25px
heightPerItem = (276 - 2×1) / 2 = 137px

actualSize = min(95.25, 137) = 95.25px

Check 1: arePictographsTooSmall = 95.25 < 80 = FALSE ✗
Check 2: isHeightConstrained = N/A (check 1 failed)

Result: ✅ Header visible (pictographs are comfortable size)
Why: Even though layout is technically width-constrained,
     pictographs at 95px are plenty big enough. No help needed.
```

## Why This Works Better

### Old Approach (Fixed Height Threshold)
❌ Arbitrary cutoff (e.g., "if height < 300px")
❌ Doesn't consider actual content
❌ Doesn't adapt to different grid configurations
❌ Can trigger at wrong times

### New Approach (Dual-Condition: Size + Constraint)
✅ **Pragmatic:** Only helps when pictographs are uncomfortably small
✅ **Smart:** Only triggers when removing header will actually help
✅ **Adaptive:** Works with 4-column, 8-column, any number of items
✅ **Efficient:** Early exit if pictographs are already comfortable
✅ **User-focused:** Based on clickability (< 80px is hard to tap)
✅ **Result-oriented:** Won't show button if it can't improve things

## Edge Cases Handled

1. **No content:** Returns `false` (no floating button)
2. **Service not ready:** Returns `false` (safe default)
3. **Very few items:** Rows calculated correctly
4. **Many items:** Rows increase, height constraint more likely
5. **Different column modes:** 4-column vs 8-column handled automatically

## Summary

**The floating button appears when pictographs are uncomfortably small (< 80px) AND the grid is height-constrained.**

This dual-condition approach ensures we:
1. **Only help when needed:** Pictographs < 80px are hard to click
2. **Only help when possible:** Header removal must actually improve things
3. **Never help pointlessly:** If width-constrained, floating button won't help

### Decision Tree:
```
Are pictographs < 80px?
├─ NO → Show header (pictographs are fine)
└─ YES → Is height the constraint?
   ├─ NO → Show header (width-constrained, can't help)
   └─ YES → Show floating button! (Will improve pictograph size)
```

This approach is:
- **Pragmatic:** Based on actual user needs (clickability)
- **Semantic:** Based on actual layout constraints
- **Adaptive:** Works across all screen sizes and configurations
- **Robust:** Tied to the same logic that sizes the grid
- **Smart:** Only optimizes when optimization is both needed AND helpful
