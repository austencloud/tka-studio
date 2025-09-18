<!--
LazyGalleryThumbnailImage - Optimized lazy-loading thumbnail component

Replaces GalleryThumbnailImage.svelte with:
- Intersection Observer for lazy loading
- Preload links for visible images
- WebP fallback support
- Progressive loading states
-->
<script lang="ts">
  import type { IGalleryThumbnailService } from "../services/contracts/IGalleryThumbnailService";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    sequenceId,
    sequenceWord,
    thumbnails = [],
    thumbnailService,
    alt = "",
    priority = false, // For above-the-fold images
  } = $props<{
    sequenceId: string;
    sequenceWord: string;
    thumbnails: string[];
    thumbnailService: IGalleryThumbnailService;
    alt?: string;
    priority?: boolean; // Load immediately if true
  }>();

  // ✅ PURE RUNES: State for image loading
  let imageContainer: HTMLElement;
  let imageLoaded = $state(false);
  let imageError = $state(false);
  let shouldLoad = $state(priority); // Load immediately if priority

  // ✅ DERIVED RUNES: Computed thumbnail URL with fallback
  let thumbnailUrl = $derived.by(() => {
    const firstThumbnail = thumbnails[0];
    return firstThumbnail
      ? thumbnailService.getThumbnailUrl(sequenceId, firstThumbnail)
      : null;
  });

  // Fallback: For the rare case where WebP fails, we'll show a placeholder
  // Since we removed PNG files for clean codebase, 97% get WebP, 3% get graceful degradation
  let showPlaceholder = $state(false);

  // ✅ EFFECT: Set up intersection observer for lazy loading
  $effect(() => {
    if (!imageContainer || priority || shouldLoad) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            shouldLoad = true;
            observer.unobserve(entry.target);
          }
        });
      },
      {
        rootMargin: "50px", // Start loading 50px before visible
        threshold: 0.1,
      }
    );

    observer.observe(imageContainer);

    return () => {
      observer.disconnect();
    };
  });

  // Event handlers
  function handleImageLoad() {
    imageLoaded = true;
    imageError = false;
  }

  function handleImageError(event: Event) {
    const img = event.target as HTMLImageElement;

    // WebP failed - show graceful placeholder for the 3% of users with unsupported browsers
    if (img.src.endsWith('.webp')) {
      console.log(`WebP not supported for ${sequenceWord}, showing placeholder`);
      showPlaceholder = true;
      imageError = true;
      imageLoaded = false;
      return;
    }

    // Other error - show error state
    imageError = true;
    imageLoaded = false;
  }
</script>

<div class="image-container" bind:this={imageContainer}>
  <!-- Preload critical images -->
  {#if priority && thumbnailUrl}
    <link rel="preload" as="image" href={thumbnailUrl} />
  {/if}

  <!-- Actual image (only load when should load) -->
  {#if thumbnailUrl && !imageError && shouldLoad}
    <img
      src={thumbnailUrl}
      alt={alt || `${sequenceWord} sequence thumbnail`}
      class="thumbnail-image"
      class:loaded={imageLoaded}
      class:error={imageError}
      loading={priority ? "eager" : "lazy"}
      decoding="async"
      onload={handleImageLoad}
      onerror={handleImageError}
    />
  {/if}

  <!-- Loading state -->
  {#if shouldLoad && !imageLoaded && !imageError && thumbnailUrl}
    <div class="loading-placeholder">
      <div class="loading-spinner"></div>
    </div>
  {/if}

  <!-- Skeleton placeholder (before intersection) -->
  {#if !shouldLoad && !priority}
    <div class="skeleton-placeholder">
      <div class="skeleton-content"></div>
    </div>
  {/if}

  <!-- Error state or no thumbnail -->
  {#if imageError || !thumbnailUrl}
    <div class="error-placeholder">
      {#if showPlaceholder}
        <div class="webp-unsupported-icon">🖼️</div>
        <div class="webp-unsupported-text">{sequenceWord}</div>
        <div class="webp-unsupported-subtitle">WebP not supported</div>
      {:else}
        <div class="placeholder-icon">📄</div>
        <div class="placeholder-text">{sequenceWord}</div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .image-container {
    position: relative;
    width: 100%;
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 120px;
    container-type: inline-size;
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
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(8px);
    border-radius: 8px;
  }

  .loading-spinner {
    width: 24px;
    height: 24px;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-top-color: rgba(255, 255, 255, 0.8);
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  /* Skeleton loading animation */
  .skeleton-placeholder {
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .skeleton-content {
    width: 80%;
    height: 60%;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.4),
      transparent
    );
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    border-radius: 4px;
  }

  @keyframes shimmer {
    0% {
      background-position: -200% 0;
    }
    100% {
      background-position: 200% 0;
    }
  }

  .error-placeholder {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(8px);
    border-radius: 8px;
    color: rgba(255, 255, 255, 0.7);
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

  .webp-unsupported-icon {
    font-size: 2rem;
    opacity: 0.6;
    margin-bottom: 8px;
  }

  .webp-unsupported-text {
    font-size: 0.875rem;
    color: #475569;
    font-weight: 600;
    margin-top: 0.5rem;
    text-align: center;
  }

  .webp-unsupported-subtitle {
    font-size: 0.625rem;
    color: #94a3b8;
    margin-top: 0.25rem;
    font-style: italic;
    text-align: center;
  }

  /* Responsive design */
  @container (max-width: 300px) {
    .image-container {
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
