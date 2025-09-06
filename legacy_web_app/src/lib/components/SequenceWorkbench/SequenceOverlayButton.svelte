<!-- src/lib/components/SequenceWorkbench/SequenceOverlayButton.svelte -->
<script lang="ts">
	import { fly } from 'svelte/transition';
	import { openSequenceOverlay } from '$lib/state/sequenceOverlay/sequenceOverlayState';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import { browser } from '$app/environment';

	function handleClick() {
		// Provide haptic feedback when opening the sequence overlay
		if (browser && hapticFeedbackService.isAvailable()) {
			hapticFeedbackService.trigger('selection');
		}

		openSequenceOverlay();
	}
</script>

<button
	class="sequence-overlay-button ripple"
	on:click={handleClick}
	aria-label="View sequence in overlay"
	data-mdb-ripple="true"
	data-mdb-ripple-color="light"
	in:fly={{ x: 20, duration: 300, delay: 200 }}
>
	<div class="icon-wrapper">
		<i class="fa-solid fa-up-right-and-down-left-from-center"></i>
	</div>
</button>

<style>
	.sequence-overlay-button {
		/* Base sizes for dynamic scaling - match other buttons */
		--base-size: 45px; /* Base size of the button */
		--base-icon-size: 19px; /* Base size of the icon */
		--base-margin: 10px; /* Base margin from corner */

		position: absolute;
		/* Bottom inset is important as it affects the entire bottom edge */
		bottom: max(
			calc(var(--button-size-factor, 1) * var(--base-margin)),
			var(--safe-inset-bottom, 0px)
		);
		/* Right inset is rarely needed for corner buttons */
		right: calc(var(--button-size-factor, 1) * var(--base-margin));

		width: calc(var(--button-size-factor, 1) * var(--base-size)); /* Dynamic width */
		height: calc(var(--button-size-factor, 1) * var(--base-size)); /* Dynamic height */
		min-width: 38px; /* Minimum width */
		min-height: 38px; /* Minimum height */

		background-color: var(
			--tkc-button-panel-background,
			#2a2a2e
		); /* Dark background, consistent with other buttons */
		color: var(
			--tkc-icon-color-sequence-overlay,
			#4cc9f0
		); /* Blue icon color for sequence overlay */

		border-radius: 50%; /* Perfectly round */
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition:
			transform 0.2s ease-out,
			background-color 0.2s ease-out,
			box-shadow 0.2s ease-out;
		z-index: 40; /* Ensure it's above most content but potentially below modals/side panels */
		box-shadow:
			0 3px 6px rgba(0, 0, 0, 0.16),
			0 3px 6px rgba(0, 0, 0, 0.23);
		border: none; /* Remove any default button border */
		padding: 0; /* Remove padding, icon centered by flex */
		pointer-events: auto; /* Ensure it's clickable */
	}

	.sequence-overlay-button:hover {
		background-color: var(
			--tkc-button-panel-background-hover,
			#3c3c41
		); /* Slightly lighter on hover */
		transform: translateY(-2px) scale(1.05);
		box-shadow:
			0 6px 12px rgba(0, 0, 0, 0.2),
			0 4px 8px rgba(0, 0, 0, 0.26);
	}

	.sequence-overlay-button:active {
		transform: translateY(0px) scale(1); /* Click down effect */
		background-color: var(--tkc-button-panel-background-active, #1e1e21); /* Darker when pressed */
		box-shadow:
			0 1px 3px rgba(0, 0, 0, 0.12),
			0 1px 2px rgba(0, 0, 0, 0.24);
	}

	.icon-wrapper {
		background: transparent; /* Ensure wrapper doesn't obscure button background */
		display: flex;
		align-items: center;
		justify-content: center;
		width: auto;
		height: auto;
		color: inherit; /* Inherit color from .sequence-overlay-button */
	}

	.icon-wrapper i {
		font-size: calc(var(--button-size-factor, 1) * var(--base-icon-size)); /* Dynamic icon size */
		/* Color is inherited from .sequence-overlay-button via .icon-wrapper */
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.sequence-overlay-button {
			--button-size-factor: 0.9;
		}
	}

	@media (max-width: 480px) {
		.sequence-overlay-button {
			--button-size-factor: 0.8;
		}
	}
</style>
