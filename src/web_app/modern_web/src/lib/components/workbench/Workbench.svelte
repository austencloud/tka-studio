<script lang="ts">
  import { onMount } from 'svelte';
  import { workbenchService } from '$lib/services/WorkbenchService.svelte';
  import { sequenceStateService } from '$lib/services/SequenceStateService.svelte';
  import BeatFrame from './BeatFrame.svelte';

  const currentSequence = $derived(workbenchService.currentSequence);
  const selectedBeatIndex = $derived(sequenceStateService.selectedBeatIndex);

  onMount(() => {
    workbenchService.initialize();
  });

  function handleBeatClick(index: number) {
    workbenchService.handleBeatClick(index);
  }

  function handleBeatDoubleClick(index: number) {
    workbenchService.handleBeatDoubleClick(index);
  }
</script>

<div class="workbench">

  <div class="workbench-content">
    <!-- Left: Beat Frame; Right: Button Panel placeholder (like desktop) -->
    <div class="content-row">
      <div class="left">
        <BeatFrame
          beats={currentSequence?.beats ?? [] as any}
          selectedBeatIndex={selectedBeatIndex}
          onBeatClick={handleBeatClick}
          onBeatDoubleClick={handleBeatDoubleClick}
          onStartClick={() => sequenceStateService.selectBeat(-1)}
        />
      </div>
      <div class="right">
        <div class="button-panel">
          <button type="button" class="panel-btn" title="Add to Dictionary">📚</button>
          <button type="button" class="panel-btn" title="Fullscreen">⛶</button>
          <button type="button" class="panel-btn" title="Mirror Sequence">⇄</button>
          <button type="button" class="panel-btn" title="Swap Colors">🔁</button>
          <button type="button" class="panel-btn" title="Rotate Sequence">⟲</button>
          <button type="button" class="panel-btn" title="Copy JSON">{`{ }`}</button>
          <button type="button" class="panel-btn" title="Delete Beat">🗑️</button>
          <button type="button" class="panel-btn" title="Clear Sequence">🧹</button>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .workbench {
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 24px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    max-width: 1200px;
    margin: 0 auto;
  }

  .workbench-content {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .content-row {
    display: grid;
    grid-template-columns: 10fr 1fr; /* desktop ~10:1 ratio */
    gap: 12px;
    align-items: stretch;
  }

  .left, .right { min-height: 300px; }
  .right { display: flex; flex-direction: column; gap: 8px; }

  .button-panel {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    padding: 8px;
    border: 1px solid rgba(0,0,0,0.1);
    border-radius: 12px;
    min-width: 60px;
  }

  .panel-btn {
    width: 56px;
    height: 56px;
    border-radius: 12px;
    border: 1px solid rgba(0,0,0,0.15);
    background: #fff;
    cursor: pointer;
    font-size: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .panel-btn:hover { background: #f6f6f6; }
</style>
