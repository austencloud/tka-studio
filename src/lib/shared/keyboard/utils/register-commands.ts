/**
 * Register Command Palette Commands
 *
 * Registers all commands available in the command palette.
 *
 * Domain: Keyboard Shortcuts - Command Registration
 */

import type { ICommandPaletteService } from "../services/contracts";
import type { createKeyboardShortcutState } from "../state/keyboard-shortcut-state.svelte";
import { showSettingsDialog } from "$shared/application/state/ui/ui-state.svelte";
import {
  handleModuleChange,
  getModuleDefinitions,
} from "$shared/navigation-coordinator/navigation-coordinator.svelte";
import { authStore } from "$shared/auth";

export function registerCommandPaletteCommands(
  service: ICommandPaletteService,
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

  // ==================== Navigation Commands ====================

  // Dynamically register commands for accessible modules
  accessibleModules.forEach((module, index) => {
    const shortcutNumber = index + 1;

    service.registerCommand({
      id: `navigate.${module.id}`,
      label: `Go to ${module.label.toUpperCase()}`,
      description: module.description || `Navigate to the ${module.label} module`,
      icon: module.icon || "fa-circle",
      category: "Navigation",
      shortcut: shortcutNumber <= 5 ? `${shortcutNumber}` : undefined,
      keywords: [
        module.label.toLowerCase(),
        module.id,
        ...(module.keywords || []),
      ],
      available: true,
      action: async () => {
        await handleModuleChange(module.id as any);
        state.closeCommandPalette();
      },
    });
  });

  // ==================== Settings Commands ====================

  service.registerCommand({
    id: "settings.open",
    label: "Open Settings",
    description: "Configure application settings",
    icon: "fa-cog",
    category: "Settings",
    shortcut: state.isMac ? "⌘," : "Ctrl+Shift+,",
    keywords: ["settings", "preferences", "config", "options"],
    available: true,
    action: () => {
      showSettingsDialog();
      state.closeCommandPalette();
    },
  });

  // ==================== Help Commands ====================

  service.registerCommand({
    id: "help.shortcuts",
    label: "Show Keyboard Shortcuts",
    description: "View all available shortcuts",
    icon: "fa-keyboard",
    category: "Help",
    shortcut: state.isMac ? "⌘/" : "Ctrl+/",
    keywords: ["help", "shortcuts", "keyboard", "hotkeys"],
    available: true,
    action: () => {
      state.openHelp();
      state.closeCommandPalette();
    },
  });

  console.log("✅ Command palette commands registered");
}
