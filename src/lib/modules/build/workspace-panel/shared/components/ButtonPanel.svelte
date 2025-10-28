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

    // Play button
    showPlayButton = false,
    onPlayAnimation,
    isAnimating = false,

    // Sequence Actions button
    onOpenSequenceActions,

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

    // Play button props
    showPlayButton?: boolean;
    onPlayAnimation?: () => void;
    isAnimating?: boolean;

    // Sequence Actions button props
    onOpenSequenceActions?: () => void;

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
</script>

{#if visible}
  <div class="button-panel" transition:fade={{ duration: 200 }}>
    <!-- Construct/Generate Toggle (when not shown in ToolPanel header) -->
    {#if showToggle && activeTab && onTabChange}
      <ConstructGenerateToggle
        {activeTab}
        onTabChange={onTabChange}
      />
    {/if}

    <!-- Undo Button (when buildTabState is available) or Back Button -->
    {#if buildTabState}
      <UndoButton
        {buildTabState}
        showHistoryDropdown={true}
      />
    {:else if canGoBack}
      <BackButton onclick={onBack} />
    {/if}

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

    <!-- Play Button (central position - opens inline animator) -->
    {#if showPlayButton}
      <PlayButton onclick={onPlayAnimation} {isAnimating} />
    {/if}

    <!-- Sequence Actions Button (opens sheet with more actions) -->
    <SequenceActionsButton onclick={onOpenSequenceActions} />

    <!-- Full Screen Button (rightmost) -->
    {#if showFullScreen}
      <FullscreenButton />
    {/if}
  </div>
{/if}

<style>
  .button-panel {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    gap: 16px;
    border-radius: 24px;
    z-index: 1;
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .button-panel {
      gap: 12px;
    }
  }

  @media (max-width: 480px) {
    .button-panel {
      gap: 8px;
    }
  }

  @media (max-width: 320px) {
    .button-panel {
      gap: 6px;
    }
  }

  /* 🎯 LANDSCAPE MOBILE: Ultra-compact mode for devices like Z Fold 5 horizontal (882x344) */
  /* Matches app's isLandscapeMobile() criteria: aspectRatio > 1.7 AND height < 500px */
  /* This preserves precious vertical space on wide but short screens */
  @media (min-aspect-ratio: 17/10) and (max-height: 500px) {
    .button-panel {
      gap: 16px;
      border-radius: 16px;
      /* Reduce vertical footprint */
      min-height: 0;
    }
  }

  /* 🔥 EXTREME CONSTRAINTS: Very narrow landscape mode */
  /* For devices in horizontal orientation with extreme width constraints */
  @media (max-width: 500px) and (min-aspect-ratio: 17/10) and (max-height: 500px) {
    .button-panel {
      gap: 6px;
      border-radius: 12px;
    }
  }
</style>
