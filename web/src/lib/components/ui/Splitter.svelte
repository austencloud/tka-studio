<!--
Resizable Splitter Component

Provides drag-to-resize functionality between panels.
Follows Svelte 5 runes pattern with clean event handling.
-->
<script lang="ts">
  // Direction can be "left" or "right" for horizontal splitters

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    direction = "right",
    disabled = false,
    thickness = 8,
    onResizeStart = () => {},
    onResizeMove = (deltaX: number) => {},
    onResizeEnd = () => {},
  } = $props<{
    direction?: "left" | "right";
    disabled?: boolean;
    thickness?: number;
    onResizeStart?: (startX: number) => void;
    onResizeMove?: (deltaX: number) => void;
    onResizeEnd?: () => void;
  }>();

  // ✅ PURE RUNES: Local component state
  let isDragging = $state(false);
  let startX = $state(0);
  let startY = $state(0);

  // Handle mouse down to start dragging
  function handleMouseDown(event: MouseEvent) {
    if (disabled) return;

    event.preventDefault();
    event.stopPropagation();

    isDragging = true;
    startX = event.clientX;
    startY = event.clientY;

    // Add global listeners for drag and release
    document.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseup", handleMouseUp);
    document.body.style.cursor =
      direction === "right" ? "col-resize" : "col-resize";
    document.body.style.userSelect = "none";

    onResizeStart(startX);
  }

  // Handle mouse move during drag
  function handleMouseMove(event: MouseEvent) {
    if (!isDragging) return;

    event.preventDefault();
    const currentX = event.clientX;
    const deltaX = currentX - startX;

    onResizeMove(deltaX);
  }

  // Handle mouse up to end drag
  function handleMouseUp(event: MouseEvent) {
    if (!isDragging) return;

    isDragging = false;

    // Remove global listeners
    document.removeEventListener("mousemove", handleMouseMove);
    document.removeEventListener("mouseup", handleMouseUp);
    document.body.style.cursor = "";
    document.body.style.userSelect = "";

    onResizeEnd();
  }

  // Handle touch events for mobile support
  function handleTouchStart(event: TouchEvent) {
    if (disabled) return;

    event.preventDefault();
    const touch = event.touches[0];
    if (!touch) return;

    isDragging = true;
    startX = touch.clientX;
    startY = touch.clientY;

    document.addEventListener("touchmove", handleTouchMove, { passive: false });
    document.addEventListener("touchend", handleTouchEnd);

    onResizeStart(startX);
  }

  function handleTouchMove(event: TouchEvent) {
    if (!isDragging) return;

    event.preventDefault();
    const touch = event.touches[0];
    if (!touch) return;

    const currentX = touch.clientX;
    const deltaX = currentX - startX;

    onResizeMove(deltaX);
  }

  function handleTouchEnd(event: TouchEvent) {
    if (!isDragging) return;

    isDragging = false;

    document.removeEventListener("touchmove", handleTouchMove);
    document.removeEventListener("touchend", handleTouchEnd);

    onResizeEnd();
  }

  // Cleanup on destroy
  import { onDestroy } from "svelte";
  onDestroy(() => {
    if (isDragging) {
      document.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseup", handleMouseUp);
      document.removeEventListener("touchmove", handleTouchMove);
      document.removeEventListener("touchend", handleTouchEnd);
      document.body.style.cursor = "";
      document.body.style.userSelect = "";
    }
  });
</script>

<div
  class="splitter"
  class:disabled
  class:dragging={isDragging}
  class:left-direction={direction === "left"}
  class:right-direction={direction === "right"}
  style="width: {thickness}px;"
  role="slider"
  tabindex={disabled ? -1 : 0}
  aria-label="Resize panel"
  aria-valuemin="10"
  aria-valuemax="90"
  aria-valuenow="50"
  onmousedown={handleMouseDown}
  ontouchstart={handleTouchStart}
  onkeydown={(e) => {
    // Allow keyboard resizing with arrow keys
    if (disabled) return;
    if (e.key === "ArrowLeft") {
      onResizeMove(-10);
    } else if (e.key === "ArrowRight") {
      onResizeMove(10);
    }
  }}
>
  <!-- Visual handle -->
  <div class="splitter-handle">
    <div class="splitter-grip">
      <div class="grip-dot"></div>
      <div class="grip-dot"></div>
      <div class="grip-dot"></div>
    </div>
  </div>
</div>

<style>
  .splitter {
    position: relative;
    flex-shrink: 0;
    cursor: col-resize;
    background: transparent;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10;
    transition: background-color 0.2s ease;
  }

  .splitter:hover:not(.disabled) {
    background: rgba(255, 255, 255, 0.05);
  }

  .splitter.dragging {
    background: rgba(255, 255, 255, 0.1);
  }

  .splitter.disabled {
    cursor: default;
    opacity: 0.3;
    pointer-events: none;
  }

  .splitter:focus-visible {
    outline: 2px solid var(--color-primary);
    outline-offset: -1px;
  }

  .splitter-handle {
    position: relative;
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    border-left: 1px solid transparent;
    border-right: 1px solid transparent;
    transition: border-color 0.2s ease;
  }

  .splitter:hover:not(.disabled) .splitter-handle {
    border-left-color: rgba(255, 255, 255, 0.1);
    border-right-color: rgba(255, 255, 255, 0.1);
  }

  .splitter.dragging .splitter-handle {
    border-left-color: var(--color-primary);
    border-right-color: var(--color-primary);
  }

  .splitter-grip {
    display: flex;
    flex-direction: column;
    gap: 3px;
    opacity: 0.4;
    transition: opacity 0.2s ease;
  }

  .splitter:hover:not(.disabled) .splitter-grip {
    opacity: 0.7;
  }

  .splitter.dragging .splitter-grip {
    opacity: 1;
  }

  .grip-dot {
    width: 3px;
    height: 3px;
    background: currentColor;
    border-radius: 50%;
  }

  /* Direction-specific styling */
  .splitter.left-direction {
    border-right: 1px solid rgba(255, 255, 255, 0.1);
  }

  .splitter.right-direction {
    border-left: 1px solid rgba(255, 255, 255, 0.1);
  }

  /* Responsive behavior */
  @media (max-width: 1024px) {
    .splitter {
      /* Make splitter thicker on touch devices */
      min-width: 12px;
    }

    .splitter-grip {
      transform: scale(1.2);
    }
  }

  @media (max-width: 768px) {
    .splitter {
      display: none; /* Hide splitters on mobile */
    }
  }

  /* High contrast mode support */
  @media (prefers-contrast: high) {
    .splitter-handle {
      border-left-color: currentColor;
      border-right-color: currentColor;
    }

    .grip-dot {
      background: currentColor;
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .splitter,
    .splitter-handle,
    .splitter-grip {
      transition: none;
    }
  }
</style>
