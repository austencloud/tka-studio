<!-- src/lib/components/SequenceWorkbench/SharedWorkbench.svelte -->
<script lang="ts">
	import { workbenchStore } from '$lib/state/stores/workbenchStore';
	import SequenceWidget from './SequenceWidget.svelte';
	import RightPanel from './RightPanel/RightPanel.svelte';
	import ToolsPanel from './ToolsPanel/ToolsPanel.svelte';
	import { fly } from 'svelte/transition';
	import type { ButtonDefinition } from './ButtonPanel/types';

	// Props
	export let toolsPanelButtons: ButtonDefinition[];
	export let onToolsPanelAction: (id: string) => void;

	// Listen for toggleToolsPanel events
	import { onMount, onDestroy } from 'svelte';

	let toggleToolsPanelListener: (event: Event) => void;
	let closeToolsPanelListener: (event: Event) => void;

	onMount(() => {
		// Toggle tools panel listener
		toggleToolsPanelListener = () => {
			workbenchStore.update((state) => ({ ...state, toolsPanelOpen: !state.toolsPanelOpen }));
		};
		document.addEventListener('toggleToolsPanel', toggleToolsPanelListener);

		// Close tools panel listener
		closeToolsPanelListener = () => {
			workbenchStore.update((state) => ({ ...state, toolsPanelOpen: false }));
		};
		document.addEventListener('close-tools-panel', closeToolsPanelListener);

		// We no longer need a document-level event listener for button actions
		// as we're using Svelte's component events directly
		// This prevents the circular reference that was causing infinite recursion

		return () => {
			// No need to remove the button action listener as it no longer exists
		};
	});

	onDestroy(() => {
		if (toggleToolsPanelListener) {
			document.removeEventListener('toggleToolsPanel', toggleToolsPanelListener);
		}
		if (closeToolsPanelListener) {
			document.removeEventListener('close-tools-panel', closeToolsPanelListener);
		}
		// We no longer need to clean up the buttonActionListener
	});
</script>

<div class="shared-workbench">
	<div class="sequenceWorkbenchContainer">
		<SequenceWidget />
	</div>
	<div class="optionPickerContainer" class:tools-panel-active={$workbenchStore.toolsPanelOpen}>
		{#if $workbenchStore.toolsPanelOpen}
			<div class="tools-panel-overlay" transition:fly={{ duration: 300, x: 20 }}>
				<ToolsPanel
					buttons={toolsPanelButtons}
					activeMode={$workbenchStore.activeTab}
					on:action={(e) => onToolsPanelAction(e.detail.id)}
					on:close={() => workbenchStore.update((state) => ({ ...state, toolsPanelOpen: false }))}
				/>
			</div>
		{:else}
			<RightPanel />
		{/if}
	</div>
</div>

<style>
	.shared-workbench {
		display: flex;
		flex: 1;
		min-height: 0;
		overflow: hidden;
		position: relative;
		z-index: 1;
		width: 100%;
		height: 100%;
	}

	.sequenceWorkbenchContainer {
		flex: 1;
		min-width: 0;
		height: 100%;
		overflow: hidden;
		position: relative;
	}

	.optionPickerContainer {
		flex: 1;
		min-width: 0;
		height: 100%;
		overflow: hidden;
		display: flex;
		flex-direction: column;
		position: relative;
		box-sizing: border-box;
		transition: all 0.3s ease;
	}

	.tools-panel-active {
		background: rgba(248, 249, 250, 0.1);
		backdrop-filter: blur(5px);
		-webkit-backdrop-filter: blur(5px);
	}

	.tools-panel-overlay {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		z-index: 100;
		display: flex;
		flex-direction: column;
		overflow: hidden;
	}

	@media (max-width: 732px) {
		.shared-workbench {
			flex-direction: column;
		}

		.sequenceWorkbenchContainer {
			flex: 1;
			height: 50%;
		}

		.optionPickerContainer {
			flex: 1;
			height: 50%;
		}
	}
</style>
