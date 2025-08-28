/**
 * Build Tab Service Interface
 *
 * Orchestrates complex business workflows for the Build tab.
 * Coordinates multiple microservices and manages cross-cutting concerns
 * like error handling, loading states, and state synchronization.
 */

import type { PictographData } from "./domain-types";

export interface IBuildTabService {
  /**
   * Handles the complete workflow for start position selection
   *
   * Orchestrates:
   * - UI loading state management
   * - Start position state updates
   * - Business logic execution via StartPositionSelectionService
   * - Error handling and cleanup
   *
   * @param position - The selected start position pictograph
   */
  selectStartPosition(position: PictographData): Promise<void>;

  /**
   * Handles the complete workflow for option selection
   *
   * Orchestrates:
   * - Option selection business logic via ConstructTabEventService
   * - Error handling and state management
   *
   * @param option - The selected pictograph option
   */
  selectOption(option: PictographData): Promise<void>;

  /**
   * Initializes the Build tab state and sets up component coordination
   *
   * Orchestrates:
   * - Component coordination setup
   * - Start position picker state initialization
   * - Initial data loading
   */
  initialize(): Promise<void>;
}
