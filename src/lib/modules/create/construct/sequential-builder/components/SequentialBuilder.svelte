<!--
SequentialBuilder.svelte - Main orchestrator for Guided Construct mode

Flow:
1. Start Position Picker (4 positions + grid toggle)
2. Blue Hand Phase (select from 6 options, builds in workspace)
3. "Next Hand" button → transition to Red Hand Phase
4. Red Hand Phase (select from 6 options, overlays on workspace)
5. Completion → Confetti animation

Integrates with workspace for real-time updates
-->
<script lang="ts">
  import {
    GridLocation,
    GridMode,
    MotionColor,
    PropType,
    type IHapticFeedbackService,
    type PictographData,
  } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import { SequentialOptionGenerator } from "../services/SequentialOptionGenerator";
  import { createSequentialConstructState } from "../state/sequential-construct-state.svelte";
  import ConstructPickerHeader from "../../shared/components/ConstructPickerHeader.svelte";
  import SinglePropStartPositionPicker from "./SinglePropStartPositionPicker.svelte";
  import SequentialOptionViewer from "./SequentialOptionViewer.svelte";

  const { onSequenceUpdate, onSequenceComplete, onHeaderTextChange } = $props<{
    onSequenceUpdate?: (sequence: PictographData[]) => void;
    onSequenceComplete?: (sequence: PictographData[]) => void;
    onHeaderTextChange?: (text: string) => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;
  const optionGenerator = new SequentialOptionGenerator();

  // State
  const sequentialState = createSequentialConstructState({
    startingLocation: GridLocation.NORTH,
    gridMode: GridMode.DIAMOND,
    propType: PropType.HAND,
  });

  let showStartPicker = $state(true);
  let currentOptions = $state<PictographData[]>([]);
  let isTransitioning = $state(false);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Notify parent of header text changes
  $effect(() => {
    const text = headerText();
    if (onHeaderTextChange) {
      onHeaderTextChange(text);
    }
  });

  // Header text based on phase
  const headerText = $derived(() => {
    if (showStartPicker) {
      return "Choose Starting Position";
    }

    if (sequentialState.currentPhase === "blue") {
      return `Blue Hand - Beat ${sequentialState.currentBeatNumber}`;
    }

    if (sequentialState.currentPhase === "red") {
      return `Red Hand - Beat ${sequentialState.currentBeatNumber} of ${sequentialState.blueSequenceLength}`;
    }

    return "Sequence Complete!";
  });

  // Generate options for current state
  function updateOptions() {
    if (showStartPicker || sequentialState.isComplete) {
      currentOptions = [];
      return;
    }

    currentOptions = optionGenerator.generateOptions(
      sequentialState.currentLocation,
      sequentialState.currentHand,
      sequentialState.config.gridMode,
      sequentialState.config.propType
    );
  }

  // Handle starting position selection
  function handleStartPositionSelected(
    _position: PictographData,
    location: GridLocation
  ) {
    sequentialState.updateConfig({ startingLocation: location });
    showStartPicker = false;
    updateOptions();
  }

  // Handle grid mode change
  function handleGridModeChange(newGridMode: GridMode) {
    sequentialState.updateConfig({ gridMode: newGridMode });

    // If we haven't started building yet, just update
    if (showStartPicker) {
      return;
    }

    // If we're mid-build, regenerate options
    updateOptions();
  }

  // Handle option selection
  async function handleOptionSelected(option: PictographData) {
    if (isTransitioning) return;

    isTransitioning = true;
    hapticService?.trigger("selection");

    // Add to appropriate sequence
    if (sequentialState.currentPhase === "blue") {
      sequentialState.addBlueBeat(option);

      // Update workspace with blue-only pictograph
      const workspaceSequence = [...sequentialState.blueSequence];
      onSequenceUpdate?.(workspaceSequence);
    } else if (sequentialState.currentPhase === "red") {
      sequentialState.addRedBeat(option);

      // Create merged sequence up to current point
      const mergedSoFar = sequentialState.blueSequence.map((blue, idx) => {
        const red = sequentialState.redSequence[idx];
        if (red) {
          // Merge blue + red
          return {
            id: crypto.randomUUID(),
            motions: {
              blue: blue.motions.blue,
              red: red.motions.red,
            },
          } as PictographData;
        } else {
          // Still only blue (for beats not yet complete)
          return blue;
        }
      });

      onSequenceUpdate?.(mergedSoFar);

      // Check if complete
      if (sequentialState.isComplete) {
        handleSequenceComplete();
        return;
      }
    }

    // Brief delay for transition smoothness
    await new Promise((resolve) => setTimeout(resolve, 300));

    // Generate next options
    updateOptions();
    isTransitioning = false;
  }

  // Handle "Next Hand" button
  function handleNextHand() {
    if (sequentialState.blueSequence.length === 0) {
      console.warn("Cannot proceed to red hand - no blue beats added");
      return;
    }

    hapticService?.trigger("selection");
    sequentialState.completeBlueHand();
    updateOptions();
  }

  // Handle sequence completion
  function handleSequenceComplete() {
    hapticService?.trigger("success");

    // Notify parent with final merged sequence
    onSequenceComplete?.(sequentialState.mergedSequence as PictographData[]);

    // TODO: Trigger confetti animation
    console.log("🎉 Sequence complete!", sequentialState.mergedSequence);
  }

  // Handle reset
  function handleReset() {
    hapticService?.trigger("selection");
    sequentialState.reset();
    showStartPicker = true;
    currentOptions = [];
    onSequenceUpdate?.([]);
  }
</script>

<div class="sequential-builder">
  <!-- Header Bar -->
  <ConstructPickerHeader
    variant="sequential"
    title={headerText()}
    showNextHandButton={!showStartPicker &&
      sequentialState.currentPhase === "blue" &&
      sequentialState.blueSequence.length > 0}
    nextHandButtonText="Build Red Hand"
    onBackClick={handleReset}
    onNextHand={handleNextHand}
    currentGridMode={sequentialState.config.gridMode}
    {...showStartPicker ? { onGridModeChange: handleGridModeChange } : {}}
  />

  <!-- Content Area -->
  <div class="builder-content">
    {#if showStartPicker}
      <!-- Start Position Picker -->
      <SinglePropStartPositionPicker
        onPositionSelected={handleStartPositionSelected}
        onGridModeChange={handleGridModeChange}
        currentGridMode={sequentialState.config.gridMode}
        handColor={MotionColor.BLUE}
        showInlineGridToggle={false}
      />
    {:else if sequentialState.isComplete}
      <!-- Completion Screen -->
      <div class="completion-screen">
        <div class="completion-icon">
          <i class="fas fa-check-circle"></i>
        </div>
        <h2 class="completion-title">Sequence Complete!</h2>
        <p class="completion-text">
          You built a {sequentialState.blueSequenceLength}-beat sequence
        </p>
        <button class="completion-button" onclick={handleReset}>
          Build Another
        </button>
      </div>
    {:else}
      <!-- Option Viewer (Blue or Red phase) -->
      <SequentialOptionViewer
        options={currentOptions}
        onOptionSelected={handleOptionSelected}
        visibleHand={sequentialState.currentHand}
        {isTransitioning}
      />
    {/if}
  </div>
</div>

<style>
  .sequential-builder {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    background: linear-gradient(
      180deg,
      rgba(15, 23, 42, 0.95) 0%,
      rgba(30, 41, 59, 0.98) 100%
    );
  }

  /* Content */
  .builder-content {
    flex: 1;
    overflow: hidden;
    position: relative;
  }

  /* Completion Screen */
  .completion-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    gap: 1.5rem;
    padding: 2rem;
  }

  .completion-icon {
    font-size: 4rem;
    color: #10b981;
    animation: scaleIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  .completion-title {
    font-size: 2rem;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
  }

  .completion-text {
    font-size: 1.1rem;
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
  }

  .completion-button {
    padding: 1rem 2rem;
    background: linear-gradient(135deg, #10b981, #059669);
    border: none;
    border-radius: 12px;
    color: white;
    font-weight: 600;
    font-size: 1.1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
  }

  .completion-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
  }

  /* Animations */
  @keyframes scaleIn {
    0% {
      transform: scale(0);
      opacity: 0;
    }
    60% {
      transform: scale(1.1);
      opacity: 1;
    }
    100% {
      transform: scale(1);
    }
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .completion-icon {
      font-size: 3rem;
    }

    .completion-title {
      font-size: 1.5rem;
    }
  }
</style>
