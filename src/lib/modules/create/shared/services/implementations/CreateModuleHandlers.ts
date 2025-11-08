/**
 * CreateModuleHandlers.ts
 *
 * Service implementation for CreateModule event handlers.
 * Extracts handler logic from component to improve testability and maintainability.
 */

import { injectable, inject } from "inversify";
import { TYPES } from "$shared";
import type { PictographData, BuildModeId } from "$shared";
import type { NavigationState } from "$shared/navigation/state/navigation-state.svelte";
import type { CreateModuleState } from "../../state/create-module-state.svelte";
import type { PanelCoordinationState } from "../../state/panel-coordination-state.svelte";
import type {
  ICreateModuleHandlers,
  ClearSequenceParams,
} from "../contracts/ICreateModuleHandlers";
import type { ICreateModuleService } from "../contracts/ICreateModuleService";
import type { IBeatOperationsService } from "../contracts/IBeatOperationsService";
import { executeClearSequenceWorkflow } from "../../utils/clearSequenceWorkflow";

@injectable()
export class CreateModuleHandlers implements ICreateModuleHandlers {
  constructor(
    @inject(TYPES.ICreateModuleService)
    private createModuleService: ICreateModuleService,
    @inject(TYPES.IBeatOperationsService)
    private beatOperationsService: IBeatOperationsService
  ) {}

  /**
   * Handle option selection from option viewer
   */
  async handleOptionSelected(option: PictographData): Promise<void> {
    try {
      await this.createModuleService.selectOption(option);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to select option";
      console.error(
        "❌ CreateModuleHandlers: Error handling option selection:",
        err
      );
      throw new Error(errorMessage);
    }
  }

  /**
   * Handle play animation button click
   */
  handlePlayAnimation(panelState: PanelCoordinationState): void {
    panelState.openAnimationPanel();
  }

  /**
   * Handle share button click
   */
  handleOpenSharePanel(panelState: PanelCoordinationState): void {
    panelState.openSharePanel();
  }

  /**
   * Handle creation method selection
   */
  handleCreationMethodSelected(
    method: BuildModeId,
    CreateModuleState: CreateModuleState | null,
    navigationState: NavigationState,
    onMethodSelected: () => void
  ): void {
    // Clear undo history when starting new creation session
    // This creates a clean mental model: each creation session is independent
    if (CreateModuleState) {
      CreateModuleState.clearUndoHistory();
    }

    // Mark that user has selected a creation method
    onMethodSelected();

    // Switch to the selected tab
    navigationState.setActiveTab(method);
    // The effect will automatically hide the selector based on hasSelectedCreationMethod
  }

  /**
   * Handle clear sequence button click
   */
  async handleClearSequence(params: ClearSequenceParams): Promise<void> {
    try {
      await executeClearSequenceWorkflow(params);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to clear sequence";
      console.error(
        "❌ CreateModuleHandlers: Failed to clear sequence completely",
        err
      );
      throw new Error(errorMessage);
    }
  }

  /**
   * Handle remove beat button click
   */
  handleRemoveBeat(
    beatIndex: number,
    CreateModuleState: CreateModuleState | null
  ): void {
    if (!CreateModuleState) {
      console.warn(
        "⚠️ CreateModuleHandlers: Cannot remove beat - CreateModuleState not initialized"
      );
      throw new Error("CreateModuleState not initialized");
    }

    try {
      this.beatOperationsService.removeBeat(beatIndex, CreateModuleState);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to remove beat";
      console.error("❌ CreateModuleHandlers: Failed to remove beat", err);
      throw new Error(errorMessage);
    }
  }

  /**
   * Handle open filter panel button click
   */
  handleOpenFilterPanel(panelState: PanelCoordinationState): void {
    panelState.openFilterPanel();
  }

  /**
   * Handle open sequence actions button click
   */
  handleOpenSequenceActions(panelState: PanelCoordinationState): void {
    panelState.openSequenceActionsPanel();
  }
}
