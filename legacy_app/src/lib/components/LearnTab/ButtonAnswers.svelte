<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let options: any[] = [];
	export let disabled: boolean = false;

	const dispatch = createEventDispatcher<{
		select: any;
	}>();

	function handleSelect(option: any) {
		if (!disabled) {
			dispatch('select', option);
		}
	}
</script>

<div class="button-answers">
	{#each options as option}
		<button class="answer-button" on:click={() => handleSelect(option)} {disabled}>
			{option}
		</button>
	{/each}
</div>

<style>
	.button-answers {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: 1rem;
		margin-top: 1rem;
	}

	.answer-button {
		font-size: 1.5rem;
		min-width: 4rem;
		padding: 1rem 1.5rem;
		border-radius: 8px;
		border: none;
		background-color: var(--color-surface-700, #2d2d2d);
		color: var(--color-text, white);
		cursor: pointer;
		transition:
			transform 0.15s,
			background-color 0.15s;
	}

	.answer-button:hover:not(:disabled) {
		background-color: var(--color-surface-600, #3d3d3d);
		transform: translateY(-3px);
	}

	.answer-button:active:not(:disabled) {
		transform: translateY(0);
	}

	.answer-button:disabled {
		opacity: 0.7;
		cursor: not-allowed;
	}
</style>
