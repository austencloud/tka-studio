# Haptic Feedback Standards

**Last Updated**: 2025-10-30

---

## Overview

This document defines the **standard haptic feedback patterns** for TKA to ensure consistent tactile feedback across the application.

## Design Philosophy

**Consistency Over Complexity**: Research from iOS, Android, and PWA guidelines shows that users benefit more from consistent haptic feedback than from subtle variations in intensity.

### Key Principles:

- ✅ **"Be consistent within your app"** - If a particular interaction has haptic feedback, apply the same effect to all similar interactions
- ✅ **"Clear, crisp, predictable, short feedback"** - Users need immediate, recognizable confirmation
- ✅ **"Less is more"** - Use haptics sparingly and meaningfully
- ✅ **One standard pattern for all interactions** - Opening a hamburger menu vs opening settings are the same interaction type

### Why We Simplified:

Previously, we had separate patterns for "navigation" (35ms) and "selection" (70ms). User feedback and research revealed:

- The 2x difference (35ms vs 70ms) was not perceptible enough to be meaningful
- Opening a modal vs navigating to a page are both interactive elements that should feel identical
- Complexity made it harder for developers to choose the right pattern
- Consistency is more valuable than subtle differentiation

---

## Haptic Feedback Patterns

### Defined in `HapticFeedbackService.ts`:

| Type            | Pattern (ms)            | Total Duration | Use Case                                                               |
| --------------- | ----------------------- | -------------- | ---------------------------------------------------------------------- |
| **`selection`** | `[70]`                  | 70ms           | **ALL interactive elements** - Buttons, modals, navigation, selections |
| **`success`**   | `[100, 30, 50]`         | 180ms          | Strong pattern - Confirmations, saves                                  |
| **`warning`**   | `[60, 0, 60]`           | 120ms          | Double tap - Cautions, destructive previews                            |
| **`error`**     | `[100, 0, 100, 0, 100]` | 300ms          | Triple tap - Errors, failures                                          |

---

## Usage Standards

### 1. `selection` (70ms) - ALL INTERACTIVE ELEMENTS ✅

**Use for:** **EVERYTHING** except success/warning/error feedback

**Includes:**

- ✅ Opening/closing modals and dialogs
- ✅ Opening/closing bottom sheets
- ✅ Button clicks (play, save, clear, undo, back, etc.)
- ✅ Item selections (CAP cards, options, lists)
- ✅ Toggles (panels, fullscreen, settings)
- ✅ Navigation (module switching, tabs, page changes)
- ✅ Menu interactions (hamburger menu, dropdowns)
- ✅ All user-initiated interactions

**Why one pattern for everything:**

- Users experience consistent feedback across the entire app
- No cognitive load deciding between "is this navigation or selection?"
- Research shows consistency is more valuable than subtle intensity differences
- Simpler to implement and maintain

**Examples:**

```typescript
// ALL interactions use selection
function handleButtonClick() {
  hapticService?.trigger("selection"); // ✅ Standard for all buttons
}

function handleModalOpen() {
  hapticService?.trigger("selection"); // ✅ Standard for all modals
}

function handleModuleNavigation() {
  hapticService?.trigger("selection"); // ✅ Standard for all navigation
}

function handleTabSwitch() {
  hapticService?.trigger("selection"); // ✅ Standard for all tabs
}

function handleItemSelection() {
  hapticService?.trigger("selection"); // ✅ Standard for all selections
}
```

**Components using `selection`:** (ALL interactive components)

- **Buttons**: PlayButton, UndoButton, ShareButton, BackButton, SequenceActionsButton, ClearSequenceButton, SaveSequenceButton, RemoveBeatButton, FullscreenButton
- **Navigation**: HamburgerMenuButton, ModuleList,SectionTabs, BuildTabHeader
- **Modals/Sheets**: Settings button, SettingsSheet, SharePanel, AnimationPanel
- **Selections**: CAP cards, Start position picker, Option selections
- **All other interactive elements**

---

### 2. `success` (180ms pattern) - CONFIRMATIONS ✅

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

### 3. `warning` (120ms double-tap) - CAUTIONS ⚠️

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

### 4. `error` (300ms triple-tap) - ERRORS ❌

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

When adding haptic feedback to a new component, follow this simple decision tree:

```
Is this an error state?
├─ YES → Use `error` (300ms triple-tap)
└─ NO
   └─ Is this a warning or caution?
      ├─ YES → Use `warning` (120ms double-tap)
      └─ NO
         └─ Is this a success/completion?
            ├─ YES → Use `success` (180ms triple-pulse)
            └─ NO → Use `selection` (70ms) ✅ DEFAULT FOR ALL INTERACTIONS
```

**Rule of thumb:** If it's not an error, warning, or success feedback, use `selection`. This covers:

- Buttons, modals, sheets, dialogs
- Navigation (module switching, back button, tabs)
- Selections (CAP cards, options, items)
- Toggles (fullscreen, panels, settings)
- **Literally every other interactive element**

---

## Anti-Patterns ❌

### DON'T:

❌ **Use different haptics for similar interactions**

```typescript
// WRONG - Inconsistent
function openHamburgerMenu() {
  hapticService?.trigger("navigation"); // ❌ Pattern doesn't exist anymore!
}

function openSettingsDialog() {
  hapticService?.trigger("selection"); // Different feel for same action
}

// CORRECT ✅ - Consistent
function openHamburgerMenu() {
  hapticService?.trigger("selection"); // Both modals use same haptic
}

function openSettingsDialog() {
  hapticService?.trigger("selection"); // Consistent user experience
}
```

❌ **Over-engineer haptic patterns**

```typescript
// WRONG - Unnecessary complexity
function handleClick() {
  if (isModal) {
    hapticService?.trigger("selection");
  } else if (isNavigation) {
    hapticService?.trigger("selection"); // Same thing!
  } else if (isButton) {
    hapticService?.trigger("selection"); // Same thing!
  }
}

// CORRECT ✅ - Simple and consistent
function handleClick() {
  hapticService?.trigger("selection"); // One pattern for all
}
```

❌ **Use success/warning/error for regular interactions**

```typescript
// WRONG
function openModal() {
  hapticService?.trigger("success"); // Too strong, confusing
  showModal();
}

// CORRECT
function openModal() {
  hapticService?.trigger("selection"); // Appropriate
  showModal();
}
```

---

## Testing Checklist

When adding haptic feedback:

- [ ] Is this an error? → `error`
- [ ] Is this a warning/caution? → `warning`
- [ ] Is this a success confirmation? → `success`
- [ ] Is this ANY other interaction? → `selection` ✅ (99% of cases)
- [ ] Test on physical device (simulator haptics differ!)
- [ ] Verify consistency with similar actions elsewhere
- [ ] Confirm haptic respects reduced motion preferences

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
  hapticService?.trigger("selection"); // ✅ Standard for all interactions
  openModal();
}

// Tab switch
function switchTab(newTab: string) {
  hapticService?.trigger("selection"); // ✅ Same haptic for consistency
  activeTab = newTab;
}

// Module navigation
function navigateToModule(moduleId: string) {
  hapticService?.trigger("selection"); // ✅ Same haptic for consistency
  goto(`/module/${moduleId}`);
}

// Save success
async function saveSequence() {
  try {
    await save();
    hapticService?.trigger("success"); // ✅ 180ms pattern for success
  } catch (error) {
    hapticService?.trigger("error"); // ✅ 300ms triple-tap for error
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

| Intensity    | Duration | Type        | Use Case                                                                        |
| ------------ | -------- | ----------- | ------------------------------------------------------------------------------- |
| **Standard** | 70ms     | `selection` | **ALL interactive elements** - buttons, modals, navigation, selections, toggles |
| **Strong**   | 180ms    | `success`   | Confirmations, saves, completions                                               |
| **Double**   | 120ms    | `warning`   | Cautions, destructive previews                                                  |
| **Triple**   | 300ms    | `error`     | Errors, failures                                                                |

**Golden Rule**: Use `selection` for everything except explicit success/warning/error feedback.

---

## Research References

This simplified approach is based on:

- [Android Haptics Design Principles](https://developer.android.com/develop/ui/views/haptics/haptics-principles) - "Be consistent within your app"
- [iOS Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/playing-haptics) - "Clear, crisp, predictable feedback"
- [PWA Vibration API Best Practices](https://developer.mozilla.org/en-US/docs/Web/API/Vibration_API) - "Use sparingly and meaningfully"
- 2025 Mobile UX Research - "Consistency is more valuable than subtle intensity differences"

---

_Last reviewed: 2025-10-30_
_Migration completed: All 54 files updated from dual-pattern to single-pattern system_
