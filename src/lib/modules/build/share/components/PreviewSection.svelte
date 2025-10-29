<!-- PreviewSection.svelte - Preview display in the middle -->
<script lang="ts">
  import type { SequenceData } from "$shared";
  import SharePreview from "./SharePreview.svelte";

  let {
    currentSequence = null,
    previewUrl = null,
    isGenerating = false,
    error = null,
    onRetry,
  }: {
    currentSequence?: SequenceData | null;
    previewUrl?: string | null;
    isGenerating?: boolean;
    error?: string | null;
    onRetry?: () => void;
  } = $props();

  // Handle retry action
  function handleRetry() {
    onRetry?.();
  }

  // Get preview status for accessibility
  let previewStatus = $derived(() => {
    if (!currentSequence) return 'No sequence selected';
    if (currentSequence.beats?.length === 0) return 'Empty sequence';
    if (isGenerating) return 'Generating preview';
    if (error) return `Preview error: ${error}`;
    if (previewUrl) return 'Preview ready';
    return 'Preview pending';
  });
</script>

<!-- Preview Status (for screen readers) -->
<div class="sr-only" aria-live="polite" aria-atomic="true">
  {previewStatus()}
</div>

<!-- Direct preview - no wrapper needed -->
<SharePreview
  {currentSequence}
  {previewUrl}
  {isGenerating}
  {error}
  onRetry={handleRetry}
/>

<style>
  /* Screen reader only content */
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }
</style>
