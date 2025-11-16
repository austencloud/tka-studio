/**
 * ExploreEventHandlerService - Handles all explore module events and actions
 *
 * Coordinates sequence actions, detail panel interactions, and navigation
 * following the service-based architecture pattern.
 */

import type { SequenceData } from "$shared";
import { injectable, inject } from "inversify";
import { TYPES } from "$shared";
import type { IExploreEventHandlerService } from "../contracts/IExploreEventHandlerService";
import type { IExploreThumbnailService } from "../../../display/services/contracts";
import { openSpotlightViewer } from "../../../../../shared/application/state/app-state.svelte";
import { navigationState } from "../../../../../shared/navigation/state/navigation-state.svelte";
import { galleryPanelManager } from "../../state/gallery-panel-state.svelte";

interface ExploreEventHandlerParams {
  galleryState: any;
  setSelectedSequence: (sequence: SequenceData | null) => void;
  setDeleteConfirmationData: (data: any) => void;
  setError: (error: string | null) => void;
}

@injectable()
export class ExploreEventHandlerService implements IExploreEventHandlerService {
  private params: ExploreEventHandlerParams | null = null;

  constructor(
    @inject(TYPES.IExploreThumbnailService)
    private thumbnailService: IExploreThumbnailService
  ) {}

  /**
   * Initialize the service with required parameters
   * Called by ExploreModule on mount
   */
  initialize(params: ExploreEventHandlerParams): void {
    this.params = params;
  }

  private ensureInitialized(): void {
    if (!this.params) {
      throw new Error("ExploreEventHandlerService not initialized");
    }
  }

  handleSequenceSelect(sequence: SequenceData): void {
    this.ensureInitialized();
    this.params!.setSelectedSequence(sequence);
    this.params!.galleryState.selectSequence(sequence);
  }

  async handleSequenceAction(
    action: string,
    sequence: SequenceData
  ): Promise<void> {
    this.ensureInitialized();

    try {
      switch (action) {
        case "select":
          this.handleSequenceSelect(sequence);
          break;
        case "view-detail":
          this.handleViewDetail(sequence);
          break;
        case "delete":
          this.handleSequenceDelete(sequence);
          break;
        case "favorite":
          await this.params!.galleryState.toggleFavorite(sequence.id);
          break;
        case "fullscreen":
          this.handleSpotlightView(sequence);
          break;
        case "animate":
          this.params!.galleryState.openAnimationModal(sequence);
          break;
        default:
          console.warn("⚠️ Unknown action:", action);
      }
    } catch (err) {
      console.error("❌ Action failed:", err);
      this.params!.setError(
        err instanceof Error ? err.message : `Failed to ${action} sequence`
      );
    }
  }

  handleViewDetail(sequence: SequenceData): void {
    galleryPanelManager.openDetail(sequence);
  }

  handleCloseDetailPanel(): void {
    galleryPanelManager.close();
  }

  handleEditSequence(sequence: SequenceData): void {
    this.ensureInitialized();

    try {
      // Store the sequence data in localStorage for the Create module to pick up
      localStorage.setItem(
        "tka-pending-edit-sequence",
        JSON.stringify(sequence)
      );

      // Close the detail panel if open
      this.handleCloseDetailPanel();

      // Navigate to Create module's construct tab
      navigationState.setCurrentModule("create");
      navigationState.setCurrentSection("construct");

      console.log("🖊️ Navigating to edit sequence:", sequence.id);
    } catch (err) {
      console.error("❌ Failed to initiate edit:", err);
      this.params!.setError(
        err instanceof Error
          ? err.message
          : "Failed to open sequence for editing"
      );
    }
  }

  async handleDetailPanelAction(
    action: string,
    sequence: SequenceData
  ): Promise<void> {
    this.ensureInitialized();

    // Handle actions from the detail panel
    switch (action) {
      case "play":
      case "animate":
        this.params!.galleryState.openAnimationModal(sequence);
        break;
      case "fullscreen":
        this.handleSpotlightView(sequence);
        break;
      case "favorite":
        await this.params!.galleryState.toggleFavorite(sequence.id);
        break;
      case "edit":
        this.handleEditSequence(sequence);
        break;
      case "delete":
        this.handleSequenceDelete(sequence);
        this.handleCloseDetailPanel(); // Close panel before showing delete dialog
        break;
      default:
        console.warn("⚠️ Unknown detail panel action:", action);
    }
  }

  handleSequenceDelete(sequence: SequenceData): void {
    this.ensureInitialized();
    this.params!.setDeleteConfirmationData({
      sequence: sequence,
      relatedSequences: [],
      totalCount: 1,
    });
  }

  handleSpotlightView(sequence: SequenceData): void {
    openSpotlightViewer(sequence, this.thumbnailService);

    // Also update URL for sharing/bookmarking
    import("$shared/navigation/utils/sheet-router").then(
      ({ openSpotlight }) => {
        openSpotlight(sequence.id);
      }
    );
  }

  async handleDeleteConfirm(deleteConfirmationData: any): Promise<void> {
    this.ensureInitialized();

    if (!deleteConfirmationData?.sequence) return;

    try {
      // TODO: Implement actual delete logic
      console.log(
        "🗑️ Deleting sequence:",
        deleteConfirmationData.sequence.id
      );
      this.params!.setDeleteConfirmationData(null);
      // Refresh the sequence list
      await this.params!.galleryState.loadAllSequences();
    } catch (err) {
      console.error("❌ Delete failed:", err);
      this.params!.setError(
        err instanceof Error ? err.message : "Failed to delete sequence"
      );
    }
  }

  handleDeleteCancel(): void {
    this.ensureInitialized();
    this.params!.setDeleteConfirmationData(null);
  }

  handleErrorDismiss(): void {
    this.ensureInitialized();
    this.params!.setError(null);
  }

  handleRetry(): void {
    this.ensureInitialized();
    this.params!.setError(null);
    this.params!.galleryState.loadAllSequences();
  }
}
