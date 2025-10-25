<!--
ToggleCard.svelte - Card for binary toggle options with vertical layout
Shows BOTH options stacked vertically, with clear active/inactive states
Perfect for narrow screens and provides immediate visual affordance
-->
<script lang="ts">
  import type { IDeviceDetector, IHapticFeedbackService, IRippleEffectService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
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
    headerFontSize = "9px"
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

  let hapticService: IHapticFeedbackService;
  let rippleService: IRippleEffectService;
  let deviceDetector: IDeviceDetector;
  let isLandscapeMobile = $state(false);
  let cardElement: HTMLButtonElement | null = $state(null);

  onMount(async () => {
    // Resolve services from DI container
    hapticService = await resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
    rippleService = await resolve<IRippleEffectService>(TYPES.IRippleEffectService);
    deviceDetector = await resolve<IDeviceDetector>(TYPES.IDeviceDetector);

    // Set initial layout state
    isLandscapeMobile = deviceDetector.isLandscapeMobile();

    // Subscribe to device capability changes (ViewportService handles resize/orientation internally)
    const cleanupDeviceListener = deviceDetector.onCapabilitiesChanged(() => {
      isLandscapeMobile = deviceDetector.isLandscapeMobile();
    });

    // 🌊 Attach ripple effect to card
    const cleanupRipple = cardElement
      ? rippleService.attachRipple(cardElement, {
          color: 'rgba(255, 255, 255, 0.4)',
          duration: 600,
          opacity: 0.5
        })
      : () => {};

    // Consolidated cleanup
    return () => {
      cleanupDeviceListener();
      cleanupRipple();
    };
  });

  function handleToggle(value: any) {
    if (value !== activeOption) {
      hapticService?.trigger("selection");
      onToggle(value);
    }
  }

  function handleCardClick() {
    // Toggle to the inactive option when clicking anywhere on card
    hapticService?.trigger("selection");
    const newValue = activeOption === option1.value ? option2.value : option1.value;
    onToggle(newValue);
  }

  function handleKeydown(event: KeyboardEvent, value?: any) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      if (value !== undefined) {
        handleToggle(value);
      } else {
        handleCardClick();
      }
    }
  }

  // Determine which option is active
  const isOption1Active = $derived(activeOption === option1.value);
  const isOption2Active = $derived(activeOption === option2.value);
</script>

<button
  bind:this={cardElement}
  class="toggle-card"
  class:landscape-mobile={isLandscapeMobile}
  style="--card-color: {color}; --shadow-color: {shadowColor}; --card-index: {cardIndex}; --header-font-size: {headerFontSize}; grid-column: span {gridColumnSpan};"
  onclick={handleCardClick}
  onkeydown={handleKeydown}
  aria-label={`${title}: ${activeOption === option1.value ? option1.label : option2.label}. Click to toggle.`}
>
  <!-- Card Header -->
  <div class="card-header">

    <div class="card-title">{title}</div>
  </div>

  <!-- Toggle Options Container -->
  <div class="toggle-options">
    <ToggleOption
      label={option1.label}
      icon={option1.icon}
      isActive={isOption1Active}
      {isLandscapeMobile}
    />
    <ToggleOption
      label={option2.label}
      icon={option2.icon}
      isActive={isOption2Active}
      {isLandscapeMobile}
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

    /* Responsive padding */
    padding: clamp(6px, .75vw, 12px) clamp(4px, 1vw, 8px);

    /* Modern border-radius matching BaseCard */
    border-radius: 16px;
    background: var(--card-color);
    border: none;

    /* Layered shadows matching BaseCard + inner highlight for 3D depth */
    box-shadow:
      0 1px 2px hsl(var(--shadow-color) / 0.15),
      0 2px 4px hsl(var(--shadow-color) / 0.12),
      0 4px 8px hsl(var(--shadow-color) / 0.10),
      /* Inner highlight for 3D effect */
      inset 0 1px 0 rgba(255, 255, 255, 0.2);

    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: hidden;
    color: white;
    text-align: center;
    cursor: pointer;

    /* 🎬 ANIMATION - Clean fade in on load (400ms - 2025 standard) */
    animation: cardEnter 0.4s ease-out;
  }

  /* 🌟 GLOSSY SHEEN OVERLAY - Creates 3D glass effect */
  .toggle-card::after {
    content: '';
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
        0 4px 8px hsl(var(--shadow-color) / 0.10),
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

  .card-header {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 4px;
    width: 100%;
    flex-shrink: 0;
    justify-content: center;
    padding: clamp(3px, 0.8cqh, 6px) clamp(6px, 1.5cqw, 10px); /* Match StepperCard padding */
  }


  .card-title {
    font-size: var(--header-font-size, 9px); /* Use centralized font size from parent */
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
    text-align: center;
    letter-spacing: 0.2px;
    text-transform: uppercase;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
  }

  .toggle-options {
    display: flex;
    /* DEFAULT: Vertical (top/bottom) layout - looks nicer and more readable */
    /* Only switches to horizontal when container height is severely constrained */
    flex-direction: column;
    gap: clamp(3px, 0.75vw, 6px);
    width: 100%;
    flex: 1;
  }

  .toggle-option {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    flex: 1;
    min-height: 0;

    /* Responsive padding */

    /* Softer border-radius for inner elements */
    border-radius: 10px;

    /* Base styling */
    background: transparent;
    border: 1.5px solid rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.6);

    font-size: clamp(11px, 1.5vw, 16px);
    font-weight: 600;

    /* Smooth transitions for state changes */
    transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);

    /* Prevent text selection */
    user-select: none;
    -webkit-user-select: none;
    pointer-events: none; /* Card handles all clicks */
  }

  /* Active state - solid, readable, no glass morphism */
  .toggle-option.active {
    background: rgba(255, 255, 255, 0.2);
    border-color: white;
    border-width: 3px;
    color: white;
    font-weight: 700;

    /* Clear shadow without inner glow */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);

    /* Scale slightly larger */
    transform: scale(1.02);
  }

  /* Inactive state - solid dark background for contrast */
  .toggle-option.inactive {
    background: rgba(0, 0, 0, 0.3);
    border-color: rgba(255, 255, 255, 0.25);
    color: rgba(255, 255, 255, 0.7);
  }

  /* Desktop optimization: Scale up toggle content for better readability */
  @media (min-width: 1280px) {
    .toggle-option {
      /* Bigger padding but not excessive */
      padding: clamp(18px, 3.5vh, 28px) clamp(14px, 2.5vw, 22px);

      /* Larger text */
      font-size: clamp(16px, 3vh, 24px);

      /* More prominent borders */
      border-width: 2.5px;
    }

    .option-icon {
      font-size: clamp(24px, 4.5vh, 36px);
    }

    .option-label {
      font-size: clamp(14px, 2.5vh, 20px);
      font-weight: 600;
      line-height: 1.2;
    }
  }

  .option-icon {
    /* Responsive icon sizing using container query units */
    /* Scales based on card width to prevent overflow */
    font-size: clamp(10px, 5cqw, 18px);
    line-height: 1;
    flex-shrink: 0;
  }

  .option-label {
    /* Allow text to wrap by default to prevent truncation */
    white-space: normal;
    overflow: visible;
    text-overflow: clip;
    text-align: center;
    word-break: break-word;
    line-height: 1.2;

    /* Responsive font sizing using container query units */
    /* Font scales based on card width to prevent overflow */
    /* Increased for better readability on mobile - 12px min, 18px max */
    font-size: clamp(12px, 5.5cqw, 20px);
  }

  /* 🎯 COMPACT MODE: Hide decorative elements ONLY in landscape mobile */
  /* When in landscape mobile (very constrained height), prioritize showing option text labels */
  /* Hide card title and emojis (least important) to prevent overflow */
  .toggle-card.landscape-mobile {
    /* Reduce card padding to maximize internal space */
    padding: clamp(2px, 0.5vw, 4px);
  }

  .toggle-card.landscape-mobile .card-title {
    /* Hide title - user knows what the card is from the options */
    display: none;
  }

  .toggle-card.landscape-mobile .option-icon {
    /* Hide emoji icons - decorative, not essential */
    display: none;
  }

  .toggle-card.landscape-mobile .option-label {
    /* Keep text labels visible - these are what users need to see */
    font-size: clamp(10px, 1.5vw, 14px);
  }

  .toggle-card.landscape-mobile .toggle-option {
    /* Minimal padding to maximize space for text */
    padding: clamp(2px, 0.5vw, 4px);
  }

  .toggle-card.landscape-mobile .toggle-options {
    /* Keep vertical stacking for readability */
    flex-direction: column;
    gap: clamp(2px, 0.5vw, 4px); /* Minimal gap */
  }

  /* 🎯 UNIFIED LAYOUT CONTROL: Pure CSS Container Query (2025 Gold Standard) */
  /* Switch to horizontal layout when the card itself is wide enough (200px+) */
  /* This ensures all cards switch together since they all hit the same width threshold */
  /* No JavaScript needed - browser-native, performant, declarative */
  @container toggle-card (min-width: 200px) {
    .toggle-options {
      flex-direction: row; /* Horizontal stacking when card is wide */
      justify-content: center;
      gap: clamp(6px, 1.5vw, 12px);
    }

    .toggle-option {
      flex: 1; /* Equal width for both options */
      min-width: 0; /* Allow flex shrinking */
      flex-direction: column; /* Stack icon above text when options are side-by-side */
      gap: clamp(2px, 0.5vw, 4px); /* Tighter gap between icon and text */
    }

    .option-label {
      white-space: normal; /* Allow text to wrap if needed */
      text-align: center; /* Center the text */
      word-break: break-word; /* Break long words if necessary */
      overflow: visible; /* Remove ellipsis truncation */
      text-overflow: clip; /* Don't add ellipsis */
    }
  }

  /* Ensure text is readable on very small screens */
  @media (max-width: 320px) {
    .option-label {
      font-size: 10px;
    }
  }
</style>
