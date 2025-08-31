/**
 * Start Position Selection Service Interface
 *
 * Interface for handling start position selection business logic.
 * Manages the complete start position selection process including
 * data extraction, storage, and coordination.
 */

import type { PictographData } from "$domain";
import type { IStartPositionService } from "./IStartPositionService";

export interface IStartPositionSelectionService {
  /**
   * Handle the complete start position selection process
   * Includes data extraction, storage, preloading, and coordination
   */
  selectStartPosition(
    startPosPictograph: PictographData,
    applicationStartPositionService: IStartPositionService
  ): Promise<void>;
}
