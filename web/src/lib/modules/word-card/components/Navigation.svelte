<!-- Navigation.svelte - Simple navigation matching legacy desktop -->
<script lang="ts">
  // Props
  interface Props {
    selectedLength: number;
    columnCount: number;
    onLengthSelected: (length: number) => void;
    onColumnCountChanged: (count: number) => void;
  }

  let {
    selectedLength,
    columnCount,
    onLengthSelected,
    onColumnCountChanged,
  }: Props = $props();

  // Length options matching desktop exactly
  const lengthOptions = [
    { value: 0, label: "Show All" },
    { value: 2, label: "2 beats" },
    { value: 3, label: "3 beats" },
    { value: 4, label: "4 beats" },
    { value: 5, label: "5 beats" },
    { value: 6, label: "6 beats" },
    { value: 8, label: "8 beats" },
    { value: 10, label: "10 beats" },
    { value: 12, label: "12 beats" },
    { value: 16, label: "16 beats" },
  ];

  // Column options matching desktop
  const columnOptions = [
    { value: 1, label: "1 Column" },
    { value: 2, label: "2 Columns" },
    { value: 3, label: "3 Columns" },
    { value: 4, label: "4 Columns" },
    { value: 5, label: "5 Columns" },
    { value: 6, label: "6 Columns" },
  ];

  function handleLengthClick(length: number) {
    onLengthSelected(length);
  }

  function handleColumnChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    const newCount = parseInt(target.value);
    onColumnCountChanged(newCount);
  }
</script>

<div class="word-card-navigation">
  <!-- Header -->
  <div class="nav-header">
    <h2 class="nav-title">Navigation</h2>
    <p class="nav-subtitle">Filter and layout options</p>
  </div>

  <!-- Length Selection -->
  <div class="length-section">
    <h3 class="section-title">Sequence Length</h3>
    <div class="length-scroll-area">
      <div class="length-options">
        {#each lengthOptions as option (option.value)}
          <button
            class="length-button"
            class:selected={selectedLength === option.value}
            onclick={() => handleLengthClick(option.value)}
            title="Show sequences with {option.value === 0
              ? 'any length'
              : `${option.value} beats`}"
          >
            {option.label}
          </button>
          {#if option.value === 0}
            <div class="separator"></div>
          {/if}
        {/each}
      </div>
    </div>
  </div>

  <!-- Column Count Selection -->
  <div class="column-section">
    <h3 class="section-title">Page Layout</h3>
    <select
      class="column-select"
      value={columnCount}
      onchange={handleColumnChange}
    >
      {#each columnOptions as option (option.value)}
        <option value={option.value}>{option.label}</option>
      {/each}
    </select>
  </div>
</div>

<style>
  .word-card-navigation {
    height: 100%;
    padding: var(--spacing-lg);
    display: flex;
    flex-direction: column;
    gap: var(--spacing-lg);
    background: transparent;
  }

  /* Header */
  .nav-header {
    border-bottom: var(--glass-border);
    padding-bottom: var(--spacing-lg);
  }

  .nav-title {
    margin: 0 0 var(--spacing-xs) 0;
    font-size: var(--font-size-lg);
    font-weight: 600;
    color: var(--text-color);
    text-shadow: var(--text-shadow-glass);
  }

  .nav-subtitle {
    margin: 0;
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
  }

  /* Section Titles */
  .section-title {
    margin: 0 0 var(--spacing-md) 0;
    font-size: var(--font-size-sm);
    font-weight: 500;
    color: var(--text-color);
  }

  /* Length Selection */
  .length-section {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-height: 0;
  }

  .length-scroll-area {
    flex: 1;
    overflow-y: auto;
    min-height: 120px;
    max-height: 400px;
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
  }

  .length-scroll-area::-webkit-scrollbar {
    width: 8px;
  }

  .length-scroll-area::-webkit-scrollbar-track {
    background: transparent;
    border-radius: var(--border-radius-sm);
  }

  .length-scroll-area::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.2);
    border-radius: var(--border-radius-sm);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .length-scroll-area::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.3);
  }

  .length-options {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
  }

  .length-button {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--text-color);
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--border-radius-md);
    cursor: pointer;
    text-align: left;
    font-size: var(--font-size-sm);
    font-weight: 500;
    transition: all var(--transition-normal);
    backdrop-filter: blur(8px);
  }

  .length-button:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .length-button.selected {
    background: var(--primary-color);
    border-color: var(--primary-light);
    color: white;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
  }

  .separator {
    height: 1px;
    background: linear-gradient(
      90deg,
      transparent 0%,
      rgba(255, 255, 255, 0.1) 50%,
      transparent 100%
    );
    margin: var(--spacing-sm) 0;
  }

  /* Column Selection */
  .column-section {
    border-top: var(--glass-border);
    padding-top: var(--spacing-lg);
  }

  .column-select {
    width: 100%;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--text-color);
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--border-radius-md);
    font-size: var(--font-size-sm);
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition-normal);
    backdrop-filter: blur(8px);
  }

  .column-select:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
  }

  .column-select:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
  }

  .column-select option {
    background: var(--background);
    color: var(--text-color);
  }

  /* Responsive */
  @media (max-width: 768px) {
    .word-card-navigation {
      padding: var(--spacing-md);
      gap: var(--spacing-md);
    }

    .length-scroll-area {
      max-height: 150px;
    }

    .length-button {
      padding: var(--spacing-sm);
      font-size: var(--font-size-xs);
    }

    .column-select {
      padding: var(--spacing-sm);
      font-size: var(--font-size-xs);
    }
  }
</style>
