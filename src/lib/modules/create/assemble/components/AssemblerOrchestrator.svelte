<!--
AssemblerOrchestrator.svelte - Main orchestrator for Guided Construct mode

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
  import { GuidedOptionGenerator } from "../services/GuidedOptionGenerator";
  import { createGuidedConstructState } from "../state/guided-construct-state.svelte";
  import ConstructPickerHeader from "../../construct/shared/components/ConstructPickerHeader.svelte";
  import SinglePropStartPositionPicker from "./SinglePropStartPositionPicker.svelte";
  import GuidedOptionViewer from "./AssemblyOptionPicker.svelte";

  const {
    onSequenceUpdate,
    onSequenceComplete,
    onHeaderTextChange,
    onGridModeChange,
    onStartPositionSet,
  } = $props<{
    onSequenceUpdate?: (sequence: PictographData[]) => void;
    onSequenceComplete?: (sequence: PictographData[]) => void;
    onHeaderTextChange?: (text: string) => void;
    onGridModeChange?: (gridMode: GridMode) => void;
    onStartPositionSet?: (startPosition: PictographData) => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;
  const optionGenerator = new GuidedOptionGenerator();

  // State
  const guidedState = createGuidedConstructState({
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

  // Header text based on phase
  const headerText = $derived.by(() => {
    if (showStartPicker) {
      return ""; // Empty - text shown in workspace tile instead
    }

    if (guidedState.currentPhase === "blue") {
      return `Blue Hand - Beat ${guidedState.currentBeatNumber}`;
    }

    if (guidedState.currentPhase === "red") {
      return `Red Hand - Beat ${guidedState.currentBeatNumber} of ${guidedState.blueSequenceLength}`;
    }

    return "Sequence Complete!";
  });

  // Notify parent of header text changes
  $effect(() => {
    const text = headerText;
    if (onHeaderTextChange) {
      onHeaderTextChange(text);
    }
  });

  // Generate options for current state
  function updateOptions() {
    if (showStartPicker || guidedState.isComplete) {
      currentOptions = [];
      return;
    }

    currentOptions = optionGenerator.generateOptions(
      guidedState.currentLocation,
      guidedState.currentHand,
      guidedState.config.gridMode,
      guidedState.config.propType
    );
  }

  // Handle starting position selection
  function handleStartPositionSelected(
    position: PictographData,
    location: GridLocation
  ) {
    console.log(
      "[AssemblerOrchestrator] Start position selected:",
      location,
      position
    );
    hapticService?.trigger("selection");

    // Update config with starting location
    guidedState.updateConfig({ startingLocation: location });

    // Notify parent to set the starting position (not as a beat, but as startingPositionBeat)
    console.log("[AssemblerOrchestrator] Sending start position to parent");
    onStartPositionSet?.(position);

    // Hide start picker and show options for next beat
    showStartPicker = false;
    updateOptions();
  }

  // Handle grid mode change
  function handleGridModeChange(newGridMode: GridMode) {
    guidedState.updateConfig({ gridMode: newGridMode });

    // Notify parent so workspace can update grid SVG
    onGridModeChange?.(newGridMode);

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

    console.log(
      "[AssemblerOrchestrator] Option selected in phase:",
      guidedState.currentPhase
    );
    isTransitioning = true;
    hapticService?.trigger("selection");

    // Add to appropriate sequence
    if (guidedState.currentPhase === "blue") {
      guidedState.addBlueBeat(option);
      console.log(
        "[AssemblerOrchestrator] Blue sequence now has",
        guidedState.blueSequence.length,
        "beats"
      );

      // Update workspace with blue-only pictograph
      const workspaceSequence = [...guidedState.blueSequence];
      console.log(
        "[AssemblerOrchestrator] Calling onSequenceUpdate with",
        workspaceSequence.length,
        "beats"
      );
      onSequenceUpdate?.(workspaceSequence);
    } else if (guidedState.currentPhase === "red") {
      guidedState.addRedBeat(option);

      // Create merged sequence up to current point
      const mergedSoFar = guidedState.blueSequence.map((blue, idx) => {
        const red = guidedState.redSequence[idx];
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
      if (guidedState.isComplete) {
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
    if (guidedState.blueSequence.length === 0) {
      console.warn("Cannot proceed to red hand - no blue beats added");
      return;
    }

    hapticService?.trigger("selection");
    guidedState.completeBlueHand();

    // Keep blue sequence visible in workspace during red hand phase
    onSequenceUpdate?.([...guidedState.blueSequence]);

    updateOptions();
  }

  // Handle sequence completion
  function handleSequenceComplete() {
    hapticService?.trigger("success");

    // Notify parent with final merged sequence
    onSequenceComplete?.(guidedState.mergedSequence as PictographData[]);

    // TODO: Trigger confetti animation
    console.log("🎉 Sequence complete!", guidedState.mergedSequence);
  }

  // Handle reset
  function handleReset() {
    hapticService?.trigger("selection");
    guidedState.reset();
    showStartPicker = true;
    currentOptions = [];
    onSequenceUpdate?.([]);
  }
</script>

<div class="guided-builder">
  <!-- Header Bar -->
  <ConstructPickerHeader
    variant="guided"
    title={headerText}
    showNextHandButton={!showStartPicker &&
      guidedState.currentPhase === "blue" &&
      guidedState.blueSequence.length > 0}
    nextHandButtonText="Build Red Hand"
    onBackClick={handleReset}
    onNextHand={handleNextHand}
    currentGridMode={guidedState.config.gridMode}
    {...showStartPicker ? { onGridModeChange: handleGridModeChange } : {}}
  />

  <!-- Content Area -->
  <div class="builder-content">
    {#if showStartPicker}
      <!-- Start Position Picker -->
      <SinglePropStartPositionPicker
        onPositionSelected={handleStartPositionSelected}
        onGridModeChange={handleGridModeChange}
        currentGridMode={guidedState.config.gridMode}
        handColor={MotionColor.BLUE}
        showInlineGridToggle={false}
      />
    {:else if guidedState.isComplete}
      <!-- Completion Screen -->
      <div class="completion-screen">
        <div class="completion-icon">
          <i class="fas fa-check-circle"></i>
        </div>
        <h2 class="completion-title">Sequence Complete!</h2>
        <p class="completion-text">
          You built a {guidedState.blueSequenceLength}-beat sequence
        </p>
        <button class="completion-button" onclick={handleReset}>
          Build Another
        </button>
      </div>
    {:else}
      <!-- Option Viewer (Blue or Red phase) -->
      <GuidedOptionViewer
        options={currentOptions}
        onOptionSelected={handleOptionSelected}
        visibleHand={guidedState.currentHand}
        {isTransitioning}
      />
    {/if}
  </div>
</div>

<style>
  .guided-builder {
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
