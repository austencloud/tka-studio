/**
 * Comprehensive Interface definitions for arrow positioning services.
 *
 * These interfaces define the contracts for the complete positioning services
 * that achieve functional parity with the reference Python implementation.
 *
 * Direct TypeScript mirror of reference/modern/core/interfaces/positioning_services.py
 */

import type { ArrowData, GridMode, Location, MotionData, PictographData } from '$lib/domain';
import type { LetterType } from '$lib/utils/letterTypeUtils';

// Enhanced type definitions with comprehensive coverage
export type { Location } from '$lib/domain';

export type MotionType = 'static' | 'pro' | 'anti' | 'dash' | 'float';
export type RotationDirection =
	| 'clockwise'
	| 'counter_clockwise'
	| 'no_rotation'
	| 'cw'
	| 'ccw'
	| 'none';
export type ArrowColor = 'blue' | 'red';

// Basic types
export interface Point {
	x: number;
	y: number;
}

export interface ArrowPosition extends Point {
	rotation: number;
}

export interface BeatData {
	beatNumber: number;
	letter?: string;
	pictographData: {
		motions?: {
			blue?: MotionData;
			red?: MotionData;
		};
	};
}

// Core positioning service interfaces

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
		letterType?: LetterType,
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

// Directional tuple processing interfaces

export interface IDirectionalTupleCalculator {
	calculateDirectionalTuple(motion: MotionData, location: Location): [number, number];
	generateDirectionalTuples(
		motion: MotionData,
		baseX: number,
		baseY: number
	): Array<[number, number]>;
}

export interface IQuadrantIndexCalculator {
	calculateQuadrantIndex(location: Location): number;
}

export interface IDirectionalTupleProcessor {
	processDirectionalTuples(baseAdjustment: Point, motion: MotionData, location: Location): Point;
}

// Placement service interfaces

export interface ISpecialPlacementService {
	getSpecialAdjustment(
		motionData: MotionData,
		pictographData: PictographData,
		arrowColor?: string
	): Point | null;
}

export interface IDefaultPlacementService {
	getDefaultAdjustment(
		placementKey: string,
		turns: number | string,
		motionType: MotionType,
		gridMode: GridMode
	): Promise<{ x: number; y: number }>;
	getAvailablePlacementKeys(motionType: MotionType, gridMode: GridMode): Promise<string[]>;
	isLoaded(): boolean;
	getPlacementData(
		motionType: MotionType,
		placementKey: string,
		gridMode: GridMode
	): Promise<{ [turns: string]: [number, number] }>;
	debugAvailableKeys(motionType: MotionType, gridMode: GridMode): Promise<void>;
}

// Adjustment lookup interfaces

export interface IArrowAdjustmentLookup {
	getBaseAdjustment(
		pictographData: PictographData,
		motionData: MotionData,
		letter: string,
		arrowColor?: string
	): Promise<Point>;
}

// Supporting service interfaces

export interface IPlacementKeyGenerator {
	generatePlacementKey(
		motionData: MotionData,
		pictographData: PictographData,
		defaultPlacements: Record<string, unknown>,
		gridMode?: string
	): string;
}

export interface IAttributeKeyGenerator {
	getKeyFromArrow(arrowData: ArrowData, pictographData: PictographData): string;
}

export interface ISpecialPlacementOriKeyGenerator {
	generateOrientationKey(motionData: MotionData, pictographData: PictographData): string;
}

export interface ITurnsTupleKeyGenerator {
	generateTurnsTuple(pictographData: PictographData): number[];
}

// Data service interfaces (existing)

export interface GridData {
	allHandPointsNormal: Record<Location, { coordinates: Point }>;
	allLayer2PointsNormal: Record<Location, { coordinates: Point }>;
}

export interface IArrowPlacementDataService {
	getDefaultAdjustment(
		motionType: MotionType,
		placementKey: string,
		turns: number | string,
		gridMode: GridMode
	): Promise<{ x: number; y: number }>;
	getAvailablePlacementKeys(motionType: MotionType, gridMode: GridMode): Promise<string[]>;
	isLoaded(): boolean;
	loadPlacementData(): Promise<void>;
}

export interface IArrowPlacementKeyService {
	generatePlacementKey(motionData: MotionData, letter: string): string;
}

export interface IArrowPositioningService {
	calculateArrowPosition(
		arrowData: ArrowData,
		pictographData: PictographData,
		gridData: GridData
	): Promise<ArrowPosition>;
	calculateAllArrowPositions(
		pictographData: PictographData,
		gridData: GridData
	): Promise<Map<string, ArrowPosition>>;
	calculateRotationAngle(motion: MotionData, location: Location, isMirrored: boolean): number;
	shouldMirrorArrow(motion: MotionData): boolean;
}

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
