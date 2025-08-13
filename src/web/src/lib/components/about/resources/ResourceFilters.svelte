<!--
Resource Filters Component

Handles search and category filtering for the resources list.
-->
<script lang="ts">
  import { categories, levels, resources } from './resourcesData';

  // Bindable props
  let {
    searchTerm = $bindable(''),
    selectedCategory = $bindable('all'), 
    selectedLevel = $bindable('all')
  } = $props<{
    searchTerm?: string;
    selectedCategory?: string;
    selectedLevel?: string;
  }>();

  function getResourceCountForCategory(categoryValue: string): number {
    if (categoryValue === 'all') {
      return resources.length;
    }
    return resources.filter(resource => resource.category === categoryValue).length;
  }
</script>

<div class="filters-section">
  <!-- Search -->
  <div class="search-section">
    <div class="search-container">
      <input
        type="text"
        placeholder="Search resources..."
        bind:value={searchTerm}
        class="search-input"
      />
      <span class="search-icon">🔍</span>
    </div>
  </div>

  <!-- Level Filter -->
  <div class="level-filter">
    <label for="level-select">Level:</label>
    <select id="level-select" bind:value={selectedLevel}>
      {#each levels as level}
        <option value={level.value}>{level.label}</option>
      {/each}
    </select>
  </div>

  <!-- Category Tabs -->
  <nav class="categories-nav" aria-label="Resource categories">
    {#each categories as category}
      <button
        type="button"
        class="category-tab"
        class:active={selectedCategory === category.value}
        onclick={() => selectedCategory = category.value}
        aria-pressed={selectedCategory === category.value}
      >
        <span class="tab-label">{category.label}</span>
        <span class="tab-count">({getResourceCountForCategory(category.value)})</span>
      </button>
    {/each}
  </nav>
</div>

<style>
  .filters-section {
    margin-bottom: var(--spacing-xl);
  }

  /* Search */
  .search-section {
    margin-bottom: var(--spacing-lg);
  }

  .search-container {
    position: relative;
    max-width: 500px;
    margin: 0 auto;
  }

  .search-input {
    width: 100%;
    padding: var(--spacing-md) var(--spacing-lg) var(--spacing-md) var(--spacing-xl);
    border: 2px solid var(--color-border);
    border-radius: var(--radius-lg);
    font-size: var(--font-size-md);
    background: var(--color-bg-secondary);
    color: var(--color-text-primary);
    transition: all 0.2s ease;
  }

  .search-input:focus {
    outline: none;
    border-color: var(--color-accent);
    box-shadow: 0 0 0 3px var(--color-accent-alpha);
  }

  .search-icon {
    position: absolute;
    left: var(--spacing-md);
    top: 50%;
    transform: translateY(-50%);
    color: var(--color-text-secondary);
    pointer-events: none;
  }

  /* Level Filter */
  .level-filter {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-sm);
    margin-bottom: var(--spacing-lg);
  }

  .level-filter label {
    font-weight: 600;
    color: var(--color-text-primary);
  }

  .level-filter select {
    padding: var(--spacing-sm) var(--spacing-md);
    border: 2px solid var(--color-border);
    border-radius: var(--radius-md);
    background: var(--color-bg-secondary);
    color: var(--color-text-primary);
    font-size: var(--font-size-sm);
  }

  /* Categories Navigation */
  .categories-nav {
    display: flex;
    justify-content: center;
    gap: var(--spacing-xs);
    border-bottom: 2px solid var(--color-border);
    flex-wrap: wrap;
  }

  .category-tab {
    background: none;
    border: none;
    padding: var(--spacing-md) var(--spacing-lg);
    cursor: pointer;
    border-bottom: 3px solid transparent;
    color: var(--color-text-secondary);
    font-weight: 500;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    white-space: nowrap;
  }

  .category-tab:hover {
    color: var(--color-text-primary);
    background: var(--color-bg-secondary);
  }

  .category-tab.active {
    color: var(--color-accent);
    border-bottom-color: var(--color-accent);
    background: var(--color-accent-alpha);
  }

  .tab-label {
    font-size: var(--font-size-sm);
  }

  .tab-count {
    font-size: var(--font-size-xs);
    opacity: 0.7;
    background: var(--color-bg-tertiary);
    padding: 2px 6px;
    border-radius: var(--radius-sm);
  }

  .category-tab.active .tab-count {
    background: var(--color-accent);
    color: white;
    opacity: 1;
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .categories-nav {
      overflow-x: auto;
      justify-content: flex-start;
      padding-bottom: var(--spacing-xs);
    }

    .category-tab {
      padding: var(--spacing-sm) var(--spacing-md);
      font-size: var(--font-size-xs);
    }

    .search-input {
      font-size: var(--font-size-sm);
    }
  }
</style>
