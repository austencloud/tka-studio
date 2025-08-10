<!-- SequenceViewerPanel.svelte - REFACTORED VERSION using pure Svelte 5 runes -->
<script lang="ts">
	import type { SequenceData } from '$domain/SequenceData';
	import SequenceViewer from './sequence-viewer/SequenceViewer.svelte';

	interface Props {
		sequence?: SequenceData;
		onBackToBrowser?: () => void;
		onSequenceAction?: (action: string, sequence: SequenceData) => void;
	}

	let { sequence = null, onBackToBrowser, onSequenceAction }: Props = $props();

	// Simple pass-through to the refactored SequenceViewer
	function handleBackToBrowser() {
		onBackToBrowser?.();
	}

	function handleSequenceAction(action: string, seq: SequenceData) {
		onSequenceAction?.(action, seq);
	}
</script>

<SequenceViewer
	{sequence}
	onBackToBrowser={handleBackToBrowser}
	onSequenceAction={handleSequenceAction}
/>
