<!--
  Visual Test Component for AnimatedPictographDataService
  
  This component allows manual testing of the service by rendering
  pictographs with different motion parameters and comparing results.
-->

<script lang="ts">
  import { resolve } from "$lib/services/bootstrap";
  import { IAnimatedPictographDataServiceInterface } from "$lib/services/di/interfaces/motion-tester-interfaces";
  import Pictograph from "$lib/components/pictograph/Pictograph.svelte";
  import type { PictographData } from "$lib/domain";

  // Resolve service
  const pictographDataService = resolve(
    IAnimatedPictographDataServiceInterface
  );

  // Test configurations
  const testConfigs = [
    {
      name: "Basic Pro Motion",
      gridType: "diamond",
      blueMotionParams: {
        motionType: "pro",
        startLoc: "n",
        endLoc: "s",
        startOri: "in",
        endOri: "out",
        propRotDir: "cw",
        turns: 1,
      },
      redMotionParams: {
        motionType: "anti",
        startLoc: "e",
        endLoc: "w",
        startOri: "out",
        endOri: "in",
        propRotDir: "ccw",
        turns: 1,
      },
    },
    {
      name: "Float Motion",
      gridType: "box",
      blueMotionParams: {
        motionType: "float",
        startLoc: "ne",
        endLoc: "sw",
        startOri: "clock",
        endOri: "counter",
        propRotDir: "no_rot",
        turns: 0,
      },
      redMotionParams: {
        motionType: "float",
        startLoc: "nw",
        endLoc: "se",
        startOri: "counter",
        endOri: "clock",
        propRotDir: "no_rot",
        turns: 0,
      },
    },
    {
      name: "Dash Motion",
      gridType: "diamond",
      blueMotionParams: {
        motionType: "dash",
        startLoc: "n",
        endLoc: "n",
        startOri: "in",
        endOri: "in",
        propRotDir: "no_rot",
        turns: 0,
      },
      redMotionParams: {
        motionType: "dash",
        startLoc: "s",
        endLoc: "s",
        startOri: "out",
        endOri: "out",
        propRotDir: "no_rot",
        turns: 0,
      },
    },
    {
      name: "Static Motion",
      gridType: "box",
      blueMotionParams: {
        motionType: "static",
        startLoc: "w",
        endLoc: "w",
        startOri: "in",
        endOri: "in",
        propRotDir: "no_rot",
        turns: 0,
      },
      redMotionParams: {
        motionType: "static",
        startLoc: "e",
        endLoc: "e",
        startOri: "out",
        endOri: "out",
        propRotDir: "no_rot",
        turns: 0,
      },
    },
  ];

  // Generate pictograph data for each test config
  let testResults: Array<{
    config: (typeof testConfigs)[0];
    pictographData: PictographData | null;
    error?: string;
  }> = [];

  function runTests() {
    testResults = testConfigs.map((config) => {
      try {
        const mockState = {
          gridType: config.gridType,
          blueMotionParams: config.blueMotionParams,
          redMotionParams: config.redMotionParams,
          animationState: { progress: 0.5 },
        };

        const pictographData =
          pictographDataService.createAnimatedPictographData(mockState as any);

        return {
          config,
          pictographData,
          error: pictographData ? undefined : "Service returned null",
        };
      } catch (error) {
        return {
          config,
          pictographData: null,
          error: error instanceof Error ? error.message : "Unknown error",
        };
      }
    });
  }

  // Run tests on component mount
  runTests();

  function logPictographData(data: PictographData | null, configName: string) {
    console.log(`📊 Visual Test - ${configName}:`, data);
  }
</script>

<div class="visual-test-container">
  <h2>🧪 AnimatedPictographDataService Visual Tests</h2>

  <div class="test-controls">
    <button on:click={runTests} class="run-tests-btn"> 🔄 Re-run Tests </button>
  </div>

  <div class="test-results">
    {#each testResults as result, index}
      <div class="test-case">
        <h3>{result.config.name}</h3>

        <div class="test-info">
          <div class="config-details">
            <h4>Configuration:</h4>
            <ul>
              <li><strong>Grid:</strong> {result.config.gridType}</li>
              <li>
                <strong>Blue Motion:</strong>
                {result.config.blueMotionParams.motionType}
                ({result.config.blueMotionParams.startLoc} → {result.config
                  .blueMotionParams.endLoc})
              </li>
              <li>
                <strong>Red Motion:</strong>
                {result.config.redMotionParams.motionType}
                ({result.config.redMotionParams.startLoc} → {result.config
                  .redMotionParams.endLoc})
              </li>
            </ul>
          </div>

          <div class="pictograph-container">
            {#if result.error}
              <div class="error">
                ❌ Error: {result.error}
              </div>
            {:else if result.pictographData}
              <div class="pictograph-wrapper">
                <Pictograph
                  pictographData={result.pictographData}
                  width={200}
                  height={200}
                />
                <button
                  on:click={() =>
                    logPictographData(
                      result.pictographData,
                      result.config.name
                    )}
                  class="log-data-btn"
                >
                  📋 Log Data
                </button>
              </div>
            {:else}
              <div class="no-data">⚠️ No pictograph data generated</div>
            {/if}
          </div>
        </div>
      </div>
    {/each}
  </div>

  <div class="test-summary">
    <h3>📈 Test Summary</h3>
    <p>
      <strong>Total Tests:</strong>
      {testResults.length}<br />
      <strong>Passed:</strong>
      {testResults.filter((r) => r.pictographData && !r.error).length}<br />
      <strong>Failed:</strong>
      {testResults.filter((r) => r.error || !r.pictographData).length}
    </p>
  </div>
</div>

<style>
  .visual-test-container {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
  }

  .test-controls {
    margin-bottom: 20px;
  }

  .run-tests-btn {
    background: #4caf50;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
  }

  .run-tests-btn:hover {
    background: #45a049;
  }

  .test-results {
    display: grid;
    gap: 20px;
  }

  .test-case {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    background: #f9f9f9;
  }

  .test-case h3 {
    margin-top: 0;
    color: #333;
  }

  .test-info {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    align-items: start;
  }

  .config-details ul {
    list-style-type: none;
    padding: 0;
  }

  .config-details li {
    margin-bottom: 5px;
    padding: 5px;
    background: #fff;
    border-radius: 3px;
  }

  .pictograph-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
  }

  .pictograph-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
  }

  .log-data-btn {
    background: #2196f3;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 3px;
    cursor: pointer;
    font-size: 12px;
  }

  .log-data-btn:hover {
    background: #1976d2;
  }

  .error {
    color: #f44336;
    font-weight: bold;
    padding: 10px;
    background: #ffebee;
    border-radius: 5px;
  }

  .no-data {
    color: #ff9800;
    font-weight: bold;
    padding: 10px;
    background: #fff3e0;
    border-radius: 5px;
  }

  .test-summary {
    margin-top: 30px;
    padding: 20px;
    background: #e3f2fd;
    border-radius: 8px;
  }

  .test-summary h3 {
    margin-top: 0;
  }
</style>
