<!--
HandPathSettingsView.svelte - Centered Settings View for Hand Path Builder

Pre-flight settings screen shown before the user starts drawing.
Displays settings in a beautifully centered layout, then transitions
to the full workspace/tool panel layout when "Start Drawing" is clicked.
-->
<script lang="ts">
  import { fade, scale } from "svelte/transition";
  import { cubicOut } from "svelte/easing";
  import type { HandPathCoordinator } from "../state/hand-path-coordinator.svelte";
  import SequenceLengthPicker from "../../construct/handpath-builder/components/SequenceLengthPicker.svelte";

  // Props
  let {
    handPathCoordinator,
  }: {
    handPathCoordinator: HandPathCoordinator;
  } = $props();
</script>

<div
  class="settings-view"
  in:fade={{ duration: 400, easing: cubicOut }}
  out:fade={{ duration: 300, easing: cubicOut }}
>
  <div
    class="settings-container"
    in:scale={{ duration: 500, delay: 100, easing: cubicOut, start: 0.95 }}
  >
    <!-- Settings Section -->
    <div class="settings-content">
      <SequenceLengthPicker
        bind:sequenceLength={handPathCoordinator.sequenceLength}
        bind:gridMode={handPathCoordinator.gridMode}
      />
    </div>

    <!-- Start Drawing Button -->
    <button
      class="start-drawing-btn"
      onclick={() => handPathCoordinator.startDrawing()}
    >
      <i class="fas fa-play"></i>
      Start Drawing
    </button>

    <!-- Helpful hint -->
    <div class="hint">
      <i class="fas fa-lightbulb"></i>
      <span>You'll draw paths for both blue and red hands</span>
    </div>
  </div>
</div>

<style>
  .settings-view {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: clamp(1rem, 4vh, 2rem);
    z-index: 100;
  }

  .settings-container {
    width: 100%;
    max-width: 450px;
    display: flex;
    flex-direction: column;
    gap: clamp(1.75rem, 4vh, 2.25rem);
    padding: clamp(1.5rem, 4vh, 2rem);
  }

  .settings-content {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .start-drawing-btn {
    padding: clamp(1.125rem, 3vh, 1.375rem);
    background: linear-gradient(135deg, #10b981, #059669);
    border: none;
    border-radius: 18px;
    color: white;
    font-size: clamp(1.125rem, 4vw, 1.25rem);
    font-weight: 700;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    min-height: 64px;
    box-shadow:
      0 6px 20px rgba(16, 185, 129, 0.35),
      0 0 0 1px rgba(255, 255, 255, 0.12) inset;
    position: relative;
    overflow: hidden;
  }

  .start-drawing-btn::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.2) 0%,
      rgba(255, 255, 255, 0) 100%
    );
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .start-drawing-btn:hover {
    transform: translateY(-4px);
    box-shadow:
      0 10px 30px rgba(16, 185, 129, 0.5),
      0 0 0 1px rgba(255, 255, 255, 0.2) inset;
  }

  .start-drawing-btn:hover::before {
    opacity: 1;
  }

  .start-drawing-btn:active {
    transform: translateY(-2px);
  }

  .start-drawing-btn i {
    font-size: 1.3em;
  }

  .hint {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.625rem;
    padding: 1rem 1.25rem;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.12), rgba(37, 99, 235, 0.08));
    border: 1px solid rgba(59, 130, 246, 0.25);
    border-radius: 14px;
    color: rgba(147, 197, 253, 0.95);
    font-size: clamp(0.875rem, 3vw, 0.9375rem);
    line-height: 1.5;
    font-weight: 500;
  }

  .hint i {
    font-size: 1.15em;
    color: #60a5fa;
    flex-shrink: 0;
  }

  /* Responsive adjustments */
  @media (max-width: 640px) {
    .settings-container {
      max-width: 100%;
    }
  }

  @media (max-height: 650px) {
    .settings-view {
      padding: 1rem;
    }

    .settings-container {
      gap: 1.5rem;
      padding: 1.25rem;
      max-height: 90vh;
      overflow-y: auto;
    }

    .start-drawing-btn {
      min-height: 56px;
    }
  }

  /* Accessibility: Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .start-drawing-btn,
    .start-drawing-btn::before {
      transition: none;
    }

    .start-drawing-btn:hover {
      transform: none;
    }
  }
</style>
