/**
 * ConstructTab Event Service
 *
 * Centralized event handling for the ConstructTab component.
 * This service handles all the event coordination between different child components
 * that was previously scattered throughout the massive ConstructTab component.
 */

import { resolve, TYPES, type PictographData } from "$shared";
import { injectable } from "inversify";
import type { IBuildTabEventService, IConstructSubTabCoordinationService } from "../contracts";
import {  createBeatData, type BeatData } from "../../../workbench";


@injectable()
export class BuildTabEventService implements IBuildTabEventService {
  private constructCoordinator: IConstructSubTabCoordinationService | null = null;
  private initialized = false;

  constructor() {
    // Don't initialize services in constructor - wait for lazy initialization
  }

  private initializeServices() {
    if (this.initialized) {
      return; // Already initialized
    }

    try {
  this.constructCoordinator = resolve<IConstructSubTabCoordinationService>(TYPES.IConstructTabCoordinator);
      this.initialized = true;
    } catch (error) {
      // This is expected during SSR - services will be resolved once client-side DI container is ready
      // Services will remain null and methods will handle gracefully
    }
  }

  private ensureInitialized() {
    if (!this.initialized) {
      this.initializeServices();
    }
  }

  /**
   * Handle start position selection in the Build tab
   */
  async handleStartPositionSelected(startPosition: BeatData): Promise<void> {
    try {
      // DON'T set transitioning immediately - let the fade transitions handle the UI
      // setTransitioning(true); // ← REMOVED to prevent flash

      // Ensure services are initialized
      this.ensureInitialized();

      // Use coordination service to handle the selection
      if (this.constructCoordinator) {
        await this.constructCoordinator.handleStartPositionSet(startPosition);
      } else {
        throw new Error(
          "Coordination service not available after initialization"
        );
      }

      // Clear any previous errors
      // State management removed - components should handle their own state
    } catch (error) {
      console.error("❌ Error handling start position selection:", error);
      // State management removed - throw error for component to handle
      throw error;
    }
  }

  /**
   * Handle option selection in the Build tab
   */
  async handleOptionSelected(option: PictographData): Promise<void> {
    try {
      // State management removed - components should handle transitions

      // Create beat data from option
      // TODO: Service shouldn't access global state - pass beat number as parameter
      const beatData = createBeatData({
        beatNumber: 1, // Default for now - should be passed as parameter
        pictographData: option,
      });

      // Use coordination service to handle beat addition
      if (this.constructCoordinator) {
        await this.constructCoordinator.handleBeatAdded(beatData);
      }

      // Clear any previous errors
      // State management removed - components should handle their own state
    } catch (error) {
      console.error("❌ Error handling option selection:", error);
      // State management removed - throw error for component to handle
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
