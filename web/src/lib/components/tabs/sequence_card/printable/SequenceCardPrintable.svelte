<!-- SequenceCardPrintable.svelte - Print-optimized sequence card -->
<script lang="ts">
  import type { SequenceData } from "$services/interfaces/domain-types";

  // Props
  interface Props {
    sequence: SequenceData;
    width: number;
    height: number;
    scale?: number;
    showMetadata?: boolean;
    showBeatNumbers?: boolean;
    onclick?: () => void;
  }

  let {
    sequence,
    width,
    height,
    scale = 1,
    showMetadata = true,
    showBeatNumbers = true,
    onclick,
  }: Props = $props();

  // Derived properties optimized for print
  let sequenceName = $derived(sequence.name || "Untitled");
  let beatCount = $derived(
    sequence.beats?.length || sequence.sequence_length || 0
  );
  let difficulty = $derived(sequence.difficulty_level || "Intermediate");
  let author = $derived(sequence.author || "");
  let gridMode = $derived(sequence.grid_mode || "diamond");

  // Font sizes scaled appropriately for card size
  let titleFontSize = $derived(Math.max(10, Math.min(16, width * 0.04)));
  let metadataFontSize = $derived(Math.max(8, Math.min(12, width * 0.025)));
  let beatCountFontSize = $derived(Math.max(12, Math.min(20, width * 0.06)));

  // Generate placeholder color for visualization
  let placeholderColor = $derived(() => {
    const colors = ["#2563eb", "#059669", "#dc2626", "#7c3aed", "#ea580c"];
    const hash = sequenceName.split("").reduce((a, b) => {
      a = (a << 5) - a + b.charCodeAt(0);
      return a & a;
    }, 0);
    return colors[Math.abs(hash) % colors.length];
  });

  // Handle card click
  function handleClick() {
    onclick?.();
  }

  // Handle keyboard interaction
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      handleClick();
    }
  }
</script>

<!-- Use svelte:element to conditionally render button or div -->
<svelte:element
  this={onclick ? "button" : "div"}
  class="sequence-card-printable {onclick ? 'interactive' : ''}"
  style:width="{width}px"
  style:height="{height}px"
  style:--title-font-size="{titleFontSize}px"
  style:--metadata-font-size="{metadataFontSize}px"
  style:--beat-count-font-size="{beatCountFontSize}px"
  style:--placeholder-color={placeholderColor()}
  {onclick}
  type={onclick ? "button" : undefined}
>
  <!-- Card Header -->
  <div class="card-header">
    <div class="sequence-name" title={sequenceName}>
      {sequenceName}
    </div>
    {#if showMetadata && beatCount}
      <div class="beat-count-badge">
        {beatCount}
      </div>
    {/if}
  </div>

  <!-- Main Content Area -->
  <div class="card-content">
    <!-- Sequence Visualization Placeholder -->
    <div
      class="sequence-visualization"
      style:background-color={placeholderColor()}
    >
      <div class="visualization-overlay">
        <!-- Grid pattern indicator -->
        <div class="grid-pattern {gridMode}">
          {#each Array(Math.min(beatCount, 12)) as _, i}
            <div
              class="beat-indicator"
              class:numbered={showBeatNumbers && beatCount <= 8}
              style:animation-delay="{i * 0.1}s"
            >
              {#if showBeatNumbers && beatCount <= 8}
                <span class="beat-number">{i + 1}</span>
              {/if}
            </div>
          {/each}
        </div>

        <!-- Central beat count -->
        <div class="beat-count-display">
          <span class="beat-count-large">{beatCount}</span>
          <span class="beat-label">beats</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Card Footer -->
  {#if showMetadata}
    <div class="card-footer">
      <div class="metadata-grid">
        <div class="metadata-item">
          <span class="metadata-label">Difficulty:</span>
          <span class="metadata-value difficulty-{difficulty.toLowerCase()}">
            {difficulty}
          </span>
        </div>

        <div class="metadata-item">
          <span class="metadata-label">Grid:</span>
          <span class="metadata-value">{gridMode}</span>
        </div>

        {#if author}
          <div class="metadata-item author">
            <span class="metadata-label">By:</span>
            <span class="metadata-value" title={author}>{author}</span>
          </div>
        {/if}
      </div>
    </div>
  {/if}
</svelte:element>

<style>
  .sequence-card-printable {
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    background: white;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    cursor: pointer;
    transition: all var(--transition-fast);

    /* Print optimization */
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;
  }

  /* Reset button styles when used as interactive element */
  .sequence-card-printable.interactive {
    padding: 0;
    margin: 0;
    font: inherit;
    color: inherit;
    text-align: inherit;
  }

  .sequence-card-printable:hover {
    border-color: #d1d5db;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transform: translateY(-1px);
  }

  .sequence-card-printable:focus {
    outline: 2px solid #3b82f6;
    outline-offset: 1px;
  }

  /* Header */
  .card-header {
    padding: 6px 8px;
    background: #f9fafb;
    border-bottom: 1px solid #e5e7eb;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 4px;
    min-height: 32px;
  }

  .sequence-name {
    font-size: var(--title-font-size);
    font-weight: 600;
    color: #111827;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    flex: 1;
    line-height: 1.2;
  }

  .beat-count-badge {
    background: #3b82f6;
    color: white;
    font-size: calc(var(--title-font-size) * 0.75);
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 4px;
    min-width: 20px;
    text-align: center;
    flex-shrink: 0;
  }

  /* Content */
  .card-content {
    flex: 1;
    position: relative;
    min-height: 60px;
  }

  .sequence-visualization {
    width: 100%;
    height: 100%;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(
      135deg,
      var(--placeholder-color) 0%,
      color-mix(in srgb, var(--placeholder-color) 80%, white) 100%
    );
  }

  .visualization-overlay {
    position: relative;
    width: 90%;
    height: 90%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  /* Grid patterns */
  .grid-pattern {
    position: absolute;
    inset: 0;
    display: grid;
    gap: 2px;
    align-items: center;
    justify-items: center;
    opacity: 0.6;
  }

  .grid-pattern.diamond {
    grid-template-columns: repeat(2, 1fr);
    transform: rotate(45deg);
  }

  .grid-pattern.box {
    grid-template-columns: repeat(3, 1fr);
  }

  .grid-pattern.hexagon {
    grid-template-columns: repeat(2, 1fr);
    transform: rotate(30deg);
  }

  .beat-indicator {
    width: 6px;
    height: 6px;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 50%;
    animation: pulse 2s infinite;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 6px;
    font-weight: bold;
    color: #333;
  }

  .beat-indicator.numbered {
    width: 12px;
    height: 12px;
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(0, 0, 0, 0.2);
  }

  .beat-number {
    font-size: 6px;
    font-weight: 700;
    color: #333;
  }

  /* Central beat count */
  .beat-count-display {
    background: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 4px 8px;
    border-radius: 6px;
    text-align: center;
    backdrop-filter: blur(4px);
    border: 1px solid rgba(255, 255, 255, 0.2);
  }

  .beat-count-large {
    display: block;
    font-size: var(--beat-count-font-size);
    font-weight: 800;
    line-height: 1;
  }

  .beat-label {
    font-size: calc(var(--beat-count-font-size) * 0.5);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    opacity: 0.9;
  }

  /* Footer */
  .card-footer {
    padding: 4px 8px;
    background: #f9fafb;
    border-top: 1px solid #e5e7eb;
  }

  .metadata-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 4px 8px;
    align-items: center;
  }

  .metadata-item {
    display: flex;
    align-items: center;
    gap: 2px;
    font-size: var(--metadata-font-size);
  }

  .metadata-item.author {
    flex: 1 1 100%;
  }

  .metadata-label {
    color: #6b7280;
    font-weight: 500;
  }

  .metadata-value {
    color: #111827;
    font-weight: 600;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  /* Difficulty colors */
  .difficulty-beginner {
    color: #059669;
  }
  .difficulty-intermediate {
    color: #d97706;
  }
  .difficulty-advanced {
    color: #dc2626;
  }
  .difficulty-expert {
    color: #7c3aed;
  }

  /* Animations */
  @keyframes pulse {
    0%,
    100% {
      opacity: 0.6;
      transform: scale(0.8);
    }
    50% {
      opacity: 1;
      transform: scale(1);
    }
  }

  /* Print styles */
  @media print {
    .sequence-card-printable {
      border-color: #000 !important;
      box-shadow: none !important;
      transform: none !important;
    }

    .sequence-card-printable:hover {
      border-color: #000;
      box-shadow: none;
      transform: none;
    }

    .beat-indicator {
      animation: none;
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .sequence-card-printable {
      transition: none;
    }

    .sequence-card-printable:hover {
      transform: none;
    }

    .beat-indicator {
      animation: none;
    }
  }

  /* High contrast */
  @media (prefers-contrast: high) {
    .sequence-card-printable {
      border-color: #000;
      border-width: 2px;
    }

    .card-header,
    .card-footer {
      background: #f0f0f0;
      border-color: #000;
    }

    .metadata-label {
      color: #000;
    }
  }
</style>
