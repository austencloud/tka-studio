<script lang="ts">
	import { onMount } from 'svelte';
	import ArrowDebugCanvas from './ArrowDebugCanvas.svelte';
	import ArrowDebugControlPanel from './ArrowDebugControlPanel.svelte';
	import ArrowDebugInfoPanel from './ArrowDebugInfoPanel.svelte';
	import { createArrowDebugState } from './state/arrow-debug-state.svelte';
	import { initializeDebugApp } from './debug-app-init';

	// Reactive state for app initialization
	let isAppReady = false;
	let initError: string | null = null;
	let state: ReturnType<typeof createArrowDebugState> | null = null;

	// Initialize the application on mount
	onMount(async () => {
		try {
			await initializeDebugApp();
			state = createArrowDebugState();
			isAppReady = true;
		} catch (error) {
			console.error('Failed to initialize debug app:', error);
			initError = error instanceof Error ? error.message : 'Unknown initialization error';
		}
	});
</script>

<svelte:head>
	<title>TKA Arrow Positioning Debug - Step-by-Step Analysis</title>
</svelte:head>

<div class="arrow-debug-container">
	<header class="debug-header">
		<h1>🎯 Arrow Positioning Debug</h1>
		<p>Visual step-by-step analysis of arrow placement with coordinate system debugging</p>
	</header>

	{#if initError}
		<div class="error-container">
			<div class="error-box">
				<h2>❌ Initialization Error</h2>
				<p>Failed to initialize the debug system:</p>
				<code>{initError}</code>
				<p>Please check the console for more details.</p>
			</div>
		</div>
	{:else if !isAppReady || !state}
		<div class="loading-container">
			<div class="loading-box">
				<div class="spinner"></div>
				<h2>🔧 Initializing Debug System</h2>
				<p>Setting up DI container and positioning services...</p>
			</div>
		</div>
	{:else if state}
		<main class="debug-main">
			<!-- Left Panel: Controls & Pictograph Selection -->
			<div class="panel control-panel">
				<ArrowDebugControlPanel {state} />
			</div>

			<!-- Center Panel: Visual Canvas with Step-by-Step Positioning -->
			<div class="panel canvas-panel">
				<ArrowDebugCanvas {state} />
			</div>

			<!-- Right Panel: Debug Information & Coordinate Details -->
			<div class="panel debug-info-panel">
				<ArrowDebugInfoPanel {state} />
			</div>
		</main>
	{/if}
</div>

<style>
	.arrow-debug-container {
		min-height: 100vh;
		background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e1b4b 100%);
		color: white;
		padding: 20px;
		font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
	}

	.debug-header {
		text-align: center;
		margin-bottom: 30px;
		padding-bottom: 20px;
		border-bottom: 2px solid rgba(99, 102, 241, 0.3);
	}

	.debug-header h1 {
		font-size: 2rem;
		margin-bottom: 10px;
		background: linear-gradient(135deg, #fbbf24, #f59e0b);
		background-clip: text;
		-webkit-background-clip: text;
		color: transparent;
	}

	.debug-header p {
		color: #c7d2fe;
		font-size: 1.1rem;
	}

	.debug-main {
		display: grid;
		grid-template-columns: 400px 1fr 450px;
		gap: 20px;
		max-width: 1600px;
		margin: 0 auto;
		min-height: calc(100vh - 200px);
	}

	.panel {
		background: rgba(255, 255, 255, 0.1);
		backdrop-filter: blur(20px);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 16px;
		padding: 20px;
		overflow-y: auto;
	}

	.canvas-panel {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background: rgba(255, 255, 255, 0.05);
	}

	.control-panel {
		max-height: calc(100vh - 200px);
	}

	.debug-info-panel {
		max-height: calc(100vh - 200px);
	}

	.loading-container,
	.error-container {
		display: flex;
		justify-content: center;
		align-items: center;
		min-height: calc(100vh - 200px);
		padding: 40px;
	}

	.loading-box,
	.error-box {
		background: rgba(255, 255, 255, 0.1);
		backdrop-filter: blur(20px);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 16px;
		padding: 40px;
		text-align: center;
		max-width: 500px;
		width: 100%;
	}

	.error-box {
		border-color: rgba(248, 113, 113, 0.5);
		background: rgba(248, 113, 113, 0.1);
	}

	.loading-box h2,
	.error-box h2 {
		margin: 20px 0 15px 0;
		color: #fbbf24;
		font-size: 1.5rem;
	}

	.error-box h2 {
		color: #f87171;
	}

	.loading-box p,
	.error-box p {
		color: #c7d2fe;
		margin-bottom: 10px;
		line-height: 1.5;
	}

	.error-box code {
		background: rgba(0, 0, 0, 0.4);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 4px;
		padding: 8px 12px;
		font-family: 'Courier New', monospace;
		color: #f87171;
		display: block;
		margin: 15px 0;
		word-break: break-all;
	}

	.spinner {
		width: 50px;
		height: 50px;
		border: 4px solid rgba(251, 191, 36, 0.3);
		border-top: 4px solid #fbbf24;
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin: 0 auto;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}

	@media (max-width: 1400px) {
		.debug-main {
			grid-template-columns: 350px 1fr 400px;
		}
	}

	@media (max-width: 1200px) {
		.debug-main {
			grid-template-columns: 1fr;
			grid-template-rows: auto 1fr auto;
			gap: 15px;
		}

		.panel {
			min-height: auto;
		}
	}

	@media (max-width: 768px) {
		.arrow-debug-container {
			padding: 10px;
		}

		.debug-header h1 {
			font-size: 1.5rem;
		}

		.panel {
			padding: 15px;
		}
	}
</style>
