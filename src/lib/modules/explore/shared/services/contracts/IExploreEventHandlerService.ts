import type { SequenceData } from "$shared";

/**
 * Service for handling explore module events and actions
 */
export interface IExploreEventHandlerService {
  /**
   * Handle sequence selection
   */
  handleSequenceSelect(sequence: SequenceData): void;

  /**
   * Handle sequence actions (select, view-detail, delete, favorite, fullscreen, animate)
   */
  handleSequenceAction(action: string, sequence: SequenceData): Promise<void>;

  /**
   * Handle viewing sequence details
   */
  handleViewDetail(sequence: SequenceData): void;

  /**
   * Handle closing detail panel
   */
  handleCloseDetailPanel(): void;

  /**
   * Handle editing a sequence
   */
  handleEditSequence(sequence: SequenceData): void;

  /**
   * Handle detail panel actions (play, animate, fullscreen, favorite, edit, delete)
   */
  handleDetailPanelAction(action: string, sequence: SequenceData): Promise<void>;

  /**
   * Handle sequence deletion
   */
  handleSequenceDelete(sequence: SequenceData): void;

  /**
   * Handle opening spotlight view
   */
  handleSpotlightView(sequence: SequenceData): void;

  /**
   * Handle delete confirmation
   */
  handleDeleteConfirm(deleteConfirmationData: any): Promise<void>;

  /**
   * Handle delete cancellation
   */
  handleDeleteCancel(): void;

  /**
   * Handle error dismissal
   */
  handleErrorDismiss(): void;

  /**
   * Handle retry after error
   */
  handleRetry(): void;
}
