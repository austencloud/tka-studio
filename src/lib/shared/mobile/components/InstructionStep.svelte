<!--
  InstructionStep.svelte

  Displays a single instruction step with optional image/placeholder.
  Reusable component that adapts to compact mode.
-->
<script lang="ts">
  import type { InstructionStep } from "../config/pwa-install-instructions";

  let {
    step,
    index,
    compact = false,
  }: {
    step: InstructionStep;
    index: number;
    compact?: boolean;
  } = $props();
</script>

<div class="step-card" class:compact>
  <div class="step-header">
    <div class="step-number">{index + 1}</div>
    <div class="step-text">{@html step.text}</div>
  </div>

  <!-- Show placeholder for future screenshots (only when not in compact mode) -->
  {#if !compact}
    <div class="step-image-container">
      {#if step.image}
        <img src={step.image} alt="Step {index + 1}" class="step-image" />
      {:else}
        <div class="image-placeholder">
          <i class="fas fa-image"></i>
          <span class="placeholder-text">Screenshot coming soon</span>
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .step-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: clamp(8px, 2cqw, 12px);
    padding: clamp(10px, 2.5cqh, 14px);
    transition: all 0.2s ease;
  }

  .compact.step-card {
    padding: clamp(8px, 2cqh, 10px);
  }

  .step-card:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.15);
  }

  .step-header {
    display: flex;
    align-items: flex-start;
    gap: clamp(8px, 2cqw, 12px);
    margin-bottom: clamp(6px, 1.5cqh, 10px);
  }

  .compact .step-header {
    margin-bottom: 0;
  }

  .step-number {
    display: flex;
    align-items: center;
    justify-content: center;
    width: clamp(26px, 6cqw, 30px);
    height: clamp(26px, 6cqw, 30px);
    flex-shrink: 0;
    border-radius: clamp(6px, 1.5cqw, 8px);
    background: linear-gradient(
      135deg,
      rgba(99, 102, 241, 0.3) 0%,
      rgba(139, 92, 246, 0.3) 100%
    );
    border: 1px solid rgba(99, 102, 241, 0.4);
    color: rgba(139, 92, 246, 1);
    font-weight: 700;
    font-size: clamp(13px, 3cqw, 15px);
  }

  .step-text {
    flex: 1;
    margin: 0;
    color: rgba(255, 255, 255, 0.88);
    line-height: 1.5;
    font-size: clamp(12px, 3cqw, 14px);
  }

  .compact .step-text {
    font-size: clamp(11px, 2.5cqw, 13px);
    line-height: 1.4;
  }

  .step-text :global(strong) {
    color: rgba(255, 255, 255, 0.98);
    font-weight: 600;
  }

  /* Step Screenshot Thumbnails - Fluid sizing */
  .step-image-container {
    position: relative;
    margin-top: clamp(6px, 1.5cqh, 8px);
    border-radius: clamp(6px, 1.5cqw, 8px);
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.12);
    max-width: clamp(150px, 40cqw, 200px);
  }

  .step-image {
    width: 100%;
    height: auto;
    display: block;
  }

  .image-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: clamp(6px, 1.5cqh, 8px);
    padding: clamp(12px, 3cqh, 20px);
    background: rgba(255, 255, 255, 0.03);
    color: rgba(255, 255, 255, 0.3);
    min-height: 80px;
  }

  .image-placeholder i {
    font-size: clamp(18px, 4cqw, 24px);
    opacity: 0.5;
  }

  .placeholder-text {
    font-size: clamp(10px, 2cqw, 11px);
    opacity: 0.6;
    font-style: italic;
  }
</style>
