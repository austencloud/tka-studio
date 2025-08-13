/**
 * Core type definitions for the Pictograph Animator
 *
 * PHASE 1 REFACTORING: Native Compatibility with Web App Data Structures
 * This file now supports both legacy array format and modern web app object format
 */

// ============================================================================
// PHASE 1: WEB APP COMPATIBLE TYPE DEFINITIONS
// These types match the web app's domain models for native compatibility
// ============================================================================

/**
 * Web app compatible MotionData interface
 * Matches src/web/web_app/src/lib/domain/MotionData.ts
 */
export interface WebAppMotionData {
  readonly motion_type: string;
  readonly prop_rot_dir: string;
  readonly start_loc: string;
  readonly end_loc: string;
  readonly turns: number | "fl";
  readonly start_ori: string;
  readonly end_ori: string;
  readonly is_visible: boolean;
  readonly metadata: Record<string, unknown>;
}

/**
 * Web app compatible PictographData interface
 * Matches src/web/web_app/src/lib/domain/PictographData.ts
 */
export interface WebAppPictographData {
  readonly id: string;
  readonly grid_data: any;
  readonly arrows: readonly any[];
  readonly props: readonly any[];
  readonly motions: {
    readonly blue: WebAppMotionData;
    readonly red: WebAppMotionData;
  };
  readonly letter: string;
  readonly metadata: Record<string, unknown>;
}

/**
 * Web app compatible BeatData interface
 * Matches src/web/web_app/src/lib/domain/BeatData.ts
 */
export interface WebAppBeatData {
  readonly id: string;
  readonly beat_number: number;
  readonly duration: number;
  readonly blue_reversal: boolean;
  readonly red_reversal: boolean;
  readonly is_blank: boolean;
  readonly pictograph_data?: WebAppPictographData;
  readonly metadata: Record<string, unknown>;
}

/**
 * Web app compatible SequenceData interface
 * Matches src/web/web_app/src/lib/domain/SequenceData.ts
 */
export interface WebAppSequenceData {
  readonly id: string;
  readonly name: string;
  readonly word: string;
  readonly beats: readonly WebAppBeatData[];
  readonly start_position?: WebAppBeatData;
  readonly thumbnails?: readonly string[];
  readonly sequence_length?: number;
  readonly author?: string;
  readonly level?: number;
  readonly date_added?: Date;
  readonly grid_mode?: string;
  readonly prop_type?: string;
  readonly is_favorite?: boolean;
  readonly is_circular?: boolean;
  readonly starting_position?: string;
  readonly difficulty_level?: string;
  readonly tags?: readonly string[];
  readonly metadata: Record<string, unknown>;
}

export type MotionType = "pro" | "anti" | "static" | "dash" | "fl" | "none";
export type PropRotDir = "cw" | "ccw" | "no_rot" | undefined;
export type Orientation = "in" | "out" | "clock" | "counter" | undefined;

export interface PropAttributes {
  start_loc: string;
  end_loc: string;
  start_ori?: Orientation;
  end_ori?: Orientation;
  prop_rot_dir?: PropRotDir;
  turns?: number;
  motion_type: MotionType;
  // Manual rotation override fields (in radians)
  manual_start_rotation?: number;
  manual_end_rotation?: number;
  manual_rotation_direction?: "cw" | "ccw" | "shortest";
}

export interface SequenceStep {
  beat: number;
  letter?: string;
  start_pos?: string;
  end_pos?: string;
  blue_attributes: PropAttributes;
  red_attributes: PropAttributes;
  [key: string]: unknown;
}

export interface SequenceMeta {
  word?: string;
  author?: string;
  level?: number;
  prop_type?: string;
  grid_mode?: string;
  [key: string]: unknown;
}

export type SequenceData = [SequenceMeta, ...SequenceStep[]];

// ============================================================================
// PHASE 1: UNIFIED DATA STRUCTURES FOR NATIVE COMPATIBILITY
// ============================================================================

/**
 * Unified sequence data interface that supports both legacy array format
 * and modern web app object format for seamless integration
 */
export interface UnifiedSequenceData {
  // Web app format (primary) - object-based structure
  id: string;
  name: string;
  word: string;
  beats: readonly WebAppBeatData[];
  start_position?: WebAppBeatData;
  thumbnails?: readonly string[];
  sequence_length?: number;
  author?: string;
  level?: number;
  date_added?: Date;
  grid_mode?: string;
  prop_type?: string;
  is_favorite?: boolean;
  is_circular?: boolean;
  starting_position?: string;
  difficulty_level?: string;
  tags?: readonly string[];
  metadata: Record<string, unknown>;

  // Legacy support (during transition) - array-based structure
  legacy?: SequenceData;
}

/**
 * Type union for accepting both formats during transition
 */
export type AnySequenceData =
  | UnifiedSequenceData
  | SequenceData
  | WebAppSequenceData;

/**
 * Motion data extraction result from web app beat data
 */
export interface ExtractedMotionData {
  blue: PropAttributes;
  red: PropAttributes;
  hasMotionData: boolean;
  source: "pictograph_data" | "legacy" | "default";
}

export interface PropState {
  centerPathAngle: number;
  staffRotationAngle: number;
  x: number;
  y: number;
}

export interface DictionaryItem {
  id: string;
  name: string;
  filePath: string;
  metadata: SequenceMeta;
  sequenceData: SequenceData;
  thumbnailUrl?: string;
  versions: string[];
}

export interface DictionaryIndex {
  items: DictionaryItem[];
  categories: string[];
  totalCount: number;
  lastUpdated: Date;
}

// ============================================================================
// PHASE 1: MOTION DATA EXTRACTION UTILITIES
// ============================================================================

/**
 * Extract motion data from web app beat structure
 * Converts nested PictographData.motions to PropAttributes format
 */
export function extractMotionData(beat: WebAppBeatData): ExtractedMotionData {
  // Check if beat has pictograph data with motions
  if (beat.pictograph_data?.motions) {
    const motions = beat.pictograph_data.motions;

    return {
      blue: convertMotionDataToPropAttributes(motions.blue),
      red: convertMotionDataToPropAttributes(motions.red),
      hasMotionData: true,
      source: "pictograph_data",
    };
  }

  // Fallback to default motion data
  return {
    blue: createDefaultPropAttributes(),
    red: createDefaultPropAttributes(),
    hasMotionData: false,
    source: "default",
  };
}

/**
 * Convert web app MotionData to animator PropAttributes
 */
export function convertMotionDataToPropAttributes(
  motionData: WebAppMotionData,
): PropAttributes {
  return {
    start_loc: String(motionData.start_loc),
    end_loc: String(motionData.end_loc),
    start_ori: String(motionData.start_ori) as Orientation,
    end_ori: String(motionData.end_ori) as Orientation,
    prop_rot_dir: String(motionData.prop_rot_dir) as PropRotDir,
    turns: typeof motionData.turns === "number" ? motionData.turns : 0,
    motion_type: String(motionData.motion_type) as MotionType,
  };
}

/**
 * Create default prop attributes for missing motion data
 */
export function createDefaultPropAttributes(): PropAttributes {
  return {
    start_loc: "center",
    end_loc: "center",
    start_ori: "in",
    end_ori: "in",
    prop_rot_dir: "no_rot",
    turns: 0,
    motion_type: "static",
  };
}

// ============================================================================
// PHASE 1: BACKWARD COMPATIBILITY ADAPTERS
// ============================================================================

/**
 * Adapt any sequence data format to unified format
 * Handles both legacy array format and modern web app object format
 */
export function adaptSequenceData(data: AnySequenceData): UnifiedSequenceData {
  // Check if it's already in unified format
  if (isUnifiedSequenceData(data)) {
    return data;
  }

  // Check if it's legacy array format
  if (Array.isArray(data)) {
    return convertLegacyToUnified(data);
  }

  // Check if it's web app format
  if (isWebAppSequenceData(data)) {
    return convertWebAppToUnified(data);
  }

  throw new Error("Unknown sequence data format");
}

/**
 * Type guard for unified sequence data
 */
export function isUnifiedSequenceData(
  data: unknown,
): data is UnifiedSequenceData {
  return (
    data !== null &&
    data !== undefined &&
    typeof data === "object" &&
    "beats" in data &&
    "id" in data &&
    "word" in data &&
    "metadata" in data
  );
}

/**
 * Type guard for web app sequence data
 */
export function isWebAppSequenceData(
  data: unknown,
): data is WebAppSequenceData {
  return (
    data !== null &&
    data !== undefined &&
    typeof data === "object" &&
    "beats" in data &&
    "id" in data &&
    "word" in data &&
    !("legacy" in data)
  );
}

/**
 * Type guard for legacy array format
 */
export function isLegacySequenceData(data: unknown): data is SequenceData {
  return Array.isArray(data) && data.length >= 2;
}

/**
 * Convert legacy array format to unified format
 */
export function convertLegacyToUnified(
  legacyData: SequenceData,
): UnifiedSequenceData {
  const [meta, ...steps] = legacyData;

  // Convert legacy steps to web app beat format
  const beats: WebAppBeatData[] = steps.map((step, index) => ({
    id: `beat-${index + 1}`,
    beat_number: step.beat || index + 1,
    duration: 1, // Default duration
    blue_reversal: false,
    red_reversal: false,
    is_blank: false,
    pictograph_data: {
      id: `pictograph-${index + 1}`,
      grid_data: null,
      arrows: [],
      props: [],
      motions: {
        blue: convertPropAttributesToMotionData(step.blue_attributes),
        red: convertPropAttributesToMotionData(step.red_attributes),
      },
      letter: step.letter || "",
      metadata: {},
    },
    metadata: {},
  }));

  return {
    id: (meta.id as string) || `legacy-${Date.now()}`,
    name: meta.word || "Legacy Sequence",
    word: meta.word || "",
    beats,
    metadata: {
      author: meta.author,
      level: meta.level,
      grid_mode: meta.grid_mode,
      ...meta,
    },
    legacy: legacyData,
  };
}

/**
 * Convert web app format to unified format
 */
export function convertWebAppToUnified(
  webAppData: WebAppSequenceData,
): UnifiedSequenceData {
  return {
    ...webAppData,
    // Ensure all required fields are present
    metadata: webAppData.metadata || {},
  };
}

/**
 * Convert animator PropAttributes to web app MotionData format
 * Used when converting legacy data to web app format
 */
export function convertPropAttributesToMotionData(
  propAttrs: PropAttributes,
): WebAppMotionData {
  return {
    motion_type: propAttrs.motion_type,
    prop_rot_dir: propAttrs.prop_rot_dir || "no_rot",
    start_loc: propAttrs.start_loc,
    end_loc: propAttrs.end_loc,
    turns: propAttrs.turns || 0,
    start_ori: propAttrs.start_ori || "in",
    end_ori: propAttrs.end_ori || "in",
    is_visible: true,
    metadata: {},
  };
}

// ============================================================================
// PHASE 1: SEQUENCE STEP EXTRACTION UTILITIES
// ============================================================================

/**
 * Extract sequence steps from unified sequence data
 * Converts web app beats back to animator step format for engine compatibility
 */
export function extractStepsFromUnified(
  data: UnifiedSequenceData,
): SequenceStep[] {
  return data.beats.map((beat) => {
    const motionData = extractMotionData(beat);
    return {
      beat: beat.beat_number,
      letter: beat.pictograph_data?.letter || "",
      blue_attributes: motionData.blue,
      red_attributes: motionData.red,
    };
  });
}

/**
 * Extract sequence metadata from unified sequence data
 */
export function extractMetaFromUnified(
  data: UnifiedSequenceData,
): SequenceMeta {
  return {
    id: data.id,
    word: data.word,
    author: (data.metadata.author as string) || "",
    level: (data.metadata.level as number) || 1,
    grid_mode: (data.metadata.grid_mode as string) || "grid",
    ...data.metadata,
  };
}
