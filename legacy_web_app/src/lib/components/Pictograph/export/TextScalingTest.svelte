<script lang="ts">
	import { onMount } from 'svelte';
	import { exportSequenceImage } from './SequenceImageExporter';
	import type { Beat } from '$lib/types/Beat';
	import { Letter } from '$lib/types/Letter';
	import type { TKAPosition } from '$lib/types/TKAPosition';

	let testResults: Array<{
		size: string;
		imageUrl: string;
		success: boolean;
	}> = [];

	let isRunning = false;

	// Test different image sizes
	const testSizes = [
		{ width: 320, height: 320, label: 'Small Square' },
		{ width: 640, height: 480, label: 'Medium Rectangle' },
		{ width: 1024, height: 768, label: 'Large Rectangle' },
		{ width: 1920, height: 1080, label: 'Full HD' }
	];

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

	async function runTests() {
		isRunning = true;
		testResults = [];

		// Create a container for the test elements
		const container = document.createElement('div');
		container.style.position = 'absolute';
		container.style.left = '-9999px';
		container.style.top = '-9999px';

		// Test each size
		for (const size of testSizes) {
			try {
				// Create SVG elements for beats
				container.innerHTML = '';

				// Create 4 beats for testing
				for (let i = 0; i < 4; i++) {
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
					text.textContent = String.fromCharCode(65 + i); // A, B, C, D

					svg.appendChild(rect);
					svg.appendChild(text);
					container.appendChild(svg);
				}

				// Add container to the document
				document.body.appendChild(container);

				// Create dummy beats
				const beats: Beat[] = Array.from({ length: 4 }, (_, i) => createDummyBeat(i));

				// Export image with the current size
				container.style.width = `${size.width}px`;
				container.style.height = `${size.height}px`;

				// Export image
				const result = await exportSequenceImage(container, {
					beats,
					startPosition: createDummyBeat(0),
					includeStartPosition: true,
					addWord: true,
					addUserInfo: true,
					addDifficultyLevel: true,
					title: 'ABCD',
					userName: 'Test User',
					notes: 'Created using The Kinetic Alphabet',
					difficultyLevel: 3
				});

				// Add result
				testResults = [
					...testResults,
					{
						size: `${size.label} (${size.width}x${size.height})`,
						imageUrl: result.dataUrl,
						success: true
					}
				];
			} catch (error) {
				console.error(`Error testing size ${size.label}:`, error);
				testResults = [
					...testResults,
					{
						size: `${size.label} (${size.width}x${size.height})`,
						imageUrl: '',
						success: false
					}
				];
			}
		}

		// Clean up
		if (document.body.contains(container)) {
			document.body.removeChild(container);
		}

		isRunning = false;
	}

	onMount(() => {
		// Automatically run tests when component mounts
		runTests();
	});
</script>

<div class="text-scaling-test">
	<h1>Text Scaling Test</h1>

	<button on:click={runTests} disabled={isRunning}>
		{isRunning ? 'Running Tests...' : 'Run Tests Again'}
	</button>

	<div class="test-results">
		<h2>Test Results</h2>

		<div class="results-grid">
			{#each testResults as result}
				<div class="result-card {result.success ? 'success' : 'error'}">
					<h3>{result.size}</h3>

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
	.text-scaling-test {
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
