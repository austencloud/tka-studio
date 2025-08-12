/**
 * Positioning Service Factory
 *
 * Factory for creating and wiring up all positioning services with proper dependencies.
 * Provides a centralized way to create the complete positioning pipeline.
 */

import { GridMode, MotionType } from '$lib/domain/enums';
import type {
	IArrowAdjustmentCalculator,
	IArrowCoordinateSystemService,
	IArrowLocationCalculator,
	IArrowPositioningOrchestrator,
	IArrowRotationCalculator,
	IDirectionalTupleProcessor,
	IPositioningServiceFactory,
} from '$services/positioning';
import { ArrowAdjustmentCalculator } from '$services/positioning/arrows/calculation/ArrowAdjustmentCalculator';
import { ArrowLocationCalculator } from '$services/positioning/arrows/calculation/ArrowLocationCalculator';
import { ArrowRotationCalculator } from '$services/positioning/arrows/calculation/ArrowRotationCalculator';
import { DashLocationCalculator } from '$services/positioning/arrows/calculation/DashLocationCalculator';
import { ArrowCoordinateSystemService } from '$services/positioning/arrows/coordinate_system/ArrowCoordinateSystemService';
import { AttributeKeyGenerator } from '$services/positioning/arrows/key_generators/AttributeKeyGenerator';
import { PlacementKeyGenerator } from '$services/positioning/arrows/key_generators/PlacementKeyGenerator';
import { SpecialPlacementOriKeyGenerator } from '$services/positioning/arrows/key_generators/SpecialPlacementOriKeyGenerator';
import { TurnsTupleKeyGenerator } from '$services/positioning/arrows/key_generators/TurnsTupleKeyGenerator';
import { ArrowAdjustmentLookup as AdvancedLookup } from '$services/positioning/arrows/orchestration/ArrowAdjustmentLookup';
import { ArrowPositioningOrchestrator } from '$services/positioning/arrows/orchestration/ArrowPositioningOrchestrator';
import { DefaultPlacementService } from '$services/positioning/arrows/placement/DefaultPlacementService';
import { SpecialPlacementService } from '$services/positioning/arrows/placement/SpecialPlacementService';
import {
	DirectionalTupleCalculator,
	DirectionalTupleProcessor,
	QuadrantIndexCalculator,
} from '$services/positioning/arrows/processors/DirectionalTupleProcessor';

export class PositioningServiceFactory implements IPositioningServiceFactory {
	/**
	 * Factory for creating the complete positioning service ecosystem.
	 *
	 * Creates all services with proper dependency injection and ensures
	 * they are wired together correctly for optimal positioning accuracy.
	 */

	private static instance: PositioningServiceFactory;

	// Singleton services (shared across all arrows)
	private dashLocationCalculator: DashLocationCalculator | undefined;
	private coordinateSystemService: IArrowCoordinateSystemService | undefined;
	private specialPlacementService: SpecialPlacementService | undefined;
	private defaultPlacementService: DefaultPlacementService | undefined;
	private directionalTupleProcessor: IDirectionalTupleProcessor | undefined;

	/**
	 * Get the singleton instance of the positioning service factory.
	 */
	static getInstance(): PositioningServiceFactory {
		if (!PositioningServiceFactory.instance) {
			PositioningServiceFactory.instance = new PositioningServiceFactory();
		}
		return PositioningServiceFactory.instance;
	}

	createLocationCalculator(): IArrowLocationCalculator {
		/**
		 * Create arrow location calculator with dash location service dependency.
		 */
		if (!this.dashLocationCalculator) {
			this.dashLocationCalculator = this.createDashLocationCalculator();
		}

		return new ArrowLocationCalculator(this.dashLocationCalculator);
	}

	createRotationCalculator(): IArrowRotationCalculator {
		/**
		 * Create arrow rotation calculator (no dependencies).
		 */
		return new ArrowRotationCalculator();
	}

	createAdjustmentCalculator(): IArrowAdjustmentCalculator {
		/**
		 * Create arrow adjustment calculator with placement services and tuple processor.
		 */
		if (!this.specialPlacementService) {
			this.specialPlacementService = new SpecialPlacementService();
		}

		if (!this.defaultPlacementService) {
			this.defaultPlacementService = new DefaultPlacementService();
		}

		if (!this.directionalTupleProcessor) {
			this.directionalTupleProcessor = this.createDirectionalTupleProcessor();
		}

		// Import and create ArrowAdjustmentLookup with cached services
		// This prevents creating new placement services on each instantiation
		const lookupService = new AdvancedLookup(
			this.specialPlacementService,
			this.defaultPlacementService,
			new SpecialPlacementOriKeyGenerator(),
			new PlacementKeyGenerator(),
			new TurnsTupleKeyGenerator(),
			new AttributeKeyGenerator()
		);

		return new ArrowAdjustmentCalculator(
			lookupService, // Use cached placement services
			this.directionalTupleProcessor
		);
	}

	createCoordinateSystemService(): IArrowCoordinateSystemService {
		/**
		 * Create coordinate system service (singleton for consistency).
		 */
		if (!this.coordinateSystemService) {
			this.coordinateSystemService = new ArrowCoordinateSystemService();
		}
		return this.coordinateSystemService;
	}

	createDashLocationCalculator(): DashLocationCalculator {
		/**
		 * Create dash location calculator (singleton for consistency).
		 */
		if (!this.dashLocationCalculator) {
			this.dashLocationCalculator = new DashLocationCalculator();
		}
		return this.dashLocationCalculator;
	}

	createDirectionalTupleProcessor(): IDirectionalTupleProcessor {
		/**
		 * Create directional tuple processor with dependencies.
		 */
		if (!this.directionalTupleProcessor) {
			const directionalTupleCalculator = new DirectionalTupleCalculator();
			const quadrantIndexCalculator = new QuadrantIndexCalculator();

			this.directionalTupleProcessor = new DirectionalTupleProcessor(
				directionalTupleCalculator,
				quadrantIndexCalculator
			);
		}
		return this.directionalTupleProcessor;
	}

	createPositioningOrchestrator(): IArrowPositioningOrchestrator {
		/**
		 * Create the complete positioning orchestrator with all dependencies.
		 * This is the main service that coordinates all positioning calculations.
		 */
		const locationCalculator = this.createLocationCalculator();
		const rotationCalculator = this.createRotationCalculator();
		const adjustmentCalculator = this.createAdjustmentCalculator();
		const coordinateSystemService = this.createCoordinateSystemService();

		return new ArrowPositioningOrchestrator(
			locationCalculator,
			rotationCalculator,
			adjustmentCalculator,
			coordinateSystemService
		);
	}

	/**
	 * Create a complete positioning pipeline for use in services.
	 * Returns all the key services needed for positioning operations.
	 */
	createPositioningPipeline(): {
		locationCalculator: IArrowLocationCalculator;
		rotationCalculator: IArrowRotationCalculator;
		adjustmentCalculator: IArrowAdjustmentCalculator;
		coordinateSystemService: IArrowCoordinateSystemService;
		orchestrator: IArrowPositioningOrchestrator;
	} {
		return {
			locationCalculator: this.createLocationCalculator(),
			rotationCalculator: this.createRotationCalculator(),
			adjustmentCalculator: this.createAdjustmentCalculator(),
			coordinateSystemService: this.createCoordinateSystemService(),
			orchestrator: this.createPositioningOrchestrator(),
		};
	}

	/**
	 * Reset all singleton services (useful for testing).
	 */
	resetServices(): void {
		this.dashLocationCalculator = undefined;
		this.coordinateSystemService = undefined;
		this.specialPlacementService = undefined;
		this.defaultPlacementService = undefined;
		this.directionalTupleProcessor = undefined;
	}

	/**
	 * Pre-warm all services by creating them in advance.
	 * Useful for ensuring consistent performance.
	 */
	async preWarmServices(): Promise<void> {
		console.log('Pre-warming positioning services...');

		// Create all singleton services
		this.createLocationCalculator();
		this.createRotationCalculator();
		this.createCoordinateSystemService();
		this.createDirectionalTupleProcessor();

		// Load placement data
		if (!this.defaultPlacementService) {
			this.defaultPlacementService = new DefaultPlacementService();
		}

		// Ensure placement data is loaded
		if (!this.defaultPlacementService.isLoaded()) {
			try {
				await this.defaultPlacementService.debugAvailableKeys(
					MotionType.PRO,
					GridMode.DIAMOND
				);
				console.log('✅ Positioning services pre-warmed successfully');
			} catch (error) {
				console.warn('⚠️ Some positioning services failed to pre-warm:', error);
			}
		}
	}
}

/**
 * Convenience function to get the positioning service factory instance.
 */
export function getPositioningServiceFactory(): PositioningServiceFactory {
	return PositioningServiceFactory.getInstance();
}

/**
 * Convenience function to create a complete positioning orchestrator.
 */
export function createPositioningOrchestrator(): IArrowPositioningOrchestrator {
	return getPositioningServiceFactory().createPositioningOrchestrator();
}
