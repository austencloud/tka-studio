<!--
ToggleOption.svelte - Individual toggle option display component
Presentational component for a single toggle option with icon and label
-->
<script lang="ts">
  import { FontAwesomeIcon } from "$shared";

  let {
    label,
    icon,
    isActive,
    isLandscapeMobile
  } = $props<{
    label: string;
    icon?: string;
    isActive: boolean;
    isLandscapeMobile: boolean;
  }>();

  // Helper function to detect if icon is a Font Awesome icon name
  function isFontAwesomeIcon(iconStr: string | undefined): boolean {
    if (!iconStr) return false;
    // Font Awesome icon names are lowercase with hyphens only
    return /^[a-z-]+$/.test(iconStr);
  }
</script>

<div
  class="toggle-option"
  class:active={isActive}
  class:inactive={!isActive}
  class:landscape-mobile={isLandscapeMobile}
  role="presentation"
  title={label}
  aria-label={label}
>
  {#if icon && !isLandscapeMobile}
    <span class="option-icon">
      {#if isFontAwesomeIcon(icon)}
        <FontAwesomeIcon icon={icon} size="1em" />
      {:else}
        {icon}
      {/if}
    </span>
  {/if}
  <span class="option-label">{label}</span>
</div>

<style>
  /* ============================================
     BASE OPTION STYLES
     ============================================ */
  .toggle-option {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    flex: 1;
    min-height: 0;

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

  /* ============================================
     STATE STYLES
     ============================================ */
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

  /* ============================================
     ICON & LABEL STYLES
     ============================================ */
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

  /* ============================================
     RESPONSIVE: DESKTOP OPTIMIZATION
     ============================================ */
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

  /* ============================================
     RESPONSIVE: LANDSCAPE MOBILE COMPACT MODE
     ============================================ */
  /* When in landscape mobile (very constrained height), hide decorative elements */
  .toggle-option.landscape-mobile {
    /* Minimal padding to maximize space for text */
    padding: clamp(2px, 0.5vw, 4px);
  }

  .toggle-option.landscape-mobile .option-label {
    /* Keep text labels visible - these are what users need to see */
    font-size: clamp(10px, 1.5vw, 14px);
  }

  /* ============================================
     RESPONSIVE: SMALL SCREENS
     ============================================ */
  /* Ensure text is readable on very small screens */
  @media (max-width: 320px) {
    .option-label {
      font-size: 10px;
    }
  }
</style>
