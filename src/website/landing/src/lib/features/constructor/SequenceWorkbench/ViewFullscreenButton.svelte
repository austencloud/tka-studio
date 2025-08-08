<!-- src/lib/components/SequenceWorkbench/ViewFullscreenButton.svelte -->
<script lang="ts">
	import { fly } from 'svelte/transition';
	import { createEventDispatcher } from 'svelte';

	// Event dispatcher
	const dispatch = createEventDispatcher<{
		viewFullscreen: void;
	}>();

	function handleClick() {
		dispatch('viewFullscreen');
	}
</script>

<button
	class="fullscreen-button ripple"
	on:click={handleClick}
	aria-label="View fullscreen"
	data-mdb-ripple="true"
	data-mdb-ripple-color="light"
	in:fly={{ x: 20, duration: 300, delay: 200 }}
>
	<div class="icon-wrapper">
		<i class="fa-solid fa-expand"></i>
	</div>
</button>

<style>
	.fullscreen-button {
		/* Base sizes for dynamic scaling - match other buttons */
		--base-size: 45px; /* Base size of the button */
		--base-icon-size: 19px; /* Base size of the icon */
		--base-margin: 10px; /* Base margin from corner */

		position: absolute;
		bottom: calc(var(--button-size-factor, 1) * var(--base-margin));
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
			--tkc-icon-color-fullscreen,
			#4cc9f0
		); /* Blue icon color, matching the original fullscreen button */

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

	.fullscreen-button:hover {
		background-color: var(
			--tkc-button-panel-background-hover,
			#3c3c41
		); /* Slightly lighter on hover */
		transform: translateY(-2px) scale(1.05);
		box-shadow:
			0 6px 12px rgba(0, 0, 0, 0.2),
			0 4px 8px rgba(0, 0, 0, 0.26);
	}

	.fullscreen-button:active {
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
		color: inherit; /* Inherit color from .fullscreen-button */
	}

	.icon-wrapper i.fa-expand {
		font-size: calc(var(--button-size-factor, 1) * var(--base-icon-size)); /* Dynamic icon size */
		/* Color is inherited from .fullscreen-button via .icon-wrapper */
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.fullscreen-button {
			--button-size-factor: 0.9;
		}
	}

	@media (max-width: 480px) {
		.fullscreen-button {
			--button-size-factor: 0.8;
		}
	}
</style>
