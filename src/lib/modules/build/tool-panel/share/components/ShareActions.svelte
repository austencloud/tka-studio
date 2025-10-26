<!-- ShareActions.svelte - Share and download actions -->
<script lang="ts">
  import { onMount } from "svelte";
  import type { SequenceData } from "$shared";
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";

  let {
    currentSequence,
    canShare = false,
    isDownloading = false,
    onDownload,
  }: {
    currentSequence: SequenceData | null;
    canShare?: boolean;
    isDownloading?: boolean;
    onDownload?: () => void;
  } = $props();

  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });

  // Handle download
  function handleDownload() {
    if (!canShare || isDownloading) return;
    hapticService?.trigger("success");
    onDownload?.();
  }

  // Get sequence info for display
  let sequenceInfo = $derived(() => {
    if (!currentSequence) return null;

    const beatCount = currentSequence.beats?.length || 0;
    const word = currentSequence.word || currentSequence.name || "Untitled";

    return {
      name: word,
      beatCount,
      isEmpty: beatCount === 0,
    };
  });

  // Download button text
  function getDownloadButtonText() {
    if (isDownloading) {
      return "Downloading...";
    }

    const info = sequenceInfo();
    if (!info) {
      return "No Sequence to Download";
    }

    if (info.isEmpty) {
      return "Empty Sequence";
    }

    return "Download Image";
  }
</script>

<div class="share-actions">


  <!-- Primary Action: Download -->
  <div class="action-section primary">
    <div class="action-info">
      {#if sequenceInfo()}
        <div class="sequence-info">
          <span class="sequence-name">{sequenceInfo()?.name}</span>
          <span class="sequence-details">
            {sequenceInfo()?.beatCount} beats
          </span>
        </div>
      {:else}
        <div class="no-sequence">
          <span class="no-sequence-text">No sequence selected</span>
        </div>
      {/if}
    </div>

    <button
      class="action-button download"
      class:disabled={!canShare || isDownloading}
      onclick={handleDownload}
      disabled={!canShare || isDownloading}
    >
      {#if isDownloading}
        <span class="loading-spinner"></span>
        {getDownloadButtonText()}
      {:else}
        <span class="button-icon">💾</span>
        {getDownloadButtonText()}
      {/if}
    </button>
  </div>

  <!-- Future Actions: Social Media -->
  <div class="action-section secondary">
    <div class="action-info">
      <h4>Social Media Sharing</h4>
      <p class="coming-soon">Coming soon! Share directly to Instagram, TikTok, and more.</p>
    </div>

    <div class="social-buttons">
      <button class="social-button instagram" disabled>
        <span class="social-icon">📷</span>
        Instagram
      </button>
      <button class="social-button tiktok" disabled>
        <span class="social-icon">🎵</span>
        TikTok
      </button>
      <button class="social-button share" disabled>
        <span class="social-icon">📤</span>
        Share Link
      </button>
    </div>
  </div>
</div>

<style>
  .share-actions {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    background: var(--bg-primary);
  }

  .action-section {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .action-section.primary {
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border-color);
  }

  .action-info h4 {
    margin: 0 0 0.25rem 0;
    font-size: 1rem;
    font-weight: 500;
    color: var(--text-primary);
  }

  .sequence-info {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .sequence-name {
    font-weight: 500;
    color: var(--text-primary);
  }

  .sequence-details {
    font-size: 0.85rem;
    color: var(--text-secondary);
  }

  .no-sequence-text {
    color: var(--text-secondary);
    font-style: italic;
  }

  .coming-soon {
    margin: 0;
    font-size: 0.85rem;
    color: var(--text-secondary);
    font-style: italic;
  }

  .action-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    border: none;
    border-radius: 6px;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .action-button.download {
    background: var(--accent-color);
    color: white;
  }

  .action-button.download:hover:not(.disabled) {
    background: var(--accent-color-hover);
    transform: translateY(-1px);
  }

  .action-button.disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none !important;
  }

  .button-icon {
    font-size: 1.1rem;
  }

  .loading-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top: 2px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .social-buttons {
    display: flex;
    flex-direction: row;
    gap: 0.75rem;
    flex-wrap: wrap;
  }

  .social-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.75rem;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    background: var(--bg-secondary);
    color: var(--text-secondary);
    font-size: 0.9rem;
    cursor: not-allowed;
    opacity: 0.6;
  }

  .social-icon {
    font-size: 1rem;
  }
</style>
