<!--
  ButtonPanel.svelte

  Unified action button panel for workbench layout.
  Pure orchestration component - composes individual button components.

  Architecture:
  - Uses CreateModuleContext for state access
  - Derives all boolean flags locally from context
  - Only receives event handler callbacks as props
  - No business logic (delegated to services)
  - Just composition and prop passing
-->
<script lang="ts">
  import { fade } from "svelte/transition";
  import { PresenceAnimation } from "$shared/animation";
  import { shouldHideUIForPanels } from "$shared";
  import { getCreateModuleContext } from "$create/shared/context";
  import {
    ClearSequencePanelButton,
    PlayButton,
    SequenceActionsButton,
    ShareButton,
    UndoButton,
  } from "./buttons/index.js";

  // Get context - ButtonPanel is ONLY used inside CreateModule, so context is always available
  const { CreateModuleState, panelState, layout } = getCreateModuleContext();

  // Props interface - only event handler callbacks
  const {
    onClearSequence,
    onSequenceActionsClick,
    onShare,
    onPlayAnimation,
    visible = true,
  }: {
    onClearSequence?: () => void;
    onSequenceActionsClick?: () => void;
    onShare?: () => void;
    onPlayAnimation?: () => void;
    visible?: boolean;
  } = $props();

  // Derive computed values from context
  const showPlayButton = $derived(CreateModuleState.canShowActionButtons());
  const showShareButton = $derived(CreateModuleState.canShowActionButtons());
  const showSequenceActions = $derived(
    CreateModuleState.canShowSequenceActionsButton()
  );
  const canClearSequence = $derived(CreateModuleState.canClearSequence(true));
  const isAnimating = $derived(panelState.isAnimationPanelOpen);
  const isShareOpen = $derived(panelState.isSharePanelOpen);

  // Determine if button panel should be hidden (any modal panel open in side-by-side layout)
  const shouldHidePanel = $derived(shouldHideUIForPanels());

  // Count center-zone buttons to key the container (for smooth cross-fade on layout changes)
  const centerZoneButtonCount = $derived(() => {
    let count = 0;
    if (showPlayButton) count++;
    if (showSequenceActions) count++;
    if (showShareButton) count++;
    // Note: Clear button moved to right zone
    return count;
  });

  /**
   * Spring scale transition using unified animation system
   * Replaces old springScaleTransition with physics-based PresenceAnimation
   */
  function presenceTransition(
    _node: Element,
    { duration = 550, delay = 0 }: { duration?: number; delay?: number } = {}
  ) {
    const animation = new PresenceAnimation("snappy");

    // Trigger enter animation
    animation.enter();

    return {
      duration,
      delay,
      css: (t: number) => {
        // Interpolate between start (0.95 scale) and end (1.0 scale)
        const scale = 0.95 + (1 - 0.95) * t;
        return `
          transform: scale(${scale});
          opacity: ${t};
        `;
      },
    };
  }
</script>

{#if visible}
  <div
    class="button-panel"
    class:hidden={shouldHidePanel}
    transition:fade={{ duration: 200 }}
  >
    <!-- LEFT ZONE: Undo button (always left edge) -->
    <div class="left-zone">
      <div transition:presenceTransition>
        <UndoButton {CreateModuleState} showHistoryDropdown={true} />
      </div>
    </div>

    <!-- CENTER ZONE: Contextual action buttons (centered in available space) -->
    <!-- Wrapper maintains layout space during transitions -->
    <div class="center-zone-wrapper">
      {#key centerZoneButtonCount()}
        <div
          class="center-zone"
          out:fade={{ duration: 150 }}
          in:fade={{ duration: 150, delay: 150 }}
        >
          <!-- Sequence Actions Button -->
          {#if showSequenceActions && onSequenceActionsClick}
            <div>
              <SequenceActionsButton onclick={onSequenceActionsClick} />
            </div>
          {/if}

          <!-- Play Button -->
          {#if showPlayButton && onPlayAnimation}
            <div>
              <PlayButton onclick={onPlayAnimation} {isAnimating} />
            </div>
          {/if}

          <!-- Share Button -->
          {#if showShareButton && onShare}
            <div>
              <ShareButton onclick={onShare} isActive={isShareOpen} />
            </div>
          {/if}
        </div>
      {/key}
    </div>

    <!-- RIGHT ZONE: Clear Sequence button (rightmost) -->
    <div class="right-zone">
      {#if canClearSequence && onClearSequence}
        <div transition:presenceTransition>
          <ClearSequencePanelButton onclick={onClearSequence} />
        </div>
      {/if}
    </div>
  </div>
{/if}

<style>
  .button-panel {
    /* Enable container queries for responsive spacing */
    container-type: inline-size;
    container-name: button-panel;

    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between; /* Space between left, center, right zones */
    width: 100%;
    border-radius: 24px;
    z-index: 1;

    /* Intelligent reactive padding to prevent overlap */
    padding: clamp(8px, 1.5vh, 16px) clamp(12px, 2vw, 24px);

    /* Smooth opacity transition for hiding */
    opacity: 1;
    transition: opacity 0.3s ease;
    pointer-events: auto;
  }

  /* Hidden state - fade to invisible while maintaining space */
  .button-panel.hidden {
    opacity: 0;
    pointer-events: none;
  }

  /* LEFT ZONE: Undo button always at left edge */
  .left-zone {
    display: flex;
    align-items: center;
    gap: 12px; /* Slightly reduced for better mobile fit */
    flex-shrink: 0; /* Don't shrink */
  }

  /* CENTER ZONE WRAPPER: Maintains layout space during transitions */
  .center-zone-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-grow: 1; /* Take up available space */
    position: relative;
    min-height: 44px; /* Prevent collapse */
  }

  /* CENTER ZONE: Contextual buttons centered in available space */
  .center-zone {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px; /* Slightly reduced for better mobile fit */
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
  }

  /* RIGHT ZONE: Toggle always at right edge */
  .right-zone {
    display: flex;
    align-items: center;
    gap: 12px; /* Slightly reduced for better mobile fit */
    flex-shrink: 0; /* Don't shrink */
  }

  /* Ensure transition wrappers don't interfere with layout */
  .left-zone > div,
  .center-zone > div,
  .right-zone > div {
    display: inline-block;
  }

  /* Remove mobile tap highlight (blue selection box) */
  .button-panel :global(button),
  .button-panel :global(a) {
    -webkit-tap-highlight-color: transparent;
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    user-select: none;
  }

  /* Container-based responsive adjustments - Progressive gap reduction to fit 44px buttons */
  @container button-panel (max-width: 768px) {
    .button-panel {
      padding: clamp(6px, 1.2vh, 12px) clamp(10px, 1.8vw, 18px);
    }

    .left-zone,
    .center-zone,
    .right-zone {
      gap: 10px; /* Balanced spacing for 44px buttons */
    }
  }

  /* Tighter spacing on smaller containers to accommodate 44px buttons */
  @container button-panel (max-width: 480px) {
    .button-panel {
      padding: clamp(4px, 1vh, 10px) clamp(8px, 1.5vw, 12px);
    }

    .left-zone,
    .center-zone,
    .right-zone {
      gap: 8px; /* Compact but comfortable spacing */
    }
  }

  /* Very narrow containers - minimal gaps but NEVER shrink buttons */
  @container button-panel (max-width: 360px) {
    .button-panel {
      padding: 6px 8px;
    }

    .left-zone,
    .center-zone,
    .right-zone {
      gap: 6px; /* Tight spacing to fit all buttons */
    }
  }

  /* Extremely narrow containers */
  @container button-panel (max-width: 340px) {
    .button-panel {
      padding: 6px 6px;
    }

    .left-zone,
    .center-zone,
    .right-zone {
      gap: 5px; /* Minimum comfortable gap */
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
