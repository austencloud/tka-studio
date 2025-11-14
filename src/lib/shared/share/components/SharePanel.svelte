<!-- SharePanel.svelte - Modern Share Interface with Advanced Options -->
<script lang="ts">
  import { browser } from "$app/environment";
  import type {
    IHapticFeedbackService,
    SequenceData,
    IDeviceDetector,
  } from "$shared";
  import { createServiceResolver, resolve, TYPES } from "$shared";
  import type { ResponsiveSettings } from "$shared/device/domain/models/device-models";
  import { onMount } from "svelte";
  import type { IShareService } from "../services/contracts";
  import { createShareState } from "../state";
  import InstagramLinkSheet from "./InstagramLinkSheet.svelte";
  import ContentTypeSelector from "./ContentTypeSelector.svelte";
  import ImagePreviewDrawer from "./ImagePreviewDrawer.svelte";
  import { getInstagramLink } from "../domain";
  import type { InstagramLink } from "../domain";

  // Services
  let hapticService: IHapticFeedbackService;
  let deviceDetector: IDeviceDetector | null = null;

  // Reactive responsive settings from DeviceDetector
  let responsiveSettings = $state<ResponsiveSettings | null>(null);

  // Reactive mobile detection
  const isMobile = $derived(responsiveSettings?.isMobile ?? false);

  // Preview & Options drawer state
  let showPreviewDrawer = $state(false);

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

  // Content type state
  type ContentType = "video" | "animation" | "image";
  let selectedTypes = $state<ContentType[]>(["image"]);

  // Instagram modal state
  let showInstagramModal = $state(false);

  // Open preview drawer
  function openPreviewDrawer() {
    hapticService?.trigger("selection");
    showPreviewDrawer = true;
  }

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
    } catch (error) {
      console.error("Download failed:", error);
      hapticService?.trigger("error");
    }
  }

  async function handleShareViaDevice() {
    if (!shareState || !currentSequence || shareState.isDownloading) return;

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

    // If no native sharing available, show message
    alert(
      "Sharing not available on this device. Use the download button to save the image."
    );
    hapticService?.trigger("error");
  }

  async function handleInstagramPost() {
    hapticService?.trigger("selection");
    // Instagram posting will be handled by the InstagramCarouselComposer
    // For now, just trigger feedback
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

  // Handle toggle with haptic feedback
  function handleToggle(key: keyof NonNullable<typeof shareState>["options"]) {
    hapticService?.trigger("selection");
    if (!shareState) return;
    shareState.updateOptions({ [key]: !shareState.options[key] });
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
</script>

<div class="panel-content">
    <!-- Content Type Selector -->
    <section class="content-section">
      <ContentTypeSelector bind:selectedTypes />
    </section>

    <!-- Preview & Options Button -->
    {#if selectedTypes.includes("image")}
      <section class="preview-options-section">
        <button
          class="preview-options-button"
          onclick={openPreviewDrawer}
          disabled={!canShare()}
        >
          <i class="fas fa-eye"></i>
          <span>Preview & Options</span>
          <i class="fas fa-chevron-right"></i>
        </button>
      </section>
    {/if}

    <!-- Action Buttons -->
    <section class="actions-section">
      <div class="primary-actions">
        <button
          class="action-btn primary"
          disabled={!canShare()}
          onclick={handleDownload}
        >
          {#if shareState?.isDownloading}
            <span class="btn-spinner"></span>
          {:else}
            <i class="fas fa-download"></i>
          {/if}
          <span>Download</span>
        </button>

        <button
          class="action-btn secondary"
          disabled={!canShare()}
          onclick={handleShareViaDevice}
        >
          <i class="fas fa-share-nodes"></i>
          <span>Share via Device</span>
        </button>
      </div>

      <div class="divider">
        <span>Share to Social</span>
      </div>

      <div class="social-actions">
        <button
          class="action-btn social instagram"
          disabled={!canShare()}
          onclick={handleInstagramPost}
        >
          <i class="fab fa-instagram"></i>
          <span>Post to Instagram</span>
        </button>

        <button class="action-btn social facebook" disabled>
          <i class="fab fa-facebook"></i>
          <span>Post to Facebook</span>
        </button>
      </div>
    </section>
  </div>

<!-- Instagram Link Sheet -->
<InstagramLinkSheet
  show={showInstagramModal}
  existingLink={instagramLink()}
  onSave={handleSaveInstagramLink}
  onRemove={handleRemoveInstagramLink}
  onClose={() => (showInstagramModal = false)}
/>

<!-- Preview & Options Drawer -->
<ImagePreviewDrawer
  bind:isOpen={showPreviewDrawer}
  {currentSequence}
  {shareState}
  onRetryPreview={handleRetryPreview}
  onToggle={handleToggle}
/>

<style>
  /* Main Content Area */
  .panel-content {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 24px;
    padding: 24px;
    overflow-y: auto;
    overflow-x: hidden;
  }

  /* Preview & Options Button */
  .preview-options-button {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 16px 20px;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.12), rgba(37, 99, 235, 0.08));
    border: 1.5px solid rgba(59, 130, 246, 0.3);
    border-radius: 12px;
    color: rgba(255, 255, 255, 0.95);
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .preview-options-button:hover:not(:disabled) {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.18), rgba(37, 99, 235, 0.12));
    border-color: rgba(59, 130, 246, 0.4);
    transform: translateY(-1px);
  }

  .preview-options-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
  }


  /* Action button groups */
  .primary-actions,
  .social-actions {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px;
  }

  .divider {
    position: relative;
    text-align: center;
    margin: 12px 0;
  }

  .divider span {
    display: inline-block;
    padding: 0 18px;
    background: rgba(15, 20, 30, 0.96);
    color: rgba(255, 255, 255, 0.45);
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    position: relative;
    z-index: 1;
  }

  .divider::before {
    content: "";
    position: absolute;
    top: 50%;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(
      90deg,
      transparent 0%,
      rgba(255, 255, 255, 0.15) 20%,
      rgba(255, 255, 255, 0.15) 80%,
      transparent 100%
    );
  }

  .action-btn {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 16px 28px;
    border: none;
    border-radius: 14px;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    overflow: hidden;
    isolation: isolate;
  }

  .action-btn > * {
    position: relative;
    z-index: 2;
  }

  .action-btn::before {
    content: "";
    position: absolute;
    inset: 0;
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
    z-index: 0;
  }

  .action-btn::after {
    z-index: 1;
  }

  .action-btn:hover::before {
    opacity: 1;
  }

  .action-btn.primary {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
    box-shadow:
      0 4px 16px rgba(59, 130, 246, 0.4),
      0 2px 8px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.25);
    position: relative;
  }

  .action-btn.primary::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 14px;
    background: radial-gradient(
      circle at top left,
      rgba(255, 255, 255, 0.2),
      transparent 50%
    );
    pointer-events: none;
  }

  .action-btn.primary::before {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  }

  .action-btn.primary:hover:not(:disabled) {
    transform: scale(1.03) translateY(-2px);
    box-shadow:
      0 8px 24px rgba(59, 130, 246, 0.5),
      0 4px 12px rgba(0, 0, 0, 0.15),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }

  .action-btn.primary i {
    font-size: 18px;
    filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
  }

  .action-btn.secondary {
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.12),
      rgba(255, 255, 255, 0.08)
    );
    color: rgba(255, 255, 255, 0.95);
    border: 1.5px solid rgba(255, 255, 255, 0.25);
    box-shadow:
      0 2px 8px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.15);
    position: relative;
  }

  .action-btn.secondary::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 14px;
    background: radial-gradient(
      circle at top right,
      rgba(255, 255, 255, 0.1),
      transparent 60%
    );
    pointer-events: none;
  }

  .action-btn.secondary::before {
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.18),
      rgba(255, 255, 255, 0.12)
    );
  }

  .action-btn.secondary:hover:not(:disabled) {
    transform: scale(1.02) translateY(-1px);
    border-color: rgba(255, 255, 255, 0.35);
    box-shadow:
      0 4px 12px rgba(0, 0, 0, 0.15),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
  }

  .action-btn.secondary i {
    font-size: 18px;
    opacity: 0.9;
  }

  .action-btn.social {
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.08),
      rgba(255, 255, 255, 0.04)
    );
    color: rgba(255, 255, 255, 0.95);
    border: 1.5px solid rgba(255, 255, 255, 0.18);
    box-shadow:
      0 2px 8px rgba(0, 0, 0, 0.08),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
  }

  .action-btn.social::before {
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.12),
      rgba(255, 255, 255, 0.06)
    );
  }

  .action-btn.social:hover:not(:disabled) {
    transform: scale(1.02) translateY(-1px);
    border-color: rgba(255, 255, 255, 0.28);
    box-shadow:
      0 4px 12px rgba(0, 0, 0, 0.12),
      inset 0 1px 0 rgba(255, 255, 255, 0.15);
  }

  /* Instagram button - colorful gradient */
  .action-btn.instagram {
    background: linear-gradient(
      135deg,
      #f09433 0%,
      #e6683c 25%,
      #dc2743 50%,
      #cc2366 75%,
      #bc1888 100%
    );
    border: none;
    color: white;
    box-shadow:
      0 4px 16px rgba(188, 24, 136, 0.35),
      0 2px 8px rgba(0, 0, 0, 0.15),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
  }

  .action-btn.instagram::before {
    background: linear-gradient(
      135deg,
      #e6683c 0%,
      #dc2743 25%,
      #cc2366 50%,
      #bc1888 75%,
      #8a0868 100%
    );
  }

  .action-btn.instagram:hover:not(:disabled) {
    transform: scale(1.03) translateY(-2px);
    box-shadow:
      0 8px 24px rgba(188, 24, 136, 0.5),
      0 4px 12px rgba(0, 0, 0, 0.2),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }

  .action-btn.instagram i {
    font-size: 18px;
    filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.3));
  }

  /* Facebook button styling */
  .action-btn.facebook {
    position: relative;
  }

  .action-btn.facebook i {
    color: #1877f2;
    font-size: 18px;
  }

  .action-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
  }

  .action-btn:disabled::before {
    display: none;
  }

  .btn-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top: 2px solid white;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }


  /* Section spacing and animations */
  .content-section,
  .preview-options-section,
  .actions-section {
    animation: fadeIn 0.4s ease-out backwards;
  }

  .content-section {
    animation-delay: 0.05s;
  }

  .preview-options-section {
    animation-delay: 0.1s;
  }

  .actions-section {
    animation-delay: 0.15s;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(8px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
    }

    .action-btn:hover {
      transform: none !important;
    }
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .panel-content {
      padding: 16px;
      gap: 20px;
    }

    .primary-actions,
    .social-actions {
      grid-template-columns: 1fr;
    }
  }
</style>
