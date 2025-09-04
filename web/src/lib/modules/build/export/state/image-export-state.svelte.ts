/**
 * TKA Image Export State
 *
 * Reactive state management for TKA image export functionality using Svelte 5 runes.
 * This state layer provides the reactive interface between the export UI components
 * and the image export services.
 *
 * Critical: All state uses Svelte 5 runes, no legacy stores.
 */

import type { SequenceData, SequenceExportOptions } from "$domain";
import type { ITKAImageExportService } from "$services";

export interface ImageExportState {
  // Export options state
  readonly exportOptions: SequenceExportOptions;

  // Preview state
  readonly previewImageUrl: string | null;
  readonly isGeneratingPreview: boolean;
  readonly previewError: string | null;

  // Export state
  readonly isExporting: boolean;
  readonly exportError: string | null;
  readonly lastExportedFile: string | null;

  // Validation state
  readonly canExport: boolean;
  readonly validationErrors: string[];

  // Actions
  updateOptions: (newOptions: Partial<SequenceExportOptions>) => Promise<void>;
  generatePreview: (sequence?: SequenceData) => Promise<void>;
  exportSequence: (sequence: SequenceData, filename?: string) => Promise<void>;
  clearPreview: () => void;
  clearErrors: () => void;
  resetToDefaults: () => void;
}

/**
 * Create TKA image export state factory
 * Returns reactive state object using Svelte 5 runes
 */
export function createImageExportState(
  exportService: ITKAImageExportService,
  initialOptions?: Partial<SequenceExportOptions>
): ImageExportState {
  // Core export options state
  let exportOptions = $state<SequenceExportOptions>(
    exportService.getDefaultOptions()
  );

  // Preview state
  let previewImageUrl = $state<string | null>(null);
  let isGeneratingPreview = $state(false);
  let previewError = $state<string | null>(null);

  // Export state
  let isExporting = $state(false);
  let exportError = $state<string | null>(null);
  let lastExportedFile = $state<string | null>(null);

  // Current sequence being worked with
  let currentSequence = $state<SequenceData | null>(null);

  // Initialize with provided options
  if (initialOptions) {
    exportOptions = { ...exportOptions, ...initialOptions };
  }

  // Derived state - validation
  const validationErrors = $derived(() => {
    if (!currentSequence) return [];

    const validation = exportService.validateExport(
      currentSequence,
      exportOptions // This is properly reactive now
    );
    return validation.errors;
  });

  // Derived state - can export
  const canExport = $derived(() => {
    return (
      !isExporting &&
      !isGeneratingPreview &&
      validationErrors.length === 0 &&
      currentSequence !== null
    );
  });

  // Auto-regenerate preview when options change
  $effect(() => {
    // Track exportOptions to ensure reactivity

    if (currentSequence && previewImageUrl) {
      // Debounce preview generation to avoid excessive updates
      const timeoutId = setTimeout(() => {
        if (currentSequence) {
          generatePreview(currentSequence);
        }
      }, 300);

      return () => clearTimeout(timeoutId);
    }
  });

  /**
   * Update export options
   * Triggers preview regeneration if sequence is available
   */
  async function updateOptions(
    newOptions: Partial<SequenceExportOptions>
  ): Promise<void> {
    try {
      clearErrors();
      exportOptions = { ...exportOptions, ...newOptions };

      // Auto-regenerate preview if we have a sequence
      if (currentSequence) {
        await generatePreview(currentSequence);
      }
    } catch (error) {
      console.error("Failed to update export options:", error);
    }
  }

  /**
   * Generate preview image
   * Updates preview state with generated image URL
   */
  async function generatePreview(sequence?: SequenceData): Promise<void> {
    if (!sequence) {
      clearPreview();
      return;
    }

    // Update current sequence
    currentSequence = sequence;

    isGeneratingPreview = true;
    previewError = null;

    try {
      // Capture current options to avoid reactivity warning
      const currentOptions = exportOptions;
      const dataUrl = await exportService.generatePreview(
        sequence,
        currentOptions
      );
      previewImageUrl = dataUrl;
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Preview generation failed";
      console.error("Preview generation failed:", error);
      previewError = errorMessage;
      previewImageUrl = null;
    } finally {
      isGeneratingPreview = false;
    }
  }

  /**
   * Export sequence as downloadable file
   */
  async function exportSequence(
    sequence: SequenceData,
    filename?: string
  ): Promise<void> {
    if (!sequence) {
      throw new Error("Sequence is required for export");
    }

    isExporting = true;
    exportError = null;
    lastExportedFile = null;

    try {
      // Update current sequence
      currentSequence = sequence;

      // Capture current options to avoid reactivity warning
      const currentOptions = exportOptions;

      // Perform export and download
      await exportService.exportAndDownload(sequence, filename, currentOptions);

      // Generate filename for display (if not provided)
      const displayFilename =
        filename ||
        `${sequence.word || "sequence"}.${currentOptions.format.toLowerCase()}`;
      lastExportedFile = displayFilename;
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Export failed";
      console.error("Export failed:", error);
      exportError = errorMessage;
    } finally {
      isExporting = false;
    }
  }

  /**
   * Clear preview state
   */
  function clearPreview(): void {
    previewImageUrl = null;
    previewError = null;
    isGeneratingPreview = false;
  }

  /**
   * Clear error states
   */
  function clearErrors(): void {
    previewError = null;
    exportError = null;
  }

  /**
   * Reset options to defaults
   */
  function resetToDefaults(): void {
    clearErrors();
    clearPreview();
    exportOptions = exportService.getDefaultOptions();
    lastExportedFile = null;
  }

  return {
    // State getters (using derived for reactivity)
    get exportOptions() {
      return exportOptions;
    },
    get previewImageUrl() {
      return previewImageUrl;
    },
    get isGeneratingPreview() {
      return isGeneratingPreview;
    },
    get previewError() {
      return previewError;
    },
    get isExporting() {
      return isExporting;
    },
    get exportError() {
      return exportError;
    },
    get lastExportedFile() {
      return lastExportedFile;
    },
    get canExport() {
      return canExport();
    },
    get validationErrors() {
      return validationErrors();
    },

    // Actions
    updateOptions,
    generatePreview,
    exportSequence,
    clearPreview,
    clearErrors,
    resetToDefaults,
  };
}

/**
 * Create image export state with settings persistence
 * Automatically saves and restores export options
 */
export function createPersistentImageExportState(
  exportService: ITKAImageExportService,
  storageKey: string = "tka-image-export-options"
): ImageExportState {
  // Load saved options from localStorage
  let savedOptions: Partial<SequenceExportOptions> = {};
  try {
    const saved = localStorage.getItem(storageKey);
    if (saved) {
      savedOptions = JSON.parse(saved);
    }
  } catch (error) {
    console.warn("Failed to load saved export options:", error);
  }

  // Create state with saved options
  const state = createImageExportState(exportService, savedOptions);

  // Wrap updateOptions to save to localStorage
  const originalUpdateOptions = state.updateOptions;
  const persistentUpdateOptions = async (
    newOptions: Partial<SequenceExportOptions>
  ) => {
    await originalUpdateOptions(newOptions);

    // Save updated options
    try {
      localStorage.setItem(storageKey, JSON.stringify(state.exportOptions));
    } catch (error) {
      console.warn("Failed to save export options:", error);
    }
  };

  // Wrap resetToDefaults to clear localStorage
  const originalResetToDefaults = state.resetToDefaults;
  const persistentResetToDefaults = () => {
    originalResetToDefaults();

    // Clear saved options
    try {
      localStorage.removeItem(storageKey);
    } catch (error) {
      console.warn("Failed to clear saved export options:", error);
    }
  };

  return {
    ...state,
    updateOptions: persistentUpdateOptions,
    resetToDefaults: persistentResetToDefaults,
  };
}

/**
 * Image export state for specific use cases
 */
export function createQuickExportState(
  exportService: ITKAImageExportService,
  purpose: "sharing" | "printing" | "archival"
): ImageExportState {
  // Preset options for different purposes
  const presetOptions: Record<string, Partial<SequenceExportOptions>> = {
    sharing: {
      // beatScale: 0.8, // Not available in ImageExportOptions
      format: "PNG",
      quality: 0.9,
      // addUserInfo: false, // Not available in ImageExportOptions
      // addDifficultyLevel: false, // Not available in ImageExportOptions
    },
    printing: {
      // beatScale: 1.2, // Not available in ImageExportOptions
      format: "PNG",
      quality: 1.0,
      // addUserInfo: true, // Not available in ImageExportOptions
      // addWord: true, // Not available in ImageExportOptions
      // addDifficultyLevel: true, // Not available in ImageExportOptions
    },
    archival: {
      // beatScale: 1.0, // Not available in ImageExportOptions
      format: "PNG",
      quality: 1.0,
      // addUserInfo: true, // Not available in ImageExportOptions
      // addWord: true, // Not available in ImageExportOptions
      // addBeatNumbers: true, // Not available in ImageExportOptions
      // addReversalSymbols: true, // Not available in ImageExportOptions
      // addDifficultyLevel: true, // Not available in ImageExportOptions
    },
  };

  return createImageExportState(exportService, presetOptions[purpose]);
}

/**
 * Batch export state for multiple sequences
 */
export function createBatchExportState(
  exportService: ITKAImageExportService
): ImageExportState & {
  batchProgress: { current: number; total: number };
  exportBatch: (sequences: SequenceData[]) => Promise<void>;
} {
  const baseState = createImageExportState(exportService);

  // Batch-specific state
  let batchProgress = $state({ current: 0, total: 0 });

  /**
   * Export multiple sequences
   */
  async function exportBatch(sequences: SequenceData[]): Promise<void> {
    if (!sequences || sequences.length === 0) {
      throw new Error("No sequences provided for batch export");
    }

    batchProgress = { current: 0, total: sequences.length };

    try {
      // Capture current options to avoid reactivity warning
      const currentOptions = baseState.exportOptions;
      await exportService.batchExport(
        sequences,
        currentOptions,
        (current: number, total: number) => {
          batchProgress = { current, total };
        }
      );
    } finally {
      batchProgress = { current: 0, total: 0 };
    }
  }

  return {
    ...baseState,
    get batchProgress() {
      return batchProgress;
    },
    exportBatch,
  };
}
