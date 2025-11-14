<!-- Desktop Navigation Sidebar -->
<!-- Modern 2026-style sidebar navigation for desktop in side-by-side layout -->
<script lang="ts">
  import {
    resolve,
    TYPES,
    type IHapticFeedbackService,
  } from "$shared";
  import { onMount } from "svelte";
  import { slide } from 'svelte/transition';
  import {
    getShowSettings,
    toggleSettingsDialog,
  } from "../../application/state/app-state.svelte";
  import type { ModuleDefinition, Section, ModuleId } from "../domain/types";
  import {
    desktopSidebarState,
    toggleDesktopSidebarCollapsed,
    setDesktopSidebarCollapsed,
    initializeDesktopSidebarCollapsedState,
    saveDesktopSidebarCollapsedState,
  } from "../../layout/desktop-sidebar-state.svelte";
  import InfoButton from "../../info/components/InfoButton.svelte";
  import { toggleInfo } from "../../info/state/info-state.svelte";

  let {
    currentModule,
    currentSection,
    modules = [],
    onModuleChange,
    onSectionChange,
    onHeightChange,
  } = $props<{
    currentModule: string;
    currentSection: string;
    modules: ModuleDefinition[];
    onModuleChange?: (moduleId: ModuleId) => void | Promise<void>;
    onSectionChange?: (sectionId: string) => void;
    onHeightChange?: (height: number) => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  // Ref to sidebar element
  let sidebarElement = $state<HTMLElement | null>(null);

  // Track which modules are expanded
  let expandedModules = $state<Set<string>>(new Set([currentModule]));

  // Get collapsed state reactively
  const isCollapsed = $derived(desktopSidebarState.isCollapsed);

  // Track when we're transitioning from collapsed to expanded
  // This prevents sections from sliding in while the sidebar is still narrow
  let isTransitioningFromCollapsed = $state(false);

  function toggleModuleExpansion(moduleId: string) {
    const newExpanded = new Set(expandedModules);
    if (newExpanded.has(moduleId)) {
      newExpanded.delete(moduleId);
    } else {
      newExpanded.add(moduleId);
    }
    expandedModules = newExpanded;
  }

  function handleModuleTap(moduleId: string, isDisabled: boolean = false) {
    // Don't trigger haptic or allow interaction for disabled modules
    if (isDisabled) {
      return;
    }

    hapticService?.trigger("selection");

    // If sidebar is collapsed, expand it and show the clicked module's sections
    if (isCollapsed) {
      // Expand the sidebar
      setDesktopSidebarCollapsed(false);
      saveDesktopSidebarCollapsedState(false);

      // Set transition flag to prevent section slide animation during width expansion
      isTransitioningFromCollapsed = true;

      // Delay expanding the module until after the sidebar width transition completes (300ms)
      setTimeout(() => {
        expandedModules = new Set([moduleId]);
        isTransitioningFromCollapsed = false;
      }, 300);
    } else {
      // When expanded, module buttons toggle expansion
      toggleModuleExpansion(moduleId);
    }
  }

  function handleSectionTap(moduleId: string, section: Section) {
    if (!section.disabled) {
      hapticService?.trigger("selection");

      // Switch to the section's module if we're not already on it
      if (moduleId !== currentModule) {
        onModuleChange?.(moduleId as ModuleId);
      }

      // Then switch to the section
      onSectionChange?.(section.id);

      // Ensure the module is expanded after navigation
      expandedModules = new Set([...expandedModules, moduleId]);
    }
  }

  function handleSettingsTap() {
    hapticService?.trigger("selection");
    toggleSettingsDialog();
  }

  function handleToggleCollapse() {
    hapticService?.trigger("selection");
    toggleDesktopSidebarCollapsed();
    saveDesktopSidebarCollapsedState(desktopSidebarState.isCollapsed);
  }

  function handleLogoTap() {
    hapticService?.trigger("selection");
    toggleInfo();
  }

  onMount(() => {
    // Initialize collapsed state from localStorage
    initializeDesktopSidebarCollapsedState();

    // Initialize services
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );

    // Set up ResizeObserver to measure and report sidebar height
    let resizeObserver: ResizeObserver | null = null;
    if (sidebarElement) {
      resizeObserver = new ResizeObserver((entries) => {
        for (const entry of entries) {
          const height =
            entry.borderBoxSize?.[0]?.blockSize ?? entry.contentRect.height;
          onHeightChange?.(height);
        }
      });
      resizeObserver.observe(sidebarElement);

      // Report initial height
      const initialHeight = sidebarElement.getBoundingClientRect().height;
      if (initialHeight > 0) {
        onHeightChange?.(initialHeight);
      }
    }

    // Return cleanup function
    return () => {
      resizeObserver?.disconnect();
    };
  });
</script>

<nav class="desktop-navigation-sidebar" class:collapsed={isCollapsed} bind:this={sidebarElement}>
  <!-- Sidebar Header/Branding -->
  <div class="sidebar-header">
    <button
      class="studio-logo"
      onclick={handleLogoTap}
      aria-label="Open resources and support"
      title="Resources & Support"
    >
      <InfoButton variant="sidebar-icon" />
      {#if !isCollapsed}
        <span class="studio-name">TKA Studio</span>
      {/if}
    </button>
    <!-- Collapse Toggle Button -->
    <button
      class="collapse-toggle"
      onclick={handleToggleCollapse}
      aria-label={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
      title={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
    >
      <i class="fas fa-{isCollapsed ? 'angle-right' : 'angle-left'}"></i>
    </button>
  </div>

  <!-- Modules List -->
  <div class="modules-container">
    {#each modules.filter((m: ModuleDefinition) => m.isMain) as module}
      {@const isActive = currentModule === module.id}
      {@const isExpanded = expandedModules.has(module.id)}
      {@const isDisabled = module.disabled ?? false}

      <div class="module-group">
        <!-- Module Button -->
        <button
          class="module-button"
          class:active={isActive}
          class:expanded={isExpanded}
          class:disabled={isDisabled}
          onclick={() => handleModuleTap(module.id, isDisabled)}
          aria-label={module.label}
          aria-expanded={isExpanded}
          aria-current={isActive ? "page" : undefined}
          aria-disabled={isDisabled}
          disabled={isDisabled}
        >
          <span class="module-icon">{@html module.icon}</span>
          {#if !isCollapsed}
            <span class="module-label">{module.label}</span>
            {#if isDisabled && module.disabledMessage}
              <span class="disabled-badge">{module.disabledMessage}</span>
            {:else}
              <span class="expand-icon">
                <i class="fas fa-chevron-{isExpanded ? 'down' : 'right'}"></i>
              </span>
            {/if}
          {/if}
        </button>

        <!-- Module Sections/Tabs (collapsible) -->
        {#if isExpanded && module.sections.length > 0 && !isCollapsed && !isTransitioningFromCollapsed}
          <div class="sections-list" transition:slide={{ duration: 200 }}>
            {#each module.sections as section}
              {@const isSectionActive = currentSection === section.id && isActive}

              <button
                class="section-button"
                class:active={isSectionActive}
                class:disabled={section.disabled}
                onclick={() => handleSectionTap(module.id, section)}
                disabled={section.disabled}
                aria-label={section.label}
                style="--section-color: {section.color ||
                  'var(--muted-foreground)'}; --section-gradient: {section.gradient ||
                  section.color ||
                  'var(--muted-foreground)'};"
              >
                <span class="section-icon">{@html section.icon}</span>
                <span class="section-label">{section.label}</span>
                {#if isSectionActive}
                  <span class="active-indicator"></span>
                {/if}
              </button>
            {/each}
          </div>
        {/if}
      </div>
    {/each}
  </div>

  <!-- Sidebar Footer -->
  <div class="sidebar-footer">
    <button
      class="footer-button settings-button"
      class:active={getShowSettings()}
      onclick={handleSettingsTap}
      aria-label="Settings"
    >
      <i class="fas fa-cog"></i>
      {#if !isCollapsed}
        <span>Settings</span>
      {/if}
    </button>
  </div>
</nav>

<style>
  /* ============================================================================
     DESKTOP NAVIGATION SIDEBAR - 2026 MODERN DESIGN
     ============================================================================ */
  .desktop-navigation-sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    width: 220px;
    display: flex;
    flex-direction: column;
    background: rgba(10, 10, 15, 0.85);
    backdrop-filter: blur(40px) saturate(180%);
    -webkit-backdrop-filter: blur(40px) saturate(180%);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
    z-index: 150;
    overflow: hidden;
    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);

    /* Safe area support */
    padding-left: env(safe-area-inset-left);
  }

  .desktop-navigation-sidebar.collapsed {
    width: 64px;
  }

  /* ============================================================================
     SIDEBAR HEADER
     ============================================================================ */
  .sidebar-header {
    padding: 20px 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    background: linear-gradient(
      135deg,
      rgba(103, 126, 234, 0.08) 0%,
      rgba(118, 75, 162, 0.08) 100%
    );
    display: flex;
    flex-direction: column;
    gap: 10px;
    position: relative;
  }

  .desktop-navigation-sidebar.collapsed .sidebar-header {
    padding: 20px 10px;
    align-items: center;
  }

  .studio-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    color: rgba(255, 255, 255, 0.95);
    width: 100%;
    padding: 0;
    background: transparent;
    border: none;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 10px;
    position: relative;
  }

  .studio-logo::before {
    content: '';
    position: absolute;
    inset: -8px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    opacity: 0;
    transition: opacity 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .studio-logo:hover::before {
    opacity: 1;
  }

  .studio-logo:hover {
    transform: translateX(2px);
  }

  .studio-logo:active {
    transform: scale(0.98);
  }

  .desktop-navigation-sidebar.collapsed .studio-logo {
    justify-content: center;
    gap: 0;
  }

  /* InfoButton in sidebar logo inherits its own styling from InfoButton.svelte */

  .studio-name {
    font-size: 18px;
    font-weight: 700;
    letter-spacing: -0.02em;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.95) 0%,
      rgba(255, 255, 255, 0.75) 100%
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  /* ============================================================================
     COLLAPSE TOGGLE BUTTON
     ============================================================================ */
  .collapse-toggle {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px;
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: rgba(255, 255, 255, 0.6);
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    font-size: 16px;
  }

  .collapse-toggle:hover {
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.95);
    border-color: rgba(255, 255, 255, 0.2);
  }

  .collapse-toggle:active {
    transform: scale(0.95);
  }

  .desktop-navigation-sidebar.collapsed .collapse-toggle {
    padding: 12px 8px;
  }

  /* ============================================================================
     MODULES CONTAINER
     ============================================================================ */
  .modules-container {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 16px 12px;

    /* Custom scrollbar */
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.1) transparent;
  }

  .modules-container::-webkit-scrollbar {
    width: 6px;
  }

  .modules-container::-webkit-scrollbar-track {
    background: transparent;
  }

  .modules-container::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
  }

  .modules-container::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.15);
  }

  /* ============================================================================
     MODULE GROUP
     ============================================================================ */
  .module-group {
    margin-bottom: 8px;
  }

  .module-group:last-child {
    margin-bottom: 0;
  }

  /* ============================================================================
     MODULE BUTTON
     ============================================================================ */
  .module-button {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    background: transparent;
    border: none;
    border-radius: 10px;
    color: rgba(255, 255, 255, 0.7);
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
  }

  .desktop-navigation-sidebar.collapsed .module-button {
    justify-content: center;
    padding: 10px 6px;
  }

  .module-button::before {
    content: '';
    position: absolute;
    inset: 0;
    background: rgba(255, 255, 255, 0.05);
    opacity: 0;
    transition: opacity 0.25s ease;
    border-radius: 12px;
  }

  .module-button:hover::before {
    opacity: 1;
  }

  .module-button:hover {
    color: rgba(255, 255, 255, 0.95);
    transform: translateX(2px);
  }

  /* Module buttons are just expand/collapse controls, not primary navigation */
  /* Keep them subtle - only tabs should have strong active states */
  .module-button.expanded {
    color: rgba(255, 255, 255, 0.85);
  }

  /* Active module indicator - shows which module you're currently in */
  .module-button.active {
    color: rgba(255, 255, 255, 0.95);
    position: relative;
  }

  .module-button.active::after {
    content: '';
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 3px;
    height: 60%;
    background: linear-gradient(
      135deg,
      rgba(103, 126, 234, 0.8) 0%,
      rgba(118, 75, 162, 0.8) 100%
    );
    border-radius: 0 2px 2px 0;
    box-shadow: 0 0 8px rgba(103, 126, 234, 0.4);
  }

  .desktop-navigation-sidebar.collapsed .module-button.active::after {
    left: 50%;
    transform: translate(-50%, -50%);
    width: 60%;
    height: 3px;
    border-radius: 2px;
  }

  .module-icon {
    font-size: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    width: 20px;
    height: 20px;
    transition: transform 0.25s ease;
  }

  .module-button:hover .module-icon {
    transform: scale(1.05);
  }

  .module-label {
    flex: 1;
    text-align: left;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: -0.01em;
  }

  .expand-icon {
    font-size: 12px;
    opacity: 0.5;
    transition: all 0.25s ease;
  }

  .module-button.expanded .expand-icon {
    opacity: 0.8;
  }

  .module-button:hover .expand-icon {
    opacity: 1;
  }

  /* Disabled module styles */
  .module-button.disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .module-button.disabled:hover {
    transform: none;
    color: rgba(255, 255, 255, 0.7);
  }

  .module-button.disabled::before {
    display: none;
  }

  .disabled-badge {
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.15);
    letter-spacing: 0.5px;
  }

  /* ============================================================================
     SECTIONS LIST
     ============================================================================ */
  .sections-list {
    margin-top: 4px;
    padding-left: 12px;
    border-left: 2px solid rgba(255, 255, 255, 0.06);
    margin-left: 28px;
  }

  /* ============================================================================
     SECTION BUTTON
     ============================================================================ */
  .section-button {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    background: transparent;
    border: none;
    border-radius: 8px;
    color: rgba(255, 255, 255, 0.6);
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    margin-bottom: 2px;
  }

  .section-button:hover:not(.disabled) {
    background: rgba(255, 255, 255, 0.05);
    color: rgba(255, 255, 255, 0.9);
    transform: translateX(2px);
  }

  .section-button.active {
    color: rgba(255, 255, 255, 1);
    background: rgba(255, 255, 255, 0.08);
  }

  .section-button.disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }

  .section-icon {
    font-size: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    width: 20px;
    height: 20px;
  }

  /* Style icons with gradient colors */
  .section-icon :global(i) {
    background: var(--section-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 6px rgba(0, 0, 0, 0.2));
  }

  .section-button:not(.active) .section-icon :global(i) {
    opacity: 0.7;
  }

  .section-button:hover .section-icon :global(i) {
    opacity: 1;
  }

  .section-button.active .section-icon :global(i) {
    opacity: 1;
    filter: drop-shadow(0 0 10px var(--section-color)) brightness(1.1);
  }

  .section-label {
    flex: 1;
    text-align: left;
    font-size: 14px;
    font-weight: 500;
    letter-spacing: -0.005em;
  }

  .active-indicator {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--section-gradient);
    box-shadow: 0 0 8px var(--section-color);
    flex-shrink: 0;
  }

  /* ============================================================================
     SIDEBAR FOOTER
     ============================================================================ */
  .sidebar-footer {
    padding: 16px 12px;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    background: linear-gradient(
      0deg,
      rgba(0, 0, 0, 0.2) 0%,
      transparent 100%
    );
  }

  .footer-button {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: transparent;
    border: none;
    border-radius: 10px;
    color: rgba(255, 255, 255, 0.7);
    cursor: pointer;
    transition: all 0.25s ease;
    font-size: 15px;
    font-weight: 500;
  }

  .desktop-navigation-sidebar.collapsed .footer-button {
    justify-content: center;
    padding: 12px 8px;
  }

  .footer-button:hover {
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.95);
    transform: translateX(2px);
  }

  .footer-button.active {
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 1);
  }

  .footer-button i {
    font-size: 18px;
  }

  /* ============================================================================
     ANIMATIONS & TRANSITIONS
     ============================================================================ */
  @media (prefers-reduced-motion: reduce) {
    .desktop-navigation-sidebar * {
      transition: none !important;
      animation: none !important;
    }

    .studio-logo:hover,
    .studio-logo:active {
      transform: none !important;
    }
  }

  /* ============================================================================
     ACCESSIBILITY
     ============================================================================ */
  @media (prefers-contrast: high) {
    .desktop-navigation-sidebar {
      background: rgba(0, 0, 0, 0.95);
      border-right: 2px solid white;
    }

    .section-button.active {
      background: rgba(255, 255, 255, 0.25);
      outline: 2px solid white;
    }
  }

  /* Focus styles for keyboard navigation */
  .studio-logo:focus-visible,
  .module-button:focus-visible,
  .section-button:focus-visible,
  .footer-button:focus-visible,
  .collapse-toggle:focus-visible {
    outline: 2px solid rgba(102, 126, 234, 0.6);
    outline-offset: 2px;
  }
</style>
