<!--
  CopySequenceButton.svelte

  Copy sequence JSON button for ButtonPanel.
  Copies condensed sequence data to clipboard using SequenceExportService.
-->
<script lang="ts">
  import type { IHapticFeedbackService, ISequenceExportService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  // Props
  const {
    sequenceData
  }: {
    sequenceData: any;
  } = $props();

  // Services
  let hapticService: IHapticFeedbackService;
  let exportService: ISequenceExportService;

  // State
  let copyButtonState = $state<'idle' | 'copied' | 'error'>('idle');

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
    exportService = resolve<ISequenceExportService>(TYPES.ISequenceExportService);
  });

  async function handleClick() {
    if (!sequenceData) {
      copyButtonState = 'error';
      setTimeout(() => copyButtonState = 'idle', 2000);
      return;
    }

    try {
      hapticService?.trigger("selection");

      // Use SequenceExportService to create condensed data
      const condensedData = exportService.createCondensedSequence(sequenceData);
      const jsonString = JSON.stringify(condensedData, null, 2);

      await navigator.clipboard.writeText(jsonString);
      copyButtonState = 'copied';
      setTimeout(() => copyButtonState = 'idle', 2000);
    } catch (error) {
      console.error('Failed to copy sequence JSON:', error);
      copyButtonState = 'error';
      setTimeout(() => copyButtonState = 'idle', 2000);
    }
  }
</script>

<button
  class="panel-button copy-json-button"
  class:copied={copyButtonState === 'copied'}
  class:error={copyButtonState === 'error'}
  onclick={handleClick}
  aria-label="Copy sequence JSON to clipboard"
  title={copyButtonState === 'copied' ? 'Copied!' : copyButtonState === 'error' ? 'Error copying' : 'Copy Sequence JSON'}
>
  {#if copyButtonState === 'copied'}
    <i class="fa-solid fa-check" aria-hidden="true"></i>
  {:else if copyButtonState === 'error'}
    <i class="fa-solid fa-xmark" aria-hidden="true"></i>
  {:else}
    <i class="fa-solid fa-copy" aria-hidden="true"></i>
  {/if}
</button>

<style>
  .panel-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    font-size: 18px;
    color: #ffffff;

    /* Base button styling */
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  }

  .panel-button:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .panel-button:active {
    transform: scale(0.95);
    transition: all 0.1s ease;
  }

  .panel-button:focus-visible {
    outline: 2px solid #818cf8;
    outline-offset: 2px;
  }

  .copy-json-button {
    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
    border-color: rgba(139, 92, 246, 0.3);
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
  }

  .copy-json-button:hover {
    background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
    box-shadow: 0 6px 16px rgba(139, 92, 246, 0.6);
  }

  .copy-json-button.copied {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    border-color: rgba(16, 185, 129, 0.3);
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
  }

  .copy-json-button.error {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    border-color: rgba(239, 68, 68, 0.3);
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .panel-button {
      width: 44px;
      height: 44px;
      font-size: 16px;
    }
  }

  @media (max-width: 480px) {
    .panel-button {
      width: 40px;
      height: 40px;
      font-size: 14px;
    }
  }

  @media (max-width: 320px) {
    .panel-button {
      width: 36px;
      height: 36px;
      font-size: 12px;
    }
  }

  /* 🎯 LANDSCAPE MOBILE: Compact buttons for Z Fold 5 horizontal (882x344) */
  @media (min-aspect-ratio: 17/10) and (max-height: 500px) {
    .panel-button {
      width: 36px;
      height: 36px;
      font-size: 14px;
    }
  }
</style>
