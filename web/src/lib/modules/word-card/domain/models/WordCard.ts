/**
 * Word Card Domain Types
 *
 * Type definitions for word card functionality including layout,
 * export options, device capabilities, and cache management.
 */

import type { SequenceData } from "$shared";
import type { ExportResult } from "../../../../shared/foundation/ui/UITypes";
import type { CacheEntry } from "./cache-models";
import type { WordCardExportOptions } from "./word-card-export";

// ============================================================================
// LAYOUT CONFIGURATION TYPES
// ============================================================================

export interface WordCardLayoutConfig {
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

export interface ResponsiveBreakpoints {
  mobile: number;
  tablet: number;
  desktop: number;
  largeDesktop: number;
}

// ============================================================================
// EXPORT OPTIONS & SETTINGS
// ============================================================================

// ExportOptions is now imported from word-card-export.ts

export interface WordCardExportSettings {
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
  paperSize: WordCardPaperSize;
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

type WordCardPaperSize = "A4" | "Letter" | "Legal" | "Tabloid";

// ============================================================================
// SEQUENCE CARD DISPLAY TYPES
// ============================================================================

export interface WordCardDisplayOptions {
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

export interface WordCardMetrics {
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
// Import shared validation types instead of defining locally
// Using shared ValidationResult from $shared/domain

// VALIDATION & ERROR TYPES
// ============================================================================
// All validation types now imported from shared domain

// ============================================================================
// EVENT TYPES
// ============================================================================

export interface WordCardEvents {
  // Selection events
  cardSelected: { sequenceId: string; card: SequenceData };
  cardDeselected: { sequenceId: string };
  multipleSelected: { sequenceIds: string[] };

  // Export events
  exportStarted: { sequences: SequenceData[]; options: WordCardExportOptions };
  exportProgress: { progress: ProgressInfo };
  exportCompleted: { results: ExportResult[] };
  exportCancelled: { reason: string };
  exportError: { error: Error; sequences: SequenceData[] };

  // Layout events
  layoutChanged: { layout: WordCardLayoutConfig };
  columnCountChanged: { count: number };
  viewModeChanged: { mode: "grid" | "list" | "printable" };

  // Cache events
  cacheHit: { sequenceId: string };
  cacheMiss: { sequenceId: string };
  cacheEvicted: { entries: CacheEntry[] };
  cacheCleared: { reason: string };
}

// Note: WordCardExportResult is defined above
// to avoid duplication across the domain

// ============================================================================
// UTILITY TYPES
// ============================================================================

export type SortOrder = "asc" | "desc";
export type SortField =
  | "name"
  | "beats"
  | "difficulty"
  | "author"
  | "created"
  | "modified";

export interface WordCardSortConfig {
  field: SortField;
  order: SortOrder;
}

export interface WordCardFilterConfig {
  lengthFilter: number | null; // null means "all"
  difficultyFilter: string[];
  authorFilter: string[];
  searchQuery: string;
}

// ============================================================================
// COMPONENT PROPS TYPES
// ============================================================================

export interface WordCardProps {
  sequence: SequenceData;
  displayOptions?: Partial<WordCardDisplayOptions>;
  isSelected?: boolean;
  isLoading?: boolean;
  onSelect?: (sequence: SequenceData) => void;
  onExport?: (sequence: SequenceData) => void;
  onPreview?: (sequence: SequenceData) => void;
}

export interface WordCardGridProps {
  sequences: SequenceData[];
  layout: WordCardLayoutConfig;
  displayOptions?: Partial<WordCardDisplayOptions>;
  onSequenceSelect?: (sequence: SequenceData) => void;
  onLayoutChange?: (layout: WordCardLayoutConfig) => void;
}

export interface WordCardExportDialogProps {
  sequences: SequenceData[];
  initialSettings?: Partial<WordCardExportSettings>;
  onExport?: (settings: WordCardExportSettings) => void;
  onCancel?: () => void;
}
