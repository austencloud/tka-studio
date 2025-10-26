<!-- MainAdjustmentPanel.svelte - Switches between orientation and turn controls -->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { BeatData } from "../../workbench";
  import OrientationControlPanel from "./OrientationControlPanel.svelte";
  import TurnControlPanel from "./TurnControlPanel.svelte";
  import TurnEditModal from "./TurnEditModal.svelte";

  let hapticService: IHapticFeedbackService;

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
  let showTurnModal = $state(false);

  // Component references
  let orientationControlPanel = $state<OrientationControlPanel>();
  let turnControlPanel = $state<TurnControlPanel>();

  // Set beat data (called from parent)
  export function setBeatData(beatIndex: number, beatData: BeatData | null) {
    currentBeatIndex = beatIndex;
    currentBeatData = beatData;

    // Determine which panel to show
    // Start position has beatNumber === 0, regular beats have beatNumber >= 1
    if (beatData && beatData.beatNumber === 0) {
      // Show orientation picker for start position (beatNumber 0)
      activePanel = "orientation";
    } else if (beatData && beatData.beatNumber >= 1) {
      // Show turn controls for regular beats (beatNumber 1, 2, 3, etc.)
      activePanel = "turn";
    } else {
      // Fallback for no data - show orientation picker
      activePanel = "orientation";
    }

    console.log(
      `MainAdjustmentPanel: Set beat data for beat ${beatIndex}, beatNumber ${beatData?.beatNumber}, showing ${activePanel} panel`
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
    if (activePanel === "orientation" && orientationControlPanel) {
      return orientationControlPanel.getSelectedArrow();
    }
    return null;
  }

  // Modal handlers
  function handleEditTurnsRequested() {
    showTurnModal = true;
  }

  function handleCloseTurnModal() {
    showTurnModal = false;
  }

  function handleTurnModalAmountChanged(color: string, turnAmount: number) {
    console.log(`Turn amount changed via modal: ${color} = ${turnAmount}`);
    // Update through the parent's handler
    onTurnAmountChanged(color, turnAmount);
    showTurnModal = false;
  }

  // Reactive updates
  $effect(() => {
    if (selectedBeatIndex !== null) {
      setBeatData(selectedBeatIndex, selectedBeatData);
    } else if (selectedBeatData && selectedBeatData.beatNumber === 0) {
      // Handle start position selection (selectedBeatIndex is null but we have start position data)
      setBeatData(-1, selectedBeatData); // Use -1 as a special index for start position
    }
  });

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
    console.log("MainAdjustmentPanel mounted");
  });
</script>

<div class="main-adjustment-panel" data-testid="main-adjustment-panel">


  <div class="panel-content">
    {#if activePanel === "orientation"}
      <OrientationControlPanel
        bind:this={orientationControlPanel}
        {currentBeatData}
        {onOrientationChanged}
      />
    {:else if activePanel === "turn"}
      <TurnControlPanel
        {currentBeatData}
        {onTurnAmountChanged}
        onEditTurnsRequested={handleEditTurnsRequested}
      />
    {:else}
      <div class="no-controls">
        <p>No controls available</p>
      </div>
    {/if}
  </div>
</div>

<!-- Turn Edit Modal - Desktop App Pattern -->
<TurnEditModal
  isOpen={showTurnModal}
  {currentBeatData}
  onClose={handleCloseTurnModal}
  onTurnAmountChanged={handleTurnModalAmountChanged}
/>

<style>
  .main-adjustment-panel {
    display: flex;
    flex-direction: column;
    height: 100%;
    /* Smooth height transition when panels expand/collapse */
    transition: height var(--transition-normal);
  }

  .panel-content {
    flex: 1;
    overflow: auto;
    min-height: 0;
    /* Smooth height transition for content changes */
    transition: height var(--transition-normal);
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
    /* Mobile responsive styles can be added here if needed */
  }
</style>
