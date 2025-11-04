# Aurora Background Contrast System

## Overview

The Aurora animated background uses beautiful, vibrant pastel colors (purples, pinks, blues) that create a light, ethereal atmosphere. However, this light background can make UI elements like cards, panels, and text harder to see.

This document describes the **Adaptive Contrast System** that automatically enhances visibility when the Aurora background is active.

## Problem Statement

When the Aurora background is selected:
- The gradient uses light colors: `#667eea`, `#764ba2`, `#f093fb`, `#f5576c`, `#4facfe`
- UI cards with `rgba(255, 255, 255, 0.05)` backgrounds appear washed out
- Text contrast is reduced
- Interactive elements are less noticeable

## Solution: Background-Aware CSS Variables

We've implemented a system that applies **darker, more opaque overlays** specifically for the Aurora background while keeping the existing light overlays for dark backgrounds (Night Sky, Deep Ocean, etc.).

### How It Works

1. **CSS Variables** ([app.css:257-343](src/app.css#L257-L343))
   - Each background type (nightSky, aurora, snowfall, deepOcean) has its own set of themed variables
   - Variables are defined for: panels, cards, text, inputs, and buttons
   - Current theme variables (e.g., `--card-bg-current`) point to the active background's values

2. **ThemeService** ([ThemeService.ts:46-68](src/lib/shared/theme/services/ThemeService.ts#L46-L68))
   - Automatically updates CSS variables when background changes
   - Maps background type to corresponding theme variables
   - Called from MainApplication.svelte via `$effect`

3. **Component Integration**
   - Components use `var(--card-bg-current)` instead of hard-coded `rgba()` values
   - Styles automatically adapt when background changes
   - No JavaScript required in components

## Available CSS Variables

### Panel Backgrounds
```css
--panel-bg-nightSky: rgba(255, 255, 255, 0.05);
--panel-bg-aurora: rgba(20, 10, 40, 0.85);    /* Dark purple overlay */
--panel-bg-snowfall: rgba(255, 255, 255, 0.05);
--panel-bg-deepOcean: rgba(255, 255, 255, 0.05);

--panel-border-nightSky: rgba(255, 255, 255, 0.1);
--panel-border-aurora: rgba(168, 85, 247, 0.3); /* Purple-tinted border */
--panel-border-snowfall: rgba(255, 255, 255, 0.1);
--panel-border-deepOcean: rgba(255, 255, 255, 0.1);

--panel-hover-nightSky: rgba(255, 255, 255, 0.08);
--panel-hover-aurora: rgba(30, 15, 60, 0.9);    /* Darker on hover */
--panel-hover-snowfall: rgba(255, 255, 255, 0.08);
--panel-hover-deepOcean: rgba(255, 255, 255, 0.08);
```

### Card Backgrounds
```css
--card-bg-nightSky: rgba(255, 255, 255, 0.05);
--card-bg-aurora: rgba(25, 15, 45, 0.88);       /* Deep dark purple */
--card-bg-snowfall: rgba(255, 255, 255, 0.05);
--card-bg-deepOcean: rgba(255, 255, 255, 0.05);

--card-border-nightSky: rgba(255, 255, 255, 0.1);
--card-border-aurora: rgba(168, 85, 247, 0.35);
--card-border-snowfall: rgba(255, 255, 255, 0.1);
--card-border-deepOcean: rgba(255, 255, 255, 0.1);

--card-hover-nightSky: rgba(255, 255, 255, 0.08);
--card-hover-aurora: rgba(35, 20, 65, 0.92);
--card-hover-snowfall: rgba(255, 255, 255, 0.08);
--card-hover-deepOcean: rgba(255, 255, 255, 0.08);
```

### Text Colors
```css
--text-primary-nightSky: #ffffff;
--text-primary-aurora: #ffffff;                 /* White text on dark overlays */
--text-primary-snowfall: #ffffff;
--text-primary-deepOcean: #ffffff;

--text-secondary-nightSky: rgba(255, 255, 255, 0.7);
--text-secondary-aurora: rgba(255, 255, 255, 0.85);  /* Brighter for readability */
--text-secondary-snowfall: rgba(255, 255, 255, 0.7);
--text-secondary-deepOcean: rgba(255, 255, 255, 0.7);
```

### Input/Search Fields
```css
--input-bg-nightSky: rgba(255, 255, 255, 0.05);
--input-bg-aurora: rgba(30, 20, 50, 0.75);
--input-bg-snowfall: rgba(255, 255, 255, 0.05);
--input-bg-deepOcean: rgba(255, 255, 255, 0.05);

--input-border-nightSky: rgba(255, 255, 255, 0.1);
--input-border-aurora: rgba(168, 85, 247, 0.4);
--input-border-snowfall: rgba(255, 255, 255, 0.1);
--input-border-deepOcean: rgba(255, 255, 255, 0.1);

--input-focus-nightSky: rgba(255, 255, 255, 0.08);
--input-focus-aurora: rgba(40, 25, 70, 0.85);
--input-focus-snowfall: rgba(255, 255, 255, 0.08);
--input-focus-deepOcean: rgba(255, 255, 255, 0.08);
```

### Active Buttons/Filters
```css
--button-active-nightSky: rgba(255, 255, 255, 0.15);
--button-active-aurora: rgba(88, 28, 135, 0.75);     /* Rich purple for active state */
--button-active-snowfall: rgba(255, 255, 255, 0.15);
--button-active-deepOcean: rgba(255, 255, 255, 0.15);
```

### Current Theme Variables (Auto-Updated)
```css
--panel-bg-current
--panel-border-current
--panel-hover-current

--card-bg-current
--card-border-current
--card-hover-current

--text-primary-current
--text-secondary-current

--input-bg-current
--input-border-current
--input-focus-current

--button-active-current
```

## Usage Examples

### Before (Hard-coded values)
```css
.my-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
}

.my-card:hover {
  background: rgba(255, 255, 255, 0.08);
}
```

### After (Theme-aware)
```css
.my-card {
  background: var(--card-bg-current);
  border: var(--card-border-current);
  color: var(--text-primary-current);
}

.my-card:hover {
  background: var(--card-hover-current);
}
```

### Input Fields
```css
.search-input {
  background: var(--input-bg-current);
  border: var(--input-border-current);
  color: var(--text-primary-current);
}

.search-input:focus {
  background: var(--input-focus-current);
}
```

### Filter Buttons
```css
.filter-button {
  background: var(--panel-bg-current);
  border: var(--panel-border-current);
  color: var(--text-secondary-current);
}

.filter-button:hover {
  background: var(--panel-hover-current);
  color: var(--text-primary-current);
}

.filter-button.active {
  background: var(--button-active-current);
}
```

## Components Already Updated

The following components have been migrated to use the new system:

1. **CollectionsExplorePanel.svelte**
   - Search inputs
   - Filter buttons
   - Collection cards

2. **SearchExplorePanel.svelte**
   - Search inputs
   - Filter tabs
   - Suggestion chips
   - Result items

## Adding Aurora Support to New Components

When creating new UI components:

1. **Use theme variables instead of hard-coded rgba values**
   ```css
   /* ❌ Don't do this */
   background: rgba(255, 255, 255, 0.05);

   /* ✅ Do this */
   background: var(--card-bg-current);
   ```

2. **Choose the appropriate variable type:**
   - Use `--panel-*` for navigation, toolbars, sidebars
   - Use `--card-*` for content cards, list items, results
   - Use `--input-*` for form fields, search boxes
   - Use `--button-active-*` for selected/active state buttons
   - Use `--text-primary-current` for main text
   - Use `--text-secondary-current` for secondary/muted text

3. **Test with Aurora background enabled**
   - Navigate to Settings > Background > Animated > Aurora
   - Verify your component has good contrast
   - Check that text is readable
   - Ensure interactive elements are noticeable

## Design Rationale: Aurora-Specific Colors

The Aurora theme uses **dark purple overlays** (`rgba(20-40, 10-25, 40-70, 0.75-0.92)`) because:

1. **Complementary to Aurora colors**: Purple complements the pink/blue aurora gradient
2. **High opacity (75-92%)**: Provides strong contrast against the light background
3. **Maintains theme consistency**: Purple borders (`rgba(168, 85, 247, *)`) tie into the aurora palette
4. **Preserves visual hierarchy**: Cards are darker than panels, active elements are richest purple

## Performance Considerations

- CSS variables are natively supported by all modern browsers
- No JavaScript execution overhead after initial theme application
- Theme changes are instant (CSS property updates)
- Variables cascade naturally through component tree

## Future Enhancements

Potential improvements for consideration:

1. **Add more backgrounds with theme support** (e.g., a bright "Daylight" theme)
2. **Per-component theme overrides** for special cases
3. **Automatic contrast calculation** based on background luminance
4. **Theme preview** in background settings

## Testing Checklist

When making UI changes, test with all backgrounds:

- [ ] Night Sky (dark blue - default)
- [ ] **Aurora** (light purple/pink - requires high contrast)
- [ ] Snowfall (dark blue-black)
- [ ] Deep Ocean (very dark blue)

## Related Files

- [app.css:257-343](c:\_TKA-STUDIO\src\app.css#L257-L343) - CSS variable definitions
- [ThemeService.ts](c:\_TKA-STUDIO\src\lib\shared\theme\services\ThemeService.ts) - Theme management logic
- [MainApplication.svelte:263-270](c:\_TKA-STUDIO\src\lib\shared\application\components\MainApplication.svelte#L263-L270) - Theme initialization
- [BackgroundGradients.ts](c:\_TKA-STUDIO\src\lib\shared\background\shared\domain\constants\BackgroundGradients.ts) - Background gradient definitions

## Questions or Issues?

If you encounter visibility issues with the Aurora background or have suggestions for improvement, please create an issue with:
- Component name
- Screenshot with Aurora background
- Description of the visibility problem
- Suggested color values (if applicable)
