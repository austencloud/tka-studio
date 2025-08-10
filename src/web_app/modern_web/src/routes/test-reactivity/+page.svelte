<!-- Minimal test to isolate reactivity issue -->
<script>
	import { createOptionPickerRunes } from '$lib/components/construct/option-picker/optionPickerRunes.svelte.ts';

	// Test 1: Direct state access
	const state = createOptionPickerRunes();
	
	// Test 2: Effect with direct access
	$effect(() => {
		console.log('🔄 Test effect running:', {
			optionsLength: state.optionsData.length,
			timestamp: new Date().toLocaleTimeString()
		});
	});

	// Test 3: Manual trigger
	function loadTestOptions() {
		console.log('🧪 Manually setting test options');
		state.setOptions([
			{ id: 1, letter: 'A', name: 'Test Option 1' },
			{ id: 2, letter: 'B', name: 'Test Option 2' },
			{ id: 3, letter: 'C', name: 'Test Option 3' }
		]);
	}

	// Test 4: Load from start position
	function loadFromStartPosition() {
		console.log('🧪 Loading from start position');
		state.loadOptions([]);
	}
</script>

<h1>Reactivity Test</h1>

<div>
	<h2>Current State</h2>
	<p>Options count: {state.optionsData.length}</p>
	<p>First option: {state.optionsData[0]?.letter || 'none'}</p>
</div>

<div>
	<h2>Actions</h2>
	<button onclick={loadTestOptions}>Load Test Options</button>
	<button onclick={loadFromStartPosition}>Load From Start Position</button>
</div>

<div>
	<h2>Options List</h2>
	{#each state.optionsData as option}
		<div>{option.letter}: {option.name}</div>
	{/each}
</div>
