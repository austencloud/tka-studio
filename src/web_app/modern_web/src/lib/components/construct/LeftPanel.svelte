<!--
	LeftPanel.svelte
	
	Left panel component extracted from ConstructTab.
	Contains the workbench with header showing sequence information.
-->
<script lang="ts">
	import Workbench from '$components/workbench/Workbench.svelte';
	import { constructTabState } from '$stores/constructTabState.svelte';

	// Reactive state from store
	let currentSequence = $derived(constructTabState.currentSequence);
</script>

<div class="left-panel" data-testid="left-panel">
	<div class="panel-header">
		<h2>Sequence Workbench</h2>
		{#if currentSequence}
			<div class="sequence-info">
				<span class="sequence-name">{currentSequence.name}</span>
				<span class="beat-count">{currentSequence.beats.length} beats</span>
			</div>
		{/if}
	</div>
	<div class="workbench-container">
		<Workbench />
	</div>
</div>

<style>
	.left-panel {
		flex: 1;
		display: flex;
		flex-direction: column;
		/* Transparent background to show beautiful background without blur */
		background: rgba(255, 255, 255, 0.05);
		/* backdrop-filter: blur(20px); - REMOVED to show background */
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: var(--border-radius);
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
		overflow: hidden;
	}

	.panel-header {
		flex-shrink: 0;
		padding: var(--spacing-lg);
		background: var(--muted) / 30;
		border-bottom: 1px solid var(--border);
		text-align: center;
	}

	.panel-header h2 {
		margin: 0 0 var(--spacing-sm) 0;
		color: var(--foreground);
		font-size: var(--font-size-xl);
		font-weight: 500;
	}

	.sequence-info {
		margin-top: var(--spacing-md);
		display: flex;
		justify-content: center;
		gap: var(--spacing-md);
		font-size: var(--font-size-sm);
	}

	.beat-count {
		padding: var(--spacing-xs) var(--spacing-sm);
		background: var(--primary);
		color: var(--primary-foreground);
		border-radius: var(--border-radius-sm);
		font-weight: 500;
	}

	.sequence-name {
		padding: var(--spacing-xs) var(--spacing-sm);
		background: var(--muted);
		color: var(--muted-foreground);
		border-radius: var(--border-radius-sm);
	}

	.workbench-container {
		flex: 1;
		overflow: auto;
		padding: var(--spacing-md);
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.panel-header {
			padding: var(--spacing-md);
		}
	}
</style>
