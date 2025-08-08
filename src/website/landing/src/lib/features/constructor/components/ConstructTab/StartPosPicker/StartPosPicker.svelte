<!--
🎯 ENHANCED START POSITION PICKER

A working enhanced start position picker that shows actual pictographs using the existing Pictograph component.
Uses existing TKA constructor infrastructure and pictograph rendering system.

Based on legacy v1-legacy implementation patterns.
-->

<script lang="ts">
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  import type { PictographData } from '@tka/domain';
  import Pictograph from '../../Pictograph/Pictograph.svelte';

  // ============================================================================
  // COMPONENT STATE
  // ============================================================================

  let startPositionPictographs: PictographData[] = [];
  let filteredDataAvailable = false;
  let isLoading = true;
  let loadingError = false;

  // ============================================================================
  // DATA GENERATION
  // ============================================================================

  // Create start position data directly instead of relying on data store
  function createStartPositionData(positionType: 'alpha' | 'beta' | 'gamma'): PictographData {
    // Real TKA data from data_modern/datasets/pictographs/diamond_pictograph_dataframe.csv
    // and data_modern/core/positions_maps.py
    console.log(`🔧 Creating start position data for: ${positionType}`);

    const positionConfigs = {
      alpha: {
        letter: 'α' as any,
        startPos: 'alpha1' as any,
        endPos: 'alpha1' as any,
        // From positions_map: (SOUTH, NORTH): ALPHA1
        blueStart: { loc: 's' as any, ori: 'in' as any },
        redStart: { loc: 'n' as any, ori: 'in' as any }
      },
      beta: {
        letter: 'β' as any,
        startPos: 'beta5' as any,
        endPos: 'beta5' as any,
        // From positions_map: (SOUTH, SOUTH): BETA5 - FIXED DATA
        blueStart: { loc: 's' as any, ori: 'in' as any },
        redStart: { loc: 's' as any, ori: 'in' as any }
      },
      gamma: {
        letter: 'Γ' as any,
        startPos: 'gamma11' as any,
        endPos: 'gamma11' as any,
        // From positions_map: (SOUTH, EAST): GAMMA11 - FIXED DATA
        blueStart: { loc: 's' as any, ori: 'in' as any },
        redStart: { loc: 'e' as any, ori: 'in' as any }
      }
    };

    const config = positionConfigs[positionType];

    return {
      letter: config.letter,
      startPos: config.startPos,
      endPos: config.endPos,
      timing: null,
      direction: null,
      gridMode: 'diamond' as any,
      gridData: null,
      blueMotionData: {
        motionType: 'static' as any,
        startLoc: config.blueStart.loc,
        endLoc: config.blueStart.loc,
        startOri: config.blueStart.ori,
        endOri: config.blueStart.ori,
        propRotDir: 'no_rot' as any,
        turns: 0
      },
      redMotionData: {
        motionType: 'static' as any,
        startLoc: config.redStart.loc,
        endLoc: config.redStart.loc,
        startOri: config.redStart.ori,
        endOri: config.redStart.ori,
        propRotDir: 'no_rot' as any,
        turns: 0
      },
      redPropData: null,
      bluePropData: null,
      redArrowData: null,
      blueArrowData: null,
      grid: 'diamond',
      isStartPosition: true
    };
  }



  // ============================================================================
  // POSITION CALCULATION FUNCTIONS
  // ============================================================================



  // ============================================================================
  // LIFECYCLE HOOKS
  // ============================================================================

  onMount(() => {
    console.log('🎯 StartPosPicker: Initializing with real TKA data...');

    try {
      // Generate start position data directly
      const positions = [
        createStartPositionData('alpha'),
        createStartPositionData('beta'),
        createStartPositionData('gamma')
      ];

      console.log('✅ StartPosPicker: Start positions created:', positions);

      startPositionPictographs = positions;
      filteredDataAvailable = positions.length > 0;
      isLoading = false;
    } catch (err) {
      console.error('❌ StartPosPicker: Error:', err);
      loadingError = true;
      isLoading = false;
    }
  });

  // ============================================================================
  // EVENT HANDLERS
  // ============================================================================

  function safeCopyPictographData(data: PictographData): PictographData {
    const safeCopy: PictographData = {
      letter: data.letter,
      startPos: data.startPos,
      endPos: data.endPos,
      timing: data.timing,
      direction: data.direction,
      gridMode: data.gridMode,
      grid: data.grid,

      redMotionData: data.redMotionData
        ? {
            motionType: data.redMotionData.motionType,
            startLoc: data.redMotionData.startLoc,
            endLoc: data.redMotionData.endLoc,
            startOri: data.redMotionData.startOri,
            endOri: data.redMotionData.endOri,
            propRotDir: data.redMotionData.propRotDir,
            turns: data.redMotionData.turns
          }
        : null,

      blueMotionData: data.blueMotionData
        ? {
            motionType: data.blueMotionData.motionType,
            startLoc: data.blueMotionData.startLoc,
            endLoc: data.blueMotionData.endLoc,
            startOri: data.blueMotionData.startOri,
            endOri: data.blueMotionData.endOri,
            propRotDir: data.blueMotionData.propRotDir,
            turns: data.blueMotionData.turns
          }
        : null,

      redPropData: null,
      bluePropData: null,
      redArrowData: null,
      blueArrowData: null,
      gridData: null
    };

    return safeCopy;
  }

  const handleSelect = async (startPosPictograph: PictographData) => {
    try {
      console.log('🎯 StartPosPicker: Position selected:', startPosPictograph);

      // Create a copy for the start position
      const startPosCopy = safeCopyPictographData(startPosPictograph);
      startPosCopy.isStartPosition = true;

      // Ensure motion data is static for start positions
      if (startPosCopy.redMotionData) {
        startPosCopy.redMotionData.motionType = 'static';
        startPosCopy.redMotionData.endLoc = startPosCopy.redMotionData.startLoc;
        startPosCopy.redMotionData.endOri = startPosCopy.redMotionData.startOri;
        startPosCopy.redMotionData.turns = 0;
      }

      if (startPosCopy.blueMotionData) {
        startPosCopy.blueMotionData.motionType = 'static';
        startPosCopy.blueMotionData.endLoc = startPosCopy.blueMotionData.startLoc;
        startPosCopy.blueMotionData.endOri = startPosCopy.blueMotionData.startOri;
        startPosCopy.blueMotionData.turns = 0;
      }

      // Save to localStorage
      try {
        localStorage.setItem('start_position', JSON.stringify(startPosCopy));
      } catch (error) {
        console.error('Failed to save start position to localStorage:', error);
      }

      // Dispatch event for parent components
      if (browser) {
        const customEvent = new CustomEvent('start-position-selected', {
          detail: {
            startPosition: startPosCopy,
            isTransitioning: true
          },
          bubbles: true
        });

        document.dispatchEvent(customEvent);
        console.log('✅ StartPosPicker: Event dispatched');
      }
    } catch (error) {
      console.error('Error adding start position:', error);
    }
  };
</script>

<div class="enhanced-start-pos-picker">
  <div class="instruction-text">Choose your start position</div>

  {#if isLoading}
    <div class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">Loading Start Positions...</p>
    </div>
  {:else if loadingError}
    <div class="error-container">
      <p>Unable to load start positions. Please try refreshing the page.</p>
      <button
        onclick={() => {
          if (browser) window.location.reload();
        }}>Refresh</button
      >
    </div>
  {:else if !filteredDataAvailable}
    <div class="error-container">
      <p>No valid start positions found for the current configuration.</p>
    </div>
  {:else}
    <div class="pictograph-row">
      {#each startPositionPictographs as pictograph (pictograph.letter + '_' + pictograph.startPos + '_' + pictograph.endPos)}
        <div
          class="pictograph-container enhanced"
          role="button"
          tabindex="0"
          onclick={() => {
            handleSelect(pictograph);
          }}
          onkeydown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              handleSelect(pictograph);
            }
          }}
        >
          <!-- Use existing Pictograph component for proper rendering -->
          <Pictograph
            pictographData={pictograph}
            showLoadingIndicator={false}
            debug={false}
            size={200}
          />

        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .enhanced-start-pos-picker {
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

  .loading-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
    flex: 1;
  }

  .loading-text {
    margin-top: 20px;
    font-size: 1.2rem;
    color: #555;
    animation: pulse 1.5s infinite ease-in-out;
  }

  @keyframes pulse {
    0% {
      opacity: 0.6;
    }
    50% {
      opacity: 1;
    }
    100% {
      opacity: 0.6;
    }
  }

  .error-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
    background-color: rgba(255, 220, 220, 0.7);
    padding: 20px;
    border-radius: 10px;
    flex: 1;
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
    transition: all 0.3s ease-in-out;
    border-radius: 12px;
    overflow: hidden;
  }

  .pictograph-container.enhanced {
    background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
    border: 2px solid rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
  }

  .pictograph-container:hover {
    transform: scale(1.05) translateY(-5px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.2);
    border-color: rgba(255,255,255,0.4);
  }



  /* Pictograph container adjustments for proper rendering */
  .pictograph-container.enhanced {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .instruction-text {
    font-size: 1.1rem;
    color: #374151;
    margin-bottom: 20px;
    text-align: center;
    font-weight: 500;
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #e5e7eb;
    border-top: 4px solid #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>
