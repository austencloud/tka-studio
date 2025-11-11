<!--
  ModuleList - Module switching UI component (2026 Premium Design)

  Displays a list of available modules (main and developer) and allows
  the user to switch between them with visual feedback for the current module.

  Features:
  - Module-specific gradient colors extracted from icon HTML
  - Premium glassmorphic card design with layered backgrounds
  - Icon glow effects matching desktop sidebar quality
  - Active indicator dots (not checkboxes - avoids misleading UX)
  - Sophisticated hover effects with radial gradients
-->
<script lang="ts">
  import type { ModuleDefinition, ModuleId } from "../domain/types";
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { preloadFeatureModule } from "../../inversify/container";
  import { onMount } from "svelte";

  let {
    currentModule,
    modules = [],
    onModuleSelect,
  } = $props<{
    currentModule: ModuleId;
    modules: ModuleDefinition[];
    onModuleSelect?: (moduleId: ModuleId) => void;
  }>();

  let hapticService: IHapticFeedbackService;

  // Track drag state to prevent clicks during swipe gestures
  let dragState = $state<{
    isDragging: boolean;
    startY: number;
    startTime: number;
  }>({
    isDragging: false,
    startY: 0,
    startTime: 0,
  });

  // Track hover timers for preloading (2025 standard: 50ms delay)
  let hoverTimers = new Map<ModuleId, number>();

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Filter to main modules and dev modules
  const mainModules = $derived(
    modules.filter((m: ModuleDefinition) => m.isMain)
  );
  const devModules = $derived(
    modules.filter((m: ModuleDefinition) => !m.isMain)
  );

  /**
   * 🎨 Extract primary color from module icon HTML
   * Parses gradient/color values from icon SVG or inline styles
   * Falls back to purple gradient if no color found
   */
  function extractModuleColor(iconHtml: string): string {
    // Try to find gradient color in SVG or inline styles
    const gradientMatch = iconHtml.match(/stop-color[:\s=]["']?([#\w]+)/);
    if (gradientMatch?.[1]) return gradientMatch[1];

    const colorMatch = iconHtml.match(/color[:\s=]["']?([#\w]+)/);
    if (colorMatch?.[1]) return colorMatch[1];

    // Default fallback gradient color
    return "#667eea";
  }

  function handlePointerDown(event: PointerEvent | MouseEvent) {
    dragState.isDragging = false;
    dragState.startY = event.clientY;
    dragState.startTime = Date.now();
  }

  function handlePointerMove(event: PointerEvent | MouseEvent) {
    const deltaY = Math.abs(event.clientY - dragState.startY);
    // If moved more than 10px vertically, consider it a drag
    if (deltaY > 10) {
      dragState.isDragging = true;
    }
  }

  function handleModuleClick(
    moduleId: ModuleId,
    event: PointerEvent | MouseEvent,
    isDisabled: boolean = false
  ) {
    // Don't trigger click for disabled modules
    if (isDisabled) {
      event.preventDefault();
      event.stopPropagation();
      return;
    }

    // If user was dragging, don't trigger the click
    if (dragState.isDragging) {
      event.preventDefault();
      event.stopPropagation();
      return;
    }

    // If the pointer was down for more than 300ms and moved, likely a drag
    const duration = Date.now() - dragState.startTime;
    const deltaY = Math.abs(event.clientY - dragState.startY);
    if (duration > 300 && deltaY > 5) {
      event.preventDefault();
      event.stopPropagation();
      return;
    }

    hapticService?.trigger("selection");
    onModuleSelect?.(moduleId);
  }

  /**
   * ⚡ PERFORMANCE: Hover-based preloading (2025 best practice)
   * Preload module DI services after 50ms hover (user intent detection)
   * By the time user clicks, module is already loaded = instant navigation
   */
  function handleModuleHoverStart(moduleId: ModuleId) {
    // Don't preload if already active
    if (moduleId === currentModule) {
      return;
    }

    // Clear any existing timer
    const existingTimer = hoverTimers.get(moduleId);
    if (existingTimer) {
      clearTimeout(existingTimer);
    }

    // Start 50ms timer before preloading (industry standard)
    const timer = setTimeout(() => {
      try {
        preloadFeatureModule(moduleId);
      } catch (error) {
        // Silently ignore modules without DI dependencies (e.g., about page)
        console.debug(`Module ${moduleId} has no DI dependencies to preload`);
      }
      hoverTimers.delete(moduleId);
    }, 50) as unknown as number;

    hoverTimers.set(moduleId, timer);
  }

  /**
   * Cancel preload if user moves away before 50ms
   */
  function handleModuleHoverEnd(moduleId: ModuleId) {
    const timer = hoverTimers.get(moduleId);
    if (timer) {
      clearTimeout(timer);
      hoverTimers.delete(moduleId);
    }
  }
</script>

<!-- Main Modules Section -->
<section class="module-section">
  <h3 class="section-title">Switch Module</h3>
  <div class="module-items">
    {#each mainModules as module}
      {@const moduleColor = extractModuleColor(module.icon)}
      {@const isActive = currentModule === module.id}
      {@const isDisabled = module.disabled ?? false}

      <button
        class="module-item"
        class:active={isActive}
        class:disabled={isDisabled}
        onpointerdown={handlePointerDown}
        onpointermove={handlePointerMove}
        onclick={(e) => handleModuleClick(module.id, e, isDisabled)}
        onmouseenter={() => !isDisabled && handleModuleHoverStart(module.id)}
        onmouseleave={() => !isDisabled && handleModuleHoverEnd(module.id)}
        style="--module-color: {moduleColor};"
        aria-disabled={isDisabled}
        disabled={isDisabled}
      >
        <!-- Premium layered background -->
        <div class="card-background"></div>
        <div class="hover-glow"></div>

        <!-- Content layer -->
        <div class="item-content">
          <span class="item-icon">{@html module.icon}</span>
          <div class="item-info">
            <span class="item-label">{module.label}</span>
            {#if module.description}
              <span class="item-description">{module.description}</span>
            {/if}
          </div>

          <!-- Coming soon badge for disabled modules -->
          {#if isDisabled && module.disabledMessage}
            <div class="disabled-badge">{module.disabledMessage}</div>
          {:else if isActive}
            <!-- Active indicator dot -->
            <div class="active-indicator"></div>
          {/if}
        </div>
      </button>
    {/each}
  </div>
</section>

<!-- Developer/Admin Modules Section -->
{#if devModules.length > 0}
  <section class="module-section">
    <h3 class="section-title">Developer Tools</h3>
    <div class="module-items">
      {#each devModules as module}
        {@const moduleColor = extractModuleColor(module.icon)}
        {@const isActive = currentModule === module.id}
        {@const isDisabled = module.disabled ?? false}

        <button
          class="module-item"
          class:active={isActive}
          class:disabled={isDisabled}
          onpointerdown={handlePointerDown}
          onpointermove={handlePointerMove}
          onclick={(e) => handleModuleClick(module.id, e, isDisabled)}
          onmouseenter={() => !isDisabled && handleModuleHoverStart(module.id)}
          onmouseleave={() => !isDisabled && handleModuleHoverEnd(module.id)}
          style="--module-color: {moduleColor};"
          aria-disabled={isDisabled}
          disabled={isDisabled}
        >
          <!-- Premium layered background -->
          <div class="card-background"></div>
          <div class="hover-glow"></div>

          <!-- Content layer -->
          <div class="item-content">
            <span class="item-icon">{@html module.icon}</span>
            <div class="item-info">
              <span class="item-label">{module.label}</span>
              {#if module.description}
                <span class="item-description">{module.description}</span>
              {/if}
            </div>

            <!-- Coming soon badge for disabled modules -->
            {#if isDisabled && module.disabledMessage}
              <div class="disabled-badge">{module.disabledMessage}</div>
            {:else if isActive}
              <!-- Active indicator dot -->
              <div class="active-indicator"></div>
            {/if}
          </div>
        </button>
      {/each}
    </div>
  </section>
{/if}

<style>
  /* ============================================================================
     2026 PREMIUM MODULE LIST DESIGN
     ============================================================================ */

  .module-section {
    margin-bottom: 24px;
  }

  .module-section:last-child {
    margin-bottom: 0;
  }

  .section-title {
    margin: 0 0 16px 0;
    padding: 0 8px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: rgba(255, 255, 255, 0.5);
  }

  .module-items {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  /* ============================================================================
     MODULE ITEM - PREMIUM CARD DESIGN
     ============================================================================ */
  .module-item {
    position: relative;
    display: flex;
    align-items: stretch;
    min-height: 72px;
    background: transparent;
    border: none;
    border-radius: 16px;
    color: rgba(255, 255, 255, 0.9);
    cursor: pointer;
    text-align: left;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    isolation: isolate;
  }

  /* Layered Background System */
  .card-background {
    position: absolute;
    inset: 0;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.08) 0%,
      rgba(255, 255, 255, 0.04) 100%
    );
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 0;
  }

  .hover-glow {
    position: absolute;
    inset: 0;
    background: radial-gradient(
      circle at 50% 50%,
      var(--module-color, #667eea) 0%,
      transparent 70%
    );
    opacity: 0;
    transition: opacity 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 1;
    mix-blend-mode: screen;
  }

  /* Content Layer */
  .item-content {
    position: relative;
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px 14px;
    width: 100%;
    z-index: 2;
  }

  /* ============================================================================
     HOVER STATES
     ============================================================================ */
  .module-item:hover .card-background {
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.12) 0%,
      rgba(255, 255, 255, 0.06) 100%
    );
    border-color: rgba(255, 255, 255, 0.18);
    transform: translateY(-2px);
  }

  .module-item:hover .hover-glow {
    opacity: 0.08;
  }

  .module-item:hover {
    transform: translateX(4px);
  }

  /* ============================================================================
     ACTIVE STATE - MODULE-SPECIFIC COLORS
     ============================================================================ */
  .module-item.active .card-background {
    background: linear-gradient(
      135deg,
      color-mix(in srgb, var(--module-color) 20%, transparent) 0%,
      color-mix(in srgb, var(--module-color) 8%, transparent) 100%
    );
    border-color: color-mix(in srgb, var(--module-color) 40%, transparent);
    box-shadow:
      0 0 20px color-mix(in srgb, var(--module-color) 15%, transparent),
      0 4px 12px rgba(0, 0, 0, 0.2);
  }

  .module-item.active .hover-glow {
    opacity: 0.12;
  }

  /* ============================================================================
     ICON WITH GLOW EFFECTS
     ============================================================================ */
  .item-icon {
    font-size: 28px;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .module-item:hover .item-icon {
    transform: scale(1.08);
  }

  /* Apply subtle shadow to icons */
  .item-icon :global(svg),
  .item-icon :global(i) {
    filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
  }

  /* Subtle glow on active state - just a hint of color */
  .module-item.active .item-icon :global(svg),
  .module-item.active .item-icon :global(i) {
    filter: drop-shadow(0 0 6px color-mix(in srgb, var(--module-color) 40%, transparent));
  }

  /* ============================================================================
     TEXT CONTENT
     ============================================================================ */
  .item-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-width: 0;
  }

  .item-label {
    font-size: 17px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    letter-spacing: -0.01em;
    transition: color 0.2s ease;
  }

  .module-item.active .item-label {
    color: rgba(255, 255, 255, 1);
  }

  .item-description {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
    line-height: 1.4;
    transition: color 0.2s ease;
  }

  .module-item.active .item-description {
    color: rgba(255, 255, 255, 0.75);
  }

  /* ============================================================================
     ACTIVE INDICATOR DOT
     ============================================================================ */
  .active-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--module-color, #667eea);
    flex-shrink: 0;
    box-shadow:
      0 0 12px var(--module-color),
      0 0 20px color-mix(in srgb, var(--module-color) 60%, transparent);
    animation: indicator-pulse 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  }

  @keyframes indicator-pulse {
    0% {
      transform: scale(0);
      opacity: 0;
    }
    50% {
      transform: scale(1.2);
    }
    100% {
      transform: scale(1);
      opacity: 1;
    }
  }

  /* ============================================================================
     PRESS/ACTIVE INTERACTION
     ============================================================================ */
  .module-item:active {
    transform: translateX(4px) scale(0.98);
  }

  .module-item.active:active {
    transform: translateX(2px) scale(0.98);
  }

  /* ============================================================================
     DISABLED STATE
     ============================================================================ */
  .module-item.disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .module-item.disabled:hover {
    transform: none;
  }

  .module-item.disabled:hover .card-background {
    transform: none;
  }

  .module-item.disabled:hover .hover-glow {
    opacity: 0;
  }

  .module-item.disabled .item-icon {
    opacity: 0.7;
  }

  .disabled-badge {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    padding: 4px 10px;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.12);
    color: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.2);
    letter-spacing: 0.6px;
    flex-shrink: 0;
  }

  /* ============================================================================
     ACCESSIBILITY & REDUCED MOTION
     ============================================================================ */
  @media (prefers-reduced-motion: reduce) {
    .module-item,
    .card-background,
    .hover-glow,
    .item-icon,
    .active-indicator {
      transition: none !important;
      animation: none !important;
    }

    .module-item:hover,
    .module-item:active {
      transform: none !important;
    }
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    .card-background {
      background: rgba(255, 255, 255, 0.15) !important;
      border: 2px solid rgba(255, 255, 255, 0.4) !important;
    }

    .module-item.active .card-background {
      background: rgba(255, 255, 255, 0.25) !important;
      border: 2px solid white !important;
    }
  }

  /* Focus styles for keyboard navigation */
  .module-item:focus-visible {
    outline: 2px solid rgba(102, 126, 234, 0.6);
    outline-offset: 3px;
  }
</style>
