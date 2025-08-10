# Safe Area Inset Implementation

This document explains the implementation of safe area insets in the Kinetic Constructor web application to properly handle device-specific screen obstructions like notches, punch holes, Dynamic Island, and other hardware elements.

## Overview

Modern mobile devices often have hardware elements that intrude into the display area, such as:

- iPhone notch and Dynamic Island
- Android punch-hole cameras
- Rounded corners
- Home indicators (iPhone X and newer)

To ensure our UI elements don't get obscured by these hardware features, we've implemented comprehensive safe area inset handling using CSS environment variables.

## Implementation Details

### 1. Viewport Meta Tag

The viewport meta tag in `app.html` includes `viewport-fit=cover` to enable safe area inset detection:

```html
<meta
  name="viewport"
  content="width=device-width, initial-scale=1.0, user-scalable=no, viewport-fit=cover"
/>
```

### 2. CSS Variables

We've created a dedicated CSS file (`src/lib/styles/safe-area.css`) that defines CSS custom properties mapping to the environment variables:

```css
:root {
  /* Direct mapping to environment variables with fallbacks */
  --safe-inset-top: env(safe-area-inset-top, 0px);
  --safe-inset-right: env(safe-area-inset-right, 0px);
  --safe-inset-bottom: env(safe-area-inset-bottom, 0px);
  --safe-inset-left: env(safe-area-inset-left, 0px);

  /* Combined variables that integrate with existing spacing system */
  --content-padding-top: calc(var(--base-spacing) + var(--safe-inset-top));
  --content-padding-right: calc(var(--base-spacing) + var(--safe-inset-right));
  --content-padding-bottom: calc(
    var(--base-spacing) + var(--safe-inset-bottom)
  );
  --content-padding-left: calc(var(--base-spacing) + var(--safe-inset-left));
}
```

### 3. Component Updates

We've updated the following components to respect safe area insets:

#### Sequence Overlay Components

- `SequenceOverlay.svelte`: Added padding to respect safe area insets
- `SequenceOverlayContent.svelte`: Updated layout calculations to account for safe area insets
- Close button positioning adjusted to avoid notches and other obstructions

#### UI Controls

- `BeatFrame.svelte`: Added padding to respect safe area insets on all sides
- `CurrentWordLabel.svelte`: Added horizontal padding to respect left and right safe area insets
- `SettingsButton.svelte`: Positioned very close to the top-left corner (2px from top, 3px from left) while still respecting top safe area inset
- `ClearSequenceButton.svelte`: Positioned to respect bottom safe area inset only (left inset not needed for corner buttons)
- `RemoveBeatButton.svelte`: Positioned to respect bottom safe area inset only (left inset not needed for corner buttons)
- `SequenceOverlayButton.svelte`: Positioned to respect bottom safe area inset only (right inset not needed for corner buttons)
- `ShareButton.svelte`: Positioned very close to the top-right corner (2px from top, 3px from right) while still respecting top safe area inset

### 4. Debug Visualizer

For development purposes, we've created a `SafeAreaVisualizer.svelte` component that:

- Renders colored outlines showing the boundaries of safe area insets
- Displays the current inset values in pixels
- Can be toggled on/off via a development flag

## Usage

### Applying Safe Area Insets to New Components

To apply safe area insets to new components, you can:

1. Use the CSS variables directly:

```css
.my-component {
  padding-top: var(--safe-inset-top, 0px);
  /* or */
  padding: var(--safe-inset-top, 0px) var(--safe-inset-right, 0px) var(
      --safe-inset-bottom,
      0px
    ) var(--safe-inset-left, 0px);
}
```

2. Use the utility classes:

```html
<div class="safe-area-padding">Content with safe area padding on all sides</div>
<div class="safe-area-padding-top">Content with safe area padding on top</div>
```

3. For fixed position elements:

```css
.fixed-element {
  position: fixed;
  top: var(--safe-position-top);
  right: var(--safe-position-right);
}
```

4. For dynamic positioning that respects both design margins and safe area insets:

```css
.my-button {
  position: absolute;
  top: max(10px, var(--safe-inset-top, 0px));
  right: max(10px, var(--safe-inset-right, 0px));
}
```

### Enabling the Debug Visualizer

To enable the safe area visualizer during development:

1. In `src/routes/+layout.svelte`, find the SafeAreaVisualizer component:

```html
{#if import.meta.env.DEV}
<SafeAreaVisualizer enabled="{false}" />
{/if}
```

2. Change `enabled={false}` to `enabled={true}` to see the safe area insets.

## Testing

The implementation should be tested on:

- iPhone models with notches (iPhone X through 14)
- iPhone models with Dynamic Island (iPhone 14 Pro and newer)
- Android devices with various notch/punch-hole designs
- Both portrait and landscape orientations

## Corner Button Optimization

After analyzing typical safe area inset patterns on mobile devices, we've optimized the implementation for corner buttons:

1. **Top insets**: Applied only to the top edge of buttons in the top corners, as notches and cameras typically affect the center-top of the screen, not the corners.

2. **Bottom insets**: Applied to all buttons along the bottom edge, as home indicators and gesture areas typically affect the entire bottom edge.

3. **Left/Right insets**: Not applied to corner buttons, as these insets typically affect the curved edges of the screen, not the corners themselves.

This optimization ensures that we only apply safe area insets where they're actually needed, avoiding unnecessary spacing in the corners where hardware elements rarely intrude.

## Browser Compatibility

The `env()` function is supported in:

- Safari iOS 11.2+
- Chrome for Android 69+
- Firefox for Android 62+

For browsers that don't support `env()`, we provide fallback values of `0px` to ensure the layout still works correctly.
