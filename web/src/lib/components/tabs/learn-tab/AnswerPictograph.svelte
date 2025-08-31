<!--
	Answer Pictograph Component

	Displays pictograph answer options as clickable cards.
	Handles selection states, feedback, and visual effects.
-->

<script lang="ts">
  import type { PictographData } from "$domain";
  import PictographRenderer from "./PictographRenderer.svelte";

  interface Props {
    pictographData: PictographData;
    isSelected?: boolean;
    isCorrect?: boolean;
    showFeedback?: boolean;
    disabled?: boolean;
    onclick?: () => void;
  }

  // Props
  let {
    pictographData,
    isSelected = false,
    isCorrect = false,
    showFeedback = false,
    disabled = false,
    onclick,
  }: Props = $props();

  // Derived state
  let cardClass = $derived(getCardClass());

  // Methods
  function getCardClass(): string {
    let classes = ["answer-pictograph"];

    if (disabled) {
      classes.push("disabled");
    }

    if (isSelected) {
      classes.push("selected");
    }

    if (showFeedback) {
      if (isCorrect) {
        classes.push("correct");
      } else if (isSelected && !isCorrect) {
        classes.push("incorrect");
      } else {
        classes.push("faded");
      }
    }

    return classes.join(" ");
  }

  function handleClick() {
    if (!disabled) {
      onclick?.();
    }
  }
</script>

<button class={cardClass} onclick={handleClick} {disabled} type="button">
  <div class="pictograph-container">
    <PictographRenderer {pictographData} size="medium" />
  </div>

  {#if pictographData?.letter}
    <div class="letter-label">
      {pictographData.letter}
    </div>
  {/if}

  {#if showFeedback && isCorrect}
    <div class="feedback-overlay correct">
      <span class="feedback-icon">✓</span>
    </div>
  {:else if showFeedback && isSelected && !isCorrect}
    <div class="feedback-overlay incorrect">
      <span class="feedback-icon">✗</span>
    </div>
  {/if}
</button>

<style>
  .answer-pictograph {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
    width: 100%;
    min-height: 180px;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.1);
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    color: #ffffff;
    cursor: pointer;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    overflow: hidden;
  }

  .answer-pictograph::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.1),
      transparent
    );
    transition: left 0.5s ease;
    z-index: 1;
  }

  .answer-pictograph:hover::before {
    left: 100%;
  }

  .answer-pictograph:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
  }

  .answer-pictograph:active {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  }

  .answer-pictograph.selected {
    background: rgba(102, 126, 234, 0.3);
    border-color: #667eea;
    box-shadow: 0 0 25px rgba(102, 126, 234, 0.4);
    transform: translateY(-2px);
  }

  .answer-pictograph.correct {
    background: rgba(74, 222, 128, 0.3);
    border-color: #4ade80;
    box-shadow: 0 0 25px rgba(74, 222, 128, 0.4);
    animation: correctPulse 0.8s ease-in-out;
  }

  .answer-pictograph.incorrect {
    background: rgba(248, 113, 113, 0.3);
    border-color: #f87171;
    box-shadow: 0 0 25px rgba(248, 113, 113, 0.4);
    animation: incorrectShake 0.8s ease-in-out;
  }

  .answer-pictograph.faded {
    opacity: 0.4;
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.1);
  }

  .answer-pictograph.disabled {
    cursor: not-allowed;
    opacity: 0.6;
    pointer-events: none;
  }

  .pictograph-container {
    position: relative;
    z-index: 2;
    display: flex;
    justify-content: center;
    align-items: center;
    flex: 1;
  }

  .letter-label {
    position: relative;
    z-index: 2;
    font-size: 1.125rem;
    font-weight: 600;
    color: #ffffff;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    padding: 0.25rem 0.75rem;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 6px;
    backdrop-filter: blur(4px);
  }

  .feedback-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(4px);
    z-index: 10;
    border-radius: 10px;
  }

  .feedback-overlay.correct {
    background: rgba(74, 222, 128, 0.2);
  }

  .feedback-overlay.incorrect {
    background: rgba(248, 113, 113, 0.2);
  }

  .feedback-icon {
    font-size: 3rem;
    font-weight: bold;
    text-shadow: 0 0 12px currentColor;
  }

  .feedback-overlay.correct .feedback-icon {
    color: #4ade80;
  }

  .feedback-overlay.incorrect .feedback-icon {
    color: #f87171;
  }

  @keyframes correctPulse {
    0%,
    100% {
      transform: scale(1) translateY(-2px);
    }
    50% {
      transform: scale(1.05) translateY(-4px);
    }
  }

  @keyframes incorrectShake {
    0%,
    100% {
      transform: translateX(0) translateY(-2px);
    }
    25% {
      transform: translateX(-8px) translateY(-2px);
    }
    75% {
      transform: translateX(8px) translateY(-2px);
    }
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .answer-pictograph {
      min-height: 150px;
      padding: 0.75rem;
      gap: 0.5rem;
    }

    .letter-label {
      font-size: 1rem;
    }

    .feedback-icon {
      font-size: 2.5rem;
    }
  }

  @media (max-width: 480px) {
    .answer-pictograph {
      min-height: 120px;
      padding: 0.5rem;
    }

    .letter-label {
      font-size: 0.875rem;
    }

    .feedback-icon {
      font-size: 2rem;
    }
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    .answer-pictograph {
      border-width: 3px;
    }

    .answer-pictograph.correct {
      background: rgba(74, 222, 128, 0.5);
    }

    .answer-pictograph.incorrect {
      background: rgba(248, 113, 113, 0.5);
    }

    .feedback-overlay {
      background: rgba(0, 0, 0, 0.9);
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .answer-pictograph {
      transition: none;
    }

    .answer-pictograph::before {
      transition: none;
    }

    .answer-pictograph.correct,
    .answer-pictograph.incorrect {
      animation: none;
    }
  }

  /* Focus styles for accessibility */
  .answer-pictograph:focus {
    outline: 3px solid #667eea;
    outline-offset: 2px;
  }

  .answer-pictograph:focus:not(:focus-visible) {
    outline: none;
  }
</style>
