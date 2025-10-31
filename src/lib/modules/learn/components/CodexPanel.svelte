<!--
CodexPanel - Slide-in reference panel for pictograph lookup

A slide-in drawer that provides quick access to the TKA letter codex
while working through concepts or flash card drills.

Features:
- Slides in from right side (300ms animation)
- Backdrop overlay that closes panel when clicked
- Embeds existing CodexComponent
- Filters content based on user's unlocked concepts (optional)
- Keyboard shortcut: Escape to close
- Mobile: Full-screen overlay
- Desktop: Side panel (600px width)
-->
<script lang="ts">
  import { onMount } from "svelte";
  import CodexComponent from "../codex/components/CodexComponent.svelte";
  import type { PictographData } from "$shared";

  interface Props {
    /** Whether the panel is currently open */
    isOpen?: boolean;
    /** Callback when panel should close */
    onClose?: () => void;
    /** Whether to filter codex by unlocked concepts */
    filterByProgress?: boolean;
    /** Optional title override */
    title?: string;
  }

  let {
    isOpen = $bindable(false),
    onClose,
    filterByProgress = false,
    title = "Letters Reference",
  }: Props = $props();

  // Panel animation state
  let panelElement: HTMLElement | undefined = $state();
  let isAnimating = $state(false);

  // Handle Escape key to close panel
  function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Escape" && isOpen) {
      closePanel();
    }
  }

  // Close panel with animation
  function closePanel() {
    if (isAnimating) return;
    isOpen = false;
    onClose?.();
  }

  // Handle backdrop click (close panel)
  function handleBackdropClick(event: MouseEvent) {
    // Only close if clicking the backdrop, not the panel itself
    if (event.target === event.currentTarget) {
      closePanel();
    }
  }

  // Handle pictograph selection
  function handlePictographSelected(pictograph: PictographData) {
    console.log("📖 CodexPanel: Pictograph selected:", pictograph);
    // Keep panel open for reference - user can close manually
  }

  // Add/remove keyboard listener
  onMount(() => {
    return () => {
      // Cleanup if needed
    };
  });

  // Prevent body scroll when panel is open
  $effect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
  });
</script>

<svelte:window onkeydown={handleKeyDown} />

{#if isOpen}
  <!-- Backdrop overlay -->
  <div
    class="codex-backdrop"
    onclick={handleBackdropClick}
    role="button"
    tabindex="-1"
    aria-label="Close codex panel"
  >
    <!-- Slide-in panel -->
    <aside
      bind:this={panelElement}
      class="codex-panel"
      class:open={isOpen}
      role="complementary"
      aria-label="Pictograph reference panel"
    >
      <!-- Panel header -->
      <header class="panel-header">
        <h2 class="panel-title">{title}</h2>
        <button
          class="close-button"
          onclick={closePanel}
          aria-label="Close panel"
          type="button"
        >
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </header>

      <!-- Panel content -->
      <div class="panel-content">
        <CodexComponent
          isVisible={isOpen}
          onPictographSelected={handlePictographSelected}
        />
      </div>

      <!-- Quick tip -->
      <div class="panel-footer">
        <p class="tip">
          <span class="tip-icon">💡</span>
          <span class="tip-text">Tap any pictograph to view details</span>
        </p>
      </div>
    </aside>
  </div>
{/if}

<style>
  /* Backdrop overlay */
  .codex-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(4px);
    z-index: 1000;
    animation: fadeIn 300ms ease-out;
    cursor: pointer;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  /* Slide-in panel */
  .codex-panel {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    width: 600px;
    max-width: 90vw;
    background: var(--background, #1a1a1a);
    border-left: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
    box-shadow: -4px 0 24px rgba(0, 0, 0, 0.3);
    display: flex;
    flex-direction: column;
    animation: slideIn 300ms cubic-bezier(0.16, 1, 0.3, 1);
    cursor: default;
    overflow: hidden;
  }

  @keyframes slideIn {
    from {
      transform: translateX(100%);
    }
    to {
      transform: translateX(0);
    }
  }

  /* Panel header */
  .panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.5rem;
    border-bottom: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
    background: var(--surface, #242424);
  }

  .panel-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--foreground, #ffffff);
    margin: 0;
  }

  .close-button {
    width: 44px;
    height: 44px;
    min-width: 44px;
    min-height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border: none;
    color: var(--foreground-muted, rgba(255, 255, 255, 0.7));
    cursor: pointer;
    border-radius: 8px;
    transition: all 200ms ease;
    padding: 0;
  }

  .close-button:hover {
    background: var(--hover-bg, rgba(255, 255, 255, 0.1));
    color: var(--foreground, #ffffff);
    transform: scale(1.05);
  }

  .close-button:active {
    transform: scale(0.95);
  }

  .close-button:focus-visible {
    outline: 2px solid var(--accent, #4a9eff);
    outline-offset: 2px;
  }

  /* Panel content */
  .panel-content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 1rem;
  }

  /* Custom scrollbar */
  .panel-content::-webkit-scrollbar {
    width: 8px;
  }

  .panel-content::-webkit-scrollbar-track {
    background: var(--surface, #242424);
  }

  .panel-content::-webkit-scrollbar-thumb {
    background: var(--border-color, rgba(255, 255, 255, 0.2));
    border-radius: 4px;
  }

  .panel-content::-webkit-scrollbar-thumb:hover {
    background: var(--border-color, rgba(255, 255, 255, 0.3));
  }

  /* Panel footer */
  .panel-footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
    background: var(--surface, #242424);
  }

  .tip {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0;
    font-size: 0.875rem;
    color: var(--foreground-muted, rgba(255, 255, 255, 0.6));
  }

  .tip-icon {
    font-size: 1rem;
    flex-shrink: 0;
  }

  .tip-text {
    flex: 1;
  }

  /* Mobile responsiveness */
  @media (max-width: 768px) {
    .codex-panel {
      width: 100vw;
      max-width: 100vw;
    }

    .panel-header {
      padding: 1rem;
    }

    .panel-title {
      font-size: 1.25rem;
    }

    .panel-content {
      padding: 0.75rem;
    }

    .panel-footer {
      padding: 0.75rem 1rem;
    }

    .tip {
      font-size: 0.8125rem;
    }
  }

  @media (max-width: 480px) {
    .panel-title {
      font-size: 1.125rem;
    }

    .tip {
      font-size: 0.75rem;
    }
  }

  /* Accessibility - reduce motion */
  @media (prefers-reduced-motion: reduce) {
    .codex-backdrop,
    .codex-panel {
      animation: none;
    }

    .close-button {
      transition: none;
    }
  }
</style>
