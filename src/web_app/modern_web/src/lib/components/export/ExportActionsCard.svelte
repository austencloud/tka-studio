<!-- ExportActionsCard.svelte - Export action buttons matching desktop app -->
<script lang="ts">
	import type { SequenceData } from '$services/interfaces';
	import { createEventDispatcher } from 'svelte';

	interface Props {
		currentSequence: SequenceData | null;
	}

	let { currentSequence }: Props = $props();
	const dispatch = createEventDispatcher();

	// Loading states
	let isExportingCurrent = $state(false);
	let isExportingAll = $state(false);

	// Derived state for button availability
	let canExportCurrent = $derived(() => {
		return currentSequence && currentSequence.beats && currentSequence.beats.length > 0;
	});

	// Handle export current sequence
	async function handleExportCurrent() {
		if (!canExportCurrent || isExportingCurrent) return;

		try {
			isExportingCurrent = true;
			dispatch('exportCurrent');

			// Simulate export process (replace with actual export logic)
			await new Promise((resolve) => setTimeout(resolve, 1000));
		} catch (error) {
			console.error('Export current failed:', error);
		} finally {
			isExportingCurrent = false;
		}
	}

	// Handle export all sequences
	async function handleExportAll() {
		if (isExportingAll) return;

		try {
			isExportingAll = true;
			dispatch('exportAll');

			// Simulate export process (replace with actual export logic)
			await new Promise((resolve) => setTimeout(resolve, 1500));
		} catch (error) {
			console.error('Export all failed:', error);
		} finally {
			isExportingAll = false;
		}
	}

	// Get current sequence info for display
	let sequenceInfo = $derived(() => {
		if (!currentSequence) return null;
		return {
			name: currentSequence.name || 'Untitled Sequence',
			beatCount: currentSequence.beats?.length || 0,
		};
	});
</script>

<div class="export-actions-card">
	<h3 class="card-title">Export Actions</h3>

	<!-- Current Sequence Export -->
	<div class="action-section">
		<div class="action-header">
			<h4 class="action-title">Current Sequence</h4>
			{#if sequenceInfo()}
				<div class="sequence-info">
					<span class="sequence-name">{sequenceInfo()?.name}</span>
					<span class="beat-count">{sequenceInfo()?.beatCount} beats</span>
				</div>
			{:else}
				<div class="no-sequence">
					<span class="no-sequence-text">No sequence loaded</span>
				</div>
			{/if}
		</div>

		<button
			class="export-button primary"
			class:disabled={!canExportCurrent || isExportingCurrent}
			onclick={handleExportCurrent}
			disabled={!canExportCurrent || isExportingCurrent}
		>
			{#if isExportingCurrent}
				<span class="loading-spinner"></span>
				Exporting...
			{:else if !canExportCurrent}
				🔤 No Sequence to Export
			{:else}
				🔤 Export Current Sequence
			{/if}
		</button>
	</div>

	<!-- All Sequences Export -->
	<div class="action-section">
		<div class="action-header">
			<h4 class="action-title">All Sequences</h4>
			<div class="all-sequences-info">
				<span class="info-text">Export all sequences in your library</span>
			</div>
		</div>

		<button
			class="export-button secondary"
			class:disabled={isExportingAll}
			onclick={handleExportAll}
			disabled={isExportingAll}
		>
			{#if isExportingAll}
				<span class="loading-spinner"></span>
				Exporting All...
			{:else}
				📚 Export All Sequences
			{/if}
		</button>
	</div>

	<!-- Export Tips (collapsed by default to keep actions visible) -->
	<details class="tips">
		<summary class="tips-summary" aria-label="Toggle export tips">💡 Export Tips</summary>
		<ul class="tips-list">
			<li>PNG format is best for sharing online</li>
			<li>PDF format preserves vector quality</li>
			<li>300 DPI is recommended for printing</li>
			<li>Include beat numbers for reference</li>
		</ul>
	</details>
</div>

<style>
	.export-actions-card {
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 8px;
		padding: var(--spacing-sm);
		display: flex;
		flex-direction: column;
		gap: var(--spacing-sm);
		position: sticky;
		top: 0;
		z-index: 1;
	}

	.card-title {
		margin: 0;
		font-size: var(--font-size-md);
		font-weight: 600;
		color: rgba(255, 255, 255, 0.95);
	}

	.action-section {
		display: flex;
		flex-direction: column;
		gap: var(--spacing-xs);
	}

	.action-header {
		display: flex;
		flex-direction: column;
		gap: 2px;
	}

	.action-title {
		margin: 0;
		font-size: var(--font-size-sm);
		font-weight: 600;
		color: rgba(255, 255, 255, 0.9);
	}

	.sequence-info {
		display: flex;
		align-items: center;
		gap: var(--spacing-xs);
		flex-wrap: wrap;
	}

	.sequence-name {
		font-size: var(--font-size-xs);
		color: rgba(255, 255, 255, 0.8);
		font-weight: 500;
	}

	.beat-count {
		font-size: var(--font-size-xs);
		color: rgba(255, 255, 255, 0.6);
		padding: 1px 4px;
		background: rgba(99, 102, 241, 0.3);
		border-radius: 8px;
		white-space: nowrap;
	}

	.no-sequence {
		display: flex;
		align-items: center;
	}

	.no-sequence-text {
		font-size: var(--font-size-xs);
		color: rgba(255, 255, 255, 0.5);
		font-style: italic;
	}

	.all-sequences-info {
		display: flex;
		align-items: center;
	}

	.info-text {
		font-size: var(--font-size-xs);
		color: rgba(255, 255, 255, 0.7);
	}

	.export-button {
		padding: var(--spacing-xs) var(--spacing-sm);
		border-radius: 6px;
		font-size: var(--font-size-xs);
		font-weight: 600;
		cursor: pointer;
		transition: all var(--transition-fast);
		border: 1px solid transparent;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: var(--spacing-xs);
		min-height: 32px;
	}

	.export-button.primary {
		background: linear-gradient(135deg, #6366f1 0%, #5855eb 100%);
		color: white;
		border-color: rgba(255, 255, 255, 0.2);
		box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
	}

	.export-button.primary:hover:not(.disabled) {
		background: linear-gradient(135deg, #5855eb 0%, #4f46e5 100%);
		transform: translateY(-1px);
		box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
	}

	.export-button.secondary {
		background: rgba(255, 255, 255, 0.08);
		color: rgba(255, 255, 255, 0.9);
		border-color: rgba(255, 255, 255, 0.2);
	}

	.export-button.secondary:hover:not(.disabled) {
		background: rgba(255, 255, 255, 0.12);
		border-color: rgba(255, 255, 255, 0.3);
		transform: translateY(-1px);
	}

	.export-button.disabled {
		opacity: 0.5;
		cursor: not-allowed;
		transform: none !important;
		box-shadow: none !important;
	}

	.loading-spinner {
		width: 12px;
		height: 12px;
		border: 2px solid rgba(255, 255, 255, 0.3);
		border-top: 2px solid currentColor;
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	/* Collapsible tips */
	.tips {
		margin-top: var(--spacing-xs);
	}

	.tips-summary {
		cursor: pointer;
		font-size: var(--font-size-xs);
		color: rgba(255, 255, 255, 0.7);
		padding: 2px 0;
		list-style: none;
	}

	.tips-summary::-webkit-details-marker {
		display: none;
	}

	.tips-list {
		margin: var(--spacing-xs) 0 0 0;
		padding-left: var(--spacing-md);
		list-style: none;
		position: relative;
	}

	.tips-list li {
		font-size: var(--font-size-xs);
		color: rgba(255, 255, 255, 0.6);
		line-height: 1.2;
		margin-bottom: 2px;
		position: relative;
	}

	.tips-list li::before {
		content: '•';
		color: #6366f1;
		position: absolute;
		left: -var(--spacing-sm);
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
		.export-actions-card {
			padding: var(--spacing-md);
		}

		.export-button {
			padding: var(--spacing-sm) var(--spacing-md);
			font-size: var(--font-size-xs);
		}
	}
</style>
