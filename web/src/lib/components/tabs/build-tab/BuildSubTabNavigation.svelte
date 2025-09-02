<!--
	BuildTabNavigation.svelte

	Tab navigation component extracted from BuildTab.
	Handles the 4-tab navigation (Build/Generate/Edit/Export) with active state management.
-->
<script lang="ts">
  import type { ActiveBuildSubTab } from "$domain";
  import { constructTabTransitionService } from "$implementations";

  // Props from parent
  interface Props {
    activeBuildSubTab: ActiveBuildSubTab;
    setActiveBuildSubTab: (tab: ActiveBuildSubTab) => void;
  }

  const {
    activeBuildSubTab: activeBuildsubTab,
    setActiveBuildSubTab: setActiveBuildSubTab,
  }: Props = $props();

  async function handleTabClick(targetTab: ActiveBuildSubTab) {
    await constructTabTransitionService.handleMainTabTransition(
      targetTab,
      activeBuildsubTab,
      setActiveBuildSubTab
    );
  }

  function handleKeyDown(event: KeyboardEvent, targetTab: ActiveBuildSubTab) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      handleTabClick(targetTab);
    }
  }
</script>

<div class="main-tab-navigation" data-testid="tab-navigation">
  <button
    type="button"
    class="main-tab-btn"
    class:active={activeBuildsubTab === "construct"}
    onclick={() => handleTabClick("construct")}
    onkeydown={(e) => handleKeyDown(e, "construct")}
  >
    🔨 Construct
  </button>
  <button
    type="button"
    class="main-tab-btn"
    class:active={activeBuildsubTab === "generate"}
    onclick={() => handleTabClick("generate")}
    onkeydown={(e) => handleKeyDown(e, "generate")}
  >
    ⚡ Generate
  </button>
  <button
    type="button"
    class="main-tab-btn"
    class:active={activeBuildsubTab === "edit"}
    onclick={() => handleTabClick("edit")}
    onkeydown={(e) => handleKeyDown(e, "edit")}
  >
    🔧 Edit
  </button>
  <button
    type="button"
    class="main-tab-btn"
    class:active={activeBuildsubTab === "export"}
    onclick={() => handleTabClick("export")}
    onkeydown={(e) => handleKeyDown(e, "export")}
  >
    🔤 Export
  </button>
</div>

<style>
  .main-tab-navigation {
    flex-shrink: 0;
    display: flex;
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px 12px 0 0;
    padding: 4px;
    gap: 2px;
    position: relative;
    overflow: hidden;
  }

  .main-tab-navigation::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.3),
      transparent
    );
  }

  .main-tab-btn {
    flex: 1;
    padding: var(--spacing-md);
    border: none;
    background: transparent;
    color: var(--muted-foreground);
    cursor: pointer;
    transition: all var(--transition-normal);
    font-size: var(--font-size-sm);
    font-weight: 600;
    border: 1px solid transparent;
    border-radius: 8px 8px 0 0;
    position: relative;
    overflow: hidden;
  }

  .main-tab-btn::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--gradient-primary);
    opacity: 0;
    transition: opacity var(--transition-normal);
    z-index: -1;
  }

  .main-tab-btn:hover {
    background: var(--surface-hover);
    color: var(--foreground);
    border-color: rgba(255, 255, 255, 0.15);
    backdrop-filter: var(--glass-backdrop);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  }

  .main-tab-btn.active {
    background: var(--surface-active);
    backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border-hover);
    color: var(--primary-light);
    box-shadow: var(--shadow-glass);
    transform: translateY(-2px);
  }

  .main-tab-btn.active::before {
    opacity: 0.1;
  }

  .main-tab-btn.active::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--gradient-primary);
    border-radius: 2px 2px 0 0;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .main-tab-navigation {
      flex-wrap: wrap;
    }

    .main-tab-btn {
      flex: 1 1 50%;
      padding: var(--spacing-sm);
      font-size: var(--font-size-xs);
    }
  }
</style>
