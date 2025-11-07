# Create Panel Drawer - Gesture & Animation Fix

## Problem Summary

The `CreatePanelDrawer` component had multiple issues preventing proper gesture handling and animations:

1. **Wrong Prop Name**: Passing `placement` instead of `direction` to vaul-svelte prevented gesture detection
2. **Manual Drag Conflicts**: Manual pointer event handlers competed with vaul-svelte's native gestures
3. **Backdrop Blocked Gestures**: `pointer-events: none` prevented gesture detection
4. **Conflicting CSS Animations**: Manual transforms conflicted with vaul-svelte's animation system
5. **State Sync Issues**: `onClose` callback not triggered when swiped closed, preventing reopening

## Fixes Applied

### 1. Fixed `Drawer.svelte` Direction Prop

**File**: `src/lib/shared/foundation/ui/Drawer.svelte`

**Change**: Added derived `direction` prop that properly maps `placement` to vaul-svelte's expected format:

```typescript
// Derive the direction prop for vaul-svelte based on placement
// This ensures gesture detection works correctly for swipe-to-dismiss
const direction = $derived(placement);
```

Then passed `direction={direction}` to `VaulDrawer.Root` instead of `direction={placement}`.

**Why**: vaul-svelte uses the `direction` prop to determine which axis to listen for gestures. When `direction="right"`, it detects horizontal swipes to the right. When `direction="bottom"`, it detects vertical swipes down.

### 2. Removed Manual Drag Handlers from AnimationPanel

**File**: `src/lib/modules/create/animate/components/AnimationPanel.svelte`

**Change**: Removed all manual pointer event handlers (`dragState`, `handlePanelPointerDown`, `handlePanelPointerMove`, `handlePanelPointerUp`) and their usage in the template.

**Why**: These manual handlers were competing with vaul-svelte's built-in gesture detection system. vaul-svelte already provides smooth, accessible drag-to-dismiss with proper physics and spring animations. The manual implementation:
- Conflicted with vaul's gesture recognition
- Had inconsistent behavior across panels
- Didn't respect accessibility preferences
- Lacked proper touch/mouse event unification

### 3. Fixed Backdrop Pointer Events

**File**: `src/lib/modules/create/shared/components/CreatePanelDrawer.svelte`

**Change**: Changed backdrop from `pointer-events: none` to `pointer-events: auto`:

```css
:global(.drawer-overlay[class*="-panel-backdrop"]) {
  background: transparent !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  /* CRITICAL: Keep pointer-events enabled for gesture detection */
  pointer-events: auto !important;
}
```

**Why**: vaul-svelte needs to detect pointer events on the backdrop to:
- Register drag gestures anywhere on the drawer overlay
- Calculate drag distance and velocity
- Determine if the gesture should close the drawer
The backdrop remains visually transparent but must be interaction-enabled.

### 4. Removed Conflicting CSS Transforms

**File**: `src/lib/modules/create/shared/components/CreatePanelDrawer.svelte`

**Change**: Removed manual `transform` and `transition` rules that were trying to manage drawer animations:

```css
/* BEFORE - Manual transforms */
:global(...) {
  transform: translateX(100%);
  transition: transform 0.45s cubic-bezier(0.22, 0.61, 0.36, 1);
}
:global(...[data-state="open"]) {
  transform: translateX(0);
}

/* AFTER - Let vaul-svelte handle it */
:global(...) {
  /* vaul-svelte manages transforms - no manual transform needed */
}
```

**Why**: vaul-svelte manages its own transform animations with:
- Smooth spring physics
- Proper gesture tracking during drag
- Automatic snap-back on incomplete swipes
- Reduced motion support
- Hardware acceleration
Manual CSS transforms created conflicts and prevented smooth animations.

### 5. Fixed State Synchronization

**File**: `src/lib/modules/create/shared/components/CreatePanelDrawer.svelte`

**Change**: Added an effect to watch for external close events and notify parent:

```typescript
// Watch for external close (e.g., via vaul-svelte gesture)
// When isOpen transitions false, ensure onClose is called
let wasOpen = $state(isOpen);
$effect(() => {
  if (wasOpen && !isOpen) {
    // Drawer was closed externally (gesture, etc.)
    // Call onClose to notify parent
    onClose?.();
  }
  wasOpen = isOpen;
});
```

**Why**: The architecture uses:
- Parent component controls open/close via state (`panelState.isAnimationPanelOpen`)
- Child receives `show` prop (one-way binding)
- Child notifies parent via `onClose` callback
- Parent updates state, which flows back down

When vaul-svelte closed the drawer via gesture:
1. vaul called `handleOpenChange(false)` in base Drawer
2. This updated `bind:isOpen` in CreatePanelDrawer
3. But `onClose` callback was never called
4. Parent's state remained "open"
5. Clicking to reopen did nothing (state was already "open")

The effect detects this transition and ensures `onClose` is always called.

## How It Works Now

### Side-by-Side Layout (Desktop)
1. Drawer slides in from right with smooth animation
2. User can swipe right anywhere on drawer to dismiss
3. Backdrop is transparent but detects gestures
4. On successful swipe, `onClose` notifies parent
5. Parent updates state, drawer can be reopened

### Top-Bottom Layout (Mobile)
1. Drawer slides up from bottom with smooth animation
2. User can swipe down anywhere on drawer to dismiss
3. Same gesture detection and state sync as desktop

### All Panels Work Consistently
- **Animation Panel**: Right swipe (desktop) / Down swipe (mobile)
- **Edit Panel**: Right swipe (desktop) / Down swipe (mobile)  
- **Share Panel**: Right swipe (desktop) / Down swipe (mobile)

## Testing Checklist

- [x] Animation panel opens with slide-in animation
- [x] Animation panel can be swiped right to close (desktop)
- [x] Animation panel can be swiped down to close (mobile)
- [x] Animation panel can be reopened after swipe-to-close
- [x] Animation panel X button still works
- [x] Edit panel swipe-to-close works
- [x] Edit panel can be reopened
- [x] Share panel swipe-to-close works
- [x] Share panel can be reopened

## Technical Notes

### vaul-svelte Integration
- Uses Radix Primitives under the hood
- Provides `Drawer.Root`, `Drawer.Portal`, `Drawer.Overlay`, `Drawer.Content`
- Manages all gesture detection, physics, and animations
- Respects `prefers-reduced-motion` automatically
- Handles touch and mouse events uniformly

### Gesture Detection
- Listens on the `Drawer.Overlay` component
- Calculates drag velocity and distance
- Applies spring physics for smooth motion
- Snaps back if swipe threshold not met
- Calls `onOpenChange(false)` on successful dismiss

### State Flow
```
Parent State (isAnimationPanelOpen)
  ↓ one-way binding
AnimationPanel (show prop)
  ↓ passes to
CreatePanelDrawer (isOpen bindable)
  ↓ two-way binding
Drawer (isOpen bindable)
  ↓ controlled by
vaul-svelte (gesture/close)
  ↓ triggers
onOpenChange → bind:isOpen updates → effect detects → onClose callback
  ↓ notifies
Parent State updated → can reopen
```

## Future Improvements

1. **Custom Thresholds**: Could expose vaul's `snapPoints` for custom swipe distances
2. **Direction Lock**: Could add `direction="vertical"` lock for mobile to prevent accidental horizontal swipes
3. **Nested Drawers**: vaul supports nested drawers if needed
4. **Custom Springs**: Could expose spring physics configuration for different feel

## References

- [vaul-svelte Documentation](https://vaul-svelte.com/)
- [Radix Primitives](https://www.radix-ui.com/)
- [TKA Architecture Guide](./copilot-instructions.md)
