/**
 * Pictograph Coordinator Implementation
 *
 * Single responsibility service for coordinating pictograph lifecycle.
 * Orchestrates arrow loading, positioning, and rendering coordination.
 */

import type { PictographData } from "$shared";
import { createArrowLifecycleResult } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { IArrowLifecycleManager } from "../../../arrow/orchestration/services/contracts";
import type {
  IPictographCoordinator,
  PictographRenderingState,
} from "../contracts/IPictographCoordinator";

@injectable()
export class PictographCoordinator implements IPictographCoordinator {
  constructor(
    @inject(TYPES.IArrowLifecycleManager)
    private arrowLifecycleManager: IArrowLifecycleManager
  ) {}

  /**
   * Coordinate complete pictograph lifecycle
   * Ensures proper loading order and state coordination
   */
  async coordinatePictographLifecycle(
    pictographData: PictographData
  ): Promise<PictographRenderingState> {
    try {
      // Use the arrow lifecycle manager to coordinate all arrow operations
      const arrowLifecycleResult =
        await this.arrowLifecycleManager.coordinateArrowLifecycle(
          pictographData
        );

      const errors: string[] = [];

      // Collect any errors from arrow lifecycle
      Object.values(arrowLifecycleResult.errors).forEach((error) => {
        if (error) errors.push(String(error));
      });

      const isReady = arrowLifecycleResult.allReady && errors.length === 0;

      return {
        arrowLifecycleResult,
        isReady,
        errors,
      };
    } catch (error) {
      console.error("Pictograph coordination failed:", error);

      const errorMessage =
        error instanceof Error ? error.message : "Unknown coordination error";

      return {
        arrowLifecycleResult: createArrowLifecycleResult({ allReady: false }),
        isReady: false,
        errors: [errorMessage],
      };
    }
  }

  /**
   * Reset coordinator state (for data changes)
   */
  resetCoordinatorState(): void {
    // Reset arrow lifecycle manager state
    this.arrowLifecycleManager.resetArrowState();
  }
}
