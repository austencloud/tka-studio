<script lang="ts">
  import { onMount } from "svelte";
  import type { IHapticFeedbackService } from "../../../../shared/application/services/contracts";
  import { resolve, TYPES } from "../../../../shared/inversify";
  import { ExploreSortMethod } from "../../shared";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    sortBy = ExploreSortMethod.ALPHABETICAL,
    viewMode = "grid",
    onSortChange = () => {},
    onViewModeChange = () => {},
  } = $props<{
    sortBy?: ExploreSortMethod;
    viewMode?: "grid" | "list";
    onSortChange?: (sortBy: ExploreSortMethod) => void;
    onViewModeChange?: (viewMode: "grid" | "list") => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService | null = $state(null);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Sort options
  const sortOptions = [
    { value: ExploreSortMethod.ALPHABETICAL, label: "Name A-Z" },
    { value: ExploreSortMethod.DIFFICULTY_LEVEL, label: "Difficulty" },
    { value: ExploreSortMethod.SEQUENCE_LENGTH, label: "Length" },
    { value: ExploreSortMethod.DATE_ADDED, label: "Recently Added" },
    { value: ExploreSortMethod.AUTHOR, label: "Author" },
  ];

  // Handle sort change
  function handleSortChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    const newSortBy = target.value as ExploreSortMethod;
    hapticService?.trigger("selection");
    onSortChange(newSortBy);
  }

  // Handle view mode change
  function handleViewModeChange(newViewMode: "grid" | "list") {
    hapticService?.trigger("selection");
    onViewModeChange(newViewMode);
  }
</script>

<div class="header-right">
  <div class="view-controls">
    <label class="sort-control">
      Sort by:
      <select value={sortBy} onchange={handleSortChange}>
        {#each sortOptions as option}
          <option value={option.value}>{option.label}</option>
        {/each}
      </select>
    </label>

    <div class="view-mode-toggle">
      <button
        class="view-button"
        class:active={viewMode === "grid"}
        onclick={() => handleViewModeChange("grid")}
        title="Grid View"
        aria-label="Switch to grid view"
        type="button"
      >
        <svg width="16" height="16" viewBox="0 0 16 16">
          <rect x="1" y="1" width="6" height="6" fill="currentColor" />
          <rect x="9" y="1" width="6" height="6" fill="currentColor" />
          <rect x="1" y="9" width="6" height="6" fill="currentColor" />
          <rect x="9" y="9" width="6" height="6" fill="currentColor" />
        </svg>
      </button>
      <button
        class="view-button"
        class:active={viewMode === "list"}
        onclick={() => handleViewModeChange("list")}
        title="List View"
        aria-label="Switch to list view"
        type="button"
      >
        <svg width="16" height="16" viewBox="0 0 16 16">
          <rect x="1" y="2" width="14" height="2" fill="currentColor" />
          <rect x="1" y="7" width="14" height="2" fill="currentColor" />
          <rect x="1" y="12" width="14" height="2" fill="currentColor" />
        </svg>
      </button>
    </div>
  </div>
</div>

<style>
  .header-right {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
  }

  .view-controls {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
  }

  .sort-control {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    font-size: var(--font-size-sm);
    color: var(--muted-foreground);
  }

  .sort-control select {
    padding: var(--spacing-xs) var(--spacing-sm);
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 6px;
    color: #ffffff;
    font-family: inherit;
    font-size: var(--font-size-sm);
  }

  .sort-control select option {
    background: #1a1a1a;
    color: #ffffff;
    padding: var(--spacing-xs);
  }

  .view-mode-toggle {
    display: flex;
    background: rgba(255, 255, 255, 0.05);
    border: var(--glass-border);
    border-radius: 6px;
    overflow: hidden;
  }

  .view-button {
    padding: var(--spacing-xs);
    background: transparent;
    border: none;
    color: var(--muted-foreground);
    cursor: pointer;
    transition: all var(--transition-fast);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .view-button:hover {
    background: rgba(255, 255, 255, 0.1);
    color: var(--foreground);
  }

  .view-button.active {
    background: var(--primary-color);
    color: white;
  }

  /* Mobile-first responsive design */
  @media (max-width: 480px) {
    .header-right {
      flex-direction: column;
      gap: var(--spacing-sm);
      align-items: stretch;
    }

    .view-controls {
      flex-direction: column;
      gap: var(--spacing-sm);
    }

    .sort-control {
      font-size: 1rem;
      justify-content: space-between;
    }

    .sort-control select {
      padding: 12px 16px;
      font-size: 1rem;
      min-height: 44px;
      border-radius: 8px;
      flex: 1;
      margin-left: var(--spacing-sm);
    }

    .view-mode-toggle {
      align-self: center;
      border-radius: 8px;
    }

    .view-button {
      padding: 12px 16px;
      min-width: 44px;
      min-height: 44px;
    }

    .view-button svg {
      width: 20px;
      height: 20px;
    }
  }

  /* Tablet responsive design */
  @media (min-width: 481px) and (max-width: 768px) {
    .sort-control select {
      padding: 10px 14px;
      font-size: 0.9375rem;
      min-height: 40px;
    }

    .view-button {
      padding: 10px 12px;
      min-width: 40px;
      min-height: 40px;
    }

    .view-button svg {
      width: 18px;
      height: 18px;
    }
  }
</style>
