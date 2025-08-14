<!-- SequenceCardHeader.svelte - Header component matching desktop modern styling -->
<script lang="ts">
	interface Props {
		isExporting?: boolean;
		isRegenerating?: boolean;
		progressValue?: number;
		progressMessage?: string;
		showProgress?: boolean;
		onexportall?: () => void;
		onrefresh?: () => void;
		onregenerateimages?: () => void;
	}

	let {
		isExporting = false,
		isRegenerating = false,
		progressValue = 0,
		progressMessage = 'Select a sequence length to view cards',
		showProgress = false,
		onexportall,
		onrefresh,
		onregenerateimages
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
				onclick={() => onexportall?.()}
				title="Export all sequence cards to files"
			>
				<span class="btn-icon">📤</span>
				Export All
			</button>

			<button
				class="action-btn refresh-btn"
				onclick={() => onrefresh?.()}
				title="Refresh the card display"
			>
				<span class="btn-icon">🔄</span>
				Refresh
			</button>

			<button
				class="action-btn regenerate-btn"
				disabled={regenerateDisabled}
				onclick={() => onregenerateimages?.()}
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
	background: var(--surface-glass);
	backdrop-filter: var(--glass-backdrop-strong);
	border-radius: 16px;
	border: var(--glass-border);
	box-shadow: var(--shadow-glass);
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
	color: rgba(255, 255, 255, 0.95);
	text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
	font-size: 24px;
	font-weight: 700;
	letter-spacing: 0.5px;
}

	.description {
	margin: 0;
	color: rgba(255, 255, 255, 0.8);
	text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
	font-size: 16px;
	font-style: italic;
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
	background: rgba(0, 0, 0, 0.3);
	border-radius: 8px;
	overflow: hidden;
	position: relative;
	box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
}

	.progress-fill {
	height: 100%;
	background: var(--gradient-primary);
	border-radius: 8px;
	transition: width var(--transition-normal);
	box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

	.progress-text {
	color: rgba(255, 255, 255, 0.9);
	text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
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
	background: var(--surface-glass);
	backdrop-filter: var(--glass-backdrop);
	color: rgba(255, 255, 255, 0.95);
	border: var(--glass-border);
	border-radius: 10px;
	padding: 10px 18px;
	font-weight: 600;
	font-size: 14px;
	min-width: 120px;
	justify-content: center;
	cursor: pointer;
	transition: all var(--transition-normal);
	box-shadow: var(--shadow-glass);
}

	.action-btn:hover:not(:disabled) {
	background: var(--surface-hover);
	border: var(--glass-border-hover);
	transform: translateY(-2px);
	box-shadow: var(--shadow-glass-hover);
}

	.action-btn:active:not(:disabled) {
	background: var(--surface-active);
	transform: translateY(-1px);
}

	.action-btn:disabled {
	background: rgba(255, 255, 255, 0.02);
	color: rgba(255, 255, 255, 0.3);
	border: 1px solid rgba(255, 255, 255, 0.05);
	cursor: not-allowed;
	transform: none;
	box-shadow: none;
}

	.btn-icon {
		font-size: 16px;
	}

	/* Specific button variations with glassmorphism */
.export-btn:hover:not(:disabled) {
	background: rgba(39, 174, 96, 0.2);
	border-color: rgba(82, 199, 136, 0.4);
	box-shadow: 0 4px 16px rgba(39, 174, 96, 0.3);
}

.refresh-btn:hover:not(:disabled) {
	background: rgba(243, 156, 18, 0.2);
	border-color: rgba(247, 197, 45, 0.4);
	box-shadow: 0 4px 16px rgba(243, 156, 18, 0.3);
}

.regenerate-btn:hover:not(:disabled) {
	background: rgba(142, 68, 173, 0.2);
	border-color: rgba(165, 105, 189, 0.4);
	box-shadow: 0 4px 16px rgba(142, 68, 173, 0.3);
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
