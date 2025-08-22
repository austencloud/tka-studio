/**
 * Movement Generation Service Interface Definitions
 * Service interfaces for the movement pattern generation system
 */

import { GridPosition, Location } from "$lib/domain/enums";
import type {
  IMovementGeneratorService,
  IMovementPatternService,
  IMovementValidatorService,
  IPositionCalculatorService,
} from "../../interfaces/generation-interfaces";
import type { IPositionMappingService } from "../../interfaces/movement/IPositionMappingService";
import { createServiceInterface } from "../types";

// Import service implementations
import { MovementPatternService } from "../../implementations/domain/MovementPatternService";
import { MovementGeneratorService } from "../../implementations/generation/MovementGeneratorService";
// import { PositionCalculatorService } from "../../implementations/positioning/PositionCalculatorService";
import { MovementValidatorService } from "../../implementations/domain/MovementValidatorService";
import { PositionMappingService } from "../../implementations/movement/PositionMappingService";

// Movement Pattern Services
export const IMovementPatternServiceInterface =
  createServiceInterface<IMovementPatternService>(
    "IMovementPatternService",
    MovementPatternService
  );

export const IPositionCalculatorServiceInterface =
  createServiceInterface<IPositionCalculatorService>(
    "IPositionCalculatorService",
    class {
      getPositionSequence(
        _system: "alpha" | "beta" | "gamma",
        _count: number
      ): GridPosition[] {
        // Placeholder implementation
        return [];
      }
      getNextPosition(current: GridPosition, _forward: boolean): GridPosition {
        return current;
      }
      getCardinalDirections(
        _startPosition: GridPosition,
        _endPosition: GridPosition,
        _motionType: string
      ): [Location, Location] {
        // Placeholder implementation
        return [Location.NORTH, Location.SOUTH];
      }
      calculatePositionPairs(
        _sequence: GridPosition[]
      ): Array<[GridPosition, GridPosition]> {
        return [];
      }
    }
  );

export const IMovementValidatorServiceInterface =
  createServiceInterface<IMovementValidatorService>(
    "IMovementValidatorService",
    MovementValidatorService
  );

export const IMovementGeneratorServiceInterface =
  createServiceInterface<IMovementGeneratorService>(
    "IMovementGeneratorService",
    class extends MovementGeneratorService {
      constructor(...args: unknown[]) {
        super(
          args[0] as IMovementPatternService,
          args[1] as IPositionCalculatorService,
          args[2] as IMovementValidatorService
        );
      }
    }
  );

export const IPositionMappingServiceInterface =
  createServiceInterface<IPositionMappingService>(
    "IPositionMappingService",
    PositionMappingService
  );
