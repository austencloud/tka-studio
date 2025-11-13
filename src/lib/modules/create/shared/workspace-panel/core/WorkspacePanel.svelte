<!--
	WorkspacePanel.svelte

	Workspace panel containing the sequence display and action buttons.
	Main area for viewing and interacting with the sequence.
-->
<script lang="ts">
  import type { IBeatOperationsService } from "$create/shared/services/contracts";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import MultiSelectOverlay from "../components/MultiSelectOverlay.svelte";
  import SelectionToolbar from "../components/SelectionToolbar.svelte";
  import Toast from "../components/Toast.svelte";
  import SequenceDisplay from "../sequence-display/components/SequenceDisplay.svelte";
  import HandPathWorkspace from "../hand-path/HandPathWorkspace.svelte";
  import { navigationState } from "$shared";

  // Services
  let beatOperationsService: IBeatOperationsService | null = null;

  // Props
  let {
    sequenceState,
    createModuleState,
    practiceBeatIndex = null,
    animatingBeatNumber = null,

    // Multi-select props
    onBatchEdit,

    // Animation state ref (for animate tab)
    animationStateRef = null,

    // Layout mode
    isSideBySideLayout = false,
    isMobilePortrait = false,

    // Tool panel height (for slide panels)
    toolPanelHeight = 0,

    // Play animation handler
    onPlayAnimation,
  }: {
    sequenceState?: any; // TODO: Type this properly
    createModuleState?: any; // TODO: Type this properly
    practiceBeatIndex?: number | null;
    animatingBeatNumber?: number | null;

    // Multi-select props
    onBatchEdit?: () => void;

    // Animation state ref
    animationStateRef?: any | null;

    // Layout mode
    isSideBySideLayout?: boolean;
    isMobilePortrait?: boolean;

    // Tool panel height
    toolPanelHeight?: number;

    // Play animation handler
    onPlayAnimation?: () => void;
  } = $props();

  // Local beat selection state (beatNumber: 0=start, 1=first beat, etc.)
  let localSelectedBeatNumber = $state<number | null>(null);

  // Effect: Update local selection when animation is playing
  $effect(() => {
    if (animatingBeatNumber !== null) {
      localSelectedBeatNumber = animatingBeatNumber;
    }
  });

  // Effect: Sync local selection with sequenceState selection
  // This ensures UI updates when selection is cleared via edit panel close
  $effect(() => {
    if (!sequenceState) return;

    const globalSelection = sequenceState.selectedBeatNumber;
    // Only sync if animation isn't playing (animation takes precedence)
    if (animatingBeatNumber === null) {
      localSelectedBeatNumber = globalSelection;
    }
  });

  // Multi-select state - use the actual mode from selection state
  const isMultiSelectMode = $derived(sequenceState?.isMultiSelectMode ?? false);
  const selectionCount = $derived(sequenceState?.selectionCount ?? 0);
  const totalBeats = $derived(
    sequenceState?.currentSequence?.beats?.length ?? 0
  );

  // Toast message for validation errors
  let toastMessage = $state<string | null>(null);

  // Inline Animator Panel state
  let showInlineAnimator = $state(false);

  // Get current word from sequence state
  const currentWord = $derived(() => {
    return sequenceState?.sequenceWord() ?? "";
  });

  // Handle beat selection (receives beatNumber: 1, 2, 3...)
  function handleBeatSelected(beatNumber: number) {
    if (!sequenceState) return;

    // Note: Animate is no longer a Create tab, it's a separate panel
    // This check may need to be updated to check panel state instead
    const isAnimateTabActive = false; // TODO: Update this to check animate panel state

    if (isAnimateTabActive && animationStateRef) {
      // In Animate tab: Jump to this beat in the animation (needs array index)
      const arrayIndex = beatNumber - 1;
      animationStateRef.jumpToBeat(arrayIndex);
      // Still update local selection for visual feedback (using beatNumber)
      localSelectedBeatNumber = beatNumber;
      sequenceState.selectBeat(beatNumber);
    } else {
      // In other tabs: Just select the beat - the edit panel will open automatically
      localSelectedBeatNumber = beatNumber;
      sequenceState.selectBeat(beatNumber);

      // Note: We no longer switch to edit tab! The edit slide panel will open instead.
      // This is handled by an effect in CreateModule.svelte that watches for beat selection.
    }
  }

  // Handle start position selection (beatNumber 0)
  function handleStartPositionSelected() {
    if (!sequenceState) return;

    // Only proceed if there's actually a start position selected
    if (
      !sequenceState.hasStartPosition ||
      !sequenceState.selectedStartPosition
    ) {
      return;
    }

    // Select start position for editing (beatNumber 0)
    localSelectedBeatNumber = 0;
    sequenceState.selectStartPositionForEditing();

    // Note: We no longer switch to edit tab! The edit slide panel will open instead.
    // This is handled by an effect in CreateModule.svelte that watches for start position selection.
  }

  // Multi-select handlers
  function handleBeatLongPress(beatNumber: number) {
    if (!sequenceState) return;
    sequenceState.enterMultiSelectMode(beatNumber);
  }

  function handleExitMultiSelect() {
    if (!sequenceState) return;
    sequenceState.exitMultiSelectMode();
    localSelectedBeatNumber = null;
  }

  function handleMultiSelectToggle(beatNumber: number) {
    if (!sequenceState) return;
    const result = sequenceState.toggleBeatInMultiSelect(beatNumber);
    if (!result.success) {
      // Show toast error
      toastMessage = result.error ?? null;
      setTimeout(() => (toastMessage = null), 3000);
    }
  }

  function handleBatchEdit() {
    if (onBatchEdit) {
      onBatchEdit();
    }
  }

  // Handle beat deletion via keyboard
  function handleBeatDelete(beatNumber: number) {
    if (!beatOperationsService || !createModuleState) {
      console.warn("Cannot delete beat - services not initialized");
      return;
    }

    // Convert beatNumber (1, 2, 3...) to beatIndex (0, 1, 2...)
    const beatIndex = beatNumber - 1;

    try {
      beatOperationsService.removeBeat(beatIndex, createModuleState);
    } catch (err) {
      console.error("Failed to remove beat", err);
      toastMessage = "Failed to remove beat";
      setTimeout(() => (toastMessage = null), 3000);
    }
  }

  // Initialize services on mount
  onMount(() => {
    beatOperationsService = resolve<IBeatOperationsService>(
      TYPES.IBeatOperationsService
    );
  });
</script>

{#if sequenceState}
  {#if navigationState.activeTab === "gestural" && createModuleState?.handPathCoordinator?.isStarted}
    <!-- Hand Path Builder Workspace - only visible when started -->
    <div class="workspace-panel" data-testid="workspace-panel">
      <div class="hand-path-workspace-container">
        <HandPathWorkspace
          pathState={createModuleState.handPathCoordinator.pathState}
          isStarted={createModuleState.handPathCoordinator.isStarted}
          onSegmentComplete={createModuleState.handPathCoordinator
            .handleSegmentComplete}
          onAdvancePressed={createModuleState.handPathCoordinator
            .handleAdvancePressed}
          onAdvanceReleased={createModuleState.handPathCoordinator
            .handleAdvanceReleased}
        />
      </div>
    </div>
  {:else if navigationState.activeTab !== "gestural"}
    <!-- Standard Sequence Display (not in gestural mode) -->
    <div class="workspace-panel" data-testid="workspace-panel">
      <!-- Sequence Display -->
      <div class="sequence-display-container">
        <SequenceDisplay
          {sequenceState}
          currentWord={currentWord()}
          onBeatSelected={isMultiSelectMode
            ? handleMultiSelectToggle
            : handleBeatSelected}
          onStartPositionSelected={handleStartPositionSelected}
          onBeatDelete={handleBeatDelete}
          selectedBeatNumber={localSelectedBeatNumber}
          practiceBeatNumber={practiceBeatIndex}
          {isSideBySideLayout}
          {isMultiSelectMode}
          selectedBeatNumbers={sequenceState?.selectedBeatNumbers ??
            new Set<number>()}
          onBeatLongPress={handleBeatLongPress}
          onStartLongPress={() => handleBeatLongPress(0)}
        />
      </div>

      <!-- Selection Toolbar (appears in multi-select mode) -->
      {#if isMultiSelectMode}
        <div class="selection-toolbar-container">
          <SelectionToolbar
            {selectionCount}
            {totalBeats}
            onEdit={handleBatchEdit}
            onCancel={handleExitMultiSelect}
          />
        </div>
      {/if}

      <!-- Toast for validation errors -->
      <Toast
        message={toastMessage ?? ""}
        onDismiss={() => (toastMessage = null)}
      />

      <!-- Multi-select mode overlay -->
      {#if isMultiSelectMode}
        <MultiSelectOverlay onCancel={handleExitMultiSelect} />
      {/if}
    </div>
  {/if}
{:else}
  <div class="workspace-panel loading" data-testid="workspace-panel">
    <div class="loading-message">Initializing workspace...</div>
  </div>
{/if}

<style>
  .workspace-panel {
    position: relative;
    flex: 1;
    display: flex;
    flex-direction: column; /* Always stack sequence display above buttons */
    /* Transparent background to show beautiful background without blur */
    background: transparent;
    border: none;
    border-radius: var(--border-radius);
    overflow: hidden;
    border-radius: 12px;
  }

  .sequence-display-container,
  .hand-path-workspace-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
    z-index: 10; /* Above multi-select overlay */
  }

  .selection-toolbar-container {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px 0;
    width: 100%;
    flex-shrink: 0; /* Prevent toolbar from shrinking */
  }

  .workspace-panel.loading {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .loading-message {
    color: #666;
    font-size: 14px;
  }
</style>
