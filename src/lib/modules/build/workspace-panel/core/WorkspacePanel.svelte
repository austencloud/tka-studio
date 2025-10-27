<!--
	WorkspacePanel.svelte

	Workspace panel containing the sequence display and action buttons.
	Main area for viewing and interacting with the sequence.
-->
<script lang="ts">
  import SequenceDisplay from "../sequence-display/components/SequenceDisplay.svelte";
  import ButtonPanel from "../shared/components/ButtonPanel.svelte";
  import SelectionToolbar from "../components/SelectionToolbar.svelte";
  import Toast from "../components/Toast.svelte";

  // Props
  let {
    sequenceState,
    onClearSequence,
    buildTabState,
    practiceBeatIndex = null,

    // Button panel props
    canGoBack = false,
    onBack,
    canRemoveBeat = false,
    onRemoveBeat,
    selectedBeatIndex = null,
    selectedBeatData = null,
    canEditBeat = false,
    onEditBeat,
    canClearSequence = false,
    canSaveSequence = false,
    onSaveSequence,
    showFullScreen = true,

    // Animation state ref (for animate tab)
    animationStateRef = null,

    // Layout mode
    isSideBySideLayout = false
  }: {
    sequenceState?: any; // TODO: Type this properly
    onClearSequence?: () => Promise<void>;
    buildTabState?: any; // TODO: Type this properly
    practiceBeatIndex?: number | null;

    // Button panel props
    canGoBack?: boolean;
    onBack?: () => void;
    canRemoveBeat?: boolean;
    onRemoveBeat?: (beatIndex: number) => void;
    selectedBeatIndex?: number | null;
    selectedBeatData?: any;
    canEditBeat?: boolean;
    onEditBeat?: () => void;
    canClearSequence?: boolean;
    canSaveSequence?: boolean;
    onSaveSequence?: () => void;
    showFullScreen?: boolean;

    // Animation state ref
    animationStateRef?: any | null;

    // Layout mode
    isSideBySideLayout?: boolean;
  } = $props();

  // Derived state for current tab
  const isAnimateTab = $derived(buildTabState?.activeSubTab === "animate");

  // Local beat selection state (beatNumber: 0=start, 1=first beat, etc.)
  let localSelectedBeatNumber = $state<number | null>(null);

  // Multi-select state
  const isMultiSelectMode = $derived(
    sequenceState?.selectedBeatNumbers && sequenceState.selectedBeatNumbers.size > 0
  );
  const selectionCount = $derived(
    sequenceState?.selectedBeatNumbers?.size ?? 0
  );
  const totalBeats = $derived(
    sequenceState?.currentSequence?.beats?.length ?? 0
  );

  // Toast message for validation errors
  let toastMessage = $state<string | null>(null);

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
    // Opening batch edit panel is handled by BuildTab watching selectedBeatNumbers
    // This function is just for the toolbar button - no action needed here
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
  {:else}
    <!-- Button Panel at bottom (context-aware) -->
    <div class="button-panel-container">
      {#if isAnimateTab}
        <!-- Animate tab: Show Undo, Remove Beat, Edit Beat, Clear Sequence, and Fullscreen buttons -->
        <ButtonPanel
          {buildTabState}
          {canRemoveBeat}
          {onRemoveBeat}
          {selectedBeatIndex}
          {selectedBeatData}
          {canEditBeat}
          {onEditBeat}
          canClearSequence={canClearSequence}
          onClearSequence={onClearSequence}
          sequenceData={sequenceState?.currentSequence}
          showFullScreen={showFullScreen}
        />
      {:else}
        <!-- Default build controls -->
        <ButtonPanel
          {buildTabState}
          {canGoBack}
          {onBack}
          {canRemoveBeat}
          {onRemoveBeat}
          {selectedBeatIndex}
          {selectedBeatData}
          {canEditBeat}
          {onEditBeat}
          {canClearSequence}
          onClearSequence={onClearSequence}
          {canSaveSequence}
          {onSaveSequence}
          sequenceData={sequenceState?.currentSequence}
          {showFullScreen}
        />
      {/if}
    </div>
  {/if}

  <!-- Toast for validation errors -->
  <Toast
    message={toastMessage ?? ""}
    onDismiss={() => toastMessage = null}
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
  }

  .button-panel-container,
  .selection-toolbar-container {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px 0;
    width: 100%;
    flex-shrink: 0; /* Prevent buttons from shrinking */
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
