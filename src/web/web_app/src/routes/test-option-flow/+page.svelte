<!-- Test page for Start Position to Option Picker flow -->
<script lang="ts">
	import OptionPickerContainer from '$components/construct/OptionPickerContainer.svelte';
	import StartPositionPicker from '$components/construct/StartPositionPicker.svelte';
	import type { BeatData } from '$domain/BeatData';
	import type { PictographData } from '$domain/PictographData';
	import { onMount } from 'svelte';

	// Test state
	let testResults = $state<string[]>([]);
	let currentStartPosition = $state<BeatData | null>(null);
	let selectedOption = $state<PictographData | null>(null);
	let isTestRunning = $state(false);

	// Log test results
	function logResult(message: string, isError = false) {
		const timestamp = new Date().toLocaleTimeString();
		const logEntry = `[${timestamp}] ${isError ? '❌' : '✅'} ${message}`;
		testResults = [...testResults, logEntry];
		console.log(logEntry);
	}

	// Handle start position selection
	function handleStartPositionSelected(position: BeatData) {
		currentStartPosition = position;
		logResult(`Start position selected: ${position.pictograph_data?.letter || 'Unknown'}`);

		// Check localStorage
		const storedData = localStorage.getItem('start_position');
		if (storedData) {
			try {
				const parsed = JSON.parse(storedData);
				logResult(`Start position saved to localStorage with endPos: ${parsed.endPos}`);
			} catch (error) {
				logResult(`Error parsing localStorage data: ${error}`, true);
			}
		} else {
			logResult('No start position found in localStorage', true);
		}
	}

	// Handle option selection
	function handleOptionSelected(option: PictographData) {
		selectedOption = option;
		logResult(`Option selected: ${option.letter} (${option.id})`);
	}

	// Run automated test
	async function runAutomatedTest() {
		isTestRunning = true;
		testResults = [];

		try {
			logResult('🚀 Starting automated test...');

			// Test 1: Check if CSV data is available
			logResult('📊 Testing CSV data availability...');

			if (typeof window !== 'undefined' && 'csvData' in window) {
				const csvData = (
					window as unknown as { csvData: { diamondData: unknown[]; boxData: unknown[] } }
				).csvData;
				logResult(
					`CSV data found: Diamond=${csvData.diamondData.length} chars, Box=${csvData.boxData.length} chars`
				);
			} else {
				logResult('No CSV data found in window.csvData', true);
			}

			// Test 2: Check CSV file accessibility
			logResult('🔍 Testing CSV file accessibility...');
			try {
				const response = await fetch('/DiamondPictographDataframe.csv');
				if (response.ok) {
					const text = await response.text();
					const lines = text.split('\n');
					logResult(
						`Diamond CSV accessible: ${lines.length} lines, first line: ${lines[0]}`
					);
				} else {
					logResult(`Diamond CSV not accessible: ${response.status}`, true);
				}
			} catch (error) {
				logResult(`Error accessing Diamond CSV: ${error}`, true);
			}

			// Test 3: Check localStorage functionality
			logResult('💾 Testing localStorage functionality...');
			try {
				localStorage.setItem('test-key', 'test-value');
				const retrieved = localStorage.getItem('test-key');
				if (retrieved === 'test-value') {
					logResult('localStorage working correctly');
					localStorage.removeItem('test-key');
				} else {
					logResult('localStorage not working correctly', true);
				}
			} catch (error) {
				logResult(`localStorage error: ${error}`, true);
			}

			// Test 4: Simulate start position selection
			logResult('🎯 Simulating start position selection...');
			const testStartPosition = {
				endPos: 'alpha1',
				pictograph_data: {
					letter: 'α',
					motions: {
						blue: {
							motionType: 'static',
							startLocation: 'SOUTH',
							endLocation: 'SOUTH',
						},
						red: { motionType: 'static', startLocation: 'NORTH', endLocation: 'NORTH' },
					},
				},
				isStartPosition: true,
			};

			localStorage.setItem('start_position', JSON.stringify(testStartPosition));
			logResult('Test start position saved to localStorage');

			// Dispatch the event that OptionPicker should listen for
			const event = new CustomEvent('start-position-selected', {
				detail: { startPosition: testStartPosition, endPosition: 'alpha1' },
				bubbles: true,
			});
			document.dispatchEvent(event);
			logResult('start-position-selected event dispatched');

			// Wait a bit for async operations
			await new Promise((resolve) => setTimeout(resolve, 1000));

			logResult('✅ Automated test completed');
		} catch (error) {
			logResult(`Automated test failed: ${error}`, true);
		} finally {
			isTestRunning = false;
		}
	}

	// Clear test results
	function clearResults() {
		testResults = [];
		currentStartPosition = null;
		selectedOption = null;
	}

	// Check services on mount
	onMount(() => {
		logResult('🔄 Test page mounted, checking services...');

		// Check if services are available
		setTimeout(() => {
			try {
				// Check global CSV data
				if (typeof window !== 'undefined' && 'csvData' in window) {
					logResult('Global CSV data is available');
				} else {
					logResult('Global CSV data not found', true);
				}

				// Check DI container
				if (typeof window !== 'undefined' && 'diContainer' in window) {
					logResult('DI container is available');
				} else {
					logResult('DI container not found - this may be normal');
				}
			} catch (error) {
				logResult(`Error checking services: ${error}`, true);
			}
		}, 500);
	});
</script>

<svelte:head>
	<title>TKA - Start Position to Option Picker Test</title>
</svelte:head>

<div class="test-page">
	<header class="test-header">
		<h1>Start Position → Option Picker Flow Test</h1>
		<p>
			This page tests the complete flow from start position selection to option loading using
			real CSV data.
		</p>

		<div class="test-controls">
			<button class="test-btn primary" onclick={runAutomatedTest} disabled={isTestRunning}>
				{isTestRunning ? '⏳ Running...' : '🚀 Run Automated Test'}
			</button>
			<button class="test-btn secondary" onclick={clearResults}> 🗑️ Clear Results </button>
		</div>
	</header>

	<div class="test-content">
		<!-- Test Results Panel -->
		<div class="test-panel results-panel">
			<h2>📊 Test Results</h2>
			<div class="results-container">
				{#if testResults.length === 0}
					<p class="no-results">
						No test results yet. Run the automated test or manually select a start
						position.
					</p>
				{:else}
					{#each testResults as result}
						<div class="result-item" class:error={result.includes('❌')}>
							{result}
						</div>
					{/each}
				{/if}
			</div>
		</div>

		<!-- Current State Panel -->
		<div class="test-panel state-panel">
			<h2>📋 Current State</h2>
			<div class="state-info">
				<div class="state-item">
					<strong>Start Position:</strong>
					{currentStartPosition?.pictograph_data?.letter || 'None selected'}
				</div>
				<div class="state-item">
					<strong>Selected Option:</strong>
					{selectedOption?.letter || 'None selected'}
				</div>
				<div class="state-item">
					<strong>localStorage start_position:</strong>
					<code>{localStorage.getItem('start_position') ? 'Present' : 'Not found'}</code>
				</div>
			</div>
		</div>

		<!-- Start Position Picker -->
		<div class="test-panel picker-panel">
			<h2>🎯 Start Position Picker</h2>
			<p>Click a start position below to test the flow:</p>
			<div class="picker-container">
				<StartPositionPicker
					gridMode="diamond"
					onStartPositionSelected={handleStartPositionSelected}
				/>
			</div>
		</div>

		<!-- Option Picker -->
		<div class="test-panel picker-panel">
			<h2>🎲 Option Picker</h2>
			<p>Options should load automatically after selecting a start position:</p>
			<div class="picker-container">
				<OptionPickerContainer onOptionSelected={handleOptionSelected} />
			</div>
		</div>
	</div>
</div>

<style>
	.test-page {
		min-height: 100vh;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		padding: 2rem;
		font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
	}

	.test-header {
		background: white;
		border-radius: 12px;
		padding: 2rem;
		margin-bottom: 2rem;
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
	}

	.test-header h1 {
		margin: 0 0 0.5rem 0;
		color: #1a202c;
		font-size: 2rem;
	}

	.test-header p {
		margin: 0 0 1.5rem 0;
		color: #4a5568;
		font-size: 1.1rem;
	}

	.test-controls {
		display: flex;
		gap: 1rem;
	}

	.test-btn {
		padding: 0.75rem 1.5rem;
		border: none;
		border-radius: 8px;
		font-size: 1rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s;
	}

	.test-btn.primary {
		background: #4299e1;
		color: white;
	}

	.test-btn.primary:hover:not(:disabled) {
		background: #3182ce;
		transform: translateY(-1px);
	}

	.test-btn.primary:disabled {
		background: #a0aec0;
		cursor: not-allowed;
	}

	.test-btn.secondary {
		background: #e2e8f0;
		color: #2d3748;
	}

	.test-btn.secondary:hover {
		background: #cbd5e0;
		transform: translateY(-1px);
	}

	.test-content {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 2rem;
	}

	.test-panel {
		background: white;
		border-radius: 12px;
		padding: 1.5rem;
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
	}

	.test-panel h2 {
		margin: 0 0 1rem 0;
		color: #1a202c;
		font-size: 1.25rem;
	}

	.results-panel {
		grid-column: 1 / -1;
		max-height: 400px;
	}

	.results-container {
		max-height: 300px;
		overflow-y: auto;
		border: 1px solid #e2e8f0;
		border-radius: 6px;
		padding: 1rem;
		background: #f8fafc;
	}

	.no-results {
		color: #718096;
		font-style: italic;
		text-align: center;
		margin: 2rem 0;
	}

	.result-item {
		padding: 0.5rem 0;
		border-bottom: 1px solid #e2e8f0;
		font-family: 'Courier New', monospace;
		font-size: 0.9rem;
	}

	.result-item:last-child {
		border-bottom: none;
	}

	.result-item.error {
		color: #e53e3e;
		background: #fed7d7;
		padding: 0.5rem;
		border-radius: 4px;
		margin: 0.25rem 0;
	}

	.state-panel {
		grid-column: 1 / -1;
	}

	.state-info {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.state-item {
		padding: 0.75rem;
		background: #f8fafc;
		border-radius: 6px;
		border-left: 4px solid #4299e1;
	}

	.state-item strong {
		color: #2d3748;
	}

	.state-item code {
		background: #e2e8f0;
		padding: 0.25rem 0.5rem;
		border-radius: 4px;
		font-family: 'Courier New', monospace;
		font-size: 0.9rem;
	}

	.picker-panel {
		min-height: 400px;
	}

	.picker-container {
		border: 2px dashed #cbd5e0;
		border-radius: 8px;
		padding: 1rem;
		min-height: 300px;
		background: #f8fafc;
	}

	@media (max-width: 1024px) {
		.test-content {
			grid-template-columns: 1fr;
		}

		.results-panel,
		.state-panel {
			grid-column: 1;
		}
	}
</style>
