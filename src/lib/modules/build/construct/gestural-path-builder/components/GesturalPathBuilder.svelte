<!--
GesturalPathBuilder.svelte - Main orchestrator for gestural path building

Coordinates state, services, and UI components for touch-based sequence construction.
Provides setup wizard, drawing interface, and conversion to MotionData.
-->
<script lang="ts">
  import { GridLocation, GridMode, HandMotionType, PropType, resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import { fade } from "svelte/transition";
  import type { IHandPathDirectionDetector, IPathToMotionConverter } from "../services/contracts";
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
  let handPathDirectionDetector = $state<IHandPathDirectionDetector | null>(null);
  let pathToMotionConverter = $state<IPathToMotionConverter | null>(null);

  // State
  const pathState: GesturalPathState = createGesturalPathState();

  // Wizard state
  const WizardStep = {
    SETUP: "setup",
    DRAWING: "drawing",
    COMPLETE: "complete",
  } as const;
  type WizardStep = typeof WizardStep[keyof typeof WizardStep];
  let currentStep = $state<WizardStep>(WizardStep.SETUP);

  // Initialize services
  onMount(() => {
    handPathDirectionDetector = resolve<IHandPathDirectionDetector>(TYPES.IHandPathDirectionDetector);
    pathToMotionConverter = resolve<IPathToMotionConverter>(TYPES.IPathToMotionConverter);
  });

  // Handle setup complete
  function handleSetupComplete(
    sequenceLength: number,
    gridMode: GridMode,
    startingLocation: GridLocation
  ): void {
    pathState.initializeSession(sequenceLength, gridMode, startingLocation);
    currentStep = WizardStep.DRAWING;
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

    // Check if session complete
    if (pathState.isSessionComplete) {
      currentStep = WizardStep.COMPLETE;
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

    // Check if both hands complete
    if (pathState.isSessionComplete) {
      currentStep = WizardStep.COMPLETE;
    }
  }

  // Handle reset
  function handleReset(): void {
    pathState.reset();
    currentStep = WizardStep.SETUP;
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

<div class="gestural-path-builder" data-testid="gestural-path-builder">
  {#if currentStep === WizardStep.SETUP}
    <div class="wizard-step" in:fade={{ duration: 250 }}>
      <h2 class="step-title">Setup Your Sequence</h2>
      <SequenceLengthPicker onComplete={handleSetupComplete} />
      {#if onCancel}
        <button class="cancel-btn" onclick={onCancel}>
          <i class="fas fa-times"></i>
          Cancel
        </button>
      {/if}
    </div>
  {:else if currentStep === WizardStep.DRAWING}
    <div class="drawing-step" in:fade={{ duration: 250 }}>
      <div class="drawing-header">
        <h2 class="step-title">Draw Your Hand Path</h2>
        <p class="step-subtitle">
          Swipe to draw each beat. Hold and release for static motions.
        </p>
      </div>

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
          onReset={handleReset}
        />
      </div>
    </div>
  {:else if currentStep === WizardStep.COMPLETE}
    <div class="complete-step" in:fade={{ duration: 250 }}>
      <div class="complete-icon">
        <i class="fas fa-check-circle"></i>
      </div>
      <h2 class="step-title">Sequence Complete!</h2>
      <p class="step-subtitle">
        Review your hand paths and select a rotation direction.
      </p>

      <div class="complete-actions">
        <button class="action-btn primary" onclick={handleFinish}>
          <i class="fas fa-check"></i>
          Finish & Import
        </button>
        <button class="action-btn secondary" onclick={() => pathState.backToBlueHand()}>
          <i class="fas fa-redo"></i>
          Redraw Blue Hand
        </button>
        <button class="action-btn secondary" onclick={handleReset}>
          <i class="fas fa-times"></i>
          Start Over
        </button>
      </div>
    </div>
  {/if}
</div>

<style>
  .gestural-path-builder {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 2rem;
    overflow-y: auto;
  }

  .wizard-step,
  .drawing-step,
  .complete-step {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;
  }

  .step-title {
    font-size: 2rem;
    font-weight: 700;
    color: white;
    text-align: center;
    margin: 0;
  }

  .step-subtitle {
    font-size: 1.1rem;
    color: rgba(255, 255, 255, 0.7);
    text-align: center;
    margin: 0;
  }

  .drawing-header {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .drawing-workspace {
    display: grid;
    grid-template-columns: 1fr 400px;
    gap: 2rem;
    align-items: start;
  }

  @media (max-width: 1024px) {
    .drawing-workspace {
      grid-template-columns: 1fr;
    }
  }

  .complete-icon {
    font-size: 5rem;
    color: #10b981;
    text-align: center;
  }

  .complete-actions {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-width: 400px;
    margin: 0 auto;
    width: 100%;
  }

  .action-btn {
    padding: 1rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
  }

  .action-btn.primary {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    border: none;
  }

  .action-btn.primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
  }

  .action-btn.secondary {
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.8);
  }

  .action-btn.secondary:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.3);
    color: white;
  }

  .cancel-btn {
    padding: 0.875rem;
    background: rgba(239, 68, 68, 0.1);
    border: 2px solid rgba(239, 68, 68, 0.3);
    border-radius: 8px;
    color: #ef4444;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }

  .cancel-btn:hover {
    background: rgba(239, 68, 68, 0.2);
    border-color: #ef4444;
  }
</style>
