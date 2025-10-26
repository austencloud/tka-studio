/**
 * Share State Management
 *
 * Reactive state for the share interface using Svelte 5 runes.
 */

import type { SequenceData } from '$shared';
import type { ShareOptions } from '../domain';
import { SHARE_PRESETS } from '../domain';
import type { IShareService } from '../services/contracts';

export interface ShareState {
  // Current options
  readonly options: ShareOptions;
  readonly selectedPreset: string;

  // Preview state
  readonly previewUrl: string | null;
  readonly isGeneratingPreview: boolean;
  readonly previewError: string | null;

  // Download state
  readonly isDownloading: boolean;
  readonly downloadError: string | null;
  readonly lastDownloadedFile: string | null;

  // Actions
  updateOptions: (newOptions: Partial<ShareOptions>) => void;
  selectPreset: (presetName: string) => void;
  generatePreview: (sequence: SequenceData) => Promise<void>;
  downloadImage: (sequence: SequenceData, filename?: string) => Promise<void>;
  resetErrors: () => void;
}

export function createShareState(shareService: IShareService): ShareState {
  // Reactive state using Svelte 5 runes
  let options = $state<ShareOptions>({ ...SHARE_PRESETS.social.options });
  let selectedPreset = $state<string>('social');

  let previewUrl = $state<string | null>(null);
  let isGeneratingPreview = $state<boolean>(false);
  let previewError = $state<string | null>(null);

  let isDownloading = $state<boolean>(false);
  let downloadError = $state<string | null>(null);
  let lastDownloadedFile = $state<string | null>(null);

  return {
    // Getters
    get options() { return options; },
    get selectedPreset() { return selectedPreset; },
    get previewUrl() { return previewUrl; },
    get isGeneratingPreview() { return isGeneratingPreview; },
    get previewError() { return previewError; },
    get isDownloading() { return isDownloading; },
    get downloadError() { return downloadError; },
    get lastDownloadedFile() { return lastDownloadedFile; },

    // Actions
    updateOptions: (newOptions: Partial<ShareOptions>) => {
      console.log('🔧 ShareState: Before update - options:', options);
      console.log('🔧 ShareState: Applying new options:', newOptions);
      options = { ...options, ...newOptions };
      console.log('🔧 ShareState: After update - options:', options);
      selectedPreset = 'custom'; // Mark as custom when manually changed
      previewError = null; // Clear preview error when options change
    },

    selectPreset: (presetName: string) => {
      const preset = SHARE_PRESETS[presetName];
      if (preset) {
        options = { ...preset.options };
        selectedPreset = presetName;
        previewError = null;
      }
    },

    generatePreview: async (sequence: SequenceData) => {
      if (!sequence) return;

      isGeneratingPreview = true;
      previewError = null;

      try {
        // Validate options first
        const validation = shareService.validateOptions(options);
        if (!validation.valid) {
          throw new Error(`Invalid options: ${validation.errors.join(', ')}`);
        }

        // Generate preview
        const newPreviewUrl = await shareService.generatePreview(sequence, options);

        // Clean up old preview URL
        if (previewUrl) {
          URL.revokeObjectURL(previewUrl);
        }

        previewUrl = newPreviewUrl;
      } catch (error) {
        previewError = error instanceof Error ? error.message : 'Failed to generate preview';
        console.error('Preview generation failed:', error);
      } finally {
        isGeneratingPreview = false;
      }
    },

    downloadImage: async (sequence: SequenceData, filename?: string) => {
      if (!sequence) return;

      isDownloading = true;
      downloadError = null;

      try {
        // Validate options first
        const validation = shareService.validateOptions(options);
        if (!validation.valid) {
          throw new Error(`Invalid options: ${validation.errors.join(', ')}`);
        }

        // Download image
        await shareService.downloadImage(sequence, options, filename);

        // Track successful download
        lastDownloadedFile = filename || shareService.generateFilename(sequence, options);
      } catch (error) {
        downloadError = error instanceof Error ? error.message : 'Failed to download image';
        console.error('Download failed:', error);
      } finally {
        isDownloading = false;
      }
    },

    resetErrors: () => {
      previewError = null;
      downloadError = null;
    }
  };
}
