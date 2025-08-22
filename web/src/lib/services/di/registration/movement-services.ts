/**
 * Movement Generation Services Registration
 * Handles registration of movement pattern generation services
 */

import type { ServiceContainer } from "../ServiceContainer";
import {
  IMovementGeneratorServiceInterface,
  IMovementPatternServiceInterface,
  IPositionCalculatorServiceInterface,
  IMovementValidatorServiceInterface,
  IPositionMappingServiceInterface,
} from "../interfaces/movement-interfaces";
import { MovementGeneratorService } from "../../implementations/generation/MovementGeneratorService";

/**
 * Register all movement generation services with their dependencies
 */
export async function registerMovementServices(
  container: ServiceContainer
): Promise<void> {
  // Register independent services first (no dependencies)
  container.registerSingletonClass(IMovementPatternServiceInterface);
  // container.registerSingletonClass(IPositionCalculatorServiceInterface);
  container.registerSingletonClass(IMovementValidatorServiceInterface);
  container.registerSingletonClass(IPositionMappingServiceInterface);

  // Register movement generator service with dependencies
  container.registerFactory(IMovementGeneratorServiceInterface, () => {
    const patternService = container.resolve(IMovementPatternServiceInterface);
    const positionCalculator = container.resolve(
      IPositionCalculatorServiceInterface
    );
    const validator = container.resolve(IMovementValidatorServiceInterface);

    return new MovementGeneratorService(
      patternService,
      positionCalculator,
      validator
    );
  });
}
