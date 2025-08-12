/**
 * Core positioning service interfaces for arrow location, rotation, and adjustment calculations.
 */

import type { ArrowData, GridMode, Location, MotionData, PictographData } from '$lib/domain';
import type { ArrowColor, MotionType, Point } from './types';

export interface IArrowLocationCalculator {
	/**
	 * Calculate the arrow location based on motion type and data.
	 */
	calculateLocation(motion: MotionData, pictographData?: PictographData): Location;
	getSupportedMotionTypes(): MotionType[];
	validateMotionData(motion: MotionData): boolean;
	isBlueArrowMotion(motion: MotionData, pictographData: PictographData): boolean;
}

export interface IArrowRotationCalculator {
	/**
	 * Calculate the arrow rotation angle based on motion type and location.
	 */
	calculateRotation(motion: MotionData, location: Location): number;
	getSupportedMotionTypes(): MotionType[];
	validateMotionData(motion: MotionData): boolean;
}

export interface IArrowAdjustmentCalculator {
	/**
	 * Calculate position adjustment for arrow based on placement rules.
	 */
	calculateAdjustment(
		pictographData: PictographData,
		motionData: MotionData,
		letter: string,
		location: Location,
		arrowColor?: string
	): Promise<Point>;

	/**
	 * Synchronous version of calculateAdjustment for use in sync contexts.
	 */
	calculateAdjustmentSync(
		pictographData: PictographData,
		motionData: MotionData,
		letter: string,
		location: Location,
		arrowColor?: string
	): Point;
}

export interface IArrowCoordinateSystemService {
	/**
	 * Get initial position coordinates based on motion type and location.
	 */
	getInitialPosition(motion: MotionData, location: Location): Point;
	getSceneCenter(): Point;
	getSceneDimensions(): [number, number];
	getCoordinateInfo(location: Location): Record<string, unknown>;
	validateCoordinates(point: Point): boolean;
	getAllHandPoints(): Record<Location, Point>;
	getAllLayer2Points(): Record<Location, Point>;
	getSupportedLocations(): Location[];
}

export interface IDashLocationCalculator {
	/**
	 * Calculate dash arrow locations with comprehensive special case handling.
	 */
	calculateDashLocationFromPictographData(
		pictographData: PictographData,
		isBlueArrow: boolean
	): Location;
	calculateDashLocation(
		motion: MotionData,
		otherMotion?: MotionData,
		letterType?: string,
		arrowColor?: ArrowColor,
		gridMode?: GridMode,
		shiftLocation?: Location,
		isPhiDash?: boolean,
		isPsiDash?: boolean,
		isLambda?: boolean,
		isLambdaDash?: boolean
	): Location;
}

export interface IArrowPositioningOrchestrator {
	/**
	 * Calculate complete arrow position using the positioning pipeline.
	 */
	calculateArrowPosition(
		arrowData: ArrowData,
		pictographData: PictographData,
		motionData?: MotionData
	): [number, number, number];

	/**
	 * Calculate positions for all arrows in the pictograph.
	 */
	calculateAllArrowPositions(pictographData: PictographData): PictographData;

	/**
	 * Determine if arrow should be mirrored based on motion type.
	 */
	shouldMirrorArrow(arrowData: ArrowData, pictographData?: PictographData): boolean;

	/**
	 * Apply mirror transformation to arrow graphics item.
	 */
	applyMirrorTransform(arrowItem: HTMLElement | SVGElement, shouldMirror: boolean): void;
}
