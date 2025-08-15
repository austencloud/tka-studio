<script lang="ts">
  import { createMotionTesterState } from "../../../routes/motion-tester/state/motion-tester-state.svelte";
  import PictographVisualizationPanel from "../../../routes/motion-tester/PictographVisualizationPanel.svelte";

  // Initialize the motion tester state
  const state = createMotionTesterState();

  console.log("🎯 MotionTesterTab rendered!");
</script>

<div class="motion-tester-tab">
  <header class="tester-header">
    <h1>🎯 Motion Tester</h1>
    <p>Test individual motion sequences with visual feedback and debugging</p>
  </header>

  <main class="tester-main">
    <PictographVisualizationPanel {state} />
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
