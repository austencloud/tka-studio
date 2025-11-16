<script lang="ts">
  /**
   * ModuleRenderer
   * Domain: Module Content Rendering
   *
   * Responsibilities:
   * - Render active module content
   * - Handle module transitions with simple, clean fade
   * - Coordinate with child module components via callbacks
   * - Provide loading states
   */
  import { isModuleActive } from "../application/state/app-state.svelte";
  import { fade } from "svelte/transition";
  import AboutTab from "../../modules/about/components/AboutTab.svelte";
  import AdminDashboard from "../../modules/admin/components/AdminDashboard.svelte";
  import AnimateTab from "../../modules/animate/AnimateTab.svelte";
  import CreateModule from "../../modules/create/shared/components/CreateModule.svelte";
  import LearnTab from "../../modules/learn/LearnTab.svelte";
  import CollectTab from "../../modules/collect/CollectTab.svelte";
  import LibraryTab from "../../modules/library/LibraryTab.svelte"; // Legacy support
  import WordCardTab from "../../modules/word-card/components/WordCardTab.svelte";
  import WriteTab from "../../modules/write/components/WriteTab.svelte";
  import { ExploreModule } from "../../modules";

  interface Props {
    activeModule: string | null;
    isModuleLoading: boolean;
    onTabAccessibilityChange: (canAccess: boolean) => void;
    onCurrentWordChange: (word: string) => void;
    onLearnHeaderChange: (header: string) => void;
  }

  let {
    activeModule,
    isModuleLoading,
    onTabAccessibilityChange,
    onCurrentWordChange,
    onLearnHeaderChange,
  }: Props = $props();
</script>

{#if isModuleLoading}
  <!-- Loading state while module is being restored -->
  <div class="module-loading">
    <div class="loading-spinner"></div>
    <p>Loading...</p>
  </div>
{:else}
  <!-- Transition container for overlaying content -->
  <div class="transition-container">
    {#key activeModule}
      <div
        class="module-content"
        class:about-module={isModuleActive("about")}
        transition:fade={{ duration: 200 }}
      >
        {#if isModuleActive("create")}
          <CreateModule {onTabAccessibilityChange} {onCurrentWordChange} />
        {:else if isModuleActive("explore")}
          <ExploreModule />
        {:else if isModuleActive("learn")}
          <LearnTab onHeaderChange={onLearnHeaderChange} />
        {:else if isModuleActive("collect")}
          <CollectTab />
        {:else if isModuleActive("animate")}
          <AnimateTab />
        {:else if isModuleActive("collection")}
          <CollectTab />
        {:else if isModuleActive("library")}
          <LibraryTab />
        {:else if isModuleActive("word_card")}
          <WordCardTab />
        {:else if isModuleActive("write")}
          <WriteTab />
        {:else if isModuleActive("admin")}
          <AdminDashboard />
        {:else if isModuleActive("about")}
          <AboutTab />
        {/if}
      </div>
    {/key}
  </div>
{/if}

<style>
  /* Container for overlaying transitions */
  .transition-container {
    position: relative;
    width: 100%;
    height: 100%;
    flex: 1;
    min-height: 0;
    overflow: hidden;
  }

  .module-content {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    width: 100%;
    height: 100%;
  }

  /* Allow scrolling for About module */
  .module-content.about-module {
    overflow-y: auto !important;
    overflow-x: hidden !important;
  }

  .module-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    min-height: 200px;
    color: var(--text-color, #333);
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid var(--border-color, #e0e0e0);
    border-top: 3px solid var(--primary-color, #007bff);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 16px;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  .module-loading p {
    margin: 0;
    font-size: 14px;
    opacity: 0.7;
  }

  @media (prefers-reduced-motion: reduce) {
    .loading-spinner {
      animation-duration: 3s;
    }
  }
</style>
