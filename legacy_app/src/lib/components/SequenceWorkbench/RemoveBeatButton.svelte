<!-- src/lib/components/SequenceWorkbench/RemoveBeatButton.svelte -->
<script lang="ts">
	import { fly, fade } from 'svelte/transition';
	import { elasticOut } from 'svelte/easing';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import { browser } from '$app/environment';

	// Use Svelte 5 events
	const dispatch = $props<{
		onRemoveBeat?: () => void;
	}>();

	function handleClick() {
		// Provide warning haptic feedback for deletion
		if (browser) {
			hapticFeedbackService.trigger('warning');
		}

		// Call the event handler if provided
		if (dispatch.onRemoveBeat) {
			dispatch.onRemoveBeat();
		}
	}
</script>

<!-- Apply transitions directly to the button for consistent behavior across all devices -->
<button
	class="remove-beat-button ripple"
	onclick={handleClick}
	aria-label="Remove selected beat"
	data-mdb-ripple="true"
	data-mdb-ripple-color="light"
	in:fly={{ x: 20, duration: 350, delay: 0, easing: elasticOut }}
	out:fade={{ duration: 200 }}
>
	<div class="icon-wrapper">
		<i class="fa-solid fa-trash"></i>
	</div>
	<span class="button-label">Remove Selected Beat</span>
</button>

<style>
	.remove-beat-button {
		/* Define base sizes for dynamic scaling */
		--base-size: 45px; /* Base size of the button */
		--base-icon-size: 19px; /* Base size of the icon */
		--base-margin: 10px; /* Define base margin to match other buttons */
		--button-height: 40px; /* Height of the button */
		--clear-button-width: calc(
			var(--button-size-factor, 1) * var(--base-size)
		); /* Width of clear button */

		position: absolute;
		/* Position to the right of the clear button with proper spacing */
		bottom: max(
			calc(var(--button-size-factor, 1) * var(--base-margin)),
			var(--safe-inset-bottom, 0px)
		);
		/* Position to the right of the clear button (clear button width + margin + extra spacing) */
		left: calc(
			var(--clear-button-width) + (var(--button-size-factor, 1) * var(--base-margin) * 2) +
				max(calc(var(--button-size-factor, 1) * var(--base-margin)), var(--safe-inset-left, 0px))
		);

		/* Set dimensions for a pill-shaped button */
		height: var(--button-height);
		min-height: 38px;
		padding: 0 16px;

		background-color: var(--tkc-button-panel-background, #2a2a2e);
		border-radius: 20px; /* Rounded corners for pill shape */
		display: flex;
		align-items: center;
		justify-content: flex-start;
		gap: 8px; /* Space between icon and text */
		cursor: pointer;
		transition:
			transform 0.2s ease-out,
			background-color 0.2s ease-out,
			box-shadow 0.2s ease-out;
		z-index: 41; /* One level higher than the clear button to ensure proper stacking */
		box-shadow:
			0 3px 6px rgba(0, 0, 0, 0.16),
			0 3px 6px rgba(0, 0, 0, 0.23);
		border: none;
		color: var(--tkc-icon-color-delete, #ff9e00); /* Orange/amber color */
		pointer-events: auto;
		white-space: nowrap; /* Prevent text wrapping */
	}

	.remove-beat-button:hover {
		background-color: var(--tkc-button-panel-background-hover, #3c3c41);
		transform: translateY(-2px) scale(1.02);
		box-shadow:
			0 6px 12px rgba(0, 0, 0, 0.2),
			0 4px 8px rgba(0, 0, 0, 0.26);
	}

	.remove-beat-button:active {
		transform: translateY(0px) scale(0.98);
		background-color: var(--tkc-button-panel-background-active, #1e1e21);
		box-shadow:
			0 1px 3px rgba(0, 0, 0, 0.12),
			0 1px 2px rgba(0, 0, 0, 0.24);
	}

	.icon-wrapper {
		background: transparent;
		display: flex;
		align-items: center;
		justify-content: center;
		width: auto;
		height: auto;
		color: inherit;
	}

	.icon-wrapper i.fa-trash {
		font-size: calc(var(--button-size-factor, 1) * var(--base-icon-size));
	}

	.button-label {
		font-size: 14px;
		font-weight: 500;
		color: white;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.remove-beat-button {
			--button-size-factor: 0.9;
			padding: 0 12px;
		}

		.button-label {
			font-size: 13px;
		}
	}

	@media (max-width: 480px) {
		.remove-beat-button {
			--button-size-factor: 0.8;
			padding: 0 10px;
		}

		.button-label {
			font-size: 12px;
		}
	}
</style>
