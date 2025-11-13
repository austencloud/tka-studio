<script lang="ts">
  /**
   * Shortcuts Help Dialog
   *
   * Displays all available keyboard shortcuts organized by category.
   *
   * Domain: Keyboard Shortcuts - UI
   */

  import { onMount } from "svelte";
  import { resolve, TYPES } from "$shared/inversify";
  import type { IKeyboardShortcutService } from "../services/contracts";
  import { keyboardShortcutState } from "../state";
  import type { ShortcutRegistrationOptions, ShortcutScope } from "../domain";

  // Service
  let shortcutService: IKeyboardShortcutService | null = null;

  // Shortcuts grouped by scope
  let shortcutsByScope = $state<Map<ShortcutScope, ShortcutRegistrationOptions[]>>(
    new Map()
  );

  onMount(async () => {
    try {
      shortcutService = await resolve<IKeyboardShortcutService>(
        TYPES.IKeyboardShortcutService
      );
      loadShortcuts();
    } catch (error) {
      console.error("Failed to resolve shortcut service:", error);
    }
  });

  function loadShortcuts() {
    if (!shortcutService) return;

    const allShortcuts = shortcutService.getAllShortcuts();
    const grouped = new Map<ShortcutScope, ShortcutRegistrationOptions[]>();

    for (const shortcut of allShortcuts) {
      const scope = shortcut.scope ?? "action";
      if (!grouped.has(scope)) {
        grouped.set(scope, []);
      }
      grouped.get(scope)!.push(shortcut);
    }

    shortcutsByScope = grouped;
  }

  function close() {
    keyboardShortcutState.closeHelp();
  }

  function formatShortcut(shortcut: ShortcutRegistrationOptions): string {
    const isMac = keyboardShortcutState.isMac;
    const modifiers = shortcut.modifiers ?? [];

    const modifierStrings = modifiers.map((mod) => {
      switch (mod) {
        case "ctrl":
          return isMac ? "⌘" : "Ctrl";
        case "meta":
          return isMac ? "⌘" : "Win";
        case "alt":
          return isMac ? "⌥" : "Alt";
        case "shift":
          return isMac ? "⇧" : "Shift";
        default:
          return mod;
      }
    });

    const keyString = formatKey(shortcut.key);

    return [...modifierStrings, keyString].join(isMac ? "" : "+");
  }

  function formatKey(key: string): string {
    const keyMap: Record<string, string> = {
      ArrowUp: "↑",
      ArrowDown: "↓",
      ArrowLeft: "←",
      ArrowRight: "→",
      Enter: "↵",
      Escape: "Esc",
      Backspace: "⌫",
      Delete: "⌦",
      Space: "Space",
      Tab: "⇥",
    };

    return keyMap[key] || key.toUpperCase();
  }

  function getScopeLabel(scope: ShortcutScope): string {
    const labels: Record<ShortcutScope, string> = {
      navigation: "Navigation",
      action: "Actions",
      editing: "Editing",
      panel: "Panels",
      focus: "Focus Management",
      help: "Help & Information",
    };

    return labels[scope] || scope;
  }

  function getScopeDescription(scope: ShortcutScope): string {
    const descriptions: Record<ShortcutScope, string> = {
      navigation: "Switch between modules and navigate the app",
      action: "Execute actions and commands",
      editing: "Edit and modify content",
      panel: "Manage panels and dialogs",
      focus: "Move focus between UI regions",
      help: "Access help and documentation",
    };

    return descriptions[scope] || "";
  }

  // Sort scopes in a logical order
  let sortedScopes = $derived.by(() => {
    const order: ShortcutScope[] = [
      "help",
      "navigation",
      "action",
      "editing",
      "panel",
      "focus",
    ];

    return order.filter((scope) => shortcutsByScope.has(scope));
  });
</script>

{#if keyboardShortcutState.showHelp}
  <div class="shortcuts-help-overlay" onclick={close}>
    <div
      class="shortcuts-help"
      onclick={(e) => e.stopPropagation()}
      role="dialog"
      aria-label="Keyboard Shortcuts Help"
    >
      <!-- Header -->
      <div class="shortcuts-help__header">
        <div>
          <h2 class="shortcuts-help__title">Keyboard Shortcuts</h2>
          <p class="shortcuts-help__subtitle">
            Use these shortcuts to navigate faster
          </p>
        </div>
        <button
          class="shortcuts-help__close"
          onclick={close}
          aria-label="Close"
          type="button"
        >
          <i class="fa fa-times"></i>
        </button>
      </div>

      <!-- Content -->
      <div class="shortcuts-help__content">
        {#if sortedScopes.length === 0}
          <div class="shortcuts-help__empty">No shortcuts available</div>
        {:else}
          {#each sortedScopes as scope}
            {@const shortcuts = shortcutsByScope.get(scope) ?? []}
            {#if shortcuts.length > 0}
              <section class="shortcuts-help__section">
                <h3 class="shortcuts-help__section-title">
                  {getScopeLabel(scope)}
                </h3>
                {#if getScopeDescription(scope)}
                  <p class="shortcuts-help__section-description">
                    {getScopeDescription(scope)}
                  </p>
                {/if}
                <div class="shortcuts-help__list">
                  {#each shortcuts as shortcut}
                    <div class="shortcuts-help__item">
                      <div class="shortcuts-help__item-info">
                        <div class="shortcuts-help__item-label">
                          {shortcut.label}
                        </div>
                        {#if shortcut.description}
                          <div class="shortcuts-help__item-description">
                            {shortcut.description}
                          </div>
                        {/if}
                      </div>
                      <kbd class="shortcuts-help__item-keys">
                        {formatShortcut(shortcut)}
                      </kbd>
                    </div>
                  {/each}
                </div>
              </section>
            {/if}
          {/each}
        {/if}
      </div>

      <!-- Footer -->
      <div class="shortcuts-help__footer">
        <span>
          Press
          <kbd>{keyboardShortcutState.isMac ? "⌘/" : "Ctrl+/"}</kbd>
          to toggle this dialog
        </span>
      </div>
    </div>
  </div>
{/if}

<style>
  .shortcuts-help-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(4px);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
  }

  .shortcuts-help {
    width: 100%;
    max-width: 900px;
    max-height: 90vh;
    background: var(--background, #1e1e1e);
    border: 1px solid var(--border-color, #333);
    border-radius: 12px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .shortcuts-help__header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 1.5rem;
    border-bottom: 1px solid var(--border-color, #333);
  }

  .shortcuts-help__title {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-primary, #fff);
  }

  .shortcuts-help__subtitle {
    margin: 0.25rem 0 0;
    font-size: 0.875rem;
    color: var(--text-secondary, #888);
  }

  .shortcuts-help__close {
    width: 2rem;
    height: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border: none;
    border-radius: 6px;
    color: var(--text-secondary, #888);
    cursor: pointer;
    transition: all 0.2s;
  }

  .shortcuts-help__close:hover {
    background: var(--background-secondary, #2a2a2a);
    color: var(--text-primary, #fff);
  }

  .shortcuts-help__content {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem;
  }

  .shortcuts-help__section {
    margin-bottom: 2rem;
  }

  .shortcuts-help__section:last-child {
    margin-bottom: 0;
  }

  .shortcuts-help__section-title {
    margin: 0 0 0.5rem;
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text-primary, #fff);
  }

  .shortcuts-help__section-description {
    margin: 0 0 1rem;
    font-size: 0.875rem;
    color: var(--text-secondary, #888);
  }

  .shortcuts-help__list {
    display: grid;
    gap: 0.5rem;
  }

  .shortcuts-help__item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem;
    background: var(--background-secondary, #2a2a2a);
    border-radius: 6px;
    gap: 1rem;
  }

  .shortcuts-help__item-info {
    flex: 1;
    min-width: 0;
  }

  .shortcuts-help__item-label {
    font-weight: 500;
    color: var(--text-primary, #fff);
    margin-bottom: 0.125rem;
  }

  .shortcuts-help__item-description {
    font-size: 0.875rem;
    color: var(--text-secondary, #888);
  }

  .shortcuts-help__item-keys {
    font-size: 0.875rem;
    padding: 0.375rem 0.75rem;
    background: var(--background-tertiary, #333);
    border-radius: 4px;
    color: var(--text-secondary, #888);
    font-family: monospace;
    white-space: nowrap;
  }

  .shortcuts-help__empty {
    text-align: center;
    padding: 3rem;
    color: var(--text-secondary, #888);
  }

  .shortcuts-help__footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid var(--border-color, #333);
    font-size: 0.875rem;
    color: var(--text-secondary, #888);
    text-align: center;
  }

  .shortcuts-help__footer kbd {
    padding: 0.25rem 0.5rem;
    background: var(--background-secondary, #2a2a2a);
    border-radius: 4px;
    font-family: monospace;
    font-size: 0.8em;
  }

  /* Responsive */
  @media (max-width: 768px) {
    .shortcuts-help {
      max-height: 95vh;
    }

    .shortcuts-help__header {
      padding: 1rem;
    }

    .shortcuts-help__content {
      padding: 1rem;
    }

    .shortcuts-help__item {
      flex-direction: column;
      align-items: flex-start;
    }
  }
</style>
