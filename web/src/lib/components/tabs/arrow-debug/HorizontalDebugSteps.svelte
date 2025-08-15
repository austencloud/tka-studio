<script lang="ts">
  /**
   * Horizontal Debug Steps Component
   * Shows debug steps as horizontal cards for better visibility
   */

  import type { DebugStepData } from "./types";

  interface Props {
    debugData: DebugStepData;
    currentStep: number;
    maxSteps: number;
    stepByStepMode: boolean;
    onStepChange: (step: number) => void;
  }

  let {
    debugData,
    currentStep,
    maxSteps,
    stepByStepMode,
    onStepChange,
  }: Props = $props();

  const stepNames = [
    "Input Data",
    "Location Calculation",
    "Coordinate System",
    "Rotation Calculation",
    "Adjustment Calculation",
  ];

  function getStepStatus(
    stepIndex: number
  ): "complete" | "current" | "pending" {
    if (stepByStepMode) {
      if (stepIndex < currentStep) return "complete";
      if (stepIndex === currentStep) return "current";
      return "pending";
    }
    // In non-step mode, show all as complete - always show all data
    return "complete";
  }

  function getStepData(stepIndex: number) {
    switch (stepIndex) {
      case 0: // Input Data
        return {
          title: "Input Data",
          data: {
            pictograph: debugData.pictographData?.letter || "None",
            motionType: debugData.motionData?.motion_type || "None",
            startOri: debugData.motionData?.start_ori || "None",
            endOri: debugData.motionData?.end_ori || "None",
            arrowColor: debugData.arrowData?.color || "None",
          },
        };
      case 1: // Location Calculation
        return {
          title: "Location Calculation",
          data: {
            location: debugData.calculatedLocation || "Not calculated",
            method:
              debugData.locationDebugInfo?.calculationMethod || "Standard",
            motionType: debugData.motionData?.motion_type || "Unknown",
          },
        };
      case 2: // Coordinate System
        return {
          title: "Coordinate System",
          data: {
            initialPosition: debugData.initialPosition
              ? `(${debugData.initialPosition.x.toFixed(1)}, ${debugData.initialPosition.y.toFixed(1)})`
              : "Not calculated",
            coordinateSet:
              debugData.coordinateSystemDebugInfo?.usedCoordinateSet ||
              "Default",
            systemType:
              debugData.coordinateSystemDebugInfo?.coordinateSystemType ||
              "Standard",
          },
        };
      case 3: // Rotation
        return {
          title: "Rotation Calculation",
          data: {
            rotation:
              debugData.finalRotation !== undefined
                ? `${debugData.finalRotation.toFixed(1)}°`
                : "Not calculated",
            location: debugData.calculatedLocation || "Not calculated",
          },
        };
      case 4: // Adjustments
        return {
          title: "Adjustment Calculation",
          data: {
            adjustment: debugData.defaultAdjustment
              ? `(${debugData.defaultAdjustment.x.toFixed(1)}, ${debugData.defaultAdjustment.y.toFixed(1)})`
              : "Not calculated",
            finalPosition: debugData.finalPosition
              ? `(${debugData.finalPosition.x.toFixed(1)}, ${debugData.finalPosition.y.toFixed(1)})`
              : "Not calculated",
          },
        };
      default:
        return { title: "Unknown", data: {} };
    }
  }
</script>

<div class="horizontal-debug-steps">
  <div class="steps-header">
    <h3>🔍 Debug Pipeline Steps</h3>
    {#if stepByStepMode}
      <div class="step-navigation">
        <button
          onclick={() => onStepChange(Math.max(0, currentStep - 1))}
          disabled={currentStep === 0}
          class="nav-btn"
        >
          ← Previous
        </button>
        <span class="step-counter"
          >Step {currentStep + 1} of {maxSteps + 1}</span
        >
        <button
          onclick={() => onStepChange(Math.min(maxSteps, currentStep + 1))}
          disabled={currentStep === maxSteps}
          class="nav-btn"
        >
          Next →
        </button>
      </div>
    {/if}
  </div>

  <div class="steps-container">
    {#each Array(5) as _, stepIndex}
      {@const stepData = getStepData(stepIndex)}
      {@const status = getStepStatus(stepIndex)}
      {#if stepByStepMode}
        <button
          class="step-card {status} clickable"
          onclick={() => onStepChange(stepIndex)}
        >
          <div class="step-header">
            <div class="step-number">{stepIndex + 1}</div>
            <h4>{stepData.title}</h4>
            <div class="step-status-indicator {status}"></div>
          </div>

          <div class="step-content">
            {#each Object.entries(stepData.data) as [key, value]}
              <div class="data-row">
                <span class="data-key">{key}:</span>
                <span class="data-value">{value}</span>
              </div>
            {/each}
          </div>
        </button>
      {:else}
        <div class="step-card {status}">
          <div class="step-header">
            <div class="step-number">{stepIndex + 1}</div>
            <h4>{stepData.title}</h4>
            <div class="step-status-indicator {status}"></div>
          </div>

          <div class="step-content">
            {#each Object.entries(stepData.data) as [key, value]}
              <div class="data-row">
                <span class="data-key">{key}:</span>
                <span class="data-value">{value}</span>
              </div>
            {/each}
          </div>
        </div>
      {/if}
    {/each}
  </div>

  {#if debugData.errors.length > 0}
    <div class="errors-section">
      <h4>⚠️ Errors</h4>
      <div class="errors-list">
        {#each debugData.errors as error}
          <div class="error-item">
            <span class="error-step">{error.step}:</span>
            <span class="error-message">{error.error}</span>
          </div>
        {/each}
      </div>
    </div>
  {/if}

  {#if debugData.timing}
    <div class="timing-section">
      <h4>⏱️ Performance</h4>
      <div class="timing-data">
        <span>Total: {debugData.timing.totalDuration.toFixed(2)}ms</span>
        {#each Object.entries(debugData.timing.stepDurations) as [step, duration]}
          <span>{step}: {duration.toFixed(2)}ms</span>
        {/each}
      </div>
    </div>
  {/if}
</div>

<style>
  .horizontal-debug-steps {
    display: flex;
    flex-direction: column;
    gap: 16px;
    width: 100%;
  }

  .steps-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }

  .steps-header h3 {
    color: #fbbf24;
    margin: 0;
    font-size: 1.1rem;
  }

  .step-navigation {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .nav-btn {
    padding: 6px 12px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 4px;
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 0.9rem;
  }

  .nav-btn:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.2);
  }

  .nav-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .step-counter {
    color: #c7d2fe;
    font-size: 0.9rem;
    font-weight: 500;
  }

  .steps-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px;
  }

  .step-card {
    background: rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 12px;
    transition: all 0.2s ease;
  }

  .step-card.clickable {
    cursor: pointer;
  }

  .step-card.clickable:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.3);
  }

  .step-card.current {
    border-color: #fbbf24;
    background: rgba(251, 191, 36, 0.1);
  }

  .step-card.complete {
    border-color: #10b981;
  }

  .step-card.pending {
    opacity: 0.6;
  }

  .step-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
  }

  .step-number {
    background: #3b82f6;
    color: white;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: 600;
  }

  .step-header h4 {
    color: white;
    margin: 0;
    font-size: 0.9rem;
    flex: 1;
  }

  .step-status-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
  }

  .step-status-indicator.complete {
    background: #10b981;
  }

  .step-status-indicator.current {
    background: #fbbf24;
  }

  .step-status-indicator.pending {
    background: #6b7280;
  }

  .step-content {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .data-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.8rem;
  }

  .data-key {
    color: #9ca3af;
    font-weight: 500;
  }

  .data-value {
    color: #c7d2fe;
    font-family: "Courier New", monospace;
    text-align: right;
  }

  .errors-section,
  .timing-section {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 12px;
  }

  .errors-section h4,
  .timing-section h4 {
    color: #fbbf24;
    margin: 0 0 8px 0;
    font-size: 0.9rem;
  }

  .errors-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .error-item {
    font-size: 0.8rem;
    color: #f87171;
  }

  .error-step {
    font-weight: 600;
  }

  .timing-data {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    font-size: 0.8rem;
    color: #c7d2fe;
    font-family: "Courier New", monospace;
  }
</style>
