/**
 * Movement Generation Service Interface Definitions
 * Service interfaces for the movement pattern generation system
 */

import type {
  IMovementGeneratorService,
  IMovementPatternService,
  IPositionCalculatorService,
  IMovementValidatorService,
} from "../../interfaces/generation-interfaces";
import { createServiceInterface } from "../types";

// Import service implementations
import { MovementGeneratorService } from "../../implementations/MovementGeneratorService";
import { MovementPatternService } from "../../implementations/MovementPatternService";
import { PositionCalculatorService } from "../../implementations/PositionCalculatorService";
import { MovementValidatorService } from "../../implementations/MovementValidatorService";

// Movement Pattern Services
export const IMovementPatternServiceInterface =
  createServiceInterface<IMovementPatternService>(
    "IMovementPatternService",
    MovementPatternService
  );

export const IPositionCalculatorServiceInterface =
  createServiceInterface<IPositionCalculatorService>(
    "IPositionCalculatorService",
    PositionCalculatorService
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
