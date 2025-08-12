/**
 * Positioning Services Registration
 * Handles registration of arrow positioning and calculation services
 */

import type { ServiceContainer } from '../ServiceContainer';
import {
	IArrowAdjustmentCalculatorInterface,
	IArrowCoordinateSystemServiceInterface,
	IArrowLocationCalculatorInterface,
	IArrowPlacementDataServiceInterface,
	IArrowPlacementKeyServiceInterface,
	IArrowPositioningOrchestratorInterface,
	IArrowPositioningServiceInterface,
	IArrowRotationCalculatorInterface,
	IDashLocationCalculatorInterface,
	IDirectionalTupleProcessorInterface,
	IPositioningServiceFactoryInterface,
} from '../interfaces/positioning-interfaces';

import { ArrowPositioningService } from '../../implementations/ArrowPositioningService';

/**
 * Register all positioning services with their dependencies
 */
export async function registerPositioningServices(container: ServiceContainer): Promise<void> {
	// Register placement services (no dependencies)
	container.registerSingletonClass(IArrowPlacementDataServiceInterface);
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

	// Register ArrowPositioningService with dependencies
	container.registerFactory(IArrowPositioningServiceInterface, () => {
		const placementDataService = container.resolve(IArrowPlacementDataServiceInterface);
		const placementKeyService = container.resolve(IArrowPlacementKeyServiceInterface);
		return new ArrowPositioningService(placementDataService, placementKeyService);
	});
}
