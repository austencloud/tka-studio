<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher<{
		click: void;
	}>();

	export let ariaLabel = 'Start over';
</script>

<button class="start-over-button" aria-label={ariaLabel} on:click={() => dispatch('click')}>
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
			<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"></path>
			<path d="M21 3v5h-5"></path>
			<path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"></path>
			<path d="M8 16H3v5"></path>
		</svg>
	</span>
	<span class="label">
		<slot>Start Over</slot>
	</span>
</button>

<style>
	.start-over-button {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem 1rem;
		background-color: var(--color-primary, #3e63dd);
		color: white;
		border: none;
		border-radius: 6px;
		cursor: pointer;
		font-weight: 500;
		transition:
			background-color 0.2s,
			transform 0.1s;
	}

	.start-over-button:hover {
		background-color: var(--color-primary-dark, #2a4cbb);
	}

	.start-over-button:active {
		transform: translateY(1px);
	}

	.icon {
		display: flex;
		align-items: center;
	}
</style>
