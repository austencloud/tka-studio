<!--
SequenceThumbnail Component - Refactored Implementation

Displays individual sequence thumbnails using extracted components for better
separation of concerns and maintainability. Reduced from 537 lines to ~80 lines.
-->
<script lang="ts">
  import type { IThumbnailService } from "$contracts";
  import type { SequenceData } from "$domain";
  import ThumbnailActions from "./ThumbnailActions.svelte";
  import ThumbnailImage from "./ThumbnailImage.svelte";
  import ThumbnailMetadata from "./ThumbnailMetadata.svelte";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    sequence,
    thumbnailService,
    viewMode = "grid",
    isFavorite = false,
    onFavoriteToggle = () => {},
    onAction = () => {},
  } = $props<{
    sequence: SequenceData;
    thumbnailService: IThumbnailService;
    viewMode?: "grid" | "list";
    isFavorite?: boolean;
    onFavoriteToggle?: (sequenceId: string) => void;
    onAction?: (action: string, sequence: SequenceData) => void;
  }>();

  // Event handlers - Updated for new UX: click to animate
  function handleClick() {
    // New UX: Default click behavior is to animate the sequence
    onAction("animate", sequence);
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      // New UX: Default keyboard behavior is to animate the sequence
      onAction("animate", sequence);
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
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(200, 220, 240, 0.8);
    border-radius: 12px;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex;
    flex-direction: column;
    position: relative;
  }

  .sequence-thumbnail:hover {
    background: rgba(240, 248, 255, 0.98);
    border-color: rgba(100, 150, 255, 0.6);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  }

  .sequence-thumbnail:focus {
    outline: 2px solid rgba(100, 150, 255, 0.8);
    outline-offset: 2px;
  }

  /* Grid view (default) - no additional styling needed */
  /* Fixed aspect-ratio and min-height removed to allow natural sizing based on content */
  /* The container will now expand vertically to accommodate the image's natural aspect ratio */

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

  /* Responsive design */
  @media (max-width: 768px) {
    .grid-view {
      min-height: 180px;
    }

    .list-view {
      height: 100px;
    }

    .list-view :global(.image-container) {
      width: 100px;
    }
  }
</style>
