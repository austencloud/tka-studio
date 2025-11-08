<!--
	Letter to Pictograph Quiz - 2025 Modern Design

	Shows a letter and asks the user to identify the correct pictograph.
	Features modern glassmorphism design with smooth animations.
-->

<script lang="ts">
  import { Pictograph } from "$lib/shared/pictograph/shared/components";
  import type { PictographData } from "$lib/shared/pictograph/shared/domain/models/PictographData";
  import { resolve, TYPES } from "$lib/shared/inversify";
  import type { IHapticFeedbackService } from "$shared";
  import { onMount } from "svelte";
  import { QuestionGeneratorService } from "../services/implementations/QuestionGenerator";
  import { QuizType, type QuizQuestionData } from "../domain";

  // Props
  let { onAnswerSubmit, onNextQuestion } = $props<{
    onAnswerSubmit?: (isCorrect: boolean) => void;
    onNextQuestion?: () => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  // State
  let questionData = $state<QuizQuestionData | null>(null);
  let selectedAnswerId = $state<string | null>(null);
  let isAnswered = $state(false);
  let showFeedback = $state(false);
  let isLoading = $state(true);
  let error = $state<string | null>(null);

  // Derived state
  let questionLetter = $derived(questionData?.questionContent as string);
  let correctAnswer = $derived(questionData?.correctAnswer as PictographData);

  // Initialize
  onMount(async () => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
    await loadQuestion();
  });

  async function loadQuestion() {
    isLoading = true;
    error = null;

    try {
      questionData = await QuestionGeneratorService.generateQuestion(
        QuizType.LETTER_TO_PICTOGRAPH
      );
      console.log("✅ Loaded question:", questionData);
    } catch (err) {
      console.error("❌ Failed to load question:", err);
      error = err instanceof Error ? err.message : "Failed to load question";
    } finally {
      isLoading = false;
    }
  }

  function handleAnswerClick(optionId: string, isCorrect: boolean) {
    if (isAnswered) return;

    // Trigger haptic
    hapticService?.trigger("selection");

    selectedAnswerId = optionId;
    isAnswered = true;
    showFeedback = true;

    // Trigger success/error haptic
    if (isCorrect) {
      hapticService?.trigger("success");
    } else {
      hapticService?.trigger("error");
    }

    onAnswerSubmit?.(isCorrect);

    // Auto-advance after 1.5 seconds
    setTimeout(() => {
      handleNextQuestion();
    }, 1500);
  }

  async function handleNextQuestion() {
    // Trigger haptic
    hapticService?.trigger("selection");

    // Reset state
    selectedAnswerId = null;
    isAnswered = false;
    showFeedback = false;

    // Load new question
    await loadQuestion();

    onNextQuestion?.();
  }

  function getPictographButtonClass(
    optionId: string,
    isCorrect: boolean
  ): string {
    const baseClass = "pictograph-btn";

    if (!isAnswered) {
      return selectedAnswerId === optionId
        ? `${baseClass} ${baseClass}--selected`
        : baseClass;
    }

    // Show feedback
    if (isCorrect) {
      return `${baseClass} ${baseClass}--correct`;
    } else if (selectedAnswerId === optionId) {
      return `${baseClass} ${baseClass}--incorrect`;
    }

    return `${baseClass} ${baseClass}--disabled`;
  }
</script>

{#if isLoading}
  <div class="quiz-container">
    <div class="loading-state">
      <div class="loading-spinner"></div>
      <p class="loading-text">Loading question...</p>
    </div>
  </div>
{:else if error}
  <div class="quiz-container">
    <div class="error-state">
      <div class="error-icon">⚠️</div>
      <p class="error-text">{error}</p>
      <button class="retry-btn" onclick={loadQuestion}>Try Again</button>
    </div>
  </div>
{:else if questionData && questionLetter}
  <div class="quiz-container">
    <!-- Question Section -->
    <div class="question-section">
      <h3 class="question-prompt">Choose the pictograph for the letter:</h3>

      <div class="letter-display">
        <div class="letter-wrapper">
          <span class="letter">{questionLetter}</span>
        </div>
      </div>
    </div>

    <!-- Answer Section -->
    <div class="answer-section">
      <div class="pictograph-grid">
        {#each questionData.answerOptions as option (option.id)}
          <button
            class={getPictographButtonClass(option.id, option.isCorrect)}
            onclick={() => handleAnswerClick(option.id, option.isCorrect)}
            disabled={isAnswered}
          >
            <div class="pictograph-option-wrapper">
              <Pictograph pictographData={option.content as PictographData} />
            </div>

            {#if showFeedback && option.isCorrect}
              <span class="check-icon">✓</span>
            {:else if showFeedback && selectedAnswerId === option.id && !option.isCorrect}
              <span class="cross-icon">✗</span>
            {/if}
          </button>
        {/each}
      </div>
    </div>

    <!-- Feedback Banner -->
    {#if showFeedback}
      <div
        class="feedback-banner"
        class:correct={selectedAnswerId &&
          questionData.answerOptions.find((o) => o.id === selectedAnswerId)
            ?.isCorrect}
      >
        {#if selectedAnswerId && questionData.answerOptions.find((o) => o.id === selectedAnswerId)?.isCorrect}
          <div class="feedback-content">
            <span class="feedback-icon">🎉</span>
            <span class="feedback-text"
              >Correct! You found the right pictograph for "{questionLetter}"</span
            >
          </div>
        {:else}
          <div class="feedback-content">
            <span class="feedback-icon">💭</span>
            <span class="feedback-text"
              >The correct pictograph is highlighted</span
            >
          </div>
        {/if}
      </div>
    {/if}
  </div>
{/if}

<style>
  .quiz-container {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    gap: 2rem;
    padding: 2rem;
    animation: fadeIn 0.4s ease-out;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* Loading & Error States */
  .loading-state,
  .error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1.5rem;
    min-height: 400px;
  }

  .loading-spinner {
    width: 48px;
    height: 48px;
    border: 4px solid rgba(255, 255, 255, 0.1);
    border-left-color: #667eea;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .loading-text,
  .error-text {
    color: rgba(255, 255, 255, 0.9);
    font-size: 1.125rem;
    font-weight: 500;
  }

  .error-icon {
    font-size: 3rem;
  }

  .retry-btn {
    padding: 0.75rem 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    border-radius: 12px;
    color: white;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  }

  .retry-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
  }

  /* Question Section */
  .question-section {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    animation: slideDown 0.5s ease-out;
  }

  @keyframes slideDown {
    from {
      opacity: 0;
      transform: translateY(-20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .question-prompt {
    text-align: center;
    font-size: 1.5rem;
    font-weight: 600;
    color: white;
    margin: 0;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  }

  .letter-display {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 3rem;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  }

  .letter-wrapper {
    width: 200px;
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(
      135deg,
      rgba(102, 126, 234, 0.2),
      rgba(118, 75, 162, 0.2)
    );
    backdrop-filter: blur(10px);
    border-radius: 20px;
    border: 2px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  }

  .letter {
    font-size: 6rem;
    font-weight: 900;
    color: white;
    text-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    font-family: Georgia, serif;
  }

  /* Answer Section */
  .answer-section {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    animation: slideUp 0.5s ease-out 0.1s backwards;
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

  .pictograph-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }

  .pictograph-btn {
    position: relative;
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(10px);
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 180px;
  }

  .pictograph-btn:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(102, 126, 234, 0.5);
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
  }

  .pictograph-btn:active:not(:disabled) {
    transform: translateY(-2px) scale(1.01);
  }

  .pictograph-option-wrapper {
    width: 140px;
    height: 140px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }

  /* Pictograph Button States */
  .pictograph-btn--selected {
    background: linear-gradient(
      135deg,
      rgba(102, 126, 234, 0.3),
      rgba(118, 75, 162, 0.3)
    );
    border-color: rgba(102, 126, 234, 0.8);
    transform: scale(1.05);
  }

  .pictograph-btn--correct {
    background: linear-gradient(
      135deg,
      rgba(34, 197, 94, 0.2),
      rgba(22, 163, 74, 0.2)
    );
    border-color: rgb(34, 197, 94);
    animation: correctPulse 0.6s ease-out;
  }

  @keyframes correctPulse {
    0%,
    100% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.08);
    }
  }

  .pictograph-btn--incorrect {
    background: linear-gradient(
      135deg,
      rgba(239, 68, 68, 0.2),
      rgba(220, 38, 38, 0.2)
    );
    border-color: rgb(239, 68, 68);
    animation: incorrectShake 0.5s ease-out;
  }

  @keyframes incorrectShake {
    0%,
    100% {
      transform: translateX(0);
    }
    25% {
      transform: translateX(-10px);
    }
    75% {
      transform: translateX(10px);
    }
  }

  .pictograph-btn--disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .check-icon,
  .cross-icon {
    position: absolute;
    top: 0.75rem;
    right: 0.75rem;
    font-size: 2rem;
    font-weight: bold;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  }

  .check-icon {
    color: rgb(34, 197, 94);
  }

  .cross-icon {
    color: rgb(239, 68, 68);
  }

  /* Feedback Banner */
  .feedback-banner {
    padding: 1.25rem 2rem;
    background: rgba(239, 68, 68, 0.15);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    border: 1px solid rgba(239, 68, 68, 0.3);
    animation: slideIn 0.4s ease-out;
  }

  .feedback-banner.correct {
    background: rgba(34, 197, 94, 0.15);
    border-color: rgba(34, 197, 94, 0.3);
  }

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateX(-20px);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }

  .feedback-content {
    display: flex;
    align-items: center;
    gap: 1rem;
    color: white;
    font-size: 1.125rem;
    font-weight: 500;
  }

  .feedback-icon {
    font-size: 1.5rem;
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .quiz-container {
      padding: 1.5rem;
      gap: 1.5rem;
    }

    .question-prompt {
      font-size: 1.25rem;
    }

    .letter-display {
      padding: 2rem;
    }

    .letter-wrapper {
      width: 150px;
      height: 150px;
    }

    .letter {
      font-size: 4.5rem;
    }

    .pictograph-grid {
      grid-template-columns: 1fr;
      gap: 1rem;
    }

    .pictograph-btn {
      min-height: 150px;
    }

    .pictograph-option-wrapper {
      width: 120px;
      height: 120px;
    }
  }

  @media (max-width: 480px) {
    .quiz-container {
      padding: 1rem;
      gap: 1rem;
    }

    .question-prompt {
      font-size: 1.125rem;
    }

    .letter-display {
      padding: 1.5rem;
    }

    .letter-wrapper {
      width: 120px;
      height: 120px;
    }

    .letter {
      font-size: 3.5rem;
    }

    .pictograph-btn {
      padding: 1rem;
      min-height: 130px;
    }

    .pictograph-option-wrapper {
      width: 100px;
      height: 100px;
    }

    .feedback-content {
      font-size: 1rem;
    }
  }
</style>
