<script lang="ts">
	import { onMount } from 'svelte';
	import SequenceContent from './SequenceContent.svelte';
	import ButtonPanel from './ButtonPanel.svelte';
	import { sequenceStateService } from '$lib/services/SequenceStateService.svelte';
	import { workbenchService } from '$lib/services/WorkbenchService.svelte';

	let containerElement: HTMLElement;
	let containerHeight = $state(0);
	let containerWidth = $state(0);

	const hasSelection = $derived(sequenceStateService.selectedBeatIndex >= 0);

	onMount(() => {
		workbenchService.initialize();

		// Simple resize observer
		const observer = new ResizeObserver((entries) => {
			for (const entry of entries) {
				containerHeight = entry.contentRect.height;
				containerWidth = entry.contentRect.width;
			}
		});

		if (containerElement) {
			observer.observe(containerElement);
		}

		return () => observer.disconnect();
	});

	function handleDeleteBeat() {
		const idx = sequenceStateService.selectedBeatIndex;
		if (idx >= 0) sequenceStateService.removeBeat(idx);
	}

	function handleClearSequence() {
		const seq = sequenceStateService.currentSequence;
		if (!seq) return;
		// Clear by setting zero beats
		sequenceStateService.setCurrentSequence({ ...seq, beats: [] } as any);
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

<div class="workbench" bind:this={containerElement}>
	<div class="main-layout">
		<div class="left-vbox">
			<SequenceContent {containerHeight} {containerWidth} onBeatSelected={handleBeatSelected} />
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
		/* Glassmorphism transparency to show beautiful background */
		background: rgba(255, 255, 255, 0.05);
		backdrop-filter: blur(20px);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 12px;
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
	}

	.main-layout {
		display: grid;
		grid-template-columns: 1fr auto; /* left fills, right button panel auto width */
		gap: 0;
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
