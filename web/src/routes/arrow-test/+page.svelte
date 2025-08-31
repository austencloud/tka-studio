<!--
Arrow Mirroring Test Route - Simple test for arrow positioning
-->
<script lang="ts">
  import type { PictographData } from "$domain";
  import {
    createMotionData,
    createPictographData,
    GridPosition,
    Letter,
    Orientation,
    RotationDirection,
  } from "$domain";
  import { Location, MotionColor, MotionType } from "$domain/enums";
  import Pictograph from "$lib/components/core/pictograph/Pictograph.svelte";
  import { onMount } from "svelte";

  // Test state
  let ccwPictograph = $state<PictographData | null>(null);
  let cwPictograph = $state<PictographData | null>(null);
  let measurements = $state<any>({});
  let isLoading = $state(true);
  let error = $state<string | null>(null);

  // Create test pictographs from CSV data
  function createTestPictographs() {
    try {
      // CCW test case: A,alpha1,alpha7,split,same,pro,ccw,s,e,pro,ccw,n,w
      const ccw = createPictographData({
        letter: Letter.A, // Use unified Letter enum
        startPosition: GridPosition.ALPHA1,
        endPosition: GridPosition.ALPHA7,
        motions: {
          blue: createMotionData({
            motionType: MotionType.PRO,
            rotationDirection: RotationDirection.COUNTER_CLOCKWISE,
            startLocation: Location.SOUTH,
            endLocation: Location.EAST,
            startOrientation: Orientation.IN,
            endOrientation: Orientation.OUT,
            turns: 1,
            color: MotionColor.BLUE,
          }),
          red: createMotionData({
            motionType: MotionType.PRO,
            rotationDirection: RotationDirection.COUNTER_CLOCKWISE,
            startLocation: Location.NORTH,
            endLocation: Location.WEST,
            startOrientation: Orientation.IN,
            endOrientation: Orientation.OUT,
            turns: 1,
            color: MotionColor.RED,
          }),
        },
      });

      // CW test case: A,alpha1,alpha3,split,same,pro,cw,s,w,pro,cw,n,e
      const cw = createPictographData({
        letter: Letter.A, // Use unified Letter enum
        startPosition: GridPosition.ALPHA1,
        endPosition: GridPosition.ALPHA3,

        motions: {
          blue: createMotionData({
            motionType: MotionType.PRO,
            rotationDirection: RotationDirection.CLOCKWISE,
            startLocation: Location.SOUTH,
            endLocation: Location.WEST,
            startOrientation: Orientation.IN,
            endOrientation: Orientation.OUT,
            turns: 1,
            color: MotionColor.BLUE,
          }),
          red: createMotionData({
            motionType: MotionType.PRO,
            rotationDirection: RotationDirection.CLOCKWISE,
            startLocation: Location.NORTH,
            endLocation: Location.EAST,
            startOrientation: Orientation.IN,
            endOrientation: Orientation.OUT,
            turns: 1,
            color: MotionColor.RED,
          }),
        },
      });

      return { ccw, cw };
    } catch (err) {
      console.error("Error creating test pictographs:", err);
      throw err;
    }
  }

  // Measure arrow positions
  async function measurePositions() {
    await new Promise((resolve) => setTimeout(resolve, 1000)); // Wait for render

    const results: any = {};

    // Measure CCW test
    const ccwSvg = document.querySelector('[data-test="ccw"] svg');
    if (ccwSvg) {
      const blueArrow = ccwSvg.querySelector(".blue-arrow-svg");
      const redArrow = ccwSvg.querySelector(".red-arrow-svg");

      results.ccw = {
        blue: measureArrow(blueArrow),
        red: measureArrow(redArrow),
        expected: "mirrored",
      };
    }

    // Measure CW test
    const cwSvg = document.querySelector('[data-test="cw"] svg');
    if (cwSvg) {
      const blueArrow = cwSvg.querySelector(".blue-arrow-svg");
      const redArrow = cwSvg.querySelector(".red-arrow-svg");

      results.cw = {
        blue: measureArrow(blueArrow),
        red: measureArrow(redArrow),
        expected: "not mirrored",
      };
    }

    return results;
  }

  function measureArrow(element: Element | null) {
    if (!element) return { error: "Arrow not found" };

    const rect = element.getBoundingClientRect();
    const transform = element.getAttribute("transform") || "";
    const isMirrored =
      transform.includes("scale(-1") || element.classList.contains("mirrored");

    return {
      x: Math.round(rect.left + rect.width / 2),
      y: Math.round(rect.top + rect.height / 2),
      width: Math.round(rect.width),
      height: Math.round(rect.height),
      transform: transform,
      isMirrored: isMirrored,
    };
  }

  async function runTest() {
    try {
      isLoading = true;
      error = null;

      // Create test data
      const { ccw, cw } = createTestPictographs();

      // For now, just use the pictographs as-is since we're testing arrow rendering
      ccwPictograph = ccw;
      cwPictograph = cw;

      // Wait for render and measure
      setTimeout(async () => {
        try {
          measurements = await measurePositions();
          isLoading = false;
        } catch (err) {
          error = `Measurement error: ${err}`;
          isLoading = false;
        }
      }, 1500);
    } catch (err) {
      error = `Test error: ${err}`;
      isLoading = false;
    }
  }

  onMount(() => {
    runTest();
  });
</script>

<svelte:head>
  <title>Arrow Mirroring Test</title>
</svelte:head>

<div class="test-page">
  <h1>Arrow Mirroring Position Test</h1>
  <p>Testing the svgData.viewBox.width offset fix for arrow mirroring</p>

  {#if isLoading}
    <div class="loading">
      <div class="spinner"></div>
      <p>Loading test pictographs...</p>
    </div>
  {:else if error}
    <div class="error">
      <h2>Error</h2>
      <p>{error}</p>
      <button onclick={() => runTest()}>Retry</button>
    </div>
  {:else}
    <div class="test-grid">
      <!-- CCW Test -->
      <div class="test-case">
        <h2>CCW Test (Should be Mirrored)</h2>
        <p><code>A,alpha1,alpha7,split,same,pro,ccw,s,e,pro,ccw,n,w</code></p>

        {#if ccwPictograph}
          <div class="pictograph-wrapper" data-test="ccw">
            <Pictograph pictographData={ccwPictograph} />
          </div>
        {/if}

        {#if measurements.ccw}
          <div class="measurements">
            <h3>Measurements</h3>
            <div class="measurement">
              <strong>Blue Arrow:</strong>
              <span
                >Position: ({measurements.ccw.blue.x}, {measurements.ccw.blue
                  .y})</span
              >
              <span
                >Mirrored: {measurements.ccw.blue.isMirrored
                  ? "✅ Yes"
                  : "❌ No"}</span
              >
            </div>
            <div class="measurement">
              <strong>Red Arrow:</strong>
              <span
                >Position: ({measurements.ccw.red.x}, {measurements.ccw.red
                  .y})</span
              >
              <span
                >Mirrored: {measurements.ccw.red.isMirrored
                  ? "✅ Yes"
                  : "❌ No"}</span
              >
            </div>
            <div class="result">
              <strong>Expected:</strong>
              {measurements.ccw.expected}
            </div>
          </div>
        {/if}
      </div>

      <!-- CW Test -->
      <div class="test-case">
        <h2>CW Test (Should NOT be Mirrored)</h2>
        <p><code>A,alpha1,alpha3,split,same,pro,cw,s,w,pro,cw,n,e</code></p>

        {#if cwPictograph}
          <div class="pictograph-wrapper" data-test="cw">
            <Pictograph pictographData={cwPictograph} />
          </div>
        {/if}

        {#if measurements.cw}
          <div class="measurements">
            <h3>Measurements</h3>
            <div class="measurement">
              <strong>Blue Arrow:</strong>
              <span
                >Position: ({measurements.cw.blue.x}, {measurements.cw.blue
                  .y})</span
              >
              <span
                >Mirrored: {measurements.cw.blue.isMirrored
                  ? "❌ Yes"
                  : "✅ No"}</span
              >
            </div>
            <div class="measurement">
              <strong>Red Arrow:</strong>
              <span
                >Position: ({measurements.cw.red.x}, {measurements.cw.red
                  .y})</span
              >
              <span
                >Mirrored: {measurements.cw.red.isMirrored
                  ? "❌ Yes"
                  : "✅ No"}</span
              >
            </div>
            <div class="result">
              <strong>Expected:</strong>
              {measurements.cw.expected}
            </div>
          </div>
        {/if}
      </div>
    </div>

    <div class="actions">
      <button onclick={() => runTest()}>Re-run Test</button>
      <button onclick={() => console.log("Measurements:", measurements)}
        >Log to Console</button
      >
    </div>
  {/if}
</div>

<style>
  .test-page {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    font-family: system-ui, sans-serif;
  }

  h1 {
    color: #2563eb;
    text-align: center;
  }

  .loading {
    text-align: center;
    padding: 3rem;
  }

  .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f4f6;
    border-top: 4px solid #2563eb;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 1rem;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  .error {
    background: #fef2f2;
    border: 1px solid #fecaca;
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
  }

  .test-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin: 2rem 0;
  }

  .test-case {
    border: 2px solid #e5e7eb;
    border-radius: 12px;
    padding: 1.5rem;
    background: white;
  }

  .pictograph-wrapper {
    display: flex;
    justify-content: center;
    margin: 1rem 0;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 1rem;
  }

  .measurements {
    background: #f9fafb;
    border-radius: 8px;
    padding: 1rem;
    margin-top: 1rem;
  }

  .measurement {
    display: grid;
    gap: 0.25rem;
    margin-bottom: 0.5rem;
    font-size: 0.875rem;
  }

  .result {
    border-top: 1px solid #e5e7eb;
    padding-top: 0.5rem;
    margin-top: 0.5rem;
    font-weight: bold;
  }

  .actions {
    text-align: center;
    margin-top: 2rem;
    gap: 1rem;
    display: flex;
    justify-content: center;
  }

  button {
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 0.75rem 1.5rem;
    cursor: pointer;
    font-weight: 500;
  }

  button:hover {
    background: #1d4ed8;
  }

  code {
    background: #f3f4f6;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.875rem;
  }
</style>
