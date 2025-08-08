<script lang="ts">
	import type { SequenceData } from '../../types/core.js';

	// Props
	let {
		sequenceData = null,
		onBeatSelect = () => {}
	}: {
		sequenceData?: SequenceData | null;
		onBeatSelect?: (_beatNumber: number) => void;
	} = $props();

	// State
	let selectedBeat = $state<number | null>(null);
	let showJsonData = $state(false);

	// Computed values
	let beats = $derived.by(() => {
		if (!sequenceData) return [];

		// Filter to get only actual beats (not metadata or start position)
		return sequenceData.filter((entry) => {
			// Skip metadata entries
			if (entry.metadata) return false;
			// Skip start position (beat: 0)
			if (entry.beat === 0) return false;
			// Keep only actual beats (beat >= 1)
			return typeof entry.beat === 'number' && entry.beat >= 1;
		});
	});

	let selectedBeatData = $derived.by(() => {
		if (selectedBeat === null || !beats.length) return null;
		return beats.find((beat) => beat.beat === selectedBeat);
	});

	function handleBeatClick(beatNumber: number): void {
		selectedBeat = beatNumber;
		// Pass the actual beat number (not array index) to the parent
		onBeatSelect(beatNumber);
	}

	function toggleJsonView(): void {
		showJsonData = !showJsonData;
	}

	function copyJsonToClipboard(): void {
		if (selectedBeatData) {
			navigator.clipboard.writeText(JSON.stringify(selectedBeatData, null, 2));
		}
	}
</script>

{#if sequenceData}
	<div class="beat-viewer">
		<!-- Compact header with controls -->
		<div class="beat-viewer-header">
			<div class="header-left">
				<h3>Beat Inspector</h3>
				{#if beats.length > 0}
					<span class="beat-count">{beats.length} beats</span>
				{/if}
			</div>

			{#if selectedBeat !== null && selectedBeatData}
				<div class="header-right">
					<span class="selected-beat">Beat {selectedBeat}</span>
					<button class="toggle-button" onclick={toggleJsonView}>
						{showJsonData ? 'Hide' : 'Show'} JSON
					</button>
					{#if showJsonData}
						<button
							class="copy-button"
							onclick={copyJsonToClipboard}
							title="Copy JSON to clipboard"
						>
							📋 Copy
						</button>
					{/if}
				</div>
			{/if}
		</div>

		<!-- Beat Selector Buttons (horizontal, space-efficient) -->
		{#if beats.length > 0}
			<div class="beat-buttons-container">
				{#each beats as beat}
					<button
						class="beat-button"
						class:selected={selectedBeat === beat.beat}
						onclick={() => handleBeatClick(beat.beat as number)}
						title="Beat {beat.beat}"
					>
						{beat.beat}
					</button>
				{/each}
			</div>
		{:else}
			<p class="no-beats">No beats found in sequence data</p>
		{/if}

		<!-- JSON Display (inline, appears below buttons when toggled) -->
		{#if selectedBeat !== null && selectedBeatData && showJsonData}
			<div class="json-display">
				<textarea readonly value={JSON.stringify(selectedBeatData, null, 2)} class="json-textarea"
				></textarea>
			</div>
		{/if}
	</div>
{/if}

<style>
	.beat-viewer {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
		padding: 0.75rem;
		background: var(--color-surface-elevated);
		border-radius: 8px;
		border: 1px solid var(--color-border);
		margin-top: 0.5rem; /* Reduced spacing from controls above */
	}

	.beat-viewer-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		flex-wrap: wrap;
		gap: 0.5rem;
	}

	.header-left {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.header-left h3 {
		margin: 0;
		font-size: 0.875rem;
		font-weight: 600;
		color: var(--color-text);
	}

	.beat-count {
		font-size: 0.75rem;
		color: var(--color-text-secondary);
		background: var(--color-surface);
		padding: 0.25rem 0.5rem;
		border-radius: 12px;
		border: 1px solid var(--color-border);
	}

	.header-right {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.selected-beat {
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--color-text);
		background: var(--color-primary-subtle);
		padding: 0.25rem 0.5rem;
		border-radius: 4px;
	}

	.beat-buttons-container {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(40px, 1fr));
		gap: 0.375rem;
		max-height: 120px; /* Compact height */
		overflow-y: auto;
		padding: 0.5rem;
		background: var(--color-surface);
		border-radius: 6px;
		border: 1px solid var(--color-border);
	}

	.beat-button {
		height: 36px; /* Slightly smaller for compactness */
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 6px;
		color: var(--color-text);
		font-weight: 600;
		font-size: 0.875rem;
		cursor: pointer;
		transition: all 0.2s ease;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.beat-button:hover {
		background: var(--color-surface-hover);
		border-color: var(--color-primary);
	}

	.beat-button.selected {
		background: var(--color-primary);
		color: white;
		border-color: var(--color-primary);
	}

	.no-beats {
		color: var(--color-text-secondary);
		font-style: italic;
		text-align: center;
		margin: 1rem 0;
	}

	.toggle-button,
	.copy-button {
		background: var(--color-primary);
		color: white;
		border: none;
		border-radius: 4px;
		padding: 0.375rem 0.75rem;
		font-size: 0.75rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.toggle-button:hover,
	.copy-button:hover {
		background: var(--color-primary-hover);
	}

	.copy-button {
		background: var(--color-success);
	}

	.copy-button:hover {
		background: #45a049;
	}

	.json-display {
		margin-top: 0.5rem;
		background: var(--color-surface);
		border-radius: 6px;
		border: 1px solid var(--color-border);
		overflow: hidden;
	}

	.json-textarea {
		width: 100%;
		height: 250px; /* Compact height */
		background: var(--color-surface);
		border: none;
		padding: 0.75rem;
		font-family: 'Courier New', monospace;
		font-size: 0.75rem;
		color: var(--color-text);
		resize: vertical;
		line-height: 1.4;
	}

	.json-textarea:focus {
		outline: none;
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.beat-viewer {
			padding: 0.5rem;
			margin-top: 0.25rem;
		}

		.beat-viewer-header {
			flex-direction: column;
			align-items: stretch;
		}

		.header-right {
			justify-content: center;
		}

		.beat-buttons-container {
			grid-template-columns: repeat(auto-fit, minmax(36px, 1fr));
			max-height: 100px;
		}

		.beat-button {
			height: 32px;
			font-size: 0.8rem;
		}

		.json-textarea {
			height: 200px;
			font-size: 0.7rem;
		}
	}
</style>
