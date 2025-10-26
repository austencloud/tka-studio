<!--
EditSlidePanel.svelte - Ultra-modern slide-out edit panel

Features:
- 🎨 Glassmorphism with backdrop blur
- 🌊 Smooth spring animations
- ⌨️ Keyboard shortcuts (Esc to close)
- 📱 Mobile-friendly with swipe gestures
- 🎯 Context-aware editing without leaving the flow
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onDestroy, onMount } from 'svelte';
  import { backOut, quintOut } from 'svelte/easing';
  import { fade, fly } from 'svelte/transition';
  import type { BeatData } from "$build/workspace-panel";
  import MainAdjustmentPanel from './MainAdjustmentPanel.svelte';

  // Props
  const {
    isOpen = false,
    onClose,
    selectedBeatIndex,
    selectedBeatData,
    onOrientationChanged,
    onTurnAmountChanged,
  } = $props<{
    isOpen: boolean;
    onClose: () => void;
    selectedBeatIndex: number | null;
    selectedBeatData: BeatData | null;
    onOrientationChanged: (color: string, orientation: string) => void;
    onTurnAmountChanged: (color: string, turnAmount: number) => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService | null = null;

  // Component refs
  let mainAdjustmentPanelRef: MainAdjustmentPanel | null = $state(null);
  let panelElement: HTMLElement | null = $state(null);

  // Touch gesture state
  let touchStartX = $state(0);
  let touchCurrentX = $state(0);
  let isDragging = $state(false);

  // Device detection for responsive behavior
  let isMobile = $state(false);
  let windowWidth = $state(0);

  // Keyboard handler
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape' && isOpen) {
      event.preventDefault();
      handleClose();
    }
  }

  // Close handler with haptic feedback
  function handleClose() {
    hapticService?.trigger('selection');
    onClose();
  }

  // Backdrop click handler
  function handleBackdropClick(event: MouseEvent) {
    // Only close if clicking the backdrop itself, not the panel
    if (event.target === event.currentTarget) {
      handleClose();
    }
  }

  // Touch gesture handlers for swipe-to-dismiss (mobile)
  function handleTouchStart(event: TouchEvent) {
    if (!isMobile) return;
    touchStartX = event.touches[0].clientX;
    touchCurrentX = touchStartX;
    isDragging = true;
  }

  function handleTouchMove(event: TouchEvent) {
    if (!isDragging || !isMobile) return;
    touchCurrentX = event.touches[0].clientX;

    // Only allow dragging to the right (to close)
    const deltaX = touchCurrentX - touchStartX;
    if (deltaX > 0 && panelElement) {
      panelElement.style.transform = `translateX(${deltaX}px)`;
    }
  }

  function handleTouchEnd() {
    if (!isDragging || !isMobile) return;
    isDragging = false;

    const deltaX = touchCurrentX - touchStartX;
    const threshold = 100; // Swipe threshold in pixels

    if (panelElement) {
      if (deltaX > threshold) {
        // Swipe far enough - close the panel
        hapticService?.trigger('warning');
        onClose();
      } else {
        // Snap back
        panelElement.style.transform = 'translateX(0)';
        panelElement.style.transition = 'transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)';
        setTimeout(() => {
          if (panelElement) {
            panelElement.style.transition = '';
          }
        }, 300);
      }
    }
  }

  // Window resize handler
  function handleResize() {
    if (typeof window !== 'undefined') {
      windowWidth = window.innerWidth;
      isMobile = windowWidth < 768;
    }
  }

  // Lifecycle
  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
    handleResize();

    // Add event listeners
    window.addEventListener('keydown', handleKeydown);
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('keydown', handleKeydown);
      window.removeEventListener('resize', handleResize);
    };
  });

  onDestroy(() => {
    window.removeEventListener('keydown', handleKeydown);
    window.removeEventListener('resize', handleResize);
  });

  // Reactive: Trigger haptic when panel opens
  $effect(() => {
    if (isOpen) {
      hapticService?.trigger('selection');
    }
  });
</script>

{#if isOpen}
  <!-- Backdrop with blur - ultra-modern glassmorphism -->
  <div
    class="edit-panel-backdrop"
    transition:fade={{ duration: 250, easing: quintOut }}
    onclick={handleBackdropClick}
    onkeydown={(e) => e.key === 'Enter' && handleBackdropClick(e as unknown as MouseEvent)}
    role="button"
    tabindex="-1"
    aria-label="Close edit panel"
  >
    <!-- Panel slides in from right with bouncy animation -->
    <div
      bind:this={panelElement}
      class="edit-panel"
      class:mobile={isMobile}
      transition:fly={{ x: 500, duration: 350, easing: backOut }}
      role="dialog"
      aria-modal="true"
      aria-labelledby="edit-panel-title"
      tabindex="0"
      ontouchstart={handleTouchStart}
      ontouchmove={handleTouchMove}
      ontouchend={handleTouchEnd}
      onclick={(e) => e.stopPropagation()}
      onkeydown={(e) => e.key === 'Enter' && e.stopPropagation()}
    >
      <!-- Header with close button -->
      <div class="edit-panel-header">
        <h2 id="edit-panel-title" class="edit-panel-title">
          <span class="title-icon">✨</span>
          Edit Beat
          {#if selectedBeatIndex !== null}
            <span class="beat-number">#{selectedBeatIndex}</span>
          {/if}
        </h2>

        <button
          class="close-button"
          onclick={handleClose}
          aria-label="Close edit panel"
          type="button"
        >
          <i class="fas fa-times"></i>
        </button>
      </div>

      <!-- Drag handle for mobile (visual indicator) -->
      {#if isMobile}
        <div class="drag-handle-container">
          <div class="drag-handle"></div>
        </div>
      {/if}

      <!-- Keyboard hint (desktop only) -->
      {#if !isMobile}
        <div class="keyboard-hint">
          Press <kbd>Esc</kbd> to close
        </div>
      {/if}

      <!-- Main content - your existing edit UI -->
      <div class="edit-panel-content">
        <MainAdjustmentPanel
          bind:this={mainAdjustmentPanelRef}
          {selectedBeatIndex}
          {selectedBeatData}
          {onOrientationChanged}
          {onTurnAmountChanged}
        />
      </div>
    </div>
  </div>
{/if}

<style>
  /* Backdrop - glassmorphism with blur */
  .edit-panel-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1000;

    /* Ultra-modern backdrop blur */
    backdrop-filter: blur(8px) saturate(180%);
    background: rgba(0, 0, 0, 0.4);

    display: flex;
    align-items: stretch;
    justify-content: flex-end;

    /* Prevent scroll on body when open */
    overflow: hidden;
  }

  /* The slide-out panel itself */
  .edit-panel {
    position: relative;
    width: min(600px, 90vw);
    height: 100%;

    /* Glassmorphism - the hot 2025 vibe */
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.15) 0%,
      rgba(255, 255, 255, 0.05) 100%
    );
    backdrop-filter: blur(20px) saturate(180%);
    border-left: 1px solid rgba(255, 255, 255, 0.2);

    /* Premium shadow */
    box-shadow:
      -8px 0 32px rgba(0, 0, 0, 0.3),
      -2px 0 8px rgba(0, 0, 0, 0.2),
      inset 1px 0 0 rgba(255, 255, 255, 0.1);

    display: flex;
    flex-direction: column;

    /* Smooth hardware-accelerated rendering */
    will-change: transform;
    transform: translateZ(0);
  }

  /* Mobile full-width */
  .edit-panel.mobile {
    width: 100vw;
    border-left: none;
  }

  /* Header */
  .edit-panel-header {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-lg) var(--spacing-xl);

    background: linear-gradient(
      180deg,
      rgba(255, 255, 255, 0.1) 0%,
      rgba(255, 255, 255, 0.05) 100%
    );
    border-bottom: 1px solid rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
  }

  .edit-panel-title {
    margin: 0;
    font-size: var(--font-size-xl);
    font-weight: 700;
    color: var(--foreground);
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);

    /* Subtle text shadow for depth */
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .title-icon {
    font-size: var(--font-size-2xl);
    animation: float 3s ease-in-out infinite;
  }

  @keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-4px); }
  }

  .beat-number {
    font-size: var(--font-size-md);
    color: var(--primary-light);
    background: rgba(var(--primary-rgb), 0.2);
    padding: 2px 8px;
    border-radius: 12px;
    font-weight: 600;
  }

  /* Close button - modern and clean */
  .close-button {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: none;
    background: rgba(255, 255, 255, 0.1);
    color: var(--foreground);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
    font-size: var(--font-size-lg);

    /* Subtle inner shadow */
    box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
  }

  .close-button:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: scale(1.1) rotate(90deg);
    box-shadow:
      inset 0 1px 2px rgba(0, 0, 0, 0.1),
      0 4px 12px rgba(0, 0, 0, 0.2);
  }

  .close-button:active {
    transform: scale(0.95) rotate(90deg);
  }

  /* Drag handle for mobile */
  .drag-handle-container {
    padding: var(--spacing-sm) 0;
    display: flex;
    justify-content: center;
    background: rgba(255, 255, 255, 0.05);
  }

  .drag-handle {
    width: 40px;
    height: 4px;
    border-radius: 2px;
    background: rgba(255, 255, 255, 0.3);
    cursor: grab;
  }

  .drag-handle:active {
    cursor: grabbing;
  }

  /* Keyboard hint */
  .keyboard-hint {
    padding: var(--spacing-sm) var(--spacing-xl);
    font-size: var(--font-size-sm);
    color: var(--muted-foreground);
    text-align: right;
    background: rgba(0, 0, 0, 0.1);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .keyboard-hint kbd {
    padding: 2px 6px;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.2);
    font-family: monospace;
    font-size: var(--font-size-xs);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  /* Content area - scrollable */
  .edit-panel-content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding: var(--spacing-lg);

    /* Custom scrollbar for modern look */
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
  }

  .edit-panel-content::-webkit-scrollbar {
    width: 8px;
  }

  .edit-panel-content::-webkit-scrollbar-track {
    background: transparent;
  }

  .edit-panel-content::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
    transition: background 0.2s;
  }

  .edit-panel-content::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.5);
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .edit-panel-header {
      padding: var(--spacing-md) var(--spacing-lg);
    }

    .edit-panel-title {
      font-size: var(--font-size-lg);
    }

    .edit-panel-content {
      padding: var(--spacing-md);
    }
  }

  /* Extra small screens (Z Fold folded) */
  @media (max-width: 320px) {
    .edit-panel-title {
      font-size: var(--font-size-md);
    }

    .title-icon {
      font-size: var(--font-size-lg);
    }

    .close-button {
      width: 36px;
      height: 36px;
    }
  }
</style>
