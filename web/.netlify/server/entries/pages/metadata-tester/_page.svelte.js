import { b as attr, e as escape_html, i as ensure_array_like, c as attr_class, f as stringify, p as pop, a as push, h as head } from "../../../chunks/index.js";
import "clsx";
import { P as PngMetadataExtractor } from "../../../chunks/png-metadata-extractor.js";
function ThumbnailBrowser($$payload, $$props) {
  push();
  let { state } = $$props;
  $$payload.out.push(`<div class="thumbnail-browser svelte-gpwe4v"><div class="browser-header svelte-gpwe4v"><h2 class="svelte-gpwe4v">📁 Available Sequences</h2> <div class="header-actions svelte-gpwe4v"><button class="batch-analyze-btn svelte-gpwe4v"${attr("disabled", state.state.isLoadingThumbnails || state.state.isBatchAnalyzing || state.state.thumbnails.length === 0, true)}>`);
  if (state.state.isBatchAnalyzing) {
    $$payload.out.push("<!--[-->");
    $$payload.out.push(`⏳ Analyzing...`);
  } else {
    $$payload.out.push("<!--[!-->");
    $$payload.out.push(`🔍 Batch Analyze`);
  }
  $$payload.out.push(`<!--]--></button> <button class="refresh-btn svelte-gpwe4v"${attr("disabled", state.state.isLoadingThumbnails, true)}>${escape_html(state.state.isLoadingThumbnails ? "🔄" : "↻")} Refresh</button></div></div> <div class="thumbnail-grid-container svelte-gpwe4v">`);
  if (state.state.isLoadingThumbnails) {
    $$payload.out.push("<!--[-->");
    $$payload.out.push(`<div class="loading-state svelte-gpwe4v"><div class="spinner svelte-gpwe4v"></div> <p class="svelte-gpwe4v">Loading thumbnails...</p></div>`);
  } else {
    $$payload.out.push("<!--[!-->");
    if (state.state.error) {
      $$payload.out.push("<!--[-->");
      $$payload.out.push(`<div class="error-state svelte-gpwe4v"><p class="svelte-gpwe4v">❌ ${escape_html(state.state.error)}</p> <button class="retry-btn svelte-gpwe4v">Retry</button></div>`);
    } else {
      $$payload.out.push("<!--[!-->");
      if (state.state.thumbnails.length === 0) {
        $$payload.out.push("<!--[-->");
        $$payload.out.push(`<div class="empty-state svelte-gpwe4v"><p class="svelte-gpwe4v">📭 No thumbnails found</p> <p class="help-text svelte-gpwe4v">Make sure PNG files are available in the static directories</p></div>`);
      } else {
        $$payload.out.push("<!--[!-->");
        const each_array = ensure_array_like(state.state.thumbnails);
        $$payload.out.push(`<div class="thumbnail-grid svelte-gpwe4v"><!--[-->`);
        for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
          let thumbnail = each_array[$$index];
          $$payload.out.push(`<button${attr_class("thumbnail-card svelte-gpwe4v", void 0, {
            "selected": state.state.selectedThumbnail?.path === thumbnail.path
          })}${attr("aria-label", `Select ${stringify(thumbnail.word)} sequence for metadata extraction`)}><div class="thumbnail-image svelte-gpwe4v"><img${attr("src", thumbnail.path)}${attr("alt", thumbnail.name)} loading="lazy" class="svelte-gpwe4v"/></div> <div class="thumbnail-info svelte-gpwe4v"><h3 class="sequence-name svelte-gpwe4v">${escape_html(thumbnail.word)}</h3> <p class="file-name svelte-gpwe4v">${escape_html(thumbnail.name)}</p></div></button>`);
        }
        $$payload.out.push(`<!--]--></div>`);
      }
      $$payload.out.push(`<!--]-->`);
    }
    $$payload.out.push(`<!--]-->`);
  }
  $$payload.out.push(`<!--]--></div> `);
  if (state.state.selectedThumbnail) {
    $$payload.out.push("<!--[-->");
    $$payload.out.push(`<div class="selection-info svelte-gpwe4v"><p class="svelte-gpwe4v">📌 Selected: <strong class="svelte-gpwe4v">${escape_html(state.state.selectedThumbnail.word)}</strong></p> <button class="clear-btn svelte-gpwe4v">Clear Selection</button></div>`);
  } else {
    $$payload.out.push("<!--[!-->");
  }
  $$payload.out.push(`<!--]--></div>`);
  pop();
}
function LoadingStates($$payload, $$props) {
  let { type, message, subtitle } = $$props;
  const defaultMessages = {
    batch: "Running batch analysis on all sequences...",
    extraction: "Extracting metadata...",
    general: "Loading..."
  };
  const defaultSubtitles = { batch: "This may take a moment", extraction: "", general: "" };
  $$payload.out.push(`<div class="loading-state svelte-9yc6sw"><div class="spinner svelte-9yc6sw"></div> <p class="svelte-9yc6sw">${escape_html(message || defaultMessages[type])}</p> `);
  if (subtitle || defaultSubtitles[type]) {
    $$payload.out.push("<!--[-->");
    $$payload.out.push(`<p class="loading-subtext svelte-9yc6sw">${escape_html(subtitle || defaultSubtitles[type])}</p>`);
  } else {
    $$payload.out.push("<!--[!-->");
  }
  $$payload.out.push(`<!--]--></div>`);
}
function EmptyState($$payload, $$props) {
  let {
    title = "🎯 Select a Sequence",
    message = 'Click on a thumbnail to extract and analyze its metadata, or use "Batch Analyze" to analyze all sequences'
  } = $$props;
  $$payload.out.push(`<div class="empty-state svelte-1ovg56q"><h3 class="svelte-1ovg56q">${escape_html(title)}</h3> <p class="svelte-1ovg56q">${escape_html(message)}</p></div>`);
}
function ErrorState($$payload, $$props) {
  let { error, title = "❌ Extraction Error" } = $$props;
  $$payload.out.push(`<div class="error-state svelte-dwllb9"><h3 class="svelte-dwllb9">${escape_html(title)}</h3> <p class="svelte-dwllb9">${escape_html(error)}</p></div>`);
}
function SequenceRankings($$payload, $$props) {
  let { bestSequences, worstSequences } = $$props;
  function getScoreClass(score) {
    return `score-${Math.floor(score / 20)}`;
  }
  const each_array = ensure_array_like(worstSequences);
  const each_array_1 = ensure_array_like(bestSequences);
  $$payload.out.push(`<div class="sequence-rankings svelte-sn8s07"><div class="worst-sequences svelte-sn8s07"><h4 class="svelte-sn8s07">❌ Worst Health Scores</h4> <ul class="ranking-list svelte-sn8s07"><!--[-->`);
  for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
    let sequence = each_array[$$index];
    $$payload.out.push(`<li class="ranking-item svelte-sn8s07"><span class="sequence-name svelte-sn8s07">${escape_html(sequence.sequence)}</span> <span${attr_class(`health-score ${stringify(getScoreClass(sequence.healthScore))}`, "svelte-sn8s07")}>${escape_html(sequence.healthScore)}%</span></li>`);
  }
  $$payload.out.push(`<!--]--></ul></div> <div class="best-sequences svelte-sn8s07"><h4 class="svelte-sn8s07">✅ Best Health Scores</h4> <ul class="ranking-list svelte-sn8s07"><!--[-->`);
  for (let $$index_1 = 0, $$length = each_array_1.length; $$index_1 < $$length; $$index_1++) {
    let sequence = each_array_1[$$index_1];
    $$payload.out.push(`<li class="ranking-item svelte-sn8s07"><span class="sequence-name svelte-sn8s07">${escape_html(sequence.sequence)}</span> <span${attr_class(`health-score ${stringify(getScoreClass(sequence.healthScore))}`, "svelte-sn8s07")}>${escape_html(sequence.healthScore)}%</span></li>`);
  }
  $$payload.out.push(`<!--]--></ul></div></div>`);
}
function BatchSummaryDisplay($$payload, $$props) {
  push();
  let { batchSummary } = $$props;
  $$payload.out.push(`<div class="batch-summary svelte-k16y93"><h3 class="svelte-k16y93">📊 Batch Analysis Summary</h3> <div class="summary-grid svelte-k16y93"><div class="summary-card svelte-k16y93"><div class="summary-title svelte-k16y93">Sequences Analyzed</div> <div class="summary-value svelte-k16y93">${escape_html(batchSummary.sequencesAnalyzed)}</div></div> <div class="summary-card healthy svelte-k16y93"><div class="summary-title svelte-k16y93">Healthy Sequences</div> <div class="summary-value svelte-k16y93">${escape_html(batchSummary.healthySequences)}</div> <div class="summary-subtitle svelte-k16y93">(${escape_html(Math.round(batchSummary.healthySequences / batchSummary.sequencesAnalyzed * 100))}%)</div></div> <div class="summary-card unhealthy svelte-k16y93"><div class="summary-title svelte-k16y93">Unhealthy Sequences</div> <div class="summary-value svelte-k16y93">${escape_html(batchSummary.unhealthySequences)}</div> <div class="summary-subtitle svelte-k16y93">(${escape_html(Math.round(batchSummary.unhealthySequences / batchSummary.sequencesAnalyzed * 100))}%)</div></div> <div class="summary-card svelte-k16y93"><div class="summary-title svelte-k16y93">Average Health Score</div> <div class="summary-value svelte-k16y93">${escape_html(batchSummary.averageHealthScore)}%</div></div></div> <div class="summary-sections svelte-k16y93">`);
  if (batchSummary.totalErrors > 0) {
    $$payload.out.push("<!--[-->");
    const each_array = ensure_array_like(batchSummary.commonErrors);
    $$payload.out.push(`<div class="error-summary svelte-k16y93"><h4 class="svelte-k16y93">🚨 Most Common Errors (${escape_html(batchSummary.totalErrors)} total)</h4> <ul class="issue-list svelte-k16y93"><!--[-->`);
    for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
      let [error, count] = each_array[$$index];
      $$payload.out.push(`<li class="error-item svelte-k16y93"><span class="error-text svelte-k16y93">${escape_html(error)}</span> <span class="error-count svelte-k16y93">${escape_html(count)} sequences</span></li>`);
    }
    $$payload.out.push(`<!--]--></ul></div>`);
  } else {
    $$payload.out.push("<!--[!-->");
  }
  $$payload.out.push(`<!--]--> `);
  if (batchSummary.totalWarnings > 0) {
    $$payload.out.push("<!--[-->");
    const each_array_1 = ensure_array_like(batchSummary.commonWarnings);
    $$payload.out.push(`<div class="warning-summary svelte-k16y93"><h4 class="svelte-k16y93">⚠️ Most Common Warnings (${escape_html(batchSummary.totalWarnings)} total)</h4> <ul class="issue-list svelte-k16y93"><!--[-->`);
    for (let $$index_1 = 0, $$length = each_array_1.length; $$index_1 < $$length; $$index_1++) {
      let [warning, count] = each_array_1[$$index_1];
      $$payload.out.push(`<li class="warning-item svelte-k16y93"><span class="warning-text svelte-k16y93">${escape_html(warning)}</span> <span class="warning-count svelte-k16y93">${escape_html(count)} sequences</span></li>`);
    }
    $$payload.out.push(`<!--]--></ul></div>`);
  } else {
    $$payload.out.push("<!--[!-->");
  }
  $$payload.out.push(`<!--]--> `);
  SequenceRankings($$payload, {
    bestSequences: batchSummary.bestSequences,
    worstSequences: batchSummary.worstSequences
  });
  $$payload.out.push(`<!----></div></div>`);
  pop();
}
function HealthScoreCard($$payload, $$props) {
  let { healthScore, errorCount, warningCount } = $$props;
  const scoreClass = () => {
    if (healthScore >= 90) return "excellent";
    if (healthScore >= 70) return "good";
    if (healthScore >= 50) return "warning";
    return "poor";
  };
  const scoreText = () => {
    if (healthScore >= 90) return "✅ Excellent metadata quality";
    if (healthScore >= 70) return "✅ Good metadata quality";
    if (healthScore >= 50) return "⚠️ Some issues found";
    return "❌ Significant issues detected";
  };
  $$payload.out.push(`<div${attr_class(`health-score ${stringify(scoreClass)}`, "svelte-176bym1")}><div class="score-circle svelte-176bym1"><span class="score-value svelte-176bym1">${escape_html(healthScore)}</span> <span class="score-label svelte-176bym1">Health</span></div> <div class="score-details svelte-176bym1"><p class="score-text svelte-176bym1">${escape_html(scoreText)}</p> <p class="issue-count svelte-176bym1">${escape_html(errorCount)} errors, ${escape_html(warningCount)} warnings</p></div></div>`);
}
function SummaryStatsGrid($$payload, $$props) {
  push();
  let { stats } = $$props;
  $$payload.out.push(`<div class="stats-grid svelte-8pry3d"><div class="stat-item svelte-8pry3d"><span class="stat-label svelte-8pry3d">Real Beats:</span> <span class="stat-value svelte-8pry3d">${escape_html(stats.realBeatsCount)}</span></div> <div class="stat-item svelte-8pry3d"><span class="stat-label svelte-8pry3d">Total Length:</span> <span class="stat-value svelte-8pry3d">${escape_html(stats.sequenceLength)}</span></div> <div class="stat-item svelte-8pry3d"><span class="stat-label svelte-8pry3d">Start Positions:</span> <span class="stat-value svelte-8pry3d">${escape_html(stats.startPositionCount)}</span></div> <div class="stat-item svelte-8pry3d"><span class="stat-label svelte-8pry3d">Author:</span> <span${attr_class("stat-value svelte-8pry3d", void 0, { "error": stats.authorMissing })}>${escape_html(stats.hasAuthor ? stats.authorName : "❌ Missing")}</span></div> <div class="stat-item svelte-8pry3d"><span class="stat-label svelte-8pry3d">Level:</span> <span${attr_class("stat-value svelte-8pry3d", void 0, { "error": stats.levelMissing || stats.levelZero })}>${escape_html(stats.hasLevel ? stats.levelZero ? "⚠️ 0 (needs calculation)" : stats.level : "❌ Missing")}</span></div> <div class="stat-item svelte-8pry3d"><span class="stat-label svelte-8pry3d">Start Position:</span> <span${attr_class("stat-value svelte-8pry3d", void 0, { "error": stats.startPositionMissing })}>${escape_html(stats.hasStartPosition ? `✅ ${stats.startPositionValue}` : "❌ Missing")}</span></div></div>`);
  pop();
}
function IssuesPanel($$payload, $$props) {
  push();
  let { stats } = $$props;
  if (stats.hasErrors || stats.hasWarnings) {
    $$payload.out.push("<!--[-->");
    $$payload.out.push(`<div class="issues-section svelte-wqkdq8"><h3 class="svelte-wqkdq8">🚨 Issues Found</h3> `);
    if (stats.hasErrors) {
      $$payload.out.push("<!--[-->");
      $$payload.out.push(`<div class="errors-panel svelte-wqkdq8"><h4 class="svelte-wqkdq8">❌ Critical Errors (${escape_html(stats.errorCount)})</h4> <ul class="issue-list svelte-wqkdq8">`);
      if (stats.authorMissing) {
        $$payload.out.push("<!--[-->");
        $$payload.out.push(`<li class="error-item svelte-wqkdq8">Missing author information - required for Browse tab filtering</li>`);
      } else {
        $$payload.out.push("<!--[!-->");
      }
      $$payload.out.push(`<!--]--> `);
      if (stats.levelMissing) {
        $$payload.out.push("<!--[-->");
        $$payload.out.push(`<li class="error-item svelte-wqkdq8">Missing difficulty level - affects sequence sorting</li>`);
      } else {
        $$payload.out.push("<!--[!-->");
      }
      $$payload.out.push(`<!--]--> `);
      if (stats.levelZero) {
        $$payload.out.push("<!--[-->");
        $$payload.out.push(`<li class="error-item svelte-wqkdq8">Level is 0 - indicates difficulty calculation needed</li>`);
      } else {
        $$payload.out.push("<!--[!-->");
      }
      $$payload.out.push(`<!--]--> `);
      if (stats.startPositionMissing) {
        $$payload.out.push("<!--[-->");
        $$payload.out.push(`<li class="error-item svelte-wqkdq8">Missing start position - affects sequence validation</li>`);
      } else {
        $$payload.out.push("<!--[!-->");
      }
      $$payload.out.push(`<!--]--> `);
      if (stats.missingLetters.length > 0) {
        $$payload.out.push("<!--[-->");
        $$payload.out.push(`<li class="error-item svelte-wqkdq8">Missing beat letters in beats: ${escape_html(stats.missingLetters.join(", "))}</li>`);
      } else {
        $$payload.out.push("<!--[!-->");
      }
      $$payload.out.push(`<!--]--> `);
      if (stats.missingMotionData.length > 0) {
        $$payload.out.push("<!--[-->");
        $$payload.out.push(`<li class="error-item svelte-wqkdq8">Missing motion data in beats: ${escape_html(stats.missingMotionData.join(", "))}</li>`);
      } else {
        $$payload.out.push("<!--[!-->");
      }
      $$payload.out.push(`<!--]--> `);
      if (stats.missingRequiredFields.length > 0) {
        $$payload.out.push("<!--[-->");
        $$payload.out.push(`<li class="error-item svelte-wqkdq8">Missing required fields (${escape_html(stats.missingRequiredFields.length)} instances)</li>`);
      } else {
        $$payload.out.push("<!--[!-->");
      }
      $$payload.out.push(`<!--]--></ul></div>`);
    } else {
      $$payload.out.push("<!--[!-->");
    }
    $$payload.out.push(`<!--]--> `);
    if (stats.hasWarnings) {
      $$payload.out.push("<!--[-->");
      $$payload.out.push(`<div class="warnings-panel svelte-wqkdq8"><h4 class="svelte-wqkdq8">⚠️ Warnings (${escape_html(stats.warningCount)})</h4> <ul class="issue-list svelte-wqkdq8">`);
      if (stats.authorInconsistent) {
        $$payload.out.push("<!--[-->");
        $$payload.out.push(`<li class="warning-item svelte-wqkdq8">Author information is inconsistent across beats</li>`);
      } else {
        $$payload.out.push("<!--[!-->");
      }
      $$payload.out.push(`<!--]--> `);
      if (stats.levelInconsistent) {
        $$payload.out.push("<!--[-->");
        $$payload.out.push(`<li class="warning-item svelte-wqkdq8">Level information is inconsistent across beats</li>`);
      } else {
        $$payload.out.push("<!--[!-->");
      }
      $$payload.out.push(`<!--]--> `);
      if (stats.startPositionInconsistent) {
        $$payload.out.push("<!--[-->");
        $$payload.out.push(`<li class="warning-item svelte-wqkdq8">Multiple different start positions found</li>`);
      } else {
        $$payload.out.push("<!--[!-->");
      }
      $$payload.out.push(`<!--]--> `);
      if (stats.duplicateBeats.length > 0) {
        $$payload.out.push("<!--[-->");
        $$payload.out.push(`<li class="warning-item svelte-wqkdq8">Duplicate beat numbers detected: ${escape_html(stats.duplicateBeats.join(", "))}</li>`);
      } else {
        $$payload.out.push("<!--[!-->");
      }
      $$payload.out.push(`<!--]--> `);
      if (stats.invalidMotionTypes.length > 0) {
        $$payload.out.push("<!--[-->");
        $$payload.out.push(`<li class="warning-item svelte-wqkdq8">${escape_html(stats.invalidMotionTypes.length)} invalid motion types found</li>`);
      } else {
        $$payload.out.push("<!--[!-->");
      }
      $$payload.out.push(`<!--]--></ul></div>`);
    } else {
      $$payload.out.push("<!--[!-->");
    }
    $$payload.out.push(`<!--]--></div>`);
  } else {
    $$payload.out.push("<!--[!-->");
    $$payload.out.push(`<div class="success-panel svelte-wqkdq8"><h3 class="svelte-wqkdq8">✅ All Checks Passed</h3> <p class="svelte-wqkdq8">This sequence has excellent metadata quality with no detected issues!</p></div>`);
  }
  $$payload.out.push(`<!--]-->`);
  pop();
}
function BeatAnalysisGrid($$payload, $$props) {
  push();
  let { beats, title = "🎵 Beat Analysis" } = $$props;
  function isStartPosition(beat) {
    return !!beat.sequence_start_position;
  }
  function getRealBeats(metadata) {
    if (!Array.isArray(metadata)) return [];
    return metadata.filter((beat) => beat.letter && !beat.sequence_start_position);
  }
  if (beats && Array.isArray(beats)) {
    $$payload.out.push("<!--[-->");
    const each_array = ensure_array_like(beats);
    $$payload.out.push(`<div class="beat-analysis svelte-ec6uhj"><h3 class="svelte-ec6uhj">${escape_html(title)}</h3> <div class="beats-container svelte-ec6uhj"><!--[-->`);
    for (let index = 0, $$length = each_array.length; index < $$length; index++) {
      let beat = each_array[index];
      $$payload.out.push(`<div${attr_class("beat-item svelte-ec6uhj", void 0, { "start-position": isStartPosition(beat) })}>`);
      if (isStartPosition(beat)) {
        $$payload.out.push("<!--[-->");
        $$payload.out.push(`<div class="beat-header start-pos svelte-ec6uhj"><span class="beat-type svelte-ec6uhj">Start Position</span> <span class="position-value svelte-ec6uhj">${escape_html(beat.sequence_start_position)}</span></div>`);
      } else {
        $$payload.out.push("<!--[!-->");
        $$payload.out.push(`<div class="beat-header svelte-ec6uhj"><span class="beat-number svelte-ec6uhj">Beat ${escape_html(getRealBeats(beats).indexOf(beat) + 1)}</span> <span class="beat-letter svelte-ec6uhj">${escape_html(beat.letter)}</span></div> <div class="motion-info svelte-ec6uhj"><div class="motion-item blue svelte-ec6uhj"><span class="prop-label svelte-ec6uhj">🔵 Blue:</span> <span class="motion-type svelte-ec6uhj">${escape_html(beat.blue_attributes?.motion_type || "Unknown")}</span></div> <div class="motion-item red svelte-ec6uhj"><span class="prop-label svelte-ec6uhj">🔴 Red:</span> <span class="motion-type svelte-ec6uhj">${escape_html(beat.red_attributes?.motion_type || "Unknown")}</span></div></div>`);
      }
      $$payload.out.push(`<!--]--></div>`);
    }
    $$payload.out.push(`<!--]--></div></div>`);
  } else {
    $$payload.out.push("<!--[!-->");
  }
  $$payload.out.push(`<!--]-->`);
  pop();
}
function RawDataViewer($$payload, $$props) {
  let { rawData, title = "🔍 Raw JSON Data" } = $$props;
  $$payload.out.push(`<details class="raw-data svelte-91t7w6"><summary class="svelte-91t7w6">${escape_html(title)} <button class="copy-btn svelte-91t7w6" title="Copy raw data to clipboard">📋 Copy</button></summary> <pre class="json-content svelte-91t7w6">${escape_html(rawData)}</pre></details>`);
}
function IndividualSequenceDisplay($$payload, $$props) {
  push();
  let { stats, selectedThumbnail, extractedMetadata, rawMetadata } = $$props;
  $$payload.out.push(`<div class="individual-sequence svelte-ywl3yh"><div class="metadata-summary svelte-ywl3yh"><h3 class="svelte-ywl3yh">📈 Analysis for ${escape_html(selectedThumbnail?.word || "Unknown")}</h3> `);
  HealthScoreCard($$payload, {
    healthScore: stats.healthScore,
    errorCount: stats.errorCount,
    warningCount: stats.warningCount
  });
  $$payload.out.push(`<!----> `);
  SummaryStatsGrid($$payload, { stats });
  $$payload.out.push(`<!----></div> `);
  IssuesPanel($$payload, { stats });
  $$payload.out.push(`<!----> `);
  if (extractedMetadata && Array.isArray(extractedMetadata)) {
    $$payload.out.push("<!--[-->");
    BeatAnalysisGrid($$payload, { beats: extractedMetadata });
  } else {
    $$payload.out.push("<!--[!-->");
  }
  $$payload.out.push(`<!--]--> `);
  if (rawMetadata) {
    $$payload.out.push("<!--[-->");
    RawDataViewer($$payload, { rawData: rawMetadata });
  } else {
    $$payload.out.push("<!--[!-->");
  }
  $$payload.out.push(`<!--]--></div>`);
  pop();
}
function MetadataDisplay($$payload, $$props) {
  push();
  let { state } = $$props;
  $$payload.out.push(`<div class="metadata-display svelte-r4q772"><div class="display-header svelte-r4q772"><h2 class="svelte-r4q772">📊 Metadata Analysis</h2> `);
  if (state.state.rawMetadata) {
    $$payload.out.push("<!--[-->");
    $$payload.out.push(`<button class="copy-btn svelte-r4q772" title="Copy raw metadata to clipboard">📋 Copy</button>`);
  } else {
    $$payload.out.push("<!--[!-->");
  }
  $$payload.out.push(`<!--]--></div> <div class="display-content svelte-r4q772">`);
  if (state.state.isBatchAnalyzing) {
    $$payload.out.push("<!--[-->");
    LoadingStates($$payload, { type: "batch" });
  } else {
    $$payload.out.push("<!--[!-->");
    if (state.state.isExtractingMetadata) {
      $$payload.out.push("<!--[-->");
      LoadingStates($$payload, { type: "extraction" });
    } else {
      $$payload.out.push("<!--[!-->");
      if (state.state.error) {
        $$payload.out.push("<!--[-->");
        ErrorState($$payload, { error: state.state.error });
      } else {
        $$payload.out.push("<!--[!-->");
        if (!state.state.selectedThumbnail && !state.state.metadataStats) {
          $$payload.out.push("<!--[-->");
          EmptyState($$payload, {});
        } else {
          $$payload.out.push("<!--[!-->");
          if (state.state.metadataStats) {
            $$payload.out.push("<!--[-->");
            if (state.state.metadataStats.isBatchSummary && state.state.metadataStats.batchSummary) {
              $$payload.out.push("<!--[-->");
              BatchSummaryDisplay($$payload, { batchSummary: state.state.metadataStats.batchSummary });
            } else {
              $$payload.out.push("<!--[!-->");
              IndividualSequenceDisplay($$payload, {
                stats: state.state.metadataStats,
                selectedThumbnail: state.state.selectedThumbnail,
                extractedMetadata: state.state.extractedMetadata,
                rawMetadata: state.state.rawMetadata
              });
            }
            $$payload.out.push(`<!--]-->`);
          } else {
            $$payload.out.push("<!--[!-->");
          }
          $$payload.out.push(`<!--]-->`);
        }
        $$payload.out.push(`<!--]-->`);
      }
      $$payload.out.push(`<!--]-->`);
    }
    $$payload.out.push(`<!--]-->`);
  }
  $$payload.out.push(`<!--]--></div></div>`);
  pop();
}
function createMetadataTesterState() {
  const state = {
    thumbnails: [],
    selectedThumbnail: null,
    extractedMetadata: null,
    rawMetadata: null,
    isLoadingThumbnails: false,
    isExtractingMetadata: false,
    isBatchAnalyzing: false,
    error: null,
    metadataStats: null
  };
  async function loadThumbnails() {
    state.isLoadingThumbnails = true;
    state.error = null;
    try {
      const thumbnails = [];
      try {
        const response = await fetch("/api/sequences");
        if (response.ok) {
          const data = await response.json();
          if (data.success && Array.isArray(data.sequences)) {
            const filteredSequences = data.sequences.filter((seq) => seq.word !== "A_A" && !seq.word.includes("_") && seq.word.length > 0);
            state.thumbnails = filteredSequences;
            console.log(`✅ Loaded ${filteredSequences.length} sequences from API (${data.sequences.length - filteredSequences.length} filtered out)`);
            return;
          }
        }
      } catch {
        console.log("📡 API not available, using manual discovery...");
      }
      const knownSequences = [
        "ABC",
        "A",
        "CAKE",
        "ALPHA",
        "EPSILON",
        "ETA",
        "MU",
        "B",
        "C",
        "DJ",
        "DJII",
        "DKIIEJII",
        "EJ",
        "EK",
        "FJ",
        "FL",
        "FLII",
        "G",
        "H",
        "I",
        "JD",
        "JGG",
        "KE",
        "LF",
        "MOON",
        "MP",
        "NQ",
        "OR",
        "OT",
        "PQV",
        "QT",
        "RT",
        "S",
        "T",
        "U",
        "V",
        "POSSUM",
        "OPOSSUM",
        "OPPOSSUM"
      ];
      const validSequences = knownSequences.filter((seq) => !seq.includes("_") && // Exclude sequences with underscores (test sequences)
      seq !== "A_A" && // Specifically exclude A_A
      seq.length > 0);
      let foundCount = 0;
      for (const sequenceName of validSequences) {
        const filePath = `/dictionary/${sequenceName}/${sequenceName}_ver1.png`;
        try {
          const response = await fetch(filePath, { method: "HEAD" });
          if (response.ok) {
            thumbnails.push({
              name: `${sequenceName}_ver1.png`,
              path: filePath,
              word: sequenceName
            });
            foundCount++;
            console.log(`✅ Found: ${sequenceName}`);
          } else {
            console.log(`❌ Not found: ${sequenceName} (${response.status})`);
          }
        } catch (error) {
          console.log(`❌ Error checking ${sequenceName}:`, error);
        }
      }
      const staticThumbnails = [];
      for (const thumb of staticThumbnails) {
        try {
          const response = await fetch(thumb.path, { method: "HEAD" });
          if (response.ok) {
            thumbnails.push(thumb);
            foundCount++;
            console.log(`✅ Found thumbnail: ${thumb.word}`);
          }
        } catch {
          console.log(`❌ Thumbnail not found: ${thumb.word}`);
        }
      }
      thumbnails.sort((a, b) => a.word.localeCompare(b.word));
      state.thumbnails = thumbnails;
      console.log(`🎯 Total sequences loaded: ${foundCount}`);
      if (foundCount === 0) {
        state.error = "No sequence files found. Please check that PNG files exist in the dictionary directories.";
      }
    } catch (error) {
      state.error = `Failed to load thumbnails: ${error}`;
      console.error("❌ Error loading thumbnails:", error);
    } finally {
      state.isLoadingThumbnails = false;
    }
  }
  async function extractMetadata(thumbnail) {
    state.isExtractingMetadata = true;
    state.error = null;
    state.selectedThumbnail = thumbnail;
    try {
      const metadata = await PngMetadataExtractor.extractMetadata(thumbnail.path);
      const metadataArray = Array.isArray(metadata) ? metadata : [];
      state.extractedMetadata = metadataArray;
      state.rawMetadata = JSON.stringify(metadata, null, 2);
      analyzeMetadata(metadataArray);
    } catch (error) {
      state.error = `Failed to extract metadata: ${error}`;
      state.extractedMetadata = null;
      state.rawMetadata = null;
      state.metadataStats = null;
      console.error("Error extracting metadata:", error);
    } finally {
      state.isExtractingMetadata = false;
    }
  }
  function analyzeMetadata(metadata) {
    if (!metadata || !Array.isArray(metadata)) {
      state.metadataStats = null;
      return;
    }
    console.log("🔍 Starting deep metadata analysis...");
    const startPositionEntries = metadata.filter((step) => step.sequence_start_position);
    const realBeats = metadata.filter((step) => step.letter && !step.sequence_start_position);
    const totalBeats = realBeats.length;
    const sequenceLength = metadata.length;
    const realBeatsCount = realBeats.length;
    const startPositionCount = startPositionEntries.length;
    const firstStep = metadata[0] || {};
    const hasAuthor = !!firstStep.author;
    const authorName = firstStep.author || null;
    const authorMissing = !hasAuthor;
    const authorsFound = new Set(metadata.map((step) => step.author).filter(Boolean));
    const authorInconsistent = authorsFound.size > 1;
    const hasLevel = !!firstStep.level;
    const level = firstStep.level || null;
    const levelMissing = !hasLevel;
    const levelZero = level === 0;
    const levelsFound = new Set(metadata.map((step) => step.level).filter((l) => l !== void 0 && l !== null));
    const levelInconsistent = levelsFound.size > 1;
    const hasStartPosition = startPositionCount > 0;
    const startPositionMissing = !hasStartPosition;
    const startPositionValue = startPositionEntries[0]?.sequence_start_position || null;
    const startPositionsFound = new Set(startPositionEntries.map((step) => step.sequence_start_position));
    const startPositionInconsistent = startPositionsFound.size > 1;
    const missingBeatNumbers = [];
    const missingLetters = [];
    const missingMotionData = [];
    const invalidMotionTypes = [];
    const duplicateBeats = [];
    const invalidBeatStructure = [];
    const missingRequiredFields = [];
    const validMotionTypes = [
      "pro",
      "anti",
      "static",
      "float",
      "dash",
      "bi_static",
      "shift",
      "kinetic_shift"
    ];
    const seenBeatNumbers = /* @__PURE__ */ new Set();
    realBeats.forEach((beat, index) => {
      const beatNumber = index + 1;
      if (!beat.letter) {
        missingLetters.push(beatNumber);
      }
      if (beat.beat_number !== void 0) {
        if (seenBeatNumbers.has(beat.beat_number)) {
          duplicateBeats.push(beatNumber);
        }
        seenBeatNumbers.add(beat.beat_number);
      }
      if (!beat.blue_attributes && !beat.red_attributes) {
        missingMotionData.push(beatNumber);
      } else {
        if (beat.blue_attributes) {
          const blueMotion = beat.blue_attributes.motion_type;
          if (!blueMotion) {
            missingRequiredFields.push({ beat: beatNumber, field: "blue_attributes.motion_type" });
          } else if (!validMotionTypes.includes(blueMotion)) {
            invalidMotionTypes.push({ beat: beatNumber, prop: "blue", type: blueMotion });
          }
        }
        if (beat.red_attributes) {
          const redMotion = beat.red_attributes.motion_type;
          if (!redMotion) {
            missingRequiredFields.push({ beat: beatNumber, field: "red_attributes.motion_type" });
          } else if (!validMotionTypes.includes(redMotion)) {
            invalidMotionTypes.push({ beat: beatNumber, prop: "red", type: redMotion });
          }
        }
      }
      if (!beat.letter && !beat.blue_attributes && !beat.red_attributes) {
        invalidBeatStructure.push(beatNumber);
      }
    });
    let errorCount = 0;
    let warningCount = 0;
    if (authorMissing) errorCount++;
    if (levelMissing) errorCount++;
    if (startPositionMissing) errorCount++;
    if (levelZero) errorCount++;
    errorCount += missingBeatNumbers.length;
    errorCount += missingLetters.length;
    errorCount += missingMotionData.length;
    errorCount += invalidBeatStructure.length;
    errorCount += missingRequiredFields.length;
    if (authorInconsistent) warningCount++;
    if (levelInconsistent) warningCount++;
    if (startPositionInconsistent) warningCount++;
    warningCount += duplicateBeats.length;
    warningCount += invalidMotionTypes.length;
    const hasErrors = errorCount > 0;
    const hasWarnings = warningCount > 0;
    const maxPossibleIssues = 10;
    const totalIssues = errorCount + warningCount * 0.5;
    const healthScore = Math.max(0, Math.round((1 - totalIssues / maxPossibleIssues) * 100));
    const errors = [];
    const warnings = [];
    if (authorMissing) errors.push("Missing author");
    if (levelMissing) errors.push("Missing level");
    if (startPositionMissing) errors.push("Missing start position");
    if (missingLetters.length > 0) errors.push(`Missing letters in ${missingLetters.length} beats`);
    if (missingMotionData.length > 0) errors.push(`Missing motion data in ${missingMotionData.length} beats`);
    if (invalidMotionTypes.length > 0) errors.push(`Invalid motion types in ${invalidMotionTypes.length} beats`);
    if (duplicateBeats.length > 0) errors.push(`Duplicate beats found: ${duplicateBeats.length}`);
    if (invalidBeatStructure.length > 0) errors.push(`Invalid beat structure in ${invalidBeatStructure.length} beats`);
    if (authorInconsistent) warnings.push("Author inconsistent across beats");
    if (levelInconsistent) warnings.push("Level inconsistent across beats");
    if (levelZero) warnings.push("Level is zero (may be invalid)");
    if (startPositionInconsistent) warnings.push("Start position inconsistent");
    if (missingRequiredFields.length > 0) warnings.push(`Missing required fields in ${missingRequiredFields.length} beats`);
    if (realBeatsCount !== sequenceLength && sequenceLength > 0) warnings.push("Beat count mismatch with sequence length");
    state.metadataStats = {
      // Basic counts
      totalBeats,
      sequenceLength,
      realBeatsCount,
      startPositionCount,
      // Author validation
      hasAuthor,
      authorName,
      authorMissing,
      authorInconsistent,
      // Level validation
      hasLevel,
      level,
      levelMissing,
      levelInconsistent,
      levelZero,
      // Start position validation
      hasStartPosition,
      startPositionMissing,
      startPositionInconsistent,
      startPositionValue,
      // Beat validation
      missingBeatNumbers,
      missingLetters,
      missingMotionData,
      invalidMotionTypes,
      // Data integrity issues
      duplicateBeats,
      invalidBeatStructure,
      missingRequiredFields,
      // Overall health
      hasErrors,
      hasWarnings,
      errorCount,
      warningCount,
      healthScore,
      // Error and warning details for batch analysis
      errors,
      warnings
    };
    console.log("📊 Metadata Analysis Results:");
    console.log(`   Health Score: ${healthScore}/100`);
    console.log(`   Errors: ${errorCount}, Warnings: ${warningCount}`);
    console.log(`   Author: ${authorName || "MISSING"}`);
    console.log(`   Level: ${level !== null ? level : "MISSING"}`);
    console.log(`   Start Position: ${startPositionValue || "MISSING"}`);
    console.log(`   Beats: ${totalBeats}, Sequence Length: ${sequenceLength}`);
    if (hasErrors || hasWarnings) {
      console.log("⚠️ Issues found:");
      if (authorMissing) console.log("   - Missing author");
      if (levelMissing) console.log("   - Missing level");
      if (startPositionMissing) console.log("   - Missing start position");
      if (missingLetters.length) console.log(`   - Missing letters in beats: ${missingLetters.join(", ")}`);
      if (missingMotionData.length) console.log(`   - Missing motion data in beats: ${missingMotionData.join(", ")}`);
      if (invalidMotionTypes.length) console.log(`   - Invalid motion types: ${invalidMotionTypes.length} found`);
    }
  }
  async function handleBatchAnalyze() {
    console.log("Starting batch metadata analysis...");
    state.isBatchAnalyzing = true;
    state.error = null;
    try {
      let analyzed = 0;
      let totalErrors = 0;
      let totalWarnings = 0;
      let healthySequences = 0;
      let totalHealthScore = 0;
      const sequenceResults = {};
      const errorPatterns = {};
      const warningPatterns = {};
      for (const thumbnail of state.thumbnails) {
        console.log(`Analyzing sequence: ${thumbnail.word}`);
        await extractMetadata(thumbnail);
        if (state.extractedMetadata) {
          analyzeMetadata(state.extractedMetadata);
        }
        if (state.metadataStats) {
          const errorCount = state.metadataStats.errors?.length || 0;
          const warningCount = state.metadataStats.warnings?.length || 0;
          sequenceResults[thumbnail.word] = {
            healthScore: state.metadataStats.healthScore,
            errorCount,
            warningCount,
            isHealthy: state.metadataStats.healthScore >= 80,
            errors: state.metadataStats.errors || [],
            warnings: state.metadataStats.warnings || []
          };
          totalErrors += errorCount;
          totalWarnings += warningCount;
          totalHealthScore += state.metadataStats.healthScore;
          if (state.metadataStats.healthScore >= 80) healthySequences++;
          if (state.metadataStats.errors) {
            state.metadataStats.errors.forEach((error) => {
              errorPatterns[error] = (errorPatterns[error] || 0) + 1;
            });
          }
          if (state.metadataStats.warnings) {
            state.metadataStats.warnings.forEach((warning) => {
              warningPatterns[warning] = (warningPatterns[warning] || 0) + 1;
            });
          }
        }
        analyzed++;
      }
      const averageHealth = totalHealthScore / analyzed;
      const batchSummary = {
        sequencesAnalyzed: analyzed,
        healthySequences,
        unhealthySequences: analyzed - healthySequences,
        averageHealthScore: Math.round(averageHealth * 10) / 10,
        totalErrors,
        totalWarnings,
        commonErrors: Object.entries(errorPatterns).sort((a, b) => b[1] - a[1]).slice(0, 5),
        commonWarnings: Object.entries(warningPatterns).sort((a, b) => b[1] - a[1]).slice(0, 5),
        worstSequences: Object.entries(sequenceResults).sort((a, b) => a[1].healthScore - b[1].healthScore).slice(0, 5).map(([seq, data]) => ({ sequence: seq, healthScore: data.healthScore })),
        bestSequences: Object.entries(sequenceResults).sort((a, b) => b[1].healthScore - a[1].healthScore).slice(0, 5).map(([seq, data]) => ({ sequence: seq, healthScore: data.healthScore }))
      };
      state.selectedThumbnail = null;
      state.metadataStats = {
        // Copy existing structure with defaults
        totalBeats: 0,
        sequenceLength: 0,
        realBeatsCount: 0,
        startPositionCount: 0,
        hasAuthor: false,
        authorName: null,
        authorMissing: true,
        authorInconsistent: false,
        hasLevel: false,
        level: null,
        levelMissing: true,
        levelInconsistent: false,
        levelZero: false,
        hasStartPosition: false,
        startPositionMissing: true,
        startPositionInconsistent: false,
        startPositionValue: null,
        missingBeatNumbers: [],
        missingLetters: [],
        missingMotionData: [],
        invalidMotionTypes: [],
        duplicateBeats: [],
        invalidBeatStructure: [],
        missingRequiredFields: [],
        hasErrors: totalErrors > 0,
        hasWarnings: totalWarnings > 0,
        errorCount: totalErrors,
        warningCount: totalWarnings,
        healthScore: averageHealth,
        errors: Object.keys(errorPatterns),
        warnings: Object.keys(warningPatterns),
        isBatchSummary: true,
        batchSummary
      };
      console.log(`Batch Analysis Complete:`);
      console.log(`- Sequences Analyzed: ${analyzed}`);
      console.log(`- Healthy Sequences (80+ score): ${healthySequences} (${Math.round(healthySequences / analyzed * 100)}%)`);
      console.log(`- Unhealthy Sequences: ${analyzed - healthySequences} (${Math.round((analyzed - healthySequences) / analyzed * 100)}%)`);
      console.log(`- Average Health Score: ${averageHealth.toFixed(1)}%`);
      console.log(`- Total Errors: ${totalErrors}`);
      console.log(`- Total Warnings: ${totalWarnings}`);
      console.log(`- Most Common Errors:`, batchSummary.commonErrors);
      console.log(`- Most Common Warnings:`, batchSummary.commonWarnings);
      console.log("Batch summary created:", batchSummary);
    } catch (error) {
      console.error("Batch analysis failed:", error);
      state.error = `Batch analysis failed: ${error}`;
    } finally {
      state.isBatchAnalyzing = false;
    }
  }
  function clearSelection() {
    state.selectedThumbnail = null;
    state.extractedMetadata = null;
    state.rawMetadata = null;
    state.metadataStats = null;
    state.error = null;
  }
  loadThumbnails();
  return {
    get state() {
      return state;
    },
    loadThumbnails,
    extractMetadata,
    clearSelection,
    analyzeMetadata,
    handleBatchAnalyze
  };
}
function MetadataTesterInterface($$payload, $$props) {
  push();
  const state = createMetadataTesterState();
  $$payload.out.push(`<div class="metadata-tester-container svelte-149nq2f"><header class="tester-header svelte-149nq2f"><h1 class="svelte-149nq2f">🔍 TKA Metadata Tester</h1> <p class="svelte-149nq2f">Test and validate PNG metadata extraction for sequence files</p></header> <main class="tester-main svelte-149nq2f"><div class="panel thumbnail-browser svelte-149nq2f">`);
  ThumbnailBrowser($$payload, { state });
  $$payload.out.push(`<!----></div> <div class="panel metadata-display svelte-149nq2f">`);
  MetadataDisplay($$payload, { state });
  $$payload.out.push(`<!----></div></main></div>`);
  pop();
}
function _page($$payload) {
  head($$payload, ($$payload2) => {
    $$payload2.title = `<title>TKA Metadata Tester - PNG Metadata Validation</title>`;
  });
  MetadataTesterInterface($$payload);
}
export {
  _page as default
};
