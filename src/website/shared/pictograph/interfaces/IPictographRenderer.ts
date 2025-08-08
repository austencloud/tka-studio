/**
 * 🎨 ENTERPRISE PICTOGRAPH RENDERING INTERFACES
 *
 * Sophisticated service interfaces for pictograph rendering based on the modern desktop app architecture.
 * Provides clean separation of concerns and dependency injection compatibility.
 *
 * Source: src/desktop/modern/src/presentation/components/pictograph/
 */

// Import shared domain types from consolidated schemas
import type {
  PictographData,
  ArrowData,
  PropData,
  GridData,
  MotionData,
} from "@tka/domain";

// Import shared enums from consolidated schemas
import {
  GridMode,
  Location,
  Orientation,
  MotionType,
  PropType,
  LetterType,
  VTGMode,
} from "@tka/domain";

// ============================================================================
// CORE RENDERING INTERFACES
// ============================================================================

/**
 * Main pictograph renderer interface - orchestrates all rendering components
 */
export interface IPictographRenderer {
  /**
   * Render a complete pictograph from data
   */
  renderPictograph(data: PictographData): Promise<SVGElement>;

  /**
   * Update an existing pictograph with new data
   */
  updatePictograph(element: SVGElement, data: PictographData): Promise<void>;

  /**
   * Clear all rendered elements
   */
  clearPictograph(element: SVGElement): void;

  /**
   * Set renderer visibility options
   */
  setVisibility(options: RendererVisibilityOptions): void;
}

/**
 * Grid renderer interface for background grids
 */
export interface IGridRenderer {
  /**
   * Render grid background
   */
  renderGrid(gridData: GridData): Promise<SVGElement>;

  /**
   * Get grid points for positioning calculations
   */
  getGridPoints(gridData: GridData): GridPoint[];

  /**
   * Update grid mode (diamond/box)
   */
  updateGridMode(element: SVGElement, mode: GridMode): void;
}

/**
 * Arrow renderer interface for motion arrows
 */
export interface IArrowRenderer {
  /**
   * Render an arrow with positioning and rotation
   */
  renderArrow(arrowData: ArrowData): Promise<SVGElement>;

  /**
   * Calculate arrow position using positioning service
   */
  calculateArrowPosition(
    arrowData: ArrowData,
    pictographData?: PictographData
  ): ArrowPosition;

  /**
   * Apply color transformation to arrow SVG
   */
  applyColorTransformation(element: SVGElement, color: string): void;

  /**
   * Get appropriate arrow SVG asset path
   */
  getArrowAssetPath(motionData: MotionData): string;
}

/**
 * Prop renderer interface for prop elements
 */
export interface IPropRenderer {
  /**
   * Render a prop with positioning and rotation
   */
  renderProp(propData: PropData): Promise<SVGElement>;

  /**
   * Calculate prop position and rotation
   */
  calculatePropPosition(propData: PropData): PropPosition;

  /**
   * Apply prop color transformation
   */
  applyPropColor(element: SVGElement, color: string): void;

  /**
   * Get prop asset path based on prop type
   */
  getPropAssetPath(propType: PropType): string;
}

/**
 * Glyph renderer interface for letters and symbols
 */
export interface IGlyphRenderer {
  /**
   * Render TKA glyph (letter + dash + dots + numbers)
   */
  renderTKAGlyph(glyphData: TKAGlyphData): Promise<SVGElement>;

  /**
   * Render VTG glyph (SS, SO, TS, TO, QS, QO)
   */
  renderVTGGlyph(
    vtgMode: VTGMode,
    letterType?: LetterType
  ): Promise<SVGElement>;

  /**
   * Render elemental glyph
   */
  renderElementalGlyph(
    vtgMode: VTGMode,
    letterType?: LetterType
  ): Promise<SVGElement>;

  /**
   * Render position glyph (start/end positions)
   */
  renderPositionGlyph(
    startPos: string,
    endPos: string,
    letter: string
  ): Promise<SVGElement>;
}

// ============================================================================
// POSITIONING SERVICE INTERFACES
// ============================================================================

/**
 * Arrow positioning orchestrator interface
 */
export interface IArrowPositioningOrchestrator {
  /**
   * Calculate complete arrow position and rotation
   */
  calculateArrowPosition(
    color: string,
    motionData: MotionData,
    pictographData?: PictographData
  ): ArrowPosition;

  /**
   * Determine if arrow should be mirrored
   */
  shouldMirrorArrow(motionData: MotionData): boolean;

  /**
   * Apply beta positioning adjustments
   */
  applyBetaPositioning(
    position: ArrowPosition,
    motionData: MotionData
  ): ArrowPosition;
}

/**
 * Prop positioning service interface
 */
export interface IPropPositioningService {
  /**
   * Calculate prop position and rotation
   */
  calculatePropPosition(motionData: MotionData): PropPosition;

  /**
   * Calculate prop rotation angle
   */
  calculatePropRotation(
    motionData: MotionData,
    startOrientation: Orientation
  ): number;

  /**
   * Get hand point coordinates for prop placement
   */
  getHandPointCoordinates(location: Location): { x: number; y: number };
}

// ============================================================================
// ASSET MANAGEMENT INTERFACES
// ============================================================================

/**
 * SVG asset manager interface
 */
export interface ISVGAssetManager {
  /**
   * Load SVG asset from path
   */
  loadSVGAsset(path: string): Promise<SVGElement>;

  /**
   * Cache SVG asset for reuse
   */
  cacheSVGAsset(path: string, element: SVGElement): void;

  /**
   * Apply color transformation to SVG
   */
  applyColorTransformation(svg: string, color: string): string;

  /**
   * Get asset path for component type
   */
  getAssetPath(type: AssetType, identifier: string): string;
}

// ============================================================================
// DATA TYPES
// ============================================================================

export interface RendererVisibilityOptions {
  grid?: boolean;
  props?: boolean;
  arrows?: boolean;
  blueMotion?: boolean;
  redMotion?: boolean;
  elemental?: boolean;
  vtg?: boolean;
  tka?: boolean;
  positions?: boolean;
}

export interface GridPoint {
  x: number;
  y: number;
  location: Location;
}

export interface ArrowPosition {
  x: number;
  y: number;
  rotation: number;
  isMirrored?: boolean;
}

export interface PropPosition {
  x: number;
  y: number;
  rotation: number;
  handPointX: number;
  handPointY: number;
}

export interface TKAGlyphData {
  letter: string;
  letterType: LetterType;
  hasDash: boolean;
  turnsData?: string;
  showLetter?: boolean;
  showDash?: boolean;
  showDots?: boolean;
  showNumbers?: boolean;
}

// ============================================================================
// ENUMS
// ============================================================================

// AssetType is pictograph-specific, not in shared schemas
export enum AssetType {
  ARROW = "arrow",
  PROP = "prop",
  GRID = "grid",
  GLYPH = "glyph",
}

// ============================================================================
// PICTOGRAPH-SPECIFIC INTERFACES (Not in shared schemas)
// ============================================================================

// Note: MotionData, GridData, ArrowData, PropData, PictographData are now imported from @tka/domain
