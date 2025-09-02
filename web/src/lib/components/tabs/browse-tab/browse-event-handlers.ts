import type { FilterType, FilterValue, SequenceData } from "$domain";
import type { BrowseState } from "$state";

/**
 * Event handlers for the Browse tab
 * Extracted from BrowseTab.svelte to reduce component complexity
 */
export function createBrowseEventHandlers(
  browseState: BrowseState,
  setPanelIndex: (index: number) => void
) {
  // Filter and navigation handlers
  function handleFilterSelected(data: { type: string; value: unknown }) {
    console.log("🔍 Filter selected:", data);
    browseState.applyFilter(data.type as FilterType, data.value as FilterValue);
    setPanelIndex(1);
  }

  function handleSequenceSelected(sequence: SequenceData) {
    console.log("📄 Sequence selected:", sequence.word);
    browseState.selectSequence(sequence);
  }

  function handleBackToFilters() {
    console.log("⬅️ Back to filters");
    browseState.backToFilters();
    setPanelIndex(0);
  }

  function handleBackToBrowser() {
    console.log("⬅️ Back to browser");
    browseState.clearSelection();
  }

  // Sequence action handlers
  function handleSequenceAction(action: string, sequence: SequenceData) {
    console.log(`🎬 Action: ${action} on sequence:`, sequence.id);

    switch (action) {
      case "edit":
        // TODO: Navigate to construct tab with this sequence
        console.log("Edit sequence:", sequence.id);
        break;
      case "save":
      case "favorite":
        // Toggle favorite status
        browseState.toggleFavorite(sequence.id);
        break;
      case "delete": {
        // No conversion needed - already using SequenceData
        browseState.prepareDeleteSequence(sequence);
        break;
      }
      case "fullscreen":
        // TODO: Open sequence in fullscreen viewer
        console.log("Fullscreen sequence:", sequence.id);
        break;
      default:
        console.warn("Unknown action:", action);
    }
  }

  // Delete confirmation handlers
  function handleConfirmDelete() {
    browseState.confirmDeleteSequence();
  }

  function handleCancelDelete() {
    browseState.cancelDeleteSequence();
  }

  // Error handling
  function handleClearError() {
    browseState.clearError();
  }

  return {
    handleFilterSelected,
    handleSequenceSelected,
    handleBackToFilters,
    handleBackToBrowser,
    handleSequenceAction,
    handleConfirmDelete,
    handleCancelDelete,
    handleClearError,
  };
}
