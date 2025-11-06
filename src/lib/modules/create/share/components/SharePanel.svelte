<!-- SharePanel.svelte - Full-Screen Modern Share Interface -->
<script lang="ts">
  import { browser } from "$app/environment";
  import type {
    IHapticFeedbackService,
    SequenceData,
    IDeviceDetector,
  } from "$shared";
  import { createServiceResolver, resolve, TYPES } from "$shared";
  import type { ResponsiveSettings } from "$shared/device/domain/models/device-models";
  import { onMount, untrack } from "svelte";
  import type { IShareService } from "../services/contracts";
  import { createShareState } from "../state";
  import ShareOptionsPanel from "./ShareOptionsPanel.svelte";
  import DownloadSection from "./ShareSection.svelte";
  import InstagramButton from "./InstagramButton.svelte";
  import InstagramLinkSheet from "./InstagramLinkSheet.svelte";
  import InstagramCarouselComposer from "./InstagramCarouselComposer.svelte";
  import { getInstagramLink } from "../domain";
  import type { InstagramLink } from "../domain";

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
    onSequenceUpdate,
  }: {
    currentSequence?: SequenceData | null;
    shareState?: ReturnType<typeof createShareState> | null;
    onClose?: () => void;
    onSequenceUpdate?: (sequence: SequenceData) => void;
  } = $props();

  // Instagram modal state
  let showInstagramModal = $state(false);

  // Instagram posting tab state
  let activeTab = $state<'download' | 'instagram'>('download');

  onMount(() => {
    // Service resolution
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );

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
  const shareServiceResolver = createServiceResolver<IShareService>(
    TYPES.IShareService
  );

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
    if (!shareState || !currentSequence || currentSequence.beats?.length === 0)
      return;

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

  // Instagram handlers
  function handleAddInstagramLink() {
    showInstagramModal = true;
  }

  function handleEditInstagramLink() {
    showInstagramModal = true;
  }

  function handleSaveInstagramLink(link: InstagramLink) {
    if (!currentSequence) return;

    // Update sequence metadata with Instagram link
    const updatedSequence = {
      ...currentSequence,
      metadata: {
        ...currentSequence.metadata,
        instagramLink: link,
      },
    };

    onSequenceUpdate?.(updatedSequence);
  }

  function handleRemoveInstagramLink() {
    if (!currentSequence) return;

    // Remove Instagram link from metadata
    const { instagramLink, ...restMetadata } = currentSequence.metadata;
    const updatedSequence = {
      ...currentSequence,
      metadata: restMetadata,
    };

    onSequenceUpdate?.(updatedSequence);
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

  let instagramLink = $derived(() => {
    if (!currentSequence) return null;
    return getInstagramLink(currentSequence.metadata);
  });

  // Handle successful Instagram post
  function handleInstagramPostSuccess(postUrl: string) {
    hapticService?.trigger("success");
    // Optionally switch back to download tab or show success message
    activeTab = 'download';
    // You could also show a toast notification here
    console.log("Successfully posted to Instagram!", postUrl);
  }
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
          <button class="retry-button" onclick={handleRetryPreview}
            >Try Again</button
          >
        </div>
      {:else if shareState?.previewUrl}
        <img
          src={shareState.previewUrl}
          alt="Sequence preview"
          class="preview-image"
        />
      {:else}
        <div class="preview-placeholder">
          <p>Preview will appear here</p>
        </div>
      {/if}
    </div>

    <!-- Right: Options & Share Button -->
    <div class="options-column">
      <!-- Tab Switcher -->
      <div class="tab-switcher">
        <button
          class="tab-button"
          class:active={activeTab === 'download'}
          onclick={() => (activeTab = 'download')}
        >
          <i class="fas fa-download"></i>
          Download
        </button>
        <button
          class="tab-button"
          class:active={activeTab === 'instagram'}
          onclick={() => (activeTab = 'instagram')}
        >
          <i class="fab fa-instagram"></i>
          Post to Instagram
        </button>
      </div>

      <!-- Tab Content -->
      {#if activeTab === 'download'}
        <!-- Download Tab -->
        {#if shareState?.options}
          <ShareOptionsPanel
            options={shareState.options}
            onOptionsChange={(newOptions) =>
              shareState?.updateOptions(newOptions)}
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

        <!-- Instagram Link (Legacy - kept for backwards compatibility) -->
        <div class="instagram-section">
          <h3>Link Instagram Post</h3>
          <p class="section-description">
            Link an existing Instagram post to this sequence
          </p>
          <InstagramButton
            instagramLink={instagramLink()}
            disabled={!currentSequence}
            onAddLink={handleAddInstagramLink}
            onEditLink={handleEditInstagramLink}
          />
        </div>
      {:else}
        <!-- Instagram Posting Tab -->
        <InstagramCarouselComposer
          {currentSequence}
          shareOptions={shareState?.options}
          onPostSuccess={handleInstagramPostSuccess}
        />
      {/if}
    </div>
  </div>
</div>

<!-- Instagram Link Sheet -->
<InstagramLinkSheet
  show={showInstagramModal}
  existingLink={instagramLink()}
  onSave={handleSaveInstagramLink}
  onRemove={handleRemoveInstagramLink}
  onClose={() => (showInstagramModal = false)}
/>

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
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
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
    overflow-y: auto;
    max-height: 100%;
  }

  /* Tab Switcher */
  .tab-switcher {
    display: flex;
    gap: 8px;
    padding: 6px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    margin: -12px -12px 0 -12px;
  }

  .tab-button {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 12px 16px;
    background: transparent;
    color: var(--text-secondary);
    border: none;
    border-radius: 8px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .tab-button:hover {
    background: rgba(255, 255, 255, 0.05);
    color: var(--text-primary);
  }

  .tab-button.active {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text-primary);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  .tab-button.active i {
    color: var(--accent-color);
  }

  .tab-button i.fa-instagram {
    background: linear-gradient(
      45deg,
      #f09433 0%,
      #e6683c 25%,
      #dc2743 50%,
      #cc2366 75%,
      #bc1888 100%
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  /* Instagram section */
  .instagram-section {
    padding: 1.5rem;
    background: var(--bg-secondary);
    border-radius: 8px;
    border: 1px solid var(--border-color);
  }

  .instagram-section h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-primary);
  }

  .instagram-section .section-description {
    margin: 0 0 1rem 0;
    font-size: 0.85rem;
    color: var(--text-secondary);
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
