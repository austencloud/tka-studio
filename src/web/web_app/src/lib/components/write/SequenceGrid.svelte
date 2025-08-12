<!-- SequenceGrid.svelte - Grid component for displaying sequences -->
<script lang="ts">
	import type { SequenceData } from '$lib/types/write';
	import SequenceThumbnail from './SequenceThumbnail.svelte';

	// Props
	interface Props {
		sequences?: SequenceData[];
		onSequenceClicked?: (position: number) => void;
		onSequenceRemoveRequested?: (position: number) => void;
	}

	let { sequences = [], onSequenceClicked, onSequenceRemoveRequested }: Props = $props();

	// Handle sequence click
	function handleSequenceClicked(position: number) {
		onSequenceClicked?.(position);
	}

	// Handle sequence remove
	function handleSequenceRemoveRequested(position: number) {
		onSequenceRemoveRequested?.(position);
	}

	// Calculate grid columns based on container width
	let containerElement: HTMLElement;
	let gridColumns = $state(6); // Default to 6 columns like desktop

	function updateGridColumns() {
		if (!containerElement) return;

		const containerWidth = containerElement.clientWidth;
		const thumbnailWidth = 120; // Base thumbnail width
		const gap = 10; // Grid gap
		const padding = 20; // Container padding

		const availableWidth = containerWidth - padding;
		const columns = Math.max(1, Math.floor((availableWidth + gap) / (thumbnailWidth + gap)));
		gridColumns = Math.min(columns, 8); // Max 8 columns
	}

	// Update grid on resize
	$effect(() => {
		if (containerElement) {
			updateGridColumns();

			const resizeObserver = new ResizeObserver(() => {
				updateGridColumns();
			});

			resizeObserver.observe(containerElement);

			return () => {
				resizeObserver.disconnect();
			};
		}
		return () => {}; // Return empty cleanup function when no container
	});
</script>

<div class="sequence-grid-container" bind:this={containerElement}>
	{#if sequences.length === 0}
		<!-- Empty state -->
		<div class="empty-state">
			<div class="empty-icon">🎭</div>
			<h4>No sequences in this act</h4>
			<p>Add sequences from the Construct tab</p>
		</div>
	{:else}
		<!-- Sequences grid -->
		<div class="sequences-grid" style="grid-template-columns: repeat({gridColumns}, 1fr);">
			{#each sequences as sequence, index (sequence.id)}
				<SequenceThumbnail
					{sequence}
					position={index}
					onSequenceClicked={handleSequenceClicked}
					onRemoveRequested={handleSequenceRemoveRequested}
				/>
			{/each}
		</div>
	{/if}
</div>

<style>
	.sequence-grid-container {
		flex: 1;
		overflow-y: auto;
		padding: var(--spacing-sm);
		background: rgba(20, 20, 30, 0.3);
		border-radius: 8px;
		min-height: 200px;
	}

	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100%;
		min-height: 200px;
		text-align: center;
		gap: var(--spacing-md);
	}

	.empty-icon {
		font-size: 4rem;
		opacity: 0.5;
	}

	.empty-state h4 {
		color: rgba(255, 255, 255, 0.8);
		font-size: var(--font-size-lg);
		margin: 0;
	}

	.empty-state p {
		color: rgba(255, 255, 255, 0.6);
		margin: 0;
		font-size: var(--font-size-sm);
	}

	.sequences-grid {
		display: grid;
		gap: var(--spacing-sm);
		justify-items: center;
		align-items: start;
		padding: var(--spacing-sm);
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.sequence-grid-container {
			padding: var(--spacing-xs);
		}

		.sequences-grid {
			gap: var(--spacing-xs);
			padding: var(--spacing-xs);
		}

		.empty-state {
			min-height: 150px;
			gap: var(--spacing-sm);
		}

		.empty-icon {
			font-size: 3rem;
		}

		.empty-state h4 {
			font-size: var(--font-size-base);
		}

		.empty-state p {
			font-size: var(--font-size-xs);
		}
	}

	@media (max-width: 480px) {
		.sequence-grid-container {
			padding: 2px;
		}

		.sequences-grid {
			gap: 4px;
			padding: 4px;
		}

		.empty-state {
			min-height: 120px;
		}

		.empty-icon {
			font-size: 2.5rem;
		}

		.empty-state h4 {
			font-size: var(--font-size-sm);
		}

		.empty-state p {
			font-size: 10px;
		}
	}

	/* Custom scrollbar */
	.sequence-grid-container::-webkit-scrollbar {
		width: 8px;
	}

	.sequence-grid-container::-webkit-scrollbar-track {
		background: rgba(40, 40, 50, 0.3);
		border-radius: 4px;
	}

	.sequence-grid-container::-webkit-scrollbar-thumb {
		background: rgba(80, 80, 100, 0.6);
		border-radius: 4px;
	}

	.sequence-grid-container::-webkit-scrollbar-thumb:hover {
		background: rgba(100, 100, 120, 0.8);
	}

	/* Grid auto-sizing for different screen sizes */
	@container (max-width: 600px) {
		.sequences-grid {
			grid-template-columns: repeat(auto-fit, minmax(80px, 1fr)) !important;
		}
	}

	@container (max-width: 400px) {
		.sequences-grid {
			grid-template-columns: repeat(auto-fit, minmax(70px, 1fr)) !important;
		}
	}
</style>
