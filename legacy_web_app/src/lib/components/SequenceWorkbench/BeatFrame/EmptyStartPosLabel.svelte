<!-- src/lib/components/SequenceWorkbench/BeatFrame/EmptyStartPosLabel.svelte -->
<script lang="ts">
	// This component displays a label prompting the user to choose a start position
	// when the sequence is empty

	import { onMount } from 'svelte';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';

	// Props using Svelte 5 runes
	const props = $props<{
		onClick?: () => void;
	}>();

	// Function to handle click with haptic feedback
	function handleClick() {
		// Provide haptic feedback when selecting the start position
		if (typeof window !== 'undefined' && hapticFeedbackService.isAvailable()) {
			hapticFeedbackService.trigger('selection');
		}

		// Call the original onClick handler
		props.onClick?.();
	}

	// Animation state
	let isVisible = $state(false);
	let isHovered = $state(false);
	let isSelected = $state(false);

	// Import the sequence container to check if this beat is selected
	import { sequenceContainer } from '$lib/state/stores/sequence/SequenceContainer';

	// Update isSelected when the selection changes
	$effect(() => {
		// Create a subscription to the sequenceContainer state
		const unsubscribe = sequenceContainer.subscribe((state) => {
			// Update the selection state immediately when it changes
			isSelected = state.selectedBeatIds.includes('start-position');
		});

		// Clean up the subscription when the component is destroyed or the effect is re-run
		return unsubscribe;
	});

	// Accessibility
	let uniqueId = $state(`start-pos-label-${Math.random().toString(36).substring(2, 9)}`);

	onMount(() => {
		// Trigger entrance animation after a short delay
		setTimeout(() => {
			isVisible = true;
		}, 100);
	});
</script>

<div
	class="empty-start-pos-label"
	class:visible={isVisible}
	class:hovered={isHovered}
	class:selected={isSelected}
	onclick={handleClick}
	onmouseenter={() => (isHovered = true)}
	onmouseleave={() => (isHovered = false)}
	role="button"
	tabindex="0"
	aria-label="Choose your start position"
	id={uniqueId}
	onkeydown={(e) => {
		if (e.key === 'Enter' || e.key === ' ') {
			e.preventDefault();
			handleClick();
		}
	}}
>
	<div class="label-content">
		<div class="glow-container">
			<div class="glow-effect"></div>
		</div>
		<div class="instruction-container">
			<span class="instruction">Choose your start position</span>
		</div>
	</div>
</div>

<style>
	.empty-start-pos-label {
		width: 100%;
		height: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
		cursor: pointer;
		border-radius: 8px;
		padding: 1rem;
		box-sizing: border-box;
		position: relative;
		overflow: hidden;
		background-color: var(--color-surface-700, rgba(30, 40, 60, 0.5));
		border: 1px solid var(--color-border, rgba(255, 255, 255, 0.1));
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
		transform: translateY(20px);
		opacity: 0;
		transition:
			transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1),
			opacity 0.5s cubic-bezier(0.34, 1.56, 0.64, 1),
			background-color 0.3s ease,
			box-shadow 0.3s ease;
	}

	.empty-start-pos-label.visible {
		transform: translateY(0);
		opacity: 1;
	}

	.empty-start-pos-label:hover,
	.empty-start-pos-label.hovered {
		background-color: var(--color-surface-600, rgba(40, 50, 70, 0.7));
		box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
	}

	/* Style for selected state - match the gold color used for regular beats */
	.empty-start-pos-label.selected {
		background-color: rgba(255, 204, 0, 0.1);
		box-shadow:
			0 0 0 2px rgba(255, 204, 0, 0.7),
			0 0 10px 2px rgba(255, 204, 0, 0.3); /* Primary border and outer glow */
		transform: scale(1.02);
		transition: all 0.2s ease-out;
		z-index: 2; /* Ensure it appears above other elements */
	}

	.empty-start-pos-label:focus-visible {
		outline: none;
		box-shadow: 0 0 0 3px var(--color-accent, #3a7bd5);
	}

	.label-content {
		position: relative;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.75rem;
		z-index: 1;
	}

	.instruction-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.5rem;
	}

	.instruction {
		font-family: var(
			--font-sans,
			system-ui,
			-apple-system,
			BlinkMacSystemFont,
			'Segoe UI',
			Roboto,
			sans-serif
		);
		font-size: 1.25rem;
		font-weight: 500;
		color: var(--color-text-primary, white);
		text-align: center;
		line-height: 1.4;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
		transition: transform 0.3s ease;
	}

	.empty-start-pos-label:hover .instruction,
	.empty-start-pos-label.hovered .instruction {
		transform: scale(1.05);
	}

	/* Arrow styles removed as they are not used in this component */

	.glow-container {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		overflow: hidden;
		opacity: 0;
		transition: opacity 0.5s ease;
	}

	.empty-start-pos-label:hover .glow-container,
	.empty-start-pos-label.hovered .glow-container {
		opacity: 1;
	}

	.glow-effect {
		position: absolute;
		top: -50%;
		left: -50%;
		width: 200%;
		height: 200%;
		background: radial-gradient(circle at center, var(--color-accent, #3a7bd5) 0%, transparent 70%);
		opacity: 0.1;
		animation: pulse 3s infinite ease-in-out;
	}

	@keyframes float {
		0%,
		100% {
			transform: translateY(0);
		}
		50% {
			transform: translateY(-8px);
		}
	}

	@keyframes pulse {
		0%,
		100% {
			transform: scale(1);
			opacity: 0.1;
		}
		50% {
			transform: scale(1.1);
			opacity: 0.2;
		}
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.instruction {
			font-size: 1rem;
		}

		/* Arrow styles removed as they are not used in this component */

		.empty-start-pos-label {
			padding: 0.75rem;
		}
	}

	/* High contrast mode support */
	@media (forced-colors: active) {
		.empty-start-pos-label {
			border: 2px solid ButtonText;
		}

		.instruction {
			color: ButtonText;
		}

		/* Arrow styles removed as they are not used in this component */
	}
</style>
