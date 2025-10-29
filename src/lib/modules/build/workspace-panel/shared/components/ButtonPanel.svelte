<!--
  ButtonPanel.svelte

  Unified action button panel for workbench layout.
  Pure orchestration component - composes individual button components.

  Architecture:
  - No business logic (delegated to services)
  - No CSS (except layout)
  - No state management (delegated to button components)
  - Just composition and prop passing
-->
<script lang="ts">
  import type { IBuildTabState } from '$build/shared/types/build-tab-types';
  import { fade } from 'svelte/transition';
  import {
    BackButton,
    ClearSequencePanelButton,
    ConstructGenerateToggle,
    FullscreenButton,
    PlayButton,
    RemoveBeatButton,
    SequenceActionsButton,
    ShareButton,
    UndoButton
  } from './buttons/index.js';

  // Props interface
  const {
    // Back button
    canGoBack = false,
    onBack,

    // Build tab state for undo functionality
    buildTabState = null,

    // Remove Beat button
    canRemoveBeat = false,
    onRemoveBeat,
    selectedBeatIndex = null,
    selectedBeatData = null,

    // Clear Sequence button
    canClearSequence = false,
    onClearSequence,

    // Sequence Actions button
    showSequenceActions = false,
    onSequenceActionsClick,

    // Share button
    showShareButton = false,
    onShare,
    isShareOpen = false,

    // Play button
    showPlayButton = false,
    onPlayAnimation,
    isAnimating = false,

    // Full Screen button
    showFullScreen = true,

    // Construct/Generate toggle props
    showToggle = false,
    activeTab = 'construct',
    onTabChange,

    // Panel visibility
    visible = true
  }: {
    // Back button props
    canGoBack?: boolean;
    onBack?: () => void;

    // Build tab state for undo functionality
    buildTabState?: IBuildTabState | null;

    // Remove Beat button props
    canRemoveBeat?: boolean;
    onRemoveBeat?: (beatIndex: number) => void;
    selectedBeatIndex?: number | null;
    selectedBeatData?: any;

    // Clear Sequence button props
    canClearSequence?: boolean;
    onClearSequence?: () => void;

    // Sequence Actions button props
    showSequenceActions?: boolean;
    onSequenceActionsClick?: () => void;

    // Share button props
    showShareButton?: boolean;
    onShare?: () => void;
    isShareOpen?: boolean;

    // Play button props
    showPlayButton?: boolean;
    onPlayAnimation?: () => void;
    isAnimating?: boolean;

    // Full Screen button props
    showFullScreen?: boolean;

    // Construct/Generate toggle props
    showToggle?: boolean;
    activeTab?: 'construct' | 'generate';
    onTabChange?: (tab: 'construct' | 'generate') => void;

    // Panel visibility
    visible?: boolean;
  } = $props();

  // Determine if Remove Beat button should be shown
  const shouldShowRemoveBeat = $derived(() => {
    return canRemoveBeat &&
           selectedBeatData &&
           selectedBeatData.beatNumber >= 1 &&
           selectedBeatIndex !== null;
  });

  // Count visible buttons to determine if toggle should show text labels
  const visibleButtonCount = $derived(() => {
    let count = 0;

    // Count toggle
    if (showToggle) count++;

    // Count undo/back button
    if (buildTabState || canGoBack) count++;

    // Count remove beat button
    if (shouldShowRemoveBeat()) count++;

    // Count clear sequence button
    if (canClearSequence) count++;

    // Count sequence actions button
    if (showSequenceActions) count++;

    // Count share button
    if (showShareButton) count++;

    // Count play button
    if (showPlayButton) count++;

    // Count fullscreen button
    if (showFullScreen) count++;

    return count;
  });

  // Show text labels when toggle is the only button visible
  const shouldShowToggleLabels = $derived(() => visibleButtonCount() === 1);
</script>

{#if visible}
  <div class="button-panel" transition:fade={{ duration: 200 }}>
    <!-- LEFT ZONE: Undo/Back button (always left edge) -->
    <div class="left-zone">
      <!-- Undo Button (when buildTabState is available) or Back Button -->
      {#if buildTabState}
        <UndoButton
          {buildTabState}
          showHistoryDropdown={true}
        />
      {:else if canGoBack}
        <BackButton onclick={onBack} />
      {/if}
    </div>

    <!-- CENTER ZONE: Contextual action buttons (centered in available space) -->
    <div class="center-zone">
      <!-- Remove Beat Button -->
      {#if shouldShowRemoveBeat()}
        <RemoveBeatButton
          beatNumber={selectedBeatData.beatNumber}
          onclick={() => onRemoveBeat?.(selectedBeatIndex!)}
        />
      {/if}

      <!-- Clear Sequence Button -->
      {#if canClearSequence}
        <ClearSequencePanelButton onclick={onClearSequence} />
      {/if}

      <!-- Sequence Actions Button -->
      {#if showSequenceActions}
        <SequenceActionsButton onclick={onSequenceActionsClick} />
      {/if}

      <!-- Share Button -->
      {#if showShareButton && onShare}
        <ShareButton onclick={onShare} isActive={isShareOpen} />
      {/if}

      <!-- Play Button -->
      {#if showPlayButton}
        <PlayButton onclick={onPlayAnimation} {isAnimating} />
      {/if}

      <!-- Full Screen Button -->
      {#if showFullScreen}
        <FullscreenButton />
      {/if}
    </div>

    <!-- RIGHT ZONE: Toggle (always right edge) -->
    <div class="right-zone">
      <!-- Construct/Generate Toggle (always rightmost) -->
      {#if showToggle && activeTab && onTabChange}
        <ConstructGenerateToggle
          {activeTab}
          onTabChange={onTabChange}
          showLabels={shouldShowToggleLabels()}
        />
      {/if}
    </div>
  </div>
{/if}

<style>
  .button-panel {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between; /* Space between left, center, right zones */
    width: 100%;
    border-radius: 24px;
    z-index: 1;

    /* Intelligent reactive padding to prevent overlap */
    padding: clamp(8px, 1.5vh, 16px) clamp(12px, 2vw, 24px);
  }

  /* LEFT ZONE: Undo button always at left edge */
  .left-zone {
    display: flex;
    align-items: center;
    gap: 16px;
    flex-shrink: 0; /* Don't shrink */
  }

  /* CENTER ZONE: Contextual buttons centered in available space */
  .center-zone {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    flex-grow: 1; /* Take up available space */
  }

  /* RIGHT ZONE: Toggle always at right edge */
  .right-zone {
    display: flex;
    align-items: center;
    gap: 16px;
    flex-shrink: 0; /* Don't shrink */
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .button-panel {
      padding: clamp(6px, 1.2vh, 12px) clamp(10px, 1.8vw, 20px);
    }

    .left-zone,
    .center-zone,
    .right-zone {
      gap: 12px;
    }
  }

  @media (max-width: 480px) {
    .button-panel {
      padding: clamp(4px, 1vh, 10px) clamp(8px, 1.5vw, 16px);
    }

    .left-zone,
    .center-zone,
    .right-zone {
      gap: 8px;
    }
  }

  @media (max-width: 320px) {
    .button-panel {
      padding: 4px 8px;
    }

    .left-zone,
    .center-zone,
    .right-zone {
      gap: 6px;
    }
  }

  /* 🎯 LANDSCAPE MOBILE: Ultra-compact mode for devices like Z Fold 5 horizontal (882x344) */
  /* Matches app's isLandscapeMobile() criteria: aspectRatio > 1.7 AND height < 500px */
  /* This preserves precious vertical space on wide but short screens */
  @media (min-aspect-ratio: 17/10) and (max-height: 500px) {
    .button-panel {
      border-radius: 16px;
      /* Reduce vertical footprint - minimal padding */
      min-height: 0;
      padding: 4px 12px;
    }

    .left-zone,
    .center-zone,
    .right-zone {
      gap: 16px;
    }
  }

  /* 🔥 EXTREME CONSTRAINTS: Very narrow landscape mode */
  /* For devices in horizontal orientation with extreme width constraints */
  @media (max-width: 500px) and (min-aspect-ratio: 17/10) and (max-height: 500px) {
    .button-panel {
      border-radius: 12px;
      padding: 3px 8px;
    }

    .left-zone,
    .center-zone,
    .right-zone {
      gap: 6px;
    }
  }
</style>
