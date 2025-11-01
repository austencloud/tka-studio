<!-- SettingsSidebar.svelte - Improved contrast navigation sidebar -->
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
  let hapticService: IHapticFeedbackService;

  // Runes for tracking sidebar dimensions
  let sidebarElement = $state<HTMLElement | null>(null);
  let sidebarWidth = $state(200);

  // Derived values based on parent width
  const isNarrow = $derived(sidebarWidth < 200);
  const isWide = $derived(sidebarWidth >= 250);

  // Smart navigation pattern selection based on tab count
  const shouldUseDropdown = $derived(tabs.length > 5);
  const shouldUseIconAboveText = $derived(tabs.length <= 5);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );

    // Track sidebar width changes with ResizeObserver
    if (sidebarElement) {
      const resizeObserver = new ResizeObserver((entries) => {
        for (const entry of entries) {
          sidebarWidth = entry.contentRect.width;
        }
      });
      resizeObserver.observe(sidebarElement);

      return () => resizeObserver.disconnect();
    }
  });

  function handleTabClick(tabId: string) {
    // Trigger navigation haptic feedback for tab switching
    hapticService?.trigger("selection");
    onTabSelect(tabId);
  }
</script>

<aside class="settings-sidebar" bind:this={sidebarElement}>
  <nav class="sidebar-nav" class:use-dropdown={shouldUseDropdown}>
    {#if shouldUseDropdown}
      <!-- Dropdown selector pattern (6+ tabs) - Future implementation -->
      <div class="tab-dropdown">
        <button class="dropdown-trigger" aria-label="Select tab">
          <span class="dropdown-icon"
            >{@html tabs.find((t: (typeof tabs)[0]) => t.id === activeTab)
              ?.icon || ""}</span
          >
          <span class="dropdown-label"
            >{tabs.find((t: (typeof tabs)[0]) => t.id === activeTab)?.label ||
              ""}</span
          >
          <i class="fas fa-chevron-down dropdown-arrow"></i>
        </button>
        <!-- Dropdown menu will be implemented when needed -->
      </div>
    {:else}
      <!-- Icon-above-text pattern (3-5 tabs) - Current implementation -->
      {#each tabs as tab}
        <button
          class="sidebar-item"
          class:active={activeTab === tab.id}
          class:narrow={isNarrow}
          class:wide={isWide}
          onclick={() => handleTabClick(tab.id)}
          title={tab.label}
          aria-label={tab.label}
        >
          <span class="sidebar-icon">{@html tab.icon}</span>
          <span class="sidebar-label">{tab.label}</span>
        </button>
      {/each}
    {/if}
  </nav>
</aside>

<style>
  .settings-sidebar {
    width: var(
      --sidebar-width,
      clamp(180px, 15vw, 250px)
    ); /* Increased min from 150px to 180px for better label readability */
    background: rgba(255, 255, 255, 0.08);
    border-right: 1px solid rgba(255, 255, 255, 0.2);
    overflow-y: auto;
    container-type: inline-size;
  }

  .sidebar-nav {
    padding: clamp(12px, 2vw, 24px);
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .sidebar-item {
    display: flex;
    align-items: center;
    gap: clamp(
      10px,
      5cqi,
      16px
    ); /* Use container inline size instead of viewport */
    padding: clamp(14px, 8cqi, 20px); /* Container-aware padding */
    background: transparent;
    border: 1.5px solid transparent;
    border-radius: 10px; /* More rounded for modern feel */
    color: rgba(255, 255, 255, 0.8);
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1); /* Smooth easing */
    text-align: left;
    font-size: clamp(
      16px,
      8cqi,
      20px
    ); /* INCREASED: Better readability, container-aware */
    font-weight: 500;
    position: relative;
    overflow: hidden;
  }

  /* Container query for sidebar responsiveness */
  @container (max-width: 160px) {
    /* Icon-only mode for very narrow sidebars */
    .sidebar-item {
      justify-content: center;
      gap: 0;
      padding: clamp(
        14px,
        2vw,
        20px
      ); /* Slightly larger padding for icon-only */
    }

    .sidebar-label {
      display: none;
    }

    .sidebar-icon {
      font-size: 20px; /* Larger icons when labels are hidden */
    }
  }

  @container (min-width: 161px) {
    /* Show labels when there's enough space */
    .sidebar-item {
      gap: clamp(8px, 1vw, 16px);
    }

    .sidebar-label {
      display: block;
    }
  }

  .sidebar-item:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    color: #ffffff;
    transform: scale(1.02); /* Subtle scale */
  }

  .sidebar-item:active {
    transform: scale(0.98); /* Press feedback */
  }

  .sidebar-item.active {
    background: rgba(99, 102, 241, 0.25); /* Indigo theme */
    color: #ffffff;
    border-color: rgba(99, 102, 241, 0.6);
    box-shadow: 0 0 12px rgba(99, 102, 241, 0.3); /* Subtle glow */
    font-weight: 600; /* Emphasize active tab */
  }

  .sidebar-item.active:hover {
    background: rgba(99, 102, 241, 0.3);
    box-shadow: 0 0 16px rgba(99, 102, 241, 0.4);
  }

  .sidebar-icon {
    font-size: 20px; /* INCREASED: More visible icons */
    width: 24px;
    text-align: center;
    transition: transform 0.2s ease;
    flex-shrink: 0; /* Prevent icon from shrinking */
  }

  .sidebar-item:hover .sidebar-icon {
    transform: scale(1.1); /* Icon emphasis on hover */
  }

  .sidebar-label {
    transition: opacity 0.2s ease;
  }

  /* Mobile responsive - Icon-above-text pattern (iOS/Android style) */
  @media (max-width: 768px) {
    .settings-sidebar {
      width: 100%;
      min-height: auto;
      border-right: none;
      border-bottom: 1px solid rgba(255, 255, 255, 0.2);
      max-height: 90px;
      position: relative;
    }

    .sidebar-nav {
      flex-direction: row;
      overflow: visible; /* No scrolling needed - all tabs fit */
      padding: 8px 8px;
      gap: 4px;
      /* Equal distribution of tabs */
      justify-content: space-between;
    }

    .sidebar-item {
      /* Icon-above-text layout */
      flex-direction: column; /* Stack icon above text */
      align-items: center;
      justify-content: center;
      flex: 1; /* Equal width for all tabs */
      gap: 4px; /* Tight spacing between icon and label */
      padding: 8px 6px;
      font-size: 13px; /* Smaller but readable */
      min-height: 62px; /* Taller for vertical layout */
      white-space: normal; /* Allow text wrapping if needed */
      text-align: center;
      border-radius: 8px;
    }

    .sidebar-icon {
      font-size: 22px; /* LARGER: Icons are the primary visual element */
      flex-shrink: 0;
      width: auto; /* Remove fixed width */
      margin: 0; /* Remove margin */
    }

    .sidebar-label {
      font-size: 12px; /* Compact but readable */
      line-height: 1.2;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100%; /* Prevent overflow */
    }
  }

  /* Narrow mobile screens - Maintain icon-above-text */
  @media (max-width: 480px) {
    .sidebar-nav {
      padding: 6px 6px;
      gap: 3px;
    }

    .sidebar-item {
      padding: 6px 4px;
      min-height: 58px;
      gap: 3px;
    }

    .sidebar-icon {
      font-size: 20px; /* Slightly smaller but still prominent */
    }

    .sidebar-label {
      font-size: 11px; /* Compact but readable */
    }
  }

  /* Ultra-narrow screens - Maintain icon-above-text with minimum sizes */
  @media (max-width: 390px) {
    .sidebar-nav {
      padding: 5px 4px;
      gap: 2px;
    }

    .sidebar-item {
      padding: 5px 3px;
      min-height: 56px;
      gap: 2px;
    }

    .sidebar-icon {
      font-size: 18px; /* Minimum practical icon size */
    }

    .sidebar-label {
      font-size: 10px; /* Minimum readable size */
    }
  }

  /* Height-constrained scenarios - Compact icon-above-text */
  @media (max-height: 600px) and (max-width: 768px) {
    .settings-sidebar {
      max-height: 60px;
    }

    .sidebar-nav {
      padding: 4px 6px;
    }

    .sidebar-item {
      min-height: 50px;
      padding: 4px 4px;
      gap: 2px;
    }

    .sidebar-icon {
      font-size: 18px;
    }

    .sidebar-label {
      font-size: 10px;
    }
  }

  /* Dropdown selector pattern (6+ tabs) - Activated automatically */
  .sidebar-nav.use-dropdown {
    padding: 12px 16px;
    justify-content: center;
  }

  .tab-dropdown {
    width: 100%;
    max-width: 400px;
  }

  .dropdown-trigger {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 18px;
    background: rgba(255, 255, 255, 0.08);
    border: 1.5px solid rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    color: rgba(255, 255, 255, 0.9);
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .dropdown-trigger:hover {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.3);
  }

  .dropdown-icon {
    font-size: 20px;
    flex-shrink: 0;
  }

  .dropdown-label {
    flex: 1;
    text-align: left;
  }

  .dropdown-arrow {
    font-size: 14px;
    transition: transform 0.2s ease;
    opacity: 0.7;
  }

  .dropdown-trigger:hover .dropdown-arrow {
    opacity: 1;
  }

  /* Mobile dropdown adjustments */
  @media (max-width: 768px) {
    .sidebar-nav.use-dropdown {
      padding: 10px 14px;
    }

    .dropdown-trigger {
      padding: 12px 16px;
      font-size: 15px;
    }

    .dropdown-icon {
      font-size: 18px;
    }
  }
</style>
