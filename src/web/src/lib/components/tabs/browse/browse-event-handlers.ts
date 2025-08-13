import type { SequenceData } from "$domain/SequenceData";
import type {
  BrowseSequenceMetadata,
  FilterType,
  FilterValue,
} from "$lib/domain/browse";
import type { BrowseState } from "$lib/state/browse-state.svelte";

/**
 * Event handlers for the Browse tab
 * Extracted from BrowseTab.svelte to reduce component complexity
 */
export function createBrowseEventHandlers(
  browseState: BrowseState,
  setPanelIndex: (index: number) => void,
) {
  // Filter and navigation handlers
  function handleFilterSelected(data: { type: string; value: unknown }) {
    console.log("🔍 Filter selected:", data);
    browseState.applyFilter(data.type as FilterType, data.value as FilterValue);
    setPanelIndex(1);
  }

  function handleSequenceSelected(sequence: BrowseSequenceMetadata) {
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
  function handleSequenceAction(
    action: string,
    sequence: SequenceData | BrowseSequenceMetadata,
  ) {
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
        // Prepare delete confirmation - convert to BrowseSequenceMetadata if needed
        const browseSequence =
          "isFavorite" in sequence
            ? (sequence as BrowseSequenceMetadata)
            : ({
                ...sequence,
                isFavorite: false,
                isCircular: false,
                word: sequence.id,
                thumbnails: [...sequence.thumbnails],
              } as unknown as BrowseSequenceMetadata);
        browseState.prepareDeleteSequence(browseSequence);
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
