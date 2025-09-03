<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher<{
		click: void;
	}>();

	export let ariaLabel = 'Go back';
</script>

<button class="back-button" aria-label={ariaLabel} on:click={() => dispatch('click')}>
	<span class="icon">
		<svg
			xmlns="http://www.w3.org/2000/svg"
			width="16"
			height="16"
			viewBox="0 0 24 24"
			fill="none"
			stroke="currentColor"
			stroke-width="2"
			stroke-linecap="round"
			stroke-linejoin="round"
		>
			<line x1="19" y1="12" x2="5" y2="12"></line>
			<polyline points="12 19 5 12 12 5"></polyline>
		</svg>
	</span>
	<span class="label">
		<slot>Back</slot>
	</span>
</button>

<style>
	.back-button {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem 1rem;
		background-color: var(--color-surface-800, #1d1d1d);
		color: var(--color-text, white);
		border: none;
		border-radius: 6px;
		cursor: pointer;
		transition:
			background-color 0.2s,
			transform 0.1s;
	}

	.back-button:hover {
		background-color: var(--color-surface-700, #2d2d2d);
	}

	.back-button:active {
		transform: translateY(1px);
	}

	.icon {
		display: flex;
		align-items: center;
	}
</style>
