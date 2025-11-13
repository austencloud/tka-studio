<script lang="ts">
  /**
   * Keyboard Shortcut Coordinator
   *
   * Initializes and coordinates the keyboard shortcut system.
   * Registers global shortcuts and manages the command palette.
   *
   * Domain: Keyboard Shortcuts - Coordination
   */

  import { onMount } from "svelte";
  import { resolve, TYPES } from "$shared/inversify";
  import type {
    IKeyboardShortcutService,
    ICommandPaletteService,
  } from "../services/contracts";
  import { keyboardShortcutState } from "../state";
  import { getActiveModule } from "$shared/application/state/ui/ui-state.svelte";
  import { registerGlobalShortcuts } from "../utils/register-global-shortcuts";
  import { registerCommandPaletteCommands } from "../utils/register-commands";
  import { registerCreateShortcuts } from "../utils/register-create-shortcuts";

  // Services
  let shortcutService: IKeyboardShortcutService | null = null;
  let commandPaletteService: ICommandPaletteService | null = null;

  onMount(async () => {
    console.log("⌨️ KeyboardShortcutCoordinator mounting...");

    try {
      // Resolve services
      console.log("⌨️ Resolving keyboard shortcut services...");
      shortcutService = await resolve<IKeyboardShortcutService>(
        TYPES.IKeyboardShortcutService
      );
      commandPaletteService = await resolve<ICommandPaletteService>(
        TYPES.ICommandPaletteService
      );

      console.log("⌨️ Services resolved successfully");

      // Initialize the shortcut service
      shortcutService.initialize();

      // Register global shortcuts
      registerGlobalShortcuts(shortcutService, keyboardShortcutState);

      // Register command palette commands
      registerCommandPaletteCommands(
        commandPaletteService,
        keyboardShortcutState
      );

      // Register CREATE module shortcuts
      registerCreateShortcuts(shortcutService, keyboardShortcutState);

      console.log("✅ Keyboard shortcuts system fully initialized!");
      console.log("💡 Press ? to view all keyboard shortcuts");
      console.log("💡 Press 1-5 to switch between modules (CREATE, EXPLORE, LEARN, COLLECT, ANIMATE)");
      console.log("💡 Press Esc to close modals/panels");
      console.log("💡 CREATE Module: Space for play/pause, arrows for navigation, Enter to accept");
      console.log("💡 Single-key shortcuts only work when not typing in an input field");
    } catch (error) {
      console.error("❌ Failed to initialize keyboard shortcuts:", error);
    }

    // Cleanup on unmount
    return () => {
      if (shortcutService) {
        shortcutService.dispose();
      }
    };
  });

  // Sync context with active module
  $effect(() => {
    const module = getActiveModule();
    console.log("⌨️ $effect triggered - Active module:", module);

    if (shortcutService) {
      if (module) {
        shortcutService.setContext(module as any);
      }
    } else {
      console.warn("⌨️ Shortcut service not yet available");
    }
  });
</script>

<!-- This coordinator has no UI -->
