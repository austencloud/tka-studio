<!-- FullscreenHeader.svelte - Header for fullscreen viewer -->
<script lang="ts">
  import type { SequenceData } from "$domain";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const { sequence, onClose = () => {} } = $props<{
    sequence?: SequenceData;
    onClose?: () => void;
  }>();

  // Handle keyboard shortcuts
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Escape") {
      event.preventDefault();
      onClose();
    }
  }
</script>

<svelte:window on:keydown={handleKeydown} />

<header class="fullscreen-header">
  <div class="header-content">
    <div class="sequence-title">
      <h1>{sequence?.word || "Sequence"}</h1>
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

    <button
      class="close-button"
      onclick={onClose}
      aria-label="Close fullscreen viewer"
    >
      <span class="close-icon">✕</span>
    </button>
  </div>
</header>

<style>
  .fullscreen-header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1001;
    background: rgba(0, 0, 0, 0.9);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding: 1rem 2rem;
  }

  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
  }

  .sequence-title {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .sequence-title h1 {
    color: white;
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0;
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

  .close-button {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    width: 3rem;
    height: 3rem;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
    color: white;
  }

  .close-button:hover {
    background: rgba(255, 255, 255, 0.2);
    border-color: rgba(255, 255, 255, 0.3);
    transform: scale(1.05);
  }

  .close-button:active {
    transform: scale(0.95);
  }

  .close-icon {
    font-size: 1.25rem;
    font-weight: 300;
  }

  /* Mobile adjustments */
  @media (max-width: 768px) {
    .fullscreen-header {
      padding: 0.75rem 1rem;
    }

    .sequence-title h1 {
      font-size: 1.25rem;
    }

    .close-button {
      width: 2.5rem;
      height: 2.5rem;
    }

    .close-icon {
      font-size: 1rem;
    }
  }
</style>
