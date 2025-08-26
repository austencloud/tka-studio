/**
 * Pictograph Generation Service Interface Definitions
 * Service interfaces for the pictograph pattern generation system
 */

import { GridPosition, Location } from "$lib/domain/enums";
import type {
  IDirectionCalculator,
  IPictographGenerator,
  IPictographValidatorService,
  IPositionPatternService,
  IPositionSequenceService,
} from "../../interfaces/generation-interfaces";
import type { IGridModeDeriver } from "../../interfaces/movement/IGridModeDeriver";
import type { IPositionMapper } from "../../interfaces/movement/IPositionMapper";
import { createServiceInterface } from "../types";

// Import service implementations
import { PositionPatternService } from "../../implementations/domain/PositionPatternService";
// import { PositionCalculatorService } from "../../implementations/positioning/PositionCalculatorService";
import { GridModeDeriver } from "../../implementations/domain/GridModeDeriver";
import { PictographValidatorService } from "../../implementations/domain/PictographValidatorService";
import { PictographGenerator } from "../../implementations/generation/PictographGenerator";
import { PositionMapper } from "../../implementations/movement/PositionMapper";
import { LetterDeriver } from "../../implementations/domain/LetterDeriver";

// Position Pattern Services
export const PositionPatternServiceDI =
  createServiceInterface<IPositionPatternService>(
    "IPositionPatternService",
    PositionPatternService
  );

// Split the large position calculator into focused services
export const PositionSequenceServiceDI =
  createServiceInterface<IPositionSequenceService>(
    "IPositionSequenceService",
    class {
      getPositionSequence(
        _system: "alpha" | "beta" | "gamma",
        _count: number
      ): GridPosition[] {
        return [];
      }
      getNextPosition(current: GridPosition, _forward: boolean): GridPosition {
        return current;
      }
      calculatePositionPairs(
        _sequence: GridPosition[]
      ): Array<[GridPosition, GridPosition]> {
        return [];
      }
    }
  );

export const DirectionCalculatorDI =
  createServiceInterface<IDirectionCalculator>(
    "IDirectionCalculator",
    class {
      getCardinalDirections(
        _startPosition: GridPosition,
        _endPosition: GridPosition,
        _motionType: string
      ): [Location, Location] {
        return [Location.NORTH, Location.SOUTH];
      }
    }
  );

export const PictographValidatorServiceDI =
  createServiceInterface<IPictographValidatorService>(
    "IPictographValidatorService",
    PictographValidatorService
  );

export const PictographGeneratorDI =
  createServiceInterface<IPictographGenerator>(
    "IPictographGenerator",
    class extends PictographGenerator {
      constructor(...args: unknown[]) {
        super(
          args[0] as IPositionPatternService,
          args[1] as IDirectionCalculator,
          args[2] as IPictographValidatorService
        );
      }
    }
  );

export const PositionMapperDI = createServiceInterface<IPositionMapper>(
  "IPositionMapper",
  PositionMapper
);

// GridModeDeriver interface - now follows standard pattern
export const GridModeDeriverDI = createServiceInterface<IGridModeDeriver>(
  "IGridModeDeriver",
  GridModeDeriver
);

// LetterDeriver interface
export const LetterDeriverDI = createServiceInterface<
  import("../../implementations/domain/LetterDeriver").ILetterDeriver
>("ILetterDeriver", LetterDeriver);
