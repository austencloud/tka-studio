<script lang="ts">
  import { createMotionTesterState, type MotionTesterState } from "$state";
  import type { Container } from "inversify";
  import { getContext } from "svelte";
  import PictographVisualizationPanel from "./PictographVisualizationPanel.svelte";

  // Get DI container from context
  const getContainer = getContext<() => Container | null>("di-container");

  // State - resolved lazily when container is available
  let state: MotionTesterState | null = null;
  let initializationError: string | null = null;

  // Initialize state when container becomes available
  $: {
    const container = getContainer?.();
    console.log(
      "🎯 MotionTesterTab reactive - container:",
      container ? "available" : "null"
    );
    if (container && !state) {
      try {
        console.log("🎯 MotionTesterTab attempting to create state...");
        state = createMotionTesterState();
        console.log("🎯 MotionTesterTab state initialized successfully!");
      } catch (error) {
        console.error("🎯 MotionTesterTab failed to initialize state:", error);
        initializationError =
          error instanceof Error ? error.message : "Unknown error";
      }
    } else if (!container) {
      console.log("🎯 MotionTesterTab waiting for container...");
    }
  }

  console.log("🎯 MotionTesterTab rendered!");
</script>

<div class="motion-tester-tab">
  <header class="tester-header">
    <h1>🎯 Animator</h1>
    <p>Test individual motion sequences with visual feedback and debugging</p>
  </header>

  <main class="tester-main">
    {#if initializationError}
      <div class="error-state">
        <h2>⚠️ Initialization Error</h2>
        <p>Failed to initialize animator: {initializationError}</p>
      </div>
    {:else if !state}
      <div class="loading-state">
        <h2>🔄 Loading...</h2>
        <p>Initializing animator services...</p>
      </div>
    {:else}
      <PictographVisualizationPanel {state} />
    {/if}
  </main>
</div>

<style>
  .motion-tester-tab {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
    background: transparent;
    color: white;
    padding: 20px;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    overflow: hidden;
  }

  .tester-header {
    text-align: center;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 2px solid rgba(99, 102, 241, 0.3);
    flex-shrink: 0;
  }

  .tester-header h1 {
    font-size: 1.8rem;
    margin-bottom: 8px;
    background: linear-gradient(135deg, #a5b4fc, #c7d2fe);
    background-clip: text;
    -webkit-background-clip: text;
    color: transparent;
  }

  .tester-header p {
    color: #c7d2fe;
    font-size: 1rem;
  }

  .tester-main {
    display: flex;
    flex-direction: column;
    flex: 1;
    min-height: 0;
  }

  .loading-state,
  .error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    flex: 1;
    text-align: center;
    padding: 40px 20px;
  }

  .loading-state h2 {
    color: #a5b4fc;
    margin-bottom: 10px;
    font-size: 1.5rem;
  }

  .loading-state p {
    color: #c7d2fe;
    font-size: 1rem;
  }

  .error-state h2 {
    color: #f87171;
    margin-bottom: 10px;
    font-size: 1.5rem;
  }

  .error-state p {
    color: #fca5a5;
    font-size: 1rem;
    max-width: 600px;
    word-wrap: break-word;
  }

  /* Responsive design */
  @media (max-width: 1000px) {
    .motion-tester-tab {
      padding: 15px;
    }

    .tester-header h1 {
      font-size: 1.5rem;
    }
  }

  @media (max-width: 768px) {
    .motion-tester-tab {
      padding: 10px;
    }

    .tester-header {
      margin-bottom: 15px;
      padding-bottom: 10px;
    }

    .tester-header h1 {
      font-size: 1.3rem;
    }

    .tester-header p {
      font-size: 0.9rem;
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .motion-tester-tab {
      transition: none;
    }
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    .tester-header {
      border-bottom-color: white;
    }
  }
</style>
