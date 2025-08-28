<!--
OptionPickerHeader.svelte - Header with title and sorting controls

Provides:
- "Choose Your Next Option" title (desktop styling)
- Sort method dropdown
- Reversal filter controls
-->
<script lang="ts">
  // Props for controlling sort and filter state
  const {
    sortMethod = "alphabetical",
    reversalFilter = "all",
    onSortMethodChanged = () => {},
    onReversalFilterChanged = () => {},
  } = $props<{
    sortMethod?: string;
    reversalFilter?: string;
    onSortMethodChanged?: (method: string) => void;
    onReversalFilterChanged?: (filter: string) => void;
  }>();

  // Available sort methods
  const sortMethods = [
    { value: "alphabetical", label: "A-Z" },
    { value: "complexity", label: "Complexity" },
    { value: "frequency", label: "Frequency" },
  ];

  // Available reversal filters
  const reversalFilters = [
    { value: "all", label: "All" },
    { value: "reversals", label: "Reversals Only" },
    { value: "no-reversals", label: "No Reversals" },
  ];
</script>

<div class="option-picker-header">
  <div class="title-section">
    <h1 class="unified-title">Choose Your Next Option</h1>
  </div>

  <div class="controls-section">
    <div class="control-group">
      <label for="sort-method">Sort by:</label>
      <select
        id="sort-method"
        value={sortMethod}
        onchange={(e) => onSortMethodChanged(e.currentTarget.value)}
      >
        {#each sortMethods as method}
          <option value={method.value}>{method.label}</option>
        {/each}
      </select>
    </div>

    <div class="control-group">
      <label for="reversal-filter">Filter:</label>
      <select
        id="reversal-filter"
        value={reversalFilter}
        onchange={(e) => onReversalFilterChanged(e.currentTarget.value)}
      >
        {#each reversalFilters as filter}
          <option value={filter.value}>{filter.label}</option>
        {/each}
      </select>
    </div>
  </div>
</div>

<style>
  .option-picker-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: transparent;
    padding: 16px;
    border-bottom: 1px solid var(--border, #e5e7eb);
    gap: 16px;
  }

  .title-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
  }

  .unified-title {
    font-family: "Monotype Corsiva", cursive, serif;
    font-size: 24px;
    font-weight: bold;
    text-align: center;
    margin: 0;
    color: var(--foreground, #000000);
    letter-spacing: 0.5px;
  }

  .controls-section {
    display: flex;
    gap: 24px;
    align-items: center;
    flex-wrap: wrap;
    justify-content: center;
  }

  .control-group {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .control-group label {
    font-size: 14px;
    font-weight: 500;
    color: var(--foreground, #374151);
    white-space: nowrap;
  }

  .control-group select {
    padding: 6px 12px;
    border: 1px solid var(--border, #d1d5db);
    border-radius: 6px;
    background: var(--background, white);
    color: var(--foreground, #374151);
    font-size: 14px;
    cursor: pointer;
    transition: border-color 0.2s ease;
  }

  .control-group select:hover {
    border-color: var(--primary, #3b82f6);
  }

  .control-group select:focus {
    outline: none;
    border-color: var(--primary, #3b82f6);
    box-shadow: 0 0 0 2px var(--primary-alpha, rgba(59, 130, 246, 0.1));
  }

  /* Fallback fonts if Monotype Corsiva isn't available */
  @supports not (font-family: "Monotype Corsiva") {
    .unified-title {
      font-family: "Brush Script MT", "Lucida Handwriting", cursive, serif;
    }
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .controls-section {
      gap: 16px;
    }

    .unified-title {
      font-size: 20px;
    }

    .option-picker-header {
      padding: 12px;
    }
  }

  @media (max-width: 480px) {
    .controls-section {
      flex-direction: column;
      gap: 12px;
    }

    .control-group {
      flex-direction: column;
      gap: 4px;
      text-align: center;
    }

    .unified-title {
      font-size: 18px;
    }

    .option-picker-header {
      padding: 8px;
    }
  }
</style>
