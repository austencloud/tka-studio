<!--
Test page for the new sectioned OptionPicker component
-->
<script lang="ts">
	import OptionPickerContainer from '$lib/components/construct/OptionPickerContainer.svelte';
	import type { PictographData } from '$lib/domain/PictographData';
	// Set up real start position data for testing
	import { onMount } from 'svelte';

	let testStatus = $state('Initializing...');

	// Real start position data that should trigger option loading
	const realStartPosition = {
		id: 'start-pos-alpha1_alpha1-0',
		letter: 'α',
		endPos: 'TL', // This should match CSV data
		pictograph_data: {
			id: 'start-pos-alpha1_alpha1-0',
			letter: 'α',
			motions: {
				blue: {
					motionType: 'static',
					endLocation: 'TL',
					turns: 0,
				},
				red: {
					motionType: 'static',
					endLocation: 'TL',
					turns: 0,
				},
			},
		},
	};

	onMount(() => {
		// Set up localStorage with real start position
		localStorage.setItem('start_position', JSON.stringify(realStartPosition));
		testStatus = 'Start position loaded into localStorage';

		// Dispatch start position selected event to trigger option loading
		setTimeout(() => {
			const event = new CustomEvent('start-position-selected', {
				detail: realStartPosition,
				bubbles: true,
			});
			document.dispatchEvent(event);
			testStatus = 'Start position event dispatched - should trigger option loading';
			console.log('🎯 Test: Dispatched start-position-selected event', realStartPosition);
		}, 1000);
	});

	function handleOptionSelected(option: PictographData) {
		console.log('Option selected:', option);
		alert(`Selected: ${option.letter} (${option.id})`);
		testStatus = `Option selected: ${option.letter} (${option.id})`;
	}

	function manuallyTriggerStartPosition() {
		// Clear localStorage first
		localStorage.removeItem('start_position');

		// Set new start position
		localStorage.setItem('start_position', JSON.stringify(realStartPosition));

		// Dispatch event
		const event = new CustomEvent('start-position-selected', {
			detail: realStartPosition,
			bubbles: true,
		});
		document.dispatchEvent(event);

		testStatus = 'Manually triggered start position loading';
		console.log('🎯 Manual trigger: start-position-selected event dispatched');
	}
</script>

<svelte:head>
	<title>Option Picker Test</title>
</svelte:head>

<div class="test-page">
	<div class="test-header">
		<h1>Option Picker Component Test</h1>
		<p>Testing the new desktop-style sectioned option picker with real data</p>
		<div class="test-status">
			<strong>Status:</strong>
			{testStatus}
		</div>
		<button class="trigger-button" onclick={manuallyTriggerStartPosition}>
			🔄 Manually Trigger Start Position Loading
		</button>
	</div>

	<div class="test-container">
		<OptionPickerContainer onOptionSelected={handleOptionSelected} />
	</div>
</div>

<style>
	.test-page {
		min-height: 100vh;
		padding: 20px;
		background: #f5f5f5;
		font-family:
			system-ui,
			-apple-system,
			sans-serif;
	}

	.test-header {
		text-align: center;
		margin-bottom: 30px;
		padding: 20px;
		background: white;
		border-radius: 8px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	.test-header h1 {
		color: #333;
		margin: 0 0 10px 0;
	}

	.test-header p {
		color: #666;
		margin: 0 0 15px 0;
	}

	.test-status {
		background: #f0f9ff;
		border: 1px solid #0ea5e9;
		border-radius: 6px;
		padding: 10px;
		margin: 15px 0;
		color: #0c4a6e;
		font-size: 14px;
	}

	.trigger-button {
		background: #2563eb;
		color: white;
		border: none;
		border-radius: 6px;
		padding: 10px 20px;
		cursor: pointer;
		font-size: 14px;
		font-weight: 500;
		transition: background-color 0.2s ease;
	}

	.trigger-button:hover {
		background: #1d4ed8;
	}

	.test-container {
		max-width: 1200px;
		margin: 0 auto 30px auto;
		height: 900px;
		background: white;
		border-radius: 8px;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
		padding: 20px;
	}
</style>
