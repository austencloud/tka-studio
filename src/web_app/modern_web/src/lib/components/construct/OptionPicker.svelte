<!-- OptionPicker.svelte - Modern implementation based on legacy component -->
<script lang="ts">
  import { onMount } from 'svelte';
  import type { PictographData, BeatData, SequenceData, OptionFilters, DifficultyLevel } from '$services/interfaces';
  import { IOptionDataService, IPictographRenderingService, ISequenceService } from '$services/interfaces';
  import { resolve } from '$services/bootstrap';
  
  // Props using runes
  const { 
    currentSequence = null, 
    difficulty = 'intermediate', 
    onOptionSelected = () => {} 
  } = $props<{ 
    currentSequence?: SequenceData | null;
    difficulty?: DifficultyLevel;
    onOptionSelected?: (option: PictographData) => void;
  }>();
  
  // Runes-based reactive state (replacing legacy stores)
  let availableOptions = $state<PictographData[]>([]);
  let filteredOptions = $state<PictographData[]>([]);
  let selectedOption = $state<PictographData | null>(null);
  let isLoading = $state(true);
  let loadingError = $state(false);
  let isTransitioning = $state(false);
  
  // Filter state
  let showFilters = $state(false);
  let selectedMotionTypes = $state<string[]>([]);
  let maxTurns = $state(3);
  let minTurns = $state(0);
  let localDifficulty = $state<DifficultyLevel>(difficulty);
  
  // Layout state (from legacy responsive layout)
  let containerWidth = $state(800);
  let containerHeight = $state(600);
  let optionsPerRow = $state(4);
  let optionSize = $state(150);
  
  // Modern services
  const optionDataService = resolve(IOptionDataService);
  const pictographRenderingService = resolve(IPictographRenderingService);
  const sequenceService = resolve(ISequenceService);
  
  // Load available options (modernized from legacy)
  async function loadOptions() {
    isLoading = true;
    loadingError = false;
    
    try {
      console.log('🎲 Loading options for sequence:', currentSequence?.id);
      
      if (!currentSequence) {
        console.warn('⚠️ No current sequence provided');
        availableOptions = [];
        filteredOptions = [];
        return;
      }
      
      // Build filters from state
      const filters: OptionFilters = {
        difficulty: localDifficulty,
        motionTypes: selectedMotionTypes.length > 0 ? selectedMotionTypes as any : undefined,
        minTurns: minTurns > 0 ? minTurns : undefined,
        maxTurns: maxTurns < 10 ? maxTurns : undefined
      };
      
      // Use modern service to get options
      const options = await optionDataService.getNextOptions(currentSequence, filters);
      availableOptions = options;
      filteredOptions = options;
      
      console.log(`✅ Loaded ${options.length} options`);
      
    } catch (error) {
      console.error('❌ Error loading options:', error);
      loadingError = true;
      availableOptions = [];
      filteredOptions = [];
    } finally {
      isLoading = false;
    }
  }
  
  // Apply filters to options
  function applyFilters() {
    console.log('🎯 Applying filters:', { selectedMotionTypes, minTurns, maxTurns });
    
    let filtered = [...availableOptions];
    
    // Filter by motion types
    if (selectedMotionTypes.length > 0) {
      filtered = filtered.filter(option => {
        const blueType = option.motions?.blue?.motionType;
        const redType = option.motions?.red?.motionType;
        return selectedMotionTypes.includes(blueType || '') || selectedMotionTypes.includes(redType || '');
      });
    }
    
    // Filter by turns range
    filtered = filtered.filter(option => {
      const blueTurns = typeof option.motions?.blue?.turns === 'number' ? option.motions.blue.turns : 0;
      const redTurns = typeof option.motions?.red?.turns === 'number' ? option.motions.red.turns : 0;
      const maxOptionTurns = Math.max(blueTurns, redTurns);
      
      return maxOptionTurns >= minTurns && maxOptionTurns <= maxTurns;
    });
    
    filteredOptions = filtered;
    console.log(`🎯 Filtered to ${filtered.length} options`);
  }
  
  // Handle option selection (modernized from legacy)
  async function handleSelect(option: PictographData) {
    try {
      console.log('🎲 Option selected:', option.id);
      
      // Show transition state
      isTransitioning = true;
      
      // Validate option compatibility
      if (currentSequence) {
        const validation = optionDataService.validateOptionCompatibility(option, currentSequence);
        if (!validation.isValid) {
          console.warn('⚠️ Option compatibility warnings:', validation.errors);
        }
      }
      
      // Update selected state
      selectedOption = option;
      
      // Create beat data from option
      const beatData: BeatData = {
        beat: currentSequence ? currentSequence.beats.length : 1,
        pictograph_data: option
      };
      
      // Call callback to notify parent component
      onOptionSelected(option);
      
      // Emit modern event
      const event = new CustomEvent('option-selected', {
        detail: { option, beatData },
        bubbles: true
      });
      document.dispatchEvent(event);
      
      console.log('✅ Option selection completed');
      
    } catch (error) {
      console.error('❌ Error selecting option:', error);
      isTransitioning = false;
    }
  }
  
  // Calculate responsive layout (from legacy)
  function calculateLayout() {
    // Simple responsive calculation
    const baseSize = 120;
    const minSize = 80;
    const maxSize = 200;
    
    optionsPerRow = Math.max(1, Math.floor(containerWidth / (baseSize + 20)));
    optionSize = Math.min(maxSize, Math.max(minSize, (containerWidth - (optionsPerRow * 20)) / optionsPerRow));
    
    console.log(`📐 Layout: ${optionsPerRow} per row, ${optionSize}px each`);
  }
  
  // Toggle motion type filter
  function toggleMotionType(motionType: string) {
    if (selectedMotionTypes.includes(motionType)) {
      selectedMotionTypes = selectedMotionTypes.filter(t => t !== motionType);
    } else {
      selectedMotionTypes = [...selectedMotionTypes, motionType];
    }
    applyFilters();
  }
  
  // Initialize on mount
  onMount(() => {
    calculateLayout();
    if (currentSequence) {
      loadOptions();
    }
    
    // Listen for window resize
    const handleResize = () => {
      containerWidth = window.innerWidth * 0.8;
      containerHeight = window.innerHeight * 0.6;
      calculateLayout();
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  });
  
  // Reload when sequence or filters change
  $effect(() => {
    if (currentSequence) {
      loadOptions();
    }
  });
  
  // Recalculate layout when dimensions change
  $effect(() => {
    calculateLayout();
  });
</script>

<div class="option-picker">
  <!-- Header with filters -->
  <div class="option-picker-header">
    <div class="header-content">
      <h2>Choose Next Move</h2>
      <div class="header-controls">
        <button
          class="filter-toggle"
          class:active={showFilters}
          onclick={() => showFilters = !showFilters}
        >
          🎛️ Filters
        </button>
        <div class="difficulty-selector">
          <select bind:value={localDifficulty} onchange={() => loadOptions()}>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>
      </div>
    </div>
    
    <!-- Expandable filters panel -->
    {#if showFilters}
      <div class="filters-panel">
        <div class="filter-group">
          <label>Motion Types:</label>
          <div class="motion-type-filters">
            {#each ['pro', 'anti', 'float', 'dash', 'static'] as motionType}
              <button
                class="motion-type-filter"
                class:active={selectedMotionTypes.includes(motionType)}
                onclick={() => toggleMotionType(motionType)}
              >
                {motionType.toUpperCase()}
              </button>
            {/each}
          </div>
        </div>
        
        <div class="filter-group">
          <label>Turns Range:</label>
          <div class="turns-range">
            <input
              type="range"
              min="0"
              max="3"
              step="0.5"
              bind:value={minTurns}
              onchange={() => applyFilters()}
            />
            <span>{minTurns}</span>
            <span>to</span>
            <input
              type="range"
              min="0"
              max="3"
              step="0.5"
              bind:value={maxTurns}
              onchange={() => applyFilters()}
            />
            <span>{maxTurns}</span>
          </div>
        </div>
      </div>
    {/if}
  </div>

  <!-- Options display area -->
  <div class="options-container">
    {#if isLoading}
      <div class="loading-container">
        <div class="loading-spinner"></div>
        <p class="loading-text">Loading Options...</p>
      </div>
    {:else if loadingError}
      <div class="error-container">
        <p>Unable to load options. Please try again.</p>
        <button class="retry-button" onclick={() => loadOptions()}>
          Retry
        </button>
      </div>
    {:else if filteredOptions.length === 0}
      <div class="empty-container">
        <p>No options available with current filters.</p>
        <button class="clear-filters-button" onclick={() => { selectedMotionTypes = []; minTurns = 0; maxTurns = 3; applyFilters(); }}>
          Clear Filters
        </button>
      </div>
    {:else}
      <div 
        class="options-grid"
        style="grid-template-columns: repeat({optionsPerRow}, 1fr); gap: var(--spacing-md);"
      >
        {#each filteredOptions as option (option.id)}
          <div
            class="option-container"
            class:selected={selectedOption?.id === option.id}
            role="button"
            tabindex="0"
            onclick={() => handleSelect(option)}
            onkeydown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                handleSelect(option);
              }
            }}
            style="width: {optionSize}px; height: {optionSize}px;"
          >
            <!-- Render option using modern service -->
            <div class="option-wrapper">
              {#await pictographRenderingService.renderPictograph(option)}
                <div class="option-loading">Loading...</div>
              {:then svgElement}
                <div class="option-svg-container">
                  {@html svgElement.outerHTML}
                </div>
              {:catch error}
                <div class="option-error">
                  <p>Error</p>
                  <small>{error.message}</small>
                </div>
              {/await}
            </div>
            
            <!-- Option info -->
            <div class="option-info">
              <div class="option-letter">{option.letter || '?'}</div>
              <div class="option-details">
                {#if option.motions?.blue}
                  <span class="motion-tag blue">{option.motions.blue.motionType}</span>
                {/if}
                {#if option.motions?.red}
                  <span class="motion-tag red">{option.motions.red.motionType}</span>
                {/if}
              </div>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </div>

  <!-- Loading overlay during transition -->
  {#if isTransitioning}
    <div class="loading-overlay">
      <div class="loading-spinner"></div>
      <p>Adding to sequence...</p>
    </div>
  {/if}
</div>

<style>
  .option-picker {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    position: relative;
  }

  .option-picker-header {
    flex-shrink: 0;
    background: var(--background);
    border-bottom: 1px solid var(--border);
    padding: var(--spacing-md);
  }

  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-md);
  }

  .header-content h2 {
    margin: 0;
    color: var(--foreground);
    font-size: var(--font-size-xl);
  }

  .header-controls {
    display: flex;
    gap: var(--spacing-md);
    align-items: center;
  }

  .filter-toggle {
    padding: var(--spacing-sm) var(--spacing-md);
    background: var(--muted);
    border: 1px solid var(--border);
    border-radius: var(--border-radius);
    cursor: pointer;
    transition: all 0.2s;
  }

  .filter-toggle:hover,
  .filter-toggle.active {
    background: var(--primary);
    color: var(--primary-foreground);
  }

  .difficulty-selector select {
    padding: var(--spacing-sm);
    border: 1px solid var(--border);
    border-radius: var(--border-radius);
    background: var(--background);
    color: var(--foreground);
  }

  .filters-panel {
    background: var(--muted);
    padding: var(--spacing-md);
    border-radius: var(--border-radius);
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .filter-group {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
  }

  .filter-group label {
    font-weight: 500;
    color: var(--foreground);
  }

  .motion-type-filters {
    display: flex;
    gap: var(--spacing-sm);
    flex-wrap: wrap;
  }

  .motion-type-filter {
    padding: var(--spacing-xs) var(--spacing-sm);
    background: var(--background);
    border: 1px solid var(--border);
    border-radius: var(--border-radius-sm);
    cursor: pointer;
    font-size: var(--font-size-sm);
    transition: all 0.2s;
  }

  .motion-type-filter:hover,
  .motion-type-filter.active {
    background: var(--primary);
    color: var(--primary-foreground);
  }

  .turns-range {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
  }

  .turns-range input[type="range"] {
    flex: 1;
  }

  .turns-range span {
    font-size: var(--font-size-sm);
    color: var(--muted-foreground);
    min-width: 20px;
    text-align: center;
  }

  .options-container {
    flex: 1;
    overflow-y: auto;
    padding: var(--spacing-md);
  }

  .loading-container,
  .error-container,
  .empty-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: var(--muted-foreground);
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid var(--muted);
    border-top: 4px solid var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: var(--spacing-md);
  }

  .retry-button,
  .clear-filters-button {
    margin-top: var(--spacing-md);
    padding: var(--spacing-sm) var(--spacing-md);
    background: var(--primary);
    color: var(--primary-foreground);
    border: none;
    border-radius: var(--border-radius);
    cursor: pointer;
  }

  .options-grid {
    display: grid;
    gap: var(--spacing-md);
    justify-items: center;
  }

  .option-container {
    position: relative;
    cursor: pointer;
    border: 2px solid transparent;
    border-radius: var(--border-radius);
    padding: var(--spacing-xs);
    transition: all 0.2s ease;
    background: var(--background);
  }

  .option-container:hover {
    transform: translateY(-2px);
    border-color: var(--primary);
    box-shadow: var(--shadow-lg);
  }

  .option-container.selected {
    border-color: var(--primary);
    background: var(--primary)/10;
  }

  .option-wrapper {
    width: 100%;
    height: calc(100% - 30px);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .option-svg-container {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .option-svg-container :global(svg) {
    max-width: 100%;
    max-height: 100%;
  }

  .option-loading,
  .option-error {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: var(--muted-foreground);
    font-size: var(--font-size-xs);
  }

  .option-info {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-xs);
  }

  .option-letter {
    font-weight: bold;
    font-size: var(--font-size-sm);
    color: var(--foreground);
  }

  .option-details {
    display: flex;
    gap: 2px;
  }

  .motion-tag {
    padding: 1px 4px;
    border-radius: 2px;
    font-size: 8px;
    font-weight: 500;
    text-transform: uppercase;
  }

  .motion-tag.blue {
    background: #2563eb;
    color: white;
  }

  .motion-tag.red {
    background: #dc2626;
    color: white;
  }

  .loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.9);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }

  .loading-overlay .loading-spinner {
    width: 32px;
    height: 32px;
    margin-bottom: var(--spacing-md);
  }

  .loading-overlay p {
    color: var(--foreground);
    margin: 0;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>
