/**
 * Positioning Services Registration
 * Handles registration of arrow positioning and calculation services
 */

import type { ServiceContainer } from "../ServiceContainer";
import {
  IArrowAdjustmentCalculatorInterface,
  IArrowCoordinateSystemServiceInterface,
  IArrowLocationCalculatorInterface,
  IArrowPlacementServiceInterface,
  IArrowPlacementKeyServiceInterface,
  IArrowPositioningOrchestratorInterface,
  IArrowPositioningServiceInterface,
  IArrowLocationServiceInterface,
  IArrowRotationCalculatorInterface,
  IDashLocationCalculatorInterface,
  IDirectionalTupleProcessorInterface,
  IPositioningServiceFactoryInterface,
} from "../interfaces/positioning-interfaces";

/**
 * Register all positioning services with their dependencies
 */
export async function registerPositioningServices(
  container: ServiceContainer
): Promise<void> {
  // Register placement services (no dependencies)
  container.registerSingletonClass(IArrowPlacementServiceInterface);
  container.registerSingletonClass(IArrowPlacementKeyServiceInterface);

  // Register enhanced positioning services
  container.registerSingletonClass(IArrowCoordinateSystemServiceInterface);
  container.registerSingletonClass(IDashLocationCalculatorInterface);
  container.registerSingletonClass(IArrowRotationCalculatorInterface);
  container.registerSingletonClass(IPositioningServiceFactoryInterface);

  // Register directional tuple processor with dependencies
  container.registerFactory(IDirectionalTupleProcessorInterface, () => {
    const factory = container.resolve(IPositioningServiceFactoryInterface);
    return factory.createDirectionalTupleProcessor();
  });

  // Register arrow location calculator with dependencies
  container.registerFactory(IArrowLocationCalculatorInterface, () => {
    const factory = container.resolve(IPositioningServiceFactoryInterface);
    return factory.createLocationCalculator();
  });

  // Register arrow adjustment calculator with dependencies
  container.registerFactory(IArrowAdjustmentCalculatorInterface, () => {
    const factory = container.resolve(IPositioningServiceFactoryInterface);
    return factory.createAdjustmentCalculator();
  });

  // Register enhanced arrow positioning orchestrator
  container.registerFactory(IArrowPositioningOrchestratorInterface, () => {
    const factory = container.resolve(IPositioningServiceFactoryInterface);
    return factory.createPositioningOrchestrator();
  });

  // Register ArrowPositioningService as a thin wrapper around orchestrator
  container.registerSingletonClass(IArrowPositioningServiceInterface);

  // Register ArrowLocationService
  container.registerSingletonClass(IArrowLocationServiceInterface);

  // Note: ArrowPositioningService is now properly registered in DI container
}
