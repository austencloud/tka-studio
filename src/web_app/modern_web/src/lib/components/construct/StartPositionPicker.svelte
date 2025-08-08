<!-- StartPositionPicker.svelte - Modern implementation based on legacy component -->
<script lang="ts">
  import { onMount } from 'svelte';
  import type { PictographData, BeatData } from '$services/interfaces';
  import { IStartPositionService, IPictographRenderingService } from '$services/interfaces';
  import { resolve } from '$services/bootstrap';
  import ModernPictograph from '../pictograph/ModernPictograph.svelte';
  
  // Props using runes
  const { 
    gridMode = 'diamond', 
    onStartPositionSelected = () => {} 
  } = $props<{ 
    gridMode?: 'diamond' | 'box';
    onStartPositionSelected?: (position: BeatData) => void;
  }>();
  
  // Runes-based reactive state (replacing legacy stores)
  let startPositionPictographs = $state<PictographData[]>([]);
  let selectedStartPos = $state<PictographData | null>(null);
  let isLoading = $state(true);
  let loadingError = $state(false);
  let isTransitioning = $state(false);
  
  // Modern services (replacing legacy service calls)
  let startPositionService = $state<any | null>(null);
  let pictographRenderingService = $state<any | null>(null);

  // Resolve services when container is ready
  $effect(() => {
    try {
      // Try to resolve services, but handle gracefully if container not ready
      if (!startPositionService) {
        try {
          startPositionService = resolve('IStartPositionService');
        } catch (containerError) {
          // Container not ready yet, will retry on next effect run
          return;
        }
      }
      if (!pictographRenderingService) {
        try {
          pictographRenderingService = resolve('IPictographRenderingService');
        } catch (containerError) {
          // Container not ready yet, will retry on next effect run
          return;
        }
      }
    } catch (error) {
      console.error('StartPositionPicker: Failed to resolve services:', error);
      // Services will remain null and component will handle gracefully
    }
  });

  // Load available start positions (modernized from legacy)
  async function loadStartPositions() {
    isLoading = true;
    loadingError = false;
    
    try {
      console.log(`🎯 Loading start positions for ${gridMode} mode`);
      
      // Use modern service to get start positions
      if (!startPositionService) {
        throw new Error('StartPositionService not available');
      }
      const startPositions = await startPositionService.getDefaultStartPositions(gridMode);
      startPositionPictographs = startPositions;
      
      console.log(`✅ Loaded ${startPositionPictographs.length} start positions`);
      
    } catch (error) {
      console.error('❌ Error loading start positions:', error);
      loadingError = true;
      startPositionPictographs = [];
    } finally {
      isLoading = false;
    }
  }
  
  // Handle start position selection (modernized from legacy)
  async function handleSelect(startPosPictograph: PictographData) {
    try {
      console.log('🎯 Start position selected:', startPosPictograph.id);
      
      // Show transition state
      isTransitioning = true;
      
      // Create start position beat data 
      const startPositionBeat: BeatData = {
        beat: 0,
        pictograph_data: {
          ...startPosPictograph,
          // Ensure static motion types for start positions
          motions: {
            blue: startPosPictograph.motions.blue ? {
              ...startPosPictograph.motions.blue,
              motionType: 'static',
              endLocation: startPosPictograph.motions.blue.startLocation,
              endOrientation: startPosPictograph.motions.blue.startOrientation,
              turns: 0
            } : null,
            red: startPosPictograph.motions.red ? {
              ...startPosPictograph.motions.red,
              motionType: 'static', 
              endLocation: startPosPictograph.motions.red.startLocation,
              endOrientation: startPosPictograph.motions.red.startOrientation,
              turns: 0
            } : null
          }
        }
      };
      
      // Update selected state
      selectedStartPos = startPosPictograph;
      
      // Use modern service to set start position
      if (startPositionService) {
        await startPositionService.setStartPosition(startPositionBeat);
      }
      
      // Call callback to notify parent component
      onStartPositionSelected(startPositionBeat);
      
      // Emit modern event (replacing legacy DOM events)
      const event = new CustomEvent('start-position-selected', {
        detail: { startPosition: startPositionBeat, isTransitioning: true },
        bubbles: true
      });
      document.dispatchEvent(event);
      
      console.log('✅ Start position selection completed');
      
    } catch (error) {
      console.error('❌ Error selecting start position:', error);
      isTransitioning = false;
    }
  }
  
  // Initialize on mount
  onMount(() => {
    loadStartPositions();
  });
  
  // Reload when grid mode changes
  $effect(() => {
    if (gridMode) {
      loadStartPositions();
    }
  });
</script>

<div class="start-pos-picker" data-testid="start-position-picker">
  {#if isLoading}
    <div class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">Loading Start Positions...</p>
    </div>
  {:else if loadingError}
    <div class="error-container">
      <p>Unable to load start positions. Please try refreshing the page.</p>
      <button
        class="refresh-button"
        onclick={() => {
          if (typeof window !== 'undefined') window.location.reload();
        }}
      >
        Refresh
      </button>
    </div>
  {:else if startPositionPictographs.length === 0}
    <div class="error-container">
      <p>No valid start positions found for the current configuration.</p>
    </div>
  {:else}
    <div class="pictograph-row">
      {#each startPositionPictographs as pictograph (pictograph.id)}
        <div
          class="pictograph-container"
          class:selected={selectedStartPos?.id === pictograph.id}
          role="button"
          tabindex="0"
          onclick={() => handleSelect(pictograph)}
          onkeydown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              handleSelect(pictograph);
            }
          }}
        >
                              <!-- Render pictograph using ModernPictograph component -->
          <div class="pictograph-wrapper">
            <ModernPictograph
              pictographData={pictograph}
              debug={false}
              showLoadingIndicator={false}
            />
          </div>
          
          <!-- Position label (from legacy) -->
          <div class="position-label">
            {pictograph.letter || 'Start Position'}
          </div>
        </div>
      {/each}
    </div>
  {/if}

  <!-- Loading overlay during transition (from legacy) -->
  {#if isTransitioning}
    <div class="loading-overlay">
      <div class="loading-spinner"></div>
      <p>Loading options...</p>
    </div>
  {/if}
</div>

<style>
  .start-pos-picker {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
    min-height: 300px;
    padding: 20px 0;
    position: relative;
  }

  .loading-container,
  .error-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
    flex: 1;
  }

  .error-container {
    background-color: rgba(255, 220, 220, 0.7);
    padding: 20px;
    border-radius: var(--border-radius);
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid var(--muted);
    border-top: 4px solid var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .loading-text {
    margin-top: 20px;
    font-size: 1.2rem;
    color: var(--muted-foreground);
    animation: pulse 1.5s infinite ease-in-out;
  }

  @keyframes pulse {
    0%, 100% { opacity: 0.6; }
    50% { opacity: 1; }
  }

  .refresh-button {
    margin-top: 15px;
    padding: 10px 20px;
    background: var(--primary);
    color: var(--primary-foreground);
    border: none;
    border-radius: var(--border-radius);
    cursor: pointer;
    font-size: 1rem;
  }

  .refresh-button:hover {
    background: var(--primary-hover, var(--primary));
    opacity: 0.9;
  }

  .pictograph-row {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    width: 90%;
    gap: 3%;
    margin: auto;
    flex: 0 0 auto;
    padding: 2rem 0;
  }

  .pictograph-container {
    width: 25%;
    aspect-ratio: 1 / 1;
    height: auto;
    position: relative;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    border: 2px solid transparent;
    border-radius: var(--border-radius);
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .pictograph-container:hover {
    transform: scale(1.05);
    border-color: var(--primary);
    box-shadow: var(--shadow-lg);
  }

  .pictograph-container.selected {
    border-color: var(--primary);
    background: var(--primary)/10;
  }

  .pictograph-wrapper {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
  }

  .pictograph-svg-container {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .pictograph-svg-container :global(svg) {
    max-width: 100%;
    max-height: 100%;
    border-radius: var(--border-radius-sm);
  }

  .pictograph-loading,
  .pictograph-error {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: var(--muted-foreground);
    font-size: var(--font-size-sm);
  }

  .pictograph-error {
    color: var(--destructive);
    text-align: center;
  }

  .position-label {
    position: absolute;
    bottom: -25px;
    left: 50%;
    transform: translateX(-50%);
    font-size: var(--font-size-sm);
    font-weight: 500;
    color: var(--foreground);
    text-align: center;
    white-space: nowrap;
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
    border-radius: var(--border-radius);
    z-index: 1000;
  }

  .loading-overlay .loading-spinner {
    width: 32px;
    height: 32px;
    margin-bottom: var(--spacing-md);
  }

  .loading-overlay p {
    color: var(--foreground);
    font-size: 1.1rem;
    margin: 0;
  }

  @media (max-width: 768px) {
    .pictograph-row {
      flex-direction: column;
      gap: var(--spacing-lg);
    }

    .pictograph-container {
      width: 80%;
      max-width: 200px;
    }
  }
</style>
