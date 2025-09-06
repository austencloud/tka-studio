<!--
  EnhancedExportTester Component

  This component provides a UI for testing the enhanced image export functionality.
  It allows exporting a sequence with additional elements like title, user info, and difficulty label.
-->
<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import Pictograph from '$lib/components/Pictograph/Pictograph.svelte';
	import { defaultPictographData } from '$lib/components/Pictograph/utils/defaultPictographData';
	import type { PictographData } from '$lib/types/PictographData';
	import type { Beat } from '$lib/types/Beat';
	import { exportSequenceImage } from './SequenceImageExporter';
	import { downloadImage } from './downloadUtils';
	import { DIAMOND } from '$lib/types/Constants';

	// State variables
	let sequenceContainer: HTMLElement | null = $state(null);
	let exportResult: { dataUrl: string; width: number; height: number } | null = $state(null);
	let exportError: string | null = $state(null);
	let isExporting: boolean = $state(false);

	// Export options
	let backgroundColor: string = $state('#FFFFFF');
	let scale: number = $state(2);
	let quality: number = $state(0.92);
	let format: 'png' | 'jpeg' = $state('png');
	let columns: number = $state(3);
	let spacing: number = $state(20);

	// Content flags
	let addWord: boolean = $state(true);
	let addUserInfo: boolean = $state(true);
	let addDifficultyLevel: boolean = $state(true);
	let showBeatNumbers: boolean = $state(true);
	// Start position is now always included
	const includeStartPosition: boolean = true;

	// Content values
	let title: string = $state('Sample Sequence');
	let userName: string = $state('Test User');
	let notes: string = $state('Created using The Kinetic Constructor');
	let difficultyLevel: number = $state(3);

	// Predefined note lengths for testing
	const noteOptions = [
		{ label: 'Short', text: 'Created using The Kinetic Constructor' },
		{
			label: 'Medium',
			text: 'Created using The Kinetic Constructor - A tool for visualizing poi sequences'
		},
		{
			label: 'Long',
			text: 'Created using The Kinetic Constructor - A tool for visualizing poi sequences and sharing them with the flow arts community'
		}
	];

	// Sample data
	let beats: Beat[] = $state([]);
	let startPosition: Beat | null = $state(null);

	// Create sample beats
	function createSampleBeats(count: number) {
		const newBeats: Beat[] = [];

		for (let i = 0; i < count; i++) {
			newBeats.push({
				id: `beat-${i}`,
				beatNumber: i + 1,
				pictographData: { ...defaultPictographData, gridMode: DIAMOND },
				filled: true,
				metadata: {
					letter: 'A',
					startPos: 'n',
					endPos: 's'
				}
			});
		}

		beats = newBeats;

		// Create start position
		startPosition = {
			id: 'start-position',
			beatNumber: 0,
			pictographData: { ...defaultPictographData, gridMode: DIAMOND, isStartPosition: true },
			filled: true,
			metadata: {
				letter: 'A',
				startPos: 'n',
				endPos: 'n'
			}
		};
	}

	// Function to update beat count
	function updateBeatCount(newCount: number) {
		// Ensure count is within reasonable limits
		const count = Math.max(1, Math.min(20, newCount));
		createSampleBeats(count);

		// Trigger automatic re-rendering
		renderPreview();
	}

	// Function to increment beat count
	function incrementBeatCount() {
		updateBeatCount(beats.length + 1);
	}

	// Function to decrement beat count
	function decrementBeatCount() {
		updateBeatCount(beats.length - 1);
	}

	// Handle export button click
	async function handleExport() {
		if (!browser || !sequenceContainer) {
			exportError = 'Cannot export: not in browser environment or no sequence container';
			return;
		}

		try {
			isExporting = true;
			exportError = null;

			// Export the sequence
			const result = await exportSequenceImage(sequenceContainer, {
				beats,
				startPosition: includeStartPosition ? startPosition : null,
				backgroundColor,
				scale,
				quality,
				format,
				columns,
				spacing,
				includeStartPosition,
				addWord,
				addUserInfo,
				addDifficultyLevel,
				addBeatNumbers: showBeatNumbers,
				title,
				userName,
				notes,
				difficultyLevel
			});

			// Update the result
			exportResult = result;

			console.log('Export successful:', result);
		} catch (error) {
			exportError = `Export failed: ${error instanceof Error ? error.message : String(error)}`;
			console.error('Export failed:', error);
		} finally {
			isExporting = false;
		}
	}

	// Function to automatically render preview when settings change
	async function renderPreview() {
		// Only render if we have a container and we're not already exporting
		if (browser && sequenceContainer && !isExporting) {
			try {
				// Set a small delay to avoid too many renders when multiple settings change at once
				await new Promise((resolve) => setTimeout(resolve, 100));

				// Only proceed if we're still not exporting (could have changed during the delay)
				if (!isExporting) {
					isExporting = true;
					exportError = null;

					// Export with current settings
					const result = await exportSequenceImage(sequenceContainer, {
						beats,
						startPosition: includeStartPosition ? startPosition : null,
						backgroundColor,
						scale,
						quality,
						format,
						columns,
						spacing,
						includeStartPosition,
						addWord,
						addUserInfo,
						addDifficultyLevel,
						addBeatNumbers: showBeatNumbers,
						title,
						userName,
						notes,
						difficultyLevel
					});

					// Update the result
					exportResult = result;
				}
			} catch (error) {
				console.error('Preview rendering failed:', error);
				// Don't show error to user for automatic previews
			} finally {
				isExporting = false;
			}
		}
	}

	// Handle download button click
	async function handleDownload() {
		if (!exportResult) {
			exportError = 'No export result to download';
			return;
		}

		try {
			// Download the image
			await downloadImage({
				dataUrl: exportResult.dataUrl,
				filename: `sequence-${Date.now()}.${format}`
			});
		} catch (error) {
			exportError = `Download failed: ${error instanceof Error ? error.message : String(error)}`;
			console.error('Download failed:', error);
		}
	}

	// Effect to trigger automatic preview rendering when settings change
	$effect(() => {
		// Using void to suppress unused variable warnings while still creating dependencies
		void beats.length;
		void backgroundColor;
		void scale;
		void quality;
		void format;
		void columns;
		void spacing;
		void includeStartPosition;
		void addWord;
		void addUserInfo;
		void addDifficultyLevel;
		void showBeatNumbers;
		void title;
		void userName;
		void notes;
		void difficultyLevel;

		// Only trigger if we have a container and beats
		if (sequenceContainer && beats.length > 0) {
			console.log('Settings changed, updating preview');
			renderPreview();
		}
	});

	// Initialize on mount
	onMount(() => {
		// Create sample beats
		createSampleBeats(5);

		// Initial render after a short delay to ensure the container is ready
		setTimeout(() => {
			renderPreview();
		}, 300);
	});
</script>

<div class="enhanced-export-tester">
	<h2>Enhanced Export Tester</h2>

	<div class="content">
		<div class="sequence-container" bind:this={sequenceContainer}>
			<h3>Sequence</h3>

			<div class="beat-grid" style="--columns: {columns}; --spacing: {spacing}px;">
				{#if includeStartPosition && startPosition}
					<div class="beat-wrapper start-position">
						<div class="beat-label">Start</div>
						<Pictograph pictographData={startPosition.pictographData} isStartPosition={true} />
					</div>
				{/if}

				{#each beats as beat}
					<div class="beat-wrapper">
						{#if showBeatNumbers}
							<div class="beat-label">Beat {beat.beatNumber}</div>
						{/if}
						<Pictograph pictographData={beat.pictographData} beatNumber={beat.beatNumber} />
					</div>
				{/each}
			</div>
		</div>

		<div class="controls">
			<h3>Export Options</h3>

			<div class="option-group">
				<label>
					Background Color:
					<input type="color" bind:value={backgroundColor} />
				</label>
			</div>

			<div class="option-group">
				<label>
					Scale:
					<input type="range" min="1" max="4" step="0.5" bind:value={scale} />
					<span>{scale}x</span>
				</label>
			</div>

			<div class="option-group">
				<label>
					Quality:
					<input type="range" min="0.1" max="1" step="0.05" bind:value={quality} />
					<span>{Math.round(quality * 100)}%</span>
				</label>
			</div>

			<div class="option-group">
				<label>
					Format:
					<select bind:value={format}>
						<option value="png">PNG</option>
						<option value="jpeg">JPEG</option>
					</select>
				</label>
			</div>

			<div class="option-group">
				<label>
					Columns:
					<input type="number" min="1" max="10" bind:value={columns} />
				</label>
			</div>

			<div class="option-group">
				<label>
					Spacing:
					<input type="number" min="0" max="100" bind:value={spacing} />
				</label>
			</div>

			<h4>Content Options</h4>

			<div class="option-group">
				<label>
					<input type="checkbox" bind:checked={addWord} />
					Add Title
				</label>
				{#if addWord}
					<input type="text" bind:value={title} placeholder="Title" />
				{/if}
			</div>

			<div class="option-group">
				<label>
					<input type="checkbox" bind:checked={addUserInfo} />
					Add User Info
				</label>
				{#if addUserInfo}
					<input type="text" bind:value={userName} placeholder="User Name" />
					<input type="text" bind:value={notes} placeholder="Notes" />

					<div class="note-length-test">
						<span>Test note lengths:</span>
						<div class="note-buttons">
							{#each noteOptions as option}
								<button class="note-test-button" onclick={() => (notes = option.text)}>
									{option.label}
								</button>
							{/each}
						</div>
					</div>
				{/if}
			</div>

			<div class="option-group">
				<label>
					<input type="checkbox" bind:checked={addDifficultyLevel} />
					Add Difficulty Level
				</label>
				{#if addDifficultyLevel}
					<input type="range" min="1" max="5" step="1" bind:value={difficultyLevel} />
					<span>Level {difficultyLevel}</span>
				{/if}
			</div>

			<div class="option-group">
				<label>
					<input type="checkbox" bind:checked={showBeatNumbers} />
					Show Beat Numbers
				</label>
			</div>

			<div class="option-group">
				<div class="info-text">Start position is always included</div>
			</div>

			<div class="option-group">
				<label>
					Number of Beats:
					<div class="beat-count-controls">
						<button
							class="beat-count-button"
							onclick={decrementBeatCount}
							disabled={beats.length <= 1}
						>
							-
						</button>
						<span class="beat-count">{beats.length}</span>
						<button
							class="beat-count-button"
							onclick={incrementBeatCount}
							disabled={beats.length >= 20}
						>
							+
						</button>
					</div>
				</label>
			</div>

			<div class="actions">
				<button onclick={handleExport} disabled={isExporting} class="export-button">
					{isExporting ? 'Exporting...' : 'Export Sequence'}
				</button>
			</div>
		</div>

		<div class="result">
			<h3>Export Result</h3>

			{#if exportError}
				<div class="error">
					{exportError}
				</div>
			{/if}

			{#if exportResult}
				<div class="success">
					<p>Export successful!</p>
					<p>Dimensions: {exportResult.width}x{exportResult.height}</p>

					<div class="preview">
						<img src={exportResult.dataUrl} alt="Exported sequence" />
					</div>

					<button onclick={handleDownload} class="download-button"> Download Image </button>
				</div>
			{/if}
		</div>
	</div>
</div>

<style>
	.enhanced-export-tester {
		padding: 1rem;
		max-width: 1200px;
		margin: 0 auto;
	}

	h2,
	h3,
	h4 {
		margin-bottom: 1rem;
	}

	h2 {
		text-align: center;
	}

	.content {
		display: grid;
		grid-template-columns: 2fr 1fr 1fr;
		gap: 1rem;
	}

	.sequence-container,
	.controls,
	.result {
		padding: 1rem;
		border: 1px solid #ccc;
		border-radius: 4px;
		overflow: auto;
	}

	.beat-grid {
		display: grid;
		grid-template-columns: repeat(var(--columns), 1fr);
		gap: var(--spacing);
		margin-top: 1rem;
	}

	.beat-wrapper {
		position: relative;
		width: 150px;
		height: 150px;
	}

	.beat-label {
		position: absolute;
		top: -20px;
		left: 0;
		font-size: 12px;
		font-weight: bold;
	}

	.option-group {
		margin-bottom: 1rem;
	}

	.option-group label {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.info-text {
		font-style: italic;
		color: #666;
		padding: 0.5rem;
		background-color: #f0f0f0;
		border-radius: 4px;
	}

	.note-length-test {
		margin-top: 0.75rem;
	}

	.note-length-test span {
		display: block;
		margin-bottom: 0.5rem;
		font-size: 0.9rem;
		font-style: italic;
	}

	.note-buttons {
		display: flex;
		gap: 0.5rem;
	}

	.note-test-button {
		padding: 0.25rem 0.5rem;
		background-color: #4a90e2;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		font-size: 0.8rem;
	}

	.note-test-button:hover {
		background-color: #3a7bc8;
	}

	.option-group input[type='text'] {
		width: 100%;
		margin-top: 0.5rem;
		padding: 0.25rem;
	}

	.beat-count-controls {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		margin-left: 0.5rem;
	}

	.beat-count-button {
		width: 30px;
		height: 30px;
		border-radius: 50%;
		background-color: #4caf50;
		color: white;
		font-weight: bold;
		font-size: 18px;
		border: none;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 0;
	}

	.beat-count-button:hover {
		background-color: #45a049;
	}

	.beat-count-button:disabled {
		background-color: #cccccc;
		cursor: not-allowed;
	}

	.beat-count {
		font-weight: bold;
		min-width: 30px;
		text-align: center;
	}

	.actions {
		margin-top: 1.5rem;
	}

	.export-button,
	.download-button {
		padding: 0.5rem 1rem;
		background-color: #4caf50;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		font-weight: bold;
	}

	.export-button:hover,
	.download-button:hover {
		background-color: #45a049;
	}

	.export-button:disabled {
		background-color: #cccccc;
		cursor: not-allowed;
	}

	.error {
		color: #f44336;
		padding: 0.5rem;
		background-color: #ffebee;
		border-radius: 4px;
		margin-bottom: 1rem;
	}

	.preview {
		margin: 1rem 0;
		border: 1px solid #ddd;
		padding: 0.5rem;
		background-color: #f5f5f5;
		text-align: center;
		overflow: auto;
	}

	.preview img {
		max-width: 100%;
	}
</style>
