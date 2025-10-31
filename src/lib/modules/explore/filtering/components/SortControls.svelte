<!--
SortControls.svelte

Sort controls component for the Explore module.
Provides sort dropdown, direction toggle, and filter button in the top section.

Follows Svelte 5 runes + microservices architecture.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import { ExploreSortMethod } from "../../shared/domain/enums/explore-enums";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    currentSort = ExploreSortMethod.ALPHABETICAL,
    sortDirection = "asc",
    onSortChange = () => {},
    onFilterClick = () => {},
  } = $props<{
    currentSort?: ExploreSortMethod;
    sortDirection?: "asc" | "desc";
    onSortChange?: (
      method: ExploreSortMethod,
      direction: "asc" | "desc"
    ) => void;
    onFilterClick?: () => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Sort options matching legacy app
  const sortOptions = [
    { id: ExploreSortMethod.ALPHABETICAL, label: "Alphabetical" },
    { id: ExploreSortMethod.DIFFICULTY_LEVEL, label: "Difficulty" },
    { id: ExploreSortMethod.DATE_ADDED, label: "Date Added" },
    { id: ExploreSortMethod.SEQUENCE_LENGTH, label: "Length" },
  ];

  // Local state for controlled component
  let localSort = $state<ExploreSortMethod>(currentSort);

  // Handle sort change
  function handleSortChange() {
    hapticService?.trigger("selection");
    onSortChange(localSort, sortDirection);
  }

  // Toggle sort direction
  function toggleSortDirection() {
    hapticService?.trigger("selection");
    const newDirection = sortDirection === "asc" ? "desc" : "asc";
    onSortChange(localSort, newDirection);
  }

  // Handle filter button click
  function handleFilterClick() {
    hapticService?.trigger("selection");
    onFilterClick();
  }
</script>

<div class="sort-controls">
  <!-- Filter button -->
  <button class="filter-button" onclick={handleFilterClick}>
    <span class="filter-icon">🔍</span>
    Filter
  </button>

  <!-- Sort controls -->
  <div class="sort-section">
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
</div>

<style>
  .sort-controls {
    display: flex;
    align-items: center;
    gap: 24px;
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .filter-button {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.2s ease;
  }

  .filter-button:hover {
    background: #0056b3;
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);
  }

  .filter-icon {
    font-size: 1rem;
  }

  .sort-section {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .sort-section label {
    font-size: 0.9rem;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.8);
    white-space: nowrap;
  }

  .sort-select-container {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  select {
    padding: 8px 12px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.05);
    color: white;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.2s ease;
    min-width: 140px;
  }

  select:hover {
    border-color: rgba(255, 255, 255, 0.3);
    background: rgba(255, 255, 255, 0.08);
  }

  select:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.2);
  }

  .sort-direction-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .sort-direction-button:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.3);
  }

  .sort-direction-button:active {
    transform: translateY(1px);
  }

  .sort-icon {
    font-size: 1.2rem;
    color: rgba(255, 255, 255, 0.8);
  }

  /* Responsive design */
  @media (max-width: 768px) {
    .sort-controls {
      flex-direction: column;
      gap: 16px;
      align-items: stretch;
    }

    .sort-section {
      justify-content: space-between;
    }

    .filter-button {
      justify-content: center;
    }
  }
</style>
