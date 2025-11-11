<!--
SequenceDetailPanel - Adaptive detail view for sequences

Desktop (>= 768px): Side panel that slides in from right and pushes grid
Mobile (< 768px): Slide-up overlay modal

Features:
- Smooth slide transitions with CSS width/height
- Backdrop blur on mobile
- Responsive width on desktop (35%, 320-500px)
- Full-height panel
-->
<script lang="ts">
  import type { SequenceData } from "$shared";
  import SequenceDetailContent from "./SequenceDetailContent.svelte";

  const {
    sequence = null,
    isOpen = false,
    onClose = () => {},
    onAction = () => {},
    viewMode = "desktop", // 'desktop' | 'mobile'
  } = $props<{
    sequence?: SequenceData | null;
    isOpen?: boolean;
    onClose?: () => void;
    onAction?: (action: string, sequence: SequenceData) => void;
    viewMode?: "desktop" | "mobile";
  }>();

  // Handle backdrop click (mobile only)
  function handleBackdropClick(event: MouseEvent) {
    if (viewMode === "mobile") {
      onClose();
    }
  }

  // Prevent content clicks from bubbling to backdrop
  function handleContentClick(event: MouseEvent) {
    event.stopPropagation();
  }

  // Handle ESC key
  function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Escape" && isOpen) {
      onClose();
    }
  }
</script>

<svelte:window onkeydown={handleKeyDown} />

{#if viewMode === "mobile"}
  <!-- Mobile: Slide-up modal overlay -->
  {#if isOpen}
    <div
      class="detail-overlay"
      class:visible={isOpen}
      onclick={handleBackdropClick}
      role="presentation"
    >
      <div
        class="detail-panel-mobile"
        class:open={isOpen}
        onclick={handleContentClick}
        onkeydown={handleKeyDown}
        role="dialog"
        aria-modal="true"
        aria-labelledby="sequence-detail-title"
        tabindex="-1"
      >
        {#if sequence}
          <SequenceDetailContent {sequence} {onClose} {onAction} />
        {/if}
      </div>
    </div>
  {/if}
{:else}
  <!-- Desktop: Side panel (always rendered, width animated) -->
  <aside
    class="detail-panel-desktop"
    class:open={isOpen && sequence}
    aria-label="Sequence details"
    aria-hidden={!isOpen}
  >
    {#if sequence}
      <SequenceDetailContent {sequence} {onClose} {onAction} />
    {/if}
  </aside>
{/if}

<style>
  /* ===== DESKTOP SIDE PANEL ===== */
  .detail-panel-desktop {
    width: 0;
    min-width: 0;
    max-width: 500px;
    height: 100%;
    background: rgba(0, 0, 0, 0.9);
    border-left: 1px solid rgba(255, 255, 255, 0.2);
    overflow-y: hidden;
    overflow-x: hidden;
    flex-shrink: 0;
    box-shadow: -4px 0 20px rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(10px);
    transition:
      width 0.3s ease,
      min-width 0.3s ease,
      opacity 0.3s ease;
    opacity: 0;
    pointer-events: none;
  }

  .detail-panel-desktop.open {
    width: 35%;
    min-width: 320px;
    overflow-y: auto;
    opacity: 1;
    pointer-events: all;
  }

  /* Custom scrollbar for desktop panel */
  .detail-panel-desktop::-webkit-scrollbar {
    width: 8px;
  }

  .detail-panel-desktop::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.2);
  }

  .detail-panel-desktop::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
  }

  .detail-panel-desktop::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.3);
  }

  /* ===== MOBILE SLIDE-UP MODAL ===== */
  .detail-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0);
    backdrop-filter: blur(0px);
    z-index: 100;
    display: flex;
    align-items: flex-end;
    transition: background 0.3s ease, backdrop-filter 0.3s ease;
    pointer-events: none;
  }

  .detail-overlay.visible {
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(4px);
    pointer-events: all;
  }

  .detail-panel-mobile {
    width: 100%;
    height: 0;
    max-height: 0;
    background: rgba(0, 0, 0, 0.95);
    border-radius: 20px 20px 0 0;
    overflow-y: hidden;
    overflow-x: hidden;
    box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(10px);
    position: relative;
    transition:
      height 0.3s ease,
      max-height 0.3s ease,
      transform 0.3s ease;
    transform: translateY(100%);
  }

  .detail-panel-mobile.open {
    height: 75%;
    max-height: calc(100% - 80px);
    overflow-y: auto;
    transform: translateY(0);
  }

  .detail-panel-mobile::before {
    content: "";
    position: absolute;
    top: 12px;
    left: 50%;
    transform: translateX(-50%);
    width: 40px;
    height: 4px;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 2px;
    z-index: 1;
  }

  /* Custom scrollbar for mobile panel */
  .detail-panel-mobile::-webkit-scrollbar {
    width: 6px;
  }

  .detail-panel-mobile::-webkit-scrollbar-track {
    background: transparent;
  }

  .detail-panel-mobile::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 3px;
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .detail-panel-mobile {
      height: 80%;
      max-height: calc(100% - 60px);
    }
  }

  @media (max-width: 480px) {
    .detail-panel-mobile {
      height: 85%;
      max-height: calc(100% - 40px);
    }
  }

  /* Tablet adjustments for desktop panel */
  @media (min-width: 768px) and (max-width: 1024px) {
    .detail-panel-desktop {
      width: 40%;
      min-width: 280px;
      max-width: 400px;
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .detail-overlay {
      animation: none;
    }
  }

  /* Safe area insets for mobile notches */
  @supports (padding: env(safe-area-inset-bottom)) {
    .detail-panel-mobile {
      padding-bottom: env(safe-area-inset-bottom);
    }
  }
</style>
