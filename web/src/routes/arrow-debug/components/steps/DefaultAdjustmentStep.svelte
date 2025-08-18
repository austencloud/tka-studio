<script lang="ts">
  import type { ArrowDebugState } from "../../state/arrow-debug-state.svelte";
  import {
    getStepStatus,
    isStepVisible,
  } from "../../utils/debug-step-utils.js";
  import { formatPoint } from "../../utils/debug-formatting.js";
  import DebugSection from "../shared/DebugSection.svelte";

  interface Props {
    state: ArrowDebugState;
  }

  let { state }: Props = $props();

  const stepNumber = 3;
  const stepStatus = $derived(getStepStatus(stepNumber, state.currentStep));
  const isVisible = $derived(isStepVisible(stepNumber, state));
</script>

{#if isVisible}
  <DebugSection
    sectionId="default_adjustment"
    title="⚙️ Step 3: Default Adjustment"
    {state}
    {stepNumber}
    {stepStatus}
  >
    {#snippet children()}
      {#if state.currentDebugData.defaultAdjustmentDebugInfo}
        <div class="adjustment-info">
          <h4>⚙️ Default Adjustment Details</h4>
          <div class="debug-grid">
            <div class="debug-item">
              <span class="label">Placement Key:</span>
              <span class="value">
                {state.currentDebugData.defaultAdjustmentDebugInfo.placementKey}
              </span>
            </div>
            <div class="debug-item">
              <span class="label">Motion Type:</span>
              <span class="value">
                {state.currentDebugData.defaultAdjustmentDebugInfo.motionType}
              </span>
            </div>
            <div class="debug-item">
              <span class="label">Grid Mode:</span>
              <span class="value">
                {state.currentDebugData.defaultAdjustmentDebugInfo.gridMode}
              </span>
            </div>
            <div class="debug-item">
              <span class="label">Adjustment Source:</span>
              <span class="value">
                {state.currentDebugData.defaultAdjustmentDebugInfo
                  .adjustmentSource}
              </span>
            </div>
          </div>
        </div>
      {/if}

      <div class="result-box">
        <span class="result-label">After Default Adjustment:</span>
        <span class="result-value">
          {formatPoint(state.currentDebugData.defaultAdjustment) ||
            "Not calculated"}
        </span>
      </div>

      {#if state.currentDebugData.timing?.stepDurations.defaultAdjustment}
        <div class="timing-info">
          Time: {state.currentDebugData.timing.stepDurations.defaultAdjustment.toFixed(
            2
          )}ms
        </div>
      {/if}
    {/snippet}
  </DebugSection>
{/if}

<style>
  .adjustment-info h4 {
    margin: 0 0 10px 0;
    color: #a78bfa;
    font-size: 0.9rem;
    border-bottom: 1px solid rgba(167, 139, 250, 0.2);
    padding-bottom: 6px;
  }

  .debug-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 12px;
  }

  .debug-item {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .label {
    color: #94a3b8;
    font-size: 0.85rem;
    font-weight: 500;
  }

  .value {
    color: #e2e8f0;
    font-family: "Courier New", monospace;
    font-size: 0.9rem;
  }

  .result-box {
    background: rgba(168, 85, 247, 0.1);
    border: 1px solid rgba(168, 85, 247, 0.3);
    border-radius: 6px;
    padding: 12px;
    margin: 12px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .result-label {
    color: #a78bfa;
    font-weight: 600;
    font-size: 0.9rem;
  }

  .result-value {
    color: #c4b5fd;
    font-family: "Courier New", monospace;
    font-size: 1rem;
    font-weight: 600;
  }

  .timing-info {
    color: #94a3b8;
    font-size: 0.8rem;
    text-align: right;
    margin-top: 8px;
    font-style: italic;
  }

  @media (max-width: 640px) {
    .debug-grid {
      grid-template-columns: 1fr;
    }

    .result-box {
      flex-direction: column;
      gap: 8px;
      text-align: center;
    }
  }
</style>
