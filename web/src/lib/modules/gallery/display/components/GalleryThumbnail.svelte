<!--
SequenceThumbnail Component - Refactored Implementation

Displays individual sequence thumbnails using extracted components for better
separation of concerns and maintainability. 

Updated UX: Clicking thumbnail opens fullscreen view directly.
-->
<script lang="ts">
  import type { SequenceData } from "$shared";
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

  // Event handlers - Updated for new UX: click to open fullscreen
  function handleClick() {
    // New UX: Default click behavior is to view fullscreen
    onAction("fullscreen", sequence);
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      // New UX: Default keyboard behavior is to view fullscreen
      onAction("fullscreen", sequence);
    }
  }
</script>

<!-- Thumbnail container with responsive design -->
<div
  class="sequence-thumbnail"
  class:list-view={viewMode === "list"}
  class:grid-view={viewMode === "grid"}
  role="button"
  tabindex="0"
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
