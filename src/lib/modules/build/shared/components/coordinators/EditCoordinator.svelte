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

  // Event handlers
  function handleOrientationChange(color: string, orientation: string) {
    const beatIndex = panelState.editPanelBeatIndex;
    if (beatIndex === null) {
      logger.warn("Cannot change orientation: no beat selected");
      return;
    }

    try {
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
  selectedBeatData={panelState.editPanelBeatData}
  selectedBeatsData={panelState.editPanelBeatsData}
  combinedPanelHeight={panelState.combinedPanelHeight}
  isSideBySideLayout={shouldUseSideBySideLayout}
  onClose={handleClosePanel}
  onOrientationChanged={handleOrientationChange}
  onTurnAmountChanged={handleTurnAmountChange}
  onBatchApply={handleBatchApply}
  onRemoveBeat={handleRemoveBeat}
/>
