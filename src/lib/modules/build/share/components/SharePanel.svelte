<!-- SharePanel.svelte - Full-Screen Modern Share Interface -->
<script lang="ts">
  import { browser } from "$app/environment";
  import type { IHapticFeedbackService, SequenceData, IDeviceDetector } from "$shared";
  import { createServiceResolver, resolve, TYPES } from "$shared";
  import type { ResponsiveSettings } from "$shared/device/domain/models/device-models";
  import { onMount, untrack } from "svelte";
  import type { IShareService } from "../services/contracts";
  import { createShareState } from "../state";
  import ShareOptionsPanel from "./ShareOptionsPanel.svelte";
  import DownloadSection from "./ShareSection.svelte";

  // Services
  let hapticService: IHapticFeedbackService;
  let deviceDetector: IDeviceDetector | null = null;

  // Reactive responsive settings from DeviceDetector
  let responsiveSettings = $state<ResponsiveSettings | null>(null);

  // Reactive mobile detection
  const isMobile = $derived(responsiveSettings?.isMobile ?? false);

  let {
    currentSequence = null,
    shareState: providedShareState = null,
    onClose,
  }: {
    currentSequence?: SequenceData | null;
    shareState?: ReturnType<typeof createShareState> | null;
    onClose?: () => void;
  } = $props();

  onMount(() => {
    // Service resolution
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);

    // Initialize DeviceDetector service
    try {
      deviceDetector = resolve<IDeviceDetector>(TYPES.IDeviceDetector);
      responsiveSettings = deviceDetector.getResponsiveSettings();

      // Return cleanup function from onCapabilitiesChanged
      return deviceDetector.onCapabilitiesChanged(() => {
        responsiveSettings = deviceDetector!.getResponsiveSettings();
      });
    } catch (error) {
      console.warn("SharePanel: Failed to resolve DeviceDetector", error);
    }

    return undefined;
  });

  // HMR-safe service resolution
  const shareServiceResolver = createServiceResolver<IShareService>(TYPES.IShareService);

  // Use provided share state or create a new one when service becomes available
  let shareState = $state<ReturnType<typeof createShareState> | null>(null);

  $effect(() => {
    // If a share state was provided (from background rendering), use it
    if (providedShareState) {
      shareState = providedShareState;
    } else if (shareServiceResolver.value) {
      // Otherwise create a new share state
      shareState = createShareState(shareServiceResolver.value);
    } else {
      shareState = null;
    }
  });

  // Only run preview generation effect when NOT using a provided state
  // When using provided state, ShareCoordinator handles all rendering
  $effect(() => {
    // Skip entirely if using provided state
    if (providedShareState) return;

    // Only for self-managed state (no background rendering)
    if (!shareState || !currentSequence || currentSequence.beats?.length === 0) return;

    // Track options as a dependency (so effect re-runs when options change)
    const options = shareState.options;

    // Generate preview when sequence or options change
    shareState.generatePreview(currentSequence);
  });

  // Event handlers
  async function handleDownload() {
    if (!shareState || !currentSequence || shareState.isDownloading) return;

    try {
      await shareState.downloadImage(currentSequence);
      hapticService?.trigger("success");
      // Optionally close panel after successful download
      // onClose?.();
    } catch (error) {
      console.error("Download failed:", error);
      hapticService?.trigger("error");
    }
  }

  function handleRetryPreview() {
    if (currentSequence && shareState) {
      shareState.generatePreview(currentSequence);
    }
  }

  // Computed properties
  let canShare = $derived(() => {
    return Boolean(
      browser &&
      shareState &&
      currentSequence &&
      currentSequence.beats?.length > 0 &&
      !shareState.isDownloading
    );
  });
</script>

<div class="share-panel">
  <div class="share-grid">
    <!-- Left: Preview Image -->
    <div class="preview-column">
      {#if !currentSequence}
        <div class="preview-placeholder">
          <p>No sequence selected</p>
          <span>Create or select a sequence to see preview</span>
        </div>
      {:else if currentSequence.beats?.length === 0}
        <div class="preview-placeholder">
          <p>Empty sequence</p>
          <span>Add beats to generate preview</span>
        </div>
      {:else if shareState?.isGeneratingPreview}
        <div class="preview-loading">
          <div class="loading-spinner"></div>
          <p>Generating preview...</p>
        </div>
      {:else if shareState?.previewError}
        <div class="preview-error">
          <p>Preview failed</p>
          <span>{shareState.previewError}</span>
          <button class="retry-button" onclick={handleRetryPreview}>Try Again</button>
        </div>
      {:else if shareState?.previewUrl}
        <img src={shareState.previewUrl} alt="Sequence preview" class="preview-image" />
      {:else}
        <div class="preview-placeholder">
          <p>Preview will appear here</p>
        </div>
      {/if}
    </div>

    <!-- Right: Options & Share Button -->
    <div class="options-column">
      {#if shareState?.options}
        <ShareOptionsPanel
          options={shareState.options}
          onOptionsChange={(newOptions) => shareState?.updateOptions(newOptions)}
        />
      {/if}

      <DownloadSection
        {currentSequence}
        canDownload={canShare()}
        isDownloading={shareState?.isDownloading || false}
        {isMobile}
        {shareState}
        onDownload={handleDownload}
        onShowExportModal={() => {}}
      />
    </div>
  </div>
</div>

<style>
  /* Clean container */
  .share-panel {
    height: 100%;
    width: 100%;
  }

  /* Simple two-column grid - no height forcing */
  .share-grid {
    display: grid;
    grid-template-columns: minmax(0, 1.5fr) minmax(300px, 500px);
    grid-auto-rows: max-content;
    align-items: start;
    gap: 20px;
    height: 100%;
    padding: 20px;
  }

  /* Preview Column - just contains the image */
  .preview-column {
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 16px;
    padding: 24px;
    overflow: hidden;
    height: 100%;
  }

  /* Preview image - fits container naturally */
  .preview-image {
    max-width: 100%;
    max-height: 100%;
    width: auto;
    height: auto;
    object-fit: contain;
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  }

  /* Preview states */
  .preview-placeholder,
  .preview-loading,
  .preview-error {
    text-align: center;
    color: rgba(255, 255, 255, 0.7);
    display: flex;
    flex-direction: column;
    gap: 12px;
    align-items: center;
  }

  .preview-placeholder p,
  .preview-loading p,
  .preview-error p {
    font-size: 16px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
    margin: 0;
  }

  .preview-placeholder span,
  .preview-error span {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.5);
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-top: 3px solid rgba(59, 130, 246, 0.8);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .retry-button {
    margin-top: 8px;
    padding: 10px 20px;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  .retry-button:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4);
  }

  /* Options Column - natural stacking, no forced spacing */
  .options-column {
    display: flex;
    flex-direction: column;
    align-content: flex-start;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 16px;
    padding: 24px;
    gap: 20px;
  }

  /* Tablet/Mobile Layout */
  @media (max-width: 1024px) {
    .share-grid {
      grid-template-columns: 1fr;
      gap: 12px;
      padding: 12px 16px 16px;
    }

    .preview-column,
    .options-column {
      padding: 14px;
    }
  }

  @media (max-width: 768px) {
    .share-grid {
      padding: 12px;
      gap: 10px;
    }

    .preview-column,
    .options-column {
      padding: 12px;
      border-radius: 10px;
    }
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    .preview-column,
    .options-column {
      background: rgba(0, 0, 0, 0.95);
      border: 2px solid white;
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    * {
      transition: none !important;
      animation: none !important;
    }
  }
</style>
