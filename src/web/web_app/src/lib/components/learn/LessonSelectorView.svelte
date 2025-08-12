<!-- LessonSelectorView.svelte - Main lesson selection interface -->
<script lang="ts">
	import { QuizMode, LessonType, LESSON_INFO } from '$lib/types/learn';
	import LessonModeToggle from './LessonModeToggle.svelte';
	import LessonButton from './LessonButton.svelte';

	// Props
	interface Props {
		selectedMode?: QuizMode;
		availableLessons?: LessonType[];
		isLoading?: boolean;
		onLessonRequested?: (data: { lessonType: LessonType; quizMode: QuizMode }) => void;
		onModeChanged?: (mode: QuizMode) => void;
	}

	let {
		selectedMode = $bindable(QuizMode.FIXED_QUESTION),
		availableLessons = Object.values(LessonType),
		isLoading = false,
		onLessonRequested,
		onModeChanged,
	}: Props = $props();

	// Handle mode change
	function handleModeChanged(mode: QuizMode) {
		selectedMode = mode;
		onModeChanged?.(selectedMode);
	}

	// Handle lesson selection
	function handleLessonClicked(lessonType: LessonType) {
		onLessonRequested?.({ lessonType, quizMode: selectedMode });
	}

	// Check if lesson is available
	function isLessonAvailable(lessonType: LessonType): boolean {
		return availableLessons.includes(lessonType);
	}
</script>

<div class="lesson-selector">
	<!-- Title Section -->
	<div class="title-section">
		<h1 class="title">Select a Lesson:</h1>
	</div>

	<!-- Mode Toggle Section -->
	<div class="mode-section">
		<LessonModeToggle
			bind:selectedMode
			disabled={isLoading}
			onModeChanged={handleModeChanged}
		/>
	</div>

	<!-- Lessons Section -->
	<div class="lessons-section">
		{#each LESSON_INFO as lesson}
			<LessonButton
				text={lesson.name}
				lessonType={lesson.lessonType}
				description={lesson.description}
				disabled={isLoading || !isLessonAvailable(lesson.lessonType)}
				onClicked={handleLessonClicked}
			/>
		{/each}
	</div>
</div>

<style>
	.lesson-selector {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100%;
		width: 100%;
		padding: var(--spacing-xl);
		gap: var(--spacing-lg);
	}

	.title-section {
		flex: 2;
		display: flex;
		align-items: flex-end;
		justify-content: center;
	}

	.title {
		color: white;
		font-family: Georgia, serif;
		font-weight: bold;
		font-size: 24px;
		text-align: center;
		margin: 0;
		text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
	}

	.mode-section {
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.lessons-section {
		flex: 2;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: flex-start;
		gap: var(--spacing-md);
		width: 100%;
		max-width: 400px;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.lesson-selector {
			padding: var(--spacing-lg);
			gap: var(--spacing-md);
		}

		.title {
			font-size: 20px;
		}
	}

	@media (max-width: 480px) {
		.lesson-selector {
			padding: var(--spacing-md);
			gap: var(--spacing-sm);
		}

		.title {
			font-size: 18px;
		}

		.lessons-section {
			max-width: 300px;
		}
	}

	/* Responsive font sizing based on container */
	@container (max-width: 600px) {
		.title {
			font-size: 18px;
		}
	}

	@container (max-width: 400px) {
		.title {
			font-size: 16px;
		}
	}
</style>
