<!-- src/lib/components/SequenceWorkbench/RightPanel/RightPanel.svelte -->
<script lang="ts">
	import { workbenchStore } from '../../state/stores/workbenchStore.js';
	import ModernGenerationControls from './ModernGenerationControls.svelte';
	import OptionPickerWithDebug from '../../components/ConstructTab/OptionPicker/OptionPickerWithDebug.svelte';
	import StartPosPicker from '../../components/ConstructTab/StartPosPicker/StartPosPicker.svelte';
	import { sequenceContainer } from '../../state/stores/sequence/SequenceContainer.js';
	import { useContainer } from '../../state/core/svelte5-integration.svelte';
	import { fade, fly } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	// Define the sequence container state type
	interface SequenceContainerState {
		beats: any[];
		startPosition: any;
		metadata: { name: string; difficulty: number };
		selectedBeatIds: string[];
	}

	// Get sequence data
	const sequence = useContainer(sequenceContainer) as SequenceContainerState;

	// Derive whether sequence is empty using inline logic to avoid function call issues
	const sequenceIsEmpty = $derived(!sequence.beats || sequence.beats.length === 0);

	// Debug logging
	$effect(() => {
		console.log('RightPanel: sequenceIsEmpty =', sequenceIsEmpty, 'beats =', sequence.beats?.length || 0);
	});

	// Transition parameters
	const transitionDuration = 400;
	const fadeParams = { duration: transitionDuration, easing: cubicInOut };
	const flyParams = {
		duration: transitionDuration,
		easing: cubicInOut,
		y: 20
	};
</script>

<div class="right-panel">
	{#if $workbenchStore.activeTab === 'generate'}
		<div in:fly={flyParams} out:fade={fadeParams}>
			<ModernGenerationControls />
		</div>
	{:else}
		<!-- Simplified panel switching without complex transitions -->
		{#if sequenceIsEmpty}
			<div class="panel-content" in:fly={flyParams} out:fade={fadeParams}>
				<StartPosPicker />
			</div>
		{:else}
			<div class="panel-content" in:fly={flyParams} out:fade={fadeParams}>
				<OptionPickerWithDebug />
			</div>
		{/if}
	{/if}
</div>

<style>
	.right-panel {
		position: relative;
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
		border-radius: 0.75rem;
		border: 1px solid rgba(255, 255, 255, 0.1);
		overflow: hidden;
	}

	/* Button panel container removed - now handled by SharedWorkbench */

	.panel-content {
		height: 100%;
		display: flex;
		flex-direction: column;
		width: 100%;
	}
</style>
