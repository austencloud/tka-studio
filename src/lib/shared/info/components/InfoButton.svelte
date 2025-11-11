<script lang="ts">
  /**
   * Info Button Component
   *
   * Opens the full-screen info page modal.
   * Provides access to resources, community links, and support options.
   *
   * Can render in two variants:
   * - "button": Standalone circular button (default, for TopBar)
   * - "sidebar-icon": Inline icon for sidebar header
   */

  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";
  import { onMount } from "svelte";
  import { toggleInfo } from "../state/info-state.svelte";

  // Props
  let {
    onclick = () => {},
    variant = "button",
    showLabel = false
  }: {
    onclick?: () => void;
    variant?: "button" | "sidebar-icon";
    showLabel?: boolean;
  } = $props();

  // Services
  let hapticService: IHapticFeedbackService | null = $state(null);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  function handleClick() {
    // Trigger haptic feedback for info button
    hapticService?.trigger("selection");
    toggleInfo();
    onclick();
  }
</script>

{#if variant === "sidebar-icon"}
  <!-- Sidebar icon variant - non-interactive, parent button handles clicks -->
  <i
    class="fas fa-circle-info sidebar-info-icon"
    aria-hidden="true"
  ></i>
{:else}
  <!-- Standard button variant for TopBar -->
  <button
    class="info-button glass-surface"
    onclick={handleClick}
    title="Resources & Support"
    aria-label="Open resources and support page"
  >
    <i class="fas fa-circle-info icon-minimal"></i>
    {#if showLabel}
      <span class="info-label">Info</span>
    {/if}
  </button>
{/if}

<style>
  /* ============================================================================
     BUTTON VARIANT (TopBar)
     ============================================================================ */
  .info-button {
    /* Match existing button sizing - WCAG AAA minimum touch target */
    width: 44px;
    height: 44px;
    min-width: 44px;
    min-height: 44px;
    border-radius: 50%;
    border: 1px solid rgba(56, 189, 248, 0.3);
    background: linear-gradient(
      135deg,
      rgba(56, 189, 248, 0.15) 0%,
      rgba(6, 182, 212, 0.1) 100%
    );
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
  }

  .info-button:hover {
    background: linear-gradient(
      135deg,
      rgba(56, 189, 248, 0.25) 0%,
      rgba(6, 182, 212, 0.2) 100%
    );
    border-color: rgba(56, 189, 248, 0.5);
    transform: scale(1.05);
  }

  .info-button:active {
    transform: scale(0.95);
  }

  /* Icon styling - White to match other buttons */
  .icon-minimal {
    font-size: 20px;
    color: rgba(255, 255, 255, 0.9);
  }

  .info-label {
    margin-left: 8px;
    font-size: 14px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.9);
  }

  /* Accessibility */
  .info-button:focus-visible {
    outline: 2px solid rgba(99, 102, 241, 0.7);
    outline-offset: 2px;
  }

  /* ============================================================================
     SIDEBAR ICON VARIANT
     ============================================================================ */
  .sidebar-info-icon {
    /* Icon styling */
    font-size: 20px;
    color: rgba(56, 189, 248, 1);

    /* Button-like container */
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 10px;

    /* Non-interactive - parent button handles clicks */
    pointer-events: none;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;

    /* Background with gradient */
    background: linear-gradient(
      135deg,
      rgba(56, 189, 248, 0.15) 0%,
      rgba(6, 182, 212, 0.1) 100%
    );

    /* Border and glow */
    border: 1px solid rgba(56, 189, 248, 0.25);
    box-shadow: 0 0 12px rgba(56, 189, 248, 0.2);
  }

  /* Hover state is applied when parent button is hovered */
  :global(button:hover) .sidebar-info-icon {
    background: linear-gradient(
      135deg,
      rgba(56, 189, 248, 0.25) 0%,
      rgba(6, 182, 212, 0.18) 100%
    );
    border-color: rgba(56, 189, 248, 0.4);
    box-shadow: 0 0 20px rgba(56, 189, 248, 0.35);
    color: rgba(56, 189, 248, 1);
  }

  :global(button:active) .sidebar-info-icon {
    transform: scale(0.95);
  }

  /* ============================================================================
     REDUCED MOTION
     ============================================================================ */
  @media (prefers-reduced-motion: reduce) {
    .info-button,
    .sidebar-info-icon {
      transition: none;
    }

    .info-button:hover,
    .info-button:active {
      transform: none;
    }

    :global(button:hover) .sidebar-info-icon,
    :global(button:active) .sidebar-info-icon {
      transform: none;
    }
  }

  /* ============================================================================
     HIGH CONTRAST
     ============================================================================ */
  @media (prefers-contrast: high) {
    .info-button {
      background: rgba(255, 255, 255, 0.2);
      border: 2px solid white;
    }

    .icon-minimal {
      color: white;
      filter: none;
    }

    .sidebar-info-icon {
      background: rgba(255, 255, 255, 0.3);
      border: 2px solid rgba(56, 189, 248, 1);
      color: rgba(56, 189, 248, 1);
    }
  }
</style>
