<script lang="ts">
  /**
   * Confirmation Dialog Coordinator Component
   *
   * Manages confirmation dialogs for Create module operations.
   * Extracts dialog logic from CreateModule for better separation of concerns.
   *
   * Currently handles:
   * - Guided mode switch confirmation (when switching with existing sequence)
   * - Exit guided mode confirmation (when leaving with work in progress)
   *
   * Domain: Create module - Confirmation Dialog Coordination
   */

  import ConfirmDialog from "$shared/foundation/ui/ConfirmDialog.svelte";
  import { getCreateModuleContext } from "../../context";

  // Get context
  const ctx = getCreateModuleContext();
  const { CreateModuleState } = ctx;

  // Dialog state
  let showGuidedConfirm = $state(false);
  let guidedConfirmResolve: ((confirmed: boolean) => void) | null =
    $state(null);

  let showExitGuidedConfirm = $state(false);
  let exitGuidedConfirmResolve: ((confirmed: boolean) => void) | null =
    $state(null);

  // Register callbacks with CreateModuleState on mount
  $effect(() => {
    // Set up guided mode confirmation callback
    CreateModuleState.setConfirmGuidedSwitchCallback(async () => {
      return new Promise<boolean>((resolve) => {
        showGuidedConfirm = true;
        guidedConfirmResolve = resolve;
      });
    });

    // Set up exit guided mode confirmation callback
    CreateModuleState.setConfirmExitGuidedCallback(async () => {
      return new Promise<boolean>((resolve) => {
        showExitGuidedConfirm = true;
        exitGuidedConfirmResolve = resolve;
      });
    });
  });

  // Event handlers - Guided mode confirmation
  function handleConfirmGuidedSwitch() {
    showGuidedConfirm = false;
    if (guidedConfirmResolve) {
      guidedConfirmResolve(true);
      guidedConfirmResolve = null;
    }
  }

  function handleCancelGuidedSwitch() {
    showGuidedConfirm = false;
    if (guidedConfirmResolve) {
      guidedConfirmResolve(false);
      guidedConfirmResolve = null;
    }
  }

  // Event handlers - Exit guided mode confirmation
  function handleConfirmExitGuided() {
    showExitGuidedConfirm = false;
    if (exitGuidedConfirmResolve) {
      exitGuidedConfirmResolve(true);
      exitGuidedConfirmResolve = null;
    }
  }

  function handleCancelExitGuided() {
    showExitGuidedConfirm = false;
    if (exitGuidedConfirmResolve) {
      exitGuidedConfirmResolve(false);
      exitGuidedConfirmResolve = null;
    }
  }
</script>

<!-- Guided Mode Confirmation Dialog -->
<ConfirmDialog
  isOpen={showGuidedConfirm}
  title="Switch to Guided Mode?"
  message="Switching to Guided Mode will clear your current sequence. You can undo this action if needed."
  confirmText="Clear and Continue"
  cancelText="Cancel"
  variant="warning"
  onConfirm={handleConfirmGuidedSwitch}
  onCancel={handleCancelGuidedSwitch}
/>

<!-- Exit Guided Mode Confirmation Dialog -->
<ConfirmDialog
  isOpen={showExitGuidedConfirm}
  title="Exit Guided Mode?"
  message="Your Guided Builder progress will be lost. You can undo this action if needed."
  confirmText="Exit"
  cancelText="Cancel"
  variant="warning"
  onConfirm={handleConfirmExitGuided}
  onCancel={handleCancelExitGuided}
/>
