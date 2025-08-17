/**
 * Motion Tester Service Interfaces
 *
 * Service interfaces for motion tester functionality following TKA DI patterns.
 */

import { createServiceInterface } from "../types";
import type { PictographData } from "$lib/domain";
import type { MotionTesterState } from "../../../../routes/motion-tester/state/motion-tester-state.svelte";
import { AnimatedPictographDataService } from "../../../../routes/motion-tester/services/AnimatedPictographDataService";

// Service interfaces
export interface IAnimatedPictographDataService {
  createAnimatedPictographData(
    motionState: MotionTesterState
  ): Promise<PictographData | null>;
}

// Service interface tokens
export const IAnimatedPictographDataServiceInterface =
  createServiceInterface<IAnimatedPictographDataService>(
    "IAnimatedPictographDataService",
    AnimatedPictographDataService as new (
      ...args: unknown[]
    ) => IAnimatedPictographDataService
  );
