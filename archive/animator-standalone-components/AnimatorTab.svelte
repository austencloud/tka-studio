<!--
Animator Tab - Main container with internal sub-modes

Features two modes:
1. Sequence Player - Animate complete sequences
2. Beat Constructor - Build and test individual beats

Sub-modes are controlled via the global navigation state.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { navigationState } from "$shared/navigation/state/navigation-state.svelte";
  import { onMount } from "svelte";
  import { fade } from "svelte/transition";
  import { createAnimatorState } from "../state/animator-state.svelte";
  import AnimationPanel from "./AnimationPanel.svelte";
  import PictographVisualizationPanel from "./PictographVisualizationPanel.svelte";

  const hapticService = resolve<IHapticFeedbackService>(
    TYPES.IHapticFeedbackService
  );

  type AnimatorSubMode = "sequence-player" | "beat-constructor";

  // Get active sub-mode from navigation state, default to sequence-player
  let activeSubMode = $derived(
    (navigationState.currentSubMode as AnimatorSubMode) || "sequence-player"
  );

  let animatorState = createAnimatorState();

  // Get current working sequence from global state
  // This is the sequence being built/edited in the Build module
  let currentSequence = $state<any>(null);

  onMount(async () => {
    // Load current sequence from persistence
    try {
      const persistenceService = resolve(
        TYPES.ISequencePersistenceService
      ) as any;
      const state = await persistenceService.loadCurrentState();
      if (state?.currentSequence) {
        currentSequence = state.currentSequence;
        console.log(
          "✅ AnimatorTab: Loaded current sequence:",
          currentSequence.word || currentSequence.name
        );
      }
    } catch (error) {
      console.error("❌ AnimatorTab: Failed to load current sequence:", error);
    }
  });

  // Create panel state for AnimationPanel
  let animationVisible = $state(true);
  let animationCollapsed = $state(false);

  const animationPanelState = {
    get isAnimationVisible() {
      return animationVisible;
    },
    get isAnimationCollapsed() {
      return animationCollapsed;
    },
    toggleAnimationCollapse: () => {
      hapticService?.trigger("navigation");
      animationCollapsed = !animationCollapsed;
    },
    setAnimationVisible: (v: boolean) => {
      animationVisible = v;
    },
  };
</script>

<div class="animator-tab-container">
  <!-- Tab Content -->
  <div class="tab-content">
    {#if activeSubMode === "sequence-player"}
      <div class="sequence-player-container" in:fade={{ duration: 200 }}>
        <div class="info-banner">
          <p class="info-text">
            <span class="info-icon">ℹ️</span>
            Select a sequence from the Explore to animate it here, or load a default
            sequence to explore.
          </p>
        </div>
        <AnimationPanel
          sequence={currentSequence}
          panelState={animationPanelState}
          onClose={() => {}}
        />
      </div>
    {:else if activeSubMode === "beat-constructor"}
      <div class="beat-constructor-container" in:fade={{ duration: 200 }}>
        <div class="info-banner">
          <p class="info-text">
            <span class="info-icon">🔧</span>
            Build and test individual beats with precise motion parameters. Adjust
            prop locations, motion types, and orientations to see results in real-time.
          </p>
        </div>
        <PictographVisualizationPanel state={animatorState} />
      </div>
    {/if}
  </div>
</div>

<style>
  .animator-tab-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    background: linear-gradient(
      135deg,
      rgba(17, 24, 39, 0.95) 0%,
      rgba(31, 41, 55, 0.95) 100%
    );
    overflow: hidden;
  }

  .tab-content {
    flex: 1;
    min-height: 0;
    overflow: hidden;
    position: relative;
  }

  .sequence-player-container,
  .beat-constructor-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
  }

  .info-banner {
    padding: 0.75rem 1rem;
    background: linear-gradient(
      135deg,
      rgba(102, 126, 234, 0.1) 0%,
      rgba(118, 75, 162, 0.1) 100%
    );
    border-bottom: 1px solid rgba(102, 126, 234, 0.2);
  }

  .info-text {
    display: flex;
    align-items: center;
    gap: 0.625rem;
    margin: 0;
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.5;
  }

  .info-icon {
    font-size: 1.125rem;
    line-height: 1;
    flex-shrink: 0;
  }

  .sequence-player-container > :global(:not(.info-banner)),
  .beat-constructor-container > :global(:not(.info-banner)) {
    flex: 1;
    min-height: 0;
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .info-banner {
      padding: 0.5rem 0.75rem;
    }

    .info-text {
      font-size: 0.8125rem;
      gap: 0.5rem;
    }

    .info-icon {
      font-size: 1rem;
    }
  }
</style>
