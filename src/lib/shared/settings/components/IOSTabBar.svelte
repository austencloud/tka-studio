<!-- IOSTabBar.svelte - True iOS-native bottom tab bar -->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  interface Tab {
    id: string;
    label: string;
    icon: string;
  }

  let { tabs, activeTab, onTabSelect } = $props<{
    tabs: Tab[];
    activeTab: string;
    onTabSelect: (tabId: string) => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService | null = null;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  function handleTabClick(tabId: string) {
    // iOS uses light impact for tab selection
    hapticService?.trigger("impact");
    onTabSelect(tabId);
  }
</script>

<nav class="ios-tab-bar" role="tablist">
  {#each tabs as tab}
    <button
      class="ios-tab-item"
      class:active={activeTab === tab.id}
      onclick={() => handleTabClick(tab.id)}
      role="tab"
      aria-selected={activeTab === tab.id}
      aria-label={tab.label}
    >
      <span class="tab-icon" aria-hidden="true">{@html tab.icon}</span>
      <span class="tab-label">{tab.label}</span>
    </button>
  {/each}
</nav>

<style>
  /* iOS Tab Bar - HIG 2025 Specification */
  .ios-tab-bar {
    display: flex;
    height: 49px; /* iOS standard tab bar height */
    width: 100%;
    background: rgba(0, 0, 0, 0.7); /* iOS system material dark */
    backdrop-filter: blur(40px) saturate(180%);
    -webkit-backdrop-filter: blur(40px) saturate(180%);
    border-top: 0.33px solid rgba(255, 255, 255, 0.2); /* iOS hairline border */
    position: relative;
    /* iOS uses system fonts */
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui,
      sans-serif;
  }

  /* Tab Item */
  .ios-tab-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2px; /* Tight spacing between icon and label */
    padding: 0;
    border: none;
    background: transparent;
    cursor: pointer;
    position: relative;
    /* iOS spring animation - approximated with cubic-bezier */
    transition: transform 0.3s cubic-bezier(0.36, 0.66, 0.04, 1);
    -webkit-tap-highlight-color: transparent;
    min-width: 0;
  }

  /* Tab Icon */
  .tab-icon {
    font-size: 24px; /* iOS standard icon size (roughly 28pt) */
    line-height: 1;
    color: rgba(255, 255, 255, 0.55); /* Inactive tint */
    transition: color 0.2s ease, transform 0.3s cubic-bezier(0.36, 0.66, 0.04, 1);
    will-change: transform;
  }

  /* Tab Label */
  .tab-label {
    font-size: 10px; /* iOS tab bar label size */
    font-weight: 500;
    letter-spacing: -0.08px; /* iOS tight tracking */
    color: rgba(255, 255, 255, 0.55); /* Inactive tint */
    transition: color 0.2s ease;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
  }

  /* Active State - iOS tint color */
  .ios-tab-item.active .tab-icon,
  .ios-tab-item.active .tab-label {
    color: #007aff; /* iOS system blue tint */
  }

  /* Active state icon bounce (iOS spring effect) */
  .ios-tab-item.active .tab-icon {
    animation: ios-spring 0.4s cubic-bezier(0.36, 0.66, 0.04, 1);
  }

  @keyframes ios-spring {
    0% {
      transform: scale(1);
    }
    40% {
      transform: scale(1.15);
    }
    70% {
      transform: scale(0.95);
    }
    100% {
      transform: scale(1);
    }
  }

  /* Press Effect - iOS standard */
  .ios-tab-item:active {
    transform: scale(0.92);
  }

  .ios-tab-item:active .tab-icon {
    transform: scale(0.88);
  }

  /* Focus State for Keyboard Navigation */
  .ios-tab-item:focus-visible {
    outline: none;
  }

  .ios-tab-item:focus-visible::before {
    content: "";
    position: absolute;
    inset: 2px;
    border-radius: 8px;
    border: 2px solid #007aff;
    pointer-events: none;
  }

  /* High Contrast Mode */
  @media (prefers-contrast: high) {
    .ios-tab-bar {
      background: rgba(0, 0, 0, 0.95);
      backdrop-filter: none;
      -webkit-backdrop-filter: none;
      border-top: 1px solid white;
    }

    .tab-icon,
    .tab-label {
      color: rgba(255, 255, 255, 0.8);
    }

    .ios-tab-item.active .tab-icon,
    .ios-tab-item.active .tab-label {
      color: #0a84ff; /* Higher contrast blue */
    }
  }

  /* Reduced Motion */
  @media (prefers-reduced-motion: reduce) {
    .ios-tab-item,
    .tab-icon,
    .tab-label {
      transition: none;
    }

    .ios-tab-item.active .tab-icon {
      animation: none;
    }

    .ios-tab-item:active,
    .ios-tab-item:active .tab-icon {
      transform: none;
    }
  }

  /* Dark Mode - iOS automatically handles this via color-scheme */
  @media (prefers-color-scheme: light) {
    .ios-tab-bar {
      background: rgba(255, 255, 255, 0.7);
      border-top: 0.33px solid rgba(0, 0, 0, 0.2);
    }

    .tab-icon,
    .tab-label {
      color: rgba(0, 0, 0, 0.4);
    }

    .ios-tab-item.active .tab-icon,
    .ios-tab-item.active .tab-label {
      color: #007aff;
    }
  }
</style>
