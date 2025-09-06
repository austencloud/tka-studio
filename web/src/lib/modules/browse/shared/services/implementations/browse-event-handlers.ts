import type { SequenceData } from "../../../../../shared/domain";
import type {
  GalleryFilterType,
  GalleryFilterValue,
} from "../../../gallery/domain";
import type { BrowseState } from "../../../gallery/state/gallery-state-factory.svelte";

/**
 * Event handlers for the Browse tab
 * Extracted from BrowseTab.svelte to reduce component complexity
 */
export function createGalleryEventHandlers(
  galleryState: BrowseState,
  setPanelIndex: (index: number) => void
) {
  // Filter and navigation handlers
  function handleFilterSelected(data: { type: string; value: unknown }) {
    console.log("🔍 Filter selected:", data);
    galleryState.applyFilter(
      data.type as GalleryFilterType,
      data.value as GalleryFilterValue
    );
    setPanelIndex(1);
  }

  function handleSequenceSelected(sequence: SequenceData) {
    console.log("📄 Sequence selected:", sequence.word);
    galleryState.selectSequence(sequence);
  }

  function handleBackToFilters() {
    console.log("⬅️ Back to filters");
    galleryState.backToFilters();
    setPanelIndex(0);
  }

  function handleBackToBrowser() {
    console.log("⬅️ Back to browser");
    galleryState.clearSelection();
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
        galleryState.toggleFavorite(sequence.id);
        break;
      case "delete": {
        // No conversion needed - already using SequenceData
        galleryState.prepareDeleteSequence(sequence);
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
    galleryState.confirmDeleteSequence();
  }

  function handleCancelDelete() {
    galleryState.cancelDeleteSequence();
  }

  // Error handling
  function handleClearError() {
    galleryState.clearError();
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
