<!-- ContentOptionsSection.svelte - Content selection controls at the top -->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { ShareState } from "../state";

  let {
    shareState,
    onShowOptions,
  }: {
    shareState?: ShareState | null;
    onShowOptions?: () => void;
  } = $props();

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });

  // Handle options button click
  function handleShowOptions() {
    hapticService?.trigger("navigation");
    onShowOptions?.();
  }

  // Get current preset display name
  function getPresetDisplayName(presetName: string): string {
    switch (presetName) {
      case 'social':
        return 'Social Media';
      case 'print':
        return 'Print Quality';
      case 'web':
        return 'Web Sharing';
      case 'custom':
        return 'Custom';
      default:
        return 'Unknown';
    }
  }

  // Get preset description
  function getPresetDescription(presetName: string): string {
    switch (presetName) {
      case 'social':
        return 'Optimized for Instagram, TikTok, and social platforms';
      case 'print':
        return 'High resolution for printing and detailed viewing';
      case 'web':
        return 'Balanced quality and file size for web sharing';
      case 'custom':
        return 'Customized settings';
      default:
        return '';
    }
  }

  // Get quick summary of current options
  let optionsSummary = $derived(() => {
    if (!shareState?.options) return null;

    const options = shareState.options;
    const features = [];

    if (options.addWord) features.push('Word');
    if (options.addBeatNumbers) features.push('Beat #s');
    if (options.addUserInfo) features.push('User Info');
    if (options.addDifficultyLevel) features.push('Difficulty');
    if (options.includeStartPosition) features.push('Start Pos');

    return {
      preset: getPresetDisplayName(shareState.selectedPreset),
      format: options.format,
      features: features.length > 0 ? features.join(', ') : 'Basic',
      hasCustomizations: features.length > 0
    };
  });
</script>

<div class="content-options-section">
  <!-- Section Header -->
  <div class="section-header">
    <h3 class="section-title">Content Options</h3>
    <p class="section-description">Customize what appears in your shared image</p>
  </div>

  <!-- Current Settings Summary -->
  {#if shareState && optionsSummary()}
    <div class="current-settings">
      <div class="setting-row">
        <span class="setting-label">Preset:</span>
        <span class="setting-value">{optionsSummary()?.preset}</span>
      </div>
      
      <div class="setting-row">
        <span class="setting-label">Format:</span>
        <span class="setting-value">{optionsSummary()?.format}</span>
      </div>
      
      <div class="setting-row">
        <span class="setting-label">Includes:</span>
        <span class="setting-value" class:has-features={optionsSummary()?.hasCustomizations}>
          {optionsSummary()?.features}
        </span>
      </div>

      <div class="preset-description">
        {getPresetDescription(shareState.selectedPreset)}
      </div>
    </div>
  {/if}

  <!-- Customize Button -->
  <div class="customize-section">
    <button
      class="customize-btn"
      onclick={handleShowOptions}
      disabled={!shareState}
    >
      <span class="btn-icon">⚙️</span>
      <span class="btn-text">Customize Options</span>
      <span class="btn-arrow">→</span>
    </button>
    
    <p class="customize-hint">
      Adjust format, quality, and content options
    </p>
  </div>
</div>

<style>
  .content-options-section {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    background: var(--bg-primary);
  }

  /* Section header */
  .section-header {
    text-align: center;
  }

  .section-title {
    margin: 0 0 0.25rem 0;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
  }

  .section-description {
    margin: 0;
    font-size: 0.85rem;
    color: var(--text-secondary);
  }

  /* Current settings summary */
  .current-settings {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding: 0.75rem;
    background: var(--bg-secondary);
    border-radius: 6px;
    border: 1px solid var(--border-color);
  }

  .setting-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.9rem;
  }

  .setting-label {
    color: var(--text-secondary);
    font-weight: 500;
  }

  .setting-value {
    color: var(--text-primary);
    font-weight: 500;
  }

  .setting-value.has-features {
    color: var(--accent-color);
  }

  .preset-description {
    margin-top: 0.5rem;
    padding-top: 0.5rem;
    border-top: 1px solid var(--border-color);
    font-size: 0.8rem;
    color: var(--text-secondary);
    font-style: italic;
    text-align: center;
  }

  /* Customize section */
  .customize-section {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    align-items: center;
  }

  .customize-btn {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1.25rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    min-width: 200px;
    justify-content: center;
  }

  .customize-btn:hover:not(:disabled) {
    background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
  }

  .customize-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none !important;
    box-shadow: none !important;
  }

  .btn-icon {
    font-size: 1.1rem;
  }

  .btn-text {
    flex: 1;
  }

  .btn-arrow {
    font-size: 1rem;
    transition: transform 0.2s ease;
  }

  .customize-btn:hover:not(:disabled) .btn-arrow {
    transform: translateX(2px);
  }

  .customize-hint {
    margin: 0;
    font-size: 0.8rem;
    color: var(--text-secondary);
    text-align: center;
  }

  /* Responsive design */
  @media (max-width: 767px) {
    .content-options-section {
      padding: 0.75rem;
    }

    .customize-btn {
      min-width: 100%;
      padding: 1rem 1.25rem;
    }

    .setting-row {
      font-size: 0.85rem;
    }
  }
</style>
