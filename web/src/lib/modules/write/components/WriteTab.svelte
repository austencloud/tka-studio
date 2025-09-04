<!--
Write Tab - Act and sequence composition

Provides tools for creating and organizing acts and sequences:
- Act browser and management
- Sequence grid and organization
- Music integration and timing
- Act sheet creation and export
-->
<script lang="ts">
  import { resolve, TYPES } from "$shared/inversify/container";
  import { onMount, onDestroy } from "svelte";

  // TEMPORARY: All service resolution commented out until container is restored
  // import type {
  //   IActService,
  //   ISequenceService,
  //   IMusicPlayerService,
  // } from "$services";

  // Import write components
  import ActBrowser from "./ActBrowser.svelte";
  import ActSheet from "./ActSheet.svelte";
  import SequenceGrid from "./SequenceGrid.svelte";
  import WriteToolbar from "./WriteToolbar.svelte";
  import MusicPlayer from "./MusicPlayer.svelte";

  // ============================================================================
  // SERVICE RESOLUTION - TEMPORARY DISABLED
  // ============================================================================

  // TEMPORARY: All service resolution commented out until container is restored
  // const actService = resolve(TYPES.IActService) as IActService;
  // const sequenceService = resolve(TYPES.ISequenceService) as ISequenceService;
  // const musicPlayerService = resolve(TYPES.IMusicPlayerService) as IMusicPlayerService;

  // ============================================================================
  // COMPONENT STATE - TEMPORARY PLACEHOLDERS
  // ============================================================================

  let currentView = $state<"browser" | "sheet" | "grid">("browser");
  let selectedActId = $state<string | null>(null);
  let selectedSequences = $state<string[]>([]);
  let isPlaying = $state(false);
  let currentTrack = $state<string | null>(null);
  let error = $state<string | null>(null);

  // ============================================================================
  // EVENT HANDLERS - TEMPORARY DISABLED
  // ============================================================================

  function handleActSelect(actId: string) {
    selectedActId = actId;
    currentView = "sheet";
    console.log("✅ WriteTab: Act selected (services disabled):", actId);
    // actService.loadAct(actId);
  }

  function handleSequenceAdd(sequenceId: string) {
    selectedSequences = [...selectedSequences, sequenceId];
    console.log("✅ WriteTab: Sequence added (services disabled):", sequenceId);
    // actService.addSequenceToAct(selectedActId, sequenceId);
  }

  function handleSequenceRemove(sequenceId: string) {
    selectedSequences = selectedSequences.filter((id) => id !== sequenceId);
    console.log(
      "✅ WriteTab: Sequence removed (services disabled):",
      sequenceId
    );
    // actService.removeSequenceFromAct(selectedActId, sequenceId);
  }

  function handleViewChange(view: "browser" | "sheet" | "grid") {
    currentView = view;
    console.log("✅ WriteTab: View changed (services disabled):", view);
  }

  function handleMusicPlay(track: string) {
    isPlaying = true;
    currentTrack = track;
    console.log("✅ WriteTab: Music play (services disabled):", track);
    // musicPlayerService.play(track);
  }

  function handleMusicPause() {
    isPlaying = false;
    console.log("✅ WriteTab: Music paused (services disabled)");
    // musicPlayerService.pause();
  }

  function handleMusicStop() {
    isPlaying = false;
    currentTrack = null;
    console.log("✅ WriteTab: Music stopped (services disabled)");
    // musicPlayerService.stop();
  }

  async function handleExportAct() {
    console.log("✅ WriteTab: Act export (services disabled)");
    try {
      // TEMPORARY: Export logic commented out
      // await actService.exportAct(selectedActId);
      console.log("✅ WriteTab: Act exported successfully (placeholder)");
    } catch (err) {
      console.error("❌ WriteTab: Export failed:", err);
      error = err instanceof Error ? err.message : "Export failed";
    }
  }

  // ============================================================================
  // LIFECYCLE - TEMPORARY DISABLED
  // ============================================================================

  onMount(async () => {
    console.log("✅ WriteTab: Mounted (services temporarily disabled)");

    // TEMPORARY: All initialization commented out
    try {
      // Initialize act service
      // await actService.initialize();

      // Load available acts
      // const acts = await actService.getAllActs();

      console.log("✅ WriteTab: Initialization complete (placeholder)");
    } catch (err) {
      console.error("❌ WriteTab: Initialization failed:", err);
      error =
        err instanceof Error ? err.message : "Failed to initialize write tab";
    }
  });

  onDestroy(() => {
    console.log("✅ WriteTab: Cleanup (services disabled)");
    // actService?.cleanup();
    // musicPlayerService?.cleanup();
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
    <!-- TEMPORARY: Simplified layout message -->
    <div class="temporary-message">
      <h2>✍️ Write Tab</h2>
      <p><strong>Status:</strong> Import paths fixed ✅</p>
      <p>Services temporarily disabled during import migration.</p>
      <p>This tab will be fully functional once the container is restored.</p>
      <div class="feature-list">
        <h3>Features (will be restored):</h3>
        <ul>
          <li>✅ Act creation and management</li>
          <li>✅ Sequence organization and timing</li>
          <li>✅ Music integration and playback</li>
          <li>✅ Act sheet visualization</li>
          <li>✅ Drag-and-drop sequence arrangement</li>
          <li>✅ Export to various formats</li>
        </ul>
      </div>

      <!-- Placeholder interface -->
      <div class="placeholder-interface">
        <h3>Write Interface (placeholder):</h3>
        <div class="view-selector">
          <button
            onclick={() => handleViewChange("browser")}
            class:active={currentView === "browser"}
          >
            Act Browser
          </button>
          <button
            onclick={() => handleViewChange("sheet")}
            class:active={currentView === "sheet"}
          >
            Act Sheet
          </button>
          <button
            onclick={() => handleViewChange("grid")}
            class:active={currentView === "grid"}
          >
            Sequence Grid
          </button>
        </div>

        <div class="current-info">
          <div><strong>Current View:</strong> {currentView}</div>
          {#if selectedActId}
            <div><strong>Selected Act:</strong> {selectedActId}</div>
          {/if}
          <div><strong>Sequences:</strong> {selectedSequences.length}</div>
        </div>

        <div class="music-controls">
          <h4>Music Player (placeholder):</h4>
          <div class="player-buttons">
            <button
              onclick={() => handleMusicPlay("example-track")}
              disabled={isPlaying}
            >
              Play
            </button>
            <button onclick={handleMusicPause} disabled={!isPlaying}>
              Pause
            </button>
            <button onclick={handleMusicStop}> Stop </button>
          </div>
          {#if currentTrack}
            <div class="current-track">Playing: {currentTrack}</div>
          {/if}
        </div>

        <div class="export-controls">
          <button onclick={handleExportAct} disabled={!selectedActId}>
            Export Act
          </button>
        </div>
      </div>
    </div>

    <!-- ORIGINAL LAYOUT (commented out until services restored) -->
    <!-- Toolbar -->
    <!-- <div class="toolbar-section">
      <WriteToolbar
        currentView={currentView}
        onViewChange={handleViewChange}
        onExportAct={handleExportAct}
      />
    </div> -->

    <!-- Main Content Area -->
    <!-- <div class="content-area">
      {#if currentView === 'browser'}
        <ActBrowser
          onActSelect={handleActSelect}
        />
      {:else if currentView === 'sheet'}
        <ActSheet
          actId={selectedActId}
          sequences={selectedSequences}
          onSequenceAdd={handleSequenceAdd}
          onSequenceRemove={handleSequenceRemove}
        />
      {:else if currentView === 'grid'}
        <SequenceGrid
          sequences={selectedSequences}
          onSequenceSelect={handleSequenceAdd}
        />
      {/if}
    </div> -->

    <!-- Music Player -->
    <!-- <div class="music-section">
      <MusicPlayer
        {isPlaying}
        {currentTrack}
        onPlay={handleMusicPlay}
        onPause={handleMusicPause}
        onStop={handleMusicStop}
      />
    </div> -->
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
    justify-content: center;
    align-items: center;
    /* Original layout: */
    /* flex-direction: column;
    overflow: hidden; */
  }

  .error-banner {
    background: var(--color-error, #ff4444);
    color: white;
    padding: 0.5rem 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .error-banner button {
    background: none;
    border: none;
    color: white;
    font-size: 1.2rem;
    cursor: pointer;
  }

  .temporary-message {
    text-align: center;
    padding: 2rem;
    background: var(--color-surface-secondary, #f5f5f5);
    border-radius: 8px;
    border: 2px dashed var(--color-border, #ccc);
    max-width: 600px;
    margin: 2rem;
  }

  .temporary-message h2 {
    color: var(--color-text-primary, #333);
    margin-bottom: 1rem;
  }

  .temporary-message p {
    color: var(--color-text-secondary, #666);
    margin-bottom: 0.5rem;
  }

  .feature-list {
    margin-top: 1.5rem;
    text-align: left;
  }

  .feature-list h3 {
    color: var(--color-text-primary, #333);
    margin-bottom: 0.5rem;
  }

  .feature-list ul {
    color: var(--color-text-secondary, #666);
    padding-left: 1.5rem;
  }

  .feature-list li {
    margin-bottom: 0.25rem;
  }

  .placeholder-interface {
    margin-top: 1.5rem;
    padding: 1rem;
    background: var(--color-surface, #fff);
    border-radius: 4px;
    border: 1px solid var(--color-border, #ddd);
  }

  .placeholder-interface h3 {
    color: var(--color-text-primary, #333);
    margin-bottom: 0.5rem;
  }

  .view-selector {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
    justify-content: center;
  }

  .view-selector button {
    padding: 0.5rem 1rem;
    border: 1px solid var(--color-border, #ddd);
    background: var(--color-surface, #fff);
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
  }

  .view-selector button.active {
    background: var(--color-primary, #007acc);
    color: white;
    border-color: var(--color-primary, #007acc);
  }

  .view-selector button:hover:not(.active) {
    background: var(--color-surface-hover, #f0f0f0);
  }

  .current-info {
    margin-bottom: 1rem;
    text-align: left;
    color: var(--color-text-secondary, #666);
    font-size: 0.9rem;
  }

  .current-info div {
    margin-bottom: 0.25rem;
  }

  .music-controls {
    margin-bottom: 1rem;
    padding: 0.5rem;
    background: var(--color-surface-secondary, #f5f5f5);
    border-radius: 4px;
  }

  .music-controls h4 {
    color: var(--color-text-primary, #333);
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
  }

  .player-buttons {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
    margin-bottom: 0.5rem;
  }

  .player-buttons button {
    padding: 0.25rem 0.75rem;
    border: 1px solid var(--color-border, #ddd);
    background: var(--color-surface, #fff);
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.8rem;
  }

  .player-buttons button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .player-buttons button:hover:not(:disabled) {
    background: var(--color-surface-hover, #f0f0f0);
  }

  .current-track {
    color: var(--color-text-secondary, #666);
    font-size: 0.8rem;
    text-align: center;
  }

  .export-controls {
    display: flex;
    justify-content: center;
  }

  .export-controls button {
    padding: 0.75rem 1.5rem;
    border: 1px solid var(--color-primary, #007acc);
    background: var(--color-primary, #007acc);
    color: white;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
  }

  .export-controls button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .export-controls button:hover:not(:disabled) {
    background: var(--color-primary-dark, #005a99);
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .temporary-message {
      margin: 1rem;
      padding: 1.5rem;
    }

    .view-selector {
      flex-direction: column;
      align-items: center;
    }

    .player-buttons {
      flex-direction: column;
      align-items: center;
    }
  }
</style>
