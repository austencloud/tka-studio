import type { SequenceData, IExploreThumbnailService } from "$shared";
import { openSpotlightViewer } from "../../../../shared/application/state/app-state.svelte";
import { navigationState } from "../../../../shared/navigation/state/navigation-state.svelte";
import { galleryPanelManager } from "../state/gallery-panel-state.svelte";

interface ExploreHandlersParams {
  galleryState: any;
  setSelectedSequence: (sequence: SequenceData | null) => void;
  setDeleteConfirmationData: (data: any) => void;
  setError: (error: string | null) => void;
  thumbnailService: IExploreThumbnailService;
}

export function useExploreHandlers({
  galleryState,
  setSelectedSequence,
  setDeleteConfirmationData,
  setError,
  thumbnailService,
}: ExploreHandlersParams) {
  function handleSequenceSelect(sequence: SequenceData) {
    setSelectedSequence(sequence);
    galleryState.selectSequence(sequence);
  }

  async function handleSequenceAction(action: string, sequence: SequenceData) {
    try {
      switch (action) {
        case "select":
          handleSequenceSelect(sequence);
          break;
        case "view-detail":
          handleViewDetail(sequence);
          break;
        case "delete":
          handleSequenceDelete(sequence);
          break;
        case "favorite":
          await galleryState.toggleFavorite(sequence.id);
          break;
        case "fullscreen":
          handleSpotlightView(sequence);
          break;
        case "animate":
          galleryState.openAnimationModal(sequence);
          break;
        default:
          console.warn("⚠️ Unknown action:", action);
      }
    } catch (err) {
      console.error("❌ Action failed:", err);
      setError(
        err instanceof Error ? err.message : `Failed to ${action} sequence`
      );
    }
  }

  function handleViewDetail(sequence: SequenceData) {
    galleryPanelManager.openDetail(sequence);
  }

  function handleCloseDetailPanel() {
    galleryPanelManager.close();
  }

  function handleEditSequence(sequence: SequenceData) {
    try {
      // Store the sequence data in localStorage for the Create module to pick up
      localStorage.setItem(
        "tka-pending-edit-sequence",
        JSON.stringify(sequence)
      );

      // Close the detail panel if open
      handleCloseDetailPanel();

      // Navigate to Create module's construct tab
      navigationState.setCurrentModule("create");
      navigationState.setCurrentSection("construct");

      console.log("🖊️ Navigating to edit sequence:", sequence.id);
    } catch (err) {
      console.error("❌ Failed to initiate edit:", err);
      setError(
        err instanceof Error
          ? err.message
          : "Failed to open sequence for editing"
      );
    }
  }

  async function handleDetailPanelAction(
    action: string,
    sequence: SequenceData
  ) {
    // Handle actions from the detail panel
    switch (action) {
      case "play":
      case "animate":
        galleryState.openAnimationModal(sequence);
        break;
      case "fullscreen":
        handleSpotlightView(sequence);
        break;
      case "favorite":
        await galleryState.toggleFavorite(sequence.id);
        break;
      case "edit":
        handleEditSequence(sequence);
        break;
      case "delete":
        handleSequenceDelete(sequence);
        handleCloseDetailPanel(); // Close panel before showing delete dialog
        break;
      default:
        console.warn("⚠️ Unknown detail panel action:", action);
    }
  }

  function handleSequenceDelete(sequence: SequenceData) {
    setDeleteConfirmationData({
      sequence: sequence,
      relatedSequences: [],
      totalCount: 1,
    });
  }

  function handleSpotlightView(sequence: SequenceData) {
    openSpotlightViewer(sequence, thumbnailService);

    // Also update URL for sharing/bookmarking
    import("$shared/navigation/utils/sheet-router").then(
      ({ openSpotlight }) => {
        openSpotlight(sequence.id);
      }
    );
  }

  async function handleDeleteConfirm(deleteConfirmationData: any) {
    if (!deleteConfirmationData?.sequence) return;

    try {
      // TODO: Implement actual delete logic
      console.log(
        "🗑️ Deleting sequence:",
        deleteConfirmationData.sequence.id
      );
      setDeleteConfirmationData(null);
      // Refresh the sequence list
      await galleryState.loadAllSequences();
    } catch (err) {
      console.error("❌ Delete failed:", err);
      setError(err instanceof Error ? err.message : "Failed to delete sequence");
    }
  }

  function handleDeleteCancel() {
    setDeleteConfirmationData(null);
  }

  function handleErrorDismiss() {
    setError(null);
  }

  function handleRetry() {
    setError(null);
    galleryState.loadAllSequences();
  }

  return {
    handleSequenceSelect,
    handleSequenceAction,
    handleViewDetail,
    handleCloseDetailPanel,
    handleEditSequence,
    handleDetailPanelAction,
    handleSequenceDelete,
    handleSpotlightView,
    handleDeleteConfirm,
    handleDeleteCancel,
    handleErrorDismiss,
    handleRetry,
  };
}
