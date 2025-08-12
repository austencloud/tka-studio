/**
 * Service registration and factory interfaces for dependency injection.
 */

import type {
	IArrowAdjustmentCalculator,
	IArrowCoordinateSystemService,
	IArrowLocationCalculator,
	IArrowPositioningOrchestrator,
	IArrowRotationCalculator,
	IDashLocationCalculator,
} from './core-services';
import type { IDirectionalTupleProcessor } from './data-services';

// Service registration interfaces for dependency injection
export interface IPositioningServiceRegistry {
	registerLocationCalculator(calculator: IArrowLocationCalculator): void;
	registerRotationCalculator(calculator: IArrowRotationCalculator): void;
	registerAdjustmentCalculator(calculator: IArrowAdjustmentCalculator): void;
	registerCoordinateSystemService(service: IArrowCoordinateSystemService): void;
	registerOrchestrator(orchestrator: IArrowPositioningOrchestrator): void;
}

// Comprehensive positioning service factory interface
export interface IPositioningServiceFactory {
	createLocationCalculator(): IArrowLocationCalculator;
	createRotationCalculator(): IArrowRotationCalculator;
	createAdjustmentCalculator(): IArrowAdjustmentCalculator;
	createCoordinateSystemService(): IArrowCoordinateSystemService;
	createDashLocationCalculator(): IDashLocationCalculator;
	createDirectionalTupleProcessor(): IDirectionalTupleProcessor;
	createPositioningOrchestrator(): IArrowPositioningOrchestrator;
}
