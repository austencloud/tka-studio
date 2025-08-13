/**
 * Sequence Card Domain Types
 *
 * Type definitions for sequence card functionality including layout,
 * export options, device capabilities, and cache management.
 */

import type { SequenceData } from "./index";

// ============================================================================
// LAYOUT CONFIGURATION TYPES
// ============================================================================

export interface LayoutConfig {
  columns: number;
  rows: number;
  cardWidth: number;
  cardHeight: number;
  totalWidth: number;
  totalHeight: number;
  spacing: number;
  canFitInContainer: boolean;
  utilization: number; // 0-1 representing how well the layout uses available space
}

export interface GridConfig {
  columns: number;
  rows: number;
  gap: number;
  containerWidth: number;
  containerHeight: number;
}

export interface ResponsiveBreakpoints {
  mobile: number;
  tablet: number;
  desktop: number;
  largeDesktop: number;
}

// ============================================================================
// EXPORT OPTIONS & SETTINGS
// ============================================================================

export interface ExportOptions {
  // Image settings
  quality: "low" | "medium" | "high";
  format: "PNG" | "JPG" | "WebP";
  resolution: "150" | "300" | "600"; // DPI

  // Dimensions
  width?: number;
  height?: number;
  maxDimension?: number;

  // Content options
  includeTitle: boolean;
  includeMetadata: boolean;
  includeBeatNumbers: boolean;
  includeAuthor: boolean;
  includeDifficulty: boolean;
  includeDate: boolean;
  includeStartPosition: boolean;
  includeReversalSymbols: boolean;

  // Layout options
  beatSize: number;
  spacing: number;
  padding: number;
  backgroundColor?: string;

  // Compression settings
  pngCompression: number; // 0-9, lower is better quality
  jpgQuality: number; // 1-100, higher is better quality
}

export interface SequenceCardExportSettings {
  // Export format
  format: "individual" | "batch" | "page" | "pdf";

  // Target sequences
  sequences: SequenceData[];
  exportAll: boolean;
  lengthFilter?: number;

  // Output settings
  outputDirectory?: string;
  filenamePattern: string; // Template for generated filenames

  // Progress tracking
  enableProgressReporting: boolean;
  batchSize: number;

  // Memory management
  enableMemoryOptimization: boolean;
  maxMemoryUsage: number; // MB
  cleanupBetweenBatches: boolean;
}

export interface PrintLayoutOptions {
  paperSize: PaperSize;
  orientation: "Portrait" | "Landscape";
  margins: {
    top: number;
    right: number;
    bottom: number;
    left: number;
  };

  // Layout settings
  cardsPerPage: number;
  cardSpacing: number;
  pageSpacing: number;

  // Content options
  includePageNumbers: boolean;
  includeHeader: boolean;
  includeFooter: boolean;
  headerText?: string;
  footerText?: string;
}

export type PaperSize = "A4" | "Letter" | "Legal" | "Tabloid";

// ============================================================================
// DEVICE CAPABILITIES & RESPONSIVENESS
// ============================================================================

export interface DeviceCapabilities {
  // Primary input method
  primaryInput: "touch" | "mouse" | "hybrid";

  // Screen characteristics
  screenSize: "mobile" | "tablet" | "desktop" | "largeDesktop";

  // Device features
  hasTouch: boolean;
  hasPrecisePointer: boolean;
  hasKeyboard: boolean;

  // Viewport information
  viewport: {
    width: number;
    height: number;
  };

  // Display characteristics
  pixelRatio: number;
  colorDepth: number;
  supportsHDR: boolean;

  // Performance indicators
  memoryEstimate?: number; // MB
  hardwareConcurrency: number;
  connectionSpeed?: "slow" | "medium" | "fast";
}

export interface ResponsiveSettings {
  // Touch targets
  minTouchTarget: number;
  elementSpacing: number;

  // Layout density
  layoutDensity: "compact" | "comfortable" | "spacious";

  // Typography
  fontScaling: number;
  lineHeightMultiplier: number;

  // Interaction preferences
  allowScrolling: boolean;
  preferSwipeGestures: boolean;
  reducedMotion: boolean;
}

// ============================================================================
// CACHE MANAGEMENT TYPES
// ============================================================================

export interface CacheEntry {
  id: string;
  sequence: SequenceData;
  imageBlob: Blob;
  metadata: CacheMetadata;
  createdAt: Date;
  lastAccessed: Date;
  accessCount: number;
}

export interface CacheMetadata {
  sequenceId: string;
  sequenceName: string;
  beatCount: number;
  fileSize: number;
  format: string;
  resolution: string;
  exportOptions: ExportOptions;
  version: string; // Cache version for invalidation
}

export interface CacheConfig {
  enabled: boolean;
  maxSize: number; // Maximum number of entries
  maxSizeBytes: number; // Maximum storage in bytes
  ttl: number; // Time to live in milliseconds
  compressionEnabled: boolean;
  indexedDBName: string;
  objectStoreName: string;
}

export interface CacheStats {
  totalEntries: number;
  totalSizeBytes: number;
  hitRate: number; // 0-1
  oldestEntry?: Date;
  newestEntry?: Date;
  lastCleanup?: Date;
}

// ============================================================================
// SEQUENCE CARD DISPLAY TYPES
// ============================================================================

export interface SequenceCardDisplayOptions {
  // Visual options
  showBeatNumbers: boolean;
  showDifficulty: boolean;
  showAuthor: boolean;
  showMetadata: boolean;

  // Interaction options
  enablePreview: boolean;
  enableQuickExport: boolean;
  enableDragDrop: boolean;

  // Animation options
  enableHoverEffects: boolean;
  enableLoadAnimations: boolean;
  animationDuration: number;

  // Transparency options
  backgroundTransparency: number; // 0-1
  enableGlassmorphism: boolean;
  blurIntensity: number;
}

export interface SequenceCardMetrics {
  // Dimensions
  width: number;
  height: number;
  aspectRatio: number;

  // Performance
  renderTime: number;
  loadTime: number;

  // User interaction
  clickCount: number;
  hoverDuration: number;
  lastInteraction: Date;
}

// ============================================================================
// PROGRESS TRACKING TYPES
// ============================================================================

export interface ProgressInfo {
  current: number;
  total: number;
  percentage: number;
  message: string;
  stage: ProgressStage;
  startTime: Date;
  estimatedCompletion?: Date;
  errorCount: number;
  warningCount: number;
}

export type ProgressStage =
  | "initializing"
  | "loading"
  | "processing"
  | "rendering"
  | "exporting"
  | "finalizing"
  | "completed"
  | "error"
  | "cancelled";

export interface BatchProgress {
  batchNumber: number;
  totalBatches: number;
  batchSize: number;
  currentBatch: ProgressInfo;
  overall: ProgressInfo;

  // Performance metrics
  averageTimePerItem: number;
  memoryUsage: number;
  throughput: number; // items per second
}

// ============================================================================
// VALIDATION & ERROR TYPES
// ============================================================================

export interface ValidationResult {
  isValid: boolean;
  errors: ValidationError[];
  warnings: ValidationWarning[];
}

export interface ValidationError {
  code: string;
  message: string;
  field?: string;
  value?: unknown;
  severity: "error" | "warning" | "info";
}

export interface ValidationWarning {
  code: string;
  message: string;
  suggestion?: string;
}

// ============================================================================
// EVENT TYPES
// ============================================================================

export interface SequenceCardEvents {
  // Selection events
  cardSelected: { sequenceId: string; card: SequenceData };
  cardDeselected: { sequenceId: string };
  multipleSelected: { sequenceIds: string[] };

  // Export events
  exportStarted: { sequences: SequenceData[]; options: ExportOptions };
  exportProgress: { progress: ProgressInfo };
  exportCompleted: { results: ExportResult[] };
  exportCancelled: { reason: string };
  exportError: { error: Error; sequences: SequenceData[] };

  // Layout events
  layoutChanged: { layout: LayoutConfig };
  columnCountChanged: { count: number };
  viewModeChanged: { mode: "grid" | "list" | "printable" };

  // Cache events
  cacheHit: { sequenceId: string };
  cacheMiss: { sequenceId: string };
  cacheEvicted: { entries: CacheEntry[] };
  cacheCleared: { reason: string };
}

export interface ExportResult {
  sequenceId: string;
  success: boolean;
  blob?: Blob;
  error?: Error;
  metrics: {
    processingTime: number;
    fileSize: number;
    resolution: { width: number; height: number };
  };
}

// ============================================================================
// UTILITY TYPES
// ============================================================================

export type LayoutMode = "grid" | "list" | "printable";
export type SortOrder = "asc" | "desc";
export type SortField =
  | "name"
  | "beats"
  | "difficulty"
  | "author"
  | "created"
  | "modified";

export interface SortConfig {
  field: SortField;
  order: SortOrder;
}

export interface FilterConfig {
  lengthFilter: number | null; // null means "all"
  difficultyFilter: string[];
  authorFilter: string[];
  searchQuery: string;
}

// ============================================================================
// COMPONENT PROPS TYPES
// ============================================================================

export interface SequenceCardProps {
  sequence: SequenceData;
  displayOptions?: Partial<SequenceCardDisplayOptions>;
  isSelected?: boolean;
  isLoading?: boolean;
  onSelect?: (sequence: SequenceData) => void;
  onExport?: (sequence: SequenceData) => void;
  onPreview?: (sequence: SequenceData) => void;
}

export interface SequenceCardGridProps {
  sequences: SequenceData[];
  layout: LayoutConfig;
  displayOptions?: Partial<SequenceCardDisplayOptions>;
  onSequenceSelect?: (sequence: SequenceData) => void;
  onLayoutChange?: (layout: LayoutConfig) => void;
}

export interface SequenceCardExportDialogProps {
  sequences: SequenceData[];
  initialSettings?: Partial<SequenceCardExportSettings>;
  onExport?: (settings: SequenceCardExportSettings) => void;
  onCancel?: () => void;
}
