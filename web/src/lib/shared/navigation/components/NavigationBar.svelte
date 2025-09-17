<!-- Enhanced Navigation Bar with Dropdown Support -->
<!-- Enhanced Navigation Bar with Dropdown Support -->
<script lang="ts">
  import { onMount } from "svelte";
  import type { IAnimationService } from "../../application/services/contracts";
  import { showSettingsDialog } from "../../application/state/app-state.svelte";
  import type { IDeviceDetector } from "../../device/services/contracts/IDeviceDetector";
  import type { DropdownState, ModeOption } from "../domain/types";
  import DesktopDropdown from "./DesktopDropdown.svelte";
  import MobileModal from "./MobileModal.svelte";

  type TabID = string;
  interface TabDef {
    id: TabID;
    label: string;
    icon: string;
    isMain?: boolean;
  }

  let {
    tabs = [],
    activeTab = null,
    onTabSelect,
    onBackgroundChange,
    // New props for dropdown functionality
    buildModes = [],
    currentBuildMode = "construct",
    onBuildModeChange,
    learnModes = [],
    currentLearnMode = "codex",
    onLearnModeChange,
  } = $props<{
    tabs?: readonly TabDef[];
    activeTab?: TabID | null;
    onTabSelect?: (tabId: TabID) => void;
    onBackgroundChange?: (background: string) => void;
    // Dropdown props
    buildModes?: ModeOption[];
    currentBuildMode?: string;
    onBuildModeChange?: (mode: string) => void;
    learnModes?: ModeOption[];
    currentLearnMode?: string;
    onLearnModeChange?: (mode: string) => void;
  }>();

  // Resolve services asynchronously to avoid container initialization errors
  let animationService: IAnimationService | null = $state(null);
  let deviceDetector: IDeviceDetector | null = $state(null);

  // Initialize services when container is ready
  onMount(async () => {
    try {
      const { resolveAsync, TYPES } = await import("../../inversify");
      animationService = await resolveAsync<IAnimationService>(TYPES.IAnimationService);
      deviceDetector = await resolveAsync<IDeviceDetector>(TYPES.IDeviceDetector);
    } catch (error) {
      console.error("NavigationBar: Failed to resolve services:", error);
    }
  });

  // Dropdown state
  let dropdownState = $state<DropdownState>({
    isOpen: false,
    tabId: null,
    showDiscoveryHint: false
  });

  // Device detection - handle null service gracefully
  const isMobile = $derived(() => deviceDetector?.isMobile() ?? false);

  // Create fold transition - handle null service gracefully
  const foldTransition = (node: Element, params: any) => {
    if (!animationService) {
      // Fallback transition if service not ready
      return {
        duration: 300,
        css: (t: number) => `opacity: ${t}`,
      };
    }
    return animationService.createFoldTransition({
      direction: "fold-in",
      duration: 300,
      ...params,
    });
  };

  // Dropdown functionality with hover delay
  let openTimeout: ReturnType<typeof setTimeout> | null = null;
  let closeTimeout: ReturnType<typeof setTimeout> | null = null;

  // Track timeout IDs to prevent race conditions
  let currentOpenTimeoutId = 0;
  let currentCloseTimeoutId = 0;

  function toggleDropdown(tabId: string) {
    if (dropdownState.isOpen && dropdownState.tabId === tabId) {
      closeDropdown();
    } else {
      openDropdown(tabId);
    }
  }

  function openDropdown(tabId: string) {
    const timestamp = Date.now();
    console.log(`🔓 [${timestamp}] NavigationBar: openDropdown(${tabId})`);

    // Clear ALL pending timeouts to prevent race conditions
    if (openTimeout) {
      console.log(`🚫 [${timestamp}] NavigationBar: Clearing openTimeout in openDropdown`);
      clearTimeout(openTimeout);
      openTimeout = null;
    }
    if (closeTimeout) {
      console.log(`🚫 [${timestamp}] NavigationBar: Clearing closeTimeout in openDropdown`);
      clearTimeout(closeTimeout);
      closeTimeout = null;
    }

    console.log(`📝 [${timestamp}] NavigationBar: Setting dropdown state - isOpen: true, tabId: ${tabId}`);
    dropdownState.isOpen = true;
    dropdownState.tabId = tabId;
    console.log(`✅ [${timestamp}] NavigationBar: Dropdown opened for ${tabId}`);
  }

  function closeDropdown() {
    const timestamp = Date.now();
    console.log(`🔒 [${timestamp}] NavigationBar: closeDropdown()`);
    console.log(`📝 [${timestamp}] NavigationBar: Setting dropdown state - isOpen: false, tabId: null`);
    dropdownState.isOpen = false;
    dropdownState.tabId = null;
    console.log(`✅ [${timestamp}] NavigationBar: Dropdown closed`);
  }

  function handleMouseEnter(tabId: string) {
    const timestamp = Date.now();
    console.log(`🖱️ [${timestamp}] NavigationBar: handleMouseEnter(${tabId})`);

    if (!hasDropdown(tabId)) {
      console.log(`❌ [${timestamp}] NavigationBar: ${tabId} has no dropdown, ignoring`);
      return;
    }

    console.log(`🔍 [${timestamp}] NavigationBar: Current dropdown state:`, {
      isOpen: dropdownState.isOpen,
      tabId: dropdownState.tabId,
      openTimeout: openTimeout !== null,
      closeTimeout: closeTimeout !== null
    });

    // Clear any existing timeouts
    if (openTimeout) {
      console.log(`🚫 [${timestamp}] NavigationBar: Clearing existing openTimeout`);
      clearTimeout(openTimeout);
      openTimeout = null;
    }
    if (closeTimeout) {
      console.log(`🚫 [${timestamp}] NavigationBar: Clearing existing closeTimeout`);
      clearTimeout(closeTimeout);
      closeTimeout = null;
    }

    // Increment timeout ID to invalidate any pending timeouts
    currentCloseTimeoutId++;

    // If dropdown is already open for a different tab, switch immediately
    if (dropdownState.isOpen && dropdownState.tabId !== tabId) {
      console.log(`🔄 [${timestamp}] NavigationBar: Switching dropdown from ${dropdownState.tabId} to ${tabId} immediately`);
      openDropdown(tabId);
      return;
    }

    // Set timeout to open dropdown with ID tracking
    const timeoutId = ++currentOpenTimeoutId;
    console.log(`⏰ [${timestamp}] NavigationBar: Setting openTimeout for ${tabId} (200ms delay) - ID: ${timeoutId}`);
    openTimeout = setTimeout(() => {
      // Check if this timeout is still valid
      if (timeoutId === currentOpenTimeoutId) {
        console.log(`✅ [${Date.now()}] NavigationBar: openTimeout executed for ${tabId} - ID: ${timeoutId}`);
        openDropdown(tabId);
      } else {
        console.log(`🚫 [${Date.now()}] NavigationBar: openTimeout CANCELLED for ${tabId} - ID: ${timeoutId} (current: ${currentOpenTimeoutId})`);
      }
    }, 100);
  }

  function handleMouseLeave() {
    const timestamp = Date.now();
    console.log(`🖱️ [${timestamp}] NavigationBar: handleMouseLeave()`);

    console.log(`🔍 [${timestamp}] NavigationBar: Current dropdown state:`, {
      isOpen: dropdownState.isOpen,
      tabId: dropdownState.tabId,
      openTimeout: openTimeout !== null,
      closeTimeout: closeTimeout !== null
    });

    // Clear any pending open timeout
    if (openTimeout) {
      console.log(`🚫 [${timestamp}] NavigationBar: Clearing pending openTimeout`);
      clearTimeout(openTimeout);
      openTimeout = null;
    }

    // Increment timeout ID to invalidate any pending open timeouts
    currentOpenTimeoutId++;

    // Set timeout to close dropdown with ID tracking
    const timeoutId = ++currentCloseTimeoutId;
    console.log(`⏰ [${timestamp}] NavigationBar: Setting closeTimeout (300ms delay) - ID: ${timeoutId}`);
    closeTimeout = setTimeout(() => {
      // Check if this timeout is still valid
      if (timeoutId === currentCloseTimeoutId) {
        console.log(`✅ [${Date.now()}] NavigationBar: closeTimeout executed - ID: ${timeoutId}`);
        closeDropdown();
      } else {
        console.log(`🚫 [${Date.now()}] NavigationBar: closeTimeout CANCELLED - ID: ${timeoutId} (current: ${currentCloseTimeoutId})`);
      }
    }, 300);
  }

  // Handle mode changes
  function handleBuildModeChange(mode: string) {
    onBuildModeChange?.(mode);
    closeDropdown();
  }

  function handleLearnModeChange(mode: string) {
    onLearnModeChange?.(mode);
    closeDropdown();
  }

  // Get current mode label for display
  function getCurrentModeLabel(tabId: string): string {
    if (tabId === "construct") {
      const mode = buildModes.find((m: ModeOption) => m.id === currentBuildMode);
      return mode ? mode.label : "Build";
    } else if (tabId === "learn") {
      const mode = learnModes.find((m: ModeOption) => m.id === currentLearnMode);
      return mode ? mode.label : "Learn";
    }
    return "";
  }

  // Check if tab has dropdown
  function hasDropdown(tabId: string): boolean {
    return (tabId === "construct" && buildModes.length > 0) ||
           (tabId === "learn" && learnModes.length > 0);
  }

  // Separate main and developer tabs for display
  const mainTabs = $derived(() => tabs.filter((tab: { isMain: boolean; }) => tab.isMain !== false));
  const devTabs = $derived(() => tabs.filter((tab: { isMain: boolean; }) => tab.isMain === false));
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
    <!-- Main tabs with dropdown support -->
    {#each mainTabs() as tab}
      <div class="nav-tab-container" class:has-dropdown={hasDropdown(tab.id)}>
        <button
          class="nav-tab"
          class:active={activeTab === tab.id}
          onclick={() => handleTabClick(tab)}
          onmouseenter={() => handleMouseEnter(tab.id)}
          onmouseleave={handleMouseLeave}
          aria-pressed={activeTab === tab.id}
        >
          <span class="tab-icon">{tab.icon}</span>
          <span class="tab-label">{tab.label}</span>

          <!-- Dropdown chevron for tabs with modes -->
          {#if hasDropdown(tab.id)}
            <span
              class="dropdown-chevron"
              class:active={dropdownState.isOpen && dropdownState.tabId === tab.id}
            >
              ▼
            </span>
          {/if}
        </button>

        <!-- Desktop Dropdown -->
        {#if hasDropdown(tab.id) && !isMobile() && dropdownState.isOpen && dropdownState.tabId === tab.id}
          <div
            role="region"
            aria-label="Dropdown menu container"
            onmouseenter={() => {
              const timestamp = Date.now();
              console.log(`🖱️ [${timestamp}] NavigationBar: Dropdown container mouseenter for ${tab.id}`);
              // Clear any pending close timeout when hovering over dropdown
              if (closeTimeout) {
                console.log(`🚫 [${timestamp}] NavigationBar: Clearing closeTimeout on dropdown hover`);
                clearTimeout(closeTimeout);
                closeTimeout = null;
              }
              // Invalidate any pending close timeouts
              currentCloseTimeoutId++;
            }}
            onmouseleave={() => {
              const timestamp = Date.now();
              console.log(`🖱️ [${timestamp}] NavigationBar: Dropdown container mouseleave for ${tab.id}`);
              handleMouseLeave();
            }}
          >
            <DesktopDropdown
              modes={tab.id === "construct" ? buildModes : learnModes}
              currentMode={tab.id === "construct" ? currentBuildMode : currentLearnMode}
              onModeChange={tab.id === "construct" ? handleBuildModeChange : handleLearnModeChange}
              onClose={closeDropdown}
              isOpen={true}
            />
          </div>
        {/if}
      </div>
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

<!-- Mobile Modal for Mode Selection -->
{#if isMobile() && dropdownState.isOpen}
  <MobileModal
    modes={dropdownState.tabId === "construct" ? buildModes : learnModes}
    currentMode={dropdownState.tabId === "construct" ? currentBuildMode : currentLearnMode}
    onModeChange={dropdownState.tabId === "construct" ? handleBuildModeChange : handleLearnModeChange}
    onClose={closeDropdown}
    isOpen={true}
    contextLabel={dropdownState.tabId === "construct" ? "Build" : "Learn"}
  />
{/if}

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

  /* Dropdown-specific styles */
  .nav-tab-container {
    position: relative;
    display: flex;
    align-items: center;
  }

  .nav-tab-container.has-dropdown .nav-tab {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    justify-content: space-between;
  }

  .dropdown-chevron {
    font-size: 10px;
    color: var(--muted-foreground);
    transition: all var(--transition-fast);
    opacity: 0.7;
    margin-left: var(--spacing-xs);
    flex-shrink: 0;
  }

  .nav-tab:hover .dropdown-chevron {
    opacity: 1;
    color: var(--foreground);
  }

  .nav-tab.active .dropdown-chevron {
    opacity: 1;
    color: var(--primary-light);
  }

  .dropdown-chevron.active {
    transform: rotate(180deg);
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
