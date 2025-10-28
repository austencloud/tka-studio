<!--
	Pictograph to Letter Quiz Component

	Displays a real pictograph (with hidden letter) and provides multiple choice answers.
	Uses Svelte 5 runes and real pictograph data.
-->

<script lang="ts">
  import { resolve } from "$lib/shared/inversify";
  import { TYPES } from "$lib/shared/inversify/types";
  import { Pictograph } from "$lib/shared/pictograph/shared/components";
  import type {
    IHapticFeedbackService,
    IPersistenceService,
    PictographData,
  } from "$shared";
  import { Letter } from "$shared";
  import { onMount } from "svelte";
  import type { QuizAnswerOption, QuizQuestionData } from "../domain";

  // Props using runes
  let {
    questionData = $bindable(),
    showFeedback = false,
    selectedAnswerId = $bindable(),
    isAnswered = false,
    onAnswerSelected,
    onNextQuestion,
  } = $props<{
    questionData?: QuizQuestionData | null;
    showFeedback?: boolean;
    selectedAnswerId?: string | null;
    isAnswered?: boolean;
    onAnswerSelected?: (data: {
      answerId: string;
      answerContent: string;
      isCorrect: boolean;
    }) => void;
    onNextQuestion?: () => void;
  }>();

  // Services
  const persistenceService = resolve<IPersistenceService>(
    TYPES.IPersistenceService
  );
  let hapticService = $state<IHapticFeedbackService | null>(null);

  // Initialize haptic service
  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // State using runes
  let pictographs = $state<PictographData[]>([]);
  let availableLetters = $state<Letter[]>([]);
  let isLoading = $state(false);
  let currentPictograph = $state<PictographData | null>(null);
  let answerOptions = $state<QuizAnswerOption[]>([]);

  // Computed values using runes
  let correctAnswer = $derived(questionData?.correctAnswer);
  let question = $derived(
    questionData?.question || "What letter does this pictograph represent?"
  );

  // Initialize component
  $effect(() => {
    loadPictographData();
  });

  // Generate new question when needed
  $effect(() => {
    if (pictographs.length > 0 && !questionData) {
      generateRealQuestion();
    }
  });

  async function loadPictographData() {
    isLoading = true;
    try {
      // Load all pictographs
      pictographs = await persistenceService.getAllPictographs();

      // Extract unique letters, filtering out null/undefined values
      availableLetters = [
        ...new Set(
          pictographs
            .map((p) => p.letter)
            .filter((letter): letter is Letter => letter != null)
        ),
      ].sort();


    } catch (error) {
      console.error("❌ Failed to load pictograph data:", error);
    } finally {
      isLoading = false;
    }
  }

  async function generateRealQuestion() {
    if (availableLetters.length === 0) return;

    try {
      // Pick a random letter
      const randomLetter =
        availableLetters[Math.floor(Math.random() * availableLetters.length)];

      // Get pictographs for this letter
      const letterPictographs =
        await persistenceService.getPictographsByLetter(randomLetter);

      if (letterPictographs.length === 0) {
        console.warn(`No pictographs found for letter: ${randomLetter}`);
        return;
      }

      // Pick a random pictograph
      currentPictograph =
        letterPictographs[Math.floor(Math.random() * letterPictographs.length)];

      // Generate answer options (correct + 3 wrong)
      const wrongLetters = availableLetters
        .filter((letter) => letter !== randomLetter)
        .sort(() => Math.random() - 0.5)
        .slice(0, 3);

      const allOptions = [randomLetter, ...wrongLetters];

      // Shuffle the options
      const shuffledOptions = allOptions.sort(() => Math.random() - 0.5);

      answerOptions = shuffledOptions.map((letter) => ({
        id: `option-${letter}`,
        content: letter,
        isCorrect: letter === randomLetter,
      }));

      // Update question data
      questionData = {
        id: `pictograph-letter-${Date.now()}`,
        type: "pictograph-to-letter",
        question: "What letter does this pictograph represent?",
        options: answerOptions,
        correctAnswer: randomLetter,
        pictographData: currentPictograph,
      };

      console.log(`✅ Generated question for letter: ${randomLetter}`);
    } catch (error) {
      console.error("❌ Failed to generate question:", error);
    }
  }

  function handleAnswerClick(option: QuizAnswerOption) {
    if (isAnswered) return;

    // Trigger selection haptic for answer selection
    hapticService?.trigger("selection");

    selectedAnswerId = option.id;

    onAnswerSelected?.({
      answerId: option.id,
      answerContent: option.content,
      isCorrect: option.isCorrect,
    });
  }

  function handleNextQuestion() {
    // Trigger navigation haptic for next question
    hapticService?.trigger("navigation");

    // Reset state
    selectedAnswerId = null;
    questionData = null;
    currentPictograph = null;
    answerOptions = [];

    // Generate new question
    generateRealQuestion();

    onNextQuestion?.();
  }

  function getAnswerButtonClass(option: QuizAnswerOption): string {
    const baseClass = "quiz-answer-btn";

    if (!isAnswered) {
      return selectedAnswerId === option.id
        ? `${baseClass} selected`
        : baseClass;
    }

    // Show feedback after answering
    if (option.isCorrect) {
      return `${baseClass} correct`;
    } else if (selectedAnswerId === option.id) {
      return `${baseClass} incorrect`;
    }

    return `${baseClass} disabled`;
  }
</script>

{#if isLoading}
  <div class="quiz-loading">
    <div class="loading-spinner"></div>
    <p>Loading pictographs...</p>
  </div>
{:else if !questionData || !currentPictograph}
  <div class="quiz-empty">
    <p>No question available. Please try again.</p>
    <button onclick={loadPictographData} class="retry-btn">
      Retry Loading
    </button>
  </div>
{:else}
  <div class="pictograph-quiz-container">
    <!-- Quiz Header -->
    <div class="quiz-header">
      <h3 class="quiz-question">{question}</h3>
      <div class="quiz-stats">
        <span class="letter-count"
          >{availableLetters.length} letters available</span
        >
        <span class="pictograph-count"
          >{pictographs.length} pictographs loaded</span
        >
      </div>
    </div>

    <!-- Pictograph Display -->
    <div class="pictograph-display">
      <div class="pictograph-container">
        <Pictograph pictographData={currentPictograph} />
      </div>
    </div>

    <!-- Answer Options -->
    <div class="answer-options">
      {#each answerOptions as option (option.id)}
        <button
          class={getAnswerButtonClass(option)}
          onclick={() => handleAnswerClick(option)}
          disabled={isAnswered}
        >
          <span class="option-letter">{option.content}</span>
        </button>
      {/each}
    </div>

    <!-- Feedback -->
    {#if showFeedback && isAnswered}
      <div class="quiz-feedback">
        {#if selectedAnswerId && answerOptions.find((o) => o.id === selectedAnswerId)?.isCorrect}
          <div class="feedback correct-feedback">
            <span class="feedback-icon">✅</span>
            <span class="feedback-text"
              >Correct! This pictograph represents the letter "{correctAnswer}"</span
            >
          </div>
          {#if hapticService}
            {hapticService.trigger("success")}
          {/if}
        {:else}
          <div class="feedback incorrect-feedback">
            <span class="feedback-icon">❌</span>
            <span class="feedback-text"
              >Incorrect. This pictograph represents the letter "{correctAnswer}"</span
            >
          </div>
          {#if hapticService}
            {hapticService.trigger("error")}
          {/if}
        {/if}

        <button onclick={handleNextQuestion} class="next-question-btn">
          Next Question
        </button>
      </div>
    {/if}
  </div>
{/if}

<style>
  .pictograph-quiz-container {
    display: flex;
    flex-direction: column;
    max-width: 800px;
    margin: 0 auto;
    padding: 1.5rem;
    gap: 2rem;
  }

  .quiz-loading,
  .quiz-empty {
    text-align: center;
    padding: 3rem;
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 1rem;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  .quiz-header {
    text-align: center;
  }

  .quiz-question {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--color-text-primary);
  }

  .quiz-stats {
    display: flex;
    justify-content: center;
    gap: 1rem;
    font-size: 0.875rem;
    color: var(--color-text-secondary);
  }

  .pictograph-display {
    display: flex;
    justify-content: center;
    align-items: center;
    background: var(--color-background-secondary);
    border-radius: 12px;
    padding: 2rem;
    border: 2px solid var(--color-border);
  }

  .pictograph-container {
    background: white;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .answer-options {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    max-width: 400px;
    margin: 0 auto;
  }

  .quiz-answer-btn {
    padding: 1.5rem;
    border: 2px solid var(--color-border);
    border-radius: 12px;
    background: var(--color-background);
    color: var(--color-text-primary);
    font-size: 1.25rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
  }

  .quiz-answer-btn:hover:not(:disabled) {
    border-color: var(--color-primary);
    background: var(--color-primary-light);
    transform: translateY(-2px);
  }

  .quiz-answer-btn.selected {
    border-color: var(--color-primary);
    background: var(--color-primary);
    color: white;
  }

  .quiz-answer-btn.correct {
    border-color: var(--color-success);
    background: var(--color-success);
    color: white;
  }

  .quiz-answer-btn.incorrect {
    border-color: var(--color-error);
    background: var(--color-error);
    color: white;
  }

  .quiz-answer-btn.disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .option-letter {
    font-size: 1.5rem;
    font-weight: bold;
  }

  .quiz-feedback {
    text-align: center;
    padding: 1.5rem;
    border-radius: 12px;
    background: var(--color-background-secondary);
  }

  .feedback {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
    padding: 1rem;
    border-radius: 8px;
    font-weight: 500;
  }

  .correct-feedback {
    background: var(--color-success-light);
    color: var(--color-success-dark);
    border: 1px solid var(--color-success);
  }

  .incorrect-feedback {
    background: var(--color-error-light);
    color: var(--color-error-dark);
    border: 1px solid var(--color-error);
  }

  .feedback-icon {
    font-size: 1.25rem;
  }

  .next-question-btn,
  .retry-btn {
    padding: 0.75rem 2rem;
    border: none;
    border-radius: 8px;
    background: var(--color-primary);
    color: white;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .next-question-btn:hover,
  .retry-btn:hover {
    background: var(--color-primary-dark);
    transform: translateY(-1px);
  }
</style>
