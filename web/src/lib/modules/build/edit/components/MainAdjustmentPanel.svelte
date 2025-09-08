<!-- MainAdjustmentPanel.svelte - Switches between orientation and turn controls -->
<script lang="ts">
  import { onMount } from "svelte";
  import DualOrientationPicker from "./DualOrientationPicker.svelte";
  import TurnAdjustmentControls from "./TurnAdjustmentControls.svelte";
  import type { BeatData } from "../../workbench";

  // Props
  const {
    selectedBeatIndex,
    selectedBeatData,
    onOrientationChanged,
    onTurnAmountChanged,
  } = $props<{
    selectedBeatIndex: number | null;
    selectedBeatData: BeatData | null;
    onOrientationChanged: (color: string, orientation: string) => void;
    onTurnAmountChanged: (color: string, turnAmount: number) => void;
  }>();

  // Component state
  let currentBeatIndex = $state<number | null>(null);
  let currentBeatData = $state<BeatData | null>(null);
  let activePanel = $state<"orientation" | "turn">("orientation");

  // Component references
  let orientationPicker = $state<DualOrientationPicker>();
  let turnControls = $state<TurnAdjustmentControls>();

  // Set beat data (called from parent)
  export function setBeatData(beatIndex: number, beatData: BeatData | null) {
    currentBeatIndex = beatIndex;
    currentBeatData = beatData;

    // Determine which panel to show
    if (beatIndex === 0 || !beatData) {
      // Show orientation picker for start position (beat 0) or when no data
      activePanel = "orientation";
    } else {
      // Show turn controls for regular beats
      activePanel = "turn";
    }

    console.log(
      `MainAdjustmentPanel: Set beat data for beat ${beatIndex}, showing ${activePanel} panel`
    );
  }

  // Handle orientation changes from DualOrientationPicker
  function handleOrientationChange(data: {
    color: string;
    orientation: string;
  }) {
    onOrientationChanged(data.color, data.orientation);
  }

  // Handle turn amount changes from TurnAdjustmentControls
  function handleTurnAmountChange(data: { color: string; turnAmount: number }) {
    onTurnAmountChanged(data.color, data.turnAmount);
  }

  // Get currently selected arrow info
  export function getSelectedArrow(): string | null {
    if (activePanel === "orientation" && orientationPicker) {
      return orientationPicker.getSelectedArrow();
    } else if (activePanel === "turn" && turnControls) {
      return turnControls.getSelectedArrow();
    }
    return null;
  }

  // Reactive updates
  $effect(() => {
    if (selectedBeatIndex !== null) {
      setBeatData(selectedBeatIndex, selectedBeatData);
    }
  });

  onMount(() => {
    console.log("MainAdjustmentPanel mounted");
  });
</script>

<div class="main-adjustment-panel" data-testid="main-adjustment-panel">
  <div class="panel-header">
    <h3>
      {#if activePanel === "orientation"}
        Start Position Controls
      {:else}
        Turn Adjustment Controls
      {/if}
    </h3>
    <div class="panel-indicator">
      {#if currentBeatIndex !== null}
        <span class="beat-info">Beat {currentBeatIndex + 1}</span>
      {/if}
      <span class="panel-type"
        >{activePanel === "orientation" ? "Orientation" : "Turns"}</span
      >
    </div>
  </div>

  <div class="panel-content">
    {#if activePanel === "orientation"}
      <DualOrientationPicker
        bind:this={orientationPicker}
        {currentBeatData}
        onorientationchanged={handleOrientationChange}
      />
    {:else if activePanel === "turn"}
      <TurnAdjustmentControls
        bind:this={turnControls}
        {currentBeatData}
        onturnamountchanged={handleTurnAmountChange}
      />
    {:else}
      <div class="no-controls">
        <p>No controls available</p>
      </div>
    {/if}
  </div>
</div>

<style>
  .main-adjustment-panel {
    display: flex;
    flex-direction: column;
    height: 100%;
    background: rgba(255, 255, 255, 0.05);
    border-radius: var(--border-radius);
    overflow: hidden;
  }

  .panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-md);
    background: rgba(255, 255, 255, 0.1);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .panel-header h3 {
    margin: 0;
    color: var(--foreground);
    font-size: var(--font-size-lg);
    font-weight: 600;
  }

  .panel-indicator {
    display: flex;
    gap: var(--spacing-sm);
    align-items: center;
  }

  .beat-info {
    padding: var(--spacing-xs) var(--spacing-sm);
    background: var(--primary);
    color: var(--primary-foreground);
    border-radius: var(--border-radius-sm);
    font-size: var(--font-size-sm);
    font-weight: 500;
  }

  .panel-type {
    padding: var(--spacing-xs) var(--spacing-sm);
    background: var(--muted);
    color: var(--muted-foreground);
    border-radius: var(--border-radius-sm);
    font-size: var(--font-size-sm);
    font-weight: 500;
    text-transform: capitalize;
  }

  .panel-content {
    flex: 1;
    overflow: auto;
    padding: var(--spacing-md);
    min-height: 0;
  }

  .no-controls {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: var(--muted-foreground);
  }

  .no-controls p {
    margin: 0;
    font-size: var(--font-size-md);
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .panel-header {
      flex-direction: column;
      gap: var(--spacing-sm);
      align-items: flex-start;
    }

    .panel-indicator {
      align-self: flex-end;
    }

    .panel-content {
      padding: var(--spacing-sm);
    }
  }
</style>
