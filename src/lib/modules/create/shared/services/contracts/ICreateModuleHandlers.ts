/**
 * ICreateModuleHandlers.ts
 *
 * Service interface for CreateModule event handlers.
 * Extracts handler logic from component to improve testability and maintainability.
 */

import type { PictographData, BuildModeId } from "$shared";
import type { NavigationState } from "$shared/navigation/state/navigation-state.svelte";
import type { CreateModuleState } from "../../state/create-module-state.svelte";
import type { ConstructTabState } from "../../state/construct-tab-state.svelte";
import type { PanelCoordinationState } from "../../state/panel-coordination-state.svelte";

/**
 * Parameters for clear sequence handler
 */
export interface ClearSequenceParams {
  CreateModuleState: CreateModuleState;
  constructTabState: ConstructTabState;
  panelState: PanelCoordinationState;
  resetCreationMethodSelection: () => void;
  shouldResetCreationMethod?: boolean; // Optional flag to control whether to reset creation method (default: true)
}

/**
 * Service for handling CreateModule events
 */
export interface ICreateModuleHandlers {
  /**
   * Handle option selection from option viewer
   * @throws Error if operation fails
   */
  handleOptionSelected(option: PictographData): Promise<void>;

  /**
   * Handle play animation button click
   */
  handlePlayAnimation(panelState: PanelCoordinationState): void;

  /**
   * Handle share button click
   */
  handleOpenSharePanel(panelState: PanelCoordinationState): void;

  /**
   * Handle creation method selection
   */
  handleCreationMethodSelected(
    method: BuildModeId,
    CreateModuleState: CreateModuleState | null,
    navigationState: NavigationState,
    onMethodSelected: () => void
  ): void;

  /**
   * Handle clear sequence button click
   * @throws Error if operation fails
   */
  handleClearSequence(params: ClearSequenceParams): Promise<void>;

  /**
   * Handle remove beat button click
   * @throws Error if operation fails
   */
  handleRemoveBeat(
    beatIndex: number,
    CreateModuleState: CreateModuleState | null
  ): void;

  /**
   * Handle open filter panel button click
   */
  handleOpenFilterPanel(panelState: PanelCoordinationState): void;

  /**
   * Handle open sequence actions button click
   */
  handleOpenSequenceActions(panelState: PanelCoordinationState): void;
}
