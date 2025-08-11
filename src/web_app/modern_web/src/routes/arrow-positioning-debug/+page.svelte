<!--
Arrow Positioning Debug Test

Simple test to verify arrow positioning works with real CSV data.
Uses the same pattern as PictographDemo.svelte.
-->
<script lang="ts">
	import Pictograph from '$lib/components/pictograph/Pictograph.svelte';
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

	// Available positions from CSV data
	const availablePositions = ['alpha3', 'alpha5', 'alpha7', 'alpha1'];
	let selectedPosition = $state('alpha3');

	// Current pictograph
	const currentPictograph = $derived(() => {
		return pictographs[selectedIndex] || null;
	});

	// Position measurements
	let positionMeasurements: Record<string, any> = $state({});

	// Logging function
	function addLog(message: string, data?: unknown) {
		const timestamp = new Date().toLocaleTimeString();
		const logEntry = `[${timestamp}] ${message}${data ? ': ' + JSON.stringify(data, null, 2) : ''}`;
		debugLogs = [...debugLogs, logEntry];
		console.log(`🔍 DEBUG: ${message}`, data || '');
	}

	// Load pictographs for a position
	async function loadPictographsForPosition(position: string) {
		try {
			addLog('=== LOADING REAL PICTOGRAPHS FROM CSV ===');
			addLog('Position', position);

			// Create and initialize OptionDataService (same as PictographDemo)
			const optionDataService = new OptionDataService();
			await optionDataService.initialize();
			addLog('OptionDataService initialized');

			// Get real pictographs for this position
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

			// Store pictographs and reset selection
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

	// Initialize on mount
	onMount(async () => {
		addLog('=== ARROW POSITIONING DEBUG TEST STARTED ===');
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

	function clearLogs() {
		debugLogs = [];
	}

	// Measure actual arrow positions and compare with expected adjustments
	async function measureArrowPositions() {
		if (!currentPictograph()) return;

		addLog('=== MEASURING ARROW POSITIONS ===');

		const pictograph = currentPictograph()!;
		positionMeasurements = {};

		// Check each arrow
		for (const [color, arrowData] of Object.entries(pictograph.arrows || {})) {
			if (!arrowData || !arrowData.is_visible) continue;

			const motionData = pictograph.motions?.[color as keyof typeof pictograph.motions];
			if (!motionData) continue;

			addLog(`--- ${color.toUpperCase()} ARROW ANALYSIS ---`);

			// Current position from arrow data
			const currentPos = {
				x: arrowData.position_x || 0,
				y: arrowData.position_y || 0,
			};
			addLog(`Current position`, currentPos);

			// Motion data details
			addLog(`Motion data`, {
				motion_type: motionData.motion_type,
				start_loc: motionData.start_loc,
				end_loc: motionData.end_loc,
				turns: motionData.turns,
				start_ori: motionData.start_ori,
				end_ori: motionData.end_ori,
			});

			// Look up expected adjustment from placement data
			const letter = pictograph.letter || '';
			const turns = motionData.turns || 1;
			const motionType = motionData.motion_type;

			addLog(`Looking up placement data for`, {
				letter: letter,
				turns: turns,
				motion_type: motionType,
				grid_mode: 'diamond',
			});

			// Test the positioning pipeline directly
			try {
				addLog(`Testing positioning pipeline directly...`);

				// Import positioning services and factory
				const { createPositioningOrchestrator } = await import(
					'$lib/services/positioning/PositioningServiceFactory'
				);

				// Create orchestrator with proper dependencies
				const orchestrator = createPositioningOrchestrator();

				// Calculate position using the same method as the system
				const [calculatedX, calculatedY, calculatedRotation] =
					orchestrator.calculateArrowPosition(arrowData, pictograph, motionData);

				addLog(`Positioning pipeline result`, {
					calculated_x: calculatedX,
					calculated_y: calculatedY,
					calculated_rotation: calculatedRotation,
				});

				// Test the full positioning update
				const updatedPictograph = orchestrator.calculateAllArrowPositions(pictograph);
				const updatedArrow = updatedPictograph.arrows?.[color];
				if (updatedArrow) {
					addLog(`Updated arrow data`, {
						position_x: updatedArrow.position_x,
						position_y: updatedArrow.position_y,
						rotation_angle: updatedArrow.rotation_angle,
					});
				}

				// Expected layer2 base positions
				const expectedLayer2 = {
					w: { x: 331.9, y: 331.9 }, // WEST
					e: { x: 618.1, y: 618.1 }, // EAST
					n: { x: 618.1, y: 331.9 }, // NORTH -> NE
					s: { x: 331.9, y: 618.1 }, // SOUTH -> SW
				};

				const startLoc = motionData.start_loc;
				const expectedBase = expectedLayer2[startLoc as keyof typeof expectedLayer2];

				if (expectedBase) {
					addLog(`Expected layer2 base for ${startLoc}`, expectedBase);

					// Expected adjustment for pro motion, 1 turn: [-85, 80]
					const expectedAdjustment = { x: -85, y: 80 };
					const expectedFinal = {
						x: expectedBase.x + expectedAdjustment.x,
						y: expectedBase.y + expectedAdjustment.y,
					};

					addLog(`Expected final position`, expectedFinal);
					addLog(`Difference from expected`, {
						x_diff: calculatedX - expectedFinal.x,
						y_diff: calculatedY - expectedFinal.y,
					});
				}
			} catch (error) {
				addLog(`❌ Positioning pipeline failed`, {
					error: error instanceof Error ? error.message : String(error),
				});
			}

			// Store measurements
			positionMeasurements[color] = {
				current_position: currentPos,
				motion_data: {
					motion_type: motionType,
					start_loc: motionData.start_loc,
					end_loc: motionData.end_loc,
					turns: turns,
				},
				letter: letter,
			};
		}

		addLog('Position measurements complete', positionMeasurements);
	}
</script>

<svelte:head>
	<title>Arrow Positioning Debug Test</title>
</svelte:head>

<div class="debug-container">
	<h1>Arrow Positioning Debug Test</h1>
	<p><strong>Testing:</strong> Real CSV data → PictographData → Rendered Pictograph</p>

	<div class="status">
		<span class="indicator" class:loaded={isLoaded} class:error={errorMessage}></span>
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
		<button onclick={measureArrowPositions}>Measure Positions</button>
	</div>

	<div class="content">
		<!-- Pictograph Display -->
		<div class="pictograph-section">
			<h3>Rendered Pictograph</h3>
			{#if currentPictograph()}
				<div class="pictograph-info">
					<p><strong>Letter:</strong> {currentPictograph()?.letter}</p>
					<p><strong>ID:</strong> {currentPictograph()?.id}</p>
					<p><strong>Position:</strong> {selectedPosition}</p>
				</div>
				<div class="pictograph-display">
					<Pictograph
						pictographData={currentPictograph()}
						width={400}
						height={400}
						debug={true}
					/>
				</div>
			{:else}
				<p>No pictograph data available</p>
			{/if}
		</div>

		<!-- Position Measurements -->
		<div class="measurements-section">
			<h3>Position Measurements</h3>
			{#if Object.keys(positionMeasurements).length > 0}
				<div class="measurements">
					{#each Object.entries(positionMeasurements) as [color, data]}
						<div class="measurement-item">
							<h4>{color.toUpperCase()} Arrow</h4>
							<p>
								<strong>Current Position:</strong> ({data.current_position.x}, {data
									.current_position.y})
							</p>
							<p>
								<strong>Motion:</strong>
								{data.motion_data.motion_type} | {data.motion_data.start_loc} → {data
									.motion_data.end_loc} | {data.motion_data.turns} turns
							</p>
							<p><strong>Letter:</strong> {data.letter}</p>
						</div>
					{/each}
				</div>
			{:else}
				<p>Click "Measure Positions" to analyze arrow placement</p>
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

	.indicator.error {
		background: #ef4444;
	}

	.error-text {
		color: #ef4444;
		font-weight: 500;
	}

	.controls {
		display: flex;
		gap: 1rem;
		align-items: center;
		margin: 1rem 0;
		padding: 1rem;
		background: #f8fafc;
		border-radius: 8px;
	}

	.control-group {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.control-group label {
		font-weight: 500;
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
		grid-template-columns: 1fr 1fr 1fr;
		gap: 1.5rem;
		margin-top: 2rem;
	}

	.pictograph-section,
	.measurements-section,
	.logs-section {
		border: 1px solid #e5e7eb;
		border-radius: 8px;
		padding: 1rem;
	}

	.measurements {
		max-height: 400px;
		overflow-y: auto;
	}

	.measurement-item {
		background: #f8fafc;
		border: 1px solid #e2e8f0;
		border-radius: 4px;
		padding: 0.75rem;
		margin-bottom: 0.75rem;
	}

	.measurement-item h4 {
		margin: 0 0 0.5rem 0;
		color: #1f2937;
		font-size: 0.9rem;
	}

	.measurement-item p {
		margin: 0.25rem 0;
		font-size: 0.8rem;
		color: #374151;
	}

	.pictograph-info {
		margin-bottom: 1rem;
		font-size: 0.9rem;
	}

	.pictograph-info p {
		margin: 0.25rem 0;
	}

	.pictograph-display {
		border: 1px solid #d1d5db;
		border-radius: 4px;
		display: flex;
		justify-content: center;
		align-items: center;
		background: white;
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
		word-break: break-word;
	}

	h1 {
		color: #1f2937;
		margin-bottom: 0.5rem;
	}

	h3 {
		color: #374151;
		margin-top: 0;
		margin-bottom: 1rem;
	}
</style>
