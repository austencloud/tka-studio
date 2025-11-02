<script lang="ts">
  /**
   * ModuleRenderer
   * Domain: Module Content Rendering
   *
   * Responsibilities:
   * - Render active module content
   * - Handle module transitions
   * - Coordinate with child module components via callbacks
   * - Provide loading states
   */
  import { isModuleActive } from "../application/state/app-state.svelte";
  import type { IAnimationService } from "../application/services/contracts";
  import { isContainerReady, resolve, TYPES } from "../inversify";
  import AboutTab from "../../modules/about/components/AboutTab.svelte";
  import AdminDashboard from "../../modules/admin/components/AdminDashboard.svelte";
  import BuildTab from "../../modules/build/shared/components/BuildTab.svelte";
  import LearnTab from "../../modules/learn/LearnTab.svelte";
  import CollectionTab from "../../modules/collection/CollectionTab.svelte";
  import LibraryTab from "../../modules/library/LibraryTab.svelte"; // Legacy support
  import WordCardTab from "../../modules/word-card/components/WordCardTab.svelte";
  import WriteTab from "../../modules/write/components/WriteTab.svelte";
  import { ExploreTab } from "../../modules";

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

  // Resolve animation service - only when container is ready
  const animationService = $derived(() => {
    if (!isContainerReady()) {
      return null;
    }
    try {
      return resolve(TYPES.IAnimationService) as IAnimationService;
    } catch (error) {
      console.warn("Failed to resolve animation service:", error);
      return null;
    }
  });

  // Simple transition functions - animations are always enabled
  const moduleOut = (_node: Element) => {
    const service = animationService();
    if (!service) {
      return { duration: 250 }; // Fallback transition
    }
    return service.createFadeTransition({
      duration: 250,
    });
  };

  const moduleIn = (_node: Element) => {
    const service = animationService();
    if (!service) {
      return { duration: 300, delay: 250 }; // Fallback transition
    }
    return service.createFadeTransition({
      duration: 300,
      delay: 250, // Wait for out transition
    });
  };
</script>

{#if isModuleLoading}
  <!-- Loading state while module is being restored -->
  <div class="module-loading">
    <div class="loading-spinner"></div>
    <p>Loading...</p>
  </div>
{:else}
  <!-- App Content with reliable transitions -->
  {#key activeModule}
    <div
      class="module-content"
      class:about-module={isModuleActive("about")}
      in:moduleIn
      out:moduleOut
    >
      {#if isModuleActive("build")}
        <BuildTab
          {onTabAccessibilityChange}
          {onCurrentWordChange}
        />
      {:else if isModuleActive("explore")}
        <ExploreTab />
      {:else if isModuleActive("learn")}
        <LearnTab onHeaderChange={onLearnHeaderChange} />
      {:else if isModuleActive("collection")}
        <CollectionTab />
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
{/if}

<style>
  .module-content {
    display: flex;
    flex-direction: column;
    overflow: hidden;
    width: 100%;
    height: 100%;
    flex: 1;
    min-height: 0; /* Allow flex children to shrink */
  }

  /* Allow scrolling for About module */
  .module-content.about-module {
    overflow-y: auto !important;
    overflow-x: hidden !important;
    height: auto !important;
    min-height: 100% !important;
  }

  /* Loading state styles */
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

  /* Disable animations when user prefers reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .module-content {
      transition: none !important;
      animation: none !important;
    }
  }
</style>
