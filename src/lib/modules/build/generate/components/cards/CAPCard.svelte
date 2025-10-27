<!--
CAPCard.svelte - Card for selecting CAP type
MOBILE: Opens modal for detailed selection when clicked
DESKTOP: Shows inline component buttons for direct selection
-->
<script lang="ts">
  import { CAP_TYPE_LABELS } from "$build/generate/circular";
  import { CAP_COMPONENTS } from "$build/generate/shared/domain/constants/cap-constants";
  import type { ICAPTypeService, IHapticFeedbackService } from "$shared";
  import { CAPComponent, CAPType, FontAwesomeIcon, resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import CAPSelectionModal from "../modals/CAPSelectionModal.svelte";
  import BaseCard from "./BaseCard.svelte";

  let {
    currentCAPType,
    onCAPTypeChange,
    // 🎨 MAGICAL: Animated mesh gradient with vibrant colors (2025 design)
    color = "linear-gradient(135deg, #4338ca 0%, #6b21a8 12.5%, #db2777 25%, #f97316 37.5%, #eab308 50%, #22c55e 62.5%, #0891b2 75%, #3b82f6 87.5%, #6366f1 100%)",
    shadowColor = "270deg 70% 50%", // Purple shadow to match glow
    gridColumnSpan = 2,
    cardIndex = 0,
    headerFontSize = "9px"
  } = $props<{
    currentCAPType: CAPType;
    onCAPTypeChange: (capType: CAPType) => void;
    color?: string;
    shadowColor?: string;
    gridColumnSpan?: number;
    cardIndex?: number;
    headerFontSize?: string;
  }>();

  let hapticService: IHapticFeedbackService;
  let capTypeService: ICAPTypeService = resolve<ICAPTypeService>(TYPES.ICAPTypeService);
  let isExpanded = $state(false);
  let pendingCAPType = $state<CAPType | null>(null);
  let isDesktop = $state(false);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);

    // Simple desktop detection based on viewport width
    const checkDesktop = () => {
      isDesktop = window.innerWidth >= 1280;
    };
    checkDesktop();
    window.addEventListener('resize', checkDesktop);
    return () => window.removeEventListener('resize', checkDesktop);
  });

  // Get current selected components using service
  // Use pending CAP type if modal is open, otherwise use current
  const displayCAPType = $derived(pendingCAPType || currentCAPType);
  const selectedComponents = $derived(capTypeService.parseComponents(displayCAPType));

  // Desktop: Direct toggle with immediate application
  function toggleComponentDesktop(component: CAPComponent) {
    hapticService?.trigger("selection");
    const newComponents = new Set(selectedComponents);

    if (newComponents.has(component)) {
      newComponents.delete(component);
    } else {
      newComponents.add(component);
    }

    const capType = capTypeService.generateCAPType(newComponents);
    // Apply immediately on desktop (no modal, no pending)
    onCAPTypeChange(capType);
  }

  // Mobile: Toggle with pending state for modal
  function toggleComponentMobile(component: CAPComponent) {
    hapticService?.trigger("selection");
    const newComponents = new Set(selectedComponents);

    if (newComponents.has(component)) {
      newComponents.delete(component);
    } else {
      newComponents.add(component);
    }

    const capType = capTypeService.generateCAPType(newComponents);

    // Store pending change instead of applying immediately
    // This prevents card reconfiguration while modal is open
    pendingCAPType = capType;
  }

  function openExpanded() {
    hapticService?.trigger("selection");
    pendingCAPType = null; // Reset pending state
    isExpanded = true;
  }

  function closeExpanded() {
    hapticService?.trigger("selection");
    isExpanded = false;

    // Apply pending change now that modal is closed
    // This triggers card reconfiguration animation AFTER modal is gone
    if (pendingCAPType && pendingCAPType !== currentCAPType) {
      onCAPTypeChange(pendingCAPType);
    }
    pendingCAPType = null;
  }

  // Format CAP type display using user-friendly labels
  // Show pending CAP type on card if modal is open
  const capTypeDisplay = $derived(CAP_TYPE_LABELS[displayCAPType as CAPType] || displayCAPType);
</script>

<!-- CAP card with animated gradient wrapper -->
<div class="cap-card-wrapper" style="grid-column: span {gridColumnSpan}; --card-index: {cardIndex};">
  {#if isDesktop}
    <!-- DESKTOP: Inline component selection -->
    <div class="cap-card-desktop">
      <div class="cap-header" style="font-size: {headerFontSize};">CAP TYPE</div>
      <div class="cap-components-grid">
        {#each CAP_COMPONENTS as { component, label, icon, color: iconColor }}
          <button
            class="cap-component-btn"
            class:active={selectedComponents.has(component)}
            onclick={() => toggleComponentDesktop(component)}
            aria-label="Toggle {label}"
          >
            <span class="cap-icon">
              <FontAwesomeIcon {icon} size="1.2em" color={iconColor} />
            </span>
            <span class="cap-label">{label}</span>
          </button>
        {/each}
      </div>
    </div>
  {:else}
    <!-- MOBILE: Card that opens modal -->
    <BaseCard
      title="CAP Type"
      currentValue={capTypeDisplay}
      color="transparent"
      {shadowColor}
      gridColumnSpan={1}
      {cardIndex}
      {headerFontSize}
      onClick={openExpanded}
    />
  {/if}
</div>

<!-- CAP Selection Modal (Mobile only) -->
{#if !isDesktop}
  <CAPSelectionModal
    isOpen={isExpanded}
    {selectedComponents}
    onToggleComponent={toggleComponentMobile}
    onClose={closeExpanded}
  />
{/if}

<style>
  /* ✨ Animated CAP Card - Mesh Gradient Wrapper */

  /* The wrapper has the animated gradient background */
  .cap-card-wrapper {
    /* Enable container queries to detect card width AND height */
    container-type: size;
    container-name: cap-card;

    position: relative;
    border-radius: 16px;
    overflow: hidden;

    /* Animated mesh gradient background */
    background: linear-gradient(135deg,
      #4338ca 0%,
      #6b21a8 12.5%,
      #db2777 25%,
      #f97316 37.5%,
      #eab308 50%,
      #22c55e 62.5%,
      #0891b2 75%,
      #3b82f6 87.5%,
      #6366f1 100%
    );
    background-size: 300% 300%;

    /* Subtle shadow without glow (glow moved to Generate button) */
    box-shadow:
      0 2px 4px rgba(0, 0, 0, 0.15),
      0 4px 8px rgba(0, 0, 0, 0.10),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);

    /* Apply ONLY gradient flow and entrance animations (no glow pulse) */
    /* Glow is now on the Generate button instead */
    animation: meshGradientFlow 15s ease infinite, cardEnter 0.4s ease-out;
  }

  /* The BaseCard inside is transparent to show the wrapper's background */
  /* Disable its entrance animation since the wrapper handles it */
  .cap-card-wrapper :global(.base-card) {
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
    /* Remove entrance animation - the wrapper handles it */
    animation: none !important;
  }

  /* Maintain hover effects */
  .cap-card-wrapper:hover {
    transform: translateY(-4px) scale(1.01);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  /* Card entrance animation - clean fade in (matches BaseCard) */
  @keyframes cardEnter {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  /* Mesh Gradient Animation - Organic flowing colors */
  @keyframes meshGradientFlow {
    0%, 100% {
      background-position: 0% 50%;
    }
    25% {
      background-position: 50% 100%;
    }
    50% {
      background-position: 100% 50%;
    }
    75% {
      background-position: 50% 0%;
    }
  }

  /* DESKTOP: Inline CAP Selection Styles */
  .cap-card-desktop {
    display: flex;
    flex-direction: column;
    gap: clamp(8px, 2cqh, 12px);
    padding: clamp(10px, 2cqh, 14px) clamp(8px, 1.5cqw, 12px);
    height: 100%;
  }

  .cap-header {
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    text-align: center;
    color: rgba(255, 255, 255, 0.9);
    opacity: 0.85;
  }

  /* DEFAULT (narrow card, 2/3 width): 2×2 grid layout */
  .cap-components-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: clamp(6px, 1.5cqi, 10px);
    height: 100%;
  }

  .cap-component-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: clamp(2px, 0.5cqi, 4px);
    padding: clamp(8px, 2cqi, 14px);
    min-width: 0; /* Allow flex shrinking */

    /* Solid background for better readability - no glass morphism */
    background: rgba(0, 0, 0, 0.3);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 12px;
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  /* WIDE CARD (full width, alone): Single horizontal row */
  @container cap-card (min-width: 500px) {
    .cap-components-grid {
      display: flex;
      flex-direction: row;
      gap: clamp(8px, 2cqi, 14px);
    }
  }

  .cap-component-btn:hover {
    background: rgba(0, 0, 0, 0.4);
    border-color: rgba(255, 255, 255, 0.5);
    transform: translateY(-2px);
  }

  .cap-component-btn.active {
    background: rgba(255, 255, 255, 0.2);
    border-color: white;
    border-width: 3px;
    box-shadow: 0 0 12px rgba(255, 255, 255, 0.3);
  }

  .cap-icon {
    font-size: clamp(20px, 8cqi, 48px);
    line-height: 1;
  }

  .cap-label {
    font-size: clamp(10px, 4cqi, 18px);
    font-weight: 600;
    /* No text-transform - keep natural casing */
    letter-spacing: 0.3px;
    line-height: 1.2;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    text-align: center;
  }

  /* Respect user motion preferences */
  @media (prefers-reduced-motion: reduce) {
    .cap-card-wrapper :global(.base-card) {
      animation: cardEnter 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) backwards !important;
      animation-delay: calc(var(--card-index) * 50ms) !important;
      background-position: 0% 50% !important;
    }
  }
</style>
