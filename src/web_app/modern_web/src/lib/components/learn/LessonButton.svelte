<!-- LessonButton.svelte - Styled lesson selection button -->
<script lang="ts">
	import type { LessonType } from '$lib/types/learn';

	// Props
	interface Props {
		text: string;
		lessonType: LessonType;
		description?: string;
		disabled?: boolean;
		onClicked?: (lessonType: LessonType) => void;
	}

	let { text, lessonType, description = '', disabled = false, onClicked }: Props = $props();

	// Handle button click
	function handleClick() {
		if (disabled) return;
		onClicked?.(lessonType);
	}
</script>

<div class="lesson-button-container">
	<button
		class="lesson-button"
		class:disabled
		onclick={handleClick}
		title={description}
		{disabled}
	>
		{text}
	</button>
	{#if description}
		<p class="lesson-description">{description}</p>
	{/if}
</div>

<style>
	.lesson-button-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--spacing-sm);
		margin: var(--spacing-md) 0;
	}

	.lesson-button {
		background: rgba(255, 255, 255, 0.2);
		border: 2px solid rgba(255, 255, 255, 0.3);
		border-radius: 14px;
		color: white;
		font-family: Georgia, serif;
		font-weight: bold;
		font-size: 16px;
		padding: 12px 24px;
		cursor: pointer;
		transition: all var(--transition-normal);
		backdrop-filter: var(--glass-backdrop);
		box-shadow: var(--shadow-glass);
		min-width: 200px;
		text-align: center;
		position: relative;
		overflow: hidden;
	}

	.lesson-button::before {
		content: '';
		position: absolute;
		top: 0;
		left: -100%;
		width: 100%;
		height: 100%;
		background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
		transition: left var(--transition-slow);
	}

	.lesson-button:hover:not(.disabled) {
		background: rgba(255, 255, 255, 0.3);
		border: 2px solid rgba(255, 255, 255, 0.5);
		transform: translateY(-2px);
		box-shadow: var(--shadow-glass-hover);
	}

	.lesson-button:hover:not(.disabled)::before {
		left: 100%;
	}

	.lesson-button:active:not(.disabled) {
		background: rgba(255, 255, 255, 0.4);
		border: 2px solid rgba(255, 255, 255, 0.6);
		transform: translateY(0);
	}

	.lesson-button.disabled {
		background: rgba(255, 255, 255, 0.1);
		border: 2px solid rgba(255, 255, 255, 0.2);
		color: rgba(255, 255, 255, 0.5);
		cursor: not-allowed;
		transform: none;
	}

	.lesson-description {
		color: rgba(255, 255, 255, 0.8);
		font-family: Georgia, serif;
		font-size: 12px;
		text-align: center;
		margin: 0;
		max-width: 300px;
		line-height: 1.4;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.lesson-button {
			font-size: 14px;
			padding: 10px 20px;
			min-width: 180px;
		}

		.lesson-description {
			font-size: 11px;
			max-width: 250px;
		}
	}

	@media (max-width: 480px) {
		.lesson-button {
			font-size: 13px;
			padding: 8px 16px;
			min-width: 160px;
		}

		.lesson-description {
			font-size: 10px;
			max-width: 200px;
		}
	}

	/* Focus styles for accessibility */
	.lesson-button:focus-visible {
		outline: 2px solid rgba(255, 255, 255, 0.6);
		outline-offset: 2px;
	}
</style>
