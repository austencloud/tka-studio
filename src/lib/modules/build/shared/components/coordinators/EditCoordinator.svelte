<script lang="ts">
  /**
   * Edit Coordinator Component
   *
   * Manages edit panel state, interactions, and beat editing operations.
   * Extracts edit panel logic from BuildTab.svelte for better separation of concerns.
   *
   * Domain: Build Module - Edit Panel Coordination
   */

  import { createComponentLogger } from "$shared";
  import { EditSlidePanel } from "../../../edit/components";
  import type { IBeatOperationsService } from "../../services/contracts";
  import type { PanelCoordinationState } from "../../state/panel-coordination-state.svelte";
  import type { BatchEditChanges } from "../../types/build-tab-types";
  import type { createBuildTabState as BuildTabStateType } from "../../state/build-tab-state.svelte";

  type BuildTabState = ReturnType<typeof BuildTabStateType>;

  const logger = createComponentLogger('EditCoordinator');

  // Props
  let {
    buildTabState,
    panelState,
    beatOperationsService,
    shouldUseSideBySideLayout,
    onError
  }: {
    buildTabState: BuildTabState;
    panelState: PanelCoordinationState;
    beatOperationsService: IBeatOperationsService;
    shouldUseSideBySideLayout: boolean;
    onError?: (error: string) => void;
  } = $props();

  // Derive beat data reactively from sequence state instead of using snapshot
  const selectedBeatData = $derived(() => {
    const beatIndex = panelState.editPanelBeatIndex;
    if (beatIndex === null) return null;

    // Beat 0 = start position - read from selectedStartPosition
    if (beatIndex === 0) {
      const startPos = buildTabState.sequenceState.selectedStartPosition;
      console.log('📍 EditCoordinator selectedBeatData (start position):', startPos);
      return startPos;
    }

    // Regular beats (1, 2, 3...) - get from sequence
    const sequence = buildTabState.sequenceState.currentSequence;
    if (!sequence || !sequence.beats) return null;

    const arrayIndex = beatIndex - 1;
    const beatData = sequence.beats[arrayIndex] || null;
    console.log(`📍 EditCoordinator selectedBeatData (beat ${beatIndex}):`, beatData);
    return beatData;
  });

  // Event handlers
  function handleOrientationChange(color: string, orientation: string) {
    console.log(`🔵 EditCoordinator.handleOrientationChange called:`, { color, orientation });

    const beatIndex = panelState.editPanelBeatIndex;
    console.log(`  beatIndex from panelState:`, beatIndex);

    if (beatIndex === null) {
      logger.warn("Cannot change orientation: no beat selected");
      return;
    }

    try {
      console.log(`  Calling beatOperationsService.updateBeatOrientation...`);
      beatOperationsService.updateBeatOrientation(
        beatIndex,
        color,
        orientation,
        buildTabState,
        panelState
      );
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to update orientation";
      logger.error("Failed to update orientation", err);
      onError?.(errorMessage);
    }
  }

  function handleTurnAmountChange(color: string, turnAmount: number) {
    const beatIndex = panelState.editPanelBeatIndex;
    if (beatIndex === null) {
      logger.warn("Cannot change turns: no beat selected");
      return;
    }

    try {
      beatOperationsService.updateBeatTurns(
        beatIndex,
        color,
        turnAmount,
        buildTabState,
        panelState
      );
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to update turns";
      logger.error("Failed to update turns", err);
      onError?.(errorMessage);
    }
  }

  function handleBatchApply(changes: BatchEditChanges) {
    try {
      beatOperationsService.applyBatchChanges(changes, buildTabState);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to apply changes";
      logger.error("Failed to apply batch changes", err);
      onError?.(errorMessage);

      // Error recovery: Clear selection and close panel to prevent stuck UI
      buildTabState.sequenceState.clearSelection();
      panelState.closeEditPanel();
    }
  }

  function handleRemoveBeat(beatNumber: number) {
    try {
      beatOperationsService.removeBeat(beatNumber - 1, buildTabState);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to remove beat";
      logger.error("Failed to remove beat", err);
      onError?.(errorMessage);
    }
  }

  function handleClosePanel() {
    panelState.closeEditPanel();
    // Exit multi-select mode when closing panel
    const selectedCount = buildTabState.sequenceState.selectedBeatNumbers?.size ?? 0;
    if (selectedCount > 0) {
      buildTabState.sequenceState.exitMultiSelectMode();
    }
  }
</script>

<EditSlidePanel
  isOpen={panelState.isEditPanelOpen}
  selectedBeatNumber={panelState.editPanelBeatIndex}
  selectedBeatData={selectedBeatData()}
  selectedBeatsData={panelState.editPanelBeatsData}
  combinedPanelHeight={panelState.combinedPanelHeight}
  isSideBySideLayout={shouldUseSideBySideLayout}
  onClose={handleClosePanel}
  onOrientationChanged={handleOrientationChange}
  onTurnAmountChanged={handleTurnAmountChange}
  onBatchApply={handleBatchApply}
  onRemoveBeat={handleRemoveBeat}
/>
