/**
 * Register Global Shortcuts
 *
 * Registers all global keyboard shortcuts that are available app-wide.
 *
 * Domain: Keyboard Shortcuts - Registration
 */

import type { IKeyboardShortcutService } from "../services/contracts";
import type { createKeyboardShortcutState } from "../state/keyboard-shortcut-state.svelte";
import { showSettingsDialog } from "$shared/application/state/ui/ui-state.svelte";
import {
  handleModuleChange,
  getModuleDefinitions,
} from "$shared/navigation-coordinator/navigation-coordinator.svelte";
import { authStore } from "$shared/auth";

export function registerGlobalShortcuts(
  service: IKeyboardShortcutService,
  state: ReturnType<typeof createKeyboardShortcutState>
) {
  // Get accessible modules
  const moduleDefinitions = getModuleDefinitions();
  const isAdmin = authStore.isAdmin;

  // Filter modules to only show accessible ones
  const accessibleModules = moduleDefinitions.filter((module) => {
    // Filter out admin module for non-admin users
    if (module.id === "admin" && !isAdmin) {
      return false;
    }
    // Filter out modules that aren't implemented yet
    const notImplemented = ["write", "word-card"];
    if (notImplemented.includes(module.id)) {
      return false;
    }
    return true;
  });
  // ==================== TIER 1: Essential Global Shortcuts ====================
  // Using single-key shortcuts (Gmail/Notion style) since Chrome blocks most Ctrl combinations

  // ? - Show keyboard shortcuts help (Gmail standard)
  service.register({
    id: "global.shortcuts-help",
    label: "Show keyboard shortcuts",
    description: "Display all available shortcuts (press ? key)",
    key: "?",
    modifiers: [],
    context: "global",
    scope: "help",
    priority: "critical",
    condition: () => {
      // Only enable if settings allow single-key shortcuts
      return state.settings.enableSingleKeyShortcuts;
    },
    action: () => {
      state.toggleHelp();
    },
  });

  // Escape - Close current modal/panel
  service.register({
    id: "global.escape",
    label: "Close modal",
    description: "Close the current modal, panel, or dialog",
    key: "Escape",
    modifiers: [],
    context: "global",
    scope: "navigation",
    priority: "critical",
    action: () => {
      // Close command palette if open
      if (state.showCommandPalette) {
        state.closeCommandPalette();
        return;
      }

      // Close help if open
      if (state.showHelp) {
        state.closeHelp();
        return;
      }

      // Other escape handlers will be context-specific
    },
  });

  // ==================== Module Switching (Single Keys) ====================
  // Using single-key shortcuts (numbers 1-5) like Gmail/Notion
  // These work reliably in Chrome unlike Ctrl+1-9 or Alt+1-5

  // Map modules to number keys
  const moduleKeyMap = ["1", "2", "3", "4", "5"];

  accessibleModules.slice(0, 5).forEach((module, index) => {
    const key = moduleKeyMap[index];

    service.register({
      id: `global.switch-to-${module.id}`,
      label: `Switch to ${module.label.toUpperCase()} module`,
      description: `Navigate to the ${module.label} module (press ${key})`,
      key: key,
      modifiers: [],
      context: "global",
      scope: "navigation",
      priority: "high",
      condition: () => {
        // Only enable if settings allow single-key shortcuts
        return state.settings.enableSingleKeyShortcuts;
      },
      action: async () => {
        await handleModuleChange(module.id as any);
      },
    });
  });

  console.log("✅ Global shortcuts registered");
}
