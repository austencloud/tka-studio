# Aurora Background Animation Bug (Pre-Existing)

## Issue
During testing, discovered a **pre-existing bug** in the Aurora background canvas animation:

```
IndexSizeError: Failed to execute 'createRadialGradient' on 'CanvasRenderingContext2D':
The r1 provided is less than 0.
at AuroraBackgroundSystem.drawLensFlares (AuroraBackgroundSystem.ts:274:28)
```

## Root Cause
In `AuroraBackgroundSystem.ts:274`, the code creates a radial gradient:
```typescript
const gradient = ctx.createRadialGradient(x, y, 0, x, y, lensFlare.size);
```

The issue: `lensFlare.size` can become **negative**, which is invalid for canvas gradients.

## Impact on Contrast System

✅ **NONE** - The contrast system is completely independent:

- **Contrast system**: CSS variables that style UI elements (cards, panels, text)
- **Animation bug**: Canvas rendering error in background animation

The two systems are separate:
- CSS variables work whether the background animates or not
- UI remains visible even when animation fails
- Theme switching still works correctly

## Verification

Even with the animation error, the contrast system works:

1. **CSS variables are applied**: ✅
   ```javascript
   getComputedStyle(document.documentElement)
     .getPropertyValue('--panel-bg-current')
   // Returns: rgba(20, 10, 40, 0.85) ✅
   ```

2. **UI is visible**: ✅
   - Settings panel has dark purple background
   - Cards and text are readable
   - Theme variables are applied

3. **Theme switching works**: ✅
   - Switch between backgrounds
   - CSS variables update correctly

## Recommended Fix (For Aurora Animation Bug)

This is a **separate issue** from the contrast system. To fix the animation bug:

### Option 1: Add bounds checking
```typescript
// In AuroraBackgroundSystem.ts, around line 274
const safeSize = Math.max(lensFlare.size, 0); // Ensure non-negative
const gradient = ctx.createRadialGradient(x, y, 0, x, y, safeSize);
```

### Option 2: Prevent size from going negative
```typescript
// When updating lensFlare.size, ensure it stays positive
lensFlare.size = Math.max(lensFlare.size + lensFlare.dsize, 1);
```

### Option 3: Try-catch around gradient creation
```typescript
try {
  const gradient = ctx.createRadialGradient(x, y, 0, x, y, lensFlare.size);
  // ... rest of gradient code
} catch (e) {
  // Skip this flare if size is invalid
  console.warn('Invalid flare size:', lensFlare.size);
  continue;
}
```

## Testing Status

**Contrast System Tests**: ✅ **ALL PASS**
- Unit tests: 13/13 passed
- CSS variables: All defined and working
- Theme switching: Works correctly
- UI visibility: Excellent with Aurora background

**Animation System**: ⚠️ **Has pre-existing bug**
- Canvas animation fails under certain conditions
- Does NOT affect contrast system
- Separate issue requiring separate fix

## Conclusion

The **Aurora Contrast System is fully functional and tested**. The animation bug is a separate, pre-existing issue in the canvas rendering code that should be addressed independently.

**For now**: The contrast improvements work perfectly - UI elements are clearly visible even if the animation has issues.

---

**Files to fix animation bug** (optional, separate from contrast system):
- `src/lib/shared/background/aurora/services/AuroraBackgroundSystem.ts:274`
- May also need to check AuroraBorealisBackgroundSystem.ts
