<!--
	WorkspacePanel.svelte

	Workspace panel containing the sequence display and action buttons.
	Main area for viewing and interacting with the sequence.
-->
<script lang="ts">
  import MultiSelectOverlay from "../components/MultiSelectOverlay.svelte";
  import SelectionToolbar from "../components/SelectionToolbar.svelte";
  import Toast from "../components/Toast.svelte";
  import SequenceDisplay from "../sequence-display/components/SequenceDisplay.svelte";
  import InlineAnimatorPanel from "../shared/components/InlineAnimatorPanel.svelte";
  import SequenceActionsSheet from "../shared/components/SequenceActionsSheet.svelte";

  // Props
  let {
    sequenceState,
    buildTabState,
    practiceBeatIndex = null,

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
    onPlayAnimation
  }: {
    sequenceState?: any; // TODO: Type this properly
    buildTabState?: any; // TODO: Type this properly
    practiceBeatIndex?: number | null;

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

  // Multi-select state - use the actual mode from selection state
  const isMultiSelectMode = $derived(
    sequenceState?.isMultiSelectMode ?? false
  );
  const selectionCount = $derived(
    sequenceState?.selectionCount ?? 0
  );
  const totalBeats = $derived(
    sequenceState?.currentSequence?.beats?.length ?? 0
  );

  // Toast message for validation errors
  let toastMessage = $state<string | null>(null);

  // Sequence Actions Sheet state
  let showSequenceActionsSheet = $state(false);

  // Inline Animator Panel state
  let showInlineAnimator = $state(false);

  // Get current word from sequence state
  const currentWord = $derived(() => {
    return sequenceState?.sequenceWord() ?? "";
  });

  // Handle beat selection (receives beatNumber: 1, 2, 3...)
  function handleBeatSelected(beatNumber: number) {
    if (!sequenceState) return;

    // Check if we're in Animate tab
    const isAnimateTabActive = buildTabState?.activeSubTab === "animate";

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
      // This is handled by an effect in BuildTab.svelte that watches for beat selection.
    }
  }

  // Handle start position selection (beatNumber 0)
  function handleStartPositionSelected() {
    if (!sequenceState) return;

    // Only proceed if there's actually a start position selected
    if (!sequenceState.hasStartPosition || !sequenceState.selectedStartPosition) {
      return;
    }

    // Select start position for editing (beatNumber 0)
    localSelectedBeatNumber = 0;
    sequenceState.selectStartPositionForEditing();

    // Note: We no longer switch to edit tab! The edit slide panel will open instead.
    // This is handled by an effect in BuildTab.svelte that watches for start position selection.
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
      setTimeout(() => toastMessage = null, 3000);
    }
  }

  function handleBatchEdit() {
    if (onBatchEdit) {
      onBatchEdit();
    }
  }

  // Sequence Actions Sheet handlers
  function handleOpenSequenceActions() {
    // Mutual exclusion: close other panels before opening this one
    showInlineAnimator = false;
    showSequenceActionsSheet = true;
  }

  function handleCloseSequenceActions() {
    showSequenceActionsSheet = false;
  }

  function handleAnimate() {
    // TODO: Implement animation - for now, navigate to animate tab would be handled by BuildTab
    // This could trigger a modal/fullscreen animator instead
    console.log("Animate action triggered");
  }

  function handleMirror() {
    // TODO: Implement mirror transformation
    console.log("Mirror action triggered");
  }

  function handleRotate() {
    // TODO: Implement rotation transformation
    console.log("Rotate action triggered");
  }

  function handleColorSwap() {
    // TODO: Implement color swap transformation
    console.log("Color swap action triggered");
  }

  function handleEdit() {
    // Edit is now handled by BuildTab
    console.log("Edit action triggered");
  }

  function handleSave() {
    // Save is now handled by BuildTab
    console.log("Save action triggered");
  }

  function handleCopyJSON() {
    // Copy sequence JSON to clipboard
    const sequence = sequenceState?.currentSequence;
    if (sequence) {
      navigator.clipboard.writeText(JSON.stringify(sequence, null, 2));
      toastMessage = "Sequence JSON copied to clipboard";
      setTimeout(() => toastMessage = null, 2000);
    }
  }

  // Inline Animator Panel handlers
  function handlePlayAnimation() {
    // Toggle animator - if open, close it (Stop); if closed, open it (Play)
    if (!showInlineAnimator) {
      // Mutual exclusion: close other panels before opening animator
      showSequenceActionsSheet = false;
    }
    showInlineAnimator = !showInlineAnimator;
  }

  function handleCloseAnimator() {
    showInlineAnimator = false;
  }
</script>

{#if sequenceState}
<div class="workspace-panel" data-testid="workspace-panel">
  <div class="sequence-display-container">
    <SequenceDisplay
      {sequenceState}
      currentWord={currentWord()}
      onBeatSelected={isMultiSelectMode ? handleMultiSelectToggle : handleBeatSelected}
      onStartPositionSelected={handleStartPositionSelected}
      selectedBeatNumber={localSelectedBeatNumber}
      practiceBeatNumber={practiceBeatIndex}
      {isSideBySideLayout}
      {isMultiSelectMode}
      selectedBeatNumbers={sequenceState?.selectedBeatNumbers ?? new Set<number>()}
      onBeatLongPress={handleBeatLongPress}
      onStartLongPress={() => handleBeatLongPress(0)}
      onSequenceActionsClick={handleOpenSequenceActions}
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
    onDismiss={() => toastMessage = null}
  />

  <!-- Multi-select mode overlay -->
  {#if isMultiSelectMode}
    <MultiSelectOverlay onCancel={handleExitMultiSelect} />
  {/if}

  <!-- Sequence Actions Sheet -->
  <SequenceActionsSheet
    show={showSequenceActionsSheet}
    hasSequence={!!sequenceState?.currentSequence}
    {toolPanelHeight}
    onAnimate={handleAnimate}
    onMirror={handleMirror}
    onRotate={handleRotate}
    onColorSwap={handleColorSwap}
    onEdit={handleEdit}
    onSave={handleSave}
    onCopyJSON={handleCopyJSON}
    onClose={handleCloseSequenceActions}
  />

  <!-- Inline Animator Panel -->
  <InlineAnimatorPanel
    sequence={sequenceState?.currentSequence ?? null}
    show={showInlineAnimator}
    onClose={handleCloseAnimator}
    {toolPanelHeight}
  />

</div>
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

  .sequence-display-container {
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
