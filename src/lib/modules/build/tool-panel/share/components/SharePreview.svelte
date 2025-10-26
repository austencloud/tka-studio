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

<div class="share-preview">

  <div class="preview-content">
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
</div>

<style>
  .share-preview {
    display: flex;
    flex-direction: column;
    height: 100%;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    background: var(--bg-primary);
    overflow: hidden;
  }

  .preview-content {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 0;
    max-height: 100%;
    overflow: hidden;
  }

  .preview-placeholder,
  .preview-loading,
  .preview-error {
    text-align: center;
    color: var(--text-secondary);
  }

  .placeholder-icon,
  .error-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    opacity: 0.5;
  }

  .placeholder-hint,
  .error-message {
    font-size: 0.85rem;
    opacity: 0.7;
    display: block;
    margin-top: 0.5rem;
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid var(--border-color);
    border-top: 3px solid var(--accent-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 1rem;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .retry-button {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background: var(--accent-color);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
  }

  .retry-button:hover {
    background: var(--accent-color-hover);
  }

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
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
</style>
