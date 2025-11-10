<!--
LazyGalleryThumbnailImage - Optimized lazy-loading thumbnail component

Features (2026 Best Practices):
- Priority Queue: Visible images load first (based on IntersectionObserver ratio)
- Responsive images: 200px, 600px, 1900px (automatic size selection)
- Native lazy loading: loading="lazy" + fetchpriority hints
- Intersection Observer: Multiple thresholds (0, 0.25, 0.5, 0.75, 1.0)
- Request throttling: Prevents connection pool exhaustion
- Timeout handling: 30s timeout with manual retry
- WebP with graceful fallback
- Progressive loading states: skeleton → spinner → image
- ResizeObserver: Dynamic container-based sizing
-->
<script lang="ts">
  import type { IExploreThumbnailService } from "../services/contracts/IExploreThumbnailService";
  import { imageRequestQueue } from "../../shared/utils/image-request-queue";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    sequenceId,
    sequenceWord,
    thumbnails = [],
    thumbnailService,
    alt = "",
    priority = false, // For above-the-fold images
    width = undefined, // Image width from manifest
    height = undefined, // Image height from manifest
  } = $props<{
    sequenceId: string;
    sequenceWord: string;
    thumbnails: string[];
    thumbnailService: IExploreThumbnailService;
    alt?: string;
    priority?: boolean; // Load immediately if true
    width?: number; // Prevents layout shift
    height?: number; // Prevents layout shift
  }>();

  // ✅ PURE RUNES: State for image loading
  let imageContainer: HTMLElement;
  let imageLoaded = $state(false);
  let imageError = $state(false);
  let shouldLoad = $state(priority); // Load immediately if priority
  let imageObjectUrl = $state<string | null>(null);
  let isTimeout = $state(false);
  let isRetrying = $state(false);
  let visibilityRatio = $state(0); // How much of the image is visible (0-1)

  // ✅ DERIVED RUNES: Computed thumbnail URLs for responsive images
  let thumbnailUrl = $derived.by(() => {
    const firstThumbnail = thumbnails[0];
    return firstThumbnail
      ? thumbnailService.getThumbnailUrl(sequenceId, firstThumbnail)
      : null;
  });

  // Generate responsive image URLs
  let responsiveUrls = $derived.by(() => {
    if (!thumbnailUrl) return null;

    const baseUrl = thumbnailUrl.replace('.webp', '');
    return {
      small: `${baseUrl}_small.webp`,   // 200px
      medium: `${baseUrl}_medium.webp`, // 600px
      large: thumbnailUrl,               // 1900px (original)
    };
  });

  // Detect which size to load based on container width
  let containerWidth = $state(200); // Default to small
  let selectedImageUrl = $derived.by(() => {
    if (!responsiveUrls) return null;

    // Choose appropriate size based on container width
    if (containerWidth <= 300) return responsiveUrls.small;
    if (containerWidth <= 800) return responsiveUrls.medium;
    return responsiveUrls.large;
  });

  // Fallback: For the rare case where WebP fails, we'll show a placeholder
  // Since we removed PNG files for clean codebase, 97% get WebP, 3% get graceful degradation
  let showPlaceholder = $state(false);

  // ✅ EFFECT: Measure container width for responsive image selection
  $effect(() => {
    if (!imageContainer) return;

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        containerWidth = entry.contentRect.width;
      }
    });

    resizeObserver.observe(imageContainer);

    return () => {
      resizeObserver.disconnect();
    };
  });

  // ✅ EFFECT: Set up intersection observer for lazy loading
  $effect(() => {
    if (!imageContainer || priority || shouldLoad) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            // Capture how much of the image is visible (0-1)
            // This will be used to prioritize fully-visible images
            visibilityRatio = entry.intersectionRatio;
            shouldLoad = true;
            observer.unobserve(entry.target);
          }
        });
      },
      {
        // Use multiple thresholds to detect visibility percentage accurately
        threshold: [0, 0.25, 0.5, 0.75, 1.0],
        rootMargin: "50px", // Reduced from 100px - only preload very close images
      }
    );

    observer.observe(imageContainer);

    return () => {
      observer.disconnect();
    };
  });

  // ✅ EFFECT: Load image through queue when shouldLoad is true
  $effect(() => {
    if (!selectedImageUrl || !shouldLoad || imageLoaded || isRetrying) return;

    let cleanup: (() => void) | null = null;

    (async () => {
      try {
        // Determine priority based on visibility
        let imagePriority = 1; // Default: normal priority

        if (priority) {
          // Explicitly marked as priority (above-the-fold)
          imagePriority = 10;
        } else if (visibilityRatio >= 0.75) {
          // Mostly visible (75%+)
          imagePriority = 3;
        } else if (visibilityRatio >= 0.5) {
          // Half visible (50-75%)
          imagePriority = 2;
        } else if (visibilityRatio > 0) {
          // Partially visible (1-50%)
          imagePriority = 1;
        } else {
          // Not visible yet (preload from rootMargin)
          imagePriority = 0;
        }

        // Use queue to prevent connection pool exhaustion
        // Load the appropriately sized responsive image with priority
        const blob = await imageRequestQueue.load(selectedImageUrl, 30000, imagePriority);

        // Create object URL from blob
        const objectUrl = URL.createObjectURL(blob);
        imageObjectUrl = objectUrl;

        // Cleanup function to revoke object URL
        cleanup = () => {
          URL.revokeObjectURL(objectUrl);
        };

        // Mark as loaded
        imageLoaded = true;
        imageError = false;
        isTimeout = false;
      } catch (error) {
        console.error(`Failed to load image for ${sequenceWord}:`, error);

        // Check if it's a timeout
        if (error instanceof Error && error.message.includes('timeout')) {
          isTimeout = true;
        }

        imageError = true;
        imageLoaded = false;

        // Check if WebP not supported
        if (selectedImageUrl.endsWith('.webp')) {
          showPlaceholder = true;
        }
      }
    })();

    return () => {
      if (cleanup) cleanup();
    };
  });

  // Retry loading after timeout
  async function handleRetry() {
    isRetrying = true;
    imageError = false;
    isTimeout = false;

    try {
      // Retries get high priority (user explicitly requested)
      const blob = await imageRequestQueue.load(selectedImageUrl!, 30000, 5);
      const objectUrl = URL.createObjectURL(blob);
      imageObjectUrl = objectUrl;
      imageLoaded = true;
      imageError = false;
    } catch (error) {
      console.error(`Retry failed for ${sequenceWord}:`, error);
      if (error instanceof Error && error.message.includes('timeout')) {
        isTimeout = true;
      }
      imageError = true;
    } finally {
      isRetrying = false;
    }
  }

  // Event handlers for fallback <img> tag (not used with queue)
  function handleImageLoad() {
    imageLoaded = true;
    imageError = false;
  }

  function handleImageError(event: Event) {
    const img = event.target as HTMLImageElement;

    // WebP failed - show graceful placeholder for the 3% of users with unsupported browsers
    if (img.src.endsWith(".webp")) {
      console.log(
        `WebP not supported for ${sequenceWord}, showing placeholder`
      );
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

  <!-- Actual image (loaded through queue) -->
  {#if imageObjectUrl && imageLoaded}
    <img
      src={imageObjectUrl}
      alt={alt || `${sequenceWord} sequence thumbnail`}
      {width}
      {height}
      class="thumbnail-image loaded"
      loading={priority ? "eager" : "lazy"}
      decoding="async"
      fetchpriority={priority ? "high" : "auto"}
      aria-label={alt || `${sequenceWord} sequence thumbnail`}
    />
  {/if}

  <!-- Loading state -->
  {#if shouldLoad && !imageLoaded && !imageError && selectedImageUrl}
    <div class="loading-placeholder" role="status" aria-live="polite">
      <div class="loading-spinner" aria-label="Loading image"></div>
      <span class="sr-only">Loading {sequenceWord} image...</span>
    </div>
  {/if}

  <!-- Retrying state -->
  {#if isRetrying}
    <div class="loading-placeholder retrying" role="status" aria-live="polite">
      <div class="loading-spinner" aria-label="Retrying image load"></div>
      <span class="retry-text">Retrying...</span>
    </div>
  {/if}

  <!-- Skeleton placeholder (before intersection) -->
  {#if !shouldLoad && !priority}
    <div class="skeleton-placeholder" aria-hidden="true">
      <div class="skeleton-content"></div>
    </div>
  {/if}

  <!-- Timeout error with retry button -->
  {#if imageError && isTimeout && !isRetrying}
    <div class="error-placeholder timeout-error" role="status">
      <div class="error-icon" aria-hidden="true">⏱️</div>
      <div class="error-text">Load timeout</div>
      <button
        class="retry-button"
        onclick={handleRetry}
        aria-label="Retry loading {sequenceWord} image"
      >
        Retry
      </button>
    </div>
  {/if}

  <!-- General error state or no thumbnail -->
  {#if (imageError && !isTimeout) || !selectedImageUrl}
    <div class="error-placeholder" role="status">
      {#if showPlaceholder}
        <div class="webp-unsupported-icon" aria-hidden="true">🖼️</div>
        <div class="webp-unsupported-text">{sequenceWord}</div>
        <div class="webp-unsupported-subtitle">WebP not supported</div>
      {:else}
        <div class="placeholder-icon" aria-hidden="true">📄</div>
        <div class="placeholder-text">{sequenceWord}</div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .image-container {
    position: relative;
    width: 100%;
    background: transparent;
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

  /* Timeout error state */
  .timeout-error {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
  }

  .error-icon {
    font-size: 2rem;
    margin-bottom: 8px;
    opacity: 0.8;
  }

  .error-text {
    font-size: 0.75rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: 12px;
  }

  .retry-button {
    background: rgba(59, 130, 246, 0.8);
    color: white;
    border: none;
    padding: 6px 16px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  .retry-button:hover {
    background: rgba(59, 130, 246, 1);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  }

  .retry-button:active {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  /* Retrying state */
  .loading-placeholder.retrying {
    flex-direction: column;
    gap: 8px;
  }

  .retry-text {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.7);
    font-weight: 500;
  }

  /* Responsive design */
  @container (max-width: 300px) {
    .image-container {
      min-height: 100px;
    }

    .placeholder-icon,
    .error-icon {
      font-size: 1.5rem;
    }

    .placeholder-text,
    .error-text {
      font-size: 0.625rem;
    }

    .retry-button {
      padding: 4px 12px;
      font-size: 0.625rem;
    }
  }

  /* Screen reader only class for accessibility */
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
  }
</style>
