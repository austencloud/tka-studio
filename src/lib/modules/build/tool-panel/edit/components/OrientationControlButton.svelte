<!-- OrientationControlButton.svelte - Collapsible button with preview -->
<script lang="ts">
  import type { BeatData, IHapticFeedbackService } from '$shared';
  import { resolve, TYPES } from '$shared';
  import { onMount } from 'svelte';

  // Props
  const {
    color,
    currentBeatData,
    isExpanded = false,
    layoutMode = 'comfortable',
    onExpand,
    onOrientationChanged
  } = $props<{
    color: 'blue' | 'red';
    currentBeatData: BeatData | null;
    isExpanded?: boolean;
    layoutMode?: 'compact' | 'balanced' | 'comfortable';
    onExpand: () => void;
    onOrientationChanged: (color: string, orientation: string) => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  // Get display values
  const displayLabel = $derived(() => color === 'blue' ? 'Left' : 'Right');
  const currentOrientation = $derived(() => {
    if (!currentBeatData) return 'in';
    const motion = color === 'blue' ? currentBeatData.motions?.blue : currentBeatData.motions?.red;
    return motion?.startOrientation || 'in';
  });
  const previewText = $derived(() => `${displayLabel()}: ${currentOrientation().toUpperCase()}`);

  // Separate line display for compact mode
  const previewLine1 = $derived(() => displayLabel());
  const previewLine2 = $derived(() => currentOrientation().toUpperCase());

  function handleClick() {
    hapticService?.trigger("selection");
    onExpand();
  }

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });
</script>

<button
  class="orientation-control-button"
  class:blue={color === 'blue'}
  class:red={color === 'red'}
  class:expanded={isExpanded}
  class:compact={layoutMode === 'compact'}
  class:balanced={layoutMode === 'balanced'}
  class:comfortable={layoutMode === 'comfortable'}
  onclick={handleClick}
  aria-label={previewText()}
  data-testid={`orientation-control-button-${color}`}
>
  <div class="button-content">
    {#if isExpanded}
      <!-- Other panel is expanded - show two-line compact layout to save space -->
      <div class="preview-text two-line">
        <div class="line-1">{previewLine1()}</div>
        <div class="line-2">{previewLine2()}</div>
      </div>
      <div class="chevron">
        <i class="fas fa-chevron-down"></i>
      </div>
    {:else}
      <!-- Both panels collapsed - show single-line format -->
      <div class="preview-text">{previewText()}</div>
      <div class="chevron">
        <i class="fas fa-chevron-down"></i>
      </div>
    {/if}
  </div>
</button>

<style>
  .orientation-control-button {
    flex: 1;
    border: 4px solid;
    border-radius: 12px;
    background: white;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    user-select: none;
    -webkit-user-select: none;
    -webkit-tap-highlight-color: transparent;
    container-type: inline-size;
  }

  /* Comfortable mode - Mobile, full sizing */
  .orientation-control-button.comfortable {
    min-height: 60px;
  }

  /* Balanced mode - Tablet landscape */
  .orientation-control-button.balanced {
    min-height: 48px;
    border-width: 3px;
  }

  /* Compact mode - Desktop, minimal vertical space */
  .orientation-control-button.compact {
    min-height: 40px;
    border-width: 2px;
    border-radius: 8px;
  }

  .orientation-control-button.blue {
    border-color: #3b82f6;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(59, 130, 246, 0.04) 100%);
  }

  .orientation-control-button.red {
    border-color: #ef4444;
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(239, 68, 68, 0.04) 100%);
  }

  .orientation-control-button:hover:not(.expanded) {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .orientation-control-button.blue:hover:not(.expanded) {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.12) 0%, rgba(59, 130, 246, 0.06) 100%);
  }

  .orientation-control-button.red:hover:not(.expanded) {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.12) 0%, rgba(239, 68, 68, 0.06) 100%);
  }

  .orientation-control-button:active:not(.expanded) {
    transform: translateY(0);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  }

  .orientation-control-button.expanded {
    flex: 0 0 auto;
    min-width: 80px;
    opacity: 0.6;
  }

  .button-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }

  .preview-text {
    font-weight: 600;
    flex: 1;
    text-align: left;
  }

  /* Two-line layout for collapsed state */
  .preview-text.two-line {
    display: flex;
    flex-direction: column;
    gap: 2px;
    line-height: 1.2;
  }

  .preview-text.two-line .line-1 {
    font-weight: 700;
    font-size: clamp(12px, 3cqw, 15px);
  }

  .preview-text.two-line .line-2 {
    font-size: clamp(10px, 2.5cqw, 13px);
    opacity: 0.8;
    font-weight: 500;
  }

  /* Font sizes by layout mode (for expanded state) */
  .orientation-control-button.comfortable .preview-text:not(.two-line) {
    font-size: 16px;
  }

  .orientation-control-button.balanced .preview-text:not(.two-line) {
    font-size: 15px;
  }

  .orientation-control-button.compact .preview-text:not(.two-line) {
    font-size: 14px;
  }

  .orientation-control-button.blue .preview-text {
    color: #3b82f6;
  }

  .orientation-control-button.red .preview-text {
    color: #ef4444;
  }

  .orientation-control-button.expanded .preview-text {
    font-size: 14px;
    text-align: center;
  }

  .orientation-control-button.expanded.compact .preview-text {
    font-size: 12px;
  }

  .chevron {
    font-size: 12px;
    opacity: 0.6;
    transition: transform 0.3s ease;
  }

  .orientation-control-button.compact .chevron {
    font-size: 10px;
  }

  .orientation-control-button.blue .chevron {
    color: #3b82f6;
  }

  .orientation-control-button.red .chevron {
    color: #ef4444;
  }

  /* Responsive adjustments for very small screens */
  @media (max-width: 400px) {
    .orientation-control-button {
      min-height: 50px;
    }

    .preview-text {
      font-size: 14px;
    }

    .orientation-control-button.expanded .preview-text {
      font-size: 12px;
    }
  }
</style>

