<!--
FilterPanel - Explore Filtering and Sorting Controls

Matches the legacy desktop app's FilterPanel structure:
1. Header: "Browse Sequences"
2. Sort controls: Sort dropdown + direction button
3. Filter sections: All, Favorites, Difficulty, etc.

Follows Svelte 5 runes + microservices architecture.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { ExploreFilterValue } from "../../shared/domain";
  import { ExploreSortMethod } from "../../shared/domain/enums/explore-enums";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    currentFilter = { type: "all", value: null },
    currentSort = ExploreSortMethod.ALPHABETICAL,
    sortDirection = "asc",
    onFilterChange = () => {},
    onSortChange = () => {},
  } = $props<{
    currentFilter?: { type: string; value: ExploreFilterValue };
    currentSort?: ExploreSortMethod;
    sortDirection?: "asc" | "desc";
    onFilterChange?: (type: string, value?: ExploreFilterValue) => void;
    onSortChange?: (
      method: ExploreSortMethod,
      direction: "asc" | "desc"
    ) => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Filter sections matching legacy app
  const filterSections = [
    { id: "all", label: "All Sequences" },
    { id: "favorites", label: "Favorites" },
    { id: "difficulty", label: "Difficulty Level" },
    { id: "startingPosition", label: "Starting Position" },
    { id: "startingLetter", label: "Starting Letter" },
    { id: "containsLetters", label: "Contains Letters" },
    { id: "length", label: "Sequence Length" },
    { id: "gridMode", label: "Grid Mode" },
    { id: "tag", label: "Tags" },
  ];

  // Sort options matching legacy app
  const sortOptions = [
    { id: ExploreSortMethod.ALPHABETICAL, label: "Alphabetical" },
    { id: ExploreSortMethod.DIFFICULTY_LEVEL, label: "Difficulty" },
    { id: ExploreSortMethod.DATE_ADDED, label: "Date Added" },
    { id: ExploreSortMethod.SEQUENCE_LENGTH, label: "Length" },
  ];

  // Difficulty levels
  const difficultyLevels = [1, 2, 3, 4, 5];

  // Starting positions
  const startingPositions = ["home", "extended", "split", "opposite"];

  // Grid modes
  const gridModes = ["diamond", "box"];

  // Common tags
  const commonTags = [
    "beginner",
    "intermediate",
    "advanced",
    "expert",
    "master",
    "tutorial",
    "performance",
    "showcase",
  ];

  // Sequence lengths
  const sequenceLengths = [2, 4, 6, 8, 10, 12, 16];

  // Letters for filtering
  const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");

  // State for multi-select filters
  let selectedLetters = $state<string[]>([]);
  let localSort = $state<ExploreSortMethod>(currentSort);

  // Apply a filter
  function applyFilter(type: string, value?: ExploreFilterValue) {
    // Trigger selection haptic feedback for filter selection
    hapticService?.trigger("selection");

    onFilterChange(type, value);
  }

  // Apply a sort
  function applySort(method: ExploreSortMethod, direction: "asc" | "desc") {
    // Trigger selection haptic feedback for sort change
    hapticService?.trigger("selection");

    onSortChange(method, direction);
  }

  // Handle sort change
  function handleSortChange() {
    applySort(localSort, sortDirection);
  }

  // Toggle sort direction
  function toggleSortDirection() {
    // Trigger selection haptic feedback for sort direction toggle
    hapticService?.trigger("selection");

    const newDirection = sortDirection === "asc" ? "desc" : "asc";
    applySort(localSort, newDirection);
  }

  // Toggle letter selection for "Contains Letters" filter
  function toggleLetter(letter: string) {
    // Trigger selection haptic feedback for letter toggle
    hapticService?.trigger("selection");

    if (selectedLetters.includes(letter)) {
      selectedLetters = selectedLetters.filter((l) => l !== letter);
    } else {
      selectedLetters = [...selectedLetters, letter];
    }

    if (selectedLetters.length > 0) {
      applyFilter("containsLetters", selectedLetters);
    } else {
      applyFilter("all");
    }
  }

  // Check if filter is active
  function isFilterActive(type: string, value?: ExploreFilterValue): boolean {
    if (currentFilter.type !== type) return false;
    if (value === undefined) return true;
    return currentFilter.value === value;
  }
</script>

<div class="filter-panel">
  <div class="filter-header">
    <h2>Browse Sequences</h2>
  </div>

  <div class="sort-controls">
    <label for="sort-select">Sort by:</label>
    <div class="sort-select-container">
      <select
        id="sort-select"
        bind:value={localSort}
        onchange={handleSortChange}
      >
        {#each sortOptions as option}
          <option value={option.id}>{option.label}</option>
        {/each}
      </select>

      <button
        class="sort-direction-button"
        onclick={toggleSortDirection}
        aria-label={sortDirection === "asc"
          ? "Sort ascending"
          : "Sort descending"}
      >
        {#if sortDirection === "asc"}
          <span class="sort-icon">↑</span>
        {:else}
          <span class="sort-icon">↓</span>
        {/if}
      </button>
    </div>
  </div>

  <div class="filter-sections">
    <h3>Filter By</h3>

    <!-- Basic filters -->
    <div class="filter-section">
      <button
        class="filter-button"
        class:active={isFilterActive("all")}
        onclick={() => applyFilter("all")}
      >
        All Sequences
      </button>

      <button
        class="filter-button"
        class:active={isFilterActive("favorites")}
        onclick={() => applyFilter("favorites")}
      >
        Favorites
      </button>
    </div>

    <!-- Difficulty filter -->
    <div class="filter-section">
      <h4>Difficulty Level</h4>
      <div class="button-grid">
        {#each difficultyLevels as level}
          <button
            class="filter-button"
            class:active={isFilterActive("difficulty", level)}
            onclick={() => applyFilter("difficulty", level)}
          >
            {level}
          </button>
        {/each}
      </div>
    </div>

    <!-- Starting Position filter -->
    <div class="filter-section">
      <h4>Starting Position</h4>
      <div class="button-grid">
        {#each startingPositions as position}
          <button
            class="filter-button"
            class:active={isFilterActive("startingPosition", position)}
            onclick={() => applyFilter("startingPosition", position)}
          >
            {position}
          </button>
        {/each}
      </div>
    </div>

    <!-- Grid Mode filter -->
    <div class="filter-section">
      <h4>Grid Mode</h4>
      <div class="button-grid">
        {#each gridModes as mode}
          <button
            class="filter-button"
            class:active={isFilterActive("gridMode", mode)}
            onclick={() => applyFilter("gridMode", mode)}
          >
            {mode}
          </button>
        {/each}
      </div>
    </div>

    <!-- Starting Letter filter -->
    <div class="filter-section">
      <h4>Starting Letter</h4>
      <div class="letter-grid">
        {#each letters as letter}
          <button
            class="filter-button small"
            class:active={isFilterActive("startingLetter", letter)}
            onclick={() => applyFilter("startingLetter", letter)}
          >
            {letter}
          </button>
        {/each}
      </div>
    </div>

    <!-- Contains Letters filter -->
    <div class="filter-section">
      <h4>Contains Letters</h4>
      <div class="letter-grid">
        {#each letters as letter}
          <button
            class="filter-button small"
            class:active={selectedLetters.includes(letter)}
            onclick={() => toggleLetter(letter)}
          >
            {letter}
          </button>
        {/each}
      </div>
      {#if selectedLetters.length > 0}
        <div class="selected-letters">
          <span>Selected: {selectedLetters.join(", ")}</span>
          <button
            class="clear-button"
            onclick={() => {
              selectedLetters = [];
              applyFilter("all");
            }}
          >
            Clear
          </button>
        </div>
      {/if}
    </div>

    <!-- Sequence Length filter -->
    <div class="filter-section">
      <h4>Sequence Length</h4>
      <div class="button-grid">
        {#each sequenceLengths as length}
          <button
            class="filter-button small"
            class:active={isFilterActive("length", length)}
            onclick={() => applyFilter("length", length)}
          >
            {length}
          </button>
        {/each}
      </div>
    </div>

    <!-- Tags filter -->
    <div class="filter-section">
      <h4>Tags</h4>
      <div class="tag-grid">
        {#each commonTags as tag}
          <button
            class="filter-button tag"
            class:active={isFilterActive("tag", tag)}
            onclick={() => applyFilter("tag", tag)}
          >
            {tag}
          </button>
        {/each}
      </div>
    </div>
  </div>
</div>

<style>
  .filter-panel {
    display: flex;
    flex-direction: column;
    height: 100%;
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
    overflow-y: auto;
  }

  .filter-header {
    padding: var(--spacing-lg);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.05);
  }

  .filter-header h2 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: white;
  }

  .sort-controls {
    padding: var(--spacing-lg);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.03);
  }

  .sort-controls label {
    display: block;
    margin-bottom: var(--spacing-sm);
    font-size: 0.9rem;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.8);
  }

  .sort-select-container {
    display: flex;
    gap: var(--spacing-sm);
    align-items: center;
  }

  .sort-select-container select {
    flex: 1;
    padding: var(--spacing-sm);
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--border-radius);
    color: white;
    font-size: 0.9rem;
  }

  .sort-select-container select:focus {
    outline: none;
    border-color: var(--accent-color);
    box-shadow: 0 0 0 2px rgba(var(--accent-color-rgb), 0.2);
  }

  .sort-direction-button {
    padding: var(--spacing-sm);
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--border-radius);
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 40px;
  }

  .sort-direction-button:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
  }

  .sort-icon {
    font-size: 1.1rem;
    font-weight: bold;
  }

  .filter-sections {
    flex: 1;
    padding: var(--spacing-lg);
  }

  .filter-sections h3 {
    margin: 0 0 var(--spacing-lg) 0;
    font-size: 1.1rem;
    font-weight: 600;
    color: white;
  }

  .filter-section {
    margin-bottom: var(--spacing-xl);
  }

  .filter-section h4 {
    margin: 0 0 var(--spacing-md) 0;
    font-size: 0.95rem;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.9);
  }

  .filter-button {
    padding: var(--spacing-sm) var(--spacing-md);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius);
    color: rgba(255, 255, 255, 0.8);
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 0.9rem;
    margin-bottom: var(--spacing-sm);
    width: 100%;
    text-align: left;
  }

  .filter-button:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    color: white;
  }

  .filter-button.active {
    background: var(--accent-color);
    border-color: var(--accent-color);
    color: white;
    font-weight: 500;
  }

  .button-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-sm);
  }

  .letter-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: var(--spacing-xs);
  }

  .tag-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-sm);
  }

  .filter-button.small {
    padding: var(--spacing-xs) var(--spacing-sm);
    font-size: 0.8rem;
    text-align: center;
  }

  .filter-button.tag {
    font-size: 0.85rem;
  }

  .selected-letters {
    margin-top: var(--spacing-md);
    padding: var(--spacing-sm);
    background: rgba(255, 255, 255, 0.05);
    border-radius: var(--border-radius);
    font-size: 0.85rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .clear-button {
    padding: var(--spacing-xs) var(--spacing-sm);
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--border-radius);
    color: white;
    cursor: pointer;
    font-size: 0.8rem;
    transition: all 0.2s ease;
  }

  .clear-button:hover {
    background: rgba(255, 255, 255, 0.15);
  }
</style>
