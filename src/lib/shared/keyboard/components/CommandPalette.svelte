<script lang="ts">
  /**
   * Command Palette Component
   *
   * Searchable command palette (Cmd+K) for quick navigation and actions.
   *
   * Domain: Keyboard Shortcuts - UI
   */

  import { onMount } from "svelte";
  import { resolve, TYPES } from "$shared/inversify";
  import type { ICommandPaletteService } from "../services/contracts";
  import { commandPaletteState, keyboardShortcutState } from "../state";
  import type { CommandPaletteItem } from "../domain";

  // Service
  let paletteService: ICommandPaletteService | null = null;

  // Local state
  let inputElement: HTMLInputElement | null = null;
  let dialogElement: HTMLDialogElement | null = null;

  onMount(async () => {
    try {
      paletteService = await resolve<ICommandPaletteService>(
        TYPES.ICommandPaletteService
      );
    } catch (error) {
      console.error("Failed to resolve command palette service:", error);
    }
  });

  // Watch for open state changes
  $effect(() => {
    if (commandPaletteState.isOpen) {
      // Focus the input when opened
      setTimeout(() => {
        inputElement?.focus();
      }, 50);

      // Load initial results (recent commands)
      performSearch("");
    }
  });

  // Perform search when query changes
  $effect(() => {
    const query = commandPaletteState.query;
    if (commandPaletteState.isOpen) {
      performSearch(query);
    }
  });

  function performSearch(query: string) {
    if (!paletteService) return;

    commandPaletteState.setLoading(true);

    try {
      const results = paletteService.search(query);
      commandPaletteState.setResults(results);
    } catch (error) {
      console.error("Search failed:", error);
      commandPaletteState.setResults([]);
    } finally {
      commandPaletteState.setLoading(false);
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    switch (event.key) {
      case "ArrowDown":
        event.preventDefault();
        commandPaletteState.selectNext();
        break;
      case "ArrowUp":
        event.preventDefault();
        commandPaletteState.selectPrevious();
        break;
      case "Enter":
        event.preventDefault();
        executeSelected();
        break;
      case "Escape":
        event.preventDefault();
        close();
        break;
    }
  }

  function handleItemClick(item: CommandPaletteItem) {
    commandPaletteState.selectByIndex(commandPaletteState.results.indexOf(item));
    executeSelected();
  }

  function handleItemHover(item: CommandPaletteItem) {
    commandPaletteState.selectByIndex(commandPaletteState.results.indexOf(item));
  }

  async function executeSelected() {
    if (!paletteService) return;

    const selected = commandPaletteState.selectedItem;
    if (!selected) return;

    try {
      await paletteService.executeCommand(selected.id);
      close();
    } catch (error) {
      console.error("Failed to execute command:", error);
    }
  }

  function close() {
    commandPaletteState.close();
    keyboardShortcutState.closeCommandPalette();
  }

  // Group results by category
  let groupedResults = $derived.by(() => {
    const groups = new Map<string, CommandPaletteItem[]>();

    for (const item of commandPaletteState.results) {
      const category = item.category || "Other";
      if (!groups.has(category)) {
        groups.set(category, []);
      }
      groups.get(category)!.push(item);
    }

    return Array.from(groups.entries());
  });
</script>

{#if commandPaletteState.isOpen}
  <div class="command-palette-overlay" onclick={close}>
    <div
      class="command-palette"
      onclick={(e) => e.stopPropagation()}
      role="dialog"
      aria-label="Command Palette"
    >
      <!-- Search Input -->
      <div class="command-palette__search">
        <i class="fa fa-search command-palette__search-icon"></i>
        <input
          bind:this={inputElement}
          type="text"
          placeholder="Type a command or search..."
          value={commandPaletteState.query}
          oninput={(e) =>
            commandPaletteState.setQuery(e.currentTarget.value)}
          onkeydown={handleKeydown}
          class="command-palette__input"
        />
        <span class="command-palette__hint">
          {keyboardShortcutState.isMac ? "⌘K" : "Ctrl+K"}
        </span>
      </div>

      <!-- Results -->
      <div class="command-palette__results">
        {#if commandPaletteState.isLoading}
          <div class="command-palette__loading">Searching...</div>
        {:else if commandPaletteState.results.length === 0}
          <div class="command-palette__empty">
            {commandPaletteState.query
              ? "No commands found"
              : "Start typing to search commands"}
          </div>
        {:else}
          {#each groupedResults as [category, items]}
            <div class="command-palette__category">
              <div class="command-palette__category-label">{category}</div>
              {#each items as item, index}
                {@const globalIndex = commandPaletteState.results.indexOf(item)}
                {@const isSelected = globalIndex === commandPaletteState.selectedIndex}
                <button
                  class="command-palette__item"
                  class:command-palette__item--selected={isSelected}
                  onclick={() => handleItemClick(item)}
                  onmouseenter={() => handleItemHover(item)}
                  type="button"
                >
                  {#if item.icon}
                    <i class="fa {item.icon} command-palette__item-icon"></i>
                  {/if}
                  <div class="command-palette__item-content">
                    <div class="command-palette__item-label">{item.label}</div>
                    {#if item.description}
                      <div class="command-palette__item-description">
                        {item.description}
                      </div>
                    {/if}
                  </div>
                  {#if item.shortcut}
                    <kbd class="command-palette__item-shortcut">
                      {item.shortcut}
                    </kbd>
                  {/if}
                </button>
              {/each}
            </div>
          {/each}
        {/if}
      </div>

      <!-- Footer -->
      <div class="command-palette__footer">
        <span>
          <kbd>↑</kbd>
          <kbd>↓</kbd>
          to navigate
        </span>
        <span>
          <kbd>↵</kbd>
          to select
        </span>
        <span>
          <kbd>Esc</kbd>
          to close
        </span>
      </div>
    </div>
  </div>
{/if}

<style>
  .command-palette-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(4px);
    z-index: 9999;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    padding-top: 15vh;
  }

  .command-palette {
    width: 90%;
    max-width: 640px;
    background: var(--background, #1e1e1e);
    border: 1px solid var(--border-color, #333);
    border-radius: 12px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    max-height: 70vh;
    overflow: hidden;
  }

  .command-palette__search {
    display: flex;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid var(--border-color, #333);
    gap: 0.75rem;
  }

  .command-palette__search-icon {
    color: var(--text-secondary, #888);
    font-size: 1.125rem;
  }

  .command-palette__input {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: var(--text-primary, #fff);
    font-size: 1.125rem;
    padding: 0;
  }

  .command-palette__input::placeholder {
    color: var(--text-secondary, #888);
  }

  .command-palette__hint {
    color: var(--text-secondary, #888);
    font-size: 0.875rem;
    padding: 0.25rem 0.5rem;
    background: var(--background-secondary, #2a2a2a);
    border-radius: 4px;
  }

  .command-palette__results {
    flex: 1;
    overflow-y: auto;
    padding: 0.5rem;
  }

  .command-palette__category {
    margin-bottom: 1rem;
  }

  .command-palette__category-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    color: var(--text-secondary, #888);
    padding: 0.5rem 0.75rem;
    letter-spacing: 0.5px;
  }

  .command-palette__item {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem;
    background: transparent;
    border: none;
    border-radius: 6px;
    color: var(--text-primary, #fff);
    cursor: pointer;
    transition: background 0.1s;
    text-align: left;
  }

  .command-palette__item:hover,
  .command-palette__item--selected {
    background: var(--background-secondary, #2a2a2a);
  }

  .command-palette__item-icon {
    font-size: 1.125rem;
    width: 1.5rem;
    text-align: center;
    color: var(--text-secondary, #888);
  }

  .command-palette__item-content {
    flex: 1;
    min-width: 0;
  }

  .command-palette__item-label {
    font-weight: 500;
    margin-bottom: 0.125rem;
  }

  .command-palette__item-description {
    font-size: 0.875rem;
    color: var(--text-secondary, #888);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .command-palette__item-shortcut {
    font-size: 0.75rem;
    padding: 0.25rem 0.5rem;
    background: var(--background-tertiary, #333);
    border-radius: 4px;
    color: var(--text-secondary, #888);
    font-family: monospace;
  }

  .command-palette__loading,
  .command-palette__empty {
    text-align: center;
    padding: 2rem;
    color: var(--text-secondary, #888);
  }

  .command-palette__footer {
    display: flex;
    gap: 1.5rem;
    padding: 0.75rem 1rem;
    border-top: 1px solid var(--border-color, #333);
    font-size: 0.75rem;
    color: var(--text-secondary, #888);
  }

  .command-palette__footer kbd {
    padding: 0.125rem 0.375rem;
    background: var(--background-secondary, #2a2a2a);
    border-radius: 3px;
    font-family: monospace;
    font-size: 0.7rem;
  }
</style>
