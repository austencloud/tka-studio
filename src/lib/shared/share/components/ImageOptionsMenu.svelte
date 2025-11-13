<!--
  ImageOptionsMenu.svelte

  Collapsible menu containing image appearance options.
  Wraps ShareOptionsForm in an expandable/collapsible interface to save space.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import ShareOptionsForm from "./ShareOptionsForm.svelte";
  import type { ShareOptions } from "../domain";

  let {
    options,
    onOptionsChange,
    isExpanded = $bindable(false),
  }: {
    options?: ShareOptions;
    onOptionsChange?: (newOptions: Partial<ShareOptions>) => void;
    isExpanded?: boolean;
  } = $props();

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Toggle expansion
  function toggleExpansion() {
    hapticService?.trigger("selection");
    isExpanded = !isExpanded;
  }
</script>

<div class="image-options-menu">
  <button
    type="button"
    class="menu-header"
    class:expanded={isExpanded}
    onclick={toggleExpansion}
    aria-expanded={isExpanded}
    aria-controls="image-options-content"
  >
    <div class="header-content">
      <i class="fas fa-sliders header-icon"></i>
      <span class="header-title">Image Options</span>
    </div>
    <i class="fas fa-chevron-{isExpanded ? 'up' : 'down'} chevron-icon"></i>
  </button>

  {#if isExpanded && options && onOptionsChange}
    <div
      id="image-options-content"
      class="menu-content"
      role="region"
      aria-label="Image options"
    >
      <ShareOptionsForm {options} {onOptionsChange} />
    </div>
  {/if}
</div>

<style>
  .image-options-menu {
    display: flex;
    flex-direction: column;
    gap: 0;
    border-radius: 12px;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.12);
  }

  .menu-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 14px 16px;
    background: rgba(255, 255, 255, 0.05);
    border: none;
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
    user-select: none;
    width: 100%;
    text-align: left;
  }

  .menu-header:hover {
    background: rgba(255, 255, 255, 0.08);
  }

  .menu-header:active {
    background: rgba(255, 255, 255, 0.1);
  }

  .menu-header.expanded {
    background: rgba(255, 255, 255, 0.07);
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
  }

  .menu-header:focus-visible {
    outline: 3px solid rgba(59, 130, 246, 0.4);
    outline-offset: -3px;
  }

  .header-content {
    display: flex;
    align-items: center;
    gap: 12px;
    flex: 1;
  }

  .header-icon {
    font-size: 18px;
    color: rgba(59, 130, 246, 0.9);
    flex-shrink: 0;
  }

  .header-title {
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 0.2px;
    color: rgba(255, 255, 255, 0.95);
  }

  .chevron-icon {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.6);
    transition: transform 0.2s ease;
    flex-shrink: 0;
  }

  .menu-header.expanded .chevron-icon {
    transform: rotate(180deg);
  }

  .menu-content {
    padding: 16px;
    animation: slideDown 0.2s ease-out;
  }

  @keyframes slideDown {
    from {
      opacity: 0;
      transform: translateY(-8px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .menu-header,
    .chevron-icon {
      transition: none;
    }

    .menu-content {
      animation: none;
    }

    .menu-header.expanded .chevron-icon {
      transform: none;
    }
  }
</style>
