<!--
Simple Pictograph Test
Just shows a pictograph to verify arrows are visible
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

	// Current pictograph
	const currentPictograph = $derived(() => {
		return pictographs[selectedIndex] || null;
	});

	// Logging function
	function addLog(message: string, data?: unknown) {
		const timestamp = new Date().toLocaleTimeString();
		const logEntry = `[${timestamp}] ${message}${data ? ': ' + JSON.stringify(data, null, 2) : ''}`;
		debugLogs = [...debugLogs, logEntry];
		console.log(`🔍 SIMPLE TEST: ${message}`, data || '');
	}

	// Clear logs
	function clearLogs() {
		debugLogs = [];
	}

	// Load pictographs
	async function loadPictographs() {
		try {
			addLog('=== LOADING SIMPLE PICTOGRAPH TEST ===');

			const optionDataService = new OptionDataService();
			await optionDataService.initialize();
			addLog('OptionDataService initialized');

			const options = await optionDataService.getNextOptionsFromEndPosition(
				'alpha3',
				DomainGridMode.DIAMOND
			);
			addLog('Pictographs loaded', { count: options.length });

			if (options.length === 0) {
				throw new Error('No pictographs found');
			}

			pictographs = options;
			selectedIndex = 0;

			const current = currentPictograph();
			addLog('Current pictograph selected', {
				letter: current?.letter,
				id: current?.id,
				arrows: Object.keys(current?.arrows || {}),
				motions: Object.keys(current?.motions || {}),
			});

			return options;
		} catch (error) {
			const errorMsg = error instanceof Error ? error.message : String(error);
			addLog('❌ Error loading pictographs', { error: errorMsg });
			errorMessage = errorMsg;
			throw error;
		}
	}

	// Initialize on mount
	onMount(async () => {
		addLog('=== SIMPLE PICTOGRAPH TEST STARTED ===');

		try {
			await loadPictographs();
			isLoaded = true;
			addLog('✅ Test initialization complete');
		} catch (error) {
			errorMessage = error instanceof Error ? error.message : String(error);
			addLog('❌ Test initialization failed', { error: errorMessage });
		}
	});
</script>

<svelte:head>
	<title>Simple Pictograph Test</title>
</svelte:head>

<div class="test-container">
	<h1>Simple Pictograph Test</h1>
	<p>Basic test to verify pictograph and arrow rendering</p>

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

	<div class="content">
		<!-- Pictograph Display -->
		<div class="pictograph-section">
			<h3>Pictograph</h3>
			{#if currentPictograph()}
				<div class="pictograph-info">
					<p><strong>Letter:</strong> {currentPictograph()?.letter}</p>
					<p><strong>ID:</strong> {currentPictograph()?.id}</p>
					<p>
						<strong>Arrows:</strong>
						{Object.keys(currentPictograph()?.arrows || {}).join(', ') || 'None'}
					</p>
					<p>
						<strong>Motions:</strong>
						{Object.keys(currentPictograph()?.motions || {}).join(', ') || 'None'}
					</p>
				</div>
				<div class="pictograph-display">
					<Pictograph
						pictographData={currentPictograph()}
						width={600}
						height={600}
						debug={true}
					/>
				</div>
			{:else}
				<p>No pictograph data available</p>
			{/if}
		</div>

		<!-- Debug Logs -->
		<div class="logs-section">
			<h3>Debug Logs</h3>
			<button onclick={clearLogs}>Clear Logs</button>
			<div class="logs">
				{#each debugLogs as log}
					<div class="log-entry">{log}</div>
				{/each}
			</div>
		</div>
	</div>
</div>

<style>
	.test-container {
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

	.content {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 2rem;
		margin-top: 2rem;
	}

	.pictograph-section,
	.logs-section {
		background: white;
		border: 1px solid #e5e7eb;
		border-radius: 8px;
		padding: 1.5rem;
	}

	.pictograph-info {
		margin-bottom: 1rem;
	}

	.pictograph-info p {
		margin: 0.25rem 0;
		font-size: 0.9rem;
	}

	.pictograph-display {
		border: 1px solid #d1d5db;
		border-radius: 4px;
		display: flex;
		justify-content: center;
		align-items: center;
		background: white;
		min-height: 400px;
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
		margin-top: 1rem;
	}

	.log-entry {
		margin-bottom: 0.5rem;
		white-space: pre-wrap;
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
</style>
