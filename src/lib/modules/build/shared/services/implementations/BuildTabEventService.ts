/**
 * ConstructTab Event Service
 *
 * Centralized event handling for the ConstructTab component.
 * This service handles all the event coordination between different child components
 * that was previously scattered throughout the massive ConstructTab component.
 */

import { createBeatData, resolve, type BeatData, type IOrientationCalculationService, type PictographData, type SequenceData } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { injectable } from "inversify";
import type { IBuildTabEventService, IBuildConstructSectionCoordinator } from "../contracts";


@injectable()
export class BuildTabEventService implements IBuildTabEventService {
  private constructCoordinator: IBuildConstructSectionCoordinator | null = null;
  private orientationCalculationService: IOrientationCalculationService | null = null;
  private initialized = false;

  // Callback to access current sequence from component state
  private getCurrentSequenceCallback: (() => SequenceData | null) | null = null;
  private updateSequenceCallback: ((sequence: SequenceData) => void) | null = null;

  // Callback to add option to history
  private addOptionToHistoryCallback: ((beatIndex: number, beatData: BeatData) => void) | null = null;

  // Callback to push undo snapshot
  private pushUndoSnapshotCallback: ((type: 'ADD_BEAT', metadata?: any) => void) | null = null;

  constructor() {
    // Don't initialize services in constructor - wait for lazy initialization
  }

  private initializeServices() {
    if (this.initialized) {
      return; // Already initialized
    }

    try {
      this.constructCoordinator = resolve<IBuildConstructSectionCoordinator>(TYPES.IBuildConstructTabCoordinator);
      this.orientationCalculationService = resolve<IOrientationCalculationService>(TYPES.IOrientationCalculationService);
      this.initialized = true;
    } catch (error) {
      // This is expected during SSR - services will be resolved once client-side DI container is ready
      // Services will remain null and methods will handle gracefully
    }
  }

  /**
   * Set callbacks to access sequence state from component
   */
  setSequenceStateCallbacks(
    getCurrentSequence: () => SequenceData | null,
    updateSequence: (sequence: SequenceData) => void
  ): void {
    this.getCurrentSequenceCallback = getCurrentSequence;
    this.updateSequenceCallback = updateSequence;
  }

  /**
   * Set callback to add option to history
   */
  setAddOptionToHistoryCallback(
    addOptionToHistory: (beatIndex: number, beatData: BeatData) => void
  ): void {
    this.addOptionToHistoryCallback = addOptionToHistory;
  }

  /**
   * Set callback to push undo snapshot
   */
  setPushUndoSnapshotCallback(
    pushUndoSnapshot: (type: 'ADD_BEAT', metadata?: any) => void
  ): void {
    this.pushUndoSnapshotCallback = pushUndoSnapshot;
  }

  private ensureInitialized() {
    if (!this.initialized) {
      this.initializeServices();
    }
  }


  /**
   * Handle option selection in the Build tab
   * OPTIMIZED: Add to sequence immediately for responsive UX, then process in background
   */
  async handleOptionSelected(option: PictographData): Promise<void> {
    try {
      performance.mark('event-service-start');
      this.ensureInitialized();

      // Get current sequence from component state
      const currentSequence = this.getCurrentSequenceCallback?.();
      if (!currentSequence) {
        throw new Error("No current sequence available");
      }

      performance.mark('initialization-complete');

      // Calculate correct beat number based on current sequence length
      const nextBeatNumber = currentSequence.beats.length + 1;

      // 📸 PUSH UNDO SNAPSHOT: Save state BEFORE adding beat (now deferred via queueMicrotask)
      this.pushUndoSnapshotCallback?.('ADD_BEAT', {
        beatNumber: nextBeatNumber,
        description: `Add beat ${nextBeatNumber}`
      });

      // Create initial beat data from option with correct beat number
      let beatData = createBeatData({
        ...option, // Spread PictographData properties since BeatData extends PictographData
        beatNumber: nextBeatNumber,
        isBlank: false, // This is a real beat with pictograph data
      });

      performance.mark('beat-data-created');

      // 🔄 OPTIMIZATION: Calculate orientations BEFORE UI update to batch into single update
      if (currentSequence.beats.length > 0 && this.orientationCalculationService) {
        const lastBeat = currentSequence.beats[currentSequence.beats.length - 1];

        // Only apply orientation calculations if both beats have motion data
        if (!lastBeat.isBlank && !beatData.isBlank) {
          try {
            // Update start orientations from the last beat's end orientations
            beatData = this.orientationCalculationService.updateStartOrientations(beatData, lastBeat);
            performance.mark('start-orientations-complete');

            // Update end orientations based on the motion calculations
            beatData = this.orientationCalculationService.updateEndOrientations(beatData);
            performance.mark('end-orientations-complete');

            console.log(`🧭 BuildTabEventService: Calculated orientations for beat ${nextBeatNumber}`);
          } catch (orientationError) {
            console.warn(`⚠️ BuildTabEventService: Failed to calculate orientations for beat ${nextBeatNumber}:`, orientationError);
            // Continue without orientation updates rather than failing completely
          }
        }
      }
      performance.mark('orientation-processing-complete');

      // 🚀 SINGLE UI UPDATE: Add beat with orientations already calculated
      const finalSequence = {
        ...currentSequence,
        beats: [...currentSequence.beats, beatData]
      };
      performance.mark('sequence-updated');

      this.updateSequenceCallback?.(finalSequence);
      performance.mark('ui-callback-complete');

      // 📝 ADD TO HISTORY: Track this option addition for undo functionality
      this.addOptionToHistoryCallback?.(nextBeatNumber - 1, beatData); // beatIndex is 0-based
      performance.mark('history-updated');

      console.log(`🎯 BuildTabEventService: Added beat ${nextBeatNumber} with option:`, option.letter);

      // 📡 COORDINATION: Notify other components (async, non-blocking)
      performance.mark('coordination-start');
      if (this.constructCoordinator) {
        this.constructCoordinator.handleBeatAdded(beatData).catch(error => {
          console.warn("⚠️ BuildTabEventService: Coordination service error:", error);
        });
      }
      performance.mark('coordination-complete');

      console.log(`✅ BuildTabEventService: Successfully processed beat addition`);
    } catch (error) {
      console.error("❌ Error handling option selection:", error);
      throw error;
    }
  }

  /**
   * Handle beat modification from the Graph Editor
   */
  handleBeatModified(_beatIndex: number, _beatData: BeatData): void {
    // Handle beat modifications from graph editor
    // Note: The coordination service doesn't have handleBeatModified,
    // so we'll handle this locally or extend the interface if needed
  }

  /**
   * Handle arrow selection from the Graph Editor
   */
  handleArrowSelected(_arrowData: unknown): void {
    // Handle arrow selection events from graph editor
    // This could be used for highlighting or additional UI feedback
  }

  /**
   * Handle graph editor visibility changes
   */
  handleGraphEditorVisibilityChanged(_isVisible: boolean): void {
    // Handle graph editor visibility changes if needed
  }

  /**
   * Handle export setting changes from the Export Panel
   */
  handleExportSettingChanged(_event: CustomEvent): void {
    // Handle export setting changes - could save to settings service
  }

  /**
   * Handle preview update requests from the Export Panel
   */
  handlePreviewUpdateRequested(_event: CustomEvent): void {
    // Handle preview update requests
  }

  /**
   * Handle export requests from the Export Panel
   */
  handleExportRequested(event: CustomEvent): void {
    const { type, config } = event.detail;

    // Handle export requests
    if (type === "current") {
      // TODO: Implement actual export service call
      alert(
        `Exporting sequence "${config.sequence?.name || "Untitled"}" with ${config.sequence?.beats?.length || 0} beats`
      );
    } else if (type === "all") {
      // TODO: Implement actual export all service call
      alert("Exporting all sequences in library");
    }
  }

  /**
   * Setup component coordination
   */
  setupComponentCoordination(): void {
    // Ensure services are initialized
    this.ensureInitialized();

    // Register this service with the coordination service
    if (this.constructCoordinator) {
      this.constructCoordinator.setupComponentCoordination({
        constructTab: {
          handleEvent: (eventType: string, _data: unknown) => {
            switch (eventType) {
              case "ui_transition":
                // Handle legacy transition events if needed
                break;
              default:
                // Handle other events if needed
                break;
            }
          },
        },
      });
    }
  }

  // ============================================================================
  // INTERFACE IMPLEMENTATION
  // ============================================================================

  /**
   * Handle tab switch events
   */
  handleTabSwitch(tabId: string): void {
    console.log(`🔄 BuildTabEventService: Handling tab switch to ${tabId}`);
    // Implementation for tab switching logic
  }

  /**
   * Handle workbench update events
   */
  handleWorkbenchUpdate(data: any): void {
    console.log("🔄 BuildTabEventService: Handling workbench update", data);
    // Implementation for workbench update logic
  }

  /**
   * Handle option selection events
   */
  handleOptionSelection(option: any): void {
    console.log("🔄 BuildTabEventService: Handling option selection", option);
    // Implementation for option selection logic
  }
}

// Lazy singleton instance
let _buildTabEventService: BuildTabEventService | null = null;

/**
 * Get the singleton instance of ConstructTabEventService
 * Creates the instance only when first accessed, ensuring DI container is ready
 */
export function getBuildTabEventService(): BuildTabEventService {
  if (!_buildTabEventService) {
    _buildTabEventService = new BuildTabEventService();
  }
  return _buildTabEventService;
}

// Export the getter function directly for backward compatibility
export const constructTabEventService = getBuildTabEventService;
