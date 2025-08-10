<!-- ExportPreviewCard.svelte - Export preview matching desktop app -->
<script lang="ts">
	import type { SequenceData } from '$services/interfaces';

	interface Props {
		currentSequence: SequenceData | null;
		exportSettings: {
			include_start_position: boolean;
			add_beat_numbers: boolean;
			add_reversal_symbols: boolean;
			add_user_info: boolean;
			add_word: boolean;
			use_last_save_directory: boolean;
			export_format: string;
			export_quality: string;
			user_name: string;
			custom_note: string;
		};
	}

	let { currentSequence, exportSettings }: Props = $props();

	// Preview state
	let isGeneratingPreview = $state(false);
	let previewError = $state<string | null>(null);
	let previewImageUrl = $state<string | null>(null);

	// Preview info
	let previewInfo = $derived(() => {
		if (!currentSequence) return null;

		const enabledOptions = Object.entries(exportSettings).filter(
			([_key, value]) => typeof value === 'boolean' && value
		).length;

		return {
			sequenceName: currentSequence.name || 'Untitled Sequence',
			beatCount: currentSequence.beats?.length || 0,
			format: exportSettings.export_format,
			quality: exportSettings.export_quality,
			enabledOptions,
		};
	});

	// Status message
	let statusMessage = $derived(() => {
		if (isGeneratingPreview) return 'Generating preview...';
		if (previewError) return `Error: ${previewError}`;
		if (!currentSequence || !currentSequence.beats || currentSequence.beats.length === 0) {
			return 'Create a sequence to see preview';
		}
		const info = previewInfo();
		if (info) {
			return `Preview: ${info.format} • ${info.quality} • ${info.enabledOptions} options enabled`;
		}
		return 'Preview ready';
	});

	// Generate preview when sequence or settings change
	$effect(() => {
		if (currentSequence && currentSequence.beats && currentSequence.beats.length > 0) {
			generatePreview();
		} else {
			clearPreview();
		}
	});

	async function generatePreview() {
		if (!currentSequence || !currentSequence.beats || currentSequence.beats.length === 0) {
			clearPreview();
			return;
		}

		try {
			isGeneratingPreview = true;
			previewError = null;

			// Simulate preview generation (replace with actual preview service)
			await new Promise((resolve) => setTimeout(resolve, 800));

			// Create a simple preview image showing sequence info
			const canvas = createPreviewCanvas();
			previewImageUrl = canvas.toDataURL();
		} catch (error) {
			console.error('Preview generation failed:', error);
			previewError = error instanceof Error ? error.message : 'Preview generation failed';
			previewImageUrl = null;
		} finally {
			isGeneratingPreview = false;
		}
	}

	function createPreviewCanvas(): HTMLCanvasElement {
		const canvas = document.createElement('canvas');
		const ctx = canvas.getContext('2d')!;

		// Set canvas size
		canvas.width = 400;
		canvas.height = 300;

		// Background
		ctx.fillStyle = '#1a1a2e';
		ctx.fillRect(0, 0, canvas.width, canvas.height);

		// Border
		ctx.strokeStyle = '#6366f1';
		ctx.lineWidth = 2;
		ctx.strokeRect(10, 10, canvas.width - 20, canvas.height - 20);

		// Title
		ctx.fillStyle = '#ffffff';
		ctx.font = 'bold 18px Arial';
		ctx.textAlign = 'center';
		ctx.fillText('Export Preview', canvas.width / 2, 40);

		const info = previewInfo();
		if (info) {
			// Sequence info
			ctx.font = '14px Arial';
			ctx.fillText(`Sequence: ${info.sequenceName}`, canvas.width / 2, 70);
			ctx.fillText(`Beats: ${info.beatCount}`, canvas.width / 2, 95);

			// Format info
			ctx.fillStyle = '#6366f1';
			ctx.fillText(`Format: ${info.format}`, canvas.width / 2, 130);
			ctx.fillText(`Quality: ${info.quality}`, canvas.width / 2, 155);

			// Options info
			ctx.fillStyle = '#10b981';
			ctx.fillText(`${info.enabledOptions} export options enabled`, canvas.width / 2, 190);

			// Sample pictograph representation
			ctx.fillStyle = '#374151';
			ctx.fillRect(150, 210, 100, 60);
			ctx.fillStyle = '#6b7280';
			ctx.font = '12px Arial';
			ctx.fillText('Sample Beat', 200, 245);
		}

		return canvas;
	}

	function clearPreview() {
		previewImageUrl = null;
		previewError = null;
		isGeneratingPreview = false;
	}

	function handleRefreshPreview() {
		generatePreview();
	}
</script>

<div class="export-preview-card">
	<div class="preview-header">
		<h3 class="card-title">Export Preview</h3>
		<button
			class="refresh-button"
			onclick={handleRefreshPreview}
			disabled={isGeneratingPreview}
			title="Refresh preview"
		>
			<span class="refresh-icon" class:spinning={isGeneratingPreview}>🔄</span>
		</button>
	</div>

	<div class="preview-content">
		{#if isGeneratingPreview}
			<div class="preview-loading">
				<div class="loading-spinner"></div>
				<p>Generating preview...</p>
			</div>
		{:else if previewError}
			<div class="preview-error">
				<div class="error-icon">❌</div>
				<p>Preview generation failed</p>
				<span class="error-details">{previewError}</span>
			</div>
		{:else if previewImageUrl}
			<div class="preview-image-container">
				<img src={previewImageUrl} alt="Export preview" class="preview-image" />
			</div>
		{:else}
			<div class="preview-placeholder">
				<div class="placeholder-icon">📄</div>
				<p>Create a sequence to see preview</p>
				<span class="placeholder-hint"
					>Preview will update automatically when settings change</span
				>
			</div>
		{/if}
	</div>

	<div class="preview-footer">
		<div class="status-bar">
			<span class="status-text">{statusMessage}</span>
		</div>

		{#if previewInfo()}
			{@const info = previewInfo()}
			<div class="preview-details">
				<div class="detail-item">
					<span class="detail-label">Sequence:</span>
					<span class="detail-value">{info?.sequenceName}</span>
				</div>
				<div class="detail-item">
					<span class="detail-label">Beats:</span>
					<span class="detail-value">{info?.beatCount}</span>
				</div>
				<div class="detail-item">
					<span class="detail-label">Format:</span>
					<span class="detail-value">{info?.format}</span>
				</div>
			</div>
		{/if}
	</div>
</div>

<style>
	.export-preview-card {
		background: rgba(255, 255, 255, 0.08);
		border: 1px solid rgba(255, 255, 255, 0.15);
		border-radius: 12px;
		display: flex;
		flex-direction: column;
		height: 100%;
		overflow: hidden;
	}

	.preview-header {
		flex-shrink: 0;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: var(--spacing-lg);
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	}

	.card-title {
		margin: 0;
		font-size: var(--font-size-lg);
		font-weight: 600;
		color: rgba(255, 255, 255, 0.95);
	}

	.refresh-button {
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 6px;
		padding: var(--spacing-xs);
		cursor: pointer;
		transition: all var(--transition-fast);
		color: rgba(255, 255, 255, 0.8);
	}

	.refresh-button:hover:not(:disabled) {
		background: rgba(255, 255, 255, 0.15);
		color: rgba(255, 255, 255, 1);
	}

	.refresh-button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.refresh-icon {
		display: inline-block;
		transition: transform 0.3s ease;
	}

	.refresh-icon.spinning {
		animation: spin 1s linear infinite;
	}

	.preview-content {
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: var(--spacing-lg);
		min-height: 200px;
	}

	.preview-loading,
	.preview-error,
	.preview-placeholder {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--spacing-md);
		text-align: center;
		color: rgba(255, 255, 255, 0.7);
	}

	.loading-spinner {
		width: 32px;
		height: 32px;
		border: 3px solid rgba(255, 255, 255, 0.3);
		border-top: 3px solid #6366f1;
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	.error-icon,
	.placeholder-icon {
		font-size: 2rem;
		opacity: 0.7;
	}

	.error-details,
	.placeholder-hint {
		font-size: var(--font-size-xs);
		color: rgba(255, 255, 255, 0.5);
		max-width: 200px;
	}

	.preview-image-container {
		width: 100%;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.preview-image {
		max-width: 100%;
		max-height: 100%;
		border-radius: 8px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
	}

	.preview-footer {
		flex-shrink: 0;
		padding: var(--spacing-md) var(--spacing-lg);
		border-top: 1px solid rgba(255, 255, 255, 0.1);
		background: rgba(255, 255, 255, 0.02);
	}

	.status-bar {
		margin-bottom: var(--spacing-sm);
	}

	.status-text {
		font-size: var(--font-size-xs);
		color: rgba(255, 255, 255, 0.6);
	}

	.preview-details {
		display: flex;
		flex-wrap: wrap;
		gap: var(--spacing-sm);
	}

	.detail-item {
		display: flex;
		gap: var(--spacing-xs);
		font-size: var(--font-size-xs);
	}

	.detail-label {
		color: rgba(255, 255, 255, 0.5);
	}

	.detail-value {
		color: rgba(255, 255, 255, 0.8);
		font-weight: 500;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.preview-header,
		.preview-footer {
			padding: var(--spacing-md);
		}

		.preview-content {
			padding: var(--spacing-md);
			min-height: 150px;
		}

		.preview-details {
			flex-direction: column;
			gap: var(--spacing-xs);
		}
	}
</style>
