/**
 * Positioning and Placement Service Interfaces
 *
 * Interfaces for arrow positioning, placement calculations, and coordinate systems.
 * This handles all spatial calculations and arrow placement logic.
 */

import type {
  ArrowPlacementData,
  MotionData,
  PictographData,
} from "./domain-types";
import type { GridMode } from "./core-types";
import type { MotionType } from "./domain-types";
import { MotionColor } from "../../domain/enums";
import type { Direction } from "../implementations/positioning/BetaPropDirectionCalculator";
import { GridPosition, Location } from "../../domain/enums";
import type { GridData } from "../../domain/GridData";

// Re-export types that are used by positioning services
export type { Location, MotionType };

// Note: IArrowPositioningOrchestrator is defined below in this file

// ============================================================================
// BASIC TYPES
// ============================================================================

/**
 * Basic point interface for coordinates
 */
export interface Point {
  x: number;
  y: number;
}

/**
 * Position interface for beta offset calculations
 */
export interface Position {
  x: number;
  y: number;
}

/**
 * Service interface for beta offset calculations
 * Converts direction values to pixel offsets for beta prop positioning
 */
export interface IBetaOffsetCalculator {
  /**
   * Calculate new position with offset based on direction
   */
  calculateNewPositionWithOffset(
    currentPosition: Position,
    direction: Direction
  ): Position;

  /**
   * Calculate beta separation offsets for both props
   * Returns offsets for blue and red props based on their calculated directions
   */
  calculateBetaSeparationOffsets(
    blueDirection: Direction | null,
    redDirection: Direction | null
  ): { blue: Position; red: Position };
}

// ============================================================================
// POSITION MAPPING SERVICE
// ============================================================================

/**
 * Position Mapping Service Interface
 *
 * Service for mapping between hand location combinations and grid positions.
 * A position represents the combination of (blue_hand_location, red_hand_location).
 */
export interface IPositionMapper {
  /**
   * Get the hand location pair for a given position
   */
  getLocationPair(position: GridPosition): [Location, Location];

  /**
   * Get the position for a given hand location pair
   */
  getPositionFromLocations(
    blueLocation: Location,
    redLocation: Location
  ): GridPosition;
}

// ============================================================================
// ARROW POSITIONING SERVICE
// ============================================================================

/**
 * Service interface for arrow positioning (thin wrapper around orchestrator)
 */
export interface IArrowPositioningService {
  calculatePosition(
    arrowData: ArrowPlacementData,
    motionData: MotionData,
    pictographData: PictographData
  ): Promise<{ x: number; y: number; rotation: number }>;
  shouldMirror(
    arrowData: ArrowPlacementData,
    motionData: MotionData,
    pictographData: PictographData
  ): boolean;
}

/**
 * Service interface for arrow location calculation
 */
export interface IArrowLocationService {
  calculateArrowLocation(input: {
    startLocation: string;
    endLocation: string;
    motionType: string;
  }): string;
}

// Note: IArrowPositioningOrchestrator provides the complete positioning pipeline

// ============================================================================
// ARROW PLACEMENT DATA SERVICE
// ============================================================================

/**
 * Service for managing arrow placement data and adjustments
 */
export interface IArrowPlacementService {
  getDefaultAdjustment(
    motionType: MotionType,
    placementKey: string,
    turns: number | string,
    gridMode: GridMode
  ): Promise<{ x: number; y: number }>;

  getAvailablePlacementKeys(
    motionType: MotionType,
    gridMode: GridMode
  ): Promise<string[]>;

  isLoaded(): boolean;
  loadPlacementData(): Promise<void>;
}

// ============================================================================
// ARROW PLACEMENT KEY SERVICE
// ============================================================================

/**
 * Service for generating and managing placement keys
 */
export interface IArrowPlacementKeyService {
  generatePlacementKey(
    motionData: MotionData,
    pictographData: PictographData,
    availableKeys: string[]
  ): string;

  generateBasicKey(motionType: MotionType): string;
}

// ============================================================================
// PROP RENDERING SERVICE
// ============================================================================

/**
 * Service for rendering and positioning props
 */
export interface IPropRenderingService {
  renderProp(
    propType: string,
    color: MotionColor,
    motionData: MotionData,
    gridMode: GridMode
  ): Promise<SVGElement>;

  calculatePropPosition(
    motionData: MotionData,
    color: MotionColor,
    gridMode: GridMode
  ): Promise<{ x: number; y: number; rotation: number }>;

  loadPropSVG(propType: string, color: MotionColor): Promise<string>;

  getSupportedPropTypes(): string[];
}

// ============================================================================
// ARROW RENDERING INTERFACES
// ============================================================================

/**
 * Arrow Path Resolution Service Interface
 *
 * Responsible for determining the correct SVG file path based on motion data.
 */
export interface IArrowPathResolutionService {
  /**
   * Get arrow SVG path based on motion type and properties
   */
  getArrowPath(
    arrowData: ArrowPlacementData,
    motionData: MotionData
  ): string | null;

  /**
   * Get the correct arrow SVG path based on motion data (optimized version)
   */
  getArrowSvgPath(motionData: MotionData | undefined): string;
}

// Note: IArrowPositioningService is defined above with calculatePosition and shouldMirror methods

// ============================================================================
// CORE POSITIONING SERVICES (from core-services.ts)
// ============================================================================

/**
 * Arrow Location Calculator Interface
 */
export interface IArrowLocationCalculator {
  /**
   * Calculate the arrow location based on motion type and data.
   */
  calculateLocation(
    motion: MotionData,
    pictographData?: PictographData
  ): Location;
  getSupportedMotionTypes(): MotionType[];
  validateMotionData(motion: MotionData): boolean;
  isBlueArrowMotion(
    motion: MotionData,
    pictographData: PictographData
  ): boolean;
}

/**
 * Arrow Rotation Calculator Interface
 */
export interface IArrowRotationCalculator {
  /**
   * Calculate the arrow rotation angle based on motion type and location.
   */
  calculateRotation(motion: MotionData, location: Location): number;
  getSupportedMotionTypes(): MotionType[];
  validateMotionData(motion: MotionData): boolean;
}

/**
 * Arrow Adjustment Calculator Interface
 */
export interface IArrowAdjustmentCalculator {
  /**
   * Calculate position adjustment for arrow based on placement rules.
   */
  calculateAdjustment(
    pictographData: PictographData,
    motionData: MotionData,
    location: Location,
    arrowColor?: string
  ): Promise<Point>;
}

/**
 * Arrow Coordinate System Service Interface
 */
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

/**
 * Dash Location Calculator Interface
 */
export interface IDashLocationCalculator {
  /**
   * Calculate dash arrow locations with comprehensive special case handling.
   */
  calculateDashLocationFromPictographData(
    pictographData: PictographData,
    motionData: MotionData,
    arrowColor: string
  ): Location;
  calculateDashLocation(
    letter: string,
    startLocation: Location,
    endLocation: Location,
    motionType: MotionType,
    isLambda?: boolean,
    isLambdaDash?: boolean
  ): Location;
}

/**
 * Arrow Positioning Orchestrator Interface
 */
export interface IArrowPositioningOrchestrator {
  /**
   * Calculate complete arrow position using the positioning pipeline.
   */
  calculateArrowPosition(
    pictographData: PictographData,
    motionData?: MotionData
  ): Promise<[number, number, number]>;

  /**
   * Calculate positions for all arrows in the pictograph.
   */
  calculateAllArrowPositions(
    pictographData: PictographData
  ): Promise<PictographData>;

  /**
   * Determine if arrow should be mirrored based on motion type.
   */
  shouldMirrorArrow(
    arrowData: ArrowPlacementData,
    pictographData?: PictographData,
    motionData?: MotionData
  ): boolean;

  /**
   * Apply mirror transformation to arrow graphics item.
   */
  applyMirrorTransform(
    arrowItem: HTMLElement | SVGElement,
    shouldMirror: boolean
  ): void;
}

// ============================================================================
// DATA PROCESSING SERVICES (from data-services.ts)
// ============================================================================

/**
 * Directional Tuple Calculator Interface
 */
export interface IDirectionalTupleCalculator {
  calculateDirectionalTuple(
    motion: MotionData,
    location: Location
  ): [number, number];
  generateDirectionalTuples(
    motion: MotionData,
    baseX: number,
    baseY: number
  ): Array<[number, number]>;
}

/**
 * Quadrant Index Calculator Interface
 */
export interface IQuadrantIndexCalculator {
  calculateQuadrantIndex(motion: MotionData, location: Location): number;
}

/**
 * Directional Tuple Processor Interface
 */
export interface IDirectionalTupleProcessor {
  processDirectionalTuples(
    baseAdjustment: Point,
    motion: MotionData,
    location: Location
  ): Point;
}

/**
 * Placement Key Generator Interface
 */
export interface IPlacementKeyGenerator {
  generatePlacementKey(
    motionData: MotionData,
    pictographData: PictographData,
    defaultPlacements: Record<string, unknown>,
    gridMode?: string
  ): string;
}

/**
 * Attribute Key Generator Interface
 */
export interface IAttributeKeyGenerator {
  getKeyFromArrow(
    arrowData: ArrowPlacementData,
    pictographData: PictographData,
    color: string
  ): string;
}

/**
 * Special Placement Orientation Key Generator Interface
 */
export interface ISpecialPlacementOriKeyGenerator {
  generateOrientationKey(
    motionData: MotionData,
    pictographData: PictographData
  ): string;
}

/**
 * Turns Tuple Key Generator Interface
 */
export interface ITurnsTupleKeyGenerator {
  generateTurnsTuple(pictographData: PictographData): number[];
}

/**
 * Arrow Placement Key Service Interface
 */
export interface IArrowPlacementKeyService {
  generatePlacementKey(motionData: MotionData, letter: string): string;
}

// ============================================================================
// PLACEMENT SERVICES (from placement-services.ts)
// ============================================================================

/**
 * Special Placement Service Interface
 */
export interface ISpecialPlacementService {
  getSpecialAdjustment(
    motionData: MotionData,
    pictographData: PictographData,
    arrowColor?: string
  ): Promise<Point | null>;
}

/**
 * Default Placement Service Interface
 */
export interface IDefaultPlacementService {
  getDefaultAdjustment(
    placementKey: string,
    turns: number | string,
    motionType: MotionType,
    gridMode: GridMode
  ): Promise<{ x: number; y: number }>;
  getAvailablePlacementKeys(
    motionType: MotionType,
    gridMode: GridMode
  ): Promise<string[]>;
  isLoaded(): boolean;
  getPlacementData(
    motionType: MotionType,
    placementKey: string,
    gridMode: GridMode
  ): Promise<{ [turns: string]: [number, number] }>;
  debugAvailableKeys(motionType: MotionType, gridMode: GridMode): Promise<void>;
}

/**
 * Default Placement Service JSON Interface (mirrors Python implementation)
 */
export interface IDefaultPlacementServiceJson {
  getDefaultAdjustment(
    placementKey: string,
    turns: number | string,
    motionType: MotionType,
    gridMode: GridMode
  ): Promise<{ x: number; y: number }>;
  getAvailablePlacementKeys(
    motionType: MotionType,
    gridMode: GridMode
  ): Promise<string[]>;
  isLoaded(): boolean;
  getPlacementData(
    motionType: MotionType,
    placementKey: string,
    gridMode: GridMode
  ): Promise<{ [turns: string]: [number, number] }>;
  debugAvailableKeys(motionType: MotionType, gridMode: GridMode): Promise<void>;
}

/**
 * Arrow Adjustment Lookup Interface
 */
export interface IArrowAdjustmentLookup {
  getBaseAdjustment(
    pictographData: PictographData,
    motionData: MotionData,
    letter: string,
    arrowColor?: string
  ): Promise<Point>;
}

// ============================================================================
// GRID MODE DERIVATION
// ============================================================================

/**
 * Grid Mode Deriver Interface - Interface for grid mode determination
 */
export interface IGridModeDeriver {
  /**
   * Determine grid mode from motion start/end locations
   * Cardinal locations (N, E, S, W) = DIAMOND mode
   * Intercardinal locations (NE, SE, SW, NW) = BOX mode
   */
  deriveGridMode(blueMotion: MotionData, redMotion: MotionData): GridMode;

  /**
   * Check if motion uses cardinal locations
   */
  usesDiamondLocations(motion: MotionData): boolean;

  /**
   * Check if motion uses intercardinal locations
   */
  usesBoxLocations(motion: MotionData): boolean;

  /**
   * Compute complete GridData from motion data
   * Uses deriveGridMode logic and creates GridData with default positioning
   */
  computeGridData(blueMotion: MotionData, redMotion: MotionData): GridData;
}
