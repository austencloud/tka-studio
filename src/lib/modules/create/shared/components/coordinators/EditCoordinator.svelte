<script lang="ts">
  /**
   * Edit Coordinator Component
   *
   * Manages edit panel state, interactions, and beat editing operations.
   * Extracts edit panel logic from CreateModule.svelte for better separation of concerns.
   *
   * Domain: Create module - Edit Panel Coordination
   */

  import { createComponentLogger } from "$shared";
  import { EditSlidePanel } from "../../../edit/components";
  import type { IBeatOperationsService } from "../../services/contracts";
  import type { createCreateModuleState as CreateModuleStateType } from "../../state/create-module-state.svelte";
  import type { PanelCoordinationState } from "../../state/panel-coordination-state.svelte";
  import type { BatchEditChanges } from "../../types/create-module-types";

  type CreateModuleState = ReturnType<typeof CreateModuleStateType>;

  const logger = createComponentLogger("EditCoordinator");

  // Props
  let {
    CreateModuleState,
    panelState,
    beatOperationsService,
    shouldUseSideBySideLayout,
    onError,
  }: {
    CreateModuleState: CreateModuleState;
    panelState: PanelCoordinationState;
    beatOperationsService: IBeatOperationsService;
    shouldUseSideBySideLayout: boolean;
    onError?: (error: string) => void;
  } = $props();

  // Derive beat data reactively from sequence state instead of using snapshot
  const selectedBeatData = $derived(() => {
    const beatIndex = panelState.editPanelBeatIndex;
    if (beatIndex === null) return null;

    // Beat 0 = start position - read from selectedStartPosition and convert to BeatData
    if (beatIndex === 0) {
      const startPos = CreateModuleState.sequenceState.selectedStartPosition;
      console.log(
        "📍 EditCoordinator selectedBeatData (start position):",
        startPos
      );
      if (!startPos) return null;

      // Convert PictographData to BeatData
      return {
        ...startPos,
        beatNumber: 0,
        duration: 1000,
        blueReversal: false,
        redReversal: false,
        isBlank: false,
      };
    }

    // Regular beats (1, 2, 3...) - get from sequence
    const sequence = CreateModuleState.sequenceState.currentSequence;
    if (!sequence || !sequence.beats) return null;

    const arrayIndex = beatIndex - 1;
    const beatData = sequence.beats[arrayIndex] || null;
    console.log(
      `📍 EditCoordinator selectedBeatData (beat ${beatIndex}):`,
      beatData
    );
    return beatData;
  });

  // Event handlers
  function handleOrientationChange(color: string, orientation: string) {
    console.log(`🔵 EditCoordinator.handleOrientationChange called:`, {
      color,
      orientation,
    });

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
        CreateModuleState,
        panelState
      );
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to update orientation";
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
        CreateModuleState,
        panelState
      );
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to update turns";
      logger.error("Failed to update turns", err);
      onError?.(errorMessage);
    }
  }

  function handleBatchApply(changes: BatchEditChanges) {
    try {
      beatOperationsService.applyBatchChanges(changes, CreateModuleState);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to apply changes";
      logger.error("Failed to apply batch changes", err);
      onError?.(errorMessage);

      // Error recovery: Clear selection and close panel to prevent stuck UI
      CreateModuleState.sequenceState.clearSelection();
      panelState.closeEditPanel();
    }
  }

  function handleRemoveBeat(beatNumber: number) {
    try {
      beatOperationsService.removeBeat(beatNumber - 1, CreateModuleState);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to remove beat";
      logger.error("Failed to remove beat", err);
      onError?.(errorMessage);
    }
  }

  function handleClosePanel() {
    console.log("🔴 handleClosePanel called");
    console.log(
      "🔴 selectedBeatNumber before clear:",
      CreateModuleState.sequenceState.selectedBeatNumber
    );

    panelState.closeEditPanel();

    // Clear single beat selection
    CreateModuleState.sequenceState.clearSelection();

    console.log(
      "🔴 selectedBeatNumber after clear:",
      CreateModuleState.sequenceState.selectedBeatNumber
    );

    // Exit multi-select mode if active
    const selectedCount =
      CreateModuleState.sequenceState.selectedBeatNumbers?.size ?? 0;
    if (selectedCount > 0) {
      CreateModuleState.sequenceState.exitMultiSelectMode();
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
