/**
 * Sequence Card State - Svelte 5 Runes Implementation
 *
 * Manages reactive state for sequence card functionality including:
 * - Length filtering and column management
 * - Export progress and settings
 * - Layout calculations and pagination
 * - Page layout and printable page creation
 * - Cache management
 *
 * Uses pure runes ($state, $derived, $effect) for all reactivity
 */

import type { SequenceData } from "$lib/domain";
import type {
  LayoutConfig,
  // ExportOptions,
  // SequenceCardExportSettings,
  DeviceCapabilities,
} from "$lib/domain/sequenceCard";
import type {
  IPrintablePageLayoutService,
  IPageFactoryService,
} from "$services/interfaces/sequence-interfaces";
import {
  createPageLayoutState,
  type PageLayoutState,
} from "./page-layout-state.svelte";

// ============================================================================
// CORE SEQUENCE CARD STATE
// ============================================================================

const sequenceCardState = $state({
  // Filter & Display Settings
  selectedLength: 16,
  columnCount: 2,
  layoutMode: "grid" as "grid" | "list" | "printable",
  showBeatNumbers: true,
  transparentBackground: true,

  // Pagination & Navigation
  currentPage: 1,
  itemsPerPage: 24,

  // Export & Progress Management
  isExporting: false,
  isRegenerating: false,
  exportProgress: 0,
  exportMessage: "Select a sequence length to view cards",
  lastExportTimestamp: null as Date | null,

  // Layout & Responsiveness
  containerWidth: 1200,
  containerHeight: 800,
  deviceCapabilities: null as DeviceCapabilities | null,

  // Cache Management
  cacheEnabled: true,
  cacheSizeLimit: 100, // Number of images to cache
  cacheLastCleared: null as Date | null,
});

// ============================================================================
// EXPORT SETTINGS STATE
// ============================================================================

const exportSettingsState = $state({
  // Image Export Options
  quality: "high" as "low" | "medium" | "high",
  format: "PNG" as "PNG" | "JPG" | "WebP",
  resolution: "300" as "150" | "300" | "600",

  // Metadata Options
  includeTitle: true,
  includeMetadata: true,
  includeBeatNumbers: true,
  includeAuthor: true,
  includeDifficulty: true,
  includeDate: true,

  // Layout Options
  paperSize: "A4" as "A4" | "Letter" | "Legal" | "Tabloid",
  orientation: "Portrait" as "Portrait" | "Landscape",
  margins: { top: 20, right: 20, bottom: 20, left: 20 },

  // Batch Options
  batchSize: 10,
  enableProgressReporting: true,
  enableMemoryOptimization: true,
});

// ============================================================================
// DERIVED REACTIVE VALUES
// ============================================================================

// Filtered sequences based on selected length
const filteredSequences = $derived(() => {
  // This will be replaced by enhancedFilteredSequences in the enhanced state
  return []; // Placeholder - actual implementation is in createEnhancedSequenceCardState
});

// Current page sequences for pagination
const currentPageSequences = $derived(() => {
  const startIndex =
    (sequenceCardState.currentPage - 1) * sequenceCardState.itemsPerPage;
  const endIndex = startIndex + sequenceCardState.itemsPerPage;
  return filteredSequences().slice(startIndex, endIndex);
});

// Total pages calculation
const totalPages = $derived(() => {
  return Math.ceil(filteredSequences().length / sequenceCardState.itemsPerPage);
});

// Layout configuration based on current settings
const currentLayout = $derived(() => {
  const { containerWidth, containerHeight, columnCount } = sequenceCardState;

  return calculateOptimalLayout(
    containerWidth,
    containerHeight,
    currentPageSequences.length,
    columnCount
  );
});

// Progress message with dynamic content
const progressMessage = $derived(() => {
  const { isExporting, isRegenerating, exportProgress, selectedLength } =
    sequenceCardState;
  const sequenceCount = filteredSequences.length;

  if (isExporting) {
    return `Exporting sequence cards... ${Math.round(exportProgress)}%`;
  }

  if (isRegenerating) {
    return `Regenerating images... ${Math.round(exportProgress)}%`;
  }

  if (sequenceCount === 0) {
    return selectedLength === 0
      ? "No sequences available"
      : `No sequences found with ${selectedLength} beats`;
  }

  const lengthText = selectedLength === 0 ? "all" : `${selectedLength}-beat`;
  return `Displaying ${sequenceCount} ${lengthText} sequence${sequenceCount === 1 ? "" : "s"}`;
});

// Export readiness check
const canExport = $derived(() => {
  return (
    !sequenceCardState.isExporting &&
    !sequenceCardState.isRegenerating &&
    filteredSequences.length > 0
  );
});

// Cache status information
const cacheStatus = $derived(() => {
  return {
    enabled: sequenceCardState.cacheEnabled,
    sizeLimit: sequenceCardState.cacheSizeLimit,
    lastCleared: sequenceCardState.cacheLastCleared,
    estimatedSize: Math.min(
      filteredSequences.length,
      sequenceCardState.cacheSizeLimit
    ),
  };
});

// ============================================================================
// LAYOUT CALCULATION HELPERS
// ============================================================================

function calculateOptimalLayout(
  containerWidth: number,
  containerHeight: number,
  itemCount: number,
  preferredColumns: number
): LayoutConfig {
  const CARD_ASPECT_RATIO = 1.4; // Width/Height ratio from legacy
  const CARD_SPACING = 16;
  const CONTAINER_PADDING = 32;

  const availableWidth = containerWidth - CONTAINER_PADDING * 2;
  const availableHeight = containerHeight - 100; // Reserve space for header

  // Calculate card dimensions for preferred column count
  const cardWidth =
    (availableWidth - CARD_SPACING * (preferredColumns - 1)) / preferredColumns;
  const cardHeight = cardWidth / CARD_ASPECT_RATIO;

  const rows = Math.ceil(itemCount / preferredColumns);
  const totalHeight = rows * cardHeight + (rows - 1) * CARD_SPACING;

  return {
    columns: preferredColumns,
    rows,
    cardWidth,
    cardHeight,
    totalWidth: availableWidth,
    totalHeight,
    spacing: CARD_SPACING,
    canFitInContainer: totalHeight <= availableHeight,
    utilization:
      (itemCount * cardWidth * cardHeight) / (availableWidth * availableHeight),
  };
}

// ============================================================================
// STATE MUTATION FUNCTIONS
// ============================================================================

// Length selection
export function setSelectedLength(length: number) {
  sequenceCardState.selectedLength = length;
  sequenceCardState.currentPage = 1; // Reset to first page
}

// Column count management
export function setColumnCount(count: number) {
  if (count >= 1 && count <= 6) {
    sequenceCardState.columnCount = count;
  }
}

// Layout mode switching
export function setLayoutMode(mode: "grid" | "list" | "printable") {
  sequenceCardState.layoutMode = mode;

  // Adjust column count for different modes
  if (mode === "list") {
    sequenceCardState.columnCount = 1;
  } else if (mode === "printable") {
    sequenceCardState.columnCount = 2; // Default for printable
  }
}

// Pagination controls
export function goToPage(page: number) {
  if (page >= 1 && page <= totalPages()) {
    sequenceCardState.currentPage = page;
  }
}

export function nextPage() {
  if (sequenceCardState.currentPage < totalPages()) {
    sequenceCardState.currentPage++;
  }
}

export function previousPage() {
  if (sequenceCardState.currentPage > 1) {
    sequenceCardState.currentPage--;
  }
}

// Container size updates (for responsive layout)
export function updateContainerSize(width: number, height: number) {
  sequenceCardState.containerWidth = width;
  sequenceCardState.containerHeight = height;
}

// Device capabilities
export function setDeviceCapabilities(capabilities: DeviceCapabilities) {
  sequenceCardState.deviceCapabilities = capabilities;

  // Adjust settings based on device
  if (capabilities.screenSize === "mobile") {
    sequenceCardState.columnCount = 1;
    sequenceCardState.itemsPerPage = 12;
  } else if (capabilities.screenSize === "tablet") {
    sequenceCardState.columnCount = 2;
    sequenceCardState.itemsPerPage = 18;
  }
}

// Export progress management
export function startExport() {
  sequenceCardState.isExporting = true;
  sequenceCardState.exportProgress = 0;
}

export function updateExportProgress(progress: number, message?: string) {
  sequenceCardState.exportProgress = Math.max(0, Math.min(100, progress));
  if (message) {
    sequenceCardState.exportMessage = message;
  }
}

export function finishExport() {
  sequenceCardState.isExporting = false;
  sequenceCardState.exportProgress = 100;
  sequenceCardState.lastExportTimestamp = new Date();

  // Reset progress after a delay
  setTimeout(() => {
    sequenceCardState.exportProgress = 0;
  }, 2000);
}

export function cancelExport() {
  sequenceCardState.isExporting = false;
  sequenceCardState.exportProgress = 0;
}

// Regeneration progress management
export function startRegeneration() {
  sequenceCardState.isRegenerating = true;
  sequenceCardState.exportProgress = 0;
}

export function finishRegeneration() {
  sequenceCardState.isRegenerating = false;
  sequenceCardState.exportProgress = 100;

  // Reset progress after a delay
  setTimeout(() => {
    sequenceCardState.exportProgress = 0;
  }, 2000);
}

export function cancelRegeneration() {
  sequenceCardState.isRegenerating = false;
  sequenceCardState.exportProgress = 0;
}

// Cache management
export function clearCache() {
  sequenceCardState.cacheLastCleared = new Date();
  // Actual cache clearing will be handled by cache service
}

export function setCacheEnabled(enabled: boolean) {
  sequenceCardState.cacheEnabled = enabled;
}

export function setCacheSizeLimit(limit: number) {
  if (limit > 0 && limit <= 1000) {
    sequenceCardState.cacheSizeLimit = limit;
  }
}

// Export settings management
export function updateExportSetting<K extends keyof typeof exportSettingsState>(
  key: K,
  value: (typeof exportSettingsState)[K]
) {
  // Type assertion is safe here since we're updating a mutable state object
  (exportSettingsState as Record<string, unknown>)[key] = value;
}

export function resetExportSettings() {
  exportSettingsState.quality = "high";
  exportSettingsState.format = "PNG";
  exportSettingsState.resolution = "300";
  exportSettingsState.includeTitle = true;
  exportSettingsState.includeMetadata = true;
  exportSettingsState.includeBeatNumbers = true;
  exportSettingsState.includeAuthor = true;
  exportSettingsState.includeDifficulty = true;
  exportSettingsState.includeDate = true;
  exportSettingsState.paperSize = "A4";
  exportSettingsState.orientation = "Portrait";
}

// ============================================================================
// GETTERS FOR EXTERNAL ACCESS
// ============================================================================

export function getSequenceCardState() {
  return sequenceCardState;
}

export function getExportSettingsState() {
  return exportSettingsState;
}

export function getFilteredSequences() {
  return filteredSequences;
}

export function getCurrentPageSequences() {
  return currentPageSequences;
}

export function getTotalPages() {
  return totalPages;
}

export function getCurrentLayout() {
  return currentLayout;
}

export function getProgressMessage() {
  return progressMessage;
}

export function getCanExport() {
  return canExport;
}

export function getCacheStatus() {
  return cacheStatus;
}

// ============================================================================
// ENHANCED SEQUENCE CARD STATE FACTORY
// ============================================================================

export interface EnhancedSequenceCardState {
  // Original sequence card state
  sequenceCardState: typeof sequenceCardState;
  exportSettingsState: typeof exportSettingsState;

  // Page layout state
  pageLayoutState: PageLayoutState;

  // Derived values
  filteredSequences: SequenceData[];
  currentPageSequences: SequenceData[];
  totalPages: number;
  currentLayout: LayoutConfig;
  progressMessage: string;
  canExport: boolean;
  cacheStatus: ReturnType<typeof getCacheStatus>;

  // Enhanced actions
  switchToPageView: () => Promise<void>;
  switchToGridView: () => void;
  refreshPages: () => Promise<void>;
  updateSequences: (sequences: SequenceData[]) => Promise<void>;
}

export function createEnhancedSequenceCardState(
  layoutService: IPrintablePageLayoutService,
  pageFactoryService: IPageFactoryService,
  initialSequences: SequenceData[] = []
): EnhancedSequenceCardState {
  // Create page layout state
  const pageLayoutState = createPageLayoutState(
    layoutService,
    pageFactoryService,
    initialSequences
  );

  // Store current sequences for integration
  let currentSequences = $state<SequenceData[]>(initialSequences);

  // Enhanced filtered sequences that use current sequences
  const enhancedFilteredSequences = $derived(() => {
    if (sequenceCardState.selectedLength === 0) {
      return currentSequences; // "All" selected
    }

    return currentSequences.filter(
      (seq) =>
        seq.beats && seq.beats.length === sequenceCardState.selectedLength
    );
  });

  // Enhanced current page sequences
  const enhancedCurrentPageSequences = $derived(() => {
    if (sequenceCardState.layoutMode === "printable") {
      // In printable mode, return sequences from current printable page
      const currentPage = pageLayoutState.pages[pageLayoutState.currentPage];
      return currentPage?.sequences || [];
    }

    // Original pagination logic for grid/list modes
    const startIndex =
      (sequenceCardState.currentPage - 1) * sequenceCardState.itemsPerPage;
    const endIndex = startIndex + sequenceCardState.itemsPerPage;
    return enhancedFilteredSequences().slice(startIndex, endIndex);
  });

  // Enhanced total pages calculation
  const enhancedTotalPages = $derived(() => {
    if (sequenceCardState.layoutMode === "printable") {
      return pageLayoutState.totalPages;
    }

    return Math.ceil(
      enhancedFilteredSequences().length / sequenceCardState.itemsPerPage
    );
  });

  // Enhanced progress message
  const enhancedProgressMessage = $derived(() => {
    const {
      isExporting,
      isRegenerating,
      exportProgress,
      selectedLength,
      layoutMode,
    } = sequenceCardState;
    const sequenceCount = enhancedFilteredSequences().length;

    if (pageLayoutState.isLoading) {
      return "Creating printable pages...";
    }

    if (pageLayoutState.error) {
      return `Error: ${pageLayoutState.error}`;
    }

    if (isExporting) {
      return `Exporting sequence cards... ${Math.round(exportProgress)}%`;
    }

    if (isRegenerating) {
      return `Regenerating images... ${Math.round(exportProgress)}%`;
    }

    if (sequenceCount === 0) {
      return selectedLength === 0
        ? "No sequences available"
        : `No sequences found with ${selectedLength} beats`;
    }

    if (layoutMode === "printable" && pageLayoutState.totalPages > 0) {
      return `${pageLayoutState.totalPages} printable page${pageLayoutState.totalPages === 1 ? "" : "s"} created`;
    }

    const lengthText = selectedLength === 0 ? "all" : `${selectedLength}-beat`;
    return `Displaying ${sequenceCount} ${lengthText} sequence${sequenceCount === 1 ? "" : "s"}`;
  });

  // Enhanced actions
  async function switchToPageView(): Promise<void> {
    sequenceCardState.layoutMode = "printable";
    await pageLayoutState.createPages(enhancedFilteredSequences());
  }

  function switchToGridView(): void {
    sequenceCardState.layoutMode = "grid";
  }

  async function refreshPages(): Promise<void> {
    if (sequenceCardState.layoutMode === "printable") {
      await pageLayoutState.regeneratePages();
    }
  }

  async function updateSequences(sequences: SequenceData[]): Promise<void> {
    currentSequences = [...sequences];

    if (sequenceCardState.layoutMode === "printable") {
      await pageLayoutState.createPages(enhancedFilteredSequences());
    }
  }

  // Auto-update pages when filter changes in printable mode
  $effect(() => {
    const filtered = enhancedFilteredSequences();
    const layoutMode = sequenceCardState.layoutMode;

    if (layoutMode === "printable" && pageLayoutState.pages.length > 0) {
      // Debounce the page recreation
      const timeoutId = setTimeout(() => {
        pageLayoutState.createPages(filtered);
      }, 300);

      return () => clearTimeout(timeoutId);
    }
  });

  return {
    sequenceCardState,
    exportSettingsState,
    pageLayoutState,

    // Enhanced derived values
    get filteredSequences() {
      return enhancedFilteredSequences();
    },
    get currentPageSequences() {
      return enhancedCurrentPageSequences();
    },
    get totalPages() {
      return enhancedTotalPages();
    },
    get currentLayout() {
      return getCurrentLayout()();
    },
    get progressMessage() {
      return enhancedProgressMessage();
    },
    get canExport() {
      return getCanExport()();
    },
    get cacheStatus() {
      return getCacheStatus();
    },

    // Enhanced actions
    switchToPageView,
    switchToGridView,
    refreshPages,
    updateSequences,
  };
}
