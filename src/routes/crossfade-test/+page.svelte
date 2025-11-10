<script lang="ts">
  import { tick } from "svelte";

  let activeTab = $state<"tab1" | "tab2" | "tab3">("tab1");
  let showSelector = $state(true);

  // Simulate the tool panel that takes time to render
  let renderCount = $state(0);

  async function handleTabSelect(tab: "tab1" | "tab2" | "tab3") {
    console.log(`🎯 User clicked ${tab}`);

    // FIRST: Change the tab (while selector still visible)
    activeTab = tab;
    console.log(`✅ Tab state changed to ${tab}`);

    // Wait for Svelte
    await tick();
    console.log(`⏱️ After tick()`);

    // Wait multiple frames to ensure effects complete and content renders
    await new Promise(resolve => requestAnimationFrame(resolve));
    console.log(`⏱️ After frame 1`);
    await new Promise(resolve => requestAnimationFrame(resolve));
    console.log(`⏱️ After frame 2`);
    await new Promise(resolve => requestAnimationFrame(resolve));
    console.log(`⏱️ After frame 3`);
    // await new Promise(resolve => requestAnimationFrame(resolve));
    console.log(`⏱️ After frame 4`);

    // THEN: Hide selector (triggers crossfade)
    showSelector = false;
    console.log(`🎬 Crossfade started - should see ${tab} content now`);
  }

  function reset() {
    showSelector = true;
    activeTab = "tab1";
    renderCount++;
  }

  // Simulate heavy rendering
  $effect(() => {
    activeTab;
    console.log(`🔄 Tool panel rendering for ${activeTab}... (render #${renderCount})`);
    // Simulate slow component
    const start = performance.now();
    while (performance.now() - start < 50) {} // Block for 50ms
    console.log(`✅ Tool panel rendered for ${activeTab}`);
  });
</script>

<div class="test-container">
  <h1>Crossfade Timing Test</h1>

  <button onclick={reset} class="reset-btn">Reset Test</button>

  <div class="transition-wrapper">
    <!-- Selector View -->
    <div
      class="transition-view"
      class:active={showSelector}
      class:inactive={!showSelector}
    >
      <div class="selector">
        <h2>Choose a Tab</h2>
        <div class="buttons">
          <button onclick={() => handleTabSelect("tab1")}>Tab 1</button>
          <button onclick={() => handleTabSelect("tab2")}>Tab 2</button>
          <button onclick={() => handleTabSelect("tab3")}>Tab 3</button>
        </div>
      </div>
    </div>

    <!-- Tool Panel View -->
    <div
      class="transition-view"
      class:active={!showSelector}
      class:inactive={showSelector}
    >
      <div class="tool-panel">
        <h2>Tool Panel</h2>
        <div class="tab-content" class:tab1={activeTab === "tab1"} class:tab2={activeTab === "tab2"} class:tab3={activeTab === "tab3"}>
          {#if activeTab === "tab1"}
            <div class="content red">Tab 1 Content (RED)</div>
          {:else if activeTab === "tab2"}
            <div class="content green">Tab 2 Content (GREEN)</div>
          {:else}
            <div class="content blue">Tab 3 Content (BLUE)</div>
          {/if}
        </div>
      </div>
    </div>
  </div>

  <div class="debug">
    <p>Active Tab: <strong>{activeTab}</strong></p>
    <p>Selector Visible: <strong>{showSelector}</strong></p>
    <p>Render Count: <strong>{renderCount}</strong></p>
  </div>
</div>

<style>
  .test-container {
    padding: 2rem;
    max-width: 800px;
    margin: 0 auto;
  }

  h1 {
    margin-bottom: 1rem;
  }

  .reset-btn {
    margin-bottom: 2rem;
    padding: 0.5rem 1rem;
    background: #3b82f6;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
  }

  .reset-btn:hover {
    background: #2563eb;
  }

  .transition-wrapper {
    position: relative;
    height: 400px;
    border: 2px solid #333;
    border-radius: 8px;
    overflow: hidden;
    background: #1a1a1a;
  }

  .transition-view {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    height: 100%;
    transition: opacity 400ms cubic-bezier(0.4, 0, 0.2, 1);
  }

  .transition-view.active {
    opacity: 1;
    pointer-events: auto;
    z-index: 1;
  }

  .transition-view.inactive {
    opacity: 0;
    pointer-events: none;
    z-index: 0;
  }

  .selector {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    gap: 2rem;
  }

  .buttons {
    display: flex;
    gap: 1rem;
  }

  button {
    padding: 1rem 2rem;
    font-size: 1rem;
    background: rgba(255, 255, 255, 0.1);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    cursor: pointer;
    transition: all 200ms;
  }

  button:hover {
    background: rgba(255, 255, 255, 0.2);
  }

  .tool-panel {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 2rem;
  }

  .tab-content {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .content {
    padding: 3rem;
    border-radius: 12px;
    font-size: 1.5rem;
    font-weight: bold;
  }

  .red {
    background: #dc2626;
    color: white;
  }

  .green {
    background: #16a34a;
    color: white;
  }

  .blue {
    background: #2563eb;
    color: white;
  }

  .debug {
    margin-top: 2rem;
    padding: 1rem;
    background: #2a2a2a;
    border-radius: 6px;
  }

  .debug p {
    margin: 0.5rem 0;
    color: #e5e5e5;
  }

  h2 {
    color: white;
  }
</style>
