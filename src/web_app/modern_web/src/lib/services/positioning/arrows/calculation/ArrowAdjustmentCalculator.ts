/**
 * Arrow Adjustment Calculator - Enhanced Orchestration Service
 *
 * Clean, focused coordinator service that delegates to specialized components.
 * Direct TypeScript port of the Python ArrowAdjustmentCalculator.
 *
 * ARCHITECTURE:
 * - DefaultPlacementService: Handles default placement lookups
 * - SpecialPlacementService: Handles special placement lookups
 * - DirectionalTupleProcessor: Handles tuple generation and selection
 * - This service: Coordinates the pipeline with proper error propagation
 *
 * USAGE:
 *     calculator = new ArrowAdjustmentCalculator(placementServices, tupleProcessor)
 *     adjustment = await calculator.calculateAdjustment(pictographData, motion, letter, location)
 */

import type { MotionData, PictographData } from '$lib/domain';
import { GridMode, MotionType } from '$lib/domain';
import type { IArrowAdjustmentCalculator } from '../../core-services';
import type { Location, Point } from '../../types';
import { DefaultPlacementService } from '../placement/DefaultPlacementService';
import { SpecialPlacementService } from '../placement/SpecialPlacementService';
import {
	DirectionalTupleCalculator,
	DirectionalTupleProcessor,
	QuadrantIndexCalculator,
	type IDirectionalTupleProcessor,
} from '../processors/DirectionalTupleProcessor';

export interface IArrowAdjustmentLookup {
	getBaseAdjustment(
		pictographData: PictographData,
		motionData: MotionData,
		letter: string,
		arrowColor?: string
	): Promise<Point>;
}

export class ArrowAdjustmentLookup implements IArrowAdjustmentLookup {
	/**
	 * Service for looking up base adjustments from special and default placement data.
	 */

	constructor(
		private specialPlacementService: SpecialPlacementService,
		private defaultPlacementService: DefaultPlacementService
	) {}

	async getBaseAdjustment(
		pictographData: PictographData,
		motionData: MotionData,
		letter: string,
		arrowColor?: string
	): Promise<Point> {
		/**
		 * Get base adjustment using special → default placement lookup chain.
		 *
		 * Args:
		 *     pictographData: Pictograph data containing context
		 *     motionData: Motion data for placement lookup
		 *     letter: Letter for special placement lookup
		 *     arrowColor: Arrow color for special placement
		 *
		 * Returns:
		 *     Base adjustment point
		 */
		try {
			// STEP 1: Try special placement first
			const specialAdjustment = this.specialPlacementService.getSpecialAdjustment(
				motionData,
				pictographData,
				arrowColor
			);

			if (specialAdjustment && (specialAdjustment.x !== 0 || specialAdjustment.y !== 0)) {
				console.log(
					`Special placement found: (${specialAdjustment.x}, ${specialAdjustment.y})`
				);
				return specialAdjustment;
			}

			// STEP 2: Fall back to default placement
			const placementKey = this.generatePlacementKey(motionData, letter);
			const turns = motionData.turns || 0;
			const motionType = motionData.motion_type?.toLowerCase() || 'static';
			const gridMode = pictographData.grid_mode || 'diamond';

			console.log(`🔍 Looking up default placement:`, {
				placementKey,
				turns,
				motionType,
				gridMode,
				letter,
			});

			const defaultAdjustment = await this.defaultPlacementService.getDefaultAdjustment(
				placementKey,
				turns,
				motionType as MotionType,
				gridMode as GridMode
			);

			console.log(
				`✅ Default placement result: (${defaultAdjustment.x}, ${defaultAdjustment.y})`
			);
			return defaultAdjustment;
		} catch (error) {
			console.warn('Base adjustment lookup failed:', error);
			return { x: 0, y: 0 };
		}
	}

	private generatePlacementKey(motionData: MotionData, _letter: string): string {
		/**Generate placement key for default placement lookup.*/
		const motionType = motionData.motion_type?.toLowerCase() || 'static';
		const startLoc = motionData.start_loc || 'north';

		// Basic placement key generation - can be enhanced with more sophisticated logic
		return `${startLoc}_${motionType}`;
	}
}

export class ArrowAdjustmentCalculator implements IArrowAdjustmentCalculator {
	/**
	 * Clean coordinator service for arrow positioning with proper error handling.
	 *
	 * Delegates to focused services:
	 * - ArrowAdjustmentLookup: Special/default placement lookups
	 * - DirectionalTupleProcessor: Tuple generation and selection
	 *
	 * Provides comprehensive arrow positioning adjustment calculation.
	 */

	private lookupService: IArrowAdjustmentLookup;
	private tupleProcessor: IDirectionalTupleProcessor;

	constructor(
		lookupService?: IArrowAdjustmentLookup,
		tupleProcessor?: IDirectionalTupleProcessor
	) {
		/**
		 * Initialize with focused services.
		 *
		 * Args:
		 *     lookupService: Service for adjustment lookups
		 *     tupleProcessor: Service for directional tuple processing
		 */
		// Use provided services or create with default dependencies
		this.lookupService = lookupService || this.createDefaultLookupService();
		this.tupleProcessor = tupleProcessor || this.createDefaultTupleProcessor();
	}

	async calculateAdjustment(
		pictographData: PictographData,
		motionData: MotionData,
		letter: string,
		location: Location,
		arrowColor?: string
	): Promise<Point> {
		/**
		 * Calculate arrow position adjustment with streamlined parameters.
		 *
		 * Args:
		 *     pictographData: Pictograph data containing context
		 *     motionData: Motion data containing type, rotation, and location info
		 *     letter: Letter for special placement lookup
		 *     location: Pre-calculated arrow location
		 *     arrowColor: Color of the arrow ('red' or 'blue')
		 *
		 * Returns:
		 *     Final position adjustment as Point (to be added to initial position)
		 */
		try {
			return await this.calculateAdjustmentResult(
				pictographData,
				motionData,
				letter,
				location,
				arrowColor
			);
		} catch (error) {
			// Log error and return default for backward compatibility
			console.error(`Adjustment calculation failed: ${error}`);
			return { x: 0, y: 0 };
		}
	}

	async calculateAdjustmentResult(
		pictographData: PictographData,
		motionData: MotionData,
		letter: string,
		location: Location,
		arrowColor?: string
	): Promise<Point> {
		/**
		 * Calculate arrow position adjustment with proper error handling.
		 *
		 * Args:
		 *     pictographData: Pictograph data containing context
		 *     motionData: Motion data containing type, rotation, and location info
		 *     letter: Letter for special placement lookup
		 *     location: Pre-calculated arrow location
		 *     arrowColor: Color of the arrow ('red' or 'blue')
		 *
		 * Returns:
		 *     Point adjustment
		 *
		 * Throws:
		 *     Error: If calculation fails due to invalid input or system error
		 */
		try {
			// STEP 1: Look up base adjustment (special → default) - EXACTLY like legacy
			const baseAdjustment = await this.lookupService.getBaseAdjustment(
				pictographData,
				motionData,
				letter,
				arrowColor
			);

			// STEP 2: Process directional tuples - EXACTLY like legacy
			const finalAdjustment = this.tupleProcessor.processDirectionalTuples(
				baseAdjustment,
				motionData,
				location
			);

			return finalAdjustment;
		} catch (error) {
			console.error(`Adjustment calculation failed for letter ${letter}: ${error}`);
			throw new Error(`Arrow adjustment calculation failed: ${error}`);
		}
	}

	private createDefaultLookupService(): IArrowAdjustmentLookup {
		/**Create lookup service with default dependencies.*/
		return new ArrowAdjustmentLookup(
			new SpecialPlacementService(),
			new DefaultPlacementService()
		);
	}

	private createDefaultTupleProcessor(): IDirectionalTupleProcessor {
		/**Create tuple processor with default dependencies.*/
		return new DirectionalTupleProcessor(
			new DirectionalTupleCalculator(),
			new QuadrantIndexCalculator()
		);
	}
}
