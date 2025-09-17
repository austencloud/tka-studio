<!--
OptionPickerHeader.svelte - Header with title and button-based filters

Provides:
- "Choose Your Next Option" title (desktop styling)
- Button-based sort method filters (legacy style)
- Button-based reversal filters (legacy style)
- ViewControl dropdown (legacy style, top-right positioned)
-->
<script lang="ts">
  import SortControl from "./SortControl.svelte";


  type ViewModeDetail =
    | { mode: "all" }
    | { mode: "group"; method: string };

  // Props for controlling sort state and filtering
  const {
    sortMethod = "type",
    onSortMethodChanged = () => {},
    optionPickerState = null,
  }: {
    sortMethod?: string;
    onSortMethodChanged?: (method: string) => void;
    optionPickerState?: any;
  } = $props();

  // Filter state for different sort methods - sync with actual state
  const typeFilters = $derived(() => {
    if (optionPickerState?.typeFilter) {
      const filter = optionPickerState.typeFilter;
      return [
        { number: "1", enabled: filter.type1 },
        { number: "2", enabled: filter.type2 },
        { number: "3", enabled: filter.type3 },
        { number: "4", enabled: filter.type4 },
        { number: "5", enabled: filter.type5 },
        { number: "6", enabled: filter.type6 },
      ];
    }
    // Fallback if no state available
    return [
      { number: "1", enabled: true },
      { number: "2", enabled: true },
      { number: "3", enabled: true },
      { number: "4", enabled: true },
      { number: "5", enabled: true },
      { number: "6", enabled: true },
    ];
  });

  let endPositionFilters = $state([
    { position: "alpha", label: "Alpha", enabled: true },
    { position: "beta", label: "Beta", enabled: true },
    { position: "gamma", label: "Gamma", enabled: true },
  ]);

  let reversalFilters = $state([
    { type: "continuous", label: "Continuous", enabled: true },
    { type: "1-reversal", label: "1 Reversal", enabled: true },
    { type: "2-reversals", label: "2 Reversals", enabled: true },
  ]);

  // Filter toggle functions
  function toggleTypeFilter(index: number) {
    // Update actual filtering logic if state is available
    if (optionPickerState?.toggleTypeFilter) {
      optionPickerState.toggleTypeFilter(index + 1); // Convert 0-based to 1-based
    }
  }

  function toggleEndPositionFilter(position: string) {
    const filter = endPositionFilters.find(f => f.position === position);
    if (filter) {
      filter.enabled = !filter.enabled;
    }
  }

  function toggleReversalFilter(type: string) {
    const filter = reversalFilters.find(f => f.type === type);
    if (filter) {
      filter.enabled = !filter.enabled;
    }
  }

  // ViewControl handler
  function handleViewChange(detail: ViewModeDetail) {
    console.log("ViewControl changed:", detail);
    if (detail.mode === "all") {
      onSortMethodChanged("all");
    } else if (detail.mode === "group" && detail.method) {
      onSortMethodChanged(detail.method);
    }
  }
</script>

<div class="option-picker-header">
  <div class="header-content">
    <div class="filter-buttons">
      {#if sortMethod === 'all'}
        <span class="showing-all-text">Showing All</span>
      {:else if sortMethod === 'type'}
        {#each typeFilters() as filter, index}
          <button
            class="filter-btn type-filter"
            class:active={filter.enabled}
            onclick={() => toggleTypeFilter(index)}
          >
            {filter.number}
          </button>
        {/each}
      {:else if sortMethod === 'endPosition'}
        {#each endPositionFilters as filter}
          <button
            class="filter-btn end-position-filter"
            class:active={filter.enabled}
            onclick={() => toggleEndPositionFilter(filter.position)}
          >
            {filter.label}
          </button>
        {/each}
      {:else if sortMethod === 'reversals'}
        {#each reversalFilters as filter}
          <button
            class="filter-btn reversal-filter"
            class:active={filter.enabled}
            onclick={() => toggleReversalFilter(filter.type)}
          >
            {filter.label}
          </button>
        {/each}
      {/if}
    </div>
    <div class="view-controls">
      <SortControl
        initialSortMethod={sortMethod}
        onViewChange={handleViewChange}
      />
    </div>
  </div>
</div>

<style>
  .option-picker-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: transparent;
    border-bottom: 1px solid var(--border, #e5e7eb);
    gap: 16px;
    position: relative;
    width: 100%;
    overflow: visible;
  }

  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    flex-wrap: nowrap;
    padding: 8px 20px; /* Increased padding to accommodate hover effects */
    min-height: 60px; /* Ensure enough height for button hover effects */
    overflow: visible;
  }

  .filter-buttons {
    display: flex;
    align-items: center;
    gap: 6px;
    flex: 1;
    max-width: calc(100% - 120px); /* Reserve space for ViewControl */
    overflow: visible; /* Allow hover effects to show */
    min-height: 50px; /* Ensure enough height for button hover effects */
  }

  .showing-all-text {
    font-size: 14px;
    color: var(--foreground, #000000);
    font-weight: 500;
    opacity: 0.7;
    white-space: nowrap;
  }

  .filter-btn {
    /* Dynamic width based on available space */
    flex: 1;

    /* Glass morphism styling to match TKA design system */
    padding: 8px 12px;
    background: var(--surface-color);
    backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-radius: 12px;
    box-shadow: var(--shadow-glass);
    color: var(--foreground);
    cursor: pointer;
    transition: all var(--transition-normal);

    /* Layout */
    display: flex;
    align-items: center;
    justify-content: center;

    /* Text handling */
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;

    /* Touch-friendly */
    touch-action: manipulation;
    user-select: none;

    /* Position for glass overlay */
    position: relative;
    overflow: hidden;
  }

  .filter-btn::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.1) 0%,
      rgba(255, 255, 255, 0.05) 50%,
      rgba(255, 255, 255, 0) 100%
    );
    opacity: 0;
    transition: opacity var(--transition-fast);
    border-radius: inherit;
  }

  .filter-btn:hover {
    background: var(--surface-hover);
    border: var(--glass-border-hover);
    box-shadow: var(--shadow-glass-hover);
    transform: translateY(-1px);
  }

  .filter-btn:hover::before {
    opacity: 1;
  }

  .filter-btn.active {
    background: var(--surface-color); /* Keep elegant glass background */
    color: #d4af37; /* Rich gold text */
    border: 2px solid #d4af37; /* Gold outline */
    box-shadow:
      0 0 0 1px rgba(212, 175, 55, 0.3), /* Inner glow */
      0 0 12px rgba(212, 175, 55, 0.4), /* Outer glow */
      var(--shadow-glass); /* Maintain glass shadow */
    backdrop-filter: var(--glass-backdrop); /* Keep glass effect */
  }

  .filter-btn.active:hover {
    background: var(--surface-color);
    color: #f4d03f; /* Brighter gold on hover */
    border: 2px solid #f4d03f;
    transform: translateY(-1px);
    box-shadow:
      0 0 0 1px rgba(244, 208, 63, 0.4), /* Enhanced inner glow */
      0 0 16px rgba(244, 208, 63, 0.6), /* Enhanced outer glow */
      var(--shadow-glass-hover); /* Enhanced glass shadow */
  }

  .filter-btn:active {
    transform: translateY(0);
  }

  .view-controls {
    display: flex;
    align-items: center;
    flex-shrink: 0;
    overflow: visible;
  }



  /* Responsive adjustments */
  @media (max-width: 768px) {
    .option-picker-header {
      gap: 12px;
    }

    .header-content {
      flex-direction: column;
      align-items: center;
      gap: 16px;
      padding: 0 12px;
    }

    .filter-buttons {
      justify-content: center;
      flex-wrap: wrap;
      gap: 4px;
      max-width: 100%;
    }

    .view-controls {
      align-self: flex-end;
    }



    .filter-btn {
      flex: 0 1 auto; /* Don't grow, allow shrink */
      min-width: 60px;
      max-width: 100px;
      padding: 6px 8px;
      font-size: 12px;
      height: 36px;
    }
  }

  @media (max-width: 480px) {

    .header-content {
      padding: 0 8px;
      gap: 12px;
    }



    .filter-buttons {
      flex-wrap: wrap;
      justify-content: center;
      gap: 3px;
      max-width: 100%;
    }

    .filter-btn {
      flex: 0 1 auto;
      min-width: 50px;
      max-width: 80px;
      padding: 4px 6px;
      font-size: 11px;
      height: 32px;
      border-width: 1px;
    }

    .view-controls {
      position: absolute;
      top: 8px;
      right: 8px;
    }
  }
</style>
