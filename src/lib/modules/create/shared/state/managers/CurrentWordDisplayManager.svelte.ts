/**
 * Current Word Display Manager
 *
 * Manages the effect that determines what text to display in the top bar
 * based on the current creation state.
 *
 * Handles contextual messaging for:
 * - Creation method selection prompt
 * - Guided mode header text
 * - Gestural mode (hand path) state messages
 * - Construct mode instructions
 * - Default sequence word display
 *
 * Extracted from CreateModule to reduce component complexity.
 *
 * Domain: Create module - Current word display management
 */

import { navigationState } from "$shared";
import type { createCreateModuleState as CreateModuleStateType } from "../create-module-state.svelte";
import type { createConstructTabState as ConstructTabStateType } from "../construct-tab-state.svelte";

type CreateModuleState = ReturnType<typeof CreateModuleStateType>;
type ConstructTabState = ReturnType<typeof ConstructTabStateType>;

export interface CurrentWordDisplayConfig {
  CreateModuleState: CreateModuleState;
  constructTabState: ConstructTabState;
  hasSelectedCreationMethod: () => boolean;
  onCurrentWordChange?: (word: string) => void;
}

/**
 * Creates the current word display effect
 * @returns Cleanup function
 */
export function createCurrentWordDisplayEffect(
  config: CurrentWordDisplayConfig
): () => void {
  const {
    CreateModuleState,
    constructTabState,
    hasSelectedCreationMethod,
    onCurrentWordChange,
  } = config;

  if (!onCurrentWordChange) {
    // No callback provided, return no-op cleanup
    return () => {};
  }

  // Effect: Notify parent of current word changes (or contextual message for hand path)
  const cleanup = $effect.root(() => {
    $effect(() => {
      if (!CreateModuleState) return;

      let displayText = "";

      // When creation method selector is visible, show selection prompt
      if (
        CreateModuleState.isWorkspaceEmpty() &&
        !hasSelectedCreationMethod()
      ) {
        displayText = "Choose Creation Mode";
      }
      // In guided mode, show the header text from Guided Builder
      else if (CreateModuleState.activeSection === "guided") {
        displayText =
          CreateModuleState.guidedModeHeaderText || "Guided Builder";
      }
      // In gestural (hand path) mode, show contextual message instead of word
      else if (
        navigationState.activeTab === "gestural" &&
        CreateModuleState.handPathCoordinator
      ) {
        const coordinator = CreateModuleState.handPathCoordinator;

        if (!coordinator.isStarted) {
          displayText = "Configure Your Settings";
        } else if (coordinator.pathState.isSessionComplete) {
          displayText = "Sequence Complete!";
        } else if (coordinator.pathState.currentHand === "blue") {
          displayText = "Drawing Blue Hand Path";
        } else if (coordinator.pathState.currentHand === "red") {
          displayText = "Drawing Red Hand Path";
        } else {
          displayText = "Draw Hand Path";
        }
      } else if (navigationState.activeTab === "construct") {
        // Show contextual instruction based on sequence state
        if (constructTabState?.shouldShowStartPositionPicker()) {
          // On start position picker: Show instruction
          displayText = "Choose your start position!";
        } else if (CreateModuleState.getCurrentBeatCount() === 0) {
          // Has start position but no beats yet
          displayText = "Select your first beat!";
        } else {
          // Has beats: Show the actual sequence word
          displayText = CreateModuleState.sequenceState?.sequenceWord() ?? "";
        }
      } else {
        // Default: Show current word
        displayText = CreateModuleState.sequenceState?.sequenceWord() ?? "";
      }

      onCurrentWordChange(displayText);
    });
  });

  return cleanup;
}
