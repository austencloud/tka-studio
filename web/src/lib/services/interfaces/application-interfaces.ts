/**
 * Application Service Interfaces
 *
 * Interfaces for application-level services including settings, initialization,
 * and configuration management.
 */

import type {
  BeatData,
  SequenceData,
  PictographData,
  ValidationResult,
} from "./domain-types";
import type { GridMode, DifficultyLevel, OptionFilters } from "./core-types";
import type { MotionType } from "./domain-types";
import { BackgroundType } from "$lib/components/backgrounds/types/types";
import type {
  MotionType as DomainMotionType,
  Location,
  Orientation,
  RotationDirection,
  GridPosition,
} from "$lib/domain/enums";

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

/**
 * Application initialization and startup service
 */
export interface IApplicationInitializationService {
  initialize(): Promise<void>;
}

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
