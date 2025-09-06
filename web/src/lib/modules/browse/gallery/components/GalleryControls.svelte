<script lang="ts">
  import { GallerySortMethod } from "../domain";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    sortBy = GallerySortMethod.ALPHABETICAL,
    viewMode = "grid",
    onSortChange = () => {},
    onViewModeChange = () => {},
  } = $props<{
    sortBy?: GallerySortMethod;
    viewMode?: "grid" | "list";
    onSortChange?: (sortBy: GallerySortMethod) => void;
    onViewModeChange?: (viewMode: "grid" | "list") => void;
  }>();

  // Sort options
  const sortOptions = [
    { value: GallerySortMethod.ALPHABETICAL, label: "Name A-Z" },
    { value: GallerySortMethod.difficultyLevel, label: "Difficulty" },
    { value: GallerySortMethod.sequenceLength, label: "Length" },
    { value: GallerySortMethod.dateAdded, label: "Recently Added" },
    { value: GallerySortMethod.AUTHOR, label: "Author" },
  ];

  // Handle sort change
  function handleSortChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    const newSortBy = target.value as GallerySortMethod;
    onSortChange(newSortBy);
  }

  // Handle view mode change
  function handleViewModeChange(newViewMode: "grid" | "list") {
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
    background: rgba(255, 255, 255, 0.1);
    border: var(--glass-border);
    border-radius: 6px;
    color: var(--foreground);
    font-family: inherit;
    font-size: var(--font-size-sm);
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
</style>
