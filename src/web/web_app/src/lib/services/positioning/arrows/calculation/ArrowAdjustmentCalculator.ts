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
import { MotionType } from '$lib/domain';
import type { IArrowAdjustmentCalculator } from '../../core-services';
import type { Location, Point } from '../../types';
import { AttributeKeyGenerator } from '../key_generators/AttributeKeyGenerator';
import { PlacementKeyGenerator } from '../key_generators/PlacementKeyGenerator';
import { SpecialPlacementOriKeyGenerator } from '../key_generators/SpecialPlacementOriKeyGenerator';
import { TurnsTupleKeyGenerator } from '../key_generators/TurnsTupleKeyGenerator';
import { ArrowAdjustmentLookup as AdvancedLookup } from '../orchestration/ArrowAdjustmentLookup';
import { DefaultPlacementService } from '../placement/DefaultPlacementService';
import { SpecialPlacementService } from '../placement/SpecialPlacementService';
import {
	DirectionalTupleCalculator,
	DirectionalTupleProcessor,
	QuadrantIndexCalculator,
	type IDirectionalTupleProcessor,
} from '../processors/DirectionalTupleProcessor';

export type IArrowAdjustmentLookup = AdvancedLookup;

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

	calculateAdjustmentSync(
		pictographData: PictographData,
		motionData: MotionData,
		letter: string,
		location: Location,
		arrowColor?: string
	): Point {
		/**
		 * Synchronous version of calculateAdjustment for use in sync contexts.
		 * Note: This may have limited functionality compared to the async version.
		 */
		try {
			// For now, we'll use a simplified synchronous approach
			// In a full implementation, this would need synchronous versions of all services

			// Use the directional tuple processor directly with basic adjustments
			const baseAdjustment = this.getBasicAdjustmentSync(motionData);
			const finalAdjustment = this.tupleProcessor.processDirectionalTuples(
				baseAdjustment,
				motionData,
				location
			);

			console.debug(
				`Sync adjustment for ${motionData.motion_type} ${motionData.turns} turns at ${location}: (${finalAdjustment.x}, ${finalAdjustment.y})`
			);

			return finalAdjustment;
		} catch (error) {
			console.warn(`Sync adjustment calculation failed for letter ${letter}: ${error}`);
			return { x: 0, y: 0 };
		}
	}

	private getBasicAdjustmentSync(motionData: MotionData): Point {
		/**Get basic adjustment values for synchronous operation using proper placement logic.*/
		const motionType = motionData.motion_type;
		const turns = typeof motionData.turns === 'number' ? motionData.turns : 0;
		const turnsStr = turns === Math.floor(turns) ? turns.toString() : turns.toString();

		// Use actual placement data structure (simplified for sync operation)
		// These values come from the actual JSON files in static/data/arrow_placement
		const placementData: Record<string, Record<string, [number, number]>> = {
			[MotionType.PRO]: {
				'0': [-10, -40],
				'0.5': [30, 105],
				'1': [30, 25],
				'1.5': [-35, 145],
				'2': [-10, -35],
				'2.5': [20, 100],
				'3': [30, 25],
			},
			[MotionType.ANTI]: {
				'0': [0, -40],
				'0.5': [-15, 110],
				'1': [0, -40],
				'1.5': [20, 155],
				'2': [0, -40],
				'2.5': [0, 100],
				'3': [0, -50],
			},
			[MotionType.STATIC]: {
				'0': [0, 0],
				'0.5': [0, -140],
				'1': [50, 50],
				'1.5': [0, 0],
				'2': [0, 0],
				'2.5': [0, 0],
				'3': [0, 0],
			},
			[MotionType.DASH]: {
				'0': [0, 0],
			},
			[MotionType.FLOAT]: {
				fl: [30, -30],
			},
		};

		const motionAdjustments = placementData[motionType];
		if (motionAdjustments && motionAdjustments[turnsStr]) {
			const [x, y] = motionAdjustments[turnsStr];
			return { x, y };
		}

		return { x: 0, y: 0 };
	}

	private createDefaultLookupService(): IArrowAdjustmentLookup {
		/**Create lookup service with default dependencies.*/
		return new AdvancedLookup(
			new SpecialPlacementService(),
			new DefaultPlacementService(),
			new SpecialPlacementOriKeyGenerator(),
			new PlacementKeyGenerator(),
			new TurnsTupleKeyGenerator(),
			new AttributeKeyGenerator()
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
