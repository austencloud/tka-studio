<script lang="ts">
	import { writable, get } from 'svelte/store'; // Import get
	import { FoldableDeviceUtils } from '$lib/utils/deviceDetection';
	import { onMount } from 'svelte'; // Import onMount

	// Local state for simulation controls
	let simulateFoldable = writable(false); // Initialize to false
	let simulatedFoldableType = writable<'zfold' | 'other'>('zfold');
	let simulatedFoldState = writable<boolean>(true); // Default to unfolded

	// Track if an override is currently active (read from localStorage on mount)
	let isOverrideActive = writable(false);

	onMount(() => {
		try {
			const existingOverride = localStorage.getItem('foldableDeviceOverride');
			if (existingOverride) {
				isOverrideActive.set(true);
				simulateFoldable.set(true); // Sync toggle state if override exists
				const settings = JSON.parse(existingOverride);
				simulatedFoldableType.set(settings.foldableType || 'zfold');
				simulatedFoldState.set(settings.isUnfolded ?? true); // Use ?? true for default
			} else {
				isOverrideActive.set(false);
				simulateFoldable.set(false); // Ensure toggle is off if no override
			}
		} catch (e) {
			console.error('Error reading existing foldable override:', e);
			isOverrideActive.set(false);
			simulateFoldable.set(false);
		}
	});

	function handleApplyOrClear() {
		const shouldSimulate = get(simulateFoldable); // Get current toggle state

		if (shouldSimulate) {
			// Apply the override
			FoldableDeviceUtils.setManualOverride({
				isFoldable: true,
				foldableType: get(simulatedFoldableType),
				isUnfolded: get(simulatedFoldState)
			});

			// Message to user that reload is required
			const needsReload = confirm(
				'Foldable device simulation settings applied! Page reload required to see changes. Reload now?'
			);
			if (needsReload) {
				window.location.reload();
			} else {
				// If they don't reload, update the active state indicator
				isOverrideActive.set(true);
			}
		} else {
			// Clear the override
			FoldableDeviceUtils.clearManualOverride();
			const needsReload = confirm(
				'Foldable device simulation disabled! Page reload required to remove the override. Reload now?'
			);
			if (needsReload) {
				window.location.reload();
			} else {
				// If they don't reload, update the active state indicator
				isOverrideActive.set(false);
			}
		}
	}

	// Reactive statement to derive button text and action message
	$: actionButtonText = $simulateFoldable ? 'Apply Simulation' : 'Clear Simulation';
	$: actionMessage = $simulateFoldable
		? 'Apply the selected foldable settings.'
		: 'Remove any active foldable simulation.';

</script>

<div class="foldable-test-controls">
	<div class="test-header">
		Test Foldable Detection
		{#if $isOverrideActive}
			<span class="active-indicator">(Override Active)</span>
		{/if}
	</div>
	<label class="switch">
		<input type="checkbox" bind:checked={$simulateFoldable} />
		<span class="slider"></span>
		<span class="label">Simulate Foldable Device</span>
	</label>

	{#if $simulateFoldable}
		<div class="test-options">
			<label>
				<span>Type:</span>
				<select bind:value={$simulatedFoldableType}>
					<option value="zfold">Z Fold</option>
					<option value="other">Other</option>
				</select>
			</label>
			<label>
				<span>State:</span>
				<select bind:value={$simulatedFoldState}>
					<option value={true}>Unfolded</option>
					<option value={false}>Folded</option>
				</select>
			</label>
		</div>
	{/if}

	<button class="apply-button" on:click={handleApplyOrClear} title={actionMessage}>
		{actionButtonText} & Reload
	</button>
</div>

<style>
	.foldable-test-controls {
		margin-top: 12px;
		padding: 10px;
		background-color: #1e293b;
		border: 1px dashed #475569;
		border-radius: 4px;
	}

	.test-header {
		font-weight: bold;
		color: #7dd3fc;
		margin-bottom: 8px;
		font-size: 11px;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.active-indicator {
		font-size: 9px;
		color: #10b981; /* Green */
		font-style: italic;
		font-weight: normal;
	}

	.switch {
		position: relative;
		display: inline-flex;
		align-items: center;
		margin-bottom: 10px; /* Increased margin */
		cursor: pointer;
		width: 100%; /* Make label clickable */
	}

	.switch input {
		opacity: 0;
		width: 0;
		height: 0;
	}

	.slider {
		position: relative;
		display: inline-block;
		width: 30px;
		height: 16px;
		background-color: #334155;
		border-radius: 34px;
		margin-right: 8px;
		transition: 0.4s;
		flex-shrink: 0; /* Prevent slider from shrinking */
	}

	.slider:before {
		position: absolute;
		content: '';
		height: 12px;
		width: 12px;
		left: 2px;
		bottom: 2px;
		background-color: white;
		border-radius: 50%;
		transition: 0.4s;
	}

	input:checked + .slider {
		background-color: #0ea5e9; /* Light blue when checked */
	}

	input:checked + .slider:before {
		transform: translateX(14px);
	}

	.label {
		color: #e2e8f0;
		font-size: 11px;
		flex-grow: 1; /* Allow label text to take remaining space */
	}

	.test-options {
		display: flex;
		flex-direction: column;
		gap: 8px;
		margin-top: 0px; /* Reduced top margin */
		margin-bottom: 10px;
		padding-left: 5px; /* Indent options slightly */
		border-left: 2px solid #334155; /* Add visual separation */
		margin-left: 15px; /* Align with slider */
	}

	.test-options label {
		display: flex;
		align-items: center;
		justify-content: space-between;
		font-size: 11px;
	}
	.test-options label span {
		color: #94a3b8; /* Lighter color for option labels */
	}

	.test-options select {
		background-color: #0f172a;
		border: 1px solid #334155;
		border-radius: 3px;
		color: #e2e8f0;
		padding: 2px 4px;
		font-size: 10px;
		width: 65%; /* Adjusted width */
	}

	.apply-button {
		background-color: #0c4a6e; /* Darker blue */
		color: white;
		border: none;
		border-radius: 3px;
		padding: 5px 10px; /* Slightly larger padding */
		font-size: 11px; /* Slightly larger font */
		font-weight: 500;
		cursor: pointer;
		width: 100%;
		transition: background-color 0.2s;
		margin-top: 5px; /* Add some space above button */
	}

	.apply-button:hover {
		background-color: #075985; /* Slightly lighter blue on hover */
	}


</style>
