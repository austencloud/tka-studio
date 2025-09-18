<!-- SettingsDialog.svelte - Simplified main settings dialog -->
<script lang="ts">
  import { quintOut } from "svelte/easing";
  import { fade, scale } from "svelte/transition";
  import {
    getSettings,
    hideSettingsDialog,
    updateSettings,
  } from "../../application/state/app-state.svelte";
  import SettingsSidebar from "./SettingsSidebar.svelte";
  import BackgroundTab from "./tabs/background/BackgroundTab.svelte";
  import PropTypeTab from "./tabs/PropTypeTab.svelte";

  // Current settings state with null safety
  let settings = $state(getSettings());
  let activeTab = $state("PropType");

  // Check if settings are loaded
  const isSettingsLoaded = $derived(
    () =>
      settings &&
      typeof settings === "object" &&
      Object.keys(settings).length > 0
  );



  // Simplified tab configuration
  const tabs = [
    { id: "PropType", label: "Prop Type", icon: "🏷️" },
    { id: "Background", label: "Background", icon: "🌌" },
  ];

  // Handle tab switching
  function switchTab(tabId: string) {
    activeTab = tabId;
  }



  // Adapter for modern prop-based updates
  function handlePropUpdate(event: { key: string; value: unknown }) {
    console.log("🔧 SettingsDialog handlePropUpdate called:", event);
    const newSettings = { ...settings, [event.key]: event.value };
    console.log("🔧 About to call updateSettings with:", newSettings);
    updateSettings(newSettings);
    settings = newSettings;
    console.log("🔧 Settings updated locally in dialog:", settings);
  }



  // Handle apply/save
  function handleApply() {
    console.log("✅ Settings applied:", settings);
    hideSettingsDialog();
  }

  // Handle close/cancel
  function handleClose() {
    hideSettingsDialog();
  }

  // Handle outside click to close
  function handleBackdropClick(event: MouseEvent) {
    if (event.target === event.currentTarget) {
      handleClose();
    }
  }

  // Handle keyboard events for backdrop
  function handleBackdropKeyDown(event: KeyboardEvent) {
    if (event.key === "Escape") {
      handleClose();
    }
  }
</script>

<!-- Settings Dialog Overlay -->
<div
  class="settings-overlay"
  onclick={handleBackdropClick}
  onkeydown={handleBackdropKeyDown}
  role="dialog"
  aria-modal="true"
  aria-labelledby="settings-title"
  tabindex="-1"
  in:fade={{ duration: 200, easing: quintOut }}
  out:fade={{ duration: 200, easing: quintOut }}
>
  <div
    class="settings-dialog"
    in:scale={{
      duration: 250,
      start: 0.95,
      opacity: 0,
      easing: quintOut
    }}
    out:scale={{
      duration: 200,
      start: 0.95,
      opacity: 0,
      easing: quintOut
    }}
  >
    <!-- Dialog Header -->
    <div
      class="dialog-header"
      in:fade={{ duration: 200, delay: 100, easing: quintOut }}
      out:fade={{ duration: 150, easing: quintOut }}
    >
      <h2 id="settings-title">Settings</h2>
      <button
        class="close-button"
        onclick={handleClose}
        aria-label="Close settings"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
          <path
            d="M18 6L6 18M6 6l12 12"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
          />
        </svg>
      </button>
    </div>

    <!-- Dialog Content -->
    <div
      class="dialog-content"
      in:fade={{ duration: 200, delay: 150, easing: quintOut }}
      out:fade={{ duration: 150, easing: quintOut }}
    >
      <!-- Sidebar Navigation -->
      <div
        in:fade={{ duration: 200, delay: 200, easing: quintOut }}
        out:fade={{ duration: 150, easing: quintOut }}
      >
        <SettingsSidebar {tabs} {activeTab} onTabSelect={switchTab} />
      </div>

      <!-- Content Area -->
      <main
        class="settings-content"
        in:fade={{ duration: 200, delay: 250, easing: quintOut }}
        out:fade={{ duration: 150, easing: quintOut }}
      >
        {#if !isSettingsLoaded}
          <div class="loading-state">
            <p>Loading settings...</p>
          </div>
        {:else if activeTab === "PropType"}
          <PropTypeTab {settings} onUpdate={handlePropUpdate} />
        {:else if activeTab === "Background"}
          <BackgroundTab {settings} onUpdate={handlePropUpdate} />
        {/if}
      </main>
    </div>

    <!-- Dialog Footer -->
    <div
      class="dialog-footer"
      in:fade={{ duration: 200, delay: 300, easing: quintOut }}
      out:fade={{ duration: 150, easing: quintOut }}
    >
      <button class="cancel-button" onclick={handleClose}>Cancel</button>
      <button class="apply-button" onclick={handleApply}>Apply Settings</button>
    </div>
  </div>
</div>

<style>
  .settings-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: var(--spacing-lg);

    /* Enhanced glassmorphism effect */
    background: linear-gradient(
      135deg,
      rgba(0, 0, 0, 0.7) 0%,
      rgba(0, 0, 0, 0.85) 100%
    );
  }

  .settings-dialog {
    width: min(
      90vw,
      1400px
    ); /* Increased from 800px to 1400px for much larger dialog */
    height: min(
      90vh,
      900px
    ); /* Increased to 90vh and 900px for much taller dialog */
    background: rgba(20, 25, 35, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 24px;
    backdrop-filter: blur(32px);
    -webkit-backdrop-filter: blur(32px);
    box-shadow:
      0 32px 64px rgba(0, 0, 0, 0.4),
      0 16px 32px rgba(0, 0, 0, 0.3),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    container-type: inline-size;

    /* Enhanced glassmorphism */
    background: linear-gradient(
      135deg,
      rgba(20, 25, 35, 0.98) 0%,
      rgba(15, 20, 30, 0.95) 100%
    );

    /* Subtle glow effect */
    position: relative;
  }

  .settings-dialog::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.1) 0%,
      rgba(255, 255, 255, 0.05) 50%,
      rgba(255, 255, 255, 0.1) 100%
    );
    border-radius: 26px;
    z-index: -1;
    opacity: 0.6;
  }

  .settings-dialog {
    /* CSS Custom Properties for responsive sizing */
    --dialog-width: min(90vw, 1400px);
    --dialog-height: min(90vh, 900px);
    --sidebar-width: clamp(150px, 15vw, 250px);
    --content-width: calc(var(--dialog-width) - var(--sidebar-width));
    --content-padding: clamp(16px, 2vw, 32px);
    --responsive-columns: 1;
    --max-content-width: none;
  }

  /* Dialog Header */
  .dialog-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: clamp(16px, 2vw, 32px);
    border-bottom: var(--glass-border);
    background: rgba(255, 255, 255, 0.03);
  }

  .dialog-header h2 {
    margin: 0;
    font-size: clamp(16px, 2vw, 24px);
    font-weight: 600;
    color: #ffffff;
  }

  .close-button {
    background: transparent;
    border: none;
    color: var(--text-secondary);
    cursor: pointer;
    padding: clamp(8px, 1vw, 12px);
    border-radius: var(--border-radius-sm);
    transition: all var(--transition-fast);
    min-width: clamp(32px, 4vw, 44px);
    min-height: clamp(32px, 4vw, 44px);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .close-button:hover {
    background: rgba(255, 255, 255, 0.08);
    color: white;
  }

  /* Dialog Content Layout */
  .dialog-content {
    flex: 1;
    display: flex;
    overflow: hidden;
    min-height: 0;
  }

  /* Content Area */
  .settings-content {
    flex: 1;
    overflow-y: auto;
    padding: var(--content-padding);
    background: rgba(255, 255, 255, 0.01);
    container-type: inline-size;
  }

  /* Container Queries for Responsive Layout */
  @container (min-width: 400px) {
    .settings-dialog {
      --responsive-columns: 1;
      --max-content-width: 100%;
    }
  }

  @container (min-width: 600px) {
    .settings-dialog {
      --responsive-columns: 1;
      --max-content-width: 90%;
    }
  }

  @container (min-width: 800px) {
    .settings-dialog {
      --responsive-columns: 2;
      --max-content-width: 85%;
    }
  }

  @container (min-width: 1000px) {
    .settings-dialog {
      --responsive-columns: 2;
      --max-content-width: 80%;
      --content-padding: clamp(24px, 3vw, 48px);
    }
  }

  @container (min-width: 1200px) {
    .settings-dialog {
      --responsive-columns: 3;
      --max-content-width: 75%;
      --content-padding: clamp(32px, 4vw, 64px);
    }
  }

  /* Dialog Footer */
  .dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: clamp(12px, 1.5vw, 24px);
    padding: clamp(16px, 2vw, 32px);
    border-top: var(--glass-border);
    background: rgba(255, 255, 255, 0.03);
    flex-wrap: wrap;
  }

  .cancel-button,
  .apply-button {
    padding: clamp(8px, 1vw, 12px) clamp(16px, 2vw, 32px);
    border-radius: 6px;
    font-size: clamp(12px, 1.2vw, 16px);
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition-fast);
    min-width: clamp(80px, 10vw, 120px);
  }

  .cancel-button {
    background: transparent;
    border: var(--glass-border);
    color: var(--text-secondary);
  }

  .cancel-button:hover {
    background: rgba(255, 255, 255, 0.06);
    color: white;
  }

  .apply-button {
    background: var(--primary-color);
    border: 1px solid var(--primary-color);
    color: white;
  }

  .apply-button:hover {
    background: var(--primary-light);
    border-color: var(--primary-light);
  }

  /* Responsive Design */
  @media (max-width: 1024px) {
    .settings-dialog {
      --sidebar-width: clamp(120px, 12vw, 180px);
    }
  }

  @media (max-width: 768px) {
    .settings-overlay {
      padding: clamp(8px, 2vw, 16px);
    }

    .settings-dialog {
      width: 100%;
      height: 100%;
      max-height: none;
      border-radius: 0;
      --sidebar-width: 100%;
      --content-padding: clamp(12px, 3vw, 24px);
    }

    .dialog-content {
      flex-direction: column;
    }
  }

  @media (max-width: 480px) {
    .settings-dialog {
      --content-padding: clamp(8px, 2vw, 16px);
    }
  }

  /* High DPI / Retina Display Support */
  @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
    .settings-dialog {
      border-width: 0.5px;
    }
  }
</style>
