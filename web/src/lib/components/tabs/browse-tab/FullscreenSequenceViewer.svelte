<!-- FullscreenSequenceViewer.svelte - Fullscreen sequence viewer with actions -->
<script lang="ts">
  import type { IThumbnailService } from "$contracts";
  import type { SequenceData } from "$domain";
  import { fade } from "svelte/transition";
  // Import subcomponents
  import FullscreenActionButtons from "./fullscreen/FullscreenActionButtons.svelte";
  import FullscreenImageViewer from "./fullscreen/FullscreenImageViewer.svelte";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    show = false,
    sequence,
    thumbnailService,
    onClose = () => {},
    onAction = () => {},
  } = $props<{
    show?: boolean;
    sequence?: SequenceData;
    thumbnailService?: IThumbnailService;
    onClose?: () => void;
    onAction?: (action: string, sequence: SequenceData) => void;
  }>();

  // State for current variation (shared with image viewer)
  let currentVariationIndex = $state(0);

  // Dynamic header height detection
  let closeButtonTopOffset = $state(16); // Default 1rem

  // Calculate header height on mount and window resize
  $effect(() => {
    function calculateHeaderOffset() {
      // Look for navigation bar or any fixed header
      const navBar =
        document.querySelector(".app-navigation-bar") ||
        document.querySelector(".landing-navbar") ||
        document.querySelector("nav") ||
        document.querySelector("header");

      if (navBar) {
        const rect = navBar.getBoundingClientRect();
        // Position button below the header with some margin
        closeButtonTopOffset = rect.bottom + 16; // Add 1rem margin
      } else {
        // Fallback if no header found
        closeButtonTopOffset = 16;
      }
    }

    // Calculate on mount
    calculateHeaderOffset();

    // Recalculate on window resize
    const handleResize = () => calculateHeaderOffset();
    window.addEventListener("resize", handleResize);

    // Also recalculate after a short delay to ensure DOM is ready
    const timeoutId = setTimeout(calculateHeaderOffset, 100);

    return () => {
      window.removeEventListener("resize", handleResize);
      clearTimeout(timeoutId);
    };
  });

  // Reset state when sequence changes
  $effect(() => {
    if (sequence) {
      currentVariationIndex = 0;
    }
  });

  // Event handlers
  function handleClose() {
    console.log("❌ Closing fullscreen viewer");
    onClose();
  }

  function handleBackdropClick(event: MouseEvent) {
    if (event.target === event.currentTarget) {
      handleClose();
    }
  }
</script>

{#if show && sequence}
  <!-- Fullscreen overlay -->
  <div
    class="fullscreen-overlay"
    transition:fade={{ duration: 300 }}
    onclick={handleBackdropClick}
    onkeydown={(e) => e.key === "Escape" && handleClose()}
    role="dialog"
    aria-modal="true"
    aria-labelledby="fullscreen-title"
    tabindex="-1"
  >
    <!-- Close button positioned intelligently below header -->
    <button
      class="close-button"
      onclick={handleClose}
      aria-label="Close fullscreen viewer"
      style="top: {closeButtonTopOffset}px;"
    >
      <span class="close-icon">✕</span>
    </button>

    <!-- Main content area -->
    <div class="fullscreen-content">
      <!-- Sequence title above image -->
      <div class="sequence-title-container">
        <h1 class="sequence-title">{sequence?.word || "Sequence"}</h1>
        {#if sequence?.difficulty}
          <span
            class="difficulty-badge"
            class:beginner={sequence.difficulty === "Beginner"}
            class:intermediate={sequence.difficulty === "Intermediate"}
            class:advanced={sequence.difficulty === "Advanced"}
          >
            {sequence.difficulty}
          </span>
        {/if}
      </div>

      <!-- Image viewer (centered) -->
      <FullscreenImageViewer
        {sequence}
        {thumbnailService}
        bind:currentVariationIndex
      />

      <!-- Centered bottom panel -->
      <div class="bottom-panel">
        <FullscreenActionButtons {sequence} {onAction} />
      </div>
    </div>
  </div>
{/if}

<style>
  .fullscreen-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.95);
    backdrop-filter: blur(10px);
    z-index: 1000;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .close-button {
    position: fixed;
    right: 1rem;
    z-index: 9999;
    background: rgba(0, 0, 0, 0.8);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    width: 3rem;
    height: 3rem;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
    color: white;
    backdrop-filter: blur(4px);
  }

  .close-button:hover {
    background: rgba(0, 0, 0, 0.9);
    border-color: rgba(255, 255, 255, 0.5);
    transform: scale(1.1);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .close-button:active {
    transform: scale(0.95);
  }

  .close-icon {
    font-size: 1.25rem;
    font-weight: 300;
  }

  .fullscreen-content {
    flex: 1;
    display: flex;
    flex-direction: column; /* Always use vertical layout */
    position: relative;
    min-height: 0;
    padding: 2rem 2rem 2rem 2rem; /* Reduced top padding since header is simplified */
    gap: 1rem; /* Reduced gap for tighter layout */
  }

  .sequence-title-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .sequence-title {
    color: white;
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0;
    text-align: center;
  }

  .difficulty-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.75rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .difficulty-badge.beginner {
    background: rgba(34, 197, 94, 0.2);
    color: #22c55e;
    border: 1px solid rgba(34, 197, 94, 0.3);
  }

  .difficulty-badge.intermediate {
    background: rgba(251, 191, 36, 0.2);
    color: #fbbf24;
    border: 1px solid rgba(251, 191, 36, 0.3);
  }

  .difficulty-badge.advanced {
    background: rgba(239, 68, 68, 0.2);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.3);
  }

  .bottom-panel {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    max-width: 600px;
    margin: 0 auto;
  }

  /* Mobile adjustments */
  @media (max-width: 768px) {
    .close-button {
      width: 2.5rem;
      height: 2.5rem;
      right: 0.75rem;
      z-index: 10000;
    }

    .close-icon {
      font-size: 1rem;
    }

    .fullscreen-content {
      padding: 1rem;
      gap: 1rem;
    }

    .sequence-title {
      font-size: 1.25rem;
    }

    .sequence-title-container {
      margin-bottom: 0.75rem;
    }

    .bottom-panel {
      gap: 1rem;
      max-width: 100%;
    }
  }
</style>
