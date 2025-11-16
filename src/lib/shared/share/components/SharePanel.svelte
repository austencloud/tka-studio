<!-- SharePanel.svelte - Modern Share Interface with Advanced Options -->
<script lang="ts">
  import { browser } from "$app/environment";
  import type { IHapticFeedbackService, SequenceData } from "$shared";
  import { createServiceResolver, resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { IShareService } from "../services/contracts";
  import { createShareState } from "../state";
  import InstagramLinkSheet from "./InstagramLinkSheet.svelte";
  import ContentTypeSelector from "./ContentTypeSelector.svelte";
  import ImagePreviewDrawer from "./ImagePreviewDrawer.svelte";
  import PreviewOptionsButton from "./PreviewOptionsButton.svelte";
  import PrimaryActions from "./PrimaryActions.svelte";
  import SocialActions from "./SocialActions.svelte";
  import SectionDivider from "./SectionDivider.svelte";
  import { getInstagramLink } from "../domain";
  import type { InstagramLink } from "../domain";

  // Services
  let hapticService: IHapticFeedbackService;

  // Preview & Options drawer state
  let showPreviewDrawer = $state(false);

  let {
    currentSequence = null,
    shareState: providedShareState = null,
    onSequenceUpdate,
  }: {
    currentSequence?: SequenceData | null;
    shareState?: ReturnType<typeof createShareState> | null;
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

    try {
      // Use the share service to handle all sharing logic
      const shareService = resolve<IShareService>(TYPES.IShareService);
      await shareService.shareViaDevice(currentSequence, shareState.options);
      hapticService?.trigger("success");
    } catch (error) {
      // Handle user cancellation or errors
      if (error instanceof Error && error.name === "AbortError") {
        // User cancelled the share - no error feedback needed
        return;
      }

      // Show error message for actual failures
      const message =
        error instanceof Error
          ? error.message
          : "Sharing failed. Please try downloading instead.";
      alert(message);
      hapticService?.trigger("error");
    }
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
      <PreviewOptionsButton canShare={canShare()} onClick={openPreviewDrawer} />
    </section>
  {/if}

  <!-- Action Buttons -->
  <section class="actions-section">
    <PrimaryActions
      canShare={canShare()}
      isDownloading={shareState?.isDownloading}
      onDownload={handleDownload}
      onShare={handleShareViaDevice}
    />

    <SectionDivider label="Share to Social" />

    <SocialActions
      canShare={canShare()}
      onInstagramPost={handleInstagramPost}
    />
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
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .panel-content {
      padding: 16px;
      gap: 20px;
    }
  }
</style>
