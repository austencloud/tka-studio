<!--
Write Tab - Act and sequence composition

Provides tools for creating and organizing acts and sequences:
- Act browser and management
- Sequence grid and organization
- Music integration and timing
- Act sheet creation and export
-->
<script lang="ts">
  import { onDestroy, onMount } from "svelte";
  import { ActBrowser, ActSheet, MusicPlayer, WriteToolbar } from ".";
  import { resolve, TYPES } from "../../../shared/inversify";
  import type { ISequenceService } from "../../build/workbench";
  import type { IActService, IMusicPlayerService } from "../services";
  import SequenceGrid from "./SequenceGrid.svelte";

  // ============================================================================
  // SERVICE RESOLUTION
  // ============================================================================

  const actService = resolve(TYPES.IActService) as IActService;
  const sequenceService = resolve(TYPES.ISequenceService) as ISequenceService;
  const musicPlayerService = resolve(
    TYPES.IMusicPlayerService
  ) as IMusicPlayerService;

  // ============================================================================
  // COMPONENT STATE
  // ============================================================================

  let currentView = $state<"browser" | "sheet" | "grid">("browser");
  let selectedActId = $state<string | null>(null);
  let selectedSequences = $state<string[]>([]);
  let isPlaying = $state(false);
  let currentTrack = $state<string | null>(null);
  let error = $state<string | null>(null);

  // ============================================================================
  // EVENT HANDLERS
  // ============================================================================

  async function handleActSelect(actId: string) {
    try {
      selectedActId = actId;
      currentView = "sheet";
      console.log("✅ WriteTab: Act selected:", actId);

      const act = await actService.loadAct(actId);
      if (act?.sequences) {
        selectedSequences = act.sequences;
      }
    } catch (err) {
      console.error("❌ WriteTab: Failed to load act:", err);
      error = err instanceof Error ? err.message : "Failed to load act";
    }
  }

  async function handleSequenceAdd(sequenceId: string) {
    try {
      if (!selectedActId) {
        throw new Error("No act selected");
      }

      selectedSequences = [...selectedSequences, sequenceId];
      console.log("✅ WriteTab: Sequence added:", sequenceId);

      await actService.addSequenceToAct(selectedActId, sequenceId);
    } catch (err) {
      console.error("❌ WriteTab: Failed to add sequence:", err);
      error = err instanceof Error ? err.message : "Failed to add sequence";
      // Revert state on error
      selectedSequences = selectedSequences.filter((id) => id !== sequenceId);
    }
  }

  async function handleSequenceRemove(sequenceId: string) {
    try {
      if (!selectedActId) {
        throw new Error("No act selected");
      }

      selectedSequences = selectedSequences.filter((id) => id !== sequenceId);
      console.log("✅ WriteTab: Sequence removed:", sequenceId);

      await actService.removeSequenceFromAct(selectedActId, sequenceId);
    } catch (err) {
      console.error("❌ WriteTab: Failed to remove sequence:", err);
      error = err instanceof Error ? err.message : "Failed to remove sequence";
      // Revert state on error
      selectedSequences = [...selectedSequences, sequenceId];
    }
  }

  function handleViewChange(view: "browser" | "sheet" | "grid") {
    currentView = view;
    console.log("✅ WriteTab: View changed:", view);
  }

  async function handleMusicPlay(track: string) {
    try {
      isPlaying = true;
      currentTrack = track;
      console.log("✅ WriteTab: Music play:", track);

      await musicPlayerService.play(track);
    } catch (err) {
      console.error("❌ WriteTab: Failed to play music:", err);
      error = err instanceof Error ? err.message : "Failed to play music";
      isPlaying = false;
      currentTrack = null;
    }
  }

  async function handleMusicPause() {
    try {
      isPlaying = false;
      console.log("✅ WriteTab: Music paused");

      await musicPlayerService.pause();
    } catch (err) {
      console.error("❌ WriteTab: Failed to pause music:", err);
      error = err instanceof Error ? err.message : "Failed to pause music";
    }
  }

  async function handleMusicStop() {
    try {
      isPlaying = false;
      currentTrack = null;
      console.log("✅ WriteTab: Music stopped");

      await musicPlayerService.stop();
    } catch (err) {
      console.error("❌ WriteTab: Failed to stop music:", err);
      error = err instanceof Error ? err.message : "Failed to stop music";
    }
  }

  async function handleExportAct() {
    if (!selectedActId) {
      error = "No act selected for export";
      return;
    }

    console.log("✅ WriteTab: Starting act export");
    try {
      await actService.exportAct(selectedActId);
      console.log("✅ WriteTab: Act exported successfully");
    } catch (err) {
      console.error("❌ WriteTab: Export failed:", err);
      error = err instanceof Error ? err.message : "Export failed";
    }
  }

  // ============================================================================
  // LIFECYCLE
  // ============================================================================

  onMount(async () => {
    console.log("✅ WriteTab: Mounted");

    try {
      // Initialize services
      await actService.initialize();
      await sequenceService.initialize();
      await musicPlayerService.initialize();

      // Load available acts
      const acts = await actService.getAllActs();
      console.log(
        "✅ WriteTab: Initialization complete, loaded",
        acts.length,
        "acts"
      );
    } catch (err) {
      console.error("❌ WriteTab: Initialization failed:", err);
      error =
        err instanceof Error ? err.message : "Failed to initialize write tab";
    }
  });

  onDestroy(() => {
    console.log("✅ WriteTab: Cleanup");
    actService?.cleanup();
    sequenceService?.cleanup();
    musicPlayerService?.cleanup();
  });
</script>

<!-- ============================================================================ -->
<!-- TEMPLATE -->
<!-- ============================================================================ -->

<div class="write-tab" data-testid="write-tab">
  <!-- Error display -->
  {#if error}
    <div class="error-banner">
      <span>{error}</span>
      <button onclick={() => (error = null)}>×</button>
    </div>
  {/if}

  <div class="write-layout">
    <!-- Toolbar -->
    <div class="toolbar-section">
      <WriteToolbar
        {currentView}
        {selectedActId}
        onViewChange={handleViewChange}
        onExportAct={handleExportAct}
      />
    </div>

    <!-- Main Content Area -->
    <div class="content-area">
      {#if currentView === "browser"}
        <ActBrowser onActSelect={handleActSelect} />
      {:else if currentView === "sheet"}
        <ActSheet
          actId={selectedActId}
          sequences={selectedSequences}
          onSequenceAdd={handleSequenceAdd}
          onSequenceRemove={handleSequenceRemove}
        />
      {:else if currentView === "grid"}
        <SequenceGrid
          sequences={selectedSequences}
          onSequenceSelect={handleSequenceAdd}
        />
      {/if}
    </div>

    <!-- Music Player -->
    <div class="music-section">
      <MusicPlayer
        {isPlaying}
        {currentTrack}
        onPlay={handleMusicPlay}
        onPause={handleMusicPause}
        onStop={handleMusicStop}
      />
    </div>
  </div>
</div>

<!-- ============================================================================ -->
<!-- STYLES -->
<!-- ============================================================================ -->

<style>
  .write-tab {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
    position: relative;
  }

  .write-layout {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .error-banner {
    background: var(--color-error, #ff4444);
    color: white;
    padding: 0.5rem 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 1000;
  }

  .error-banner button {
    background: none;
    border: none;
    color: white;
    font-size: 1.2rem;
    cursor: pointer;
    padding: 0;
    margin-left: 1rem;
  }

  .error-banner button:hover {
    opacity: 0.8;
  }

  .toolbar-section {
    flex-shrink: 0;
    border-bottom: 1px solid var(--color-border, #ddd);
    background: var(--color-surface, #fff);
  }

  .content-area {
    flex: 1;
    overflow: hidden;
    position: relative;
  }

  .music-section {
    flex-shrink: 0;
    border-top: 1px solid var(--color-border, #ddd);
    background: var(--color-surface, #fff);
    padding: 0.5rem;
    max-height: 120px;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .write-layout {
      gap: 0;
    }

    .music-section {
      max-height: 100px;
      padding: 0.25rem;
    }

    .error-banner {
      padding: 0.25rem 0.5rem;
      font-size: 0.9rem;
    }
  }

  @media (max-width: 480px) {
    .error-banner {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.25rem;
    }

    .error-banner button {
      align-self: flex-end;
      margin-left: 0;
    }
  }
</style>
