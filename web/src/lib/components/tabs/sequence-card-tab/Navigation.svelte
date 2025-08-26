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

<div class="sequence-card-navigation">
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
  .sequence-card-navigation {
    height: 100%;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    background: #2a2a2a;
  }

  /* Header */
  .nav-header {
    border-bottom: 1px solid #444;
    padding-bottom: 16px;
  }

  .nav-title {
    margin: 0 0 4px 0;
    font-size: 18px;
    font-weight: 600;
    color: white;
  }

  .nav-subtitle {
    margin: 0;
    font-size: 12px;
    color: #aaa;
  }

  /* Section Titles */
  .section-title {
    margin: 0 0 12px 0;
    font-size: 14px;
    font-weight: 500;
    color: #ccc;
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
  }

  .length-options {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .length-button {
    background: #333;
    border: 1px solid #555;
    color: white;
    padding: 10px 12px;
    border-radius: 6px;
    cursor: pointer;
    text-align: left;
    font-size: 13px;
    font-weight: 500;
    transition: all 0.2s ease;
  }

  .length-button:hover {
    background: #444;
    border-color: #666;
    transform: translateY(-1px);
  }

  .length-button.selected {
    background: #0066cc;
    border-color: #0088ff;
    color: white;
    box-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);
  }

  .separator {
    height: 1px;
    background: #444;
    margin: 8px 0;
  }

  /* Column Selection */
  .column-section {
    border-top: 1px solid #444;
    padding-top: 16px;
  }

  .column-select {
    width: 100%;
    background: #333;
    border: 1px solid #555;
    color: white;
    padding: 10px 12px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .column-select:hover {
    background: #444;
    border-color: #666;
  }

  .column-select:focus {
    outline: none;
    border-color: #0088ff;
    box-shadow: 0 0 0 2px rgba(0, 136, 255, 0.2);
  }

  /* Scrollbar styling */
  .length-scroll-area::-webkit-scrollbar {
    width: 6px;
  }

  .length-scroll-area::-webkit-scrollbar-track {
    background: #333;
    border-radius: 3px;
  }

  .length-scroll-area::-webkit-scrollbar-thumb {
    background: #555;
    border-radius: 3px;
  }

  .length-scroll-area::-webkit-scrollbar-thumb:hover {
    background: #666;
  }

  /* Responsive */
  @media (max-width: 768px) {
    .sequence-card-navigation {
      padding: 12px;
      gap: 16px;
    }

    .length-scroll-area {
      max-height: 150px;
    }

    .length-button {
      padding: 8px 10px;
      font-size: 12px;
    }

    .column-select {
      padding: 8px 10px;
      font-size: 12px;
    }
  }
</style>
