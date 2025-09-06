<!-- src/lib/components/GenerateTab/controls/GenerateButtonSection.svelte -->
<script lang="ts">
	import { sequenceSelectors } from '$lib/state/machines/sequenceMachine';
	import { isGenerating, hasError, statusMessage } from '../store/generator';
	import GenerateButton from '../components/GenerateButton.svelte';

	// Use Svelte 5 props rune
	const props = $props<{
		useNewStateManagement?: boolean;
		onGenerateClick: () => void;
	}>();

	// Default values with derived values
	const useNewStateManagement = $derived(props.useNewStateManagement ?? true);

	// Get state from sequence machine using $derived rune
	const newIsGenerating = $derived(sequenceSelectors.isGenerating());
	const newHasError = $derived(sequenceSelectors.hasError());
	const newStatusMessage = $derived(sequenceSelectors.message());
</script>

<div class="generate-button-container">
	<GenerateButton
		isLoading={useNewStateManagement ? newIsGenerating : $isGenerating}
		hasError={useNewStateManagement ? newHasError : $hasError}
		statusMessage={useNewStateManagement ? newStatusMessage : $statusMessage}
		onClick={props.onGenerateClick}
	/>
</div>

<style>
	.generate-button-container {
		padding: 1.5rem;
		background: var(--color-surface-800, rgba(20, 30, 50, 0.7));
		border-radius: 0.5rem;
		border: 1px solid rgba(255, 255, 255, 0.05);
		display: flex;
		justify-content: center;
		position: relative;
		overflow: hidden;
		margin-bottom: 1rem;
		animation: fadeIn 0.4s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
		animation-delay: 0.6s;
		opacity: 0;
		background: linear-gradient(
			135deg,
			var(--color-surface-800, rgba(20, 30, 50, 0.7)),
			var(--color-surface-700, rgba(30, 40, 60, 0.7)),
			var(--color-surface-800, rgba(20, 30, 50, 0.7))
		);
		background-size: 200% 200%;
		animation:
			gradientShift 15s ease infinite,
			fadeIn 0.4s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
	}

	.generate-button-container::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 2px;
		background: linear-gradient(to right, transparent, rgba(58, 123, 213, 0.5), transparent);
		opacity: 0;
		transition: opacity 0.3s ease;
	}

	.generate-button-container:hover::before {
		opacity: 1;
	}

	/* Animation for panel transitions */
	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(20px);
			filter: blur(5px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
			filter: blur(0);
		}
	}

	/* Subtle background animation */
	@keyframes gradientShift {
		0% {
			background-position: 0% 50%;
		}
		50% {
			background-position: 100% 50%;
		}
		100% {
			background-position: 0% 50%;
		}
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.generate-button-container {
			padding: 1rem;
		}
	}
</style>
