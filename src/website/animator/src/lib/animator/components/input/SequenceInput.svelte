<script lang="ts">
	import type { SequenceData } from '../../types/core.js';
	import FileDropZone from './FileDropZone.svelte';
	import FilePicker from './FilePicker.svelte';
	import JSONInput from './JSONInput.svelte';

	// Props
	let {
		onSequenceLoaded
	}: {
		onSequenceLoaded?: (_data: SequenceData) => void;
	} = $props();

	// State
	let errorMessage = $state('');
	let jsonValue = $state('');
	let isProcessing = $state(false);

	function handleSequenceLoaded(data: SequenceData): void {
		onSequenceLoaded?.(data);
		errorMessage = '';
		jsonValue = JSON.stringify(data, null, 2);
	}

	function handleError(error: string): void {
		errorMessage = error;
	}

	function clearInput(): void {
		jsonValue = '';
		errorMessage = '';
	}
</script>

<div class="sequence-input">
	<!-- Input method selection -->
	<div class="input-options">
		<FilePicker onSequenceLoaded={handleSequenceLoaded} onError={handleError} {isProcessing} />
		<div class="separator">or</div>
		<button
			type="button"
			class="json-button"
			onclick={clearInput}
			disabled={isProcessing}
			aria-label="Clear input and paste JSON data"
		>
			📝 Paste JSON Data
		</button>
	</div>

	<!-- Drag and drop area with JSON input -->
	<FileDropZone
		onSequenceLoaded={handleSequenceLoaded}
		onError={handleError}
		disabled={isProcessing}
		bind:isProcessing
	>
		<div class="input-container">
			<JSONInput
				bind:value={jsonValue}
				onSequenceLoaded={handleSequenceLoaded}
				onError={handleError}
				disabled={isProcessing}
			/>

			{#if errorMessage}
				<div class="error" role="alert" aria-live="polite">{errorMessage}</div>
			{/if}

			{#if !jsonValue.trim() && !isProcessing}
				<div class="help-text">
					<p><strong>💡 How to use:</strong></p>
					<ul>
						<li>
							<strong>PNG Import:</strong> Click "Load from PNG Image" or drag & drop PNG files with
							embedded metadata (created by the Python pictograph tools)
						</li>
						<li>
							<strong>JSON Input:</strong> Paste sequence data in the format:
							<code>[metadata, step1, step2, ...]</code>
						</li>
						<li>
							<strong>Drag & Drop:</strong> Simply drag PNG image files onto this area for quick import
						</li>
					</ul>
				</div>
			{/if}

			{#if isProcessing}
				<div class="loading-indicator" role="status" aria-live="polite">
					<div class="spinner" aria-hidden="true"></div>
					<span>Processing PNG file...</span>
				</div>
			{/if}
		</div>
	</FileDropZone>
</div>

<style>
	.sequence-input {
		height: 100%;
		display: flex;
		flex-direction: column;
		padding: 1rem;
	}

	.input-options {
		display: flex;
		flex-direction: column;
		align-items: stretch;
		gap: 0.75rem;
		margin-bottom: 1rem;
		flex-shrink: 0;
	}

	.separator {
		color: var(--color-text-secondary);
		font-style: italic;
		font-size: 0.9rem;
		text-align: center;
		padding: 0.5rem 0;
	}

	.json-button {
		padding: 0.75rem 1.5rem;
		border: 2px solid var(--color-primary);
		border-radius: 8px;
		cursor: pointer;
		font-weight: 500;
		transition: all 0.2s ease;
		font-size: 0.9rem;
		background: transparent;
		color: var(--color-primary);
	}

	.json-button:hover:not(:disabled) {
		background: var(--color-primary-alpha);
		transform: translateY(-1px);
	}

	.json-button:disabled {
		opacity: 0.6;
		cursor: not-allowed;
		transform: none !important;
	}

	.input-container {
		padding: 1rem;
	}

	.error {
		color: var(--color-error);
		font-size: 0.875rem;
		margin-top: 0.5rem;
		padding: 0.75rem;
		background: var(--color-surface);
		border-radius: 8px;
		border-left: 4px solid var(--color-error);
		white-space: pre-line;
		line-height: 1.5;
		max-height: 200px;
		overflow-y: auto;
		transition: all 0.3s ease;
	}

	.loading-indicator {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.75rem;
		margin-top: 1rem;
		padding: 1rem;
		background: var(--color-surface);
		border-radius: 8px;
		border-left: 4px solid var(--color-warning);
		color: var(--color-warning);
		font-weight: 500;
		transition: all 0.3s ease;
	}

	.spinner {
		width: 20px;
		height: 20px;
		border: 2px solid var(--color-border);
		border-top: 2px solid var(--color-warning);
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

	.help-text {
		margin-top: 1rem;
		padding: 1rem;
		background: var(--color-surface);
		border-radius: 8px;
		border-left: 4px solid var(--color-primary);
		font-size: 0.875rem;
		line-height: 1.5;
		transition: all 0.3s ease;
	}

	.help-text p {
		margin: 0 0 0.5rem 0;
		color: var(--color-primary);
	}

	.help-text ul {
		margin: 0;
		padding-left: 1.5rem;
	}

	.help-text li {
		margin-bottom: 0.5rem;
		color: var(--color-text-secondary);
	}

	.help-text code {
		background: var(--color-primary-alpha);
		padding: 0.2rem 0.4rem;
		border-radius: 3px;
		font-family: monospace;
		font-size: 0.8rem;
		color: var(--color-primary);
	}
</style>
