<!-- src/lib/components/examples/SimpleStateExample.svelte -->
<script lang="ts">
	// Simple local state for testing
	let beatName = '';
	let isDarkTheme = false;
	let theme = 'light';
	let sequence: Array<{ id: string; name: string; data: { value: number } }> = [];
	let selectedBeatIndex: number | null = null;
	let isGenerating = false;
	let generationProgress = 0;
	let generationMessage = '';
	let error: string | null = null;

	// Handle form submission
	function handleAddBeat() {
		if (!beatName.trim()) return;

		sequence = [
			...sequence,
			{
				id: `beat-${Date.now()}`,
				name: beatName,
				data: { value: Math.random() }
			}
		];

		beatName = '';
	}

	// Handle beat selection
	function handleSelectBeat(index: number) {
		if (selectedBeatIndex === index) {
			selectedBeatIndex = null;
		} else {
			selectedBeatIndex = index;
		}
	}

	// Handle beat removal
	function handleRemoveBeat(index: number) {
		sequence = sequence.filter((_, i) => i !== index);
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
				sequence = Array.from({ length: 8 }, (_, i) => ({
					id: `beat-${i}`,
					name: `Generated Beat ${i + 1}`,
					data: { value: Math.random() }
				}));

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
		sequence = [];
		selectedBeatIndex = null;
	}
</script>

<div class="container" class:dark={isDarkTheme}>
	<header>
		<h1>Modern State Management Example</h1>
		<button on:click={toggleTheme}>
			Toggle Theme ({theme})
		</button>
	</header>

	<div class="sequence-controls">
		<h2>Sequence Controls</h2>

		<div class="control-group">
			<button on:click={generateSequence} disabled={isGenerating}> Generate Sequence </button>

			<button on:click={clearSequence} disabled={sequence.length === 0}> Clear Sequence </button>
		</div>

		{#if isGenerating}
			<div class="progress-container">
				<div class="progress-bar" style="width: {generationProgress}%"></div>
				<div class="progress-text">
					{generationMessage}
					({generationProgress}%)
				</div>
				<button on:click={cancelGeneration}> Cancel </button>
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
		<form on:submit|preventDefault={handleAddBeat}>
			<input type="text" bind:value={beatName} placeholder="Beat name" disabled={isGenerating} />
			<button type="submit" disabled={!beatName.trim() || isGenerating}> Add Beat </button>
		</form>
	</div>

	<div class="sequence-display">
		<h2>Sequence ({sequence.length} beats)</h2>

		{#if sequence.length === 0}
			<div class="empty-state">No beats in sequence. Generate or add beats to get started.</div>
		{:else}
			<ul class="beat-list">
				{#each sequence as beat, index}
					<div
						class="beat-item"
						class:selected={selectedBeatIndex === index}
						on:click={() => handleSelectBeat(index)}
						on:keydown={(e) => e.key === 'Enter' && handleSelectBeat(index)}
						tabindex="0"
						role="button"
					>
						<div class="beat-content">
							<span class="beat-index">{index + 1}</span>
							<span class="beat-name">{beat.name || `Beat ${index + 1}`}</span>
							<span class="beat-value">{beat.data?.value?.toFixed(2) || 'N/A'}</span>
						</div>
						<button
							class="remove-button"
							on:click|stopPropagation={() => handleRemoveBeat(index)}
							aria-label={`Remove beat ${index + 1}`}
						>
							✕
						</button>
					</div>
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

	.sequence-display {
		margin-top: 20px;
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
