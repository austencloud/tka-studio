/**
 * Application Service Interfaces
 *
 * Interfaces for application-level services including settings, initialization,
 * and configuration management.
 */

import type { PropState } from "$lib/components/tabs/browse-tab/animator/types/PropState";
import type {
  MotionType as DomainMotionType,
  GridPosition,
  Location,
  Orientation,
  RotationDirection,
} from "$lib/domain";
import type { DifficultyLevel, GridMode, OptionFilters } from "./core-types";
import type {
  BeatData,
  MotionData,
  MotionType,
  PictographData,
  SequenceData,
  ValidationResult,
} from "./domain-types";

// BackgroundType is not exported from domain index, so import directly
import { BackgroundType } from "$lib/domain/background/BackgroundTypes";

// ============================================================================
// SHARED UTILITY SERVICES
// ============================================================================

/**
 * Service for centralized enum mapping utilities
 */
export interface IEnumMappingService {
  mapMotionType(motionType: string): DomainMotionType;
  mapLocation(location: string): Location;
  mapOrientation(orientation: string): Orientation;
  mapRotationDirection(rotationDirection: string): RotationDirection;
  convertToGridPosition(
    positionString: string | null | undefined
  ): GridPosition | null;
  normalizeMotionType(motionType: string): string;
  normalizeLocation(location: string): string;
  normalizeTurns(turns: number | string): number;
}

/**
 * Service for CSV parsing utilities
 */
export interface ICSVParserService {
  parseCSV(csvText: string): {
    headers: string[];
    rows: Array<Record<string, string>>;
    totalRows: number;
    successfulRows: number;
    errors: Array<{ rowIndex: number; error: string; rawRow: string }>;
  };
  parseCSVToRows(csvText: string): Array<Record<string, string>>;
  validateCSVStructure(csvText: string): { isValid: boolean; errors: string[] };
  createRowFromValues(
    headers: string[],
    values: string[]
  ): Record<string, string>;
}

/**
 * Service for CSV loading utilities
 */
export interface ICSVLoaderService {
  loadCSVFile(filename: string): Promise<{
    success: boolean;
    data?: string;
    error?: string;
    source: "fetch" | "window" | "cache";
  }>;
  loadCSVDataSet(): Promise<{
    success: boolean;
    data?: { diamondData: string; boxData: string };
    error?: string;
    sources: {
      diamond: "fetch" | "window" | "cache";
      box: "fetch" | "window" | "cache";
    };
  }>;
  loadCSVForGridMode(gridMode: GridMode): Promise<{
    success: boolean;
    data?: string;
    error?: string;
    source: "fetch" | "window" | "cache";
  }>;
  clearCache(): void;
  isDataCached(): boolean;
}

// ============================================================================
// APPLICATION SETTINGS
// ============================================================================

export interface AppSettings {
  theme: "light" | "dark";
  gridMode: GridMode;
  showBeatNumbers: boolean;
  autoSave: boolean;
  exportQuality: "low" | "medium" | "high";
  workbenchColumns: number;
  userName?: string;
  propType?: string;
  backupFrequency?: string;
  enableFades?: boolean;
  animationsEnabled?: boolean; // Simple animation control
  growSequence?: boolean;
  numBeats?: number;
  beatLayout?: string;
  // Background settings
  backgroundType?: BackgroundType;
  backgroundQuality?: "high" | "medium" | "low" | "minimal";
  backgroundEnabled?: boolean;
  visibility?: {
    TKA?: boolean;
    Reversals?: boolean;
    Positions?: boolean;
    Elemental?: boolean;
    VTG?: boolean;
    nonRadialPoints?: boolean;
  };
  imageExport?: {
    includeStartPosition?: boolean;
    addReversalSymbols?: boolean;
    addBeatNumbers?: boolean;
    addDifficultyLevel?: boolean;
    addWord?: boolean;
    addInfo?: boolean;
    addUserInfo?: boolean;
  };
  // Sequence Card Settings
  sequenceCard?: {
    defaultColumnCount?: number;
    defaultLayoutMode?: "grid" | "list" | "printable";
    enableTransparency?: boolean;
    cacheEnabled?: boolean;
    cacheSizeLimit?: number;
    exportQuality?: "low" | "medium" | "high";
    exportFormat?: "PNG" | "JPG" | "WebP";
    defaultPaperSize?: "A4" | "Letter" | "Legal" | "Tabloid";
  };
  // Developer Settings
  developerMode?: boolean;
}

// ============================================================================
// APPLICATION SERVICE INTERFACES
// ============================================================================

// IApplicationInitializationService moved to individual file: ./application/IApplicationInitializationService.ts

/**
 * Settings management service
 */
export interface ISettingsService {
  currentSettings: AppSettings;
  updateSetting<K extends keyof AppSettings>(
    key: K,
    value: AppSettings[K]
  ): Promise<void>;
  loadSettings(): Promise<void>;
}

// ============================================================================
// CONSTRUCT TAB COORDINATION SERVICE
// ============================================================================

/**
 * Service for coordinating construct tab operations
 */
export interface IConstructTabCoordinationService {
  setupComponentCoordination(components: Record<string, unknown>): void;
  handleSequenceModified(sequence: SequenceData): Promise<void>;
  handleStartPositionSet(startPosition: BeatData): Promise<void>;
  handleBeatAdded(beatData: BeatData): Promise<void>;
  handleGenerationRequest(config: Record<string, unknown>): Promise<void>;
  handleUITransitionRequest(targetPanel: string): Promise<void>;
}

// ============================================================================
// OPTION DATA SERVICE
// ============================================================================

/**
 * Service for managing motion options and compatibility
 */
export interface IOptionDataService {
  getNextOptions(
    currentSequence: SequenceData,
    filters?: OptionFilters
  ): Promise<PictographData[]>;
  filterOptionsByDifficulty(
    options: PictographData[],
    level: DifficultyLevel
  ): PictographData[];
  validateOptionCompatibility(
    option: PictographData,
    sequence: SequenceData
  ): ValidationResult;
  getAvailableMotionTypes(): MotionType[];
  convertCsvRowToPictographData(
    row: Record<string, string>,
    index: number
  ): PictographData | null;
}

// ============================================================================
// START POSITION SERVICE
// ============================================================================

/**
 * Service for managing sequence start positions
 */
export interface IStartPositionService {
  getAvailableStartPositions(
    propType: string,
    gridMode: GridMode
  ): Promise<BeatData[]>;
  setStartPosition(startPosition: BeatData): Promise<void>;
  validateStartPosition(position: BeatData): ValidationResult;
  getDefaultStartPositions(gridMode: GridMode): Promise<PictographData[]>;
}

// ============================================================================
// ANIMATOR INTERFACES (migrated from deleted animator-interfaces.ts)
// ============================================================================

/**
 * Animation engine for sequence playback
 */
export interface ISequenceAnimationEngine {
  initializeWithDomainData(sequenceData: SequenceData): boolean;
  calculateState(currentBeat: number): void;
  getCurrentPropStates(): PropStates;
  getBluePropState(): PropState;
  getRedPropState(): PropState;
  getMetadata(): SequenceMetadata;
  isInitialized(): boolean;
  dispose(): void;
  reset(): void;
}

/**
 * Animation orchestrator for coordinating multiple services
 */
export interface ISequenceAnimationOrchestrator {
  initializeWithDomainData(sequenceData: SequenceData): boolean;
  calculateState(currentBeat: number): void;
  getPropStates(): PropStates;
  getBluePropState(): PropState;
  getRedPropState(): PropState;
  getMetadata(): SequenceMetadata;
  getCurrentPropStates(): PropStates;
  isInitialized(): boolean;
  dispose(): void;
}

/**
 * Beat calculation service for timing
 */
export interface IBeatCalculationService {
  calculateBeatState(
    currentBeat: number,
    beats: readonly BeatData[],
    totalBeats: number
  ): BeatCalculationResult;
  validateBeats(beats: readonly BeatData[]): boolean;
  getBeatSafely(beats: readonly BeatData[], index: number): BeatData | null;
  calculateTotalDuration(beats: readonly BeatData[]): number;
  findBeatByNumber(
    beats: readonly BeatData[],
    beatNumber: number
  ): BeatData | null;
}

/**
 * Animation state management service
 */
export interface IAnimationStateService {
  getBluePropState(): PropState;
  getRedPropState(): PropState;
  getPropStates(): PropStates;
  updatePropStates(interpolationResult: InterpolationResult): PropStates;
  updateBluePropState(updates: Partial<PropState>): void;
  updateRedPropState(updates: Partial<PropState>): void;
  setPropStates(blue: PropState, red: PropState): void;
  resetPropStates(): void;
}

/**
 * Prop interpolation service for smooth transitions
 */
export interface IPropInterpolationService {
  interpolatePropAngles(
    currentBeatData: BeatData,
    beatProgress: number
  ): InterpolationResult;
  calculateInitialAngles(firstBeat: BeatData): InterpolationResult;
  getMotionData(beatData: BeatData): { blue: MotionData; red: MotionData };
  getEndpoints(beatData: BeatData): { blue: any; red: any };
}

/**
 * Animation control service
 */
export interface IAnimationControlService {
  play(): void;
  pause(): void;
  stop(): void;
  seek(position: number): void;
  setSpeed(speed: number): void;
}

// Type definitions for animator interfaces
export interface SequenceMetadata {
  word: string;
  author: string;
  totalBeats: number;
}

export interface PropStates {
  blue: PropState;
  red: PropState;
}

export interface InterpolationResult {
  blueAngles: {
    centerPathAngle: number;
    staffRotationAngle: number;
  };
  redAngles: {
    centerPathAngle: number;
    staffRotationAngle: number;
  };
  isValid: boolean;
}

export interface BeatCalculationResult {
  currentBeatIndex: number;
  beatProgress: number;
  currentBeatData: BeatData;
  isValid: boolean;
}

// ============================================================================
// MISSING SERVICE INTERFACES (from deleted legacy DI system)
// ============================================================================
// TODO: Add these interfaces back when needed

/**
 * Codex service interface
 */
export interface ICodexService {
  /**
   * Load all pictographs in alphabetical order
   */
  loadAllPictographs(): Promise<PictographData[]>;

  /**
   * Search pictographs by letter or pattern
   */
  searchPictographs(searchTerm: string): Promise<PictographData[]>;

  /**
   * Get a specific pictograph by letter
   */
  getPictographByLetter(letter: string): Promise<PictographData | null>;

  /**
   * Get pictographs for a specific lesson type
   */
  getPictographsForLesson(lessonType: string): Promise<PictographData[]>;

  /**
   * Get letters organized by rows for grid display (matches desktop layout)
   */
  getLettersByRow(): string[][];

  /**
   * Apply rotate operation to all pictographs
   */
  rotateAllPictographs(
    pictographs: PictographData[]
  ): Promise<PictographData[]>;

  /**
   * Apply mirror operation to all pictographs
   */
  mirrorAllPictographs(
    pictographs: PictographData[]
  ): Promise<PictographData[]>;

  /**
   * Apply color swap operation to all pictographs
   */
  colorSwapAllPictographs(
    pictographs: PictographData[]
  ): Promise<PictographData[]>;

  /**
   * Get all pictograph data organized by letter
   */
  getAllPictographData(): Promise<Record<string, PictographData | null>>;
}

// Additional interfaces will be added here as needed during the InversifyJS migration
