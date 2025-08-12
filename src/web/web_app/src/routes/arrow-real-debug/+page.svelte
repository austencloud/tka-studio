<!--
Real Arrow Positioning Debug
Deep debugging of the actual positioning calculation pipeline
-->
<script lang="ts">
	import { arrowPositioningService } from '$lib/components/pictograph/services/arrowPositioningService';
	import type { PictographData } from '$lib/domain';
	import { GridMode as DomainGridMode } from '$lib/domain';
	import { OptionDataService } from '$lib/services/implementations/OptionDataService';
	import { onMount } from 'svelte';

	// State
	let isLoaded = $state(false);
	let errorMessage = $state<string | null>(null);
	let pictographs: PictographData[] = $state([]);
	let selectedIndex = $state(0);
	let debugLogs: string[] = $state([]);
	let positioningResults: Record<string, unknown> = $state({});

	// Available positions from CSV data
	const availablePositions = ['alpha3', 'alpha5', 'alpha7', 'alpha1'];
	let selectedPosition = $state('alpha3');

	// Current pictograph
	const currentPictograph = $derived(() => {
		return pictographs[selectedIndex] || null;
	});

	// Logging function
	function addLog(message: string, data?: unknown) {
		const timestamp = new Date().toLocaleTimeString();
		const logEntry = `[${timestamp}] ${message}${data ? ': ' + JSON.stringify(data, null, 2) : ''}`;
		debugLogs = [...debugLogs, logEntry];
		console.log(`🔍 REAL DEBUG: ${message}`, data || '');
	}

	// Clear logs
	function clearLogs() {
		debugLogs = [];
	}

	// Load pictographs for a position
	async function loadPictographsForPosition(position: string) {
		try {
			addLog('=== LOADING REAL PICTOGRAPHS FROM CSV ===');
			addLog('Position', position);

			const optionDataService = new OptionDataService();
			await optionDataService.initialize();
			addLog('OptionDataService initialized');

			const options = await optionDataService.getNextOptionsFromEndPosition(
				position,
				DomainGridMode.DIAMOND
			);
			addLog('Pictographs loaded', {
				count: options.length,
				position: position,
			});

			if (options.length === 0) {
				throw new Error(`No pictographs found for position ${position}`);
			}

			pictographs = options;
			selectedIndex = 0;

			addLog('Current pictograph', {
				letter: currentPictograph()?.letter,
				id: currentPictograph()?.id,
				has_arrows: Object.keys(currentPictograph()?.arrows || {}).length,
				has_motions: Object.keys(currentPictograph()?.motions || {}).length,
			});

			return options;
		} catch (error) {
			const errorMsg = error instanceof Error ? error.message : String(error);
			addLog('❌ Error loading pictographs', { error: errorMsg });
			errorMessage = errorMsg;
			throw error;
		}
	}

	// Change position
	async function changePosition(newPosition: string) {
		selectedPosition = newPosition;
		await loadPictographsForPosition(newPosition);
	}

	// Change pictograph option
	function changePictograph(newIndex: number) {
		if (newIndex >= 0 && newIndex < pictographs.length) {
			selectedIndex = newIndex;
			addLog('Changed to pictograph', {
				index: selectedIndex,
				letter: currentPictograph()?.letter,
				id: currentPictograph()?.id,
			});
		}
	}

	// Deep test positioning calculations
	async function testPositioningCalculations() {
		const pictograph = currentPictograph();
		if (!pictograph) {
			addLog('❌ No pictograph selected');
			return;
		}

		addLog('=== DEEP POSITIONING CALCULATION TEST ===');
		addLog('Testing pictograph', {
			letter: pictograph.letter,
			id: pictograph.id,
		});

		const results: Record<string, unknown> = {};

		// Test each arrow
		for (const [color, arrowData] of Object.entries(pictograph.arrows || {})) {
			if (!arrowData) continue;

			const motionData = pictograph.motions?.[color];
			if (!motionData) {
				addLog(`❌ No motion data for ${color} arrow`);
				continue;
			}

			addLog(`\n--- TESTING ${color.toUpperCase()} ARROW ---`);
			addLog('Arrow data', {
				motion_type: arrowData.motion_type,
				start_loc: arrowData.start_loc,
				end_loc: arrowData.end_loc,
				turns: arrowData.turns,
				position_x: arrowData.position_x,
				position_y: arrowData.position_y,
			});

			addLog('Motion data', {
				motion_type: motionData.motion_type,
				start_loc: motionData.start_loc,
				end_loc: motionData.end_loc,
				turns: motionData.turns,
			});

			try {
				// Test the positioning service directly
				const calculatedPosition = await arrowPositioningService.calculatePosition(
					arrowData,
					motionData,
					pictograph
				);

				addLog(`✅ Positioning service result for ${color}`, calculatedPosition);

				results[color] = {
					arrow_data: arrowData,
					motion_data: motionData,
					original_position: {
						x: arrowData.position_x,
						y: arrowData.position_y,
						rotation: arrowData.rotation_angle || 0,
					},
					calculated_position: calculatedPosition,
					positioning_used: 'sophisticated_service',
				};
			} catch (error) {
				addLog(`❌ Error calculating position for ${color}`, error);
				results[color] = {
					error: error instanceof Error ? error.message : String(error),
				};
			}
		}

		positioningResults = results;
		addLog('=== POSITIONING TEST COMPLETE ===');
	}

	// Initialize on mount
	onMount(async () => {
		addLog('=== REAL ARROW POSITIONING DEBUG STARTED ===');
		addLog('Using real CSV data via OptionDataService');

		try {
			await loadPictographsForPosition(selectedPosition);
			isLoaded = true;
			addLog('✅ Test initialization complete');
		} catch (error) {
			errorMessage = error instanceof Error ? error.message : String(error);
			addLog('❌ Test initialization failed', { error: errorMessage });
		}
	});
</script>

<svelte:head>
	<title>Real Arrow Positioning Debug</title>
</svelte:head>

<div class="debug-container">
	<h1>Real Arrow Positioning Debug</h1>
	<p>Deep testing of the sophisticated positioning service with real CSV data</p>

	<!-- Status -->
	<div class="status">
		<div class="indicator" class:loaded={isLoaded}></div>
		{#if errorMessage}
			<span class="error-text">Error: {errorMessage}</span>
		{:else if isLoaded}
			<span>✅ Loaded {pictographs.length} pictographs</span>
		{:else}
			<span>Loading...</span>
		{/if}
	</div>

	<div class="controls">
		<!-- Position Selector -->
		<div class="control-group">
			<label for="position">Position:</label>
			<select
				id="position"
				bind:value={selectedPosition}
				onchange={() => changePosition(selectedPosition)}
			>
				{#each availablePositions as position}
					<option value={position}>{position}</option>
				{/each}
			</select>
		</div>

		<!-- Pictograph Selector -->
		{#if pictographs.length > 1}
			<div class="control-group">
				<label for="pictograph">Pictograph:</label>
				<select
					id="pictograph"
					bind:value={selectedIndex}
					onchange={() => changePictograph(selectedIndex)}
				>
					{#each pictographs as pictograph, index}
						<option value={index}>
							{index + 1}. Letter {pictograph.letter} ({pictograph.id})
						</option>
					{/each}
				</select>
			</div>
		{/if}

		<button onclick={clearLogs}>Clear Logs</button>
		<button onclick={testPositioningCalculations}>Test Positioning Calculations</button>
	</div>

	<div class="content">
		<!-- Current Pictograph Info -->
		<div class="pictograph-info-section">
			<h3>Current Pictograph Info</h3>
			{#if currentPictograph()}
				<div class="pictograph-info">
					<p><strong>Letter:</strong> {currentPictograph()?.letter}</p>
					<p><strong>ID:</strong> {currentPictograph()?.id}</p>
					<p><strong>Position:</strong> {selectedPosition}</p>
					<p>
						<strong>Arrows:</strong>
						{Object.keys(currentPictograph()?.arrows || {}).join(', ')}
					</p>
					<p>
						<strong>Motions:</strong>
						{Object.keys(currentPictograph()?.motions || {}).join(', ')}
					</p>
				</div>
			{:else}
				<p>No pictograph data available</p>
			{/if}
		</div>

		<!-- Positioning Results -->
		<div class="results-section">
			<h3>Positioning Calculation Results</h3>
			{#if Object.keys(positioningResults).length > 0}
				<div class="results">
					{#each Object.entries(positioningResults) as [color, data]}
						<div class="result-item">
							<h4>{color.toUpperCase()} Arrow</h4>
							{#if data.error}
								<p class="error-text">Error: {data.error}</p>
							{:else}
								<div class="result-details">
									<p>
										<strong>Original Position:</strong> ({data.original_position
											.x}, {data.original_position.y})
									</p>
									<p>
										<strong>Calculated Position:</strong> ({data
											.calculated_position.x}, {data.calculated_position.y})
									</p>
									<p>
										<strong>Rotation:</strong>
										{data.calculated_position.rotation}°
									</p>
									<p>
										<strong>Position Changed:</strong>
										{data.original_position.x !== data.calculated_position.x ||
										data.original_position.y !== data.calculated_position.y
											? 'YES'
											: 'NO'}
									</p>
									<p>
										<strong>Motion Type:</strong>
										{data.motion_data.motion_type}
									</p>
									<p>
										<strong>Path:</strong>
										{data.motion_data.start_loc} → {data.motion_data.end_loc}
									</p>
									<p><strong>Turns:</strong> {data.motion_data.turns}</p>
								</div>
							{/if}
						</div>
					{/each}
				</div>
			{:else}
				<p>Click "Test Positioning Calculations" to analyze positioning</p>
			{/if}
		</div>

		<!-- Debug Logs -->
		<div class="logs-section">
			<h3>Debug Logs</h3>
			<div class="logs">
				{#each debugLogs as log}
					<div class="log-entry">{log}</div>
				{/each}
			</div>
		</div>
	</div>
</div>

<style>
	.debug-container {
		padding: 2rem;
		max-width: 1200px;
		margin: 0 auto;
		font-family: system-ui, sans-serif;
	}

	.status {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		margin: 1rem 0;
	}

	.indicator {
		width: 12px;
		height: 12px;
		border-radius: 50%;
		background: #ccc;
	}

	.indicator.loaded {
		background: #22c55e;
	}

	.error-text {
		color: #dc2626;
		font-weight: 500;
	}

	.controls {
		display: flex;
		gap: 1rem;
		align-items: center;
		margin: 1rem 0;
		padding: 1rem;
		background: #f3f4f6;
		border-radius: 8px;
		flex-wrap: wrap;
	}

	.control-group {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.control-group label {
		font-weight: 500;
		min-width: 80px;
	}

	.control-group select {
		padding: 0.25rem 0.5rem;
		border: 1px solid #d1d5db;
		border-radius: 4px;
	}

	button {
		padding: 0.5rem 1rem;
		background: #3b82f6;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
	}

	button:hover {
		background: #2563eb;
	}

	.content {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 2rem;
		margin-top: 2rem;
	}

	.pictograph-info-section,
	.results-section,
	.logs-section {
		background: white;
		border: 1px solid #e5e7eb;
		border-radius: 8px;
		padding: 1.5rem;
	}

	.logs-section {
		grid-column: 1 / -1;
	}

	.pictograph-info,
	.results,
	.result-details {
		margin-top: 1rem;
	}

	.pictograph-info p,
	.result-details p {
		margin: 0.25rem 0;
		font-size: 0.9rem;
	}

	.result-item {
		border: 1px solid #d1d5db;
		border-radius: 4px;
		padding: 1rem;
		margin-bottom: 1rem;
	}

	.result-item h4 {
		margin: 0 0 0.5rem 0;
		color: #374151;
	}

	.logs {
		max-height: 400px;
		overflow-y: auto;
		background: #1f2937;
		color: #f9fafb;
		padding: 1rem;
		border-radius: 4px;
		font-family: 'Courier New', monospace;
		font-size: 0.8rem;
	}

	.log-entry {
		margin-bottom: 0.5rem;
		white-space: pre-wrap;
	}
</style>
