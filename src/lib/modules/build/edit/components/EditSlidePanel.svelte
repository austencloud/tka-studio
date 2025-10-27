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
  import type { BeatData } from "$build/workspace-panel";
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onDestroy, onMount } from 'svelte';
  import { backOut, quintOut } from 'svelte/easing';
  import { fade, fly } from 'svelte/transition';
  import EditPanelLayout from './EditPanelLayout.svelte';

  // Props
  const {
    isOpen = false,
    onClose,
    selectedBeatNumber,
    selectedBeatData,
    toolPanelHeight = 0,
    onOrientationChanged,
    onTurnAmountChanged,
  } = $props<{
    isOpen: boolean;
    onClose: () => void;
    selectedBeatNumber: number | null; // 0=start, 1=first beat, 2=second beat, etc.
    selectedBeatData: BeatData | null;
    toolPanelHeight?: number;
    onOrientationChanged: (color: string, orientation: string) => void;
    onTurnAmountChanged: (color: string, turnAmount: number) => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService | null = null;

  // Component refs
  let editPanelLayoutRef: EditPanelLayout | null = $state(null);
  let panelElement: HTMLElement | null = $state(null);

  // Touch gesture state
  let touchStartX = $state(0);
  let touchCurrentX = $state(0);
  let touchStartY = $state(0);
  let touchCurrentY = $state(0);
  let isDragging = $state(false);

  // Device detection for responsive behavior
  let isMobile = $state(false);
  let windowWidth = $state(0);

  // Calculate panel height for mobile (use tool panel height when available)
  const panelHeightStyle = $derived(() => {
    if (!isMobile) return '';
    // Use tool panel height if available, fallback to 75vh
    if (toolPanelHeight > 0) {
      return `height: ${toolPanelHeight}px;`;
    }
    return 'max-height: 75vh;';
  });

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

  // Note: No backdrop click handler - allow clicking beats to switch editing
  // Users can close via: X button, Escape key, or swipe gesture

  // Touch gesture handlers for swipe-to-dismiss
  // Mobile: Vertical swipe (down to dismiss from bottom)
  // Desktop: Horizontal swipe (right to dismiss from side)
  function handleTouchStart(event: TouchEvent) {
    touchStartX = event.touches[0].clientX;
    touchCurrentX = touchStartX;
    touchStartY = event.touches[0].clientY;
    touchCurrentY = touchStartY;
    isDragging = true;
  }

  function handleTouchMove(event: TouchEvent) {
    if (!isDragging) return;
    touchCurrentX = event.touches[0].clientX;
    touchCurrentY = event.touches[0].clientY;

    if (isMobile) {
      // Mobile: Allow dragging downward (to close from bottom)
      const deltaY = touchCurrentY - touchStartY;
      if (deltaY > 0 && panelElement) {
        panelElement.style.transform = `translateY(${deltaY}px)`;
      }
    } else {
      // Desktop: Allow dragging to the right (to close from side)
      const deltaX = touchCurrentX - touchStartX;
      if (deltaX > 0 && panelElement) {
        panelElement.style.transform = `translateX(${deltaX}px)`;
      }
    }
  }

  function handleTouchEnd() {
    if (!isDragging) return;
    isDragging = false;

    const threshold = 100; // Swipe threshold in pixels

    if (panelElement) {
      if (isMobile) {
        // Mobile: Check vertical swipe distance
        const deltaY = touchCurrentY - touchStartY;
        if (deltaY > threshold) {
          // Swipe far enough - close the panel
          hapticService?.trigger('warning');
          onClose();
        } else {
          // Snap back
          panelElement.style.transform = 'translateY(0)';
          panelElement.style.transition = 'transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)';
          setTimeout(() => {
            if (panelElement) {
              panelElement.style.transition = '';
            }
          }, 300);
        }
      } else {
        // Desktop: Check horizontal swipe distance
        const deltaX = touchCurrentX - touchStartX;
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
  <!-- Backdrop - transparent, allows clicking through to beats -->
  <div
    class="edit-panel-backdrop"
    transition:fade={{ duration: 250, easing: quintOut }}
  >
    <!-- Panel slides in - from bottom on mobile, from right on desktop -->
    <div
      bind:this={panelElement}
      class="edit-panel"
      class:mobile={isMobile}
      style={panelHeightStyle()}
      transition:fly={isMobile
        ? { y: 500, duration: 350, easing: backOut }
        : { x: 500, duration: 350, easing: backOut }}
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
          {#if selectedBeatNumber === 0}
            Edit Start Position
          {:else}
            Edit Beat
            {#if selectedBeatNumber !== null}
              <span class="beat-number">#{selectedBeatNumber}</span>
            {/if}
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


      <!-- Keyboard hint (desktop only) -->
      {#if !isMobile}
        <div class="keyboard-hint">
          Press <kbd>Esc</kbd> to close
        </div>
      {/if}

      <!-- Main content - Pictograph + Edit Controls with Responsive Layout -->
      <div class="edit-panel-content">
        <EditPanelLayout
          bind:this={editPanelLayoutRef}
          {selectedBeatNumber}
          {selectedBeatData}
          {onOrientationChanged}
          {onTurnAmountChanged}
        />
      </div>
    </div>
  </div>
{/if}

<style>
  /* Backdrop - transparent, allows sequence to remain visible AND clickable */
  .edit-panel-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1000;

    /* NO blur - keep sequence visible and clear */
    background: transparent;

    display: flex;
    align-items: stretch;
    justify-content: flex-end;

    /* Allow clicks to pass through backdrop to beats behind */
    pointer-events: none;
  }

  /* Mobile: Align panel to bottom instead of right */
  @media (max-width: 768px) {
    .edit-panel-backdrop {
      align-items: flex-end;
      justify-content: stretch;
    }
  }

  /* The slide-out panel itself - OPAQUE, not glass */
  .edit-panel {
    position: relative;
    width: min(600px, 90vw);
    height: 100%;

    /* FULLY OPAQUE solid background - dark theme color */
    background: #1a1a2e;
    border-left: 1px solid rgba(255, 255, 255, 0.2);

    /* Premium shadow */
    box-shadow:
      -8px 0 32px rgba(0, 0, 0, 0.3),
      -2px 0 8px rgba(0, 0, 0, 0.2);

    display: flex;
    flex-direction: column;

    /* Smooth hardware-accelerated rendering */
    will-change: transform;
    transform: translateZ(0);

    /* Re-enable pointer events for the panel itself */
    pointer-events: auto;
  }

  /* Mobile: Full-width bottom panel with beautiful rounded top corners */
  .edit-panel.mobile {
    width: 100vw;
    /* Height set dynamically via inline style to match tool panel height */
    /* Fallback max-height if dynamic height not available */
    max-height: 75vh;

    /* Remove side border, add top border */
    border-left: none;
    border-top: 1px solid hsl(var(--border));

    /* Gorgeous rounded top corners for bottom-slide aesthetic */
    border-radius: 24px 24px 0 0;

    /* Shadow goes UPWARD for bottom panel - stronger for visibility */
    box-shadow:
      0 -8px 32px rgba(0, 0, 0, 0.4),
      0 -4px 16px rgba(0, 0, 0, 0.3),
      0 -2px 8px rgba(0, 0, 0, 0.2);

    /* Entire panel is draggable */
    cursor: grab;
  }

  .edit-panel.mobile:active {
    cursor: grabbing;
  }

  /* Subtle drag indicator at top - doesn't take layout space */
  .edit-panel.mobile::before {
    content: '';
    position: absolute;
    top: 8px;
    left: 50%;
    transform: translateX(-50%);
    width: 40px;
    height: 4px;
    border-radius: 2px;
    background: rgba(255, 255, 255, 0.3);
    pointer-events: none;
    z-index: 1;
  }

  /* Header */
  .edit-panel-header {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-lg) var(--spacing-xl);

    /* Solid opaque header - matches panel background */
    background: #252540;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
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
    background: hsl(var(--muted));
    color: hsl(var(--foreground));
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
    background: hsl(var(--muted) / 0.8);
    transform: scale(1.1) rotate(90deg);
    box-shadow:
      inset 0 1px 2px rgba(0, 0, 0, 0.1),
      0 4px 12px rgba(0, 0, 0, 0.2);
  }

  .close-button:active {
    transform: scale(0.95) rotate(90deg);
  }


  /* Keyboard hint */
  .keyboard-hint {
    padding: var(--spacing-sm) var(--spacing-xl);
    font-size: var(--font-size-sm);
    color: #a0a0b0;
    text-align: right;
    background: #1a1a2e;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  }

  .keyboard-hint kbd {
    padding: 2px 6px;
    border-radius: 4px;
    background: hsl(var(--muted));
    border: 1px solid hsl(var(--border));
    font-family: monospace;
    font-size: var(--font-size-xs);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  /* Content area - IMPORTANT: Remove padding here, let layout component handle it */
  .edit-panel-content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;

    /* FULLY OPAQUE - matches panel background exactly */
    background: #1a1a2e;

    /* Ensure full height for container queries to work */
    min-height: 0; /* Critical for flexbox scrolling */

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
      /* Rounded top corners to match panel */
      border-radius: 24px 24px 0 0;
    }

    .edit-panel-title {
      font-size: var(--font-size-lg);
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
