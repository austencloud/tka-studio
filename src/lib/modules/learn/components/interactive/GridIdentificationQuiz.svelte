<!--
GridIdentificationQuiz - Simple quiz to identify Diamond vs Box grid
First interactive quiz for "The Grid" concept
-->
<script lang="ts">
  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";

  let { onCorrect, onIncorrect } = $props<{
    onCorrect?: () => void;
    onIncorrect?: () => void;
  }>();

  const hapticService = resolve<IHapticFeedbackService>(
    TYPES.IHapticFeedbackService
  );

  type QuizState = "idle" | "correct" | "incorrect";

  let quizState = $state<QuizState>("idle");
  let selectedAnswer = $state<"left" | "right" | null>(null);

  // Randomize which side shows diamond
  let diamondOnLeft = $state(Math.random() > 0.5);

  function handleAnswer(side: "left" | "right") {
    selectedAnswer = side;

    const isDiamondCorrect =
      (side === "left" && diamondOnLeft) ||
      (side === "right" && !diamondOnLeft);

    if (isDiamondCorrect) {
      quizState = "correct";
      hapticService?.trigger("success");
      onCorrect?.();
    } else {
      quizState = "incorrect";
      hapticService?.trigger("error");
      onIncorrect?.();
    }
  }

  function resetQuiz() {
    quizState = "idle";
    selectedAnswer = null;
    diamondOnLeft = Math.random() > 0.5;
  }

  function getGridPoints(isDiamond: boolean) {
    if (isDiamond) {
      return [
        { x: 50, y: 15 },
        { x: 85, y: 50 },
        { x: 50, y: 85 },
        { x: 15, y: 50 },
        { x: 50, y: 50 },
      ];
    } else {
      return [
        { x: 25, y: 25 },
        { x: 75, y: 25 },
        { x: 75, y: 75 },
        { x: 25, y: 75 },
        { x: 50, y: 50 },
      ];
    }
  }
</script>

<div class="grid-quiz">
  <!-- Quiz header -->
  <div class="quiz-header">
    <h3 class="quiz-title">
      🎯 Quick Quiz: Can You Identify The Diamond Grid?
    </h3>
    <p class="quiz-instruction">
      Click on the grid that shows the <strong>Diamond</strong> pattern
    </p>
  </div>

  <!-- Quiz options -->
  <div class="quiz-options" class:answered={quizState !== "idle"}>
    <!-- Left option -->
    <button
      class="quiz-option"
      class:selected={selectedAnswer === "left"}
      class:correct={quizState === "correct" && selectedAnswer === "left"}
      class:incorrect={quizState === "incorrect" && selectedAnswer === "left"}
      class:correct-answer={quizState !== "idle" &&
        diamondOnLeft &&
        selectedAnswer !== "left"}
      onclick={() => quizState === "idle" && handleAnswer("left")}
      disabled={quizState !== "idle"}
    >
      <div class="option-label">Grid A</div>
      <svg viewBox="0 0 100 100" class="option-grid">
        <g class="connection-lines" opacity="0.3">
          {#if diamondOnLeft}
            <line
              x1="50"
              y1="15"
              x2="50"
              y2="85"
              stroke="white"
              stroke-width="0.5"
            />
            <line
              x1="15"
              y1="50"
              x2="85"
              y2="50"
              stroke="white"
              stroke-width="0.5"
            />
          {:else}
            <line
              x1="25"
              y1="25"
              x2="75"
              y2="75"
              stroke="white"
              stroke-width="0.5"
            />
            <line
              x1="75"
              y1="25"
              x2="25"
              y2="75"
              stroke="white"
              stroke-width="0.5"
            />
          {/if}
        </g>

        <g class="grid-points">
          {#each getGridPoints(diamondOnLeft) as point}
            <circle cx={point.x} cy={point.y} r="2" fill="white" />
          {/each}
        </g>
      </svg>
      {#if quizState === "correct" && selectedAnswer === "left"}
        <div class="result-icon correct">✓</div>
      {:else if quizState === "incorrect" && selectedAnswer === "left"}
        <div class="result-icon incorrect">✗</div>
      {:else if quizState !== "idle" && diamondOnLeft && selectedAnswer !== "left"}
        <div class="result-hint">← This was diamond!</div>
      {/if}
    </button>

    <!-- Right option -->
    <button
      class="quiz-option"
      class:selected={selectedAnswer === "right"}
      class:correct={quizState === "correct" && selectedAnswer === "right"}
      class:incorrect={quizState === "incorrect" && selectedAnswer === "right"}
      class:correct-answer={quizState !== "idle" &&
        !diamondOnLeft &&
        selectedAnswer !== "right"}
      onclick={() => quizState === "idle" && handleAnswer("right")}
      disabled={quizState !== "idle"}
    >
      <div class="option-label">Grid B</div>
      <svg viewBox="0 0 100 100" class="option-grid">
        <g class="connection-lines" opacity="0.3">
          {#if !diamondOnLeft}
            <line
              x1="50"
              y1="15"
              x2="50"
              y2="85"
              stroke="white"
              stroke-width="0.5"
            />
            <line
              x1="15"
              y1="50"
              x2="85"
              y2="50"
              stroke="white"
              stroke-width="0.5"
            />
          {:else}
            <line
              x1="25"
              y1="25"
              x2="75"
              y2="75"
              stroke="white"
              stroke-width="0.5"
            />
            <line
              x1="75"
              y1="25"
              x2="25"
              y2="75"
              stroke="white"
              stroke-width="0.5"
            />
          {/if}
        </g>

        <g class="grid-points">
          {#each getGridPoints(!diamondOnLeft) as point}
            <circle cx={point.x} cy={point.y} r="2" fill="white" />
          {/each}
        </g>
      </svg>
      {#if quizState === "correct" && selectedAnswer === "right"}
        <div class="result-icon correct">✓</div>
      {:else if quizState === "incorrect" && selectedAnswer === "right"}
        <div class="result-icon incorrect">✗</div>
      {:else if quizState !== "idle" && !diamondOnLeft && selectedAnswer !== "right"}
        <div class="result-hint">This was diamond! →</div>
      {/if}
    </button>
  </div>

  <!-- Feedback section -->
  {#if quizState !== "idle"}
    <div
      class="quiz-feedback"
      class:correct={quizState === "correct"}
      class:incorrect={quizState === "incorrect"}
    >
      {#if quizState === "correct"}
        <div class="feedback-content">
          <span class="feedback-icon">🎉</span>
          <div class="feedback-text">
            <h4>Correct!</h4>
            <p>
              Great job! You correctly identified the Diamond grid. The diamond
              pattern has points arranged vertically and horizontally, making it
              intuitive for flow patterns.
            </p>
          </div>
        </div>
      {:else}
        <div class="feedback-content">
          <span class="feedback-icon">💡</span>
          <div class="feedback-text">
            <h4>Not quite!</h4>
            <p>
              The Diamond grid has points arranged in a <strong>+ shape</strong>
              (vertical and horizontal), while the Box grid has points arranged
              in an <strong>X shape</strong> (diagonals).
            </p>
          </div>
        </div>
      {/if}

      <button class="try-again-button" onclick={resetQuiz}> Try Again </button>
    </div>
  {/if}
</div>

<style>
  .grid-quiz {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    padding: 2rem;
    background: rgba(255, 255, 255, 0.03);
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
  }

  .quiz-header {
    text-align: center;
  }

  .quiz-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: white;
    margin: 0 0 0.75rem 0;
  }

  .quiz-instruction {
    font-size: 1rem;
    color: rgba(255, 255, 255, 0.8);
    margin: 0;
  }

  .quiz-options {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
  }

  .quiz-option {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.05);
    border: 3px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    min-height: 250px;
  }

  .quiz-option:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(74, 158, 255, 0.5);
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(74, 158, 255, 0.2);
  }

  .quiz-option:disabled {
    cursor: default;
  }

  .quiz-option.selected {
    border-color: rgba(74, 158, 255, 0.6);
    background: rgba(74, 158, 255, 0.1);
  }

  .quiz-option.correct {
    border-color: rgba(80, 200, 120, 0.8);
    background: rgba(80, 200, 120, 0.15);
    animation: correctPulse 0.6s ease;
  }

  @keyframes correctPulse {
    0% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.05);
    }
    100% {
      transform: scale(1);
    }
  }

  .quiz-option.incorrect {
    border-color: rgba(255, 74, 74, 0.8);
    background: rgba(255, 74, 74, 0.15);
    animation: shake 0.4s ease;
  }

  @keyframes shake {
    0%,
    100% {
      transform: translateX(0);
    }
    25% {
      transform: translateX(-8px);
    }
    75% {
      transform: translateX(8px);
    }
  }

  .quiz-option.correct-answer {
    border-color: rgba(80, 200, 120, 0.6);
    background: rgba(80, 200, 120, 0.1);
  }

  .option-label {
    font-size: 1.125rem;
    font-weight: 700;
    color: white;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .option-grid {
    width: 100%;
    max-width: 180px;
    height: auto;
    aspect-ratio: 1;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 8px;
    padding: 1rem;
  }

  .result-icon {
    position: absolute;
    top: 1rem;
    right: 1rem;
    font-size: 2rem;
    font-weight: 800;
    animation: popIn 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  }

  @keyframes popIn {
    0% {
      transform: scale(0);
      opacity: 0;
    }
    100% {
      transform: scale(1);
      opacity: 1;
    }
  }

  .result-icon.correct {
    color: #50c878;
  }

  .result-icon.incorrect {
    color: #ff4a4a;
  }

  .result-hint {
    position: absolute;
    bottom: 0.5rem;
    left: 50%;
    transform: translateX(-50%);
    font-size: 0.875rem;
    font-weight: 600;
    color: #50c878;
    white-space: nowrap;
    animation: fadeIn 0.4s ease 0.2s both;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateX(-50%) translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }
  }

  .quiz-feedback {
    padding: 2rem;
    border-radius: 12px;
    animation: slideUp 0.4s ease;
  }

  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .quiz-feedback.correct {
    background: rgba(80, 200, 120, 0.15);
    border: 2px solid rgba(80, 200, 120, 0.4);
  }

  .quiz-feedback.incorrect {
    background: rgba(255, 158, 74, 0.15);
    border: 2px solid rgba(255, 158, 74, 0.4);
  }

  .feedback-content {
    display: flex;
    align-items: flex-start;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .feedback-icon {
    font-size: 3rem;
    flex-shrink: 0;
    line-height: 1;
  }

  .feedback-text h4 {
    font-size: 1.25rem;
    font-weight: 700;
    color: white;
    margin: 0 0 0.5rem 0;
  }

  .feedback-text p {
    font-size: 1rem;
    color: rgba(255, 255, 255, 0.9);
    margin: 0;
    line-height: 1.6;
  }

  .try-again-button {
    width: 100%;
    padding: 0.875rem 1.5rem;
    background: rgba(255, 255, 255, 0.1);
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    color: white;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s ease;
    min-height: 52px;
  }

  .try-again-button:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
  }

  /* Responsive */
  @media (max-width: 600px) {
    .grid-quiz {
      padding: 1.5rem;
    }

    .quiz-options {
      grid-template-columns: 1fr;
    }

    .feedback-content {
      flex-direction: column;
      align-items: center;
      text-align: center;
    }
  }
</style>
