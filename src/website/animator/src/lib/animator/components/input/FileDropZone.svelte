<script lang="ts">
	import type { SequenceData } from '../../types/core.js';
	import { extractSequenceFromPNG } from '../../utils/file/png-parser.js';
	import { AnimatorErrorHandler } from '../../utils/error/error-handler.js';
	import { InputValidator } from '../../utils/validation/input-validator.js';

	// Props
	let {
		onSequenceLoaded,
		onError,
		disabled = false,
		children,
		isProcessing = $bindable(false)
	}: {
		onSequenceLoaded?: (_data: SequenceData) => void;
		onError?: (_error: string) => void;
		disabled?: boolean;
		children?: import('svelte').Snippet;
		isProcessing?: boolean;
	} = $props();

	// State
	let isDragOver = $state(false);
	let dragCounter = $state(0);

	// Drag and drop handlers
	function handleDragEnter(e: DragEvent): void {
		e.preventDefault();
		e.stopPropagation();
		dragCounter++;
		if (e.dataTransfer?.types.includes('Files')) {
			isDragOver = true;
		}
	}

	function handleDragLeave(e: DragEvent): void {
		e.preventDefault();
		e.stopPropagation();
		dragCounter--;
		if (dragCounter === 0) {
			isDragOver = false;
		}
	}

	function handleDragOver(e: DragEvent): void {
		e.preventDefault();
		e.stopPropagation();
		if (e.dataTransfer) {
			e.dataTransfer.dropEffect = 'copy';
		}
	}

	async function handleDrop(e: DragEvent): Promise<void> {
		e.preventDefault();
		e.stopPropagation();
		isDragOver = false;
		dragCounter = 0;

		const files = e.dataTransfer?.files;
		if (!files || files.length === 0) return;

		// Process only the first PNG file
		const pngFile = Array.from(files).find(
			(file) => file.type.includes('png') || file.name.toLowerCase().endsWith('.png')
		);

		if (pngFile) {
			await processFile(pngFile);
		} else {
			onError?.(
				'Please drop a PNG image file. Only PNG files with embedded sequence metadata are supported.'
			);
		}
	}

	async function processFile(file: File): Promise<void> {
		// Validate file type
		const validation = InputValidator.validateFileType(file);
		if (!validation.isValid) {
			onError?.(validation.errors.join(', '));
			return;
		}

		// Log warnings if any
		if (validation.warnings.length > 0) {
			console.info('File warnings:', validation.warnings.join(', '));
		}

		isProcessing = true;

		try {
			const result = await extractSequenceFromPNG(file);
			if (result.success && result.data) {
				onSequenceLoaded?.(result.data);
			} else {
				onError?.(createNoMetadataErrorMessage(file.name));
			}
		} catch (err) {
			const error = AnimatorErrorHandler.handleFileError(
				err instanceof Error ? err : new Error(String(err))
			);
			onError?.(AnimatorErrorHandler.formatForUser(error));
		} finally {
			isProcessing = false;
		}
	}

	function createNoMetadataErrorMessage(fileName: string): string {
		return `No sequence metadata found in "${fileName}".

Expected: PNG files created by the Python pictograph tools with embedded sequence metadata.

The PNG file should contain a "metadata" text chunk with JSON data in this format:
{
  "sequence": [
    { "word": "...", "author": "...", ... },  // metadata
    { "beat": 1, "blue_attributes": {...}, "red_attributes": {...} },  // steps
    ...
  ]
}

To create compatible PNG files:
• Use the Python pictograph application to generate sequences
• Export sequences as PNG images (they automatically embed the metadata)
• Or manually add metadata to PNG files using the Python MetaDataExtractor class`;
	}

	// Expose processing state for parent components
	export { isProcessing };
</script>

<div
	class="drop-zone"
	class:disabled
	class:processing={isProcessing}
	class:drag-over={isDragOver}
	role="button"
	tabindex="0"
	aria-label="Drag and drop area for PNG files"
	ondragenter={handleDragEnter}
	ondragleave={handleDragLeave}
	ondragover={handleDragOver}
	ondrop={handleDrop}
>
	{#if isDragOver}
		<div class="drop-overlay">
			<div class="drop-message">📁 Drop PNG image here to import sequence data</div>
		</div>
	{/if}

	{@render children?.()}
</div>

<style>
	.drop-zone {
		position: relative;
		border: 2px dashed var(--color-border);
		border-radius: 12px;
		transition: all 0.3s ease;
		background: var(--color-background);
	}

	.drop-zone.drag-over {
		border-color: var(--color-primary);
		background: var(--color-primary-alpha);
		transform: scale(1.02);
	}

	.drop-zone.processing {
		border-color: var(--color-warning);
		background: var(--color-surface);
	}

	.drop-zone.disabled {
		opacity: 0.6;
		pointer-events: none;
	}

	.drop-overlay {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: var(--color-primary-alpha);
		border-radius: 10px;
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 10;
		backdrop-filter: blur(2px);
	}

	.drop-message {
		background: var(--color-primary);
		color: white;
		padding: 1rem 2rem;
		border-radius: 8px;
		font-weight: 600;
		font-size: 1.1rem;
		box-shadow: 0 4px 12px var(--color-primary-alpha);
		animation: bounce 0.6s ease-in-out infinite alternate;
	}

	@keyframes bounce {
		from {
			transform: translateY(-5px);
		}
		to {
			transform: translateY(5px);
		}
	}
</style>
