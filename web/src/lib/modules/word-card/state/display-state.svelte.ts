/**
 * Word Card Display State
 *
 * Focused state management for word card display settings only.
 * Delegates data loading to GalleryService and page layout to PageLayoutService.
 */

import type { DeviceCapabilities } from "$shared/domain";

// ============================================================================
// DISPLAY SETTINGS STATE
// ============================================================================

const displayState = $state({
  selectedLength: 16,
  columnCount: 2,
  showBeatNumbers: true,
  transparentBackground: true,
});

// ============================================================================
// EXPORT SETTINGS STATE
// ============================================================================

const exportSettings = $state({
  // Image Options
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
// PROGRESS STATE
// ============================================================================

const progressState = $state({
  isExporting: false,
  isRegenerating: false,
  progress: 0,
  message: "Ready",
});

// ============================================================================
// RESPONSIVE LAYOUT STATE
// ============================================================================

const layoutState = $state({
  containerWidth: 1200,
  containerHeight: 800,
  deviceCapabilities: null as DeviceCapabilities | null,
});

// ============================================================================
// ACTIONS
// ============================================================================

function setSelectedLength(length: number) {
  displayState.selectedLength = length;
}

function setColumnCount(count: number) {
  if (count >= 1 && count <= 6) {
    displayState.columnCount = count;
  }
}

function setShowBeatNumbers(show: boolean) {
  displayState.showBeatNumbers = show;
}

function setTransparentBackground(transparent: boolean) {
  displayState.transparentBackground = transparent;
}

function updateContainerSize(width: number, height: number) {
  layoutState.containerWidth = width;
  layoutState.containerHeight = height;
}

function setDeviceCapabilities(capabilities: DeviceCapabilities) {
  layoutState.deviceCapabilities = capabilities;

  // Auto-adjust for mobile/tablet
  if (capabilities.screenSize === "mobile") {
    displayState.columnCount = 1;
  } else if (capabilities.screenSize === "tablet") {
    displayState.columnCount = 2;
  }
}

function startExport() {
  progressState.isExporting = true;
  progressState.progress = 0;
  progressState.message = "Starting export...";
}

function updateExportProgress(progress: number, message?: string) {
  progressState.progress = Math.max(0, Math.min(100, progress));
  if (message) {
    progressState.message = message;
  }
}

function finishExport() {
  progressState.isExporting = false;
  progressState.progress = 100;
  progressState.message = "Export completed";

  // Reset after delay
  setTimeout(() => {
    progressState.progress = 0;
    progressState.message = "Ready";
  }, 2000);
}

function startRegeneration() {
  progressState.isRegenerating = true;
  progressState.progress = 0;
  progressState.message = "Regenerating images...";
}

function finishRegeneration() {
  progressState.isRegenerating = false;
  progressState.progress = 100;
  progressState.message = "Regeneration completed";

  // Reset after delay
  setTimeout(() => {
    progressState.progress = 0;
    progressState.message = "Ready";
  }, 2000);
}

function updateExportSetting<K extends keyof typeof exportSettings>(
  key: K,
  value: (typeof exportSettings)[K]
) {
  exportSettings[key] = value;
}

function resetExportSettings() {
  exportSettings.quality = "high";
  exportSettings.format = "PNG";
  exportSettings.resolution = "300";
  exportSettings.includeTitle = true;
  exportSettings.includeMetadata = true;
  exportSettings.includeBeatNumbers = true;
  exportSettings.includeAuthor = true;
  exportSettings.includeDifficulty = true;
  exportSettings.includeDate = true;
  exportSettings.paperSize = "A4";
  exportSettings.orientation = "Portrait";
  exportSettings.margins = { top: 20, right: 20, bottom: 20, left: 20 };
  exportSettings.batchSize = 10;
  exportSettings.enableProgressReporting = true;
  exportSettings.enableMemoryOptimization = true;
}

// ============================================================================
// EXPORTS
// ============================================================================

export {
  // State
  displayState,
  exportSettings,
  finishExport,
  finishRegeneration,
  layoutState,
  progressState,
  resetExportSettings,
  setColumnCount,
  setDeviceCapabilities,
  // Actions
  setSelectedLength,
  setShowBeatNumbers,
  setTransparentBackground,
  startExport,
  startRegeneration,
  updateContainerSize,
  updateExportProgress,
  updateExportSetting,
};
