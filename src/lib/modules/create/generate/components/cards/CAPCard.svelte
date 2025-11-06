<!--
CAPCard.svelte - Card for selecting CAP type
Always opens selector panel when clicked
-->
<script lang="ts">
  import { CAP_TYPE_LABELS } from "$create/generate/circular";
  import type { ICAPTypeService, IHapticFeedbackService } from "$shared";
  import { CAPType, resolve, TYPES } from "$shared";
  import { onMount, getContext } from "svelte";
  import type { PanelCoordinationState } from "$create/shared/state/panel-coordination-state.svelte";
  import BaseCard from "./BaseCard.svelte";

  let {
    currentCAPType,
    onCAPTypeChange,
    shadowColor = "30deg 75% 55%", // Orange shadow
    gridColumnSpan = 2,
    cardIndex = 0,
    headerFontSize = "9px",
  } = $props<{
    currentCAPType: CAPType;
    onCAPTypeChange: (capType: CAPType) => void;
    shadowColor?: string;
    gridColumnSpan?: number;
    cardIndex?: number;
    headerFontSize?: string;
  }>();

  let hapticService: IHapticFeedbackService;
  let capTypeService: ICAPTypeService = resolve<ICAPTypeService>(
    TYPES.ICAPTypeService
  );

  // Get panel coordination state from context (provided by CreateModule)
  const panelState = getContext<PanelCoordinationState>("panelState");

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Get current selected components using service
  const selectedComponents = $derived(
    capTypeService.parseComponents(currentCAPType)
  );

  // Open CAP panel via coordinator (renders at CreateModule level)
  function openExpanded() {
    hapticService?.trigger("selection");

    // Open the CAP panel via coordinator - this renders at CreateModule level
    // so the backdrop will properly cover the workspace
    panelState.openCAPPanel(
      currentCAPType,
      selectedComponents,
      onCAPTypeChange
    );
  }

  // Format CAP type display using user-friendly labels
  const capTypeDisplay = $derived(
    CAP_TYPE_LABELS[currentCAPType as CAPType] || currentCAPType
  );
</script>

<!-- CAP card with animated gradient wrapper -->
<div
  class="cap-card-wrapper"
  style="grid-column: span {gridColumnSpan}; --card-index: {cardIndex};"
>
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
</div>

<!-- CAP Selection Modal now renders at CreateModule level via CAPCoordinator -->

<style>
  /* ✨ Animated CAP Card - Flowing Gradient Wrapper */

  /* The wrapper has a beautiful animated gradient background */
  .cap-card-wrapper {
    /* Enable container queries to detect card width AND height */
    container-type: size;
    container-name: cap-card;

    position: relative;
    border-radius: 16px;
    overflow: visible; /* Allow hover effects to overflow and pop */

    /* Accessible rainbow gradient - deeper tones for better white text contrast */
    background: linear-gradient(
      135deg,
      #d32f2f 0%,
      /* Deep Red */ #e64a19 14%,
      /* Rich Orange */ #f57c00 28%,
      /* Amber Gold */ #388e3c 42%,
      /* Forest Green */ #00897b 57%,
      /* Teal */ #1976d2 71%,
      /* Deep Blue */ #7b1fa2 85%,
      /* Rich Purple */ #c2185b 100% /* Deep Magenta */
    );

    /* Make gradient larger so it can flow */
    background-size: 200% 200%;

    /* Animate the gradient position for flowing effect */
    animation:
      gradientFlow 8s ease-in-out infinite,
      cardEnter 0.4s ease-out;

    /* Subtle shadow - consistent with other cards */
    box-shadow:
      0 2px 4px rgba(0, 0, 0, 0.15),
      0 4px 8px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
  }

  /* Flowing gradient animation */
  @keyframes gradientFlow {
    0% {
      background-position: 0% 50%;
    }
    50% {
      background-position: 100% 50%;
    }
    100% {
      background-position: 0% 50%;
    }
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

  /* Ensure text is always readable with subtle shadow */
  .cap-card-wrapper :global(.base-card .card-header),
  .cap-card-wrapper :global(.base-card .card-value) {
    text-shadow:
      0 1px 2px rgba(0, 0, 0, 0.3),
      0 2px 4px rgba(0, 0, 0, 0.2);
  }

  /* Maintain hover effects - only on hover-capable devices */
  @media (hover: hover) {
    .cap-card-wrapper:hover {
      transform: scale(1.02);
      filter: brightness(1.05);
      box-shadow:
        0 2px 4px rgba(0, 0, 0, 0.12),
        0 4px 8px rgba(0, 0, 0, 0.1),
        0 8px 16px rgba(0, 0, 0, 0.08),
        0 16px 24px rgba(0, 0, 0, 0.06),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
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

  /* Respect user motion preferences */
  @media (prefers-reduced-motion: reduce) {
    .cap-card-wrapper :global(.base-card) {
      animation: cardEnter 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) backwards !important;
      animation-delay: calc(var(--card-index) * 50ms) !important;
      background-position: 0% 50% !important;
    }
  }
</style>
