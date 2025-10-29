<!--
  SettingsSheet.svelte - Modern slide-up settings panel

  Replaces the full-screen settings dialog with a modern bottom sheet.
  Maintains all existing settings logic and tab navigation.
-->
<script lang="ts">
  import { resolve, TYPES, type IHapticFeedbackService, BottomSheet } from "$shared";
  import { onMount } from "svelte";
  import {
    getSettings,
    hideSettingsDialog,
    updateSettings,
  } from "../../application/state/app-state.svelte";
  import SettingsSidebar from "./SettingsSidebar.svelte";
  import AccessibilityTab from "./tabs/AccessibilityTab.svelte";
  import BackgroundTab from "./tabs/background/BackgroundTab.svelte";
  import PropTypeTab from "./tabs/PropTypeTab.svelte";
  import {
    loadActiveTab,
    validateActiveTab as validateTab,
    saveActiveTab,
  } from "../utils/tab-persistence.svelte";

  // Valid tab IDs for validation
  const VALID_TAB_IDS = ["PropType", "Background", "Accessibility"];

  // Props
  let { isOpen = false } = $props<{ isOpen?: boolean }>();

  // Service resolution
  let hapticService: IHapticFeedbackService | null = null;

  // Create a local editable copy of settings
  let settings = $state({ ...getSettings() });

  // Initialize activeTab from localStorage or default to "PropType"
  let activeTab = $state(loadActiveTab(VALID_TAB_IDS, "PropType"));

  // Track if settings have been modified
  let hasUnsavedChanges = $state(false);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );

    // Validate and potentially update the active tab
    activeTab = validateTab(activeTab, tabs, "PropType");
  });

  // Check if settings are loaded
  const isSettingsLoaded = $derived(
    () =>
      settings &&
      typeof settings === "object" &&
      Object.keys(settings).length > 0
  );

  // Simplified tab configuration
  const tabs = [
    { id: "PropType", label: "Prop Type", icon: '<i class="fas fa-tag"></i>' },
    {
      id: "Background",
      label: "Background",
      icon: '<i class="fas fa-star"></i>',
    },
    {
      id: "Accessibility",
      label: "Experience",
      icon: '<i class="fas fa-universal-access"></i>',
    },
  ];

  // Handle tab switching
  function switchTab(tabId: string) {
    hapticService?.trigger("navigation");
    activeTab = tabId;
    saveActiveTab(tabId);
  }

  // Adapter for modern prop-based updates
  function handlePropUpdate(event: { key: string; value: unknown }) {
    console.log("🔧 SettingsSheet handlePropUpdate called:", event);
    settings[event.key as keyof typeof settings] = event.value as never;
    hasUnsavedChanges = true;
  }

  // Handle apply/save
  async function handleApply() {
    hapticService?.trigger("success");
    console.log("✅ Apply button clicked");

    const settingsToApply = $state.snapshot(settings);
    console.log("✅ Settings snapshot to be applied:", JSON.stringify(settingsToApply, null, 2));

    await updateSettings(settingsToApply);
    hasUnsavedChanges = false;
    hideSettingsDialog();
  }

  // Handle close/cancel with unsaved changes warning
  function handleClose() {
    if (hasUnsavedChanges) {
      const confirmClose = confirm(
        "You have unsaved changes. Are you sure you want to close without saving?"
      );
      if (!confirmClose) {
        return;
      }
    }

    hapticService?.trigger("selection");
    console.log("❌ Settings cancelled");
    hasUnsavedChanges = false;
    hideSettingsDialog();
  }
</script>

<BottomSheet
  {isOpen}
  labelledBy="settings-sheet-title"
  on:close={handleClose}
  class="settings-sheet"
  backdropClass="settings-sheet__backdrop"
>
  <div class="settings-sheet__container">
    <!-- Header -->
    <header class="settings-sheet__header">
      <h2 id="settings-sheet-title">Settings</h2>
      <button
        class="settings-sheet__close"
        onclick={handleClose}
        aria-label="Close settings"
      >
        <span aria-hidden="true">&times;</span>
      </button>
    </header>

    <!-- Main content area -->
    <div class="settings-sheet__body">
      <!-- Sidebar Navigation -->
      <aside class="settings-sheet__sidebar">
        <SettingsSidebar {tabs} {activeTab} onTabSelect={switchTab} />
      </aside>

      <!-- Content Area -->
      <main class="settings-sheet__content">
        {#if !isSettingsLoaded}
          <div class="loading-state">
            <p>Loading settings...</p>
          </div>
        {:else if activeTab === "PropType"}
          <PropTypeTab {settings} onUpdate={handlePropUpdate} />
        {:else if activeTab === "Background"}
          <BackgroundTab {settings} onUpdate={handlePropUpdate} />
        {:else if activeTab === "Accessibility"}
          <AccessibilityTab
            currentSettings={settings}
            onSettingUpdate={handlePropUpdate}
          />
        {/if}
      </main>
    </div>

    <!-- Footer with action buttons -->
    <footer class="settings-sheet__footer">
      <button
        class="settings-sheet__button settings-sheet__button--cancel"
        onclick={handleClose}
      >
        Cancel
      </button>
      <button
        class="settings-sheet__button settings-sheet__button--apply"
        onclick={handleApply}
        disabled={!hasUnsavedChanges}
      >
        Apply Changes
      </button>
    </footer>
  </div>
</BottomSheet>

<style>
  /* Backdrop styling */
  :global(.settings-sheet__backdrop) {
    z-index: 1100;
  }

  /* Container */
  .settings-sheet__container {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 90vh;
    max-height: none;
    background: linear-gradient(
      135deg,
      rgba(20, 25, 35, 0.98) 0%,
      rgba(15, 20, 30, 0.95) 100%
    );
    overflow: hidden;
  }

  /* Header */
  .settings-sheet__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .settings-sheet__header h2 {
    font-size: 24px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
  }

  .settings-sheet__close {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    border: none;
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.9);
    font-size: 28px;
    line-height: 1;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .settings-sheet__close:hover {
    background: rgba(255, 255, 255, 0.16);
    transform: scale(1.05);
  }

  .settings-sheet__close:active {
    transform: scale(0.95);
  }

  .settings-sheet__close:focus-visible {
    outline: 2px solid rgba(191, 219, 254, 0.7);
    outline-offset: 2px;
  }

  /* Body - sidebar + content */
  .settings-sheet__body {
    display: flex;
    flex: 1;
    overflow: hidden;
    min-height: 0;
  }

  .settings-sheet__sidebar {
    flex-shrink: 0;
    width: 200px;
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    overflow-y: auto;
  }

  .settings-sheet__content {
    flex: 1;
    overflow-y: auto;
    overflow-y: visible; /* No scrolling needed - everything fits on one screen */
    padding: 24px;
    background: rgba(255, 255, 255, 0.01);
  }

  /* Footer */
  .settings-sheet__footer {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 12px;
    padding: 16px 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.2);
    flex-shrink: 0;
  }

  .settings-sheet__button {
    padding: 12px 24px;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
  }

  .settings-sheet__button--cancel {
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.9);
  }

  .settings-sheet__button--cancel:hover {
    background: rgba(255, 255, 255, 0.12);
  }

  .settings-sheet__button--apply {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
  }

  .settings-sheet__button--apply:hover:not(:disabled) {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    transform: translateY(-1px);
  }

  .settings-sheet__button--apply:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .settings-sheet__button:focus-visible {
    outline: 2px solid rgba(191, 219, 254, 0.7);
    outline-offset: 2px;
  }

  /* Loading state */
  .loading-state {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 200px;
    color: rgba(255, 255, 255, 0.7);
  }

  /* Responsive design */
  @media (max-width: 768px) {
    .settings-sheet__container {
      height: 85vh;
    }

    .settings-sheet__body {
      flex-direction: column;
    }

    .settings-sheet__sidebar {
      width: 100%;
      border-right: none;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      overflow-y: visible;
    }

    .settings-sheet__content {
      padding: 20px 18px;
    }

    .settings-sheet__header {
      padding: 18px 20px;
    }

    .settings-sheet__header h2 {
      font-size: 20px;
    }
  }

  @media (max-width: 480px) {
    .settings-sheet__container {
      height: 90vh;
    }

    .settings-sheet__header {
      padding: 16px 18px;
    }

    .settings-sheet__header h2 {
      font-size: 18px;
    }

    .settings-sheet__content {
      padding: 18px 16px;
    }

    .settings-sheet__close {
      width: 40px;
      height: 40px;
      font-size: 24px;
    }

    .settings-sheet__button {
      padding: 10px 20px;
      font-size: 14px;
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .settings-sheet__close,
    .settings-sheet__button {
      transition: none;
    }

    .settings-sheet__close:hover,
    .settings-sheet__close:active,
    .settings-sheet__button--apply:hover {
      transform: none;
    }
  }

  /* High contrast */
  @media (prefers-contrast: high) {
    .settings-sheet__container {
      background: rgba(0, 0, 0, 0.98);
      border: 2px solid white;
    }

    .settings-sheet__header,
    .settings-sheet__sidebar,
    .settings-sheet__footer {
      border-color: white;
    }
  }
</style>
