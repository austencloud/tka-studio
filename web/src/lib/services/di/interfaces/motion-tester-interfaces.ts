/**
 * Motion Tester Service Interface Definitions
 * Service interfaces for the motion testing system
 */

import type { PictographData } from "$lib/domain/PictographData";
import { createServiceInterface } from "../types";

// Placeholder interface for animated pictograph data service
export interface IAnimatedPictographDataService {
  createAnimatedPictographData(_state: unknown): Promise<PictographData | null>;
}

// Placeholder service interface
export const IAnimatedPictographDataServiceInterface =
  createServiceInterface<IAnimatedPictographDataService>(
    "IAnimatedPictographDataService",
    class {
      async createAnimatedPictographData(
        _state: unknown
      ): Promise<PictographData | null> {
        // Placeholder implementation
        return null;
      }
    }
  );
