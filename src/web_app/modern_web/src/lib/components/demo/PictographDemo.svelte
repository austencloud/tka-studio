<!--
Pi		c		console.error('❌ Failed to initialize PictographDemo:', error);ole.log('✅ PictographDemo initialized with real data');ographDemo.svelte - Demo 		optionDataSer		await csvDataService.loadCsvData();
		await optionDataService.initialize();

		// Load sample pictographs from real CSV data
		await loadSamplePictographs();

		_isLoading = false;
		console.log('✅ PictographDemo initialized with real data');
	} catch (error) {
		console.error('❌ Failed to initialize PictographDemo:', error);
		_loadingError = error instanceof Error ? error.message : 'Unknown error';
		_isLoading = false;
	}tionDataService();

		await csvDataService.loadCsvData();
		await optionDataService.initialize();

		// Load sample pictographs from real CSV data
		await loadSamplePictographs();

		console.log('✅ PictographDemo initialized with real data');
	} catch (error) {
		console.error('❌ Failed to initialize PictographDemo:', error);
	} REAL CSV data

This component demonstrates the modern pictograph system using actual CSV data
from the TKA system, showing real pictographs with proper motion calculations.
-->
<script lang="ts">
	import { ModernPictograph } from '$lib/components/pictograph';
	import type { PictographData } from '$lib/domain';
	import { GridMode } from '$lib/domain/enums';
	import { CsvDataService } from '$lib/services/implementations/CsvDataService';
	import { OptionDataService } from '$lib/services/implementations/OptionDataService';
	import { onMount } from 'svelte';

	// Demo state using runes
	let selectedDemo = $state('sample');
	let debugMode = $state(false);
	let gridMode = $state<GridMode>(GridMode.DIAMOND);
	let showControls = $state(true);

	// Services
	let csvDataService: CsvDataService | null = null;
	let optionDataService: OptionDataService | null = null;

	// Real pictograph data from CSV
	let samplePictographs = $state<{ [key: string]: PictographData }>({});

	// Initialize services and load real data
	onMount(async () => {
		try {
			console.log('🎨 Initializing PictographDemo with real CSV data...');

			// Initialize services
			csvDataService = new CsvDataService();
			optionDataService = new OptionDataService();

			await csvDataService.loadCsvData();
			await optionDataService.initialize();

			// Load sample pictographs from real CSV data
			await loadSamplePictographs();

			isLoading = false;
			console.log('✅ PictographDemo initialized with real data');
		} catch (error) {
			console.error('❌ Failed to initialize PictographDemo:', error);
			loadingError = error instanceof Error ? error.message : 'Unknown error';
			isLoading = false;
		}
	});

	// Load sample pictographs from real CSV data (simplified to avoid infinite loops)
	async function loadSamplePictographs() {
		if (!optionDataService || !csvDataService) return;

		try {
			console.log('🎨 Loading sample pictographs...');

			// Get a few sample CSV rows directly without triggering option generation
			const diamondData = csvDataService.getParsedData('diamond');

			if (diamondData.length === 0) {
				throw new Error('No diamond CSV data available');
			}

			// Just take the first few rows and convert them directly
			const samples: { [key: string]: PictographData } = {};

			// Take first 3 rows as samples
			const sampleRows = diamondData.slice(0, 3);

			for (let i = 0; i < sampleRows.length; i++) {
				const row = sampleRows[i];
				const sampleKey = i === 0 ? 'sample' : i === 1 ? 'complex' : 'advanced';

				// Use the proper conversion method from OptionDataService
				const convertedPictograph = (
					optionDataService as any
				).convertCsvRowToPictographData(
					row,
					gridMode === GridMode.DIAMOND ? 'diamond' : 'box'
				);

				if (convertedPictograph) {
					// Override the ID to make it demo-specific
					samples[sampleKey] = {
						...convertedPictograph,
						id: `demo-${sampleKey}`,
						beat: 1,
					};
				}
			}

			samplePictographs = samples;
			console.log(
				`✅ Loaded ${Object.keys(samples).length} sample pictographs with real arrows and props`
			);
		} catch (error) {
			console.error('❌ Error loading sample pictographs:', error);
			throw error;
		}
	}

	// Demo options for the selector
	const demoOptions = $derived(() => {
		const options = [{ value: 'sample', label: 'Sample Pictograph' }];

		if (samplePictographs.complex) {
			options.push({ value: 'complex', label: 'Complex Pictograph' });
		}

		if (samplePictographs.advanced) {
			options.push({ value: 'advanced', label: 'Advanced Pictograph' });
		}

		return options;
	});

	// Get current demo data
	const currentPictographData = $derived(() => {
		return samplePictographs[selectedDemo] || null;
	});

	// Load a random pictograph from CSV data
	async function loadRandomPictograph() {
		if (!csvDataService) return;

		try {
			const diamondData = csvDataService.getParsedData('diamond');
			if (diamondData.length === 0) return;

			// Get a random row
			const randomIndex = Math.floor(Math.random() * diamondData.length);
			const randomRow = diamondData[randomIndex];

			// Convert using the proper conversion method
			const convertedPictograph = (optionDataService as any).convertCsvRowToPictographData(
				randomRow,
				gridMode === GridMode.DIAMOND ? 'diamond' : 'box'
			);

			if (convertedPictograph) {
				// Update the sample pictograph
				samplePictographs = {
					...samplePictographs,
					sample: {
						...convertedPictograph,
						id: `demo-random-${Date.now()}`,
						beat: 1,
					},
				};
				console.log(`🎲 Generated random pictograph: ${convertedPictograph.letter}`);
			}
		} catch (error) {
			console.error('❌ Error loading random pictograph:', error);
		}
	}

	// Grid mode change handling removed to prevent infinite loops

	function handlePictographClick() {
		console.log('Pictograph clicked!', selectedDemo);
	}
</script>

<div class="pictograph-demo">
	<h2>Modern Pictograph Demo</h2>

	{#if showControls}
		<!-- Demo Controls -->
		<div class="controls" data-testid="demo-controls">
			<div class="control-group">
				<label for="demo-selector">Demo Type:</label>
				<select id="demo-selector" bind:value={selectedDemo} data-testid="demo-selector">
					{#each demoOptions() as option}
						<option value={option.value}>{option.label}</option>
					{/each}
				</select>
			</div>

			<div class="control-group">
				<label for="grid-mode-selector">Grid Mode:</label>
				<select
					id="grid-mode-selector"
					bind:value={gridMode}
					data-testid="grid-mode-selector"
				>
					<option value={GridMode.DIAMOND}>Diamond</option>
					<option value={GridMode.BOX}>Box</option>
				</select>
			</div>

			<div class="control-group">
				<label>
					<input
						type="checkbox"
						bind:checked={debugMode}
						data-testid="debug-mode-checkbox"
					/>
					Debug Mode
				</label>
			</div>

			<div class="control-group">
				<label>
					<input type="checkbox" bind:checked={showControls} />
					Show Controls
				</label>
			</div>
		</div>
	{/if}

	<!-- Pictograph Display -->
	<div class="demo-grid">
		<!-- Main Pictograph Demo -->
		<div class="demo-item" data-testid="main-pictograph-demo">
			<h3>Real CSV Pictograph: {currentPictographData()?.letter || 'Unknown'}</h3>
			<div class="pictograph-controls">
				<button onclick={loadRandomPictograph} class="generate-btn">
					🎲 Generate Random Pictograph
				</button>
			</div>
			<div class="pictograph-wrapper large" data-testid="main-pictograph">
				{#if currentPictographData()}
					<ModernPictograph
						pictographData={currentPictographData()}
						width={500}
						height={500}
						onClick={handlePictographClick}
						debug={debugMode}
					/>
				{:else}
					<p>No pictograph data available</p>
				{/if}
			</div>
		</div>
	</div>

	<!-- Info Panel -->
	<div class="info-panel">
		<h3>Current Configuration</h3>
		<ul>
			<li>
				<strong>Demo:</strong>
				{demoOptions().find((opt) => opt.value === selectedDemo)?.label}
			</li>
			<li><strong>Grid Mode:</strong> {gridMode}</li>
			<li><strong>Debug:</strong> {debugMode ? 'Enabled' : 'Disabled'}</li>
			<li><strong>Components:</strong> ModernPictograph, Grid, Prop, Arrow, TKAGlyph</li>
			<li><strong>Reactivity:</strong> Pure Svelte 5 Runes</li>
		</ul>

		<div class="data-preview">
			<h4>Sample Data Structure</h4>
			{#if currentPictographData()}
				<div class="data-scroll">
					<pre><code>{JSON.stringify(currentPictographData(), null, 2)}</code></pre>
				</div>
			{:else}
				<p>No data available</p>
			{/if}
		</div>
	</div>

	<!-- Toggle Controls Button -->
	{#if !showControls}
		<button class="toggle-controls" onclick={() => (showControls = true)}>
			Show Controls
		</button>
	{/if}
</div>

<style>
	.pictograph-demo {
		padding: 2rem;
		max-width: 1400px;
		margin: 0 auto;
		font-family: 'Inter', system-ui, sans-serif;
	}

	h2 {
		color: #1f2937;
		margin-bottom: 2rem;
		text-align: center;
	}

	.controls {
		display: flex;
		gap: 1rem;
		margin-bottom: 2rem;
		padding: 1rem;
		background: #f8fafc;
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
		color: #374151;
	}

	.control-group select,
	.control-group input[type='checkbox'] {
		padding: 0.25rem 0.5rem;
		border: 1px solid #d1d5db;
		border-radius: 4px;
	}

	.demo-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
		gap: 2rem;
		margin-bottom: 2rem;
	}

	.demo-item {
		border: 1px solid #e5e7eb;
		border-radius: 12px;
		padding: 1.5rem;
		background: white;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
	}

	.demo-item h3 {
		margin: 0 0 1rem 0;
		color: #1f2937;
		font-size: 1.25rem;
	}

	.pictograph-wrapper {
		display: flex;
		justify-content: center;
		align-items: center;
		min-height: 300px;
	}

	.size-demo {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		align-items: center;
	}

	.size-item {
		text-align: center;
	}

	.size-item h4 {
		margin: 0 0 0.5rem 0;
		color: #6b7280;
		font-size: 0.875rem;
	}

	.info-panel {
		background: #f8fafc;
		border-radius: 12px;
		padding: 1.5rem;
		border: 1px solid #e5e7eb;
	}

	.info-panel h3 {
		margin: 0 0 1rem 0;
		color: #1f2937;
	}

	.info-panel ul {
		list-style: none;
		padding: 0;
		margin: 0 0 1rem 0;
	}

	.info-panel li {
		padding: 0.25rem 0;
		color: #4b5563;
	}

	.data-preview {
		margin-top: 1rem;
	}

	.data-preview h4 {
		margin: 0 0 0.5rem 0;
		color: #374151;
	}

	.data-preview pre {
		background: #1f2937;
		color: #e5e7eb;
		padding: 1rem;
		border-radius: 6px;
		overflow-x: auto;
		font-size: 0.75rem;
		margin: 0;
	}

	.toggle-controls {
		position: fixed;
		top: 1rem;
		right: 1rem;
		padding: 0.5rem 1rem;
		background: #3b82f6;
		color: white;
		border: none;
		border-radius: 6px;
		cursor: pointer;
		font-weight: 500;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	.toggle-controls:hover {
		background: #2563eb;
	}

	.data-scroll {
		max-height: 400px;
		overflow-y: auto;
		border: 1px solid #d1d5db;
		border-radius: 4px;
		background: white;
	}

	.pictograph-controls {
		margin-bottom: 1rem;
		text-align: center;
	}

	.generate-btn {
		background: #3b82f6;
		color: white;
		border: none;
		padding: 0.75rem 1.5rem;
		border-radius: 8px;
		font-size: 0.875rem;
		font-weight: 500;
		cursor: pointer;
		transition: background-color 0.2s;
	}

	.generate-btn:hover {
		background: #2563eb;
	}

	.pictograph-wrapper.large {
		min-height: 500px;
		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>
