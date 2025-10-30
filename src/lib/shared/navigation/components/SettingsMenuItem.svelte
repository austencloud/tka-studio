<!--
  SettingsMenuItem - Settings menu item for navigation menus

  A menu-styled settings button with icon and description.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import { toggleSettingsDialog } from "../../application/state/app-state.svelte";

  let {
    onSettingsClick,
  } = $props<{
    onSettingsClick?: () => void;
  }>();

  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  function handleClick() {
    hapticService?.trigger("navigation");
    toggleSettingsDialog();
    onSettingsClick?.();
  }
</script>

<button class="settings-menu-item" onclick={handleClick}>
  <span class="item-icon">
    <i class="fas fa-cog"></i>
  </span>
  <div class="item-info">
    <span class="item-label">Settings</span>
    <span class="item-description">App preferences and configuration</span>
  </div>
</button>

<style>
  .settings-menu-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 14px 12px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    color: rgba(255, 255, 255, 0.9);
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: left;
    min-height: 56px;
    width: 100%;
  }

  .settings-menu-item:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.15);
    transform: translateX(4px);
  }

  .settings-menu-item:active {
    transform: translateX(4px) scale(0.98);
  }

  .item-icon {
    font-size: 24px;
    width: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .item-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-width: 0;
  }

  .item-label {
    font-size: 16px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
  }

  .item-description {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
    line-height: 1.3;
  }

  /* Accessibility */
  @media (prefers-reduced-motion: reduce) {
    .settings-menu-item {
      transition: none;
    }

    .settings-menu-item:hover,
    .settings-menu-item:active {
      transform: none;
    }
  }
</style>
