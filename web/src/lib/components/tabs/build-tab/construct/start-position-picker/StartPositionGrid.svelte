<!-- StartPositionGrid.svelte - Display grid of start position options -->
<script lang="ts">
  import { getLetterBorderColorSafe, type PictographData } from "$domain";
  import Pictograph from "$lib/components/core/pictograph/Pictograph.svelte";

  // Props
  const {
    startPositions = [],
    selectedPosition = null,
    isLoading = false,
    onPositionSelected = () => {},
  } = $props<{
    startPositions: PictographData[];
    selectedPosition: PictographData | null;
    isLoading: boolean;
    onPositionSelected: (position: PictographData) => void;
  }>();

  /**
   * Handle position selection
   */
  function handlePositionClick(position: PictographData) {
    if (isLoading) return; // Prevent selection during loading

    console.log("🎯 StartPositionGrid: Position selected", position.letter);
    onPositionSelected(position);
  }

  /**
   * Check if a position is currently selected
   */
  function isSelected(position: PictographData): boolean {
    return selectedPosition?.letter === position.letter;
  }

  /**
   * Get the border color for a position based on its letter
   */
  function getBorderColor(position: PictographData): string {
    return getLetterBorderColorSafe(position.letter);
  }
</script>

<!-- Loading state -->
{#if isLoading}
  <div class="loading-state">
    <div class="loading-spinner"></div>
    <p>Loading start positions...</p>
  </div>
{:else if startPositions.length === 0}
  <!-- Empty state -->
  <div class="empty-state">
    <p>No start positions available</p>
  </div>
{:else}
  <!-- Position grid -->
  <div class="positions-grid">
    {#each startPositions as position (position.letter)}
      <div
        class="position-item"
        class:selected={isSelected(position)}
        style="border-color: {getBorderColor(position)}"
        onclick={() => handlePositionClick(position)}
        role="button"
        tabindex="0"
        onkeydown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            handlePositionClick(position);
          }
        }}
      >
        <!-- Position pictograph -->
        <div class="pictograph-container">
          <Pictograph pictographData={position} />
        </div>

        <!-- Position label -->
        <div class="position-label">
          {position.letter || "Unknown"}
        </div>

        <!-- Selection indicator -->
        {#if isSelected(position)}
          <div class="selection-indicator">✓</div>
        {/if}
      </div>
    {/each}
  </div>
{/if}

<style>
  .loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px;
    color: #666;
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid #f3f3f3;
    border-top: 3px solid #007acc;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 16px;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  .empty-state {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px;
    color: #666;
    font-style: italic;
  }

  .positions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 16px;
    padding: 20px;
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
  }

  .position-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 12px;
    border: 2px solid transparent;
    border-radius: 8px;
    background: white;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .position-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  }

  .position-item:focus {
    outline: none;
    box-shadow: 0 0 0 2px #007acc;
  }

  .position-item.selected {
    border-width: 3px;
    background: #f0f8ff;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 122, 204, 0.3);
  }

  .pictograph-container {
    width: 80px;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 8px;
  }

  .position-label {
    font-size: 14px;
    font-weight: 600;
    color: #333;
    text-align: center;
  }

  .selection-indicator {
    position: absolute;
    top: 4px;
    right: 4px;
    background: #007acc;
    color: white;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: bold;
  }

  /* Responsive design */
  @media (max-width: 600px) {
    .positions-grid {
      grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
      gap: 12px;
      padding: 16px;
    }

    .position-item {
      padding: 8px;
    }

    .pictograph-container {
      width: 60px;
      height: 60px;
    }

    .position-label {
      font-size: 12px;
    }
  }
</style>
