<!--
@component GalleryThumbnail

Displays an individual sequence thumbnail with image, metadata, and action buttons.
This component is the primary building block of the gallery display system.

@prop {SequenceData} sequence - The sequence data to display
@prop {IGalleryThumbnailService} thumbnailService - Service for generating thumbnail URLs
@prop {"grid" | "list"} [viewMode="grid"] - Display mode (grid or list layout)
@prop {boolean} [isFavorite=false] - Whether the sequence is marked as favorite
@prop {boolean} [priority=false] - If true, loads image eagerly (for above-the-fold content)
@prop {(sequenceId: string) => void} [onFavoriteToggle] - Callback when favorite is toggled
@prop {(action: string, sequence: SequenceData) => void} [onAction] - Callback for user actions

@fires action - Emitted when user performs an action (fullscreen, edit, delete, etc.)

@example
```svelte
<GalleryThumbnail
  sequence={mySequence}
  thumbnailService={thumbnailService}
  viewMode="grid"
  priority={true}
  onAction={(action, seq) => {
    if (action === 'fullscreen') openFullscreen(seq);
  }}
/>
```

@accessibility
- Full keyboard navigation support (Enter/Space to activate)
- ARIA labels describe sequence and available actions
- Focus indicators for keyboard users
- Screen reader friendly

@performance
- Lazy loading for off-screen images
- Priority loading for above-the-fold content
- Skeleton loading states for perceived performance

SequenceThumbnail Component - Refactored Implementation

Displays individual sequence thumbnails using extracted components for better
separation of concerns and maintainability.

Updated UX: Clicking thumbnail opens fullscreen view directly.
-->
<script lang="ts">
  import type { SequenceData } from "$shared";
  import { onMount } from "svelte";
  import type { IHapticFeedbackService } from "../../../../shared/application/services/contracts";
  import { resolve, TYPES } from "../../../../shared/inversify";
  import type { IGalleryThumbnailService } from "../services/contracts/IGalleryThumbnailService";
  import ThumbnailActions from "./GalleryThumbnailActions.svelte";
  import ThumbnailImage from "./GalleryThumbnailImage.svelte";
  import ThumbnailMetadata from "./GalleryThumbnailMetadata.svelte";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    sequence,
    thumbnailService,
    viewMode = "grid",
    isFavorite = false,
    priority = false, // For above-the-fold images
    onFavoriteToggle = () => {},
    onAction = () => {},
  } = $props<{
    sequence: SequenceData;
    thumbnailService: IGalleryThumbnailService;
    viewMode?: "grid" | "list";
    isFavorite?: boolean;
    priority?: boolean; // Load immediately if true
    onFavoriteToggle?: (sequenceId: string) => void;
    onAction?: (action: string, sequence: SequenceData) => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService | null = $state(null);

  // Extract dimensions from sequence metadata if available
  const imageDimensions = $derived.by(() => {
    const metadata = sequence.metadata as any;
    return {
      width: metadata?.width,
      height: metadata?.height,
    };
  });

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Event handlers - Updated for new UX: click to open fullscreen
  function handleClick() {
    hapticService?.trigger("selection");
    // New UX: Default click behavior is to view fullscreen
    onAction("fullscreen", sequence);
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Enter" || event.key === " ") {
      hapticService?.trigger("selection");
      event.preventDefault();
      // New UX: Default keyboard behavior is to view fullscreen
      onAction("fullscreen", sequence);
    }
  }

  // Generate accessible label for the thumbnail
  const accessibleLabel = $derived(
    `${sequence.word} sequence, ${sequence.sequenceLength} beats. Click to view fullscreen.`
  );
</script>

<!-- Thumbnail container with responsive design -->
<div
  class="sequence-thumbnail"
  class:list-view={viewMode === "list"}
  class:grid-view={viewMode === "grid"}
  role="button"
  tabindex="0"
  aria-label={accessibleLabel}
  title={accessibleLabel}
  onclick={handleClick}
  onkeydown={handleKeydown}
>
  <!-- Image component -->
  <ThumbnailImage
    sequenceId={sequence.id}
    sequenceWord={sequence.word}
    thumbnails={sequence.thumbnails}
    {thumbnailService}
    {priority}
    width={imageDimensions.width}
    height={imageDimensions.height}
  />

  <!-- Action buttons component -->
  <ThumbnailActions {sequence} {isFavorite} {onFavoriteToggle} {onAction} />

  <!-- Metadata component -->
  <ThumbnailMetadata
    {sequence}
    {viewMode}
    showExtendedInfo={viewMode === "list"}
  />
</div>

<style>
  .sequence-thumbnail {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex;
    flex-direction: column;
    position: relative;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    height: 100%;
  }

  .sequence-thumbnail:hover {
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(16px);
    border-color: rgba(255, 255, 255, 0.25);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  }

  .sequence-thumbnail:focus {
    outline: 2px solid rgba(255, 255, 255, 0.4);
    outline-offset: 2px;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(16px);
  }

  /* Grid view (default) - Image container takes remaining space */
  .sequence-thumbnail :global(.image-container) {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  /* Metadata section stays at bottom */
  .sequence-thumbnail :global(.metadata-section) {
    flex-shrink: 0;
    margin-top: auto;
  }

  /* List view */
  .list-view {
    flex-direction: row;
    height: 120px;
    aspect-ratio: unset;
  }

  .list-view :global(.image-container) {
    width: 120px;
    flex-shrink: 0;
  }

  /* Mobile-first responsive design */
  @media (max-width: 480px) {
    .grid-view {
      min-height: 200px;
      border-radius: 12px;
    }

    .list-view {
      height: 120px;
      border-radius: 8px;
    }

    .list-view :global(.image-container) {
      width: 120px;
    }
  }

  /* Tablet responsive design */
  @media (min-width: 481px) and (max-width: 768px) {
    .grid-view {
      min-height: 190px;
    }

    .list-view {
      height: 110px;
    }

    .list-view :global(.image-container) {
      width: 110px;
    }
  }
</style>
