/**
 * Clear Sequence Workflow Utility
 *
 * Orchestrates the complex workflow for clearing a sequence with smooth animations.
 * Extracted from CreateModule to reduce complexity and improve testability.
 *
 * Workflow:
 * 1. Push undo snapshot
 * 2. Trigger layout transition (reset creation method selection)
 * 3. Wait for fade/layout animations (300ms)
 * 4. Clear all sequence data and UI state
 * 5. Close related panels
 *
 * Domain: Create module - Sequence management
 */

import { navigationState } from "$shared";
import type { createCreateModuleState as CreateModuleStateType } from "../state/create-module-state.svelte";
import type { createConstructTabState as ConstructTabStateType } from "../state/construct-tab-state.svelte";
import type { createPanelCoordinationState as PanelCoordinationStateType } from "../state/panel-coordination-state.svelte";

type CreateModuleState = ReturnType<typeof CreateModuleStateType>;
type ConstructTabState = ReturnType<typeof ConstructTabStateType>;
type PanelCoordinationState = ReturnType<typeof PanelCoordinationStateType>;

export interface ClearSequenceConfig {
  CreateModuleState: CreateModuleState;
  constructTabState: ConstructTabState;
  panelState: PanelCoordinationState;
  resetCreationMethodSelection: () => void;
}

/**
 * Executes the clear sequence workflow
 * @throws Error if the workflow fails
 */
export async function executeClearSequenceWorkflow(
  config: ClearSequenceConfig
): Promise<void> {
  const {
    CreateModuleState,
    constructTabState,
    panelState,
    resetCreationMethodSelection,
  } = config;

  try {
    // 1. Push undo snapshot
    CreateModuleState.pushUndoSnapshot("CLEAR_SEQUENCE", {
      description: "Clear sequence",
    });

    // 2. Manually trigger layout transition - bypass the effect system
    // This ensures immediate fade starts regardless of workspace state
    resetCreationMethodSelection();
    navigationState.setCreationMethodSelectorVisible(true);

    // 3. Wait for fade and layout transition to complete (300ms)
    // Everything fades together - beats, workspace, button panel, layout
    await new Promise((resolve) => setTimeout(resolve, 300));

    // 4. After animations complete, clear all data and reset UI
    // This happens after components have faded out, so no popping
    if (constructTabState) {
      constructTabState.setShowStartPositionPicker(true);
      constructTabState.setSelectedStartPosition(null);
      constructTabState.startPositionStateService.clearSelectedPosition();
      constructTabState.clearError();
    }

    if (CreateModuleState.sequenceState) {
      CreateModuleState.sequenceState.setCurrentSequence(null);
      CreateModuleState.sequenceState.clearSelection();
      CreateModuleState.sequenceState.clearError();
      await CreateModuleState.sequenceState.clearPersistedState();
    }

    // 5. Close related panels
    panelState.closeSharePanel();
  } catch (error) {
    const errorMessage =
      error instanceof Error ? error.message : "Failed to clear sequence";
    throw new Error(errorMessage);
  }
}
