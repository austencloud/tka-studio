<!-- src/lib/components/SequenceWorkbench/GraphEditor/GraphEditor.svelte -->
<script lang="ts">
	// No store imports needed
	import TurnsBox from './TurnsBox/TurnsBox.svelte';
	import Pictograph from '$lib/components/Pictograph/Pictograph.svelte';
	import type { PictographData } from '$lib/types/PictographData';
	import { DIAMOND } from '$lib/types/Constants';

	// Component props with defaults
	export let isExpanded = false;
	export let animationDuration = 300;
	export let maxEditorHeight = 300;

	// Derived values with pure calculations
	$: borderSize = Math.floor(maxEditorHeight * 0.02); // 2% border
	$: contentWidth = maxEditorHeight - 2 * borderSize;
	$: contentHeight = contentWidth; // Square content

	// Create pictograph data - this is local to the component
	// and does not need to be shared with other components
	let pictographData: PictographData = {
		letter: null,
		startPos: null,
		endPos: null,
		timing: null,
		direction: null,
		gridMode: DIAMOND,
		blueMotionData: null,
		redMotionData: null,
		gridData: null,
		redPropData: null,
		bluePropData: null,
		redArrowData: null,
		blueArrowData: null,
		grid: ''
	};

	// Helper function to update pictograph data (if needed)
	function updatePictographData(newData: Partial<PictographData>) {
		pictographData = {
			...pictographData,
			...newData
		};
	}
</script>

<div
	class="graph-editor"
	style="
	  --animation-duration: {animationDuration}ms;
	  --editor-height: {isExpanded ? maxEditorHeight : 0}px;
	  --border-size: {borderSize}px;
	  --content-width: {contentWidth}px;
	  --content-height: {contentHeight}px;
	"
>
	<div class="turns-box-container">
		<TurnsBox color="blue" />
	</div>

	<div class="pictograph-container">
		<Pictograph {pictographData} />
	</div>

	<div class="turns-box-container">
		<TurnsBox color="red" />
	</div>
</div>

<style>
	.graph-editor {
		position: relative;
		background-color: #f4f4f4;
		overflow: hidden;
		height: var(--editor-height);
		transition: height var(--animation-duration) ease-in-out;
		display: flex;
		flex-direction: row;
		align-items: stretch;
		justify-content: space-between;
	}

	.turns-box-container {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: stretch;
		justify-content: stretch;
		height: 100%;
		min-width: 0;
	}

	.pictograph-container {
		cursor: default;
		border: var(--border-size) solid gold;
		width: var(--content-width);
		height: var(--content-height);
		display: flex;
		justify-content: center;
		align-items: center;
	}
</style>
