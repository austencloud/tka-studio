<!-- DetailedInfoPanel.svelte - Detailed information about selected beat -->
<script lang="ts">
  import { GridMode, MotionColor } from "$lib/domain/enums";
  import { resolve } from "$lib/services/bootstrap";
  import type { IGridModeDeriver } from "$lib/services/interfaces/movement/IGridModeDeriver";
  import type {
    BeatData,
    SequenceData,
  } from "$services/interfaces/domain-types";
  import { onMount } from "svelte";

  // Props
  const { selectedBeatIndex, selectedBeatData, currentSequence } = $props<{
    selectedBeatIndex: number | null;
    selectedBeatData: BeatData | null;
    currentSequence: SequenceData | null;
  }>();

  // Component state
  let displayBeatIndex = $state<number | null>(null);
  let displayBeatData = $state<BeatData | null>(null);

  // Update info display
  export function updateInfo(beatIndex: number, beatData: BeatData | null) {
    displayBeatIndex = beatIndex;
    displayBeatData = beatData;
    console.log(`DetailedInfoPanel: Updated info for beat ${beatIndex}`);
  }

  // Reactive state derived from props
  $effect(() => {
    displayBeatIndex = selectedBeatIndex;
    displayBeatData = selectedBeatData;
  });

  // Format timing information
  function formatTiming(beat: number): string {
    return `Beat ${beat + 1}`;
  }

  // Get motion info from pictograph data
  function getMotionInfo(beatData: BeatData | null) {
    if (!beatData?.pictographData) return null;

    const motions = [];
    const pictograph = beatData.pictographData;

    // Extract motion information from pictograph
    if (pictograph.motions?.blue?.motionType) {
      motions.push({
        color: MotionColor.BLUE,
        type: pictograph.motions.blue.motionType,
        direction: pictograph.motions.blue.rotationDirection || "Unknown",
      });
    }

    if (pictograph.motions?.red?.motionType) {
      motions.push({
        color: MotionColor.RED,
        type: pictograph.motions.red.motionType,
        direction: pictograph.motions.red.rotationDirection || "Unknown",
      });
    }

    return motions;
  }

  // Get position info
  function getPositionInfo(beatData: BeatData | null) {
    if (!beatData?.pictographData) return null;

    const pictographData = beatData.pictographData;

    // Compute gridMode from motion data
    const gridModeService = resolve<IGridModeDeriver>("IGridModeDeriver");
    const gridMode =
      pictographData.motions?.blue && pictographData.motions?.red
        ? gridModeService.deriveGridMode(
            pictographData.motions.blue,
            pictographData.motions.red
          )
        : GridMode.DIAMOND;

    return {
      gridMode,
      blueStart: pictographData.motions?.blue?.startLocation || "Unknown",
      redStart: pictographData.motions?.red?.startLocation || "Unknown",
    };
  }

  onMount(() => {
    console.log("DetailedInfoPanel mounted");
  });
</script>

<div class="detailed-info-panel" data-testid="detailed-info-panel">
  <div class="info-header">
    <h3>Beat Information</h3>
  </div>

  <div class="info-content">
    {#if displayBeatIndex !== null && displayBeatData}
      <!-- Beat timing info -->
      <div class="info-section">
        <h4>Timing</h4>
        <div class="info-row">
          <span class="label">Beat Number:</span>
          <span class="value">{formatTiming(displayBeatIndex)}</span>
        </div>
        {#if currentSequence}
          <div class="info-row">
            <span class="label">Sequence:</span>
            <span class="value">{currentSequence.name}</span>
          </div>
        {/if}
      </div>

      <!-- Position information -->
      {#if getPositionInfo(displayBeatData)}
        {@const posInfo = getPositionInfo(displayBeatData)}
        <div class="info-section">
          <h4>Positions</h4>
          <div class="info-row">
            <span class="label">Grid Mode:</span>
            <span class="value mode-value">{posInfo?.gridMode}</span>
          </div>
          <div class="info-row">
            <span class="label">Blue Start:</span>
            <span class="value blue-value">{posInfo?.blueStart}</span>
          </div>
          <div class="info-row">
            <span class="label">Red Start:</span>
            <span class="value red-value">{posInfo?.redStart}</span>
          </div>
        </div>
      {/if}

      <!-- Motion information -->
      {#if getMotionInfo(displayBeatData)}
        {@const motions = getMotionInfo(displayBeatData)}
        <div class="info-section">
          <h4>Motions</h4>
          {#each motions || [] as motion}
            <div class="motion-info">
              <div class="motion-header">
                <span
                  class="motion-color"
                  class:blue={motion.color === MotionColor.BLUE}
                  class:red={motion.color === MotionColor.RED}
                >
                  {motion.color}
                </span>
              </div>
              <div class="info-row">
                <span class="label">Type:</span>
                <span class="value">{motion.type}</span>
              </div>
              <div class="info-row">
                <span class="label">Direction:</span>
                <span class="value">{motion.direction}</span>
              </div>
            </div>
          {/each}
        </div>
      {/if}
    {:else}
      <div class="no-info">
        <div class="placeholder-icon">ℹ️</div>
        <p>Select a beat to view detailed information</p>
      </div>
    {/if}
  </div>
</div>

<style>
  .detailed-info-panel {
    display: flex;
    flex-direction: column;
    height: 100%;
    background: rgba(255, 255, 255, 0.05);
    border-radius: var(--border-radius);
    overflow: hidden;
  }

  .info-header {
    display: flex;
    align-items: center;
    padding: var(--spacing-md);
    background: rgba(255, 255, 255, 0.1);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .info-header h3 {
    margin: 0;
    color: var(--foreground);
    font-size: var(--font-size-md);
    font-weight: 600;
  }

  .info-content {
    flex: 1;
    overflow: auto;
    padding: var(--spacing-md);
  }

  .info-section {
    margin-bottom: var(--spacing-lg);
    padding: var(--spacing-md);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius);
  }

  .info-section h4 {
    margin: 0 0 var(--spacing-md) 0;
    color: var(--foreground);
    font-size: var(--font-size-sm);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-sm);
    padding: var(--spacing-xs) 0;
  }

  .info-row:last-child {
    margin-bottom: 0;
  }

  .label {
    color: var(--muted-foreground);
    font-size: var(--font-size-sm);
    font-weight: 500;
  }

  .value {
    color: var(--foreground);
    font-size: var(--font-size-sm);
    font-weight: 600;
    padding: var(--spacing-xs) var(--spacing-sm);
    background: rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-sm);
  }

  .mode-value {
    text-transform: capitalize;
  }

  .blue-value {
    background: rgba(59, 130, 246, 0.2);
    color: rgb(59, 130, 246);
  }

  .red-value {
    background: rgba(239, 68, 68, 0.2);
    color: rgb(239, 68, 68);
  }

  .motion-info {
    margin-bottom: var(--spacing-md);
    padding: var(--spacing-sm);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-sm);
  }

  .motion-info:last-child {
    margin-bottom: 0;
  }

  .motion-header {
    margin-bottom: var(--spacing-sm);
  }

  .motion-color {
    display: inline-block;
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: var(--border-radius-sm);
    font-size: var(--font-size-sm);
    font-weight: 600;
    text-transform: uppercase;
  }

  .motion-color.blue {
    background: rgba(59, 130, 246, 0.2);
    color: rgb(59, 130, 246);
    border: 1px solid rgba(59, 130, 246, 0.3);
  }

  .motion-color.red {
    background: rgba(239, 68, 68, 0.2);
    color: rgb(239, 68, 68);
    border: 1px solid rgba(239, 68, 68, 0.3);
  }

  .no-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    text-align: center;
    color: var(--muted-foreground);
    gap: var(--spacing-md);
  }

  .placeholder-icon {
    font-size: 2rem;
    opacity: 0.5;
  }

  .no-info p {
    margin: 0;
    font-size: var(--font-size-md);
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .info-content {
      padding: var(--spacing-sm);
    }

    .info-section {
      padding: var(--spacing-sm);
    }

    .info-row {
      flex-direction: column;
      align-items: flex-start;
      gap: var(--spacing-xs);
    }

    .value {
      align-self: flex-end;
    }
  }
</style>
