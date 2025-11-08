# HMR Testing Steps

## Immediate Fix (Browser Cache)

1. Press `Ctrl + Shift + R` (hard refresh)
2. Open DevTools (F12)
3. Go to **Network** tab → Check "Disable cache"
4. Refresh again

## If That Doesn't Work (Clear All Cache)

1. Press F12 (DevTools)
2. Go to **Application** tab
3. Click **Storage** → **Clear site data**
4. Close and reopen browser tab
5. Navigate to `http://localhost:5173`

## Verify CSS Changes

Open DevTools → **Elements** tab → Find `.floating-filter-button`:

- Should see: `top: 0;` and `left: 0;`
- If you see: `top: 8px;` and `left: 8px;` → Cache issue

## Nuclear Option (Restart Dev Server)

```bash
# Kill the dev server (Ctrl+C)
# Delete Vite cache
rm -rf node_modules/.vite
rm -rf .svelte-kit

# Restart
npm run dev
```

## Test the Button Position

1. Resize browser to small height (e.g., 300px × 250px)
2. Make pictographs < 80px (narrow + short container)
3. Button should appear **flush** with top-left corner (no gap)

## Expected CSS (After Hard Refresh)

```css
.floating-filter-button {
  position: absolute;
  top: 0; /* ← Should be 0, not 8px */
  left: 0; /* ← Should be 0, not 8px */
  z-index: 100;
}
```
