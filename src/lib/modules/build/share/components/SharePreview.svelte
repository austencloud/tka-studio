<!-- SharePreview.svelte - Preview of the sequence image -->
<script lang="ts">
  import type { SequenceData } from "$shared";

  let {
    currentSequence,
    previewUrl = null,
    isGenerating = false,
    error = null,
    onRetry,
  }: {
    currentSequence: SequenceData | null;
    previewUrl?: string | null;
    isGenerating?: boolean;
    error?: string | null;
    onRetry?: () => void;
  } = $props();

  // Handle retry
  function handleRetry() {
    if (onRetry) {
      onRetry();
    }
  }
</script>

<!-- Simple preview container - no extra wrappers -->
<div class="share-preview">
  {#if !currentSequence}
    <div class="preview-placeholder">
      <div class="placeholder-icon">📝</div>
      <p>No sequence selected</p>
      <span class="placeholder-hint">Create or select a sequence to see preview</span>
    </div>
  {:else if currentSequence.beats?.length === 0}
    <div class="preview-placeholder">
      <div class="placeholder-icon">📋</div>
      <p>Empty sequence</p>
      <span class="placeholder-hint">Add beats to generate preview</span>
    </div>
  {:else if isGenerating}
    <div class="preview-loading">
      <div class="loading-spinner"></div>
      <p>Generating preview...</p>
    </div>
  {:else if error}
    <div class="preview-error">
      <div class="error-icon">⚠️</div>
      <p>Preview failed</p>
      <span class="error-message">{error}</span>
      <button class="retry-button" onclick={handleRetry}>
        Try Again
      </button>
    </div>
  {:else if previewUrl}
    <div class="preview-image">
      <img src={previewUrl} alt="Sequence preview" />
    </div>
  {:else}
    <div class="preview-placeholder">
      <div class="placeholder-icon">🖼️</div>
      <p>Preview will appear here</p>
      <span class="placeholder-hint">Adjust options to generate preview</span>
    </div>
  {/if}
</div>

<style>
  /* Clean preview container - fills parent with equal spacing */
  .share-preview {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.03);
    overflow: hidden;
    backdrop-filter: blur(8px);
    padding: 24px;
  }

  /* Placeholder & Status States */
  .preview-placeholder,
  .preview-loading,
  .preview-error {
    text-align: center;
    color: rgba(255, 255, 255, 0.7);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
  }

  .placeholder-icon,
  .error-icon {
    font-size: 48px;
    opacity: 0.4;
    filter: grayscale(0.3);
  }

  .preview-placeholder p,
  .preview-loading p,
  .preview-error p {
    font-size: 16px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
    margin: 0;
  }

  .placeholder-hint,
  .error-message {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.5);
    line-height: 1.5;
  }

  /* Modern Loading Spinner */
  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-top: 3px solid rgba(59, 130, 246, 0.8);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  /* Modern Retry Button */
  .retry-button {
    margin-top: 8px;
    padding: 10px 20px;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: rgba(255, 255, 255, 0.98);
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.25);
  }

  .retry-button:hover {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    transform: scale(1.05);
    box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4);
  }

  .retry-button:active {
    transform: scale(0.98);
  }

  .retry-button:focus-visible {
    outline: 3px solid rgba(59, 130, 246, 0.4);
    outline-offset: 2px;
  }

  /* Preview Image Container */
  .preview-image {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }

  .preview-image img {
    max-width: 100%;
    max-height: 100%;
    width: auto;
    height: auto;
    object-fit: contain;
    border-radius: 8px;
    box-shadow:
      0 4px 16px rgba(0, 0, 0, 0.2),
      0 2px 4px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .retry-button,
    .preview-image img {
      transition: none;
    }

    .retry-button:hover,
    .retry-button:active {
      transform: none;
    }

    .loading-spinner {
      animation: none;
      border-top-color: transparent;
      opacity: 0.7;
    }
  }
</style>
