<!--
SequenceAnimationModal - Fullscreen Modal for Sequence Animation

Opens a fullscreen modal overlay containing the AnimationPanel to preview sequences
in motion. Provides an immersive animation viewing experience without leaving the
Gallery context.

Pattern: Instagram Stories / Pinterest / YouTube player
-->
<script lang="ts">
  import type { IHapticFeedbackService, SequenceData } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import { fade, scale } from "svelte/transition";
  import AnimationPanel from "../../../build/animate/components/AnimationPanel.svelte";

  const {
    sequence,
    isOpen = false,
    onClose = () => {},
  } = $props<{
    sequence: SequenceData | null;
    isOpen?: boolean;
    onClose?: () => void;
  }>();

  let hapticService: IHapticFeedbackService | null = $state(null);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Handle ESC key to close modal
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Escape" && isOpen) {
      handleClose();
    }
  }

  function handleClose() {
    hapticService?.trigger("selection");
    onClose();
  }

  function handleBackdropClick(event: MouseEvent) {
    // Only close if clicking the backdrop itself, not the content
    if (event.target === event.currentTarget) {
      handleClose();
    }
  }
</script>

<svelte:window onkeydown={handleKeydown} />

{#if isOpen && sequence}
  <!-- Modal Backdrop -->
  <div
    class="modal-backdrop"
    onclick={handleBackdropClick}
    onkeydown={handleKeydown}
    transition:fade={{ duration: 300 }}
    role="dialog"
    aria-modal="true"
    aria-labelledby="animation-modal-title"
    tabindex="-1"
  >
    <!-- Modal Content -->
    <div
      class="modal-content"
      transition:scale={{ duration: 300, start: 0.95 }}
    >
      <!-- Close Button -->
      <button
        class="modal-close-button"
        onclick={handleClose}
        aria-label="Close animation viewer"
        title="Close (ESC)"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path
            d="M18 6L6 18M6 6l12 12"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </button>

      <!-- Animation Panel -->
      <div class="animation-container">
        <h2 id="animation-modal-title" class="visually-hidden">
          Animating: {sequence.word || sequence.name || "Sequence"}
        </h2>
        <AnimationPanel {sequence} show={isOpen} onClose={handleClose} />
      </div>
    </div>
  </div>
{/if}

<style>
  /* Modal Backdrop */
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.85);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
    overflow-y: auto;
  }

  /* Modal Content */
  .modal-content {
    position: relative;
    width: 100%;
    max-width: 1400px;
    height: 90vh;
    max-height: 900px;
    background: linear-gradient(
      135deg,
      rgba(20, 20, 30, 0.98) 0%,
      rgba(30, 30, 45, 0.98) 100%
    );
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }

  /* Close Button */
  .modal-close-button {
    position: absolute;
    top: 1.5rem;
    right: 1.5rem;
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 50%; /* Consistent circular style */
    color: rgba(255, 255, 255, 0.9);
    cursor: pointer;
    transition: all 0.2s ease;
    z-index: 10;
  }

  .modal-close-button:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
    color: white;
    transform: scale(1.05);
  }

  .modal-close-button:active {
    transform: scale(0.98);
  }

  .modal-close-button:focus-visible {
    outline: 2px solid #667eea;
    outline-offset: 2px;
  }

  /* Animation Container */
  .animation-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  /* Accessibility */
  .visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
  }

  /* Mobile Optimizations */
  @media (max-width: 768px) {
    .modal-backdrop {
      padding: 0;
    }

    .modal-content {
      width: 100%;
      height: 100vh;
      max-height: none;
      border-radius: 0;
    }

    .modal-close-button {
      top: 1rem;
      right: 1rem;
      width: 40px;
      height: 40px;
    }
  }

  /* Tablet Optimizations */
  @media (min-width: 769px) and (max-width: 1024px) {
    .modal-content {
      height: 85vh;
      max-height: 800px;
    }
  }

  /* Reduced Motion Support */
  @media (prefers-reduced-motion: reduce) {
    .modal-backdrop,
    .modal-content,
    .modal-close-button {
      transition: none;
    }
  }

  /* High Contrast Mode */
  @media (prefers-contrast: high) {
    .modal-backdrop {
      background: rgba(0, 0, 0, 0.95);
    }

    .modal-content {
      border: 2px solid white;
    }

    .modal-close-button {
      border: 2px solid white;
    }
  }
</style>
