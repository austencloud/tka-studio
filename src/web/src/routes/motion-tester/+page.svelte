<script lang="ts">
	import MotionParameterPanel from './MotionParameterPanel.svelte';
	import PictographVisualizationPanel from './PictographVisualizationPanel.svelte';
	import { createMotionTesterState } from './state/motion-tester-state.svelte';

	// Initialize the motion tester state
	const state = createMotionTesterState();
</script>

<svelte:head>
	<title>TKA Motion Tester - Individual Motion Testing</title>
</svelte:head>

<div class="motion-tester-container">
	<header class="tester-header">
		<h1>TKA Motion Tester</h1>
		<p>Test individual motion sequences with visual feedback and debugging</p>
	</header>

	<main class="tester-main">
		<!-- Left Panel: Motion Parameters -->
		<div class="panel motion-params">
			<MotionParameterPanel {state} />
		</div>

		<!-- Right Panel: Pictograph Visualization -->
		<div class="panel visualization-panel">
			<PictographVisualizationPanel {state} />
		</div>
	</main>
</div>

<style>
	.motion-tester-container {
		min-height: 100vh;
		background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e1b4b 100%);
		color: white;
		padding: 20px;
		font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
	}

	.tester-header {
		text-align: center;
		margin-bottom: 30px;
		padding-bottom: 20px;
		border-bottom: 2px solid rgba(99, 102, 241, 0.3);
	}

	.tester-header h1 {
		font-size: 2rem;
		margin-bottom: 10px;
		background: linear-gradient(135deg, #a5b4fc, #c7d2fe);
		background-clip: text;
		-webkit-background-clip: text;
		color: transparent;
	}

	.tester-header p {
		color: #c7d2fe;
		font-size: 1.1rem;
	}

	.tester-main {
		display: grid;
		grid-template-columns: 400px 1fr;
		gap: 20px;
		max-width: 1400px;
		margin: 0 auto;
		height: calc(100vh - 200px);
	}

	.panel {
		background: rgba(255, 255, 255, 0.1);
		backdrop-filter: blur(20px);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 16px;
		padding: 20px;
		overflow-y: auto;
	}

	.motion-params {
		background: rgba(255, 255, 255, 0.08);
	}

	.visualization-panel {
		background: rgba(255, 255, 255, 0.05);
		display: flex;
		flex-direction: column;
	}

	@media (max-width: 1200px) {
		.tester-main {
			grid-template-columns: 1fr;
			grid-template-rows: auto 1fr;
			gap: 15px;
			height: auto;
			min-height: calc(100vh - 200px);
		}

		.panel {
			min-height: auto;
		}

		.motion-params {
			order: 1;
		}

		.visualization-panel {
			order: 2;
			min-height: 600px;
		}
	}

	@media (max-width: 768px) {
		.motion-tester-container {
			padding: 10px;
		}

		.tester-header h1 {
			font-size: 1.5rem;
		}

		.panel {
			padding: 15px;
		}
	}
</style>
