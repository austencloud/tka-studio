/**
 * Build Tab Service Implementation
 *
 * Orchestrates complex business workflows for the Build tab.
 * Coordinates multiple microservices and manages cross-cutting concerns.
 *
 * This service handles the business logic that was previously scattered
 * across components, providing a clean separation of concerns.
 */

import type { BeatData, PictographData } from "$shared";
import { injectable } from "inversify";
// import type { IStartPositionService } from "../../tool-panel/construct/start-position-picker/services/contracts";
import type { IBuildTabService } from "../contracts";
// IStartPositionSelectionService removed - using unified service
import { constructTabEventService } from "./BuildTabEventService";

@injectable()
export class BuildTabService implements IBuildTabService {
  private currentTab: string = "construct"; // Default tab
  private tabStates: Map<string, unknown> = new Map();

  constructor(
    // @inject(TYPES.IStartPositionService)
    // private readonly startPositionService: IStartPositionService

    // Start position selection now handled by unified service
  ) {}

  /**
   * Orchestrates the complete start position selection workflow
   */
  async selectStartPosition(position: PictographData): Promise<void> {
    try {
      // Business logic: Convert PictographData to BeatData for the service
      const beatData: BeatData = {
        ...position, // Spread PictographData properties since BeatData extends PictographData
        id: `beat-${Date.now()}`,
        beatNumber: 0,
        duration: 1000,
        blueReversal: false,
        redReversal: false,
        isBlank: false,
      };
      // await this.startPositionService.setStartPosition(beatData);
    } catch (error) {
      console.error(
        "❌ BuildTabService: Error selecting start position:",
        error
      );
      throw error; // Re-throw to let caller handle UI error states
    }
  }

  /**
   * Orchestrates the complete option selection workflow
   */
  async selectOption(option: PictographData): Promise<void> {
    try {
      // Business logic: Use the construct tab event service to handle option selection
      const eventService = constructTabEventService();
      await eventService.handleOptionSelected(option);
    } catch (error) {
      console.error("❌ BuildTabService: Error selecting option:", error);
      throw error; // Re-throw to let caller handle UI error states
    }
  }

  /**
   * Initializes the Build tab and sets up component coordination
   */
  async initialize(): Promise<void> {
    try {
      // Setup component coordination
      const eventService = constructTabEventService();
      eventService.setupComponentCoordination(); // Not async, no await needed
    } catch (error) {
      console.error("❌ BuildTabService: Error initializing build tab:", error);
      throw error; // Re-throw to let caller handle UI error states
    }
  }

  /**
   * Get the current active tab
   */
  getCurrentTab(): string {
    return this.currentTab;
  }

  /**
   * Switch to a different tab
   */
  async switchToTab(tabId: string): Promise<void> {
    try {
      this.currentTab = tabId;
    } catch (error) {
      console.error(
        `❌ BuildTabService: Error switching to tab ${tabId}:`,
        error
      );
      throw error;
    }
  }

  /**
   * Get the state for a specific tab
   */
  getTabState(tabId: string): unknown {
    return this.tabStates.get(tabId) || null;
  }

  /**
   * Update the state for a specific tab
   */
  updateTabState(tabId: string, state: unknown): void {
    this.tabStates.set(tabId, state);
  }
}
