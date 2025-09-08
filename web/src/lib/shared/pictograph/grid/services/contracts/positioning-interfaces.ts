/**
 * Pointing Service Interfaces
 *
 * Interfaces for arrow pointing, placement calculations, and coordinate systems.
 * This handles all spatial calculations and arrow placement logic.
 */
// Re-export types that are used by positioning services
// Note: IArrowPositioningOrchestrator is defined below in this file
// ============================================================================
// BASIC TYPES
// ============================================================================

// Import spatial Direction type from BetaPropDirectionCalculator (not domain Direction enum)
import type {
  GridData,
  GridLocation,
  GridMode,
  GridPosition,
  MotionColor,
  MotionData,
  MotionType,
  PictographCoordinate,
  PictographData,
  PropPlacementData,
} from "$shared";
import type { ArrowPlacementData } from "../../../arrow";
import type { VectorDirection } from "../../../prop";

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface IBetaOffsetCalculator {
  /**
   * Calculate new position with offset based on direction
   */
  calculateNewPointWithOffset(
    currentPoint: PictographCoordinate,
    direction: VectorDirection
  ): PictographCoordinate;

  /**
   * Calculate beta separation offsets for both props
   * Returns offsets for blue and red props based on their calculated directions
   */
  calculateBetaSeparationOffsets(
    blueDirection: VectorDirection | null,
    redDirection: VectorDirection | null
  ): { blue: PictographCoordinate; red: PictographCoordinate };
}

export interface IGridPositionDeriver {
  /**
   * Get the hand location pair for a given position
   */
  getGridLocationsFromPosition(
    position: GridPosition
  ): [GridLocation, GridLocation];

  /**
   * Get the position for a given hand location pair
   */
  getGridPositionFromLocations(
    blueLocation: GridLocation,
    redLocation: GridLocation
  ): GridPosition;
}

export interface IArrowPointCalculator {
  calculatePoint(
    arrowData: ArrowPlacementData,
    motionData: MotionData,
    pictographData: PictographData
  ): Promise<{ x: number; y: number; rotation: number }>;
  shouldMirror(
    arrowData: ArrowPlacementData,
    motionData: MotionData,
    pictographData: PictographData
  ): boolean;
  renderArrowAtPoint(
    svg: SVGElement,
    arrowPoint: { x: number; y: number; rotation: number },
    motionData: MotionData
  ): Promise<void>;
}

export interface IArrowLocationService {
  calculateArrowLocation(input: {
    startLocation: string;
    endLocation: string;
    motionType: string;
  }): string;
}

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

export interface IPropPlacementService {
  calculatePlacement(
    pictographData: PictographData,
    motionData: MotionData
  ): Promise<PropPlacementData>;
}

export interface IArrowPlacementKeyService {
  generatePlacementKey(
    motionData: MotionData,
    pictographData: PictographData,
    availableKeys: string[]
  ): string;

  generateBasicKey(motionType: MotionType): string;
}

export interface IPropRenderingService {
  renderProp(
    propType: string,
    color: MotionColor,
    motionData: MotionData,
    gridMode: GridMode
  ): Promise<SVGElement>;

  calculatePropPoint(
    motionData: MotionData,
    color: MotionColor,
    gridMode: GridMode
  ): Promise<{ x: number; y: number; rotation: number }>;

  loadPropSVG(propType: string, color: MotionColor): Promise<string>;

  getSupportedPropTypes(): string[];
}

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

export interface IArrowLocationCalculator {
  /**
   * Calculate the arrow location based on motion type and data.
   */
  calculateLocation(
    motion: MotionData,
    pictographData?: PictographData
  ): GridLocation;
  getSupportedMotionTypes(): MotionType[];
  validateMotionData(motion: MotionData): boolean;
  isBlueArrowMotion(
    motion: MotionData,
    pictographData: PictographData
  ): boolean;
}

export interface IArrowRotationCalculator {
  /**
   * Calculate the arrow rotation angle based on motion type and location.
   */
  calculateRotation(motion: MotionData, location: GridLocation): number;
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
    location: GridLocation,
    arrowColor?: string
  ): Promise<PictographCoordinate>;
}

export interface IArrowCoordinateSystemService {
  /**
   * Get initial position coordinates based on motion type and location.
   */
  getInitialPoint(motion: MotionData, location: GridLocation): PictographCoordinate;
  getSceneCenter(): PictographCoordinate;
  getSceneDimensions(): [number, number];
  getCoordinateInfo(location: GridLocation): Record<string, unknown>;
  validateCoordinates(point: PictographCoordinate): boolean;
  getAllHandPoints(): Record<GridLocation, PictographCoordinate>;
  getAllLayer2Points(): Record<GridLocation, PictographCoordinate>;
  getSupportedLocations(): GridLocation[];
}

export interface IDashLocationCalculator {
  /**
   * Calculate dash arrow locations with comprehensive special case handling.
   */
  calculateDashLocationFromPictographData(
    pictographData: PictographData,
    motionData: MotionData,
    arrowColor: string
  ): GridLocation;
  calculateDashLocation(
    letter: string,
    startLocation: GridLocation,
    endLocation: GridLocation,
    motionType: MotionType,
    isLambda?: boolean,
    isLambdaDash?: boolean
  ): GridLocation;
}

export interface IArrowPositioningOrchestrator {
  /**
   * Calculate complete arrow position using the positioning pipeline.
   */
  calculateArrowPoint(
    pictographData: PictographData,
    motionData?: MotionData
  ): Promise<[number, number, number]>;

  /**
   * Calculate positions for all arrows in the pictograph.
   */
  calculateAllArrowPoints(
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

export interface IDirectionalTupleCalculator {
  calculateDirectionalTuple(
    motion: MotionData,
    location: GridLocation
  ): [number, number];
  generateDirectionalTuples(
    motion: MotionData,
    baseX: number,
    baseY: number
  ): Array<[number, number]>;
}

export interface IQuadrantIndexCalculator {
  calculateQuadrantIndex(motion: MotionData, location: GridLocation): number;
}

export interface IDirectionalTupleProcessor {
  processDirectionalTuples(
    baseAdjustment: PictographCoordinate,
    motion: MotionData,
    location: GridLocation
  ): PictographCoordinate;
}

export interface IPlacementKeyGenerator {
  generatePlacementKey(
    motionData: MotionData,
    pictographData: PictographData,
    defaultPlacements: Record<string, unknown>,
    gridMode?: string
  ): string;
}

export interface IAttributeKeyGenerator {
  getKeyFromArrow(
    arrowData: ArrowPlacementData,
    pictographData: PictographData,
    color: string
  ): string;
}

export interface ISpecialPlacementOriKeyGenerator {
  generateOrientationKey(
    motionData: MotionData,
    pictographData: PictographData
  ): string;
}

export interface ITurnsTupleKeyGenerator {
  generateTurnsTuple(pictographData: PictographData): number[];
}

export interface IArrowPlacementKeyService {
  generatePlacementKey(motionData: MotionData, letter: string): string;
}

export interface ISpecialPlacementService {
  getSpecialAdjustment(
    motionData: MotionData,
    pictographData: PictographData,
    arrowColor?: string
  ): Promise<PictographCoordinate | null>;
}

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

export interface IArrowAdjustmentLookup {
  getBaseAdjustment(
    pictographData: PictographData,
    motionData: MotionData,
    letter: string,
    arrowColor?: string
  ): Promise<PictographCoordinate>;
}

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
