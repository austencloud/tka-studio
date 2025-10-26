/**
 * Right Panel Navigation Controller
 *
 * Handles complex back button logic for RightPanel navigation.
 * Extracted from RightPanel.svelte's massive handleBack function.
 *
 * ✅ Single responsibility: navigation logic
 * ✅ No UI concerns, pure business logic
 * ✅ Testable and maintainable
 * ✅ Clear priority hierarchy for back navigation
 */

import type { ActiveBuildTab } from "$shared";
import type { IBuildTabState, IConstructTabState } from "../types/build-tab-types";

/**
 * Navigation Controller for Right Panel back button
 *
 * Priority order for back navigation:
 * 1. Advanced start position picker navigation
 * 2. Undo destructive operations (remove/clear beats)
 * 3. Undo last option selection
 * 4. Return to start position picker from option picker
 * 5. Normal tab navigation
 */
export class RightPanelNavigationController {
  constructor(
    private buildTabState: IBuildTabState,
    private constructTabState: IConstructTabState
  ) {}

  /**
   * Handles back button press with priority hierarchy
   *
   * @param activePanel - Currently active right panel
   * @param shouldShowStartPositionPicker - Whether start position picker should be shown
   * @param hasMovedFromStartPositionPicker - Whether user has moved from start position picker to option picker
   * @param isInAdvancedStartPositionPicker - Whether user is in advanced start position picker
   * @param constructTabContentRef - Reference to ConstructTabContent for delegating start position picker navigation
   * @param onClearingSequence - Callback when sequence is being cleared
   * @param onUndoingOption - Callback when option is being undone
   * @returns Object indicating navigation result
   */
  handleBack(params: {
    activePanel: ActiveBuildTab | null;
    shouldShowStartPositionPicker: boolean | null;
    hasMovedFromStartPositionPicker: boolean;
    isInAdvancedStartPositionPicker: boolean;
    constructTabContentRef?: {
      handleStartPositionPickerBack: () => boolean;
    };
    onClearingSequence: (isClearing: boolean) => void;
    onUndoingOption: (isUndoing: boolean) => void;
  }): { handled: boolean; action?: string } {
    const {
      activePanel,
      shouldShowStartPositionPicker,
      hasMovedFromStartPositionPicker,
      isInAdvancedStartPositionPicker,
      constructTabContentRef,
      onClearingSequence,
      onUndoingOption,
    } = params;

    // Priority 1: Advanced start position picker navigation
    if (isInAdvancedStartPositionPicker && constructTabContentRef) {
      const handled = constructTabContentRef.handleStartPositionPickerBack();
      if (handled) {
        return { handled: true, action: "advanced_picker_back" };
      }
    }

    // Priority 2: Undo destructive operations (remove/clear beats)
    if (this.buildTabState.canUndo) {
      const undoSuccess = this.undoDestructiveOperation();
      if (undoSuccess) {
        return { handled: true, action: "undo_destructive" };
      }
    }

    // Priority 3: Undo last option selection
    if (
      this.buildTabState.hasOptionHistory &&
      activePanel === "construct" &&
      shouldShowStartPositionPicker === false
    ) {
      const undone = this.undoLastOption(onUndoingOption);
      if (undone) {
        return { handled: true, action: "undo_option" };
      }
    }

    // Priority 4: Return to start position picker from option picker
    if (
      activePanel === "construct" &&
      shouldShowStartPositionPicker === false &&
      hasMovedFromStartPositionPicker &&
      !this.buildTabState.hasOptionHistory
    ) {
      this.returnToStartPositionPicker(onClearingSequence);
      return { handled: true, action: "return_to_start_picker" };
    }

    // Priority 5: Normal tab navigation
    this.buildTabState.goBack();
    return { handled: true, action: "tab_navigation" };
  }

  /**
   * Checks if back navigation is available
   */
  canGoBack(params: {
    activePanel: ActiveBuildTab | null;
    shouldShowStartPositionPicker: boolean | null;
    hasMovedFromStartPositionPicker: boolean;
    isInAdvancedStartPositionPicker: boolean;
  }): boolean {
    return (
      this.buildTabState.canGoBack ||
      this.buildTabState.canUndo ||
      this.buildTabState.hasOptionHistory ||
      params.isInAdvancedStartPositionPicker ||
      (params.activePanel === "construct" &&
        params.shouldShowStartPositionPicker === false &&
        params.hasMovedFromStartPositionPicker)
    );
  }

  // ============================================================================
  // PRIVATE HELPER METHODS
  // ============================================================================

  /**
   * Undoes the last destructive operation (remove/clear beats)
   */
  private undoDestructiveOperation(): boolean {
    console.log("⏪ NavigationController: Undoing last destructive operation");

    const undoSuccess = this.buildTabState.undo();
    if (undoSuccess) {
      console.log("✅ NavigationController: Undo successful");

      // Restore picker state to show option picker instead of start position picker
      this.constructTabState.restorePickerStateAfterUndo();

      return true;
    }

    return false;
  }

  /**
   * Undoes the last option selection
   */
  private undoLastOption(onUndoingOption: (isUndoing: boolean) => void): boolean {
    const lastOption = this.buildTabState.popLastOptionFromHistory();
    if (!lastOption) {
      return false;
    }

    console.log(
      `⏪ NavigationController: Undoing last option (beat ${lastOption.beatIndex})`
    );

    // SIMULTANEOUSLY: Start fade-out AND remove beat with animation
    onUndoingOption(true);
    this.buildTabState.sequenceState.removeBeatWithAnimation(lastOption.beatIndex);

    // After fade-out completes, fade back in with new options
    setTimeout(() => {
      onUndoingOption(false);
    }, 250); // Match OUT_DURATION from OptionViewer

    return true;
  }

  /**
   * Returns to start position picker by clearing the sequence
   */
  private returnToStartPositionPicker(onClearingSequence: (isClearing: boolean) => void) {
    console.log("⏪ NavigationController: Returning to start position picker");

    // No confirmation needed - directly clear and return to start position picker
    onClearingSequence(true);

    // Clear immediately to trigger the fade transition
    this.constructTabState.clearSequenceCompletely();

    // Clear option history when returning to start position picker
    this.buildTabState.clearOptionHistory();

    // Reset clearing flag after both transitions complete (250ms out + 250ms in)
    setTimeout(() => {
      onClearingSequence(false);
    }, 500);
  }
}
