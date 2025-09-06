<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import type { LessonMode } from '$lib/state/stores/learn/learnStore';

	export let selected: LessonMode = 'fixed_question';

	const dispatch = createEventDispatcher<{
		change: LessonMode;
	}>();

	function handleSelect(mode: LessonMode) {
		if (mode !== selected) {
			selected = mode;
			dispatch('change', mode);
		}
	}
</script>

<div class="mode-toggle">
	<button
		class="toggle-button {selected === 'fixed_question' ? 'selected' : ''}"
		on:click={() => handleSelect('fixed_question')}
		aria-pressed={selected === 'fixed_question'}
	>
		Fixed Questions
	</button>

	<button
		class="toggle-button {selected === 'countdown' ? 'selected' : ''}"
		on:click={() => handleSelect('countdown')}
		aria-pressed={selected === 'countdown'}
	>
		Countdown
	</button>
</div>

<style>
	.mode-toggle {
		display: flex;
		border-radius: 6px;
		overflow: hidden;
		border: 1px solid var(--color-border, #444);
	}

	.toggle-button {
		padding: 0.5rem 1rem;
		background: none;
		border: none;
		cursor: pointer;
		font-size: 0.9rem;
		color: var(--color-text, white);
		transition: background-color 0.2s ease;
	}

	.toggle-button.selected {
		background-color: var(--color-primary, #3e63dd);
	}

	.toggle-button:not(.selected) {
		background-color: var(--color-surface-700, #2d2d2d);
	}

	.toggle-button:not(.selected):hover {
		background-color: var(--color-surface-600, #3d3d3d);
	}
</style>
