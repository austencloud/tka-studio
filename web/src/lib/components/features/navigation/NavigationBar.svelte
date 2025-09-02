<!-- Unified Navigation Bar -->
<script lang="ts">
  import { showSettingsDialog } from "$state";
  import { foldTransition } from "$utils";

  type TabID = string;
  interface TabDef {
    id: TabID;
    label: string;
    icon: string;
    isMain?: boolean;
  }
  interface Props {
    tabs?: readonly TabDef[];
    activeTab?: TabID;
    onTabSelect?: (tabId: TabID) => void;
    onBackgroundChange?: (background: string) => void;
  }

  let {
    tabs = [],
    activeTab = "",
    onTabSelect,
    onBackgroundChange,
  }: Props = $props();

  // Separate main and developer tabs for display
  const mainTabs = $derived(() => tabs.filter((tab) => tab.isMain !== false));
  const devTabs = $derived(() => tabs.filter((tab) => tab.isMain === false));
  const showDeveloperSection = $derived(() => devTabs().length > 0);

  // Handle logo click - go to About tab
  async function handleLogoClick() {
    // Always use SPA navigation when user is already in the app
    onTabSelect?.("about");
  }

  // Handle tab click - always use SPA navigation
  function handleTabClick(tab: TabDef) {
    try {
      // Normal SPA behavior: just switch tabs
      onTabSelect?.(tab.id);
    } catch (error) {
      console.error("Failed to select tab:", error);
    }
  }
</script>

<!-- App Navigation -->
<nav
  class="app-navigation-bar glass-surface"
  in:foldTransition={{ direction: "fold-in", duration: 300 }}
>
  <!-- Clickable Logo/Brand - Go to About -->
  <div
    class="nav-brand clickable"
    onclick={handleLogoClick}
    role="button"
    tabindex="0"
    onkeydown={(e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        handleLogoClick();
      }
    }}
    title="Go to About page"
    aria-label="Go to About page"
  >
    <h1>TKA</h1>
    <span class="version">v2.0</span>
    <span class="return-hint">← About</span>
  </div>

  <!-- App Tab Navigation -->
  <div class="nav-tabs">
    <!-- Main tabs -->
    {#each mainTabs() as tab}
      <button
        class="nav-tab"
        class:active={activeTab === tab.id}
        onclick={() => handleTabClick(tab)}
        aria-pressed={activeTab === tab.id}
      >
        <span class="tab-icon">{tab.icon}</span>
        <span class="tab-label">{tab.label}</span>
      </button>
    {/each}

    <!-- Developer tabs separator and tabs -->
    {#if showDeveloperSection()}
      <div class="tab-separator"></div>
      {#each devTabs() as tab}
        <button
          class="nav-tab developer-tab"
          class:active={activeTab === tab.id}
          onclick={() => handleTabClick(tab)}
          aria-pressed={activeTab === tab.id}
          title="Developer Tool: {tab.label}"
        >
          <span class="tab-icon">{tab.icon}</span>
          <span class="tab-label">{tab.label}</span>
        </button>
      {/each}
    {/if}
  </div>

  <!-- App Actions -->
  <div class="nav-actions">
    <button
      class="nav-action"
      onclick={showSettingsDialog}
      title="Settings (Ctrl+,)"
      aria-label="Open Settings"
    >
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
        <path
          d="M12 15a3 3 0 100-6 3 3 0 000 6z"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
        <path
          d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </button>
  </div>
</nav>

<style>
  .app-navigation-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-md) var(--spacing-lg);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: var(--glass-backdrop-strong);
    background: rgba(255, 255, 255, 0.05);
    position: relative;
    z-index: 100;
  }

  .nav-brand {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    transition: all 0.3s ease;
    padding: var(--spacing-sm);
    border-radius: var(--border-radius);
    position: relative;
  }

  .nav-brand.clickable {
    cursor: pointer;
    user-select: none;
  }

  .nav-brand.clickable:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .nav-brand.clickable:hover .return-hint {
    opacity: 1;
    transform: translateX(0);
  }

  .nav-brand.clickable:focus-visible {
    outline: 2px solid #667eea;
    outline-offset: 2px;
  }

  .nav-brand h1 {
    font-size: var(--font-size-xl);
    font-weight: 700;
    background: var(--gradient-primary);
    background-clip: text;
    -webkit-background-clip: text;
    color: transparent;
    margin: 0;
  }

  .version {
    font-size: var(--font-size-xs);
    color: var(--muted-foreground);
    background: rgba(255, 255, 255, 0.1);
    padding: 2px 6px;
    border-radius: 4px;
  }

  .return-hint {
    position: absolute;
    top: 100%;
    left: 0;
    font-size: var(--font-size-xs);
    color: rgba(102, 126, 234, 0.8);
    opacity: 0;
    transform: translateX(-10px);
    transition: all 0.2s ease;
    white-space: nowrap;
    margin-top: 4px;
    background: rgba(0, 0, 0, 0.8);
    padding: 2px 6px;
    border-radius: 4px;
    backdrop-filter: blur(10px);
  }

  .nav-tabs {
    display: flex;
    gap: var(--spacing-sm);
  }

  .nav-tab {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-sm) var(--spacing-md);
    background: transparent;
    border: none;
    border-radius: 8px;
    color: var(--muted-foreground);
    cursor: pointer;
    transition: all var(--transition-fast);
    font-size: var(--font-size-sm);
    font-weight: 500;
  }

  .nav-tab:hover {
    background: rgba(255, 255, 255, 0.05);
    color: var(--foreground);
  }

  .nav-tab.active {
    background: rgba(99, 102, 241, 0.2);
    color: var(--primary-light);
    border: 1px solid rgba(99, 102, 241, 0.3);
  }

  .tab-icon {
    font-size: 16px;
  }

  .tab-label {
    font-weight: 500;
  }

  .nav-actions {
    display: flex;
    gap: var(--spacing-sm);
  }

  .nav-action {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background: transparent;
    border: none;
    border-radius: 8px;
    color: var(--muted-foreground);
    cursor: pointer;
    transition: all var(--transition-fast);
  }

  .nav-action:hover {
    background: rgba(255, 255, 255, 0.1);
    color: var(--foreground);
  }

  .nav-action:focus-visible {
    outline: 2px solid #667eea;
    outline-offset: 2px;
  }

  /* Tab separator for developer mode */
  .tab-separator {
    width: 1px;
    height: 24px;
    background: rgba(255, 255, 255, 0.2);
    margin: 0 var(--spacing-sm);
    align-self: center;
  }

  /* Developer tab styling */
  .developer-tab {
    border: 1px solid rgba(255, 165, 0, 0.3);
    background: rgba(255, 165, 0, 0.05);
  }

  .developer-tab:hover {
    background: rgba(255, 165, 0, 0.1);
    border-color: rgba(255, 165, 0, 0.5);
  }

  .developer-tab.active {
    background: rgba(255, 165, 0, 0.2);
    color: #ffa500;
    border-color: #ffa500;
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .app-navigation-bar {
      padding: var(--spacing-sm) var(--spacing-md);
    }

    .nav-tabs {
      gap: var(--spacing-xs);
    }

    .nav-tab {
      padding: var(--spacing-xs) var(--spacing-sm);
      font-size: var(--font-size-xs);
    }

    .tab-label {
      display: none;
    }

    .tab-icon {
      font-size: 18px;
    }

    .nav-brand h1 {
      font-size: var(--font-size-lg);
    }

    .return-hint {
      display: none;
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .nav-brand,
    .nav-tab,
    .nav-action,
    .return-hint {
      transition: none;
    }

    .nav-brand.clickable:hover {
      transform: none;
    }

    .nav-brand.clickable:hover .return-hint {
      transform: none;
    }
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    .app-navigation-bar {
      background: rgba(0, 0, 0, 0.9);
      border-bottom: 2px solid white;
    }

    .nav-tab {
      border: 1px solid rgba(255, 255, 255, 0.3);
    }

    .nav-tab.active {
      border-color: #667eea;
      background: rgba(102, 126, 234, 0.3);
    }
  }
</style>
