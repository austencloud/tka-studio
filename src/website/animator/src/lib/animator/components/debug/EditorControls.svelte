<script lang="ts">
	// Props
	let {
		editMode = 'view',
		onStartEdit = () => {},
		onSaveEdit = () => {},
		onCancelEdit = () => {},
		onResetToOriginal = () => {},
		onToggleCompare = () => {}
	}: {
		editMode?: 'view' | 'edit' | 'compare';
		onStartEdit?: () => void;
		onSaveEdit?: () => void;
		onCancelEdit?: () => void;
		onResetToOriginal?: () => void;
		onToggleCompare?: () => void;
	} = $props();
</script>

<div class="editor-controls">
	<div class="control-buttons">
		{#if editMode === 'view'}
			<button class="control-button edit" onclick={onStartEdit}> ✏️ Edit </button>
		{:else if editMode === 'edit'}
			<button class="control-button save" onclick={onSaveEdit}> 💾 Save </button>
			<button class="control-button cancel" onclick={onCancelEdit}> ❌ Cancel </button>
			<button class="control-button reset" onclick={onResetToOriginal}> 🔄 Reset </button>
		{/if}

		<button
			class="control-button compare"
			class:active={editMode === 'compare'}
			onclick={onToggleCompare}
		>
			🔍 Compare
		</button>
	</div>

	<div class="mode-indicator">
		<span class="mode-label">Mode:</span>
		<span class="mode-value {editMode}">{editMode.toUpperCase()}</span>
	</div>
</div>

<style>
	.editor-controls {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1rem;
		background: var(--color-surface-elevated);
		border-radius: 8px;
		border: 1px solid var(--color-border);
	}

	.control-buttons {
		display: flex;
		gap: 0.5rem;
	}

	.control-button {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 6px;
		padding: 0.5rem 1rem;
		cursor: pointer;
		transition: all 0.2s ease;
		font-size: 0.875rem;
		color: var(--color-text);
	}

	.control-button:hover {
		background: var(--color-surface-hover);
	}

	.control-button.save {
		background: #10b981;
		color: white;
		border-color: #10b981;
	}

	.control-button.cancel {
		background: #ef4444;
		color: white;
		border-color: #ef4444;
	}

	.control-button.active {
		background: var(--color-primary);
		color: white;
		border-color: var(--color-primary);
	}

	.mode-indicator {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		font-size: 0.875rem;
	}

	.mode-label {
		color: var(--color-text-secondary);
		font-weight: 500;
	}

	.mode-value {
		font-weight: 600;
		padding: 0.25rem 0.5rem;
		border-radius: 4px;
		font-size: 0.75rem;
	}

	.mode-value.view {
		background: #10b981;
		color: white;
	}

	.mode-value.edit {
		background: #f59e0b;
		color: white;
	}

	.mode-value.compare {
		background: #3b82f6;
		color: white;
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.editor-controls {
			flex-direction: column;
			gap: 1rem;
		}
	}
</style>
