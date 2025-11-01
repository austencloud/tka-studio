<!--
  LibraryTab.svelte - Personal Library Interface

  Features:
  - My Sequences: User-created and starred sequences
  - My Acts: User-created acts (coming soon)
  - Organization: Folders, tags, collections

  Navigation via bottom tabs (mobile-first UX pattern)
-->
<script lang="ts">
  import { navigationState } from "$shared";
  import { onMount } from "svelte";
  import SequencesView from "./components/SequencesView.svelte";

  type LibraryMode = "sequences" | "acts";

  // Active mode synced with navigation state
  let activeMode = $state<LibraryMode>("sequences");

  // Sync with navigation state
  $effect(() => {
    const section = navigationState.currentSection;
    if (section === "sequences" || section === "acts") {
      activeMode = section;
    }
  });

  // Initialize on mount
  onMount(() => {
    // Set default mode if none persisted
    const section = navigationState.currentSection;
    if (!section || (section !== "sequences" && section !== "acts")) {
      navigationState.setCurrentSection("sequences");
    }
  });

  // Check if mode is active
  function isModeActive(mode: LibraryMode): boolean {
    return activeMode === mode;
  }
</script>

<div class="library-tab">
  <!-- Content area (all modes) -->
  <div class="content-container">
    <!-- Sequences Mode -->
    <div class="mode-panel" class:active={isModeActive("sequences")}>
      <SequencesView />
    </div>

    <!-- Acts Mode (Coming Soon) -->
    <div class="mode-panel" class:active={isModeActive("acts")}>
      <div class="coming-soon">
        <i class="fas fa-film"></i>
        <h2>Acts Coming Soon</h2>
        <p>
          Create acts by combining multiple sequences together.<br />
          This feature is under development.
        </p>
      </div>
    </div>
  </div>
</div>

<style>
  .library-tab {
    position: relative;
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
    background: transparent;
    color: var(--foreground, #ffffff);

    /* Enable container queries for responsive design */
    container-type: size;
    container-name: library-tab;
  }

  /* Content container */
  .content-container {
    position: relative;
    flex: 1;
    width: 100%;
    height: 100%;
    overflow: hidden;
  }

  /* Mode panels */
  .mode-panel {
    position: absolute;
    inset: 0;
    display: none;
    width: 100%;
    height: 100%;
    overflow: hidden;
  }

  .mode-panel.active {
    display: flex;
    flex-direction: column;
  }

  /* Coming Soon State */
  .coming-soon {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: var(--spacing-xl);
    text-align: center;
    color: rgba(255, 255, 255, 0.7);
  }

  .coming-soon i {
    font-size: 4rem;
    margin-bottom: var(--spacing-lg);
    opacity: 0.5;
  }

  .coming-soon h2 {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: var(--spacing-md);
    color: rgba(255, 255, 255, 0.9);
  }

  .coming-soon p {
    font-size: 1rem;
    line-height: 1.6;
    max-width: 400px;
  }
</style>
