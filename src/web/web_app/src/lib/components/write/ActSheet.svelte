<!-- ActSheet.svelte - Main act editing sheet combining header and sequence grid -->
<script lang="ts">
	import type { ActData } from '$lib/types/write';
	import ActHeader from './ActHeader.svelte';
	import SequenceGrid from './SequenceGrid.svelte';

	// Props
	interface Props {
		act?: ActData | null;
		disabled?: boolean;
		onActInfoChanged?: (name: string, description: string) => void;
		onMusicLoadRequested?: () => void;
		onSequenceClicked?: (position: number) => void;
		onSequenceRemoveRequested?: (position: number) => void;
	}

	let {
		act = null,
		disabled = false,
		onActInfoChanged,
		onMusicLoadRequested,
		onSequenceClicked,
		onSequenceRemoveRequested,
	}: Props = $props();

	// Handle act info changes
	function handleActInfoChanged(name: string, description: string) {
		onActInfoChanged?.(name, description);
	}

	// Handle music load request
	function handleMusicLoadRequested() {
		onMusicLoadRequested?.();
	}

	// Handle sequence interactions
	function handleSequenceClicked(position: number) {
		onSequenceClicked?.(position);
	}

	function handleSequenceRemoveRequested(position: number) {
		onSequenceRemoveRequested?.(position);
	}
</script>

<div class="act-sheet" class:disabled class:no-act={!act}>
	{#if act}
		<!-- Act header with name, description, and music controls -->
		<div class="header-section">
			<ActHeader
				{act}
				{disabled}
				onActInfoChanged={handleActInfoChanged}
				onMusicLoadRequested={handleMusicLoadRequested}
			/>
		</div>

		<!-- Sequence grid -->
		<div class="sequences-section">
			<SequenceGrid
				sequences={act.sequences}
				onSequenceClicked={handleSequenceClicked}
				onSequenceRemoveRequested={handleSequenceRemoveRequested}
			/>
		</div>
	{:else}
		<!-- No act selected state -->
		<div class="no-act-state">
			<div class="no-act-icon">📄</div>
			<h3>No Act Selected</h3>
			<p>Select an act from the browser or create a new one to start editing.</p>
		</div>
	{/if}
</div>

<style>
	.act-sheet {
		display: flex;
		flex-direction: column;
		height: 100%;
		width: 100%;
		gap: var(--spacing-md);
		padding: var(--spacing-md);
		background: rgba(20, 20, 30, 0.2);
		border-radius: 8px;
		overflow: hidden;
		transition: all var(--transition-normal);
	}

	.act-sheet.disabled {
		opacity: 0.6;
		pointer-events: none;
	}

	.act-sheet.no-act {
		justify-content: center;
		align-items: center;
	}

	.header-section {
		flex-shrink: 0;
	}

	.sequences-section {
		flex: 1;
		min-height: 0; /* Allow flex child to shrink */
		display: flex;
		flex-direction: column;
	}

	.no-act-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		text-align: center;
		gap: var(--spacing-lg);
		max-width: 400px;
		padding: var(--spacing-xl);
	}

	.no-act-icon {
		font-size: 5rem;
		opacity: 0.4;
	}

	.no-act-state h3 {
		color: rgba(255, 255, 255, 0.8);
		font-size: var(--font-size-xl);
		margin: 0;
		font-family: 'Segoe UI', sans-serif;
	}

	.no-act-state p {
		color: rgba(255, 255, 255, 0.6);
		font-size: var(--font-size-base);
		margin: 0;
		line-height: 1.5;
		font-family: 'Segoe UI', sans-serif;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.act-sheet {
			padding: var(--spacing-sm);
			gap: var(--spacing-sm);
		}

		.no-act-state {
			padding: var(--spacing-lg);
			gap: var(--spacing-md);
		}

		.no-act-icon {
			font-size: 4rem;
		}

		.no-act-state h3 {
			font-size: var(--font-size-lg);
		}

		.no-act-state p {
			font-size: var(--font-size-sm);
		}
	}

	@media (max-width: 480px) {
		.act-sheet {
			padding: var(--spacing-xs);
			gap: var(--spacing-xs);
		}

		.no-act-state {
			padding: var(--spacing-md);
			gap: var(--spacing-sm);
		}

		.no-act-icon {
			font-size: 3rem;
		}

		.no-act-state h3 {
			font-size: var(--font-size-base);
		}

		.no-act-state p {
			font-size: var(--font-size-xs);
		}
	}

	/* Ensure proper scrolling behavior */
	@media (max-height: 600px) {
		.act-sheet {
			gap: var(--spacing-sm);
		}

		.no-act-state {
			gap: var(--spacing-sm);
		}

		.no-act-icon {
			font-size: 3rem;
		}
	}
</style>
