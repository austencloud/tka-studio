<!--
HandpathBuilder.svelte - Main orchestrator for gestural path building

Coordinates state, services, and UI components for touch-based sequence construction.
Provides setup wizard, drawing interface, and conversion to MotionData.
-->
<script lang="ts">
  import {
    GridLocation,
    GridMode,
    HandMotionType,
    PropType,
    resolve,
    TYPES,
  } from "$shared";
  import { onMount } from "svelte";
  import { fade } from "svelte/transition";
  import type {
    IHandPathDirectionDetector,
    IPathToMotionConverter,
  } from "../services/contracts";
  import { createGesturalPathState, type GesturalPathState } from "../state";
  import PathControlPanel from "./PathControlPanel.svelte";
  import SequenceLengthPicker from "./SequenceLengthPicker.svelte";
  import TouchableGrid from "./TouchableGrid.svelte";

  // Props
  let {
    onSequenceComplete,
    onCancel,
  }: {
    onSequenceComplete?: (motions: { blue: any[]; red: any[] }) => void;
    onCancel?: () => void;
  } = $props();

  // Services
  let handPathDirectionDetector = $state<IHandPathDirectionDetector | null>(
    null
  );
  let pathToMotionConverter = $state<IPathToMotionConverter | null>(null);

  // State
  const pathState: GesturalPathState = createGesturalPathState();

  // Simple state - no wizard needed
  let sequenceLength = $state(16);
  let gridMode = $state<GridMode>(GridMode.DIAMOND);
  let isStarted = $state(false);

  // Computed contextual header based on state
  let contextualHeader = $derived(() => {
    if (!isStarted) return "Set Your Settings";
    if (pathState.isSessionComplete) return "Sequence Complete!";
    if (pathState.currentHand === "blue") return "Draw Blue Hand";
    if (pathState.currentHand === "red") return "Draw Red Hand";
    return "Draw Hand Paths";
  });

  // Initialize services
  onMount(() => {
    handPathDirectionDetector = resolve<IHandPathDirectionDetector>(
      TYPES.IHandPathDirectionDetector
    );
    pathToMotionConverter = resolve<IPathToMotionConverter>(
      TYPES.IPathToMotionConverter
    );
  });

  // Start or restart drawing
  function startDrawing(): void {
    // Default starting location based on grid mode
    const startLocation =
      gridMode === GridMode.DIAMOND
        ? GridLocation.NORTH
        : GridLocation.NORTHEAST;
    pathState.initializeSession(sequenceLength, gridMode, startLocation);
    isStarted = true;
  }

  // Handle segment complete
  function handleSegmentComplete(start: GridLocation, end: GridLocation): void {
    if (!handPathDirectionDetector || !pathState.config) return;

    const handMotionType = handPathDirectionDetector.getHandMotionType(
      start,
      end,
      pathState.config.gridMode
    );

    pathState.recordSegment(start, end, handMotionType);

    // Auto-complete hand if all beats drawn
    if (pathState.isCurrentHandComplete) {
      pathState.completeCurrentHand();
    }
  }

  // Handle advance button press
  function handleAdvancePressed(): void {
    pathState.pressAdvanceButton();
  }

  // Handle advance button release
  function handleAdvanceReleased(): void {
    pathState.releaseAdvanceButton();
  }

  // Handle hand complete
  function handleHandComplete(): void {
    pathState.completeCurrentHand();
  }

  // Handle restart - reset and go back to settings
  function handleRestart(): void {
    pathState.reset();
    isStarted = false;
  }

  // Handle finish
  function handleFinish(): void {
    if (!pathToMotionConverter || !pathState.selectedRotationDirection) {
      alert("Please select a rotation direction before finishing.");
      return;
    }

    const blueMotions = pathState.blueHandPath
      ? pathToMotionConverter.convertHandPathToMotions(
          pathState.blueHandPath,
          pathState.selectedRotationDirection,
          PropType.HAND
        )
      : [];

    const redMotions = pathState.redHandPath
      ? pathToMotionConverter.convertHandPathToMotions(
          pathState.redHandPath,
          pathState.selectedRotationDirection,
          PropType.HAND
        )
      : [];

    onSequenceComplete?.({ blue: blueMotions, red: redMotions });
  }
</script>

<div class="handpath-builder" data-testid="handpath-builder">
  {#if !isStarted}
    <!-- Initial setup view -->
    <div class="setup-container" in:fade={{ duration: 200 }}>
      <h2 class="title">{contextualHeader()}</h2>
      <p class="subtitle">Choose your sequence length and grid mode</p>

      <SequenceLengthPicker bind:sequenceLength bind:gridMode />

      <button class="start-btn" onclick={startDrawing}>
        <i class="fas fa-play"></i>
        Start Drawing
      </button>

      {#if onCancel}
        <button class="cancel-btn" onclick={onCancel}>
          <i class="fas fa-times"></i>
          Cancel
        </button>
      {/if}
    </div>
  {:else}
    <!-- Drawing interface with inline settings -->
    <div class="drawing-container" in:fade={{ duration: 200 }}>
      <!-- Header with inline settings and restart -->
      <div class="drawing-header">
        <div class="header-row">
          <h2 class="title">{contextualHeader()}</h2>
          <button
            class="restart-btn"
            onclick={handleRestart}
            title="Change settings"
            aria-label="Change settings and restart drawing"
          >
            <i class="fas fa-cog"></i>
          </button>
        </div>
        <SequenceLengthPicker bind:sequenceLength bind:gridMode />
      </div>

      <!-- Drawing workspace -->
      <div class="drawing-workspace">
        <TouchableGrid
          {pathState}
          gridMode={pathState.config?.gridMode || GridMode.DIAMOND}
          onSegmentComplete={handleSegmentComplete}
          onAdvancePressed={handleAdvancePressed}
          onAdvanceReleased={handleAdvanceReleased}
        />

        <PathControlPanel
          {pathState}
          onComplete={handleHandComplete}
          onReset={handleRestart}
        />
      </div>

      <!-- Finish button when complete -->
      {#if pathState.isSessionComplete}
        <div class="complete-actions" in:fade={{ duration: 200 }}>
          <button class="action-btn primary" onclick={handleFinish}>
            <i class="fas fa-check"></i>
            Finish & Import
          </button>
          <button
            class="action-btn secondary"
            onclick={() => pathState.backToBlueHand()}
          >
            <i class="fas fa-redo"></i>
            Redraw Blue Hand
          </button>
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .handpath-builder {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
    padding: clamp(0.75rem, 2vh, 1.5rem);
    overflow-y: auto;
    overflow-x: hidden;
    box-sizing: border-box;
  }

  .setup-container,
  .drawing-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 100%;
    max-width: 1000px;
    margin: auto;
  }

  .title {
    font-size: clamp(1.25rem, 4vw, 1.75rem);
    font-weight: 700;
    color: white;
    text-align: center;
    margin: 0;
    line-height: 1.2;
  }

  .subtitle {
    font-size: clamp(0.875rem, 2.5vw, 1rem);
    color: rgba(255, 255, 255, 0.7);
    text-align: center;
    margin: 0;
    line-height: 1.4;
  }

  .drawing-header {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .restart-btn {
    width: 44px;
    height: 44px;
    padding: 0;
    background: linear-gradient(
      135deg,
      rgba(168, 85, 247, 0.15),
      rgba(147, 51, 234, 0.15)
    );
    border: 2px solid rgba(168, 85, 247, 0.3);
    border-radius: 50%;
    color: #c084fc;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .restart-btn:hover {
    background: linear-gradient(
      135deg,
      rgba(168, 85, 247, 0.25),
      rgba(147, 51, 234, 0.25)
    );
    border-color: #a855f7;
    color: #e9d5ff;
    transform: scale(1.05);
  }

  .restart-btn:active {
    transform: scale(0.95);
  }

  .restart-btn i {
    font-size: 1.1rem;
  }

  .drawing-workspace {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.5rem;
    align-items: start;
  }

  /* Tablet and up: Side-by-side layout when there's room */
  @media (min-width: 768px) {
    .drawing-workspace {
      grid-template-columns: 1fr minmax(300px, 380px);
      gap: 2rem;
    }
  }

  /* Large screens: More spacing */
  @media (min-width: 1024px) {
    .drawing-workspace {
      grid-template-columns: 1fr 400px;
      gap: 2.5rem;
    }
  }

  .start-btn {
    padding: 1rem;
    background: linear-gradient(135deg, #10b981, #059669);
    border: none;
    border-radius: 14px;
    color: white;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    min-height: 48px;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
  }

  .start-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(16, 185, 129, 0.4);
  }

  .start-btn:active {
    transform: translateY(-1px);
  }

  .start-btn i {
    font-size: 1.1rem;
  }

  .complete-actions {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    max-width: 500px;
    margin: 0 auto;
    width: 100%;
  }

  @media (min-width: 500px) {
    .complete-actions {
      flex-direction: row;
    }
  }

  .action-btn {
    flex: 1;
    padding: 0.875rem 1rem;
    border-radius: 14px;
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    min-height: 48px;
  }

  .action-btn.primary {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    border: none;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
  }

  .action-btn.primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
  }

  .action-btn.primary:active {
    transform: translateY(-1px);
  }

  .action-btn.secondary {
    background: rgba(255, 255, 255, 0.08);
    border: 2px solid rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.9);
  }

  .action-btn.secondary:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.35);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(255, 255, 255, 0.1);
  }

  .action-btn.secondary:active {
    transform: translateY(0);
  }

  .cancel-btn {
    padding: 0.75rem 1rem;
    background: rgba(239, 68, 68, 0.12);
    border: 2px solid rgba(239, 68, 68, 0.35);
    border-radius: 14px;
    color: #f87171;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    min-height: 44px;
    font-size: 0.9rem;
  }

  .cancel-btn:hover {
    background: rgba(239, 68, 68, 0.2);
    border-color: #ef4444;
    color: #fca5a5;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.25);
  }

  .cancel-btn:active {
    transform: translateY(0);
  }

  /* Small screens: Compact spacing */
  @media (max-width: 375px) {
    .handpath-builder {
      padding: 0.75rem;
    }

    .drawing-workspace {
      gap: 1rem;
    }
  }
</style>
