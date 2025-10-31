<!--
Learn Tab - Master learning interface

Three learning destinations:
- Concepts: Progressive concept mastery path
- Drills: Quick pictograph flash card quizzes
- Read: Beautiful PDF flipbook reader

Navigation via bottom tabs (mobile-first UX pattern)
Plus floating Codex button for quick letter reference
-->
<script lang="ts">
  import {
    navigationState,
    resolve,
    TYPES,
    type IHapticFeedbackService,
  } from "$shared";
  import { onMount } from "svelte";
  import ConceptPathView from "./components/ConceptPathView.svelte";
  import ConceptDetailView from "./components/ConceptDetailView.svelte";
  import CodexPanel from "./components/CodexPanel.svelte";
  import QuizTab from "./quiz/components/QuizTab.svelte";
  import ReadTab from "./read/components/ReadTab.svelte";
  import { persistentPDFState } from "./read/state";

  type LearnMode = "concepts" | "drills" | "read";

  const hapticService = resolve<IHapticFeedbackService>(
    TYPES.IHapticFeedbackService
  );

  // Active mode synced with navigation state
  let activeMode = $state<LearnMode>("concepts");

  // Concept detail view state
  let selectedConceptId = $state<string | null>(null);

  // Codex panel state
  let isCodexOpen = $state(false);

  // Sync with navigation state (bottom nav controls this)
  $effect(() => {
    const navMode = navigationState.currentLearnMode;

    // Map legacy modes
    if (navMode === "codex" || navMode === "concepts") {
      activeMode = "concepts";
    } else if (navMode === "quiz" || navMode === "drills") {
      activeMode = "drills";
    } else if (navMode === "read") {
      activeMode = "read";
    }
  });

  // Reset concept detail when switching modes
  $effect(() => {
    // When active mode changes, return to list view
    const mode = activeMode; // Track dependency
    selectedConceptId = null;
  });

  // Initialize on mount
  onMount(async () => {
    // Set default mode if none persisted
    const navMode = navigationState.currentLearnMode;
    if (!navMode || navMode === "codex") {
      navigationState.setLearnMode("concepts");
    }

    // Preload PDF in background for instant Read tab access
    try {
      await persistentPDFState.ensurePDFLoaded("/static/Level 1.pdf");
    } catch (error) {
      console.warn("📚 LearnTab: Background PDF load failed:", error);
    }
  });

  // Handle concept selection
  function handleConceptClick(conceptId: string) {
    selectedConceptId = conceptId;
  }

  // Handle back from detail view
  function handleBackToPath() {
    selectedConceptId = null;
  }

  // Handle codex button click
  function handleCodexClick() {
    hapticService?.trigger("selection");
    isCodexOpen = !isCodexOpen;
  }

  // Check if mode is active
  function isModeActive(mode: LearnMode): boolean {
    return activeMode === mode;
  }
</script>

<div class="learn-tab">
  <!-- Content area (all modes) -->
  <div class="content-container">
    <!-- Concepts Mode -->
    <div class="mode-panel" class:active={isModeActive("concepts")}>
      {#if selectedConceptId}
        <ConceptDetailView
          conceptId={selectedConceptId}
          onBack={handleBackToPath}
        />
      {:else}
        <ConceptPathView onConceptClick={handleConceptClick} />
      {/if}
    </div>

    <!-- Drills Mode -->
    <div class="mode-panel" class:active={isModeActive("drills")}>
      <QuizTab />
    </div>

    <!-- Read Mode -->
    <div class="mode-panel" class:active={isModeActive("read")}>
      <ReadTab />
    </div>
  </div>

  <!-- Floating Codex Button (top-right, thumb-reachable on mobile) -->
  <button
    class="floating-codex-button glass-surface"
    class:active={isCodexOpen}
    onclick={handleCodexClick}
    aria-label="Open letters reference"
    title="Letters Reference"
  >
    <i class="fas fa-book-open"></i>
    <span class="button-label">Letters</span>
  </button>

  <!-- Codex Panel (slide-in coordinator) -->
  <CodexPanel bind:isOpen={isCodexOpen} />
</div>

<style>
  .learn-tab {
    position: relative;
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
    background: transparent;
    color: var(--foreground, #ffffff);

    /* Enable container queries for responsive design */
    container-type: size;
    container-name: learn-tab;

    /* Account for bottom navigation */
    padding-bottom: max(64px, env(safe-area-inset-bottom));
  }

  /* Content container */
  .content-container {
    position: relative;
    flex: 1;
    width: 100%;
    height: 100%;
    overflow: hidden;
  }

  /* Mode panels */
  .mode-panel {
    position: absolute;
    inset: 0;
    display: none;
    width: 100%;
    height: 100%;
    overflow: hidden;
  }

  .mode-panel.active {
    display: flex;
    flex-direction: column;
  }

  /* Floating Codex Button - 2026 glass morphism */
  .floating-codex-button {
    position: fixed;
    top: 1rem;
    right: 1rem;
    z-index: 50;

    display: flex;
    align-items: center;
    gap: 0.5rem;

    min-width: 44px;
    min-height: 44px;
    padding: 0.75rem 1rem;

    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(16px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 14px;

    color: rgba(255, 255, 255, 0.9);
    font-size: 0.875rem;
    font-weight: 600;

    cursor: pointer;
    transition: all 250ms cubic-bezier(0.4, 0, 0.2, 1);

    /* Subtle shadow for depth */
    box-shadow:
      0 4px 12px rgba(0, 0, 0, 0.15),
      0 0 0 1px rgba(255, 255, 255, 0.05) inset;
  }

  .floating-codex-button i {
    font-size: 1.125rem;
    line-height: 1;
  }

  .floating-codex-button .button-label {
    line-height: 1;
  }

  /* Hover state - lift and glow */
  .floating-codex-button:hover {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px) scale(1.02);
    box-shadow:
      0 8px 24px rgba(0, 0, 0, 0.2),
      0 0 0 1px rgba(255, 255, 255, 0.1) inset,
      0 0 20px rgba(255, 255, 255, 0.1);
  }

  /* Active/pressed state */
  .floating-codex-button:active {
    transform: translateY(0) scale(0.98);
    transition-duration: 100ms;
  }

  /* Active state when panel is open */
  .floating-codex-button.active {
    background: rgba(74, 158, 255, 0.15);
    border-color: rgba(74, 158, 255, 0.3);
    color: rgba(74, 158, 255, 1);
  }

  .floating-codex-button.active:hover {
    background: rgba(74, 158, 255, 0.2);
    box-shadow:
      0 8px 24px rgba(74, 158, 255, 0.3),
      0 0 0 1px rgba(74, 158, 255, 0.2) inset,
      0 0 20px rgba(74, 158, 255, 0.2);
  }

  /* Focus-visible for keyboard navigation */
  .floating-codex-button:focus-visible {
    outline: 2px solid rgba(74, 158, 255, 1);
    outline-offset: 2px;
  }

  /* Container query: Compact button on small screens */
  @container learn-tab (max-width: 480px) {
    .floating-codex-button {
      padding: 0.75rem;
      min-width: 48px;
      border-radius: 12px;
    }

    .floating-codex-button .button-label {
      display: none;
    }

    .floating-codex-button i {
      font-size: 1.25rem;
    }
  }

  /* Container query: Move to bottom-right on portrait mobile */
  @container learn-tab (max-height: 700px) and (max-width: 500px) {
    .floating-codex-button {
      top: auto;
      bottom: calc(64px + 1rem); /* Above bottom nav */
      right: 1rem;
    }
  }

  /* Reduced motion accessibility */
  @media (prefers-reduced-motion: reduce) {
    .floating-codex-button {
      transition: none;
    }
  }

  /* Safe area insets for notched devices */
  @supports (top: env(safe-area-inset-top)) {
    .floating-codex-button {
      top: max(1rem, env(safe-area-inset-top) + 0.5rem);
      right: max(1rem, env(safe-area-inset-right) + 0.5rem);
    }
  }
</style>
