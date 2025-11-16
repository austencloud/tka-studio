<!--
  SettingsSheet.svelte - Modern slide-up settings panel

  Replaces the full-screen settings dialog with a modern bottom sheet.
  Maintains all existing settings logic and tab navigation.
-->
<script lang="ts">
  import { resolve, TYPES, type IHapticFeedbackService, Drawer } from "$shared";
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
  import VisibilityTab from "./tabs/VisibilityTab.svelte";
  import {
    loadActiveTab,
    validateActiveTab as validateTab,
    saveActiveTab,
  } from "../utils/tab-persistence.svelte";

  // Valid tab IDs for validation
  const VALID_TAB_IDS = ["PropType", "Background", "Visibility", "Accessibility"];

  // Props
  let { isOpen = false } = $props<{ isOpen?: boolean }>();

  // Service resolution
  let hapticService: IHapticFeedbackService | null = null;

  // Create a local editable copy of settings
  let settings = $state({ ...getSettings() });

  // Initialize activeTab from localStorage or default to "PropType"
  let activeTab = $state(loadActiveTab(VALID_TAB_IDS, "PropType"));

  // Track if a save is in progress (for visual feedback)
  let isSaving = $state(false);

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
      id: "Visibility",
      label: "Visibility",
      icon: '<i class="fas fa-eye"></i>',
    },
    {
      id: "Accessibility",
      label: "Miscellaneous",
      icon: '<i class="fas fa-cog"></i>',
    },
  ];

  // Handle tab switching
  function switchTab(tabId: string) {
    hapticService?.trigger("selection");
    activeTab = tabId;
    saveActiveTab(tabId);
  }

  // Adapter for modern prop-based updates with instant save
  async function handlePropUpdate(event: { key: string; value: unknown }) {
    console.log("🔧 SettingsSheet handlePropUpdate called:", event);
    settings[event.key as keyof typeof settings] = event.value as never;

    // Instant save - apply changes immediately
    isSaving = true;
    const settingsToApply = $state.snapshot(settings);
    console.log(
      "💾 Auto-saving settings:",
      JSON.stringify(settingsToApply, null, 2)
    );

    await updateSettings(settingsToApply);

    // Brief delay for visual feedback
    setTimeout(() => {
      isSaving = false;
    }, 300);
  }

  // Handle close (no unsaved changes warning needed with instant save)
  function handleClose() {
    hapticService?.trigger("selection");
    console.log("✅ Settings closed (all changes auto-saved)");
    hideSettingsDialog();

    // Close via route if route-based
    import("../../navigation/utils/sheet-router").then(({ closeSheet }) => {
      closeSheet();
    });
  }
</script>

<Drawer
  {isOpen}
  labelledBy="settings-sheet-title"
  onclose={handleClose}
  class="settings-sheet"
  backdropClass="settings-sheet__backdrop"
  showHandle={true}
  closeOnBackdrop={true}
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
        {:else if activeTab === "Visibility"}
          <VisibilityTab
            currentSettings={settings}
            onSettingUpdate={handlePropUpdate}
          />
        {:else if activeTab === "Accessibility"}
          <AccessibilityTab
            currentSettings={settings}
            onSettingUpdate={handlePropUpdate}
          />
        {/if}
      </main>
    </div>

    <!-- Footer with close button and auto-save indicator -->
    <footer class="settings-sheet__footer">
      <div class="save-status">
        {#if isSaving}
          <span class="save-indicator saving">
            <i class="fas fa-sync fa-spin"></i>
            Saving...
          </span>
        {:else}
          <span class="save-indicator saved">
            <i class="fas fa-check"></i>
            All changes saved
          </span>
        {/if}
      </div>
      <button
        class="settings-sheet__button settings-sheet__button--close"
        onclick={handleClose}
        aria-label="Close settings"
      >
        <i class="fas fa-times"></i>
        Close
      </button>
    </footer>
  </div>
</Drawer>

<style>
  /* Make the bottom sheet fill full viewport height */
  :global(.settings-sheet) {
    /* Subtract 1px to prevent sub-pixel rounding overflow */
    --sheet-max-height: calc(100vh - 1px) !important;
    max-height: calc(100vh - 1px) !important;
    height: calc(100vh - 1px) !important;
    box-sizing: border-box !important;
  }

  /* Backdrop styling - MUST be behind content */
  :global(.settings-sheet__backdrop) {
    z-index: 1099 !important;
  }

  /* Sheet content - in front of backdrop */
  :global(.drawer-content.settings-sheet) {
    z-index: 1100 !important;
  }

  /* Disable overflow on drawer-inner to allow swipe-to-dismiss */
  :global(.drawer-content.settings-sheet .drawer-inner) {
    overflow-y: visible !important;
  }

  /* Container - Glass morphism design with high translucency */
  .settings-sheet__container {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    max-height: 100%;
    /* Highly translucent glass morphism background */
    background: linear-gradient(
      135deg,
      rgba(15, 20, 30, 0.45) 0%,
      rgba(10, 15, 25, 0.35) 100%
    );
    backdrop-filter: blur(32px) saturate(200%);
    -webkit-backdrop-filter: blur(32px) saturate(200%);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-bottom: none; /* Bottom sheet doesn't need bottom border */
    box-shadow:
      0 -8px 32px rgba(0, 0, 0, 0.5),
      0 -2px 8px rgba(0, 0, 0, 0.3),
      inset 0 1px 0 rgba(255, 255, 255, 0.12);
    /* NO overflow: hidden here - let child elements handle scrolling */
  }

  /* Header - Enhanced for glass morphism */
  .settings-sheet__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
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
    border-right: 1px solid rgba(255, 255, 255, 0.12);
    background: rgba(0, 0, 0, 0.08);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    overflow-y: visible; /* Changed from auto - no scrolling needed */
  }

  .settings-sheet__content {
    flex: 1;
    overflow-y: visible; /* Changed from auto - no scrolling needed */
    padding: 24px;
    background: rgba(0, 0, 0, 0.05);
    /* Smooth fade-slide animation when content changes */
    animation: contentFadeIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    /* Hide scrollbar completely - only show when actually scrolling */
    scrollbar-width: none;
    -ms-overflow-style: none;
  }

  /* Hide scrollbar on WebKit browsers */
  .settings-sheet__content::-webkit-scrollbar {
    display: none;
    width: 0;
  }

  /* Content entrance animation */
  @keyframes contentFadeIn {
    from {
      opacity: 0;
      transform: translateY(8px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* Footer - 2025 Standard: Auto-save indicator + Close button */
  .settings-sheet__footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 16px 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.12);
    background: rgba(0, 0, 0, 0.15);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    flex-shrink: 0;
  }

  /* Save status indicator */
  .save-status {
    flex: 1;
    display: flex;
    align-items: center;
  }

  .save-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.3s ease;
  }

  .save-indicator.saving {
    color: rgba(147, 197, 253, 0.9); /* Light blue */
  }

  .save-indicator.saved {
    color: rgba(134, 239, 172, 0.9); /* Light green */
  }

  .save-indicator i {
    font-size: 14px;
  }

  .settings-sheet__button {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 24px;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    border: none;
    min-height: 44px; /* Touch target */
  }

  /* Close button - primary action in instant-save pattern */
  .settings-sheet__button--close {
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.9);
    border: 1.5px solid rgba(255, 255, 255, 0.15);
  }

  .settings-sheet__button--close:hover {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.25);
    transform: scale(1.02);
  }

  .settings-sheet__button--close:active {
    transform: scale(0.98);
  }

  .settings-sheet__button:focus-visible {
    outline: 2px solid #6366f1; /* Indigo focus ring */
    outline-offset: 2px;
  }

  /* Icon spacing within buttons */
  .settings-sheet__button i {
    font-size: 14px;
    transition: transform 0.2s ease;
  }

  .settings-sheet__button:hover:not(:disabled) i {
    transform: scale(1.1); /* Subtle icon emphasis */
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
      height: 100%;
      max-height: 100%;
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
      height: 100%;
      max-height: 100%;
    }

    .settings-sheet__header {
      padding: 14px 16px;
    }

    .settings-sheet__header h2 {
      font-size: 18px;
    }

    .settings-sheet__content {
      padding: 8px 14px;
    }

    .settings-sheet__close {
      width: 44px; /* Maintain 44px minimum for accessibility */
      height: 44px;
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
    .settings-sheet__button,
    .save-indicator {
      transition: none;
    }

    .settings-sheet__close:hover,
    .settings-sheet__close:active,
    .settings-sheet__button--close:hover {
      transform: none;
    }
  }

  /* High contrast - Disable glass morphism for clarity */
  @media (prefers-contrast: high) {
    .settings-sheet__container {
      background: rgba(0, 0, 0, 0.98);
      backdrop-filter: none;
      -webkit-backdrop-filter: none;
      border: 2px solid white;
    }

    .settings-sheet__header,
    .settings-sheet__sidebar,
    .settings-sheet__footer {
      border-color: white;
      backdrop-filter: none;
      -webkit-backdrop-filter: none;
      background: rgba(0, 0, 0, 0.5);
    }
  }
</style>
