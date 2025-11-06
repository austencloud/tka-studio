<!--
ToggleCard.svelte - Card for binary toggle options with vertical layout
Shows BOTH options stacked vertically, with clear active/inactive states
Perfect for narrow screens and provides immediate visual affordance
Hides header when card height is below 65px for space optimization
-->
<script lang="ts">
  import { onMount } from "svelte";
  import { createToggleCardState } from "../../state/toggle-card-state.svelte";
  import CardHeader from "./shared/CardHeader.svelte";
  import ToggleOption from "./ToggleOption.svelte";

  let {
    title,
    option1,
    option2,
    activeOption,
    onToggle,
    color = "#3b82f6",
    shadowColor = "0deg 0% 0%",
    gridColumnSpan = 2,
    cardIndex = 0,
    headerFontSize = "9px",
  } = $props<{
    title: string;
    icon?: string;
    option1: { value: any; label: string; icon?: string };
    option2: { value: any; label: string; icon?: string };
    activeOption: any;
    onToggle: (newValue: any) => void;
    color?: string;
    shadowColor?: string;
    gridColumnSpan?: number;
    cardIndex?: number;
    headerFontSize?: string;
  }>();

  // Create state using factory function
  // Use getter for activeOption to ensure reactivity
  const state = createToggleCardState({
    option1,
    option2,
    getActiveOption: () => activeOption,
    onToggle,
  });

  // Simple derived state stays in component
  const isOption1Active = $derived(activeOption === option1.value);
  const isOption2Active = $derived(activeOption === option2.value);

  onMount(() => {
    let cleanup: (() => void) | null = null;

    state.initialize().then((cleanupFn) => {
      cleanup = cleanupFn;
    });

    return () => {
      cleanup?.();
    };
  });
</script>

<button
  bind:this={state.cardElement}
  class="toggle-card"
  class:landscape-mobile={state.isLandscapeMobile}
  style="--card-color: {color}; --shadow-color: {shadowColor}; --card-index: {cardIndex}; --header-font-size: {headerFontSize}; grid-column: span {gridColumnSpan};"
  onclick={state.handleCardClick}
  onkeydown={state.handleKeydown}
  aria-label={`${title}: ${activeOption === option1.value ? option1.label : option2.label}. Click to toggle.`}
>
  <div class="card-header-wrapper">
    <CardHeader {title} {headerFontSize} />
  </div>

  <!-- Toggle Options Container -->
  <div class="toggle-options">
    <ToggleOption
      label={option1.label}
      icon={option1.icon}
      isActive={isOption1Active}
      isLandscapeMobile={state.isLandscapeMobile}
      optionsAreSideBySide={state.optionsAreSideBySide}
    />
    <ToggleOption
      label={option2.label}
      icon={option2.icon}
      isActive={isOption2Active}
      isLandscapeMobile={state.isLandscapeMobile}
      optionsAreSideBySide={state.optionsAreSideBySide}
    />
  </div>
</button>

<style>
  .toggle-card {
    /* Enable container queries to detect card aspect ratio */
    container-type: size;
    container-name: toggle-card;

    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;

    width: 100%;
    height: 100%;
    min-height: 0;
    min-width: 0;

    /* Container-aware padding - scales with card size */
    padding: clamp(4px, 1.5cqh, 8px) clamp(3px, 1cqw, 6px);

    /* Modern border-radius matching BaseCard */
    border-radius: 16px;
    background: var(--card-color);
    border: none;

    /* Layered shadows matching BaseCard + inner highlight for 3D depth */
    box-shadow:
      0 1px 2px hsl(var(--shadow-color) / 0.15),
      0 2px 4px hsl(var(--shadow-color) / 0.12),
      0 4px 8px hsl(var(--shadow-color) / 0.1),
      /* Inner highlight for 3D effect */ inset 0 1px 0 rgba(255, 255, 255, 0.2);

    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: visible; /* Allow hover effects to overflow and pop over neighbors */
    color: white;
    text-align: center;
    cursor: pointer;

    /* 🎬 ANIMATION - Clean fade in on load (400ms - 2025 standard) */
    animation: cardEnter 0.4s ease-out;
  }

  /* 🌟 GLOSSY SHEEN OVERLAY - Creates 3D glass effect */
  .toggle-card::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 60%; /* Cover top 60% */
    background: linear-gradient(
      180deg,
      rgba(255, 255, 255, 0.3) 0%,
      rgba(255, 255, 255, 0.15) 40%,
      rgba(255, 255, 255, 0.05) 70%,
      rgba(255, 255, 255, 0) 100%
    );
    border-radius: 16px 16px 0 0;
    pointer-events: none;
    z-index: 1; /* Above background, below content */
  }

  /* 🎬 Card entrance animation - clean fade in */
  @keyframes cardEnter {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  /* 🖱️ DESKTOP HOVER - Only on hover-capable devices (prevents mobile stuck hover) */
  @media (hover: hover) {
    .toggle-card:hover {
      transform: scale(1.02);
      filter: brightness(1.05);
      box-shadow:
        0 2px 4px hsl(var(--shadow-color) / 0.12),
        0 4px 8px hsl(var(--shadow-color) / 0.1),
        0 8px 16px hsl(var(--shadow-color) / 0.08),
        0 16px 24px hsl(var(--shadow-color) / 0.06),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
  }

  /* 🎯 ELASTIC PRESS - Universal click/tap feedback for ALL devices */
  .toggle-card:active {
    transform: scale(0.97);
    transition: transform 0.1s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .toggle-card:focus-within {
    outline-offset: 3px;
  }

  /* 🎯 HEADER WRAPPER - Hide header when card height < 85px */
  .card-header-wrapper {
    width: 100%;
    display: block;
  }

  /* Hide header when card is too short (< 85px) */
  @container toggle-card (height < 65px) {
    .card-header-wrapper {
      display: none;
    }

    /* Center toggle options when header is hidden */
    .toggle-options {
      justify-content: center;
    }
  }

  .toggle-options {
    display: flex;
    /* DEFAULT: Vertical (top/bottom) layout - looks nicer and more readable */
    /* Only switches to horizontal when container height is severely constrained */
    flex-direction: column;
    gap: clamp(3px, 1.5cqi, 6px);
    width: 100%;
    flex: 1;
  }

  /* 🎯 COMPACT MODE: Reduce padding in landscape mobile */
  .toggle-card.landscape-mobile {
    /* Reduce card padding to maximize internal space */
    padding: clamp(2px, 0.5cqh, 4px) clamp(2px, 0.5cqw, 4px);
  }

  .toggle-card.landscape-mobile .toggle-options {
    /* Keep vertical stacking for readability */
    flex-direction: column;
    gap: clamp(2px, 0.5cqi, 4px); /* Minimal gap */
  }

  /* 🎯 UNIFIED LAYOUT CONTROL: Pure CSS Container Query (2025 Gold Standard) */
  /* Switch to horizontal layout ONLY when card is significantly wider than tall */
  /* Aspect ratio > 2.5:1 ensures vertical layout for readability */
  /* No JavaScript needed - browser-native, performant, declarative */
  @container toggle-card (aspect-ratio > 2.5) {
    .toggle-options {
      flex-direction: row; /* Horizontal stacking when card is wide */
      justify-content: center;
      gap: clamp(6px, 2cqi, 12px);
    }
  }
</style>
