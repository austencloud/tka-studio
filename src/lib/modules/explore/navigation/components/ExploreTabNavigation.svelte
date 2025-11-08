<!--
ExploreTabNavigation.svelte

Tab-based navigation for the Explore module.
Allows switching between Sequences, Users, Collections, and Search.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { ExploreTabType, ExploreTab } from "../types/explore-tab-types";

  const { currentTab = "sequences", onTabChange = () => {} } = $props<{
    currentTab?: ExploreTabType;
    onTabChange?: (tab: ExploreTabType) => void;
  }>();

  let hapticService: IHapticFeedbackService;

  const tabs: ExploreTab[] = [
    { id: "sequences", label: "Sequences", icon: "fa-list" },
    { id: "users", label: "Users", icon: "fa-users" },
    { id: "collections", label: "Collections", icon: "fa-folder" },
    { id: "search", label: "Search", icon: "fa-search" },
  ];

  function handleTabClick(tabId: ExploreTabType) {
    hapticService?.trigger("selection");
    onTabChange(tabId);
  }

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });
</script>

<nav class="explore-tab-navigation" aria-label="Explore navigation">
  <div class="tabs-container">
    {#each tabs as tab}
      <button
        class="tab-button"
        class:active={currentTab === tab.id}
        class:disabled={tab.disabled}
        onclick={() => handleTabClick(tab.id)}
        disabled={tab.disabled}
        aria-label={tab.label}
        aria-current={currentTab === tab.id ? "page" : undefined}
      >
        <i class="fas {tab.icon}"></i>
        <span class="tab-label">{tab.label}</span>
      </button>
    {/each}
  </div>
</nav>

<style>
  .explore-tab-navigation {
    width: 100%;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    overflow-x: auto;
    overflow-y: hidden;
    scrollbar-width: none; /* Firefox */
    -ms-overflow-style: none; /* IE/Edge */
  }

  .explore-tab-navigation::-webkit-scrollbar {
    display: none; /* Chrome/Safari */
  }

  .tabs-container {
    display: flex;
    gap: 4px;
    padding: 8px 12px;
    min-width: min-content;
  }

  .tab-button {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: rgba(255, 255, 255, 0.7);
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
    min-width: fit-content;
  }

  .tab-button:hover:not(.disabled) {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.9);
  }

  .tab-button.active {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
    color: white;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  }

  .tab-button.disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .tab-button i {
    font-size: 16px;
  }

  /* Mobile optimization - hide labels on very small screens */
  @media (max-width: 380px) {
    .tab-label {
      display: none;
    }

    .tab-button {
      padding: 10px 12px;
    }
  }

  /* Tablet and desktop - more spacing */
  @media (min-width: 768px) {
    .tabs-container {
      gap: 8px;
      padding: 12px 16px;
    }

    .tab-button {
      padding: 12px 20px;
      font-size: 15px;
    }
  }
</style>
