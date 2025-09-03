<!-- src/lib/components/BrowseTab/FilterPanel/FilterPanel.svelte -->
<script lang="ts">
  import { browseTabStore, type FilterCriteria, type SortCriteria } from '$lib/stores/browseTab/browseTabStore';
  import { onMount } from 'svelte';

  // Filter sections
  const filterSections = [
    { id: 'all', label: 'All Sequences' },
    { id: 'favorites', label: 'Favorites' },
    { id: 'difficulty', label: 'Difficulty Level' },
    { id: 'startingPosition', label: 'Starting Position' },
    { id: 'startingLetter', label: 'Starting Letter' },
    { id: 'containsLetters', label: 'Contains Letters' },
    { id: 'length', label: 'Sequence Length' },
    { id: 'gridMode', label: 'Grid Mode' },
    { id: 'tag', label: 'Tags' }
  ];

  // Sort options
  const sortOptions = [
    { id: 'alphabetical', label: 'Alphabetical' },
    { id: 'difficulty', label: 'Difficulty' },
    { id: 'dateAdded', label: 'Date Added' },
    { id: 'length', label: 'Length' }
  ];

  // Difficulty levels
  const difficultyLevels = [1, 2, 3, 4, 5];

  // Starting positions
  const startingPositions = ['home', 'extended', 'split', 'opposite'];

  // Grid modes
  const gridModes = ['diamond', 'box'];

  // Common tags
  const commonTags = ['beginner', 'intermediate', 'advanced', 'expert', 'master', 'tutorial', 'performance', 'showcase'];

  // Sequence lengths
  const sequenceLengths = [2, 4, 6, 8, 10, 12, 16];

  // Letters for filtering
  const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');

  // State
  let activeSection = 'all';
  let selectedLetters: string[] = [];
  let sortDirection: 'asc' | 'desc' = 'asc';
  let currentSort = 'alphabetical';

  // Apply a filter
  function applyFilter(filter: FilterCriteria) {
    activeSection = filter.type;
    browseTabStore.applyFilter(filter);
  }

  // Apply a sort
  function applySort(field: string, direction: 'asc' | 'desc') {
    currentSort = field;
    sortDirection = direction;

    const sortCriteria: SortCriteria = {
      field: field as any,
      direction
    };

    browseTabStore.applySort(sortCriteria);
  }

  // Toggle sort direction
  function toggleSortDirection() {
    const newDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    applySort(currentSort, newDirection);
  }

  // Toggle letter selection for "Contains Letters" filter
  function toggleLetter(letter: string) {
    if (selectedLetters.includes(letter)) {
      selectedLetters = selectedLetters.filter(l => l !== letter);
    } else {
      selectedLetters = [...selectedLetters, letter];
    }

    if (selectedLetters.length > 0) {
      applyFilter({
        type: 'containsLetters',
        value: selectedLetters
      });
    } else {
      applyFilter({ type: 'all' });
    }
  }

  // Initialize with "All" filter
  onMount(() => {
    applyFilter({ type: 'all' });
    applySort('alphabetical', 'asc');
  });
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
        bind:value={currentSort}
        on:change={() => applySort(currentSort, sortDirection)}
      >
        {#each sortOptions as option}
          <option value={option.id}>{option.label}</option>
        {/each}
      </select>

      <button
        class="sort-direction-button"
        on:click={toggleSortDirection}
        aria-label={sortDirection === 'asc' ? 'Sort ascending' : 'Sort descending'}
      >
        {#if sortDirection === 'asc'}
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
        class:active={activeSection === 'all'}
        on:click={() => applyFilter({ type: 'all' })}
      >
        All Sequences
      </button>

      <button
        class="filter-button"
        class:active={activeSection === 'favorites'}
        on:click={() => applyFilter({ type: 'favorites' })}
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
            class="filter-button small"
            class:active={activeSection === 'difficulty' && $browseTabStore.currentFilter.value === level}
            on:click={() => applyFilter({ type: 'difficulty', value: level })}
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
            class:active={activeSection === 'startingPosition' && $browseTabStore.currentFilter.value === position}
            on:click={() => applyFilter({ type: 'startingPosition', value: position })}
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
            class:active={activeSection === 'gridMode' && $browseTabStore.currentFilter.value === mode}
            on:click={() => applyFilter({ type: 'gridMode', value: mode })}
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
            class:active={activeSection === 'startingLetter' && $browseTabStore.currentFilter.value === letter}
            on:click={() => applyFilter({ type: 'startingLetter', value: letter })}
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
            on:click={() => toggleLetter(letter)}
          >
            {letter}
          </button>
        {/each}
      </div>
      {#if selectedLetters.length > 0}
        <div class="selected-letters">
          <span>Selected: {selectedLetters.join(', ')}</span>
          <button
            class="clear-button"
            on:click={() => {
              selectedLetters = [];
              applyFilter({ type: 'all' });
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
            class:active={activeSection === 'length' && $browseTabStore.currentFilter.value === length}
            on:click={() => applyFilter({ type: 'length', value: length })}
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
            class:active={activeSection === 'tag' && $browseTabStore.currentFilter.value === tag}
            on:click={() => applyFilter({ type: 'tag', value: tag })}
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
    height: 100%;
    overflow-y: auto;
    padding: 1rem;
    background-color: var(--background-color-secondary, #252525);
  }

  .filter-header {
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border-color, #333333);
  }

  .filter-header h2 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
  }

  .sort-controls {
    margin-bottom: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .sort-select-container {
    display: flex;
    align-items: center;
  }

  .sort-select-container select {
    flex: 1;
    padding: 0.5rem;
    background-color: var(--input-background, #333333);
    color: var(--text-color, #ffffff);
    border: 1px solid var(--border-color, #444444);
    border-radius: 4px;
    appearance: none;
  }

  .sort-direction-button {
    margin-left: 0.5rem;
    padding: 0.5rem;
    background-color: var(--input-background, #333333);
    color: var(--text-color, #ffffff);
    border: 1px solid var(--border-color, #444444);
    border-radius: 4px;
    cursor: pointer;
  }

  .sort-icon {
    font-size: 1rem;
  }

  .filter-sections {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .filter-sections h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.2rem;
    font-weight: 600;
  }

  .filter-section {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .filter-section h4 {
    margin: 0 0 0.5rem 0;
    font-size: 1rem;
    font-weight: 500;
    color: var(--text-color-secondary, #aaaaaa);
  }

  .button-grid,
  .letter-grid,
  .tag-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .filter-button {
    padding: 0.5rem 1rem;
    background-color: var(--button-background, #333333);
    color: var(--text-color, #ffffff);
    border: 1px solid var(--border-color, #444444);
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s, border-color 0.2s;
    font-size: 0.9rem;
  }

  .filter-button.small {
    padding: 0.3rem 0.6rem;
    font-size: 0.8rem;
  }

  .filter-button.tag {
    background-color: var(--tag-background, #2a3a4a);
    border-color: var(--tag-border-color, #3a4a5a);
  }

  .filter-button:hover {
    background-color: var(--button-hover-background, #444444);
  }

  .filter-button.active {
    background-color: var(--primary-color, #4a90e2);
    border-color: var(--primary-color-dark, #3a80d2);
    color: white;
  }

  .selected-letters {
    margin-top: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.9rem;
  }

  .clear-button {
    padding: 0.2rem 0.5rem;
    background-color: var(--danger-color-muted, #553333);
    color: var(--text-color, #ffffff);
    border: 1px solid var(--danger-color, #ff5555);
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.8rem;
  }

  .clear-button:hover {
    background-color: var(--danger-color, #ff5555);
  }
</style>
