<script lang="ts">
	import type { SequenceData } from '../../types/core.js';
	import { validateJSONInput } from '../../utils/validation/sequence-validator.js';
	import X from 'lucide-svelte/icons/x';
	import Upload from 'lucide-svelte/icons/upload';

	// Props
	let {
		isOpen = false,
		onClose,
		onImport
	}: {
		isOpen: boolean;
		onClose?: () => void;
		onImport?: (_data: SequenceData) => void;
	} = $props();

	// State
	let jsonInput = $state('');
	let errorMessage = $state('');
	let isProcessing = $state(false);

	// Clear state when modal opens/closes
	$effect(() => {
		if (isOpen) {
			jsonInput = '';
			errorMessage = '';
			isProcessing = false;
		}
	});

	function handleClose(): void {
		onClose?.();
	}

	function handleBackdropClick(event: MouseEvent): void {
		if (event.target === event.currentTarget) {
			handleClose();
		}
	}

	function handleKeyDown(event: KeyboardEvent): void {
		if (event.key === 'Escape') {
			handleClose();
		}
	}

	function handleInputChange(event: Event): void {
		const target = event.target as HTMLTextAreaElement;
		jsonInput = target.value;
		errorMessage = ''; // Clear errors on input change
	}

	async function handleImport(): Promise<void> {
		if (isProcessing) return;

		isProcessing = true;
		errorMessage = '';

		try {
			const validation = validateJSONInput(jsonInput);

			if (!validation.isValid) {
				errorMessage = validation.error || 'Invalid JSON input';
				return;
			}

			const parsed = JSON.parse(jsonInput);
			onImport?.(parsed as SequenceData);
			handleClose();
		} catch (err) {
			errorMessage = `Parse error: ${err instanceof Error ? err.message : String(err)}`;
		} finally {
			isProcessing = false;
		}
	}

	function handlePasteExample(): void {
		jsonInput = `[
  {
    "word": "Example",
    "author": "Demo User",
    "level": 1,
    "prop_type": "staff",
    "grid_mode": "diamond"
  },
  {
    "beat": 1,
    "letter": "A",
    "blue_attributes": {
      "start_loc": "alpha",
      "end_loc": "beta",
      "start_ori": "in",
      "end_ori": "out",
      "prop_rot_dir": "cw",
      "turns": 1,
      "motion_type": "pro"
    },
    "red_attributes": {
      "start_loc": "gamma",
      "end_loc": "delta",
      "start_ori": "in",
      "end_ori": "out",
      "prop_rot_dir": "ccw",
      "turns": 1,
      "motion_type": "pro"
    }
  }
]`;
		errorMessage = '';
	}
</script>

{#if isOpen}
	<!-- Modal backdrop -->
	<div
		class="modal-backdrop"
		onclick={handleBackdropClick}
		onkeydown={handleKeyDown}
		role="dialog"
		aria-modal="true"
		aria-labelledby="modal-title"
		tabindex="-1"
	>
		<!-- Modal content -->
		<div class="modal-content">
			<!-- Header -->
			<div class="modal-header">
				<h2 id="modal-title">Import JSON Sequence</h2>
				<button
					type="button"
					class="close-button"
					onclick={handleClose}
					aria-label="Close modal"
					title="Close"
				>
					<X size={20} />
				</button>
			</div>

			<!-- Body -->
			<div class="modal-body">
				<div class="input-section">
					<label for="json-textarea" class="input-label">
						Paste your sequence JSON data below:
					</label>
					<textarea
						id="json-textarea"
						class="json-textarea"
						value={jsonInput}
						oninput={handleInputChange}
						placeholder="Paste JSON sequence data here...
Example format: [metadata, step1, step2, ...]"
						rows="12"
						disabled={isProcessing}
					></textarea>

					{#if errorMessage}
						<div class="error-message" role="alert" aria-live="polite">
							{errorMessage}
						</div>
					{/if}

					<div class="help-section">
						<p class="help-text">
							<strong>Expected format:</strong> An array starting with metadata object, followed by sequence
							steps.
						</p>
						<button
							type="button"
							class="example-button"
							onclick={handlePasteExample}
							disabled={isProcessing}
						>
							📝 Paste Example
						</button>
					</div>
				</div>
			</div>

			<!-- Footer -->
			<div class="modal-footer">
				<button type="button" class="cancel-button" onclick={handleClose} disabled={isProcessing}>
					Cancel
				</button>
				<button
					type="button"
					class="import-button"
					onclick={handleImport}
					disabled={isProcessing || !jsonInput.trim()}
				>
					{#if isProcessing}
						<div class="spinner" aria-hidden="true"></div>
						Processing...
					{:else}
						<Upload size={16} />
						Import & Animate
					{/if}
				</button>
			</div>
		</div>
	</div>
{/if}

<style>
	.modal-backdrop {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(0, 0, 0, 0.5);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
		padding: 1rem;
		backdrop-filter: blur(2px);
	}

	.modal-content {
		background: var(--color-surface);
		border-radius: 12px;
		box-shadow:
			0 20px 25px -5px rgba(0, 0, 0, 0.1),
			0 10px 10px -5px rgba(0, 0, 0, 0.04);
		max-width: 600px;
		width: 100%;
		max-height: 90vh;
		display: flex;
		flex-direction: column;
		border: 1px solid var(--color-border);
	}

	.modal-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1.5rem 1.5rem 1rem;
		border-bottom: 1px solid var(--color-border);
		flex-shrink: 0;
	}

	.modal-header h2 {
		margin: 0;
		font-size: 1.25rem;
		font-weight: 600;
		color: var(--color-text-primary);
	}

	.close-button {
		background: none;
		border: none;
		color: var(--color-text-secondary);
		cursor: pointer;
		padding: 0.5rem;
		border-radius: 6px;
		transition: all 0.2s ease;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.close-button:hover {
		background: var(--color-background);
		color: var(--color-text-primary);
	}

	.modal-body {
		flex: 1;
		overflow-y: auto;
		padding: 1.5rem;
	}

	.input-section {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.input-label {
		font-weight: 500;
		color: var(--color-text-primary);
		font-size: 0.875rem;
	}

	.json-textarea {
		width: 100%;
		min-height: 300px;
		padding: 1rem;
		border: 1px solid var(--color-border);
		border-radius: 8px;
		font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
		font-size: 0.875rem;
		line-height: 1.5;
		background: var(--color-background);
		color: var(--color-text-primary);
		resize: vertical;
		transition: border-color 0.2s ease;
	}

	.json-textarea:focus {
		outline: none;
		border-color: var(--color-primary);
		box-shadow: 0 0 0 3px rgba(var(--color-primary-rgb), 0.1);
	}

	.json-textarea:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.error-message {
		color: var(--color-error);
		font-size: 0.875rem;
		padding: 0.75rem;
		background: var(--color-error-bg);
		border: 1px solid var(--color-error);
		border-radius: 6px;
	}

	.help-section {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 1rem;
		padding: 1rem;
		background: var(--color-background);
		border-radius: 8px;
		border: 1px solid var(--color-border);
	}

	.help-text {
		margin: 0;
		font-size: 0.875rem;
		color: var(--color-text-secondary);
		flex: 1;
	}

	.example-button {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		color: var(--color-text-primary);
		padding: 0.5rem 1rem;
		border-radius: 6px;
		cursor: pointer;
		font-size: 0.875rem;
		transition: all 0.2s ease;
		flex-shrink: 0;
	}

	.example-button:hover:not(:disabled) {
		background: var(--color-background);
		border-color: var(--color-primary);
	}

	.example-button:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.modal-footer {
		display: flex;
		justify-content: flex-end;
		gap: 0.75rem;
		padding: 1rem 1.5rem 1.5rem;
		border-top: 1px solid var(--color-border);
		flex-shrink: 0;
	}

	.cancel-button {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		color: var(--color-text-primary);
		padding: 0.75rem 1.5rem;
		border-radius: 8px;
		cursor: pointer;
		font-weight: 500;
		transition: all 0.2s ease;
	}

	.cancel-button:hover:not(:disabled) {
		background: var(--color-background);
	}

	.cancel-button:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.import-button {
		background: var(--color-primary);
		border: 1px solid var(--color-primary);
		color: white;
		padding: 0.75rem 1.5rem;
		border-radius: 8px;
		cursor: pointer;
		font-weight: 500;
		transition: all 0.2s ease;
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.import-button:hover:not(:disabled) {
		background: var(--color-primary-hover);
		border-color: var(--color-primary-hover);
	}

	.import-button:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.spinner {
		width: 16px;
		height: 16px;
		border: 2px solid transparent;
		border-top: 2px solid currentColor;
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	/* Mobile responsive */
	@media (max-width: 768px) {
		.modal-backdrop {
			padding: 0.5rem;
		}

		.modal-content {
			max-height: 95vh;
		}

		.modal-header,
		.modal-body,
		.modal-footer {
			padding-left: 1rem;
			padding-right: 1rem;
		}

		.json-textarea {
			min-height: 250px;
		}

		.help-section {
			flex-direction: column;
			align-items: flex-start;
			gap: 0.75rem;
		}

		.modal-footer {
			flex-direction: column-reverse;
		}

		.cancel-button,
		.import-button {
			width: 100%;
			justify-content: center;
		}
	}
</style>
