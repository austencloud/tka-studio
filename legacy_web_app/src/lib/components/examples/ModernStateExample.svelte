<script lang="ts">
	import { useContainer } from '$lib/state/core/svelte5-integration.svelte';
	import { sequenceContainer } from '$lib/state/stores/sequence/SequenceContainer';

	// Local state for the form
	let beatName = $state('');
	let isDarkTheme = $state(false);
	let theme = $state<'light' | 'dark' | 'system'>('light');
	let isGenerating = $state(false);
	let generationProgress = $state(0);
	let generationMessage = $state('');
	let error = $state<string | null>(null);

	// Use the sequence container with Svelte 5 runes
	const sequence = useContainer(sequenceContainer);

	// Handle form submission
	function handleAddBeat() {
		if (!beatName.trim()) return;

		sequenceContainer.addBeat({
			id: crypto.randomUUID(),
			number: sequence.beats.length + 1,
			letter: beatName
		});

		beatName = '';
	}

	// Handle beat selection
	function handleSelectBeat(beatId: string, multiSelect = false) {
		sequenceContainer.selectBeat(beatId, multiSelect);
	}

	// Handle beat removal
	function handleRemoveBeat(beatId: string) {
		sequenceContainer.removeBeat(beatId);
	}

	// Handle theme toggle
	function toggleTheme() {
		theme = theme === 'dark' ? 'light' : 'dark';
		isDarkTheme = theme === 'dark';
	}

	// Generate sequence
	function generateSequence() {
		isGenerating = true;
		generationProgress = 0;
		generationMessage = 'Initializing sequence generation...';

		// Simulate generation progress
		const interval = setInterval(() => {
			generationProgress += 10;

			if (generationProgress < 50) {
				generationMessage = 'Generating sequence...';
			} else if (generationProgress < 90) {
				generationMessage = 'Finalizing sequence...';
			} else {
				generationMessage = 'Generation complete';
				clearInterval(interval);

				// Generate a simple sequence
				const generatedBeats = Array.from({ length: 8 }, (_, i) => ({
					id: crypto.randomUUID(),
					number: i + 1,
					letter: `Generated Beat ${i + 1}`
				}));

				sequenceContainer.setSequence(generatedBeats);
				isGenerating = false;
			}
		}, 200);
	}

	// Cancel generation
	function cancelGeneration() {
		isGenerating = false;
		generationProgress = 0;
		generationMessage = 'Generation cancelled';
	}

	// Clear sequence
	function clearSequence() {
		sequenceContainer.setSequence([]);
	}
</script>

<div class="container" class:dark={isDarkTheme}>
	<header>
		<h1>State Management Example (Svelte 5 + XState 5)</h1>
		<button onclick={toggleTheme}>
			Toggle Theme ({theme})
		</button>
	</header>

	<div class="sequence-controls">
		<h2>Sequence Controls</h2>

		<div class="control-group">
			<button onclick={generateSequence} disabled={isGenerating}>Generate Sequence</button>
			<button onclick={clearSequence} disabled={sequence.beats.length === 0}>Clear Sequence</button>
		</div>

		{#if isGenerating}
			<div class="progress-container">
				<div class="progress-bar" style="width: {generationProgress}%"></div>
				<div class="progress-text">
					{generationMessage}
					({generationProgress}%)
				</div>
				<button onclick={cancelGeneration}>Cancel</button>
			</div>
		{/if}

		{#if error}
			<div class="error">
				Error: {error}
			</div>
		{/if}
	</div>

	<div class="add-beat-form">
		<h2>Add Beat</h2>
		<form
			onsubmit={(e) => {
				e.preventDefault();
				handleAddBeat();
			}}
		>
			<input type="text" bind:value={beatName} placeholder="Beat name" disabled={isGenerating} />
			<button type="submit" disabled={!beatName.trim() || isGenerating}>Add Beat</button>
		</form>
	</div>

	<div class="sequence-display">
		<h2>Sequence ({sequence.beats.length} beats)</h2>

		{#if sequence.beats.length === 0}
			<div class="empty-state">No beats in sequence. Generate or add beats to get started.</div>
		{:else}
			<ul class="beat-list">
				{#each sequence.beats as beat}
					<div
						class="beat-item"
						class:selected={sequence.selectedBeatIds.includes(beat.id)}
						onclick={() => handleSelectBeat(beat.id)}
						onkeydown={(e) => e.key === 'Enter' && handleSelectBeat(beat.id)}
						tabindex="0"
						role="button"
					>
						<div class="beat-content">
							<span class="beat-index">{beat.number}</span>
							<span class="beat-name">{beat.letter || `Beat ${beat.number}`}</span>
							<span class="beat-value">{beat.id.substring(0, 8)}</span>
						</div>
						<button
							class="remove-button"
							onclick={(e) => {
								e.stopPropagation();
								handleRemoveBeat(beat.id);
							}}
							aria-label={`Remove beat ${beat.number}`}
						>
							✕
						</button>
					</div>
				{/each}
			</ul>
		{/if}
	</div>

	<div class="selection-info">
		<h2>Selected Beats ({sequence.selectedBeatIds.length})</h2>

		{#if sequence.selectedBeatIds.length === 0}
			<div class="empty-state">No beats selected. Click on a beat to select it.</div>
		{:else}
			<ul class="selected-beats">
				{#each sequence.beats.filter((beat) => sequence.selectedBeatIds.includes(beat.id)) as beat}
					<li>Beat {beat.number} - {beat.letter || 'Unnamed'}</li>
				{/each}
			</ul>
		{/if}
	</div>
</div>

<style>
	.container {
		max-width: 800px;
		margin: 0 auto;
		padding: 20px;
		font-family:
			system-ui,
			-apple-system,
			BlinkMacSystemFont,
			'Segoe UI',
			Roboto,
			sans-serif;
		color: #333;
		background-color: #f5f5f5;
		border-radius: 8px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	}

	.container.dark {
		background-color: #222;
		color: #eee;
	}

	header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 20px;
		padding-bottom: 10px;
		border-bottom: 1px solid #ddd;
	}

	.container.dark header {
		border-bottom-color: #444;
	}

	h1 {
		font-size: 24px;
		margin: 0;
	}

	h2 {
		font-size: 18px;
		margin: 0 0 10px 0;
	}

	button {
		background-color: #4a90e2;
		color: white;
		border: none;
		padding: 8px 16px;
		border-radius: 4px;
		cursor: pointer;
		font-size: 14px;
	}

	button:hover {
		background-color: #3a80d2;
	}

	button:disabled {
		background-color: #a0a0a0;
		cursor: not-allowed;
	}

	.control-group {
		display: flex;
		gap: 10px;
		margin-bottom: 15px;
	}

	.progress-container {
		margin: 15px 0;
		background-color: #e0e0e0;
		border-radius: 4px;
		overflow: hidden;
		position: relative;
		height: 30px;
	}

	.container.dark .progress-container {
		background-color: #444;
	}

	.progress-bar {
		height: 100%;
		background-color: #4caf50;
		transition: width 0.3s ease;
	}

	.progress-text {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #333;
		font-size: 14px;
	}

	.container.dark .progress-text {
		color: #fff;
	}

	.error {
		background-color: #ffebee;
		color: #c62828;
		padding: 10px;
		border-radius: 4px;
		margin: 10px 0;
	}

	.container.dark .error {
		background-color: #4a1010;
		color: #ff8a80;
	}

	.add-beat-form {
		margin: 20px 0;
	}

	.add-beat-form form {
		display: flex;
		gap: 10px;
	}

	input {
		flex: 1;
		padding: 8px;
		border: 1px solid #ddd;
		border-radius: 4px;
		font-size: 14px;
	}

	.container.dark input {
		background-color: #333;
		color: #eee;
		border-color: #555;
	}

	.sequence-display,
	.selection-info {
		margin-top: 20px;
	}

	.selected-beats {
		list-style: none;
		padding: 0;
		margin: 10px 0;
	}

	.selected-beats li {
		background-color: #e3f2fd;
		padding: 8px 12px;
		margin-bottom: 5px;
		border-radius: 4px;
		border-left: 4px solid #2196f3;
	}

	.container.dark .selected-beats li {
		background-color: #1a3f5f;
		border-left-color: #64b5f6;
		color: #eee;
	}

	.empty-state {
		padding: 20px;
		text-align: center;
		background-color: #f0f0f0;
		border-radius: 4px;
		color: #666;
	}

	.container.dark .empty-state {
		background-color: #333;
		color: #aaa;
	}

	.beat-list {
		list-style: none;
		padding: 0;
		margin: 0;
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.beat-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 10px;
		background-color: white;
		border-radius: 4px;
		cursor: pointer;
		transition: all 0.2s ease;
		width: 100%;
		text-align: left;
	}

	.container.dark .beat-item {
		background-color: #333;
	}

	.beat-item:hover {
		transform: translateX(5px);
	}

	.beat-item.selected {
		background-color: #e3f2fd;
		border-left: 4px solid #2196f3;
	}

	.container.dark .beat-item.selected {
		background-color: #1a3f5f;
		border-left-color: #64b5f6;
	}

	.beat-content {
		display: flex;
		align-items: center;
		gap: 10px;
	}

	.beat-index {
		background-color: #eee;
		color: #333;
		width: 24px;
		height: 24px;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 12px;
		font-weight: bold;
	}

	.container.dark .beat-index {
		background-color: #555;
		color: #eee;
	}

	.beat-name {
		font-weight: 500;
	}

	.beat-value {
		color: #666;
		font-size: 12px;
	}

	.container.dark .beat-value {
		color: #aaa;
	}

	.remove-button {
		background-color: transparent;
		color: #f44336;
		padding: 4px 8px;
		font-size: 12px;
	}

	.remove-button:hover {
		background-color: #ffebee;
	}

	.container.dark .remove-button {
		color: #ff8a80;
	}

	.container.dark .remove-button:hover {
		background-color: #4a1010;
	}
</style>
