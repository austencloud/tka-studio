<!-- Metadata Display Component -->
<script lang="ts">
  import type { MetadataTesterState } from "../state/metadata-tester-state.svelte";

  interface Props {
    state: {
      state: MetadataTesterState;
    };
  }

  let { state }: Props = $props();

  // Format beat information for display
  function formatBeatInfo(beat: any, index: number): string {
    if (!beat) return "Invalid beat data";

    const beatNumber = index + 1;
    const letter = beat.letter || "Unknown";
    const blueMotion = beat.blue_attributes?.motion_type || "Unknown";
    const redMotion = beat.red_attributes?.motion_type || "Unknown";

    return `Beat ${beatNumber} (${letter}): Blue=${blueMotion}, Red=${redMotion}`;
  }

  // Check if beat is start position
  function isStartPosition(beat: any): boolean {
    return !!beat.sequence_start_position;
  }

  // Get filtered real beats (no start position entries)
  function getRealBeats(metadata: any[]): any[] {
    if (!Array.isArray(metadata)) return [];
    return metadata.filter(
      (beat) => beat.letter && !beat.sequence_start_position
    );
  }

  // Copy metadata to clipboard
  async function copyToClipboard() {
    if (!state.state.rawMetadata) return;

    try {
      await navigator.clipboard.writeText(state.state.rawMetadata);
      // You might want to show a toast notification here
    } catch (error) {
      console.error("Failed to copy to clipboard:", error);
    }
  }
</script>

<div class="metadata-display">
  <div class="display-header">
    <h2>📊 Metadata Analysis</h2>
    {#if state.state.rawMetadata}
      <button
        class="copy-btn"
        onclick={copyToClipboard}
        title="Copy raw metadata to clipboard"
      >
        📋 Copy
      </button>
    {/if}
  </div>

  <div class="display-content">
    {#if state.state.isBatchAnalyzing}
      <div class="loading-state">
        <div class="spinner"></div>
        <p>Running batch analysis on all sequences...</p>
        <p class="loading-subtext">This may take a moment</p>
      </div>
    {:else if state.state.isExtractingMetadata}
      <div class="loading-state">
        <div class="spinner"></div>
        <p>Extracting metadata...</p>
      </div>
    {:else if state.state.error}
      <div class="error-state">
        <h3>❌ Extraction Error</h3>
        <p>{state.state.error}</p>
      </div>
    {:else if !state.state.selectedThumbnail && !state.state.metadataStats}
      <div class="empty-state">
        <h3>🎯 Select a Sequence</h3>
        <p>
          Click on a thumbnail to extract and analyze its metadata, or use
          "Batch Analyze" to analyze all sequences
        </p>
      </div>
    {:else if state.state.metadataStats}
      <!-- Check if this is a batch summary -->
      {#if state.state.metadataStats.isBatchSummary && state.state.metadataStats.batchSummary}
        <!-- Batch Summary Display -->
        <div class="batch-summary">
          <h3>📊 Batch Analysis Summary</h3>

          <div class="summary-grid">
            <div class="summary-card">
              <div class="summary-title">Sequences Analyzed</div>
              <div class="summary-value">
                {state.state.metadataStats.batchSummary.sequencesAnalyzed}
              </div>
            </div>

            <div class="summary-card healthy">
              <div class="summary-title">Healthy Sequences</div>
              <div class="summary-value">
                {state.state.metadataStats.batchSummary.healthySequences}
              </div>
              <div class="summary-subtitle">
                ({Math.round(
                  (state.state.metadataStats.batchSummary.healthySequences /
                    state.state.metadataStats.batchSummary.sequencesAnalyzed) *
                    100
                )}%)
              </div>
            </div>

            <div class="summary-card unhealthy">
              <div class="summary-title">Unhealthy Sequences</div>
              <div class="summary-value">
                {state.state.metadataStats.batchSummary.unhealthySequences}
              </div>
              <div class="summary-subtitle">
                ({Math.round(
                  (state.state.metadataStats.batchSummary.unhealthySequences /
                    state.state.metadataStats.batchSummary.sequencesAnalyzed) *
                    100
                )}%)
              </div>
            </div>

            <div class="summary-card">
              <div class="summary-title">Average Health Score</div>
              <div class="summary-value">
                {state.state.metadataStats.batchSummary.averageHealthScore}%
              </div>
            </div>
          </div>

          <div class="summary-sections">
            <!-- Error Summary -->
            {#if state.state.metadataStats.batchSummary.totalErrors > 0}
              <div class="error-summary">
                <h4>
                  🚨 Most Common Errors ({state.state.metadataStats.batchSummary
                    .totalErrors} total)
                </h4>
                <ul class="issue-list">
                  {#each state.state.metadataStats.batchSummary.commonErrors as [error, count]}
                    <li class="error-item">
                      <span class="error-text">{error}</span>
                      <span class="error-count">{count} sequences</span>
                    </li>
                  {/each}
                </ul>
              </div>
            {/if}

            <!-- Warning Summary -->
            {#if state.state.metadataStats.batchSummary.totalWarnings > 0}
              <div class="warning-summary">
                <h4>
                  ⚠️ Most Common Warnings ({state.state.metadataStats
                    .batchSummary.totalWarnings} total)
                </h4>
                <ul class="issue-list">
                  {#each state.state.metadataStats.batchSummary.commonWarnings as [warning, count]}
                    <li class="warning-item">
                      <span class="warning-text">{warning}</span>
                      <span class="warning-count">{count} sequences</span>
                    </li>
                  {/each}
                </ul>
              </div>
            {/if}

            <!-- Best and Worst Sequences -->
            <div class="sequence-rankings">
              <div class="worst-sequences">
                <h4>❌ Worst Health Scores</h4>
                <ul class="ranking-list">
                  {#each state.state.metadataStats.batchSummary.worstSequences as sequence}
                    <li class="ranking-item">
                      <span class="sequence-name">{sequence.sequence}</span>
                      <span
                        class="health-score score-{Math.floor(
                          sequence.healthScore / 20
                        )}">{sequence.healthScore}%</span
                      >
                    </li>
                  {/each}
                </ul>
              </div>

              <div class="best-sequences">
                <h4>✅ Best Health Scores</h4>
                <ul class="ranking-list">
                  {#each state.state.metadataStats.batchSummary.bestSequences as sequence}
                    <li class="ranking-item">
                      <span class="sequence-name">{sequence.sequence}</span>
                      <span
                        class="health-score score-{Math.floor(
                          sequence.healthScore / 20
                        )}">{sequence.healthScore}%</span
                      >
                    </li>
                  {/each}
                </ul>
              </div>
            </div>
          </div>
        </div>
      {:else}
        <!-- Individual Sequence Display -->
        <div class="individual-sequence">
          <!-- Metadata Summary -->
          <div class="metadata-summary">
            <h3>
              📈 Analysis for {state.state.selectedThumbnail?.word || "Unknown"}
            </h3>

            <!-- Health Score -->
            <div
              class="health-score"
              class:excellent={state.state.metadataStats.healthScore >= 90}
              class:good={state.state.metadataStats.healthScore >= 70 &&
                state.state.metadataStats.healthScore < 90}
              class:warning={state.state.metadataStats.healthScore >= 50 &&
                state.state.metadataStats.healthScore < 70}
              class:poor={state.state.metadataStats.healthScore < 50}
            >
              <div class="score-circle">
                <span class="score-value"
                  >{state.state.metadataStats.healthScore}</span
                >
                <span class="score-label">Health</span>
              </div>
              <div class="score-details">
                <p class="score-text">
                  {#if state.state.metadataStats.healthScore >= 90}
                    ✅ Excellent metadata quality
                  {:else if state.state.metadataStats.healthScore >= 70}
                    ✅ Good metadata quality
                  {:else if state.state.metadataStats.healthScore >= 50}
                    ⚠️ Some issues found
                  {:else}
                    ❌ Significant issues detected
                  {/if}
                </p>
                <p class="issue-count">
                  {state.state.metadataStats.errorCount} errors, {state.state
                    .metadataStats.warningCount} warnings
                </p>
              </div>
            </div>

            <!-- Basic Stats -->
            <div class="stats-grid">
              <div class="stat-item">
                <span class="stat-label">Real Beats:</span>
                <span class="stat-value"
                  >{state.state.metadataStats.realBeatsCount}</span
                >
              </div>
              <div class="stat-item">
                <span class="stat-label">Total Length:</span>
                <span class="stat-value"
                  >{state.state.metadataStats.sequenceLength}</span
                >
              </div>
              <div class="stat-item">
                <span class="stat-label">Start Positions:</span>
                <span class="stat-value"
                  >{state.state.metadataStats.startPositionCount}</span
                >
              </div>
              <div class="stat-item">
                <span class="stat-label">Author:</span>
                <span
                  class="stat-value"
                  class:error={state.state.metadataStats.authorMissing}
                >
                  {state.state.metadataStats.hasAuthor
                    ? state.state.metadataStats.authorName
                    : "❌ Missing"}
                </span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Level:</span>
                <span
                  class="stat-value"
                  class:error={state.state.metadataStats.levelMissing ||
                    state.state.metadataStats.levelZero}
                >
                  {state.state.metadataStats.hasLevel
                    ? state.state.metadataStats.levelZero
                      ? "⚠️ 0 (needs calculation)"
                      : state.state.metadataStats.level
                    : "❌ Missing"}
                </span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Start Position:</span>
                <span
                  class="stat-value"
                  class:error={state.state.metadataStats.startPositionMissing}
                >
                  {state.state.metadataStats.hasStartPosition
                    ? `✅ ${state.state.metadataStats.startPositionValue}`
                    : "❌ Missing"}
                </span>
              </div>
            </div>
          </div>

          <!-- Issues & Warnings -->
          {#if state.state.metadataStats.hasErrors || state.state.metadataStats.hasWarnings}
            <div class="issues-section">
              <h3>🚨 Issues Found</h3>

              {#if state.state.metadataStats.hasErrors}
                <div class="errors-panel">
                  <h4>
                    ❌ Critical Errors ({state.state.metadataStats.errorCount})
                  </h4>
                  <ul class="issue-list">
                    {#if state.state.metadataStats.authorMissing}
                      <li class="error-item">
                        Missing author information - required for Browse tab
                        filtering
                      </li>
                    {/if}
                    {#if state.state.metadataStats.levelMissing}
                      <li class="error-item">
                        Missing difficulty level - affects sequence sorting
                      </li>
                    {/if}
                    {#if state.state.metadataStats.levelZero}
                      <li class="error-item">
                        Level is 0 - indicates difficulty calculation needed
                      </li>
                    {/if}
                    {#if state.state.metadataStats.startPositionMissing}
                      <li class="error-item">
                        Missing start position - affects sequence validation
                      </li>
                    {/if}
                    {#if state.state.metadataStats.missingLetters.length > 0}
                      <li class="error-item">
                        Missing beat letters in beats: {state.state.metadataStats.missingLetters.join(
                          ", "
                        )}
                      </li>
                    {/if}
                    {#if state.state.metadataStats.missingMotionData.length > 0}
                      <li class="error-item">
                        Missing motion data in beats: {state.state.metadataStats.missingMotionData.join(
                          ", "
                        )}
                      </li>
                    {/if}
                    {#if state.state.metadataStats.missingRequiredFields.length > 0}
                      <li class="error-item">
                        Missing required fields ({state.state.metadataStats
                          .missingRequiredFields.length} instances)
                      </li>
                    {/if}
                  </ul>
                </div>
              {/if}

              {#if state.state.metadataStats.hasWarnings}
                <div class="warnings-panel">
                  <h4>
                    ⚠️ Warnings ({state.state.metadataStats.warningCount})
                  </h4>
                  <ul class="issue-list">
                    {#if state.state.metadataStats.authorInconsistent}
                      <li class="warning-item">
                        Author information is inconsistent across beats
                      </li>
                    {/if}
                    {#if state.state.metadataStats.levelInconsistent}
                      <li class="warning-item">
                        Level information is inconsistent across beats
                      </li>
                    {/if}
                    {#if state.state.metadataStats.startPositionInconsistent}
                      <li class="warning-item">
                        Multiple different start positions found
                      </li>
                    {/if}
                    {#if state.state.metadataStats.duplicateBeats.length > 0}
                      <li class="warning-item">
                        Duplicate beat numbers detected: {state.state.metadataStats.duplicateBeats.join(
                          ", "
                        )}
                      </li>
                    {/if}
                    {#if state.state.metadataStats.invalidMotionTypes.length > 0}
                      <li class="warning-item">
                        {state.state.metadataStats.invalidMotionTypes.length} invalid
                        motion types found
                      </li>
                    {/if}
                  </ul>
                </div>
              {/if}
            </div>
          {:else}
            <div class="success-panel">
              <h3>✅ All Checks Passed</h3>
              <p>
                This sequence has excellent metadata quality with no detected
                issues!
              </p>
            </div>
          {/if}

          <!-- Beat-by-Beat Analysis -->
          {#if state.state.extractedMetadata && Array.isArray(state.state.extractedMetadata)}
            <div class="beat-analysis">
              <h3>🎵 Beat Analysis</h3>
              <div class="beats-container">
                {#each state.state.extractedMetadata as beat, index}
                  <div
                    class="beat-item"
                    class:start-position={isStartPosition(beat)}
                  >
                    {#if isStartPosition(beat)}
                      <div class="beat-header start-pos">
                        <span class="beat-type">Start Position</span>
                        <span class="position-value"
                          >{beat.sequence_start_position}</span
                        >
                      </div>
                    {:else}
                      <div class="beat-header">
                        <span class="beat-number"
                          >Beat {getRealBeats(
                            state.state.extractedMetadata
                          ).indexOf(beat) + 1}</span
                        >
                        <span class="beat-letter">{beat.letter}</span>
                      </div>
                      <div class="motion-info">
                        <div class="motion-item blue">
                          <span class="prop-label">🔵 Blue:</span>
                          <span class="motion-type"
                            >{beat.blue_attributes?.motion_type ||
                              "Unknown"}</span
                          >
                        </div>
                        <div class="motion-item red">
                          <span class="prop-label">🔴 Red:</span>
                          <span class="motion-type"
                            >{beat.red_attributes?.motion_type ||
                              "Unknown"}</span
                          >
                        </div>
                      </div>
                    {/if}
                  </div>
                {/each}
              </div>
            </div>
          {/if}

          <!-- Raw JSON Data (Collapsible) -->
          <details class="raw-data">
            <summary>🔍 Raw JSON Data</summary>
            <pre class="json-content">{state.state.rawMetadata}</pre>
          </details>
        </div>
      {/if}
    {/if}
  </div>
</div>

<style>
  .metadata-display {
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
  }

  .display-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .display-header h2 {
    margin: 0;
    font-size: 1.25rem;
    color: #22c55e;
  }

  .copy-btn {
    background: rgba(34, 197, 94, 0.2);
    border: 1px solid rgba(34, 197, 94, 0.4);
    color: #22c55e;
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: all 0.2s ease;
  }

  .copy-btn:hover {
    background: rgba(34, 197, 94, 0.3);
    border-color: rgba(34, 197, 94, 0.6);
  }

  .display-content {
    flex: 1;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
  }

  .display-content::-webkit-scrollbar {
    width: 8px;
  }

  .display-content::-webkit-scrollbar-track {
    background: transparent;
  }

  .display-content::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
  }

  .display-content::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.3);
  }

  .loading-state,
  .error-state,
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 300px;
    text-align: center;
  }

  .loading-state p,
  .error-state p,
  .empty-state p {
    margin: 8px 0 0 0;
    color: #9ca3af;
  }

  .loading-subtext {
    font-size: 0.9rem;
    color: #6b7280;
  }

  .spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-top: 3px solid #22c55e;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 15px;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  .metadata-summary {
    background: rgba(34, 197, 94, 0.1);
    border: 1px solid rgba(34, 197, 94, 0.2);
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
  }

  .metadata-summary h3 {
    margin: 0 0 15px 0;
    color: #22c55e;
    font-size: 1.1rem;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px;
  }

  .stat-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 6px;
  }

  .stat-label {
    font-weight: 500;
    opacity: 0.8;
  }

  .stat-value {
    font-weight: 600;
    color: #22c55e;
  }

  .stat-value.error {
    color: #f87171;
  }

  .health-score {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 20px;
    padding: 15px;
    border-radius: 8px;
    border: 2px solid;
  }

  .health-score.excellent {
    background: rgba(34, 197, 94, 0.1);
    border-color: rgba(34, 197, 94, 0.3);
  }

  .health-score.good {
    background: rgba(59, 130, 246, 0.1);
    border-color: rgba(59, 130, 246, 0.3);
  }

  .health-score.warning {
    background: rgba(251, 191, 36, 0.1);
    border-color: rgba(251, 191, 36, 0.3);
  }

  .health-score.poor {
    background: rgba(239, 68, 68, 0.1);
    border-color: rgba(239, 68, 68, 0.3);
  }

  .score-circle {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    border: 3px solid currentColor;
  }

  .score-value {
    font-size: 1.5rem;
    font-weight: 700;
    line-height: 1;
  }

  .score-label {
    font-size: 0.7rem;
    font-weight: 500;
    opacity: 0.8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .score-details {
    flex: 1;
  }

  .score-text {
    margin: 0 0 5px 0;
    font-weight: 600;
    font-size: 1.1rem;
  }

  .issue-count {
    margin: 0;
    font-size: 0.9rem;
    opacity: 0.8;
  }

  .issues-section {
    margin-bottom: 20px;
  }

  .issues-section h3 {
    margin: 0 0 15px 0;
    color: #f87171;
    font-size: 1.1rem;
  }

  .errors-panel,
  .warnings-panel {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.2);
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 15px;
  }

  .warnings-panel {
    background: rgba(251, 191, 36, 0.1);
    border-color: rgba(251, 191, 36, 0.2);
  }

  .errors-panel h4,
  .warnings-panel h4 {
    margin: 0 0 10px 0;
    font-size: 1rem;
  }

  .errors-panel h4 {
    color: #f87171;
  }

  .warnings-panel h4 {
    color: #fbbf24;
  }

  .issue-list {
    margin: 0;
    padding: 0;
    list-style: none;
  }

  .error-item,
  .warning-item {
    padding: 6px 0;
    font-size: 0.9rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .error-item:last-child,
  .warning-item:last-child {
    border-bottom: none;
  }

  .error-item {
    color: #fca5a5;
  }

  .warning-item {
    color: #fcd34d;
  }

  .success-panel {
    background: rgba(34, 197, 94, 0.1);
    border: 1px solid rgba(34, 197, 94, 0.2);
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    margin-bottom: 20px;
  }

  .success-panel h3 {
    margin: 0 0 10px 0;
    color: #22c55e;
    font-size: 1.1rem;
  }

  .success-panel p {
    margin: 0;
    opacity: 0.9;
  }

  .beat-analysis {
    margin-bottom: 20px;
  }

  .beat-analysis h3 {
    margin: 0 0 15px 0;
    color: #22c55e;
    font-size: 1.1rem;
  }

  .beats-container {
    display: grid;
    gap: 8px;
  }

  .beat-item {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 12px;
  }

  .beat-item.start-position {
    background: rgba(168, 85, 247, 0.1);
    border-color: rgba(168, 85, 247, 0.3);
  }

  .beat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }

  .beat-header.start-pos {
    margin-bottom: 0;
  }

  .beat-number {
    font-weight: 600;
    color: #60a5fa;
  }

  .beat-letter {
    font-weight: 600;
    color: #fbbf24;
    font-size: 1.1rem;
  }

  .beat-type {
    font-weight: 600;
    color: #a855f7;
  }

  .position-value {
    font-weight: 600;
    color: #c084fc;
  }

  .motion-info {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }

  .motion-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.9rem;
  }

  .motion-item.blue {
    background: rgba(59, 130, 246, 0.1);
  }

  .motion-item.red {
    background: rgba(239, 68, 68, 0.1);
  }

  .prop-label {
    font-weight: 500;
  }

  .motion-type {
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.8rem;
  }

  .raw-data {
    margin-top: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    overflow: hidden;
  }

  .raw-data summary {
    padding: 12px 16px;
    background: rgba(255, 255, 255, 0.05);
    cursor: pointer;
    font-weight: 500;
    color: #60a5fa;
    user-select: none;
  }

  .raw-data summary:hover {
    background: rgba(255, 255, 255, 0.1);
  }

  .json-content {
    padding: 16px;
    margin: 0;
    background: rgba(0, 0, 0, 0.2);
    font-family: "Courier New", monospace;
    font-size: 0.85rem;
    line-height: 1.4;
    white-space: pre-wrap;
    word-break: break-all;
    max-height: 400px;
    overflow-y: auto;
  }

  /* Batch Summary Styles */
  .batch-summary {
    background: rgba(29, 78, 216, 0.1);
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
  }

  .batch-summary h3 {
    color: #60a5fa;
    margin: 0 0 20px 0;
    font-size: 1.4rem;
  }

  .summary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
  }

  .summary-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 16px;
    text-align: center;
  }

  .summary-card.healthy {
    border-color: rgba(34, 197, 94, 0.4);
    background: rgba(34, 197, 94, 0.1);
  }

  .summary-card.unhealthy {
    border-color: rgba(239, 68, 68, 0.4);
    background: rgba(239, 68, 68, 0.1);
  }

  .summary-title {
    font-size: 0.9rem;
    color: #9ca3af;
    margin-bottom: 8px;
  }

  .summary-value {
    font-size: 2rem;
    font-weight: bold;
    color: #f9fafb;
    margin-bottom: 4px;
  }

  .summary-subtitle {
    font-size: 0.8rem;
    color: #9ca3af;
  }

  .summary-sections {
    display: grid;
    gap: 20px;
  }

  .error-summary,
  .warning-summary {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 8px;
    padding: 16px;
  }

  .warning-summary {
    background: rgba(245, 158, 11, 0.1);
    border-color: rgba(245, 158, 11, 0.3);
  }

  .error-summary h4,
  .warning-summary h4 {
    margin: 0 0 12px 0;
    color: #f9fafb;
  }

  .issue-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .error-item,
  .warning-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .error-item:last-child,
  .warning-item:last-child {
    border-bottom: none;
  }

  .error-text,
  .warning-text {
    color: #f9fafb;
  }

  .error-count,
  .warning-count {
    background: rgba(255, 255, 255, 0.1);
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    color: #9ca3af;
  }

  .sequence-rankings {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }

  .worst-sequences,
  .best-sequences {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 16px;
  }

  .worst-sequences h4,
  .best-sequences h4 {
    margin: 0 0 12px 0;
    color: #f9fafb;
  }

  .ranking-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .ranking-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .ranking-item:last-child {
    border-bottom: none;
  }

  .sequence-name {
    color: #f9fafb;
    font-family: monospace;
  }

  .health-score {
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 0.8rem;
  }

  .health-score.score-0,
  .health-score.score-1 {
    background: rgba(239, 68, 68, 0.2);
    color: #f87171;
  }

  .health-score.score-2 {
    background: rgba(245, 158, 11, 0.2);
    color: #fbbf24;
  }

  .health-score.score-3,
  .health-score.score-4 {
    background: rgba(34, 197, 94, 0.2);
    color: #4ade80;
  }

  /* Responsive design */
  @media (max-width: 768px) {
    .stats-grid {
      grid-template-columns: 1fr;
    }

    .motion-info {
      grid-template-columns: 1fr;
    }

    .display-header {
      flex-direction: column;
      gap: 10px;
      align-items: stretch;
    }
  }
</style>
