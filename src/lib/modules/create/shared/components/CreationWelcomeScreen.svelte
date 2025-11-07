<script lang="ts">
  /**
   * Creation Welcome Screen
   *
   * Displays the inviting welcome screen when the creation method selector is visible.
   * Shows:
   * - Optional undo button (if undo history exists)
   * - CreationWelcomeCue with contextual messaging
   *
   * Extracted from CreateModule to reduce component size and improve maintainability.
   *
   * Domain: Create module - Welcome screen presentation
   */

  import { fade } from "svelte/transition";
  import CreationWelcomeCue from "./CreationWelcomeCue.svelte";
  import { getCreateModuleContext } from "../context";

  // Get context
  const ctx = getCreateModuleContext();
  const { CreateModuleState } = ctx;

  // Props (only presentation-specific props)
  let {
    orientation,
    mood,
  }: {
    orientation: "horizontal" | "vertical";
    mood: "default" | "redo" | "returning" | "fresh";
  } = $props();
</script>

<!-- Layout 1: Inviting text when selector is visible -->
<div
  class="welcome-screen"
  in:fade={{ duration: 400, delay: 200 }}
  out:fade={{ duration: 200 }}
>
  <!-- Centered welcome content with undo button above -->
  <div
    class="welcome-content"
    class:horizontal-cue={orientation === "horizontal"}
  >
    <!-- Undo button - centered above title -->
    {#if CreateModuleState?.canUndo}
      <button
        class="welcome-undo-button"
        onclick={() => CreateModuleState?.undo()}
        transition:fade={{ duration: 200 }}
        title={CreateModuleState.undoHistory[
          CreateModuleState.undoHistory.length - 1
        ]?.metadata?.description || "Undo last action"}
      >
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          aria-hidden="true"
        >
          <path
            d="M9 14L4 9L9 4"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
          <path
            d="M4 9H15A6 6 0 0 1 15 21H13"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
        <span>Undo</span>
      </button>
    {/if}

    <CreationWelcomeCue {orientation} {mood} />
  </div>
</div>

<style>
  /* Welcome screen (Layout 1) */
  .welcome-screen {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    align-items: center;
    justify-content: center;

    backdrop-filter: blur(20px);
    border-radius: 12px;
    overflow: hidden;
  }

  .welcome-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    padding: 2rem;
    text-align: center;
  }

  .welcome-content.horizontal-cue {
    align-items: flex-start;
    text-align: left;
  }

  /* Welcome screen undo button - centered above title in natural flow */
  .welcome-undo-button {
    padding: 0.75rem 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;

    /* Match ButtonPanel undo button styling */
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;

    /* Smooth transitions */
    transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);

    /* Backdrop blur for better readability */
    backdrop-filter: blur(10px);
  }

  .welcome-undo-button:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
    color: rgba(255, 255, 255, 1);
    transform: translateY(-2px);
  }

  .welcome-undo-button:active {
    transform: translateY(0);
  }

  .welcome-undo-button svg {
    flex-shrink: 0;
  }

  .welcome-undo-button span {
    white-space: nowrap;
  }
</style>
