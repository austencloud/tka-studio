<!-- Thumbnail Browser Component -->
<script lang="ts">
	import type { MetadataTesterState, ThumbnailFile } from '../state/metadata-tester-state.svelte';

	interface Props {
		state: {
			state: MetadataTesterState;
			extractMetadata: (thumbnail: ThumbnailFile) => Promise<void>;
			loadThumbnails: () => Promise<void>;
			clearSelection: () => void;
			handleBatchAnalyze: () => Promise<void>;
		};
	}

	let { state }: Props = $props();

	// Handle thumbnail click
	async function handleThumbnailClick(thumbnail: ThumbnailFile) {
		await state.extractMetadata(thumbnail);
	}

	// Handle refresh
	async function handleRefresh() {
		await state.loadThumbnails();
	}

	// Handle batch analyze
	async function handleBatchAnalyze() {
		await state.handleBatchAnalyze();
	}
</script>

<div class="thumbnail-browser">
	<div class="browser-header">
		<h2>📁 Available Sequences</h2>
		<div class="header-actions">
			<button class="batch-analyze-btn" onclick={handleBatchAnalyze} 
					disabled={state.state.isLoadingThumbnails || state.state.isBatchAnalyzing || state.state.thumbnails.length === 0}>
				{#if state.state.isBatchAnalyzing}
					⏳ Analyzing...
				{:else}
					🔍 Batch Analyze
				{/if}
			</button>
			<button class="refresh-btn" onclick={handleRefresh} disabled={state.state.isLoadingThumbnails}>
				{state.state.isLoadingThumbnails ? '🔄' : '↻'} Refresh
			</button>
		</div>
	</div>

	<div class="thumbnail-grid-container">
		{#if state.state.isLoadingThumbnails}
			<div class="loading-state">
				<div class="spinner"></div>
				<p>Loading thumbnails...</p>
			</div>
		{:else if state.state.error}
			<div class="error-state">
				<p>❌ {state.state.error}</p>
				<button class="retry-btn" onclick={handleRefresh}>Retry</button>
			</div>
		{:else if state.state.thumbnails.length === 0}
			<div class="empty-state">
				<p>📭 No thumbnails found</p>
				<p class="help-text">Make sure PNG files are available in the static directories</p>
			</div>
		{:else}
			<div class="thumbnail-grid">
				{#each state.state.thumbnails as thumbnail (thumbnail.path)}
					<button 
						class="thumbnail-card"
						class:selected={state.state.selectedThumbnail?.path === thumbnail.path}
						onclick={() => handleThumbnailClick(thumbnail)}
						aria-label="Select {thumbnail.word} sequence for metadata extraction"
					>
						<div class="thumbnail-image">
							<img 
								src={thumbnail.path} 
								alt={thumbnail.name}
								loading="lazy"
							/>
						</div>
						<div class="thumbnail-info">
							<h3 class="sequence-name">{thumbnail.word}</h3>
							<p class="file-name">{thumbnail.name}</p>
						</div>
					</button>
				{/each}
			</div>
		{/if}
	</div>

	{#if state.state.selectedThumbnail}
		<div class="selection-info">
			<p>📌 Selected: <strong>{state.state.selectedThumbnail.word}</strong></p>
			<button class="clear-btn" onclick={state.clearSelection}>Clear Selection</button>
		</div>
	{/if}
</div>

<style>
	.thumbnail-browser {
		display: flex;
		flex-direction: column;
		height: 100%;
		overflow: hidden;
	}

	.browser-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 20px;
		padding-bottom: 15px;
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	}

	.header-actions {
		display: flex;
		gap: 10px;
	}

	.refresh-btn,
	.batch-analyze-btn {
		background: rgba(59, 130, 246, 0.2);
		border: 1px solid rgba(59, 130, 246, 0.4);
		color: #60a5fa;
		padding: 8px 16px;
		border-radius: 6px;
		cursor: pointer;
		font-size: 0.9rem;
		transition: all 0.2s ease;
	}

	.batch-analyze-btn {
		background: rgba(168, 85, 247, 0.2);
		border-color: rgba(168, 85, 247, 0.4);
		color: #a855f7;
	}

	.refresh-btn:hover:not(:disabled),
	.batch-analyze-btn:hover:not(:disabled) {
		background: rgba(59, 130, 246, 0.3);
		border-color: rgba(59, 130, 246, 0.6);
	}

	.batch-analyze-btn:hover:not(:disabled) {
		background: rgba(168, 85, 247, 0.3);
		border-color: rgba(168, 85, 247, 0.6);
	}

	.refresh-btn:disabled,
	.batch-analyze-btn:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.thumbnail-grid-container {
		flex: 1;
		overflow-y: auto;
		scrollbar-width: thin;
		scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
	}

	.thumbnail-grid-container::-webkit-scrollbar {
		width: 8px;
	}

	.thumbnail-grid-container::-webkit-scrollbar-track {
		background: transparent;
	}

	.thumbnail-grid-container::-webkit-scrollbar-thumb {
		background: rgba(255, 255, 255, 0.2);
		border-radius: 4px;
	}

	.thumbnail-grid-container::-webkit-scrollbar-thumb:hover {
		background: rgba(255, 255, 255, 0.3);
	}

	.thumbnail-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
		gap: 15px;
		padding: 10px;
	}

	.thumbnail-card {
		background: rgba(255, 255, 255, 0.05);
		border: 2px solid rgba(255, 255, 255, 0.1);
		border-radius: 12px;
		padding: 15px;
		cursor: pointer;
		transition: all 0.3s ease;
		display: flex;
		flex-direction: column;
		align-items: center;
		text-align: center;
		width: 100%;
		font-family: inherit;
		color: inherit;
	}

	.thumbnail-card:hover {
		background: rgba(255, 255, 255, 0.1);
		border-color: rgba(59, 130, 246, 0.4);
		transform: translateY(-2px);
	}

	.thumbnail-card.selected {
		background: rgba(59, 130, 246, 0.15);
		border-color: rgba(59, 130, 246, 0.6);
		box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
	}

	.thumbnail-image {
		width: 100%;
		height: 120px;
		margin-bottom: 12px;
		border-radius: 8px;
		overflow: hidden;
		background: rgba(255, 255, 255, 0.05);
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.thumbnail-image img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		border-radius: 6px;
	}

	.thumbnail-info h3 {
		margin: 0 0 5px 0;
		font-size: 1.1rem;
		color: #60a5fa;
	}

	.thumbnail-info p {
		margin: 0;
		font-size: 0.85rem;
		opacity: 0.7;
		word-break: break-all;
	}

	.loading-state,
	.error-state,
	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 300px;
		text-align: center;
	}

	.spinner {
		width: 40px;
		height: 40px;
		border: 3px solid rgba(255, 255, 255, 0.1);
		border-top: 3px solid #60a5fa;
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin-bottom: 15px;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}

	.retry-btn,
	.clear-btn {
		background: rgba(239, 68, 68, 0.2);
		border: 1px solid rgba(239, 68, 68, 0.4);
		color: #f87171;
		padding: 6px 12px;
		border-radius: 4px;
		cursor: pointer;
		font-size: 0.8rem;
		margin-top: 10px;
		transition: all 0.2s ease;
	}

	.retry-btn:hover,
	.clear-btn:hover {
		background: rgba(239, 68, 68, 0.3);
		border-color: rgba(239, 68, 68, 0.6);
	}

	.selection-info {
		margin-top: 15px;
		padding-top: 15px;
		border-top: 1px solid rgba(255, 255, 255, 0.1);
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.selection-info p {
		margin: 0;
		font-size: 0.9rem;
	}

	.help-text {
		font-size: 0.8rem;
		opacity: 0.6;
		margin-top: 5px;
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.thumbnail-grid {
			grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
			gap: 10px;
		}

		.thumbnail-image {
			height: 100px;
		}

		.browser-header {
			flex-direction: column;
			gap: 10px;
			align-items: stretch;
		}

		.selection-info {
			flex-direction: column;
			gap: 10px;
			align-items: stretch;
		}
	}
</style>
