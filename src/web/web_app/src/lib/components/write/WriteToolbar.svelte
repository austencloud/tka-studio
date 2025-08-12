<!-- WriteToolbar.svelte - Top toolbar with file operations -->
<script lang="ts">
	// Props
	interface Props {
		hasUnsavedChanges?: boolean;
		disabled?: boolean;
		onNewActRequested?: () => void;
		onSaveRequested?: () => void;
		onSaveAsRequested?: () => void;
	}

	let {
		hasUnsavedChanges = false,
		disabled = false,
		onNewActRequested,
		onSaveRequested,
		onSaveAsRequested,
	}: Props = $props();

	// Handle toolbar actions
	function handleNewAct() {
		if (disabled) return;
		onNewActRequested?.();
	}

	function handleSave() {
		if (disabled) return;
		onSaveRequested?.();
	}

	function handleSaveAs() {
		if (disabled) return;
		onSaveAsRequested?.();
	}
</script>

<div class="write-toolbar" class:disabled>
	<!-- File operations -->
	<div class="toolbar-section file-operations">
		<button
			class="toolbar-button new-button btn-primary"
			{disabled}
			onclick={handleNewAct}
			title="Create new act"
		>
			📄 New Act
		</button>

		<button
			class="toolbar-button save-button btn-glass"
			class:has-changes={hasUnsavedChanges}
			{disabled}
			onclick={handleSave}
			title="Save current act"
		>
			💾 Save
			{#if hasUnsavedChanges}
				<span class="unsaved-indicator">●</span>
			{/if}
		</button>

		<button
			class="toolbar-button save-as-button btn-glass"
			{disabled}
			onclick={handleSaveAs}
			title="Save act with new name"
		>
			💾 Save As...
		</button>
	</div>

	<!-- Spacer -->
	<div class="toolbar-spacer"></div>

	<!-- Status section -->
	<div class="toolbar-section status-section">
		{#if hasUnsavedChanges}
			<span class="status-text unsaved"> ● Unsaved changes </span>
		{:else}
			<span class="status-text saved"> ✓ Saved </span>
		{/if}
	</div>
</div>

<style>
	.write-toolbar {
		display: flex;
		align-items: center;
		gap: var(--spacing-md);
		padding: var(--spacing-sm) var(--spacing-md);
		background: rgba(40, 40, 50, 0.9);
		border: 1px solid rgba(80, 80, 100, 0.4);
		border-radius: 8px;
		backdrop-filter: var(--glass-backdrop);
		min-height: 48px;
		transition: all var(--transition-normal);
	}

	.write-toolbar.disabled {
		opacity: 0.6;
		pointer-events: none;
	}

	.toolbar-section {
		display: flex;
		align-items: center;
		gap: var(--spacing-sm);
	}

	.file-operations {
		flex-shrink: 0;
	}

	.toolbar-spacer {
		flex: 1;
	}

	.status-section {
		flex-shrink: 0;
	}

	.toolbar-button {
		padding: var(--spacing-xs) var(--spacing-md);
		border-radius: 6px;
		font-size: var(--font-size-sm);
		font-weight: 500;
		font-family: 'Segoe UI', sans-serif;
		transition: all var(--transition-normal);
		white-space: nowrap;
		display: flex;
		align-items: center;
		gap: var(--spacing-xs);
		position: relative;
	}

	.toolbar-button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
		transform: none;
	}

	.new-button {
		background: rgba(70, 130, 180, 0.8);
		border: 1px solid rgba(100, 150, 200, 0.6);
		color: white;
	}

	.new-button:hover:not(:disabled) {
		background: rgba(80, 140, 190, 0.9);
		transform: translateY(-1px);
	}

	.save-button,
	.save-as-button {
		background: rgba(60, 60, 70, 0.8);
		border: 1px solid rgba(100, 100, 120, 0.4);
		color: rgba(255, 255, 255, 0.9);
	}

	.save-button:hover:not(:disabled),
	.save-as-button:hover:not(:disabled) {
		background: rgba(70, 70, 80, 0.9);
		border-color: rgba(120, 120, 140, 0.6);
		transform: translateY(-1px);
	}

	.save-button.has-changes {
		background: rgba(100, 150, 100, 0.8);
		border-color: rgba(120, 170, 120, 0.6);
		color: white;
	}

	.save-button.has-changes:hover:not(:disabled) {
		background: rgba(110, 160, 110, 0.9);
	}

	.unsaved-indicator {
		color: rgba(255, 200, 100, 0.9);
		font-weight: bold;
		font-size: var(--font-size-lg);
		line-height: 1;
		animation: pulse 2s infinite;
	}

	@keyframes pulse {
		0%,
		100% {
			opacity: 1;
		}
		50% {
			opacity: 0.5;
		}
	}

	.status-text {
		font-size: var(--font-size-sm);
		font-weight: 500;
		font-family: 'Segoe UI', sans-serif;
	}

	.status-text.saved {
		color: rgba(100, 200, 100, 0.9);
	}

	.status-text.unsaved {
		color: rgba(255, 200, 100, 0.9);
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.write-toolbar {
			padding: var(--spacing-xs) var(--spacing-sm);
			gap: var(--spacing-sm);
			min-height: 40px;
		}

		.toolbar-section {
			gap: var(--spacing-xs);
		}

		.toolbar-button {
			padding: var(--spacing-xs) var(--spacing-sm);
			font-size: var(--font-size-xs);
		}

		.status-text {
			font-size: var(--font-size-xs);
		}

		.unsaved-indicator {
			font-size: var(--font-size-base);
		}
	}

	@media (max-width: 480px) {
		.write-toolbar {
			flex-direction: column;
			align-items: stretch;
			gap: var(--spacing-xs);
			padding: var(--spacing-xs);
		}

		.toolbar-section {
			justify-content: center;
		}

		.toolbar-spacer {
			display: none;
		}

		.file-operations {
			order: 1;
		}

		.status-section {
			order: 0;
		}

		.toolbar-button {
			flex: 1;
			justify-content: center;
			min-width: 0;
		}
	}

	/* Focus styles for accessibility */
	.toolbar-button:focus-visible {
		outline: 2px solid rgba(255, 255, 255, 0.6);
		outline-offset: 2px;
	}
</style>
