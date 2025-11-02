<script lang="ts">
  import { simplifyAndTruncate } from "../../shared/utils/word-simplifier";
  import type { SequenceData } from "$shared/foundation/domain/models/SequenceData";
  import type { ISequenceAnalysisService } from "$create/shared/services/contracts";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  // Props
  let {
    word = "",
    scrollMode = false,
    sequence = null
  } = $props<{
    word?: string;
    scrollMode?: boolean;
    sequence?: SequenceData | null;
  }>();

  // Services
  let sequenceAnalysisService: ISequenceAnalysisService | null = $state(null);

  // State
  let showCopiedMessage = $state(false);
  let copiedTimeout: number | null = $state(null);

  // Check if this is a contextual message (not a word)
  const isContextualMessage = $derived(() => {
    const contextualPhrases = [
      "Configure Your Settings",
      "Drawing Blue Hand Path",
      "Drawing Red Hand Path",
      "Sequence Complete!",
      "Draw Hand Path"
    ];
    return contextualPhrases.some(phrase => word.includes(phrase));
  });

  // Derived simplified word (only truncate actual words, not contextual messages)
  const displayWord = $derived(
    isContextualMessage() ? word : simplifyAndTruncate(word, 8)
  );

  // Check if sequence is circular-capable
  const isCircularCapable = $derived(() => {
    if (!sequence || !sequenceAnalysisService) return false;
    return sequenceAnalysisService.isCircularCapable(sequence);
  });

  // Initialize services
  onMount(() => {
    sequenceAnalysisService = resolve<ISequenceAnalysisService>(TYPES.ISequenceAnalysisService);
  });

  // Only show word label if there's an actual word (not empty, not default sequence names)
  const shouldShowWordLabel = $derived(() => {
    if (!word) return false;

    // Always show contextual messages
    if (isContextualMessage()) return true;

    // Don't show if it's a default sequence name without actual letters
    // Check if word starts with default sequence name patterns
    const defaultNamePrefixes = ["No sequence", "Sequence", "New Sequence"];
    if (defaultNamePrefixes.some(prefix => word.startsWith(prefix))) return false;

    return true;
  });



  /**
   * Copy word to clipboard and show feedback
   */
  async function copyToClipboard() {
    // Don't copy contextual messages
    if (!word || isContextualMessage()) return;

    try {
      await navigator.clipboard.writeText(word);

      // Show copied message
      showCopiedMessage = true;

      // Clear existing timeout
      if (copiedTimeout !== null) {
        clearTimeout(copiedTimeout);
      }

      // Hide message after 2 seconds
      copiedTimeout = window.setTimeout(() => {
        showCopiedMessage = false;
        copiedTimeout = null;
      }, 2000);
    } catch (err) {
      console.error("Failed to copy word to clipboard:", err);
    }
  }
</script>

{#if shouldShowWordLabel()}
  <div
    class="word-label-container"
    class:scroll-mode={scrollMode}
  >
    <button
      class="word-label"
      class:has-word={!!word && !isContextualMessage()}
      class:contextual-message={isContextualMessage()}
      onclick={copyToClipboard}
      title={isContextualMessage() ? word : "Click to copy '{word}' to clipboard"}
      aria-label={isContextualMessage() ? word : "Current word: {word}. Click to copy."}
    >
      {displayWord}
    </button>

    {#if showCopiedMessage}
      <div class="copied-message" role="status" aria-live="polite">
        Copied "{word}"!
      </div>
    {/if}
  </div>
{/if}

<style>
  .word-label-container {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    z-index: 10;
    pointer-events: none;
    /* Enable container queries for intrinsic sizing */
    container-type: inline-size;
    container-name: word-label;
  }

  .word-label {
    pointer-events: auto;
    font-family: Georgia, serif;
    font-weight: 600;
    font-size: clamp(1.5rem, 3vw, 2.5rem);
    color: var(--text-color, #2c3e50);
    background: transparent;
    border: none;
    cursor: pointer;
    transition: all 0.2s ease;
    border-radius: 8px;
    text-align: center;
    white-space: nowrap;
    overflow: visible;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    margin: 0;
  }

  .word-label:hover {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(4px);
    transform: scale(1.05);
  }

  .word-label:active {
    transform: scale(0.95);
  }

  .word-label.has-word {
    /* Slightly smaller to ensure 8 letter units fit comfortably on one line */
    font-size: clamp(1.5rem, 3.5vw, 2.75rem);
  }

  /* Contextual messages (hand path status, etc.) - Container-aware sizing */
  .word-label.contextual-message {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-weight: 600;
    /* Intrinsic sizing based on container width - scales from 1rem at 300px to 2.5rem at 800px+ */
    font-size: clamp(1rem, 5cqi, 2.5rem);
    max-width: 100%;
    padding: 0.5rem 1rem;
    white-space: nowrap;
    color: var(--text-color, #2c3e50);
  }

  /* Fine-tune sizing at different container widths */
  @container word-label (min-width: 600px) {
    .word-label.contextual-message {
      font-size: clamp(1.25rem, 5.5cqi, 2.5rem);
    }
  }

  @container word-label (min-width: 800px) {
    .word-label.contextual-message {
      font-size: clamp(1.5rem, 6cqi, 3rem);
    }
  }

  .word-label.contextual-message:hover {
    background: transparent;
    transform: none;
    cursor: default;
  }

  .copied-message {
    position: absolute;
    top: 110%;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(46, 204, 113, 0.95);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 600;
    white-space: nowrap;
    animation: fadeInOut 2s ease;
    pointer-events: none;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  @keyframes fadeInOut {
    0% {
      opacity: 0;
      transform: translateX(-50%) translateY(-10px);
    }
    15% {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }
    85% {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }
    100% {
      opacity: 0;
      transform: translateX(-50%) translateY(-10px);
    }
  }

  /* Mobile responsive */
  @media (max-width: 768px) {


    .word-label {
      font-size: clamp(1.25rem, 3vw, 2rem);
      padding: 0.2rem 0.5rem;
    }

    .word-label.has-word {
      font-size: clamp(1.5rem, 3vw, 2.5rem);
    }

    .copied-message {
      font-size: 0.8rem;
      padding: 0.4rem 0.8rem;
    }
  }

  /* Ultra-narrow screens */
  @media (max-width: 480px) {
    .word-label {
      font-size: clamp(1rem, 6vw, 1.75rem);
    }

    .word-label.has-word {
      font-size: clamp(1.25rem, 7vw, 2rem);
    }
  }
</style>
