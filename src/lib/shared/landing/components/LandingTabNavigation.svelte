<script lang="ts">
  import type { LandingSection, LandingTab } from "../domain";

  let {
    sections = [],
    activeTab,
    onSelect = () => {},
  }: {
    sections?: LandingSection[];
    activeTab: LandingTab;
    onSelect?: (tabId: LandingTab) => void;
  } = $props();
</script>

<div class="landing-tabs" role="tablist">
  {#each sections as section}
    <button
      id={`tab-${section.id}`}
      class="landing-tab"
      class:active={activeTab === section.id}
      type="button"
      role="tab"
      aria-selected={activeTab === section.id}
      aria-controls={`panel-${section.id}`}
      style="--tab-color: {section.color}; --tab-gradient: {section.gradient};"
      onclick={() => onSelect(section.id as LandingTab)}
    >
      <span class="tab-icon">{@html section.icon}</span>
      <span class="tab-label">{section.label}</span>
    </button>
  {/each}
</div>

<style>
  .landing-tabs {
    flex-shrink: 0;
    width: 100%;
    display: flex;
    gap: 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.03);
  }

  .landing-tab {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 14px 12px;
    background: transparent;
    border: none;
    border-bottom: 3px solid transparent;
    color: rgba(255, 255, 255, 0.6);
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 0.875rem;
    font-weight: 600;
    min-height: 72px;
  }

  .landing-tab:hover {
    background: rgba(255, 255, 255, 0.05);
    color: rgba(255, 255, 255, 0.9);
  }

  .landing-tab.active {
    color: var(--tab-color);
    border-bottom-color: var(--tab-color);
    background: rgba(255, 255, 255, 0.08);
  }

  .landing-tab:focus-visible {
    outline: 2px solid rgba(255, 255, 255, 0.5);
    outline-offset: -2px;
  }

  .tab-icon {
    font-size: 24px;
    display: block;
    line-height: 1;
  }

  .tab-label {
    font-size: 11px;
    display: block;
    line-height: 1.2;
    text-align: center;
  }

  @media (max-width: 640px) {
    .landing-tab {
      padding: 10px 8px;
      min-height: 64px;
      gap: 4px;
    }

    .tab-icon {
      font-size: 20px;
    }

    .tab-label {
      font-size: 10px;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .landing-tab:hover {
      transform: none;
    }
  }
</style>
