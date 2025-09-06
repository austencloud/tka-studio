<!-- src/lib/components/GenerateTab/ui/LevelSelector/LevelSelector.svelte -->
<script lang="ts">
	import { settingsStore } from '../store/settings';
	import LevelButton from './LevelButton.svelte';

	// Export the value property for binding
	export let value: number = 3;

	// Constants
	const MIN_LEVEL = 1;
	const MAX_LEVEL = 5;

	// Level descriptions
	const levelDescriptions = [
		'Beginner friendly patterns',
		'Easy flow with basic transitions',
		'Moderate complexity with varied patterns',
		'Advanced flow with challenging transitions',
		'Expert level with complex combinations'
	];

	// Current description
	$: currentDescription = levelDescriptions[value - 1] || levelDescriptions[0];

	// Set level
	function setLevel(newLevel: number) {
		if (newLevel >= MIN_LEVEL && newLevel <= MAX_LEVEL) {
			value = newLevel;
			settingsStore.setLevel(newLevel);
		}
	}
</script>

<div class="level-selector">
	<div class="header">
		<label for="difficulty-level" id="difficulty-label">Difficulty Level</label>
	</div>

	<div class="levels" role="radiogroup" aria-labelledby="difficulty-label" id="difficulty-level">
		{#each Array(MAX_LEVEL) as _, i}
			{@const levelNum = i + 1}
			<LevelButton
				level={levelNum}
				selected={value === levelNum}
				on:click={() => setLevel(levelNum)}
			/>
		{/each}
	</div>

	<div class="description">
		<p>{currentDescription}</p>
	</div>
</div>

<style>
	.level-selector {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.header {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	label {
		font-size: 0.875rem;
		font-weight: 500;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
	}

	.levels {
		display: flex;
		gap: 0.5rem;
		justify-content: space-between;
	}

	.description {
		font-size: 0.75rem;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.6));
		min-height: 2.5rem;
	}

	.description p {
		margin: 0;
	}
</style>
