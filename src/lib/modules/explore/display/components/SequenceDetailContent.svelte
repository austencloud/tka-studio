<!--
SequenceDetailContent - Shared content for sequence detail view

Displays:
- Large sequence preview image
- Sequence metadata (word, difficulty, length, author)
- Navigation controls (previous/next variation)
- Action buttons (Play, Favorite, Edit, Delete, Maximize)

Used by both desktop side panel and mobile slide-up overlay.
-->
<script lang="ts">
  import type { IHapticFeedbackService, SequenceData } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { IExploreThumbnailService } from "../services/contracts/IExploreThumbnailService";

  let hapticService: IHapticFeedbackService;

  const {
    sequence,
    onClose = () => {},
    onAction = () => {},
  } = $props<{
    sequence: SequenceData;
    onClose?: () => void;
    onAction?: (action: string, sequence: SequenceData) => void;
  }>();

  // Services
  const thumbnailService = resolve<IExploreThumbnailService>(
    TYPES.IExploreThumbnailService
  );

  // State
  let currentVariationIndex = $state(0);

  // Derived
  const coverUrl = $derived.by(() => {
    const thumbnail = sequence?.thumbnails?.[currentVariationIndex];
    if (!thumbnail) return undefined;
    try {
      return thumbnailService.getThumbnailUrl(sequence.id, thumbnail);
    } catch (error) {
      console.warn("Failed to resolve thumbnail", error);
      return undefined;
    }
  });

  const totalVariations = $derived(sequence?.thumbnails?.length || 1);
  const canGoBack = $derived(currentVariationIndex > 0);
  const canGoForward = $derived(currentVariationIndex < totalVariations - 1);

  // Handlers
  function handlePrevious() {
    if (canGoBack) {
      hapticService?.trigger("selection");
      currentVariationIndex--;
    }
  }

  function handleNext() {
    if (canGoForward) {
      hapticService?.trigger("selection");
      currentVariationIndex++;
    }
  }

  function handleAction(action: string) {
    hapticService?.trigger("selection");
    onAction(action, sequence);
  }

  function handleMaximize() {
    hapticService?.trigger("selection");
    onAction("fullscreen", sequence);
  }

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });
</script>

<div class="detail-content">
  <!-- Close button -->
  <button class="close-button" onclick={onClose} aria-label="Close">
    <svg
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
    >
      <line x1="18" y1="6" x2="6" y2="18"></line>
      <line x1="6" y1="6" x2="18" y2="18"></line>
    </svg>
  </button>

  <!-- Sequence Preview -->
  <div class="preview-container">
    {#if coverUrl}
      <img src={coverUrl} alt={sequence.name} class="preview-image" />
    {:else}
      <div class="preview-placeholder">No preview available</div>
    {/if}
  </div>

  <!-- Variation Navigation -->
  {#if totalVariations > 1}
    <div class="variation-nav">
      <button
        class="nav-btn"
        onclick={handlePrevious}
        disabled={!canGoBack}
        aria-label="Previous variation"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
          <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z" />
        </svg>
      </button>

      <span class="variation-counter">
        {currentVariationIndex + 1} / {totalVariations}
      </span>

      <button
        class="nav-btn"
        onclick={handleNext}
        disabled={!canGoForward}
        aria-label="Next variation"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
          <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z" />
        </svg>
      </button>
    </div>
  {/if}

  <!-- Metadata -->
  <div class="metadata">
    <h2 class="word-label">{sequence.name || sequence.word}</h2>
    <div class="metadata-row">
      <span class="metadata-item">Length: {sequence.sequenceLength} beats</span>
      <span class="metadata-item">Level: {sequence.difficultyLevel}</span>
    </div>
    {#if sequence.author}
      <div class="metadata-row">
        <span class="metadata-item">Author: {sequence.author}</span>
      </div>
    {/if}
  </div>

  <!-- Action Buttons -->
  <div class="action-buttons">
    <button
      class="action-btn action-btn-primary"
      onclick={() => handleAction("play")}
    >
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
        <path d="M8 5v14l11-7z" />
      </svg>
      <span>Play</span>
    </button>

    <button
      class="action-btn"
      class:favorited={sequence.isFavorite}
      onclick={() => handleAction("favorite")}
      aria-label={sequence.isFavorite ? "Remove from favorites" : "Add to favorites"}
    >
      <svg width="20" height="20" viewBox="0 0 24 24" fill={sequence.isFavorite ? "currentColor" : "none"} stroke="currentColor" stroke-width="2">
        <path
          d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
        />
      </svg>
    </button>

    <button class="action-btn" onclick={() => handleAction("edit")} aria-label="Edit sequence">
      <svg
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <path
          d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"
        />
        <path
          d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"
        />
      </svg>
    </button>

    <button class="action-btn" onclick={() => handleAction("delete")} aria-label="Delete sequence">
      <svg
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <polyline points="3 6 5 6 21 6" />
        <path
          d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
        />
      </svg>
    </button>

    <button class="action-btn action-btn-maximize" onclick={handleMaximize} aria-label="Maximize details">
      <svg
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <path
          d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"
        />
      </svg>
      <span>Maximize</span>
    </button>
  </div>
</div>

<style>
  .detail-content {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: clamp(16px, 4vw, 24px);
    gap: clamp(16px, 3vw, 20px);
    position: relative;
    overflow-y: auto;
  }

  /* Close button */
  .close-button {
    position: absolute;
    top: 16px;
    right: 16px;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
    z-index: 10;
  }

  .close-button:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: scale(1.1);
  }

  /* Preview - Space Maximization Algorithm (from legacy Sequence Viewer) */
  .preview-container {
    /*
     * Legacy algorithm: available_height = height() * 0.65
     * Legacy algorithm: available_width = width() * 1/3 * 0.95 (for 1/3 panel width)
     * Adapted for flexible panel: Use full panel width with 95% utilization
     */
    flex: 1; /* Grow to fill available vertical space */
    min-height: 200px; /* Minimum usable size */
    max-height: 65%; /* 65% height utilization (legacy Sequence Viewer constant) */
    width: 95%; /* 95% width utilization (legacy algorithm) */
    max-width: 100%;
    margin: 0 auto; /* Center horizontally */
    background: rgba(0, 0, 0, 0.3);
    border-radius: 12px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
  }

  .preview-image {
    /*
     * Maximize within container while preserving aspect ratio
     * CSS equivalent of legacy's iterative width/height fitting algorithm
     * object-fit: contain automatically preserves aspect ratio and fits within bounds
     */
    max-width: 100%;
    max-height: 100%;
    width: auto;
    height: auto;
    object-fit: contain; /* Preserves aspect ratio (Qt.AspectRatioMode.KeepAspectRatio) */
  }

  .preview-placeholder {
    color: rgba(255, 255, 255, 0.5);
    font-size: 14px;
  }

  /* Variation Navigation */
  .variation-nav {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    padding: 8px;
  }

  .nav-btn {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .nav-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }

  .nav-btn:not(:disabled):hover {
    background: rgba(255, 255, 255, 0.2);
    transform: scale(1.1);
  }

  .variation-counter {
    font-size: 14px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
    min-width: 60px;
    text-align: center;
  }

  /* Metadata */
  .metadata {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .word-label {
    font-size: clamp(20px, 5vw, 28px);
    font-weight: 700;
    color: white;
    margin: 0;
    text-align: center;
  }

  .metadata-row {
    display: flex;
    gap: 16px;
    justify-content: center;
    flex-wrap: wrap;
  }

  .metadata-item {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.7);
  }

  /* Action Buttons */
  .action-buttons {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: auto;
  }

  .action-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 12px 16px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    color: white;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    min-height: 44px;
  }

  .action-btn:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
  }

  .action-btn-primary {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    border-color: transparent;
    flex: 1;
    min-width: 120px;
  }

  .action-btn-primary:hover {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  }

  .action-btn-maximize {
    flex: 1;
    min-width: 120px;
  }

  .action-btn.favorited {
    color: #f87171;
    border-color: #f87171;
  }

  /* Mobile adjustments */
  @media (max-width: 768px) {
    .detail-content {
      padding: 16px;
      gap: 16px;
    }

    .action-buttons {
      gap: 8px;
    }

    .action-btn {
      padding: 10px 12px;
      font-size: 13px;
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .close-button,
    .nav-btn,
    .action-btn {
      transition: none;
    }

    .close-button:hover,
    .nav-btn:not(:disabled):hover,
    .action-btn:hover {
      transform: none;
    }
  }
</style>
