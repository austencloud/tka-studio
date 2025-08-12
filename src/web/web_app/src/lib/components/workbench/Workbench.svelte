<script lang="ts">
	import { sequenceStateService } from '$lib/services/SequenceStateService.svelte';
	import { workbenchService } from '$lib/services/WorkbenchService.svelte';
	import { onMount } from 'svelte';
	import ButtonPanel from './ButtonPanel.svelte';
	import SequenceContent from './SequenceContent.svelte';

	const hasSelection = $derived(sequenceStateService.selectedBeatIndex >= 0);

	onMount(() => {
		workbenchService.initialize();

		// Container element is available for future use if needed
	});

	function handleDeleteBeat() {
		const idx = sequenceStateService.selectedBeatIndex;
		if (idx >= 0) sequenceStateService.removeBeat(idx);
	}

	function handleClearSequence() {
		const seq = sequenceStateService.currentSequence;
		if (!seq) return;
		// Clear by setting zero beats
		sequenceStateService.setCurrentSequence({ ...seq, beats: [] });
	}

	function handleBeatSelected(index: number) {
		sequenceStateService.selectBeat(index);
	}

	// Advanced button actions (to be wired to services later)
	function handleAddToDictionary() {
		console.log('Add to Dictionary - to be implemented');
	}

	function handleFullscreen() {
		console.log('Fullscreen - to be implemented');
	}

	function handleMirror() {
		console.log('Mirror sequence - to be implemented');
	}

	function handleSwapColors() {
		console.log('Swap colors - to be implemented');
	}

	function handleRotate() {
		console.log('Rotate sequence - to be implemented');
	}

	function handleCopyJson() {
		const seq = sequenceStateService.currentSequence;
		if (seq) {
			navigator.clipboard.writeText(JSON.stringify(seq, null, 2));
			console.log('Copied sequence JSON to clipboard');
		}
	}
</script>

<div class="workbench">
	<div class="main-layout">
		<div class="left-vbox">
			<SequenceContent onBeatSelected={handleBeatSelected} />
		</div>
		<div class="workbench-button-panel">
			<ButtonPanel
				{hasSelection}
				onDeleteBeat={handleDeleteBeat}
				onClearSequence={handleClearSequence}
				onAddToDictionary={handleAddToDictionary}
				onFullscreen={handleFullscreen}
				onMirror={handleMirror}
				onSwapColors={handleSwapColors}
				onRotate={handleRotate}
				onCopyJson={handleCopyJson}
			/>
		</div>
	</div>
</div>

<style>
	.workbench {
		position: relative;
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		/* Transparent background to show beautiful app background */
		background: transparent;
	}

	.main-layout {
		display: grid;
		grid-template-columns: 1fr auto; /* left fills, right button panel auto width */
		gap: var(--spacing-xs); /* Add small gap between content and button panel */
		width: 100%;
		height: 100%;
	}

	.left-vbox {
		min-width: 0;
		display: flex;
		flex-direction: column;
	}

	.workbench-button-panel {
		display: flex;
	}
</style>
