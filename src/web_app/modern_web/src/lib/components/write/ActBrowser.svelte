<!-- ActBrowser.svelte - Act browser component with grid layout -->
<script lang="ts">
	import type { ActThumbnailInfo } from '$lib/types/write';
	import ActThumbnail from './ActThumbnail.svelte';

	// Props
	interface Props {
		acts?: ActThumbnailInfo[];
		isLoading?: boolean;
		onActSelected?: (filePath: string) => void;
		onRefresh?: () => void;
	}

	let { acts = [], isLoading = false, onActSelected, onRefresh }: Props = $props();

	// Handle refresh
	function handleRefresh() {
		onRefresh?.();
	}

	// Handle act selection
	function handleActSelected(filePath: string) {
		onActSelected?.(filePath);
	}

	// Calculate grid columns based on container width
	let containerElement: HTMLElement;
	let gridColumns = $state(1);

	function updateGridColumns() {
		if (!containerElement) return;

		const containerWidth = containerElement.clientWidth;
		const thumbnailWidth = 160; // Base thumbnail width
		const gap = 16; // Grid gap
		const padding = 32; // Container padding

		const availableWidth = containerWidth - padding;
		const columns = Math.max(1, Math.floor((availableWidth + gap) / (thumbnailWidth + gap)));
		gridColumns = columns;
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

<div class="act-browser" bind:this={containerElement}>
	<!-- Header -->
	<div class="browser-header">
		<h3 class="browser-title">Acts</h3>
		<button class="refresh-button btn-glass" onclick={handleRefresh} disabled={isLoading}>
			{#if isLoading}
				🔄 Loading...
			{:else}
				🔄 Refresh
			{/if}
		</button>
	</div>

	<!-- Content -->
	<div class="browser-content">
		{#if isLoading}
			<!-- Loading state -->
			<div class="loading-state">
				<div class="loading-spinner"></div>
				<p>Loading acts...</p>
			</div>
		{:else if acts.length === 0}
			<!-- Empty state -->
			<div class="empty-state">
				<div class="empty-icon">📄</div>
				<h4>No Acts Found</h4>
				<p>Create your first act to get started.</p>
				<button class="refresh-button btn-primary" onclick={handleRefresh}>
					🔄 Refresh
				</button>
			</div>
		{:else}
			<!-- Acts grid -->
			<div class="acts-grid" style="grid-template-columns: repeat({gridColumns}, 1fr);">
				{#each acts as act (act.id)}
					<ActThumbnail actInfo={act} onActSelected={handleActSelected} />
				{/each}
			</div>
		{/if}
	</div>
</div>

<style>
	.act-browser {
		display: flex;
		flex-direction: column;
		height: 100%;
		width: 100%;
		min-width: 250px;
		background: rgba(20, 20, 30, 0.3);
		border-radius: 8px;
		overflow: hidden;
	}

	.browser-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: var(--spacing-md);
		background: rgba(40, 40, 50, 0.8);
		border-bottom: 1px solid rgba(80, 80, 100, 0.4);
		backdrop-filter: var(--glass-backdrop);
	}

	.browser-title {
		color: rgba(255, 255, 255, 0.9);
		font-size: var(--font-size-lg);
		font-weight: bold;
		margin: 0;
	}

	.refresh-button {
		padding: var(--spacing-xs) var(--spacing-sm);
		border-radius: 6px;
		font-size: var(--font-size-sm);
		font-weight: 500;
		transition: all var(--transition-normal);
		white-space: nowrap;
	}

	.refresh-button:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.browser-content {
		flex: 1;
		overflow-y: auto;
		padding: var(--spacing-md);
	}

	.loading-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 200px;
		gap: var(--spacing-md);
	}

	.loading-spinner {
		width: 32px;
		height: 32px;
		border: 3px solid rgba(255, 255, 255, 0.2);
		border-top: 3px solid rgba(255, 255, 255, 0.8);
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	.loading-state p {
		color: rgba(255, 255, 255, 0.7);
		margin: 0;
	}

	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 300px;
		text-align: center;
		gap: var(--spacing-md);
	}

	.empty-icon {
		font-size: 4rem;
		opacity: 0.5;
	}

	.empty-state h4 {
		color: rgba(255, 255, 255, 0.9);
		font-size: var(--font-size-lg);
		margin: 0;
	}

	.empty-state p {
		color: rgba(255, 255, 255, 0.7);
		margin: 0;
		max-width: 200px;
	}

	.acts-grid {
		display: grid;
		gap: var(--spacing-md);
		justify-items: center;
		align-items: start;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.act-browser {
			min-width: 200px;
		}

		.browser-header {
			padding: var(--spacing-sm);
		}

		.browser-title {
			font-size: var(--font-size-base);
		}

		.refresh-button {
			padding: var(--spacing-xs);
			font-size: var(--font-size-xs);
		}

		.browser-content {
			padding: var(--spacing-sm);
		}

		.acts-grid {
			gap: var(--spacing-sm);
		}
	}

	@media (max-width: 480px) {
		.act-browser {
			min-width: 150px;
		}

		.empty-state {
			height: 200px;
		}

		.empty-icon {
			font-size: 3rem;
		}
	}

	/* Custom scrollbar */
	.browser-content::-webkit-scrollbar {
		width: 8px;
	}

	.browser-content::-webkit-scrollbar-track {
		background: rgba(40, 40, 50, 0.3);
		border-radius: 4px;
	}

	.browser-content::-webkit-scrollbar-thumb {
		background: rgba(80, 80, 100, 0.6);
		border-radius: 4px;
	}

	.browser-content::-webkit-scrollbar-thumb:hover {
		background: rgba(100, 100, 120, 0.8);
	}
</style>
