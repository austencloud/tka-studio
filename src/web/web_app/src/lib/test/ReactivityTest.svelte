<script lang="ts">
	// Import the ACTUAL runes function to test it in isolation
	import { createOptionPickerRunes } from '$lib/components/construct/option-picker/optionPickerRunes.svelte';

	console.log('🔧 Test: Importing real createOptionPickerRunes function');

	// Create test runes instance using the REAL runes function
	const testRunes = createOptionPickerRunes();
	console.log('🔧 Test: Real runes created:', !!testRunes);

	// Test component reactivity using EXACT OptionPicker pattern
	let effectiveOptions = $state<any[]>([]);
	let groupedOptions = $state<Record<string, any[]>>({});

	// Helper function - same as OptionPicker
	function getLetterType(letter: any) {
		if (!letter) return 'Unknown';
		// Simplified grouping for test
		if (letter >= 'A' && letter <= 'F') return 'Type1';
		if (letter >= 'G' && letter <= 'L') return 'Type2';
		return 'Type3';
	}

	$effect(() => {
		console.log('🔍 Test component $effect called');
		// EXACT same pattern as OptionPicker - access through const object
		const allOptions = testRunes.allOptions || [];
		const loadingState = testRunes.isLoading;

		console.log('🔍 Test component updating:', {
			optionsLength: allOptions.length,
			isLoading: loadingState,
			timestamp: new Date().toLocaleTimeString(),
		});

		effectiveOptions = [...allOptions];

		// Group options using legacy pattern (same as OptionPicker)
		const groups: Record<string, any[]> = {};
		allOptions.forEach((option) => {
			const groupKey = getLetterType(option.letter);
			if (!groups[groupKey]) groups[groupKey] = [];
			groups[groupKey].push(option);
		});

		// Sort keys in the same order as OptionPicker
		const sortedKeys = ['Type1', 'Type2', 'Type3', 'Unknown'];
		const sortedGroups: Record<string, any[]> = {};
		sortedKeys.forEach((key) => {
			if (groups[key]) {
				sortedGroups[key] = groups[key];
			}
		});

		console.log('🔍 Test component grouped result:', {
			groupKeys: Object.keys(sortedGroups),
			groupCounts: Object.entries(sortedGroups).map(
				([key, opts]) => `${key}: ${(opts as any[]).length}`
			),
		});

		groupedOptions = { ...sortedGroups };
	});

	function triggerLoad() {
		console.log('🎯 Triggering real loadOptions...');
		// Call the real loadOptions function with an empty sequence (same as OptionPicker)
		testRunes.loadOptions([]);
	}

	console.log('✅ Test component initialized');
</script>

<div class="test-container">
	<h2>Reactivity Test</h2>

	<button onclick={triggerLoad}>Load Options</button>

	<div class="results">
		<h3>Results:</h3>
		<p>Options Count: {effectiveOptions.length}</p>
		<p>Is Loading: {testRunes.isLoading}</p>
		<p>Groups: {Object.keys(groupedOptions).length}</p>
		{#each Object.entries(groupedOptions) as [groupKey, options]}
			<p>{groupKey}: {options.length} options</p>
		{/each}
	</div>

	<div class="debug">
		<h3>Debug Info:</h3>
		<p>Direct runes access:</p>
		<p>testRunes.allOptions.length: {testRunes.allOptions.length}</p>
		<p>testRunes.isLoading: {testRunes.isLoading}</p>
		<p>First few options: {JSON.stringify(effectiveOptions.slice(0, 3))}</p>
	</div>
</div>

<style>
	.test-container {
		padding: 20px;
		border: 2px solid #333;
		margin: 20px;
		background: #1a1a1a;
		color: white;
	}

	.results,
	.debug {
		margin: 20px 0;
		padding: 10px;
		border: 1px solid #555;
		background: #2a2a2a;
	}

	button {
		padding: 10px 20px;
		background: #4a4a4a;
		color: white;
		border: 1px solid #666;
		cursor: pointer;
	}

	button:hover {
		background: #5a5a5a;
	}
</style>
