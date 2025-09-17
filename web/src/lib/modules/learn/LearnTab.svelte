<!--
Learn Tab - Master learning interface with sub-tabs

Provides access to all learning modes:
- Codex: Browse and reference all TKA letters
- Quiz: Interactive learning and testing
- Read: Beautiful PDF flipbook reader
-->
<script lang="ts">
  import { navigationState } from "$shared";
  import { onMount } from "svelte";
  import CodexTab from "./codex/components/CodexTab.svelte";
  import QuizTab from "./quiz/components/QuizTab.svelte";
  import ReadTab from "./read/components/ReadTab.svelte";
  import { persistentPDFState } from "./read/state";

  // Sub-tab state synced with navigation state
  let activeSubTab = $state<"codex" | "quiz" | "read">(navigationState.currentLearnMode as "codex" | "quiz" | "read");

  // Sync with navigation state
  $effect(() => {
    const navMode = navigationState.currentLearnMode as "codex" | "quiz" | "read";
    if (navMode !== activeSubTab) {
      activeSubTab = navMode;
    }
  });

  // Load persisted sub-tab on mount and start PDF loading in background
  onMount(async () => {
    // Navigation state handles persistence, just sync local state
    activeSubTab = navigationState.currentLearnMode as "codex" | "quiz" | "read";
    
    // Start loading PDF in background for snappy experience
    try {
      console.log("📚 LearnTab: Starting background PDF load");
      await persistentPDFState.ensurePDFLoaded("/static/Level 1.pdf");
      console.log("📚 LearnTab: Background PDF load completed");
    } catch (error) {
      console.warn("📚 LearnTab: Background PDF load failed:", error);
    }
  });





  // Check if a sub-tab is active
  function isSubTabActive(tabId: "codex" | "quiz" | "read"): boolean {
    return activeSubTab === tabId;
  }
</script>

<div class="learn-tab">
  <!-- Sub-tab Navigation -->


  <!-- Sub-tab Content -->
  <div class="sub-tab-content">
    <!-- Use visibility instead of conditional rendering to keep components alive -->
    <div class="tab-panel" class:active={isSubTabActive("codex")}>
      <CodexTab />
    </div>
    
    <div class="tab-panel" class:active={isSubTabActive("quiz")}>
      <QuizTab />
    </div>
    
    <div class="tab-panel" class:active={isSubTabActive("read")}>
      <ReadTab />
    </div>
  </div>
</div>

<style>
  .learn-tab {
    display: flex;
    flex-direction: column;
    height: 100%;
    background: transparent;
    color: var(--foreground, #ffffff);
  }

  .sub-tab-content {
    flex: 1;
    position: relative;
    height: 100%;
  }

  .tab-panel {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: none;
    height: 100%;
    width: 100%;
  }

  .tab-panel.active {
    display: block;
  }
</style>
