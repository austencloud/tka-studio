<script lang="ts">
	import { onMount } from 'svelte';
	import { exportSequenceImage } from './SequenceImageExporter';
	import type { Beat } from '$lib/types/Beat';
	import { Letter } from '$lib/types/Letter';
	import type { TKAPosition } from '$lib/types/TKAPosition';

	let testResults: Array<{
		title: string;
		imageUrl: string;
		success: boolean;
		dimensions: { width: number; height: number };
	}> = [];

	let isRunning = false;

	// Create a dummy beat
	function createDummyBeat(index: number): Beat {
		// Convert ASCII code to Letter enum
		const letterCode = 65 + (index % 26);
		const letterChar = String.fromCharCode(letterCode);
		const letterEnum = Letter[letterChar as keyof typeof Letter];

		// Use alpha1 as a valid TKAPosition
		const startPosition: TKAPosition | null = index === 0 ? 'alpha1' : null;

		return {
			id: `beat-${index}`,
			beatNumber: index,
			filled: true,
			pictographData: {
				letter: letterEnum,
				startPos: startPosition,
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
			}
		};
	}

	// Create a dummy start position
	function createDummyStartPosition(): Beat {
		const beat = createDummyBeat(0);
		beat.pictographData.startPos = 'alpha1'; // Use a valid TKAPosition
		return beat;
	}

	async function runTests() {
		isRunning = true;
		testResults = [];

		// Create a container for the test elements
		const container = document.createElement('div');
		container.style.position = 'absolute';
		container.style.left = '-9999px';
		container.style.top = '-9999px';
		document.body.appendChild(container);

		try {
			// Test 6 beats with start position
			await testLayout(container, 6, true, '6 Beats with Start Position');

			// Test 6 beats without start position
			await testLayout(container, 6, false, '6 Beats without Start Position');

			// Test 5 beats with start position
			await testLayout(container, 5, true, '5 Beats with Start Position');

			// Test 4 beats with start position
			await testLayout(container, 4, true, '4 Beats with Start Position');
		} finally {
			// Clean up
			if (document.body.contains(container)) {
				document.body.removeChild(container);
			}

			isRunning = false;
		}
	}

	async function testLayout(
		container: HTMLElement,
		beatCount: number,
		includeStart: boolean,
		title: string
	) {
		try {
			// Clear container
			container.innerHTML = '';

			// Create SVG elements for beats
			for (let i = 0; i < beatCount; i++) {
				const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
				svg.setAttribute('width', '950');
				svg.setAttribute('height', '950');
				svg.setAttribute('viewBox', '0 0 950 950');

				// Add a background rect
				const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
				rect.setAttribute('x', '0');
				rect.setAttribute('y', '0');
				rect.setAttribute('width', '950');
				rect.setAttribute('height', '950');
				rect.setAttribute('fill', '#f0f0f0');

				// Add text to represent a letter
				const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
				text.setAttribute('x', '475');
				text.setAttribute('y', '475');
				text.setAttribute('text-anchor', 'middle');
				text.setAttribute('dominant-baseline', 'middle');
				text.setAttribute('font-size', '200');
				text.setAttribute('font-family', 'Arial');
				text.textContent = String.fromCharCode(65 + i); // A, B, C, D, etc.

				svg.appendChild(rect);
				svg.appendChild(text);
				container.appendChild(svg);
			}

			// Create beats array
			const beats: Beat[] = Array.from({ length: beatCount }, (_, i) => createDummyBeat(i));

			// Create start position if needed
			const startPosition = includeStart ? createDummyStartPosition() : null;

			// Export image
			const result = await exportSequenceImage(container, {
				beats,
				startPosition,
				includeStartPosition: includeStart,
				addWord: true,
				addUserInfo: true,
				addDifficultyLevel: true,
				title: `${beatCount} Beats${includeStart ? ' + Start' : ''}`,
				userName: 'Test User',
				notes: 'Layout Test',
				difficultyLevel: 3,
				columns: 0 // Let the calculator determine the optimal layout
			});

			// Add result
			testResults = [
				...testResults,
				{
					title,
					imageUrl: result.dataUrl,
					success: true,
					dimensions: { width: result.width, height: result.height }
				}
			];
		} catch (error) {
			console.error(`Error testing layout for ${title}:`, error);
			testResults = [
				...testResults,
				{
					title,
					imageUrl: '',
					success: false,
					dimensions: { width: 0, height: 0 }
				}
			];
		}
	}

	onMount(() => {
		// Automatically run tests when component mounts
		runTests();
	});
</script>

<div class="layout-test">
	<h1>Layout Test</h1>

	<button on:click={runTests} disabled={isRunning}>
		{isRunning ? 'Running Tests...' : 'Run Tests Again'}
	</button>

	<div class="test-results">
		<h2>Test Results</h2>

		<div class="results-grid">
			{#each testResults as result}
				<div class="result-card {result.success ? 'success' : 'error'}">
					<h3>{result.title}</h3>
					<p>Dimensions: {result.dimensions.width}x{result.dimensions.height}</p>

					{#if result.success}
						<div class="image-container">
							<img src={result.imageUrl} alt="Test Result" />
						</div>
					{:else}
						<div class="error-message">Error generating image</div>
					{/if}
				</div>
			{/each}
		</div>
	</div>
</div>

<style>
	.layout-test {
		padding: 20px;
		font-family: Arial, sans-serif;
	}

	button {
		padding: 10px 20px;
		font-size: 16px;
		margin-bottom: 20px;
	}

	.test-results {
		margin-top: 20px;
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
</style>
