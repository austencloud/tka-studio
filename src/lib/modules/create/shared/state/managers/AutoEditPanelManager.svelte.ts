/**
 * Auto Edit Panel Manager
 *
 * Handles automatic opening of edit panel when multiple beats are selected.
 * Consolidates multi-select edit panel logic from CreateModule.svelte.
 *
 * Domain: Create module - Edit Panel Automation
 */

import { createComponentLogger } from "$shared";
import type { PanelCoordinationState } from "../panel-coordination-state.svelte";
import type { createCreateModuleState as CreateModuleStateType } from "../create-module-state.svelte";

type CreateModuleState = ReturnType<typeof CreateModuleStateType>;

// Lazy logger initialization to avoid circular dependency issues
let logger: ReturnType<typeof createComponentLogger> | null = null;
const getLogger = () => {
  if (!logger) {
    logger = createComponentLogger('AutoEditPanelManager');
  }
  return logger;
};

const START_POSITION_BEAT_NUMBER = 0;

export interface AutoEditPanelConfig {
  CreateModuleState: CreateModuleState;
  panelState: PanelCoordinationState;
}

/**
 * Creates auto-open edit panel effect for multi-select
 * @returns Cleanup function
 */
export function createAutoEditPanelEffect(config: AutoEditPanelConfig): () => void {
  const { CreateModuleState, panelState } = config;

  return $effect.root(() => {
    $effect(() => {
      const selectedBeatNumbers = CreateModuleState.sequenceState?.selectedBeatNumbers;
      const selectedCount = selectedBeatNumbers?.size ?? 0;

      if (selectedCount > 1 && !panelState.isEditPanelOpen) {
        // Map beat numbers to beat data
        const beatNumbersArray = Array.from(selectedBeatNumbers).sort((a, b) => a - b);
        const beatsData = beatNumbersArray.map((beatNumber) => {
          if (beatNumber === START_POSITION_BEAT_NUMBER) {
            // Beat 0 is the start position
            return CreateModuleState.sequenceState.selectedStartPosition;
          } else {
            // Beats are numbered 1, 2, 3... but stored in array at indices 0, 1, 2...
            const beatIndex = beatNumber - 1;
            return CreateModuleState.sequenceState.currentSequence?.beats[beatIndex];
          }
        }).filter(Boolean); // Remove any null values

        getLogger().log(`Auto-opening batch edit panel: ${selectedCount} beats selected`);
        panelState.openBatchEditPanel(beatsData);
      }
    });
  });
}

/**
 * Creates single-beat edit panel effect
 * @returns Cleanup function
 */
export function createSingleBeatEditEffect(config: AutoEditPanelConfig): () => void {
  const { CreateModuleState, panelState } = config;

  return $effect.root(() => {
    $effect(() => {
      const selectedBeatNumber = CreateModuleState.sequenceState.selectedBeatNumber;
      const selectedData = CreateModuleState.sequenceState.selectedBeatData;

      console.log('🟢 AutoEditPanelManager $effect triggered:', {
        selectedBeatNumber,
        hasSelectedData: !!selectedData,
        isEditPanelOpen: panelState.isEditPanelOpen
      });

      // If a beat is selected, open the edit panel
      if (selectedBeatNumber !== null && selectedData) {
        panelState.openEditPanel(selectedBeatNumber, selectedData);
        getLogger().log(`Opening edit panel for beat ${selectedBeatNumber}`);
      }
    });
  });
}
