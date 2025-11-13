<!-- ShareSection.svelte - Share button component -->
<script lang="ts">
  import type { IHapticFeedbackService, SequenceData } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  let {
    currentSequence,
    canDownload = false,
    isDownloading = false,
    isMobile = false,
    onDownload,
    onShowExportModal,
    shareState,
  }: {
    currentSequence?: SequenceData | null;
    canDownload?: boolean;
    isDownloading?: boolean;
    isMobile?: boolean;
    onDownload?: () => void;
    onShowExportModal?: () => void;
    shareState?: any; // ShareState type
  } = $props();

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Handle share button click - ONLY share, don't download
  async function handleShareClick() {
    if (!canDownload || isDownloading || !currentSequence || !shareState)
      return;
    hapticService?.trigger("selection");

    // Try native sharing with actual image file
    if (navigator.share && navigator.canShare) {
      try {
        // Get the actual image blob from the share service
        const shareService = resolve<any>(TYPES.IShareService);
        const blob = await shareService.getImageBlob(
          currentSequence,
          shareState.options
        );

        // Create a File object with optimal metadata for Android sharing
        const filename = shareService.generateFilename(
          currentSequence,
          shareState.options
        );

        // Ensure proper MIME type based on format
        const mimeType =
          shareState.options.format === "PNG"
            ? "image/png"
            : shareState.options.format === "JPEG"
              ? "image/jpeg"
              : "image/webp";

        const file = new File([blob], filename, {
          type: mimeType,
          lastModified: Date.now(),
        });

        // Get image dimensions for debugging
        const img = new Image();
        const imageUrl = URL.createObjectURL(blob);

        await new Promise((resolve) => {
          img.onload = () => {
            URL.revokeObjectURL(imageUrl);
            resolve(null);
          };
          img.src = imageUrl;
        });

        // Check if we can share files
        const shareData = {
          title: "TKA Sequence",
          text: `Check out this TKA sequence: ${currentSequence?.name || "Untitled"}`,
          files: [file],
        };

        if (navigator.canShare(shareData)) {
          await navigator.share(shareData);
          hapticService?.trigger("success");
          return;
        } else {
          // Fallback to URL sharing if file sharing not supported
          await navigator.share({
            title: "TKA Sequence",
            text: `Check out this TKA sequence: ${currentSequence?.name || "Untitled"}`,
            url: window.location.href,
          });
          hapticService?.trigger("success");
          return;
        }
      } catch (error) {
        // Native sharing failed or was cancelled (user closed share dialog)
        hapticService?.trigger("error");
        return;
      }
    }

    // If no native sharing available, show message instead of downloading
    alert(
      "Sharing not available on this device. Use the download button to save the image."
    );
    hapticService?.trigger("error");
  }

  // Computed state for share button
  let shareButtonState = $derived(() => {
    const hasSequence = currentSequence && currentSequence.beats?.length > 0;
    const isReady = canDownload && hasSequence && !isDownloading;

    return {
      disabled: !isReady,
      showSpinner: isDownloading,
      canInteract: isReady,
    };
  });

  // Extract individual properties for easier access
  let isButtonDisabled = $derived(() => shareButtonState().disabled);
  let showSpinner = $derived(() => shareButtonState().showSpinner);
</script>

<button
  class="share-btn"
  class:disabled={isButtonDisabled()}
  onclick={handleShareClick}
  disabled={isButtonDisabled()}
>
  {#if showSpinner()}
    <span class="loading-spinner"></span>
  {:else}
    <i class="fas fa-share-nodes"></i>
  {/if}
  <span class="btn-text">Share</span>
</button>

<style>
  /* Modern 2026 Share Button - Spring Animation & Blue Gradient */
  .share-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 12px 24px;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    border: none;
    border-radius: 12px;
    color: rgba(255, 255, 255, 0.98);
    font-size: 15px;
    font-weight: 600;
    letter-spacing: -0.01em;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    box-shadow:
      0 4px 16px rgba(59, 130, 246, 0.3),
      0 2px 4px rgba(0, 0, 0, 0.1);
    position: relative;
    overflow: hidden;
  }

  .share-btn:hover:not(.disabled) {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    transform: scale(1.04) translateY(-2px);
    box-shadow:
      0 0 24px rgba(59, 130, 246, 0.5),
      0 8px 24px rgba(59, 130, 246, 0.25),
      0 4px 8px rgba(0, 0, 0, 0.15);
  }

  .share-btn:active:not(.disabled) {
    transform: scale(0.98);
    transition: all 0.15s ease;
    box-shadow:
      0 2px 12px rgba(59, 130, 246, 0.3),
      0 1px 3px rgba(0, 0, 0, 0.1);
  }

  .share-btn:focus-visible {
    outline: 3px solid rgba(59, 130, 246, 0.4);
    outline-offset: 2px;
  }

  .share-btn.disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
    box-shadow:
      0 2px 8px rgba(59, 130, 246, 0.15),
      0 1px 2px rgba(0, 0, 0, 0.05);
  }

  .share-btn i {
    font-size: 17px;
  }

  .btn-text {
    font-weight: 600;
  }

  .loading-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top: 2px solid currentColor;
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

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .share-btn {
      transition: none;
    }

    .share-btn:hover:not(.disabled),
    .share-btn:active:not(.disabled) {
      transform: none;
    }

    .loading-spinner {
      animation: none;
      border-top-color: transparent;
      opacity: 0.7;
    }
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .share-btn {
      padding: 10px 20px;
      font-size: 14px;
      border-radius: 10px;
    }

    .share-btn i {
      font-size: 16px;
    }
  }
</style>
