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
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });

  // Handle share button click - ONLY share, don't download
  async function handleShareClick() {
    if (!canDownload || isDownloading || !currentSequence || !shareState) return;
    hapticService?.trigger("navigation");

    // Try native sharing with actual image file
    if (navigator.share && navigator.canShare) {
      try {
        // Get the actual image blob from the share service
        const shareService = resolve(TYPES.IShareService) as any;
        const blob = await shareService.getImageBlob(currentSequence, shareState.options);

        // Create a File object with optimal metadata for Android sharing
        const filename = shareService.generateFilename(currentSequence, shareState.options);

        // Ensure proper MIME type based on format
        const mimeType = shareState.options.format === 'PNG' ? 'image/png' :
                        shareState.options.format === 'JPEG' ? 'image/jpeg' :
                        'image/webp';

        const file = new File([blob], filename, {
          type: mimeType,
          lastModified: Date.now()
        });

        // Get image dimensions for debugging
        const img = new Image();
        const imageUrl = URL.createObjectURL(blob);

        await new Promise((resolve) => {
          img.onload = () => {
            console.log('Sharing image:', {
              filename,
              type: mimeType,
              size: blob.size,
              sizeKB: Math.round(blob.size / 1024),
              dimensions: `${img.width}x${img.height}`,
              aspectRatio: (img.width / img.height).toFixed(2)
            });
            URL.revokeObjectURL(imageUrl);
            resolve(null);
          };
          img.src = imageUrl;
        });

        // Check if we can share files
        const shareData = {
          title: 'TKA Sequence',
          text: `Check out this TKA sequence: ${currentSequence?.name || 'Untitled'}`,
          files: [file]
        };

        if (navigator.canShare(shareData)) {
          await navigator.share(shareData);
          hapticService?.trigger("success");
          return;
        } else {
          // Fallback to URL sharing if file sharing not supported
          await navigator.share({
            title: 'TKA Sequence',
            text: `Check out this TKA sequence: ${currentSequence?.name || 'Untitled'}`,
            url: window.location.href
          });
          hapticService?.trigger("success");
          return;
        }
      } catch (error) {
        console.log('Native sharing failed or was cancelled:', error);
        hapticService?.trigger("error");
        return;
      }
    }

    // If no native sharing available, show message instead of downloading
    alert('Sharing not available on this device. Use the download button to save the image.');
    hapticService?.trigger("error");
  }

  // Computed state for share button
  let shareButtonState = $derived(() => {
    const hasSequence = currentSequence && currentSequence.beats?.length > 0;
    const isReady = canDownload && hasSequence && !isDownloading;

    return {
      disabled: !isReady,
      showSpinner: isDownloading,
      canInteract: isReady
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
  .share-btn {
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
  }

  .share-btn:hover:not(.disabled) {
    background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
  }

  .share-btn:active:not(.disabled) {
    transform: translateY(0);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  }

  .share-btn.disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }

  .share-btn i {
    font-size: 1.1rem;
  }

  .btn-text {
    font-weight: 500;
  }

  .loading-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid transparent;
    border-top: 2px solid currentColor;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }


</style>
