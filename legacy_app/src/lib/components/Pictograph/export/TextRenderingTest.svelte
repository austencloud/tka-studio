<script lang="ts">
	import { exportSequenceImage } from './SequenceImageExporter';
	import type { Beat } from '$lib/types/Beat';
	import { Letter } from '$lib/types/Letter';
	import { onMount } from 'svelte';

	// Test parameters - focusing on realistic export sizes
	let testSizes = [
		// Standard export sizes
		{ width: 950, height: 950, label: '1x1 Grid' },
		{ width: 1900, height: 950, label: '2x1 Grid' },
		{ width: 2850, height: 950, label: '3x1 Grid' },
		{ width: 1900, height: 1900, label: '2x2 Grid' },
		{ width: 2850, height: 1900, label: '3x2 Grid' },
		{ width: 3800, height: 1900, label: '4x2 Grid' },
		{ width: 2850, height: 2850, label: '3x3 Grid' },
		{ width: 3800, height: 2850, label: '4x3 Grid' },
		{ width: 3800, height: 3800, label: '4x4 Grid' }
	];

	// Test sequences designed to test different row layouts
	let testSequences = [
		// 1-row layouts
		{ beats: 1, title: 'One Beat (1 row)', difficulty: 1 },
		{ beats: 2, title: 'Two Beats (1 row)', difficulty: 1 },
		{ beats: 3, title: 'Three Beats (1 row)', difficulty: 1 },
		{ beats: 4, title: 'Four Beats (1 row)', difficulty: 1 },

		// 2-row layouts
		{ beats: 5, title: 'Five Beats (2 rows)', difficulty: 2 },
		{ beats: 6, title: 'Six Beats (2 rows)', difficulty: 2 },
		{ beats: 8, title: 'Eight Beats (2 rows)', difficulty: 2 },

		// 3-row layouts
		{ beats: 9, title: 'Nine Beats (3 rows)', difficulty: 3 },
		{ beats: 12, title: 'Twelve Beats (3 rows)', difficulty: 3 },

		// 4-row layouts
		{ beats: 16, title: 'Sixteen Beats (4 rows)', difficulty: 4 },
		{ beats: 20, title: 'Twenty Beats (4 rows)', difficulty: 5 }
	];

	// Results
	let testResults: Array<{
		size: string;
		sequence: string;
		imageUrl: string;
		success: boolean;
		error?: string;
	}> = [];

	let isRunningTests = false;
	let testContainer: HTMLDivElement;

	// Create a dummy beat for testing
	function createDummyBeat(index: number): Beat {
		return {
			id: `test-beat-${index}`,
			beatNumber: index,
			filled: true,
			pictographData: {
				letter: Letter.A,
				startPos: null,
				endPos: null,
				timing: null,
				direction: null,
				gridMode: 'diamond',
				gridData: null,
				blueMotionData: null,
				redMotionData: null,
				redPropData: null,
				bluePropData: null,
				redArrowData: null,
				blueArrowData: null,
				grid: 'diamond'
			},
			metadata: {
				tags: [`beat-${index}`]
			}
		};
	}

	// Run tests for all combinations
	async function runTests() {
		if (isRunningTests) return;
		isRunningTests = true;
		testResults = [];

		try {
			for (const size of testSizes) {
				for (const sequence of testSequences) {
					await runTest(size, sequence);
				}
			}
		} catch (error) {
			console.error('Test error:', error);
		} finally {
			isRunningTests = false;
		}
	}

	// Run a single test
	async function runTest(size: (typeof testSizes)[0], sequence: (typeof testSequences)[0]) {
		try {
			// Create test container with specified size
			const container = document.createElement('div');
			container.style.width = `${size.width}px`;
			container.style.height = `${size.height}px`;
			container.style.position = 'absolute';
			container.style.left = '-9999px';
			container.style.backgroundColor = '#FFFFFF';

			// Create dummy SVG elements
			for (let i = 0; i < sequence.beats; i++) {
				const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
				svg.setAttribute('width', '950');
				svg.setAttribute('height', '950');
				svg.setAttribute('viewBox', '0 0 950 950');

				// Add a simple rectangle to represent a pictograph
				const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
				rect.setAttribute('x', '100');
				rect.setAttribute('y', '100');
				rect.setAttribute('width', '750');
				rect.setAttribute('height', '750');
				rect.setAttribute('fill', '#EEEEEE');
				rect.setAttribute('stroke', '#000000');
				rect.setAttribute('stroke-width', '2');

				// Add text to represent a letter
				const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
				text.setAttribute('x', '475');
				text.setAttribute('y', '475');
				text.setAttribute('text-anchor', 'middle');
				text.setAttribute('dominant-baseline', 'middle');
				text.setAttribute('font-size', '200');
				text.setAttribute('font-family', 'Arial');
				text.textContent = String.fromCharCode(65 + (i % 26)); // A-Z

				svg.appendChild(rect);
				svg.appendChild(text);
				container.appendChild(svg);
			}

			// Add container to the document
			document.body.appendChild(container);

			// Create dummy beats
			const beats: Beat[] = Array.from({ length: sequence.beats }, (_, i) => createDummyBeat(i));

			// Export image
			const result = await exportSequenceImage(container, {
				beats,
				startPosition: sequence.beats > 0 ? createDummyBeat(0) : null,
				includeStartPosition: true,
				addWord: true,
				addUserInfo: true,
				addDifficultyLevel: true,
				title: sequence.title,
				userName: 'Test User',
				notes: 'Created using The Kinetic Alphabet',
				difficultyLevel: sequence.difficulty
			});

			// Add result
			testResults = [
				...testResults,
				{
					size: `${size.label} (${size.width}x${size.height})`,
					sequence: `${sequence.title} (${sequence.beats} beats)`,
					imageUrl: result.dataUrl,
					success: true
				}
			];

			// Clean up
			document.body.removeChild(container);
		} catch (error) {
			// Add error result
			testResults = [
				...testResults,
				{
					size: `${size.label} (${size.width}x${size.height})`,
					sequence: `${sequence.title} (${sequence.beats} beats)`,
					imageUrl: '',
					success: false,
					error: error instanceof Error ? error.message : String(error)
				}
			];
		}
	}

	onMount(() => {
		// Auto-run tests when component mounts
		runTests();
	});
</script>

<div class="text-rendering-test">
	<h1>Text Rendering Test</h1>

	<button on:click={runTests} disabled={isRunningTests}>
		{isRunningTests ? 'Running Tests...' : 'Run Tests'}
	</button>

	<div class="test-results">
		<h2>Test Results ({testResults.length} of {testSizes.length * testSequences.length})</h2>

		{#if testResults.length === 0 && isRunningTests}
			<p>Running tests, please wait...</p>
		{:else if testResults.length === 0}
			<p>No test results yet. Click "Run Tests" to start.</p>
		{:else}
			<div class="results-grid">
				{#each testResults as result}
					<div class="result-card" class:success={result.success} class:error={!result.success}>
						<h3>{result.size}</h3>
						<h4>{result.sequence}</h4>

						{#if result.success}
							<div class="image-container">
								<img src={result.imageUrl} alt={`${result.sequence} at ${result.size}`} />
							</div>
						{:else}
							<div class="error-message">
								<p>Error: {result.error}</p>
							</div>
						{/if}
					</div>
				{/each}
			</div>
		{/if}
	</div>

	<div bind:this={testContainer} class="test-container"></div>
</div>

<style>
	.text-rendering-test {
		padding: 20px;
		font-family: Arial, sans-serif;
		max-width: 100%;
	}

	.test-results {
		margin-top: 20px;
		max-height: 80vh;
		overflow-y: auto;
		padding-bottom: 20px;
	}

	button {
		padding: 10px 20px;
		font-size: 16px;
		margin-bottom: 20px;
	}

	.results-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
		gap: 20px;
	}

	.result-card {
		border: 1px solid #ccc;
		border-radius: 8px;
		padding: 15px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	.result-card.success {
		border-color: #4caf50;
	}

	.result-card.error {
		border-color: #f44336;
		background-color: #ffebee;
	}

	.image-container {
		margin-top: 10px;
		overflow: hidden;
		border: 1px solid #eee;
	}

	.image-container img {
		max-width: 100%;
		height: auto;
		display: block;
	}

	.error-message {
		color: #f44336;
		font-weight: bold;
	}

	h3,
	h4 {
		margin: 0 0 10px 0;
	}

	.test-container {
		position: absolute;
		left: -9999px;
		visibility: hidden;
	}
</style>
