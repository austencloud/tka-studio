<!--
ThumbnailImage Component - Image Loading and Display

Handles image loading, error states, and placeholders for sequence thumbnails.
Extracted from SequenceThumbnail.svelte for better separation of concerns.
-->
<script lang="ts">
  import type { IThumbnailService } from "$contracts";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    sequenceId,
    sequenceWord,
    thumbnails = [],
    thumbnailService,
    alt = "",
  } = $props<{
    sequenceId: string;
    sequenceWord: string;
    thumbnails: string[];
    thumbnailService: IThumbnailService;
    alt?: string;
  }>();

  // ✅ PURE RUNES: State for image loading
  let imageLoaded = $state(false);
  let imageError = $state(false);

  // ✅ DERIVED RUNES: Computed thumbnail URL
  let thumbnailUrl = $derived.by(() => {
    const firstThumbnail = thumbnails[0];
    return firstThumbnail
      ? thumbnailService.getThumbnailUrl(sequenceId, firstThumbnail)
      : null;
  });

  // Event handlers
  function handleImageLoad() {
    imageLoaded = true;
    imageError = false;
  }

  function handleImageError() {
    imageError = true;
    imageLoaded = false;
  }
</script>

<div class="image-container">
  <!-- Actual image -->
  {#if thumbnailUrl && !imageError}
    <img
      src={thumbnailUrl}
      alt={alt || `${sequenceWord} sequence thumbnail`}
      class="thumbnail-image"
      class:loaded={imageLoaded}
      class:error={imageError}
      onload={handleImageLoad}
      onerror={handleImageError}
    />
  {/if}

  <!-- Loading state -->
  {#if !imageLoaded && !imageError && thumbnailUrl}
    <div class="loading-placeholder">
      <div class="loading-spinner"></div>
    </div>
  {/if}

  <!-- Error state or no thumbnail -->
  {#if imageError || !thumbnailUrl}
    <div class="error-placeholder">
      <div class="placeholder-icon">📄</div>
      <div class="placeholder-text">{sequenceWord}</div>
    </div>
  {/if}
</div>

<style>
  .image-container {
    position: relative;
    width: 100%;
    /* Remove fixed height to allow natural sizing based on image aspect ratio */
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    /* Minimum height to ensure placeholders have reasonable size */
    min-height: 120px;
  }

  .thumbnail-image {
    width: 100%;
    /* Remove fixed height to allow natural aspect ratio */
    max-width: 100%;
    height: auto;
    /* Change from cover to contain to maintain aspect ratio */
    object-fit: contain;
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .thumbnail-image.loaded {
    opacity: 1;
  }

  .thumbnail-image.error {
    display: none;
  }

  .loading-placeholder {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(248, 250, 252, 0.9);
  }

  .loading-spinner {
    width: 24px;
    height: 24px;
    border: 2px solid #e2e8f0;
    border-top-color: #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .error-placeholder {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(248, 250, 252, 0.95);
    color: #64748b;
  }

  .placeholder-icon {
    font-size: 2rem;
    margin-bottom: 8px;
    opacity: 0.7;
  }

  .placeholder-text {
    font-size: 0.75rem;
    font-weight: 600;
    text-align: center;
    max-width: 80%;
    word-break: break-word;
  }

  /* Responsive design */
  @media (max-width: 768px) {
    .image-container {
      /* Remove fixed height for mobile as well */
      min-height: 100px;
    }

    .placeholder-icon {
      font-size: 1.5rem;
    }

    .placeholder-text {
      font-size: 0.625rem;
    }
  }
</style>
