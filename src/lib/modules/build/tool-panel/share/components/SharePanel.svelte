<!-- SharePanel.svelte - Refactored Share Interface with Proper Architecture -->
<script lang="ts">
  import { browser } from "$app/environment";
  import type { IHapticFeedbackService, SequenceData } from "$shared";
  import { createServiceResolver, resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { IShareService } from "../services/contracts";
  import { createShareState } from "../state";
  import OptionsModal from "./OptionsModal.svelte";
  import PreviewSection from "./PreviewSection.svelte";
  import DownloadSection from "./ShareSection.svelte";

  // Component state
  let isMobile = $state(false);
  let showShareModal = $state(false);
  let hapticService: IHapticFeedbackService;

  let {
    currentSequence = null,
  }: {
    currentSequence?: SequenceData | null;
  } = $props();

  onMount(() => {
    // Device detection
    const checkMobile = () => {
      isMobile = window.innerWidth <= 767;
    };

    checkMobile();
    window.addEventListener("resize", checkMobile);

    // Service resolution
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);

    return () => {
      window.removeEventListener("resize", checkMobile);
    };
  });

  // HMR-safe service resolution
  const shareServiceResolver = createServiceResolver<IShareService>(TYPES.IShareService);

  // Create share state reactively when service becomes available
  let shareState = $state<ReturnType<typeof createShareState> | null>(null);

  $effect(() => {
    if (shareServiceResolver.value) {
      shareState = createShareState(shareServiceResolver.value);
    } else {
      shareState = null;
    }
  });

  // Auto-generate preview when sequence or options change
  $effect(() => {
    if (shareState && currentSequence && currentSequence.beats?.length > 0) {
      shareState.generatePreview(currentSequence);
    }
  });

  // Event handlers
  async function handleDownload() {
    if (!shareState || !currentSequence || shareState.isDownloading) return;

    try {
      await shareState.downloadImage(currentSequence);
      hapticService?.trigger("success");
    } catch (error) {
      console.error("Download failed:", error);
      hapticService?.trigger("error");
    }
  }

  function handleShowOptionsModal() {
    showShareModal = true;
  }

  function handleCloseOptionsModal() {
    showShareModal = false;
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
  <!-- Header -->


  <!-- Main content -->
  <div class="share-content">
    <!-- Top: Preview -->
    <div class="preview-section">
      <PreviewSection
        {currentSequence}
        previewUrl={shareState?.previewUrl}
        isGenerating={shareState?.isGeneratingPreview || false}
        error={shareState?.previewError}
        onRetry={handleRetryPreview}
      />
    </div>

    <!-- Bottom: Actions (Customize + Share/Download) -->
    <div class="actions-section">
      <button
        class="customize-btn"
        onclick={handleShowOptionsModal}
        disabled={!canShare()}
      >
        <i class="fas fa-cog"></i>
        Customize
      </button>

      <DownloadSection
        {currentSequence}
        canDownload={canShare()}
        isDownloading={shareState?.isDownloading || false}
        {isMobile}
        {shareState}
        onDownload={handleDownload}
        onShowExportModal={handleShowOptionsModal}
      />
    </div>
  </div>

  <!-- Modal -->
  <OptionsModal
    show={showShareModal}
    {currentSequence}
    {shareState}
    {isMobile}
    onClose={handleCloseOptionsModal}
    onDownload={handleDownload}
  />
</div>

<style>
  .share-panel {
    display: flex;
    flex-direction: column;
    /* Multi-layer fallback for reliable viewport height */
    height: 100vh; /* Fallback 1: Static viewport height */
    height: var(--viewport-height, 100vh); /* Fallback 2: JS-calculated height */
    height: 100dvh; /* Preferred: Dynamic viewport height (when it works) */
    max-height: 100vh;
    max-height: var(--viewport-height, 100vh);
    max-height: 100dvh;
    padding: 1rem;
    position: relative;
    overflow: hidden;
    box-sizing: border-box;
  }

  .share-content {
    display: flex;
    flex-direction: column;
    flex: 1;
    min-height: 0;
    overflow: hidden;
    container-type: size;
    container-name: share-content;
    gap: 1rem;
  }

  .preview-section {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
  }

  .actions-section {
    flex-shrink: 0;
    display: flex;
    flex-direction: row;
    gap: 0.75rem;
  }

  .actions-section > :global(*) {
    flex: 1;
  }

  .customize-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    padding: 0.875rem 1.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    border-radius: 6px;
    color: white;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    position: relative;
    overflow: hidden;
    flex: 1;
  }

  .customize-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.5s ease;
  }

  .customize-btn:hover:not(:disabled) {
    background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
  }

  .customize-btn:hover:not(:disabled)::before {
    left: 100%;
  }

  .customize-btn:active:not(:disabled) {
    transform: translateY(0);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  }

  .customize-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }

  .customize-btn i {
    font-size: 1.1rem;
  }

  /* Container Queries for Responsive Gap */
  @container share-content (max-height: 400px) {
    .share-content {
      gap: 0.5rem;
    }
  }

  @container share-content (min-height: 401px) and (max-height: 600px) {
    .share-content {
      gap: 1rem;
    }
  }

  @container share-content (min-height: 601px) and (max-height: 800px) {
    .share-content {
      gap: 1.5rem;
    }
  }

  @container share-content (min-height: 801px) {
    .share-content {
      gap: 2rem;
    }
  }

  /* Responsive Design */
  @media (max-width: 767px) {
    .share-panel {
      padding: 0.75rem;
      /* svh already applied above */
    }



    .preview-section {
      min-height: 0;
      flex: 1;
    }
  }
</style>
