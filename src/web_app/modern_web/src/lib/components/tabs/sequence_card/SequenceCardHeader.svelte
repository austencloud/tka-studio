<!-- SequenceCardHeader.svelte - Header component matching desktop modern styling -->
<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher<{
		exportAll: void;
		refresh: void;
		regenerateImages: void;
	}>();

	interface Props {
		isExporting?: boolean;
		isRegenerating?: boolean;
		progressValue?: number;
		progressMessage?: string;
		showProgress?: boolean;
	}

	let {
		isExporting = false,
		isRegenerating = false,
		progressValue = 0,
		progressMessage = 'Select a sequence length to view cards',
		showProgress = false,
	}: Props = $props();

	// Button states
	let exportDisabled = $derived(isExporting || isRegenerating);
	let regenerateDisabled = $derived(isExporting || isRegenerating);
</script>

<div class="sequence-card-header">
	<div class="header-content">
		<!-- Title Section -->
		<div class="title-section">
			<h1 class="title">Sequence Card Manager</h1>
			<p class="description">{progressMessage}</p>
		</div>

		<!-- Progress Bar (shown when loading/processing) -->
		{#if showProgress}
			<div class="progress-container">
				<div class="progress-bar">
					<div class="progress-fill" style:width="{progressValue}%"></div>
				</div>
				<span class="progress-text">{progressValue}%</span>
			</div>
		{/if}

		<!-- Action Buttons -->
		<div class="button-group">
			<button
				class="action-btn export-btn"
				disabled={exportDisabled}
				onclick={() => dispatch('exportAll')}
				title="Export all sequence cards to files"
			>
				<span class="btn-icon">📤</span>
				Export All
			</button>

			<button
				class="action-btn refresh-btn"
				onclick={() => dispatch('refresh')}
				title="Refresh the card display"
			>
				<span class="btn-icon">🔄</span>
				Refresh
			</button>

			<button
				class="action-btn regenerate-btn"
				disabled={regenerateDisabled}
				onclick={() => dispatch('regenerateImages')}
				title="Regenerate all sequence card images"
			>
				<span class="btn-icon">🔧</span>
				Regenerate Images
			</button>
		</div>
	</div>
</div>

<style>
	.sequence-card-header {
		background: linear-gradient(to bottom, #34495e, #2c3e50);
		border-radius: 10px;
		border: 1px solid #4a5568;
		padding: 20px 24px;
	}

	.header-content {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 16px;
	}

	.title-section {
		text-align: center;
	}

	.title {
		margin: 0 0 8px 0;
		color: #ffffff;
		font-size: 24px;
		font-weight: 700;
		letter-spacing: 0.5px;
	}

	.description {
		margin: 0;
		color: #ffffff;
		font-size: 16px;
		font-style: italic;
		opacity: 0.9;
	}

	.progress-container {
		display: flex;
		align-items: center;
		gap: 12px;
		width: 100%;
		max-width: 400px;
	}

	.progress-bar {
		flex: 1;
		height: 12px;
		background: rgba(0, 0, 0, 0.15);
		border-radius: 6px;
		overflow: hidden;
		position: relative;
	}

	.progress-fill {
		height: 100%;
		background: #3498db;
		border-radius: 6px;
		transition: width 0.3s ease;
	}

	.progress-text {
		color: rgba(255, 255, 255, 0.9);
		font-size: 12px;
		font-weight: bold;
		min-width: 40px;
		text-align: center;
	}

	.button-group {
		display: flex;
		gap: 12px;
		align-items: center;
		flex-wrap: wrap;
		justify-content: center;
	}

	.action-btn {
		display: flex;
		align-items: center;
		gap: 8px;
		background: linear-gradient(to bottom, #3498db, #2980b9);
		color: white;
		border: 1px solid #5dade2;
		border-radius: 6px;
		padding: 10px 18px;
		font-weight: 600;
		font-size: 14px;
		min-width: 120px;
		justify-content: center;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.action-btn:hover:not(:disabled) {
		background: linear-gradient(to bottom, #5dade2, #3498db);
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
	}

	.action-btn:active:not(:disabled) {
		background: linear-gradient(to bottom, #2980b9, #1f618d);
		transform: translateY(0);
	}

	.action-btn:disabled {
		background: linear-gradient(to bottom, #7f8c8d, #95a5a6);
		color: #bdc3c7;
		cursor: not-allowed;
		transform: none;
		box-shadow: none;
	}

	.btn-icon {
		font-size: 16px;
	}

	/* Specific button variations */
	.export-btn:hover:not(:disabled) {
		background: linear-gradient(to bottom, #27ae60, #229954);
		border-color: #52c788;
	}

	.refresh-btn:hover:not(:disabled) {
		background: linear-gradient(to bottom, #f39c12, #e67e22);
		border-color: #f7c52d;
	}

	.regenerate-btn:hover:not(:disabled) {
		background: linear-gradient(to bottom, #8e44ad, #7d3c98);
		border-color: #a569bd;
	}

	/* Responsive Design */
	@media (max-width: 768px) {
		.sequence-card-header {
			padding: 16px 20px;
		}

		.title {
			font-size: 20px;
		}

		.description {
			font-size: 14px;
		}

		.button-group {
			gap: 8px;
		}

		.action-btn {
			min-width: 100px;
			padding: 8px 14px;
			font-size: 13px;
		}

		.progress-container {
			max-width: 300px;
		}
	}

	@media (max-width: 600px) {
		.button-group {
			flex-direction: column;
			width: 100%;
		}

		.action-btn {
			width: 100%;
			max-width: 250px;
		}
	}
</style>
