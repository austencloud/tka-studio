/**
 * Auto Edit Panel Manager
 *
 * Handles automatic opening of edit panel when multiple beats are selected.
 * Consolidates multi-select edit panel logic from BuildTab.svelte.
 *
 * Domain: Build Module - Edit Panel Automation
 */

import { createComponentLogger } from "$shared";
import type { PanelCoordinationState } from "../panel-coordination-state.svelte";
import type { createBuildTabState as BuildTabStateType } from "../build-tab-state.svelte";

type BuildTabState = ReturnType<typeof BuildTabStateType>;

const logger = createComponentLogger('AutoEditPanelManager');
const START_POSITION_BEAT_NUMBER = 0;

export interface AutoEditPanelConfig {
  buildTabState: BuildTabState;
  panelState: PanelCoordinationState;
}

/**
 * Creates auto-open edit panel effect for multi-select
 * @returns Cleanup function
 */
export function createAutoEditPanelEffect(config: AutoEditPanelConfig): () => void {
  const { buildTabState, panelState } = config;

  return $effect.root(() => {
    $effect(() => {
      const selectedBeatNumbers = buildTabState.sequenceState?.selectedBeatNumbers;
      const selectedCount = selectedBeatNumbers?.size ?? 0;

      if (selectedCount > 1 && !panelState.isEditPanelOpen) {
        // Map beat numbers to beat data
        const beatNumbersArray = Array.from(selectedBeatNumbers).sort((a, b) => a - b);
        const beatsData = beatNumbersArray.map((beatNumber) => {
          if (beatNumber === START_POSITION_BEAT_NUMBER) {
            // Beat 0 is the start position
            return buildTabState.sequenceState.selectedStartPosition;
          } else {
            // Beats are numbered 1, 2, 3... but stored in array at indices 0, 1, 2...
            const beatIndex = beatNumber - 1;
            return buildTabState.sequenceState.currentSequence?.beats[beatIndex];
          }
        }).filter(Boolean); // Remove any null values

        logger.log(`Auto-opening batch edit panel: ${selectedCount} beats selected`);
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
  const { buildTabState, panelState } = config;

  return $effect.root(() => {
    $effect(() => {
      const selectedBeatNumber = buildTabState.sequenceState.selectedBeatNumber;
      const selectedData = buildTabState.sequenceState.selectedBeatData;

      // If a beat is selected, open the edit panel
      if (selectedBeatNumber !== null && selectedData) {
        panelState.openEditPanel(selectedBeatNumber, selectedData);
        logger.log(`Opening edit panel for beat ${selectedBeatNumber}`);
      }
    });
  });
}
