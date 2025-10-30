# Haptic Feedback Standards
**Last Updated**: 2025-10-30

---

## Overview
This document defines the **standard haptic feedback patterns** for TKA to ensure consistent tactile feedback across the application.

---

## Haptic Feedback Patterns

### Defined in `HapticFeedbackService.ts`:

| Type | Pattern (ms) | Total Duration | Use Case |
|------|-------------|----------------|----------|
| **`navigation`** | `[35]` | 35ms | Lightest - Route changes, tabs, links |
| **`selection`** | `[70]` | 70ms | Medium - Buttons, modals, selections |
| **`success`** | `[100, 30, 50]` | 180ms | Strong pattern - Confirmations, saves |
| **`warning`** | `[60, 0, 60]` | 120ms | Double tap - Cautions, destructive previews |
| **`error`** | `[100, 0, 100, 0, 100]` | 300ms | Triple tap - Errors, failures |

---

## Usage Standards

### 1. `selection` (70ms) - PRIMARY UI ACTIONS ✅

**Use for:**
- ✅ Opening modals/dialogs
- ✅ Closing modals/dialogs  
- ✅ Opening bottom sheets
- ✅ Closing bottom sheets
- ✅ Selecting items from lists
- ✅ Toggling UI panels (animation panel, edit panel)
- ✅ Button clicks that change UI state
- ✅ Dropdown selections

**Examples:**
```typescript
// Modal/Sheet opens
hapticService?.trigger("selection");

// Modal/Sheet closes  
hapticService?.trigger("selection");

// Item selection
hapticService?.trigger("selection");

// Panel toggles
hapticService?.trigger("selection");
```

**Components using `selection`:**
- PlayButton
- UndoButton
- ShareButton (open AND close)
- SequenceActionsButton
- ClearSequenceButton
- SaveSequenceButton
- RemoveBeatButton
- HamburgerMenuButton ✅ (FIXED)
- Settings button
- CAP card selections
- Start position selections
- Option selections

---

### 2. `navigation` (35ms) - LIGHTWEIGHT NAVIGATION ✅

**Use for:**
- ✅ Page/route navigation
- ✅ Tab switching within same context
- ✅ External link clicks
- ✅ Social media links
- ✅ Back navigation when closing context
- ✅ Pagination
- ✅ Scrolling indicators

**Examples:**
```typescript
// Tab switching
hapticService?.trigger("navigation");

// External links
hapticService?.trigger("navigation");

// Route navigation
hapticService?.trigger("navigation");
```

**Components using `navigation`:**
- SubModeTabs (tab switching)
- BuildTabHeader (mode switching)
- External links (social media, downloads)
- Landing page navigation
- Resource navigation

---

### 3. `success` (180ms pattern) - CONFIRMATIONS ✅

**Use for:**
- ✅ Successful saves
- ✅ Sequence exports
- ✅ Settings applied
- ✅ Upload completions
- ✅ Form submissions

**Examples:**
```typescript
// Save completion
hapticService?.trigger("success");

// Export success
hapticService?.trigger("success");

// Settings applied
hapticService?.trigger("success");
```

**Components using `success`:**
- SaveSequenceButton (on successful save)
- ShareActions (on successful share)
- SettingsSheet (on apply)
- Export tools (on export complete)

---

### 4. `warning` (120ms double-tap) - CAUTIONS ⚠️

**Use for:**
- ⚠️ Destructive action previews
- ⚠️ Unsaved changes warnings
- ⚠️ Confirmation dialogs (before delete)
- ⚠️ Validation warnings

**Examples:**
```typescript
// Before clearing sequence
hapticService?.trigger("warning");

// Unsaved changes dialog
hapticService?.trigger("warning");

// Delete confirmation shown
hapticService?.trigger("warning");
```

**Components using `warning`:**
- ClearSequenceButton (before confirm dialog)
- DeleteTools (before confirm)
- Unsaved changes dialogs

---

### 5. `error` (300ms triple-tap) - ERRORS ❌

**Use for:**
- ❌ Save failures
- ❌ Network errors
- ❌ Validation errors
- ❌ Action failures

**Examples:**
```typescript
// Save failed
hapticService?.trigger("error");

// Network error
hapticService?.trigger("error");

// Validation failed
hapticService?.trigger("error");
```

**Components using `error`:**
- Error toasts
- Failed save operations
- Network failure handlers
- Form validation errors

---

## Decision Tree

```
ACTION TYPE?
│
├─ Opening/Closing Modal or Sheet?
│  └─ Use `selection` (70ms)
│
├─ Navigating to different page/tab?
│  └─ Use `navigation` (35ms)
│
├─ Selecting an item or option?
│  └─ Use `selection` (70ms)
│
├─ Operation succeeded?
│  └─ Use `success` (180ms)
│
├─ Warning user before destructive action?
│  └─ Use `warning` (120ms)
│
└─ Operation failed or error occurred?
   └─ Use `error` (300ms)
```

---

## Anti-Patterns ❌

### DON'T:

❌ **Use `navigation` for modal/sheet opens**
```typescript
// WRONG
function openModal() {
  hapticService?.trigger("navigation"); // Too weak!
  showModal();
}

// CORRECT
function openModal() {
  hapticService?.trigger("selection"); // Proper intensity
  showModal();
}
```

❌ **Use different haptics for open vs close**
```typescript
// WRONG  
function toggleSheet() {
  if (isOpen) {
    hapticService?.trigger("navigation"); // Inconsistent!
  } else {
    hapticService?.trigger("selection");
  }
}

// CORRECT
function toggleSheet() {
  hapticService?.trigger("selection"); // Consistent
}
```

❌ **Use `selection` for page navigation**
```typescript
// WRONG
function goToGallery() {
  hapticService?.trigger("selection"); // Too strong!
  goto('/gallery');
}

// CORRECT  
function goToGallery() {
  hapticService?.trigger("navigation"); // Lightweight
  goto('/gallery');
}
```

---

## Testing Checklist

When adding haptic feedback:

- [ ] Does this open/close a modal or sheet? → `selection`
- [ ] Does this navigate to a different page? → `navigation`
- [ ] Does this select an item? → `selection`
- [ ] Is this a success confirmation? → `success`
- [ ] Is this a warning before destructive action? → `warning`
- [ ] Is this an error? → `error`
- [ ] Test on physical device (simulator haptics differ!)
- [ ] Verify intensity feels appropriate for action importance
- [ ] Confirm consistency with similar actions elsewhere

---

## Implementation Example

```typescript
import type { IHapticFeedbackService } from "$shared";
import { resolve, TYPES } from "$shared/inversify";

// Resolve service
const hapticService = resolve<IHapticFeedbackService>(
  TYPES.IHapticFeedbackService
);

// Button click - opens modal
function handleClick() {
  hapticService?.trigger("selection"); // 70ms
  openModal();
}

// Tab switch
function switchTab(newTab: string) {
  hapticService?.trigger("navigation"); // 35ms (lighter)
  activeTab = newTab;
}

// Save success
async function saveSequence() {
  try {
    await save();
    hapticService?.trigger("success"); // 180ms pattern
  } catch (error) {
    hapticService?.trigger("error"); // 300ms triple-tap
  }
}
```

---

## Accessibility Note

The `HapticFeedbackService` automatically respects:
- ✅ `prefers-reduced-motion` - Disables haptics if user prefers reduced motion
- ✅ Device capabilities - Only triggers on devices that support vibration
- ✅ Throttling - Prevents haptic spam with 100ms throttle

---

## Summary

| Intensity | Duration | Type | Use Case |
|-----------|----------|------|----------|
| **Lightest** | 35ms | `navigation` | Pages, tabs, links |
| **Medium** | 70ms | `selection` | Modals, buttons, selections |
| **Strong** | 180ms | `success` | Confirmations, saves |
| **Double** | 120ms | `warning` | Cautions, destructive previews |
| **Triple** | 300ms | `error` | Errors, failures |

**Golden Rule**: When in doubt, use `selection` for UI interactions and `navigation` for route changes.

---

*Last reviewed: 2025-10-30*
