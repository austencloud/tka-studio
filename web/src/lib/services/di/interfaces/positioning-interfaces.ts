/**
 * Positioning Service Interface Definitions
 * These handle arrow positioning, placement, and coordinate calculations
 */

import type {
  IArrowPlacementDataService,
  IArrowPlacementKeyService,
} from "../../interfaces/positioning-interfaces";
import { createServiceInterface } from "../types";

// Import enhanced positioning service interfaces
import type {
  IArrowAdjustmentCalculator,
  IArrowCoordinateSystemService,
  IArrowLocationCalculator,
  IArrowPositioningOrchestrator,
  IArrowRotationCalculator,
  IDashLocationCalculator,
  IDirectionalTupleCalculator,
  IDirectionalTupleProcessor,
  IPositioningServiceFactory,
} from "../../positioning";

// Import service implementations
import { ArrowPlacementDataService } from "../../implementations/ArrowPlacementDataService";
import { ArrowPlacementKeyService } from "../../implementations/ArrowPlacementKeyService";

// Import enhanced positioning service implementations
import { ArrowAdjustmentCalculator } from "../../positioning/arrows/calculation/ArrowAdjustmentCalculator";
import { ArrowLocationCalculator } from "../../positioning/arrows/calculation/ArrowLocationCalculator";
import { ArrowRotationCalculator } from "../../positioning/arrows/calculation/ArrowRotationCalculator";
import { DashLocationCalculator } from "../../positioning/arrows/calculation/DashLocationCalculator";
import { ArrowCoordinateSystemService } from "../../positioning/arrows/coordinate_system/ArrowCoordinateSystemService";
import { ArrowPositionCalculator } from "../../positioning/arrows/orchestration/ArrowPositionCalculator";
import {
  DirectionalTupleProcessor,
  QuadrantIndexCalculator,
} from "../../positioning/arrows/processors/DirectionalTupleProcessor";
import { PositioningServiceFactory } from "../../positioning/PositioningServiceFactory";

// Core positioning services
export const IArrowPlacementDataServiceInterface =
  createServiceInterface<IArrowPlacementDataService>(
    "IArrowPlacementDataService",
    ArrowPlacementDataService
  );

export const IArrowPlacementKeyServiceInterface =
  createServiceInterface<IArrowPlacementKeyService>(
    "IArrowPlacementKeyService",
    ArrowPlacementKeyService
  );

// IArrowPositioningService removed - use IArrowPositioningOrchestrator directly

// Enhanced positioning service interfaces
export const IArrowLocationCalculatorInterface =
  createServiceInterface<IArrowLocationCalculator>(
    "IArrowLocationCalculator",
    class extends ArrowLocationCalculator {
      constructor(...args: unknown[]) {
        super(args[0] as DashLocationCalculator | undefined);
      }
    }
  );

export const IArrowRotationCalculatorInterface =
  createServiceInterface<IArrowRotationCalculator>(
    "IArrowRotationCalculator",
    ArrowRotationCalculator
  );

export const IArrowAdjustmentCalculatorInterface =
  createServiceInterface<IArrowAdjustmentCalculator>(
    "IArrowAdjustmentCalculator",
    class extends ArrowAdjustmentCalculator {
      constructor(..._args: unknown[]) {
        super();
      }
    }
  );

export const IArrowCoordinateSystemServiceInterface =
  createServiceInterface<IArrowCoordinateSystemService>(
    "IArrowCoordinateSystemService",
    ArrowCoordinateSystemService
  );

export const IDashLocationCalculatorInterface =
  createServiceInterface<IDashLocationCalculator>(
    "IDashLocationCalculator",
    DashLocationCalculator
  );

export const IDirectionalTupleProcessorInterface =
  createServiceInterface<IDirectionalTupleProcessor>(
    "IDirectionalTupleProcessor",
    class extends DirectionalTupleProcessor {
      constructor(...args: unknown[]) {
        super(
          args[0] as IDirectionalTupleCalculator,
          args[1] as QuadrantIndexCalculator
        );
      }
    }
  );

export const IArrowPositioningOrchestratorInterface =
  createServiceInterface<IArrowPositioningOrchestrator>(
    "IArrowPositioningOrchestrator",
    class extends ArrowPositionCalculator {
      constructor(...args: unknown[]) {
        super(
          args[0] as IArrowLocationCalculator,
          args[1] as IArrowRotationCalculator,
          args[2] as IArrowAdjustmentCalculator,
          args[3] as IArrowCoordinateSystemService
        );
      }
    }
  );

export const IPositioningServiceFactoryInterface =
  createServiceInterface<IPositioningServiceFactory>(
    "IPositioningServiceFactory",
    PositioningServiceFactory
  );
