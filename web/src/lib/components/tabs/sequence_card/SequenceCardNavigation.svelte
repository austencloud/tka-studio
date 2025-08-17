<!-- SequenceCardNavigation.svelte - Enhanced navigation with page layout controls -->
<script lang="ts">
  interface Props {
    selectedLength?: number;
    columnCount?: number;
    layoutMode?: "grid" | "list" | "printable";
    paperSize?: string;
    orientation?: string;
    showMargins?: boolean;
    onlengthselected?: (length: number) => void;
    oncolumncountchanged?: (count: number) => void;
    onviewmodechanged?: (mode: "grid" | "list" | "printable") => void;
    onpapersizechanged?: (size: string) => void;
    onorientationchanged?: (orientation: string) => void;
    onshowmarginschanged?: (show: boolean) => void;
  }

  let {
    selectedLength = 16,
    columnCount = 2,
    layoutMode = "grid",
    paperSize = "A4",
    orientation = "Portrait",
    showMargins = false,
    onlengthselected,
    oncolumncountchanged,
    onviewmodechanged,
    onpapersizechanged,
    onorientationchanged,
    onshowmarginschanged,
  }: Props = $props();

  // Length options matching desktop app exactly
  const lengthOptions = [
    { value: 0, label: "All" },
    { value: 2, label: "2" },
    { value: 3, label: "3" },
    { value: 4, label: "4" },
    { value: 5, label: "5" },
    { value: 6, label: "6" },
    { value: 8, label: "8" },
    { value: 10, label: "10" },
    { value: 12, label: "12" },
    { value: 16, label: "16" },
  ];

  // Column count options (for grid/list modes)
  const columnOptions = [1, 2, 3, 4, 5, 6];

  // View mode options
  const viewModeOptions = [
    { value: "grid", label: "📊 Grid", description: "Card grid view" },
    { value: "list", label: "📄 List", description: "Single column list" },
    { value: "printable", label: "🖨️ Pages", description: "Printable pages" },
  ];

  // Paper size options
  const paperSizeOptions = [
    { value: "A4", label: "A4", description: "210mm × 297mm" },
    { value: "Letter", label: "Letter", description: '8.5" × 11"' },
    { value: "Legal", label: "Legal", description: '8.5" × 14"' },
    { value: "Tabloid", label: "Tabloid", description: '11" × 17"' },
  ];

  // Orientation options
  const orientationOptions = [
    { value: "Portrait", label: "📄 Portrait" },
    { value: "Landscape", label: "📃 Landscape" },
  ];

  // Check if printable mode is active
  let isPrintableMode = $derived(layoutMode === "printable");

  function handleLengthClick(length: number) {
    onlengthselected?.(length);
  }

  function handleColumnChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    const newCount = parseInt(target.value);
    oncolumncountchanged?.(newCount);
  }

  function handleViewModeChange(mode: "grid" | "list" | "printable") {
    onviewmodechanged?.(mode);
  }

  function handlePaperSizeChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    onpapersizechanged?.(target.value);
  }

  function handleOrientationChange(orientation: string) {
    onorientationchanged?.(orientation);
  }

  function handleShowMarginsChange(event: Event) {
    const target = event.target as HTMLInputElement;
    onshowmarginschanged?.(target.checked);
  }
</script>

<div class="sequence-card-navigation">
  <!-- Sidebar Header -->
  <div class="sidebar-header">
    <h2 class="header-title">Sequence Cards</h2>
    <p class="header-subtitle">Configure layout and display</p>
  </div>

  <!-- View Mode Selection -->
  <div class="view-mode-section">
    <h3 class="section-title">View Mode</h3>
    <div class="view-mode-buttons">
      {#each viewModeOptions as option (option.value)}
        <button
          class="view-mode-button"
          class:selected={layoutMode === option.value}
          onclick={() => handleViewModeChange(option.value as any)}
          title={option.description}
        >
          <span class="view-mode-label">{option.label}</span>
        </button>
      {/each}
    </div>
  </div>

  <!-- Sequence Length Selection -->
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
        {/each}
      </div>
    </div>
  </div>

  <!-- Layout Controls -->
  {#if !isPrintableMode}
    <!-- Grid/List Mode Controls -->
    <div class="layout-controls">
      <h3 class="section-title">Layout</h3>
      <div class="column-selector">
        <label class="control-label" for="column-select">
          {layoutMode === "list" ? "List Columns:" : "Grid Columns:"}
        </label>
        <select
          id="column-select"
          class="control-select"
          bind:value={columnCount}
          onchange={handleColumnChange}
        >
          {#each columnOptions as count}
            <option value={count}>{count}</option>
          {/each}
        </select>
      </div>
    </div>
  {:else}
    <!-- Printable Mode Controls -->
    <div class="printable-controls">
      <h3 class="section-title">Page Setup</h3>

      <!-- Paper Size -->
      <div class="control-group">
        <label class="control-label" for="paper-size-select">Paper Size:</label>
        <select
          id="paper-size-select"
          class="control-select"
          bind:value={paperSize}
          onchange={handlePaperSizeChange}
        >
          {#each paperSizeOptions as option}
            <option value={option.value} title={option.description}>
              {option.label}
            </option>
          {/each}
        </select>
      </div>

      <!-- Orientation -->
      <div class="control-group">
        <span class="control-label">Orientation:</span>
        <div class="orientation-buttons" role="group" aria-label="Orientation">
          {#each orientationOptions as option (option.value)}
            <button
              class="orientation-button"
              class:selected={orientation === option.value}
              onclick={() => handleOrientationChange(option.value)}
              title={option.value}
            >
              {option.label}
            </button>
          {/each}
        </div>
      </div>

      <!-- Page Options -->
      <div class="control-group">
        <span class="control-label">Page Options:</span>
        <div class="page-options">
          <label class="checkbox-control">
            <input
              type="checkbox"
              checked={showMargins}
              onchange={handleShowMarginsChange}
            />
            <span class="checkbox-label">Show Margins</span>
          </label>
        </div>
      </div>
    </div>
  {/if}

  <!-- Status Information -->
  <div class="status-section">
    <div class="status-item">
      <span class="status-label">Mode:</span>
      <span class="status-value">{layoutMode}</span>
    </div>
    {#if isPrintableMode}
      <div class="status-item">
        <span class="status-label">Paper:</span>
        <span class="status-value">{paperSize} {orientation}</span>
      </div>
    {:else}
      <div class="status-item">
        <span class="status-label">Columns:</span>
        <span class="status-value">{columnCount}</span>
      </div>
    {/if}
  </div>
</div>

<style>
  .sequence-card-navigation {
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    border-radius: 16px;
    border: var(--glass-border);
    box-shadow: var(--shadow-glass);
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    height: 100%;
    overflow-y: auto;
  }

  /* Section Headers */
  .sidebar-header {
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    border-radius: 12px;
    border: var(--glass-border);
    box-shadow: var(--shadow-glass);
    padding: 16px;
    text-align: center;
  }

  .header-title {
    margin: 0 0 4px 0;
    color: rgba(255, 255, 255, 0.95);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
    font-size: 18px;
    font-weight: bold;
    letter-spacing: 0.5px;
  }

  .header-subtitle {
    margin: 0;
    color: rgba(255, 255, 255, 0.8);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    font-size: 14px;
    font-style: italic;
  }

  .section-title {
    margin: 0 0 8px 0;
    color: rgba(255, 255, 255, 0.9);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.3px;
    text-transform: uppercase;
  }

  /* View Mode Section */
  .view-mode-section {
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    border-radius: 12px;
    border: var(--glass-border);
    box-shadow: var(--shadow-glass);
    padding: 12px;
  }

  .view-mode-buttons {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .view-mode-button {
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-radius: 8px;
    padding: 10px 12px;
    color: rgba(255, 255, 255, 0.9);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    font-weight: 500;
    font-size: 13px;
    text-align: left;
    cursor: pointer;
    transition: all var(--transition-fast);
    box-shadow: var(--shadow-glass);
  }

  .view-mode-button:hover {
    background: var(--surface-hover);
    border: var(--glass-border-hover);
    transform: translateY(-1px);
    box-shadow: var(--shadow-glass-hover);
  }

  .view-mode-button.selected {
    background: var(--gradient-primary);
    border: 1px solid rgba(99, 102, 241, 0.6);
    color: white;
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4);
  }

  .view-mode-label {
    display: block;
  }

  /* Length Section */
  .length-section {
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    border-radius: 12px;
    border: var(--glass-border);
    box-shadow: var(--shadow-glass);
    padding: 12px;
    flex: 1;
    min-height: 0;
  }

  .length-scroll-area {
    max-height: 200px;
    overflow-y: auto;
  }

  .length-options {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .length-button {
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-radius: 8px;
    padding: 8px 12px;
    color: rgba(255, 255, 255, 0.9);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    font-weight: 500;
    font-size: 14px;
    text-align: center;
    cursor: pointer;
    transition: all var(--transition-fast);
    box-shadow: var(--shadow-glass);
  }

  .length-button:hover {
    background: var(--surface-hover);
    border: var(--glass-border-hover);
    transform: translateY(-1px);
    box-shadow: var(--shadow-glass-hover);
  }

  .length-button.selected {
    background: var(--gradient-primary);
    border: 1px solid rgba(99, 102, 241, 0.6);
    color: white;
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4);
  }

  /* Layout Controls */
  .layout-controls,
  .printable-controls {
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    border-radius: 12px;
    border: var(--glass-border);
    box-shadow: var(--shadow-glass);
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .control-group,
  .column-selector {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .control-label {
    color: rgba(255, 255, 255, 0.9);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    font-weight: 500;
    font-size: 12px;
    margin: 0;
  }

  .control-select {
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-radius: 6px;
    padding: 6px 10px;
    color: rgba(255, 255, 255, 0.9);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    font-size: 12px;
    min-height: 32px;
    cursor: pointer;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23ffffff' viewBox='0 0 16 16'%3E%3Cpath d='M4 6l4 4 4-4'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 6px center;
    background-size: 12px;
    padding-right: 24px;
    box-shadow: var(--shadow-glass);
  }

  .control-select:hover {
    background: var(--surface-hover);
    border: var(--glass-border-hover);
    box-shadow: var(--shadow-glass-hover);
  }

  .control-select:focus {
    outline: none;
    border-color: rgba(99, 102, 241, 0.6);
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.3);
  }

  /* Orientation Buttons */
  .orientation-buttons {
    display: flex;
    gap: 4px;
  }

  .orientation-button {
    flex: 1;
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-radius: 6px;
    padding: 6px 8px;
    color: rgba(255, 255, 255, 0.9);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    font-weight: 500;
    font-size: 11px;
    text-align: center;
    cursor: pointer;
    transition: all var(--transition-fast);
    box-shadow: var(--shadow-glass);
  }

  .orientation-button:hover {
    background: var(--surface-hover);
    border: var(--glass-border-hover);
    box-shadow: var(--shadow-glass-hover);
  }

  .orientation-button.selected {
    background: var(--gradient-primary);
    border: 1px solid rgba(99, 102, 241, 0.6);
    color: white;
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4);
  }

  /* Page Options */
  .page-options {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .checkbox-control {
    display: flex;
    align-items: center;
    gap: 6px;
    cursor: pointer;
  }

  .checkbox-control input[type="checkbox"] {
    width: 14px;
    height: 14px;
    accent-color: #6366f1;
  }

  .checkbox-label {
    color: rgba(255, 255, 255, 0.9);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    font-size: 12px;
    font-weight: 500;
  }

  /* Status Section */
  .status-section {
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    border-radius: 12px;
    border: var(--glass-border);
    box-shadow: var(--shadow-glass);
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    flex-shrink: 0;
  }

  .status-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .status-label {
    color: rgba(255, 255, 255, 0.7);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    font-size: 11px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }

  .status-value {
    color: rgba(255, 255, 255, 0.95);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
    font-size: 12px;
    font-weight: 600;
  }

  /* Scrollbar Styling */
  .length-scroll-area::-webkit-scrollbar,
  .sequence-card-navigation::-webkit-scrollbar {
    width: 6px;
  }

  .length-scroll-area::-webkit-scrollbar-track,
  .sequence-card-navigation::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 3px;
  }

  .length-scroll-area::-webkit-scrollbar-thumb,
  .sequence-card-navigation::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 3px;
  }

  .length-scroll-area::-webkit-scrollbar-thumb:hover,
  .sequence-card-navigation::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.5);
  }

  /* Responsive Design */
  @media (max-width: 1024px) {
    .sequence-card-navigation {
      height: auto;
      max-height: 300px;
    }

    .length-scroll-area {
      max-height: 120px;
    }

    .view-mode-buttons {
      flex-direction: row;
    }

    .view-mode-button {
      flex: 1;
      text-align: center;
    }
  }

  @media (max-width: 768px) {
    .sequence-card-navigation {
      gap: 12px;
      padding: 10px;
    }

    .header-title {
      font-size: 16px;
    }

    .header-subtitle {
      font-size: 12px;
    }

    .view-mode-button,
    .length-button {
      font-size: 12px;
      padding: 6px 8px;
    }

    .orientation-buttons {
      flex-direction: column;
    }

    .orientation-button {
      flex: none;
    }
  }
</style>
