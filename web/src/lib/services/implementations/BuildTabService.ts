/**
 * Build Tab Service Implementation
 *
 * Orchestrates complex business workflows for the Build tab.
 * Coordinates multiple microservices and manages cross-cutting concerns.
 *
 * This service handles the business logic that was previously scattered
 * across components, providing a clean separation of concerns.
 */

import { injectable, inject } from "inversify";
import { TYPES } from "../inversify/types";
import type { IBuildTabService } from "../interfaces/IBuildTabService";
import type { PictographData } from "../interfaces/domain-types";
import type { IStartPositionService } from "../interfaces/IStartPositionService";
// IStartPositionSelectionService removed - using unified service
import { constructTabEventService } from "./build/BuildTabEventService";

@injectable()
export class BuildTabService implements IBuildTabService {
  constructor(
    @inject(TYPES.IStartPositionService)
    private readonly startPositionService: IStartPositionService

    // Start position selection now handled by unified service
  ) {}

  /**
   * Orchestrates the complete start position selection workflow
   */
  async selectStartPosition(position: PictographData): Promise<void> {
    try {
      // Business logic: Use the unified service to handle start position selection
      await this.startPositionService.selectStartPosition(position);

      console.log("✅ BuildTabService: Start position selected successfully");
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

      console.log("✅ BuildTabService: Option selected successfully");
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

      console.log("✅ BuildTabService: Build tab initialized successfully");
    } catch (error) {
      console.error("❌ BuildTabService: Error initializing build tab:", error);
      throw error; // Re-throw to let caller handle UI error states
    }
  }
}
