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

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  function handleTabClick(tabId: string) {
    // Trigger navigation haptic feedback for tab switching
    hapticService?.trigger("selection");
    onTabSelect(tabId);
  }
</script>

<aside class="settings-sidebar">
  <nav class="sidebar-nav">
    {#each tabs as tab}
      <button
        class="sidebar-item"
        class:active={activeTab === tab.id}
        onclick={() => handleTabClick(tab.id)}
        title={tab.label}
        aria-label={tab.label}
      >
        <span class="sidebar-icon">{@html tab.icon}</span>
        <span class="sidebar-label">{tab.label}</span>
      </button>
    {/each}
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
    gap: clamp(10px, 1vw, 16px);
    padding: clamp(14px, 1.5vw, 20px);
    background: transparent;
    border: 1.5px solid transparent;
    border-radius: 10px; /* More rounded for modern feel */
    color: rgba(255, 255, 255, 0.8);
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1); /* Smooth easing */
    text-align: left;
    font-size: clamp(15px, 1.4vw, 18px); /* Increased from 12-16px to 15-18px */
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
    font-size: 18px; /* Increased from 16px */
    width: 22px;
    text-align: center;
    transition: transform 0.2s ease;
  }

  .sidebar-item:hover .sidebar-icon {
    transform: scale(1.1); /* Icon emphasis on hover */
  }

  .sidebar-label {
    transition: opacity 0.2s ease;
  }

  /* Mobile responsive with intelligent layout switching */
  @media (max-width: 768px) {
    .settings-sidebar {
      width: 100%;
      min-height: auto;
      border-right: none;
      border-bottom: 1px solid rgba(255, 255, 255, 0.2);
      /* Prevent excessive height on mobile */
      max-height: clamp(80px, 12vh, 120px);
    }

    .sidebar-nav {
      flex-direction: row;
      overflow-x: auto;
      overflow-y: hidden;
      padding: clamp(12px, 2.5vw, 20px);
      gap: clamp(6px, 1.5vw, 12px);
      /* Enhanced mobile scrolling */
      scrollbar-width: none; /* Firefox */
      -ms-overflow-style: none; /* IE/Edge */
      scroll-behavior: smooth;
      -webkit-overflow-scrolling: touch;
    }

    .sidebar-nav::-webkit-scrollbar {
      display: none; /* Chrome/Safari */
    }

    .sidebar-item {
      flex-shrink: 0;
      min-width: clamp(100px, 22vw, 140px);
      max-width: clamp(140px, 30vw, 180px);
      padding: clamp(12px, 2.5vw, 16px) clamp(16px, 3.5vw, 24px);
      font-size: clamp(13px, 2.8vw, 15px);
      /* Enhanced touch targets */
      min-height: clamp(44px, 8vh, 56px);
      white-space: nowrap;
      /* Better visual feedback */
      border-radius: clamp(6px, 1.5vw, 10px);
    }

    .sidebar-icon {
      font-size: clamp(16px, 3.5vw, 20px);
      flex-shrink: 0;
    }

    .sidebar-label {
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }

  /* Narrow mobile screens and fold devices */
  @media (max-width: 480px) {
    .settings-sidebar {
      max-height: clamp(70px, 10vh, 100px);
    }

    .sidebar-nav {
      padding: clamp(10px, 2vw, 16px);
      gap: clamp(4px, 1vw, 8px);
    }

    .sidebar-item {
      min-width: clamp(80px, 20vw, 120px);
      max-width: clamp(120px, 28vw, 160px);
      padding: clamp(10px, 2vw, 14px) clamp(12px, 3vw, 20px);
      font-size: clamp(12px, 2.5vw, 14px);
      min-height: clamp(40px, 7vh, 48px);
    }

    .sidebar-icon {
      font-size: clamp(14px, 3vw, 16px);
    }
  }

  /* Ultra-narrow screens (Z Fold outer, iPhone SE, etc.) */
  @media (max-width: 390px) {
    .settings-sidebar {
      max-height: clamp(60px, 8vh, 80px);
    }

    .sidebar-nav {
      padding: clamp(8px, 1.5vw, 12px);
      gap: clamp(3px, 0.8vw, 6px);
    }

    .sidebar-item {
      min-width: clamp(70px, 18vw, 100px);
      max-width: clamp(100px, 25vw, 130px);
      padding: clamp(8px, 1.8vw, 12px) clamp(10px, 2.5vw, 16px);
      font-size: clamp(11px, 2.2vw, 13px);
      min-height: clamp(36px, 6vh, 44px);
      /* Consider icon-only on very narrow screens */
      gap: clamp(4px, 1vw, 8px);
    }

    .sidebar-icon {
      font-size: clamp(12px, 2.5vw, 14px);
    }

    /* Hide labels on extremely narrow screens if needed */
    .sidebar-label {
      font-size: clamp(10px, 2vw, 12px);
    }
  }

  /* Height-constrained scenarios (landscape, browser chrome) */
  @media (max-height: 600px) and (max-width: 768px) {
    .settings-sidebar {
      max-height: clamp(50px, 8vh, 70px);
    }

    .sidebar-item {
      min-height: clamp(32px, 5vh, 40px);
      padding: clamp(6px, 1vw, 10px) clamp(8px, 2vw, 14px);
    }

    .sidebar-icon {
      font-size: clamp(12px, 2.5vw, 15px);
    }

    .sidebar-label {
      font-size: clamp(10px, 2vw, 12px);
    }
  }
</style>
