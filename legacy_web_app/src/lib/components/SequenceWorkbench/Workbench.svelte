<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import SequenceWidget from './SequenceWidget.svelte';
	import { useResizeObserver } from '$lib/composables/useResizeObserver';

	// Props

	// Create event dispatcher for tools panel toggle
	const dispatch = createEventDispatcher();
	let computedEditorHeight = 0;
	const { size, resizeObserver } = useResizeObserver();
	$: sequenceWorkbenchHeight = $size.height;
	onMount(() => {
		if (typeof window !== 'undefined') {
			computedEditorHeight = Math.floor(window.innerHeight);
		}
	});
</script>

{#key undefined}
	<div class="sequence-workbench" use:resizeObserver>
		<SequenceWidget
		/>
	</div>
{/key}

<style>
	.sequence-workbench {
		position: relative;
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
		overflow: hidden;
	}
</style>
