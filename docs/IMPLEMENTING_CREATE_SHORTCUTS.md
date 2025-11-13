# Implementing CREATE Module Keyboard Shortcuts

Quick guide for implementing the keyboard shortcuts you requested for the CREATE module.

## 🎯 Requested Features

1. **Ctrl+S** - Save sequence
2. **Space** - Play/pause animation
3. **Arrow Keys** - Navigate beat grid (up/down) and beats (left/right) in Edit panel
4. **Enter** - Accept edit changes and close panel
5. **Keyboard shortcuts for adding beats** (both blue and red props)

## 📝 Implementation Steps

### 1. Save Sequence (Ctrl+S)

**Location**: `src/lib/modules/create/shared/shortcuts/create-shortcuts.ts` (new file)

```typescript
import { resolve, TYPES } from "$shared/inversify";
import type { IKeyboardShortcutService } from "$shared/keyboard/services/contracts";
import type { ISequencePersistenceService } from "../services/contracts";
import { getCreateModuleContext } from "../context";

export async function registerCreateShortcuts() {
  const shortcutService = await resolve<IKeyboardShortcutService>(
    TYPES.IKeyboardShortcutService
  );

  const persistenceService = await resolve<ISequencePersistenceService>(
    TYPES.ISequencePersistenceService
  );

  // Ctrl+S - Save sequence
  shortcutService.register({
    id: "create.save-sequence",
    label: "Save sequence",
    description: "Save the current sequence to your collection",
    key: "s",
    modifiers: ["ctrl"],
    context: "create",
    scope: "action",
    priority: "high",
    condition: () => {
      // Only enable if sequence exists and has beats
      const ctx = getCreateModuleContext();
      return (
        ctx.CreateModuleState.sequenceState.currentSequence?.beats.length > 0
      );
    },
    action: async () => {
      const ctx = getCreateModuleContext();
      const sequence = ctx.CreateModuleState.sequenceState.currentSequence;

      if (!sequence) return;

      try {
        // Save sequence using persistence service
        await persistenceService.saveSequence(sequence);

        // Show success feedback
        // TODO: Add toast notification
        console.log("✅ Sequence saved!");
      } catch (error) {
        console.error("Failed to save sequence:", error);
        // TODO: Show error toast
      }
    },
  });

  console.log("✅ CREATE shortcuts registered");
}
```

**Integration**: Call `registerCreateShortcuts()` in the `KeyboardShortcutCoordinator` after the global shortcuts are registered.

---

### 2. Play/Pause Animation (Space)

**Location**: Same file as above

```typescript
// Space - Play/Pause animation
shortcutService.register({
  id: "create.play-pause",
  label: "Play/pause animation",
  description: "Toggle animation playback",
  key: "Space",
  modifiers: [],
  context: ["create", "animation-panel"],
  scope: "action",
  priority: "critical",
  condition: () => {
    // Only enable if sequence exists
    const ctx = getCreateModuleContext();
    return ctx.CreateModuleState.sequenceState.currentSequence?.beats.length > 0;
  },
  action: async () => {
    const ctx = getCreateModuleContext();

    // If animation panel is not open, open it
    if (!ctx.panelState.isAnimationPanelOpen) {
      ctx.panelState.openAnimationPanel();
      return;
    }

    // Otherwise, toggle playback
    const playbackController = await resolve<IAnimationPlaybackController>(
      TYPES.IAnimationPlaybackController
    );

    playbackController.togglePlayback();
  },
});
```

**Note**: You may need to update the `AnimationPlaybackController` to expose a `togglePlayback()` method if it doesn't already exist.

---

### 3. Beat Grid Navigation (Arrow Keys)

**Location**: Same file

```typescript
// Arrow Up/Down - Navigate beat grid
shortcutService.register({
  id: "create.navigate-grid-up",
  label: "Move up in beat grid",
  description: "Move selection up one row in the beat grid",
  key: "ArrowUp",
  modifiers: [],
  context: "create",
  scope: "navigation",
  priority: "high",
  condition: () => {
    // Only when not editing
    const ctx = getCreateModuleContext();
    return !ctx.panelState.isEditPanelOpen;
  },
  action: () => {
    // TODO: Implement grid navigation
    // This will require adding a grid selection state
    console.log("Navigate up in grid");
  },
});

shortcutService.register({
  id: "create.navigate-grid-down",
  label: "Move down in beat grid",
  description: "Move selection down one row in the beat grid",
  key: "ArrowDown",
  modifiers: [],
  context: "create",
  scope: "navigation",
  priority: "high",
  condition: () => {
    const ctx = getCreateModuleContext();
    return !ctx.panelState.isEditPanelOpen;
  },
  action: () => {
    console.log("Navigate down in grid");
  },
});
```

---

### 4. Edit Panel Navigation (Arrow Keys)

```typescript
// Arrow Left/Right - Navigate beats in Edit panel
shortcutService.register({
  id: "edit-panel.previous-beat",
  label: "Previous beat",
  description: "Navigate to the previous beat in the sequence",
  key: "ArrowLeft",
  modifiers: [],
  context: "edit-panel",
  scope: "navigation",
  priority: "high",
  action: () => {
    const ctx = getCreateModuleContext();
    const currentIndex = ctx.panelState.editPanelBeatIndex;

    if (currentIndex > 0) {
      ctx.panelState.editPanelBeatIndex = currentIndex - 1;
    }
  },
});

shortcutService.register({
  id: "edit-panel.next-beat",
  label: "Next beat",
  description: "Navigate to the next beat in the sequence",
  key: "ArrowRight",
  modifiers: [],
  context: "edit-panel",
  scope: "navigation",
  priority: "high",
  action: () => {
    const ctx = getCreateModuleContext();
    const currentIndex = ctx.panelState.editPanelBeatIndex;
    const totalBeats =
      ctx.CreateModuleState.sequenceState.currentSequence?.beats.length || 0;

    if (currentIndex < totalBeats - 1) {
      ctx.panelState.editPanelBeatIndex = currentIndex + 1;
    }
  },
});

// Enter - Accept changes and close Edit panel
shortcutService.register({
  id: "edit-panel.accept",
  label: "Accept changes",
  description: "Accept changes and close the Edit panel",
  key: "Enter",
  modifiers: [],
  context: "edit-panel",
  scope: "action",
  priority: "high",
  action: () => {
    const ctx = getCreateModuleContext();
    ctx.panelState.closeEditPanel();
  },
});

// Delete - Delete current beat
shortcutService.register({
  id: "edit-panel.delete-beat",
  label: "Delete beat",
  description: "Delete the currently selected beat",
  key: "Delete",
  modifiers: [],
  context: "edit-panel",
  scope: "editing",
  priority: "high",
  action: async () => {
    const ctx = getCreateModuleContext();
    const beatOperations = await resolve<IBeatOperationsService>(
      TYPES.IBeatOperationsService
    );

    const beatIndex = ctx.panelState.editPanelBeatIndex;
    beatOperations.deleteBeat(beatIndex);
    ctx.panelState.closeEditPanel();
  },
});
```

---

### 5. Adding Beats (Keyboard Shortcuts)

For adding beats via keyboard, you have a few options:

#### Option A: Quick Add with Modifiers

```typescript
// Ctrl+B - Add blue beat (from last position)
shortcutService.register({
  id: "create.add-blue-beat",
  label: "Add blue beat",
  description: "Add a beat for the blue prop",
  key: "b",
  modifiers: ["ctrl"],
  context: "create",
  scope: "action",
  priority: "medium",
  action: () => {
    // This would open the option picker filtered to blue options
    const ctx = getCreateModuleContext();
    // TODO: Implement quick add for blue
    console.log("Add blue beat");
  },
});

// Ctrl+R - Add red beat (from last position)
shortcutService.register({
  id: "create.add-red-beat",
  label: "Add red beat",
  description: "Add a beat for the red prop",
  key: "r",
  modifiers: ["ctrl"],
  context: "create",
  scope: "action",
  priority: "medium",
  action: () => {
    // This would open the option picker filtered to red options
    const ctx = getCreateModuleContext();
    // TODO: Implement quick add for red
    console.log("Add red beat");
  },
});
```

#### Option B: Command Palette Integration

Add these as commands in the command palette so users can discover them:

```typescript
// In register-commands.ts
service.registerCommand({
  id: "beat.add-blue",
  label: "Add Blue Beat",
  description: "Add a beat for the blue prop",
  icon: "fa-plus",
  category: "CREATE",
  shortcut: state.isMac ? "⌘B" : "Ctrl+B",
  keywords: ["add", "blue", "beat", "create"],
  available: isInCreateModule(),
  action: () => {
    // Add blue beat
    state.closeCommandPalette();
  },
});
```

---

## 🔧 Context Management

To make shortcuts context-aware (e.g., only active when Edit panel is open), you need to update the context in the coordinator:

**Location**: `KeyboardShortcutCoordinator.svelte`

```svelte
<script lang="ts">
  // ... existing code

  // Sync context with panel state
  $effect(() => {
    if (shortcutService) {
      const ctx = getCreateModuleContext();

      if (ctx.panelState.isEditPanelOpen) {
        shortcutService.setContext("edit-panel");
      } else if (ctx.panelState.isAnimationPanelOpen) {
        shortcutService.setContext("animation-panel");
      } else if (ctx.panelState.isSharePanelOpen) {
        shortcutService.setContext("share-panel");
      } else {
        // Use module context
        const module = getActiveModule();
        if (module) {
          shortcutService.setContext(module as any);
        }
      }
    }
  });
</script>
```

---

## 🎨 Visual Feedback

Add visual feedback when shortcuts are activated:

```typescript
import { keyboardShortcutState } from "$shared/keyboard/state";

// In shortcut action:
action: () => {
  // Track activation for visual feedback
  keyboardShortcutState.trackActivation("create.save-sequence");

  // ... perform action
};
```

Then in your UI, show a brief indicator:

```svelte
{#if keyboardShortcutState.recentlyActivated.includes("create.save-sequence")}
  <div class="shortcut-indicator">Sequence saved!</div>
{/if}
```

---

## 🧪 Testing Checklist

- [ ] Ctrl+S saves sequence
- [ ] Space opens animation panel and toggles playback
- [ ] Arrow keys navigate beat grid when Edit panel is closed
- [ ] Arrow keys navigate between beats when Edit panel is open
- [ ] Enter closes Edit panel and accepts changes
- [ ] Delete removes current beat
- [ ] Shortcuts disabled when typing in input fields
- [ ] Shortcuts work on Mac (Cmd) and Windows/Linux (Ctrl)
- [ ] Visual feedback shows when shortcuts are activated
- [ ] Shortcuts appear in Command Palette
- [ ] Shortcuts appear in Help dialog (Ctrl+/)

---

## 📚 Next Steps

1. Create `src/lib/modules/create/shared/shortcuts/create-shortcuts.ts`
2. Implement the shortcuts above
3. Call `registerCreateShortcuts()` in the coordinator
4. Test on multiple platforms
5. Add to command palette
6. Document in main README

---

**Need Help?**

- Check the main [KEYBOARD_SHORTCUTS.md](../KEYBOARD_SHORTCUTS.md) for API reference
- Review existing shortcuts in `register-global-shortcuts.ts`
- Ask questions in team chat or GitHub discussions
