/**
 * Motion Tester Service Interfaces
 *
 * Service interfaces for motion tester functionality following TKA DI patterns.
 */

import { createServiceInterface } from "../ServiceContainer";
import type { PictographData } from "$lib/domain";
import { GridMode } from "$lib/domain";
import type { MotionTesterState } from "../../../../routes/motion-tester/state/motion-tester-state.svelte";
import type { ParsedCsvRow } from "$lib/services/implementations/CsvDataService";
import type { MotionTestParams } from "../../../../routes/motion-tester/services/MotionParameterService";
import { AnimatedPictographDataService } from "../../../../routes/motion-tester/services/AnimatedPictographDataService";
import { MotionTesterCsvLookupService } from "../../../../routes/motion-tester/services/MotionTesterCsvLookupService";

// Service interfaces
export interface IAnimatedPictographDataService {
  createAnimatedPictographData(
    motionState: MotionTesterState
  ): Promise<PictographData | null>;
}

export interface IMotionTesterCsvLookupService {
  findMatchingPictograph(
    blueParams: MotionTestParams,
    redParams: MotionTestParams,
    gridMode: GridMode
  ): Promise<PictographData | null>;

  findMatchingCsvRow(
    blueParams: MotionTestParams,
    redParams: MotionTestParams,
    gridMode: GridMode
  ): Promise<ParsedCsvRow | null>;
}

// Service interface tokens
export const IAnimatedPictographDataServiceInterface =
  createServiceInterface<IAnimatedPictographDataService>(
    "IAnimatedPictographDataService",
    AnimatedPictographDataService
  );

export const IMotionTesterCsvLookupServiceInterface =
  createServiceInterface<IMotionTesterCsvLookupService>(
    "IMotionTesterCsvLookupService",
    MotionTesterCsvLookupService
  );
