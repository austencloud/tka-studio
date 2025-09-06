<!-- src/lib/components/SettingsDialog/ImageExportTab/PreviewRenderer.svelte -->
<script lang="ts" module>
	// Export the updatePreview method to make it accessible from outside
	export interface PreviewRenderer {
		updatePreview: () => Promise<void>;
	}
</script>

<script lang="ts">
	import { browser } from '$app/environment';
	import { exportSequenceImage } from '$lib/components/Pictograph/export/SequenceImageExporter';
	import {
		createTemporaryRenderElement,
		cloneBeatFrameContent,
		removeTemporaryElement,
		logBeatFrameDetails
	} from '$lib/components/SequenceWorkbench/BeatFrame/beatFrameHelpers';
	import type { ImageExportSettings } from '$lib/state/image-export-settings.svelte';

	// Props
	const { settings, sequenceBeats, startPosition, sequenceTitle, difficultyLevel } = $props<{
		settings: ImageExportSettings;
		sequenceBeats: any[];
		startPosition: any;
		sequenceTitle: string;
		difficultyLevel: number;
	}>();

	// Local state
	let previewElement = $state<HTMLDivElement | null>(null);
	let previewImage = $state<string | null>(null);
	let isLoading = $state(false);
	let error = $state<string | null>(null);
	let cachedPreview = $state<string | null>(null);

	// Set appropriate styles for the preview element
	$effect(() => {
		if (browser && previewElement) {
			// Set width to 100% but let height adjust naturally
			previewElement.style.width = '100%';
			// Don't set a fixed height - let it adjust based on content
			previewElement.style.height = 'auto';
			// Set a minimum height to prevent collapse during loading
			previewElement.style.minHeight = '200px';
		}
	});

	// Update the preview image
	export async function updatePreview() {
		console.log('🔍 updatePreview called', {
			timestamp: new Date().toISOString(),
			isLoading,
			hasPreviewImage: !!previewImage
		});

		// Skip if not in browser or no preview element
		if (!browser || !previewElement) {
			console.log('⚠️ Skipping preview update: browser or previewElement not available');
			return;
		}

		// Skip if sequence is empty
		if (!sequenceBeats || sequenceBeats.length === 0) {
			console.log('⚠️ Skipping preview update: sequence is empty');
			previewImage = null;
			error = 'No sequence to preview. Add beats to see a preview.';
			return;
		}

		try {
			isLoading = true;
			error = null;

			// Get the preview element dimensions
			const width = previewElement.clientWidth;
			const height = previewElement.clientHeight;

			// Skip if dimensions are too small
			if (width < 50 || height < 50) {
				return;
			}

			// Log BeatFrame details for debugging
			logBeatFrameDetails();

			// Create a temporary element for rendering
			const tempElement = createTemporaryRenderElement(width, height);

			// Clone the BeatFrame content into our temporary element
			const cloneSuccess = cloneBeatFrameContent(tempElement);

			if (!cloneSuccess) {
				throw new Error('Failed to clone BeatFrame content');
			}

			// Log preview generation details
			console.log('Generating preview with settings:', {
				sequenceTitle,
				difficultyLevel,
				beatsCount: sequenceBeats.length,
				hasStartPosition: !!startPosition,
				settings,
				svgCount: tempElement.querySelectorAll('svg').length
			});

			// Make sure we have SVG elements
			if (tempElement.querySelectorAll('svg').length === 0) {
				console.error('No SVG elements found in the cloned BeatFrame');
				throw new Error('No SVG elements found for rendering');
			}

			// Export the sequence with current settings
			const result = await exportSequenceImage(tempElement, {
				beats: sequenceBeats,
				startPosition: startPosition,
				backgroundColor: '#FFFFFF', // Always use white for better contrast
				scale: 1, // Scale for preview quality
				quality: 1.0, // Always use maximum quality
				format: 'png', // PNG format for lossless quality
				// Use dynamic columns based on sequence length
				columns: sequenceBeats.length <= 4 ? sequenceBeats.length : 4,
				spacing: 0,
				// Start position is now always included
				includeStartPosition: true,
				addUserInfo: settings.addUserInfo,
				addWord: settings.addWord,
				addDifficultyLevel: settings.addDifficultyLevel,
				addBeatNumbers: settings.addBeatNumbers,
				addReversalSymbols: settings.addReversalSymbols,
				// Pass sequence metadata
				title: sequenceTitle,
				userName: settings.userName,
				notes: settings.customNote,
				exportDate: new Date().toLocaleDateString(),
				difficultyLevel: difficultyLevel
			});

			// Clean up the temporary element
			removeTemporaryElement(tempElement);

			// Update the preview image
			if (result && result.dataUrl) {
				previewImage = result.dataUrl;
				// Cache the preview for future use
				cachedPreview = result.dataUrl;
			} else {
				throw new Error('Failed to generate preview image');
			}
		} catch (err) {
			console.error('Error generating preview:', err);
			error =
				'Failed to generate preview image: ' + (err instanceof Error ? err.message : String(err));
			previewImage = null;
		} finally {
			isLoading = false;
		}
	}
</script>

<div class="preview-panel" bind:this={previewElement}>
	{#if isLoading}
		<div class="loading-container">
			<div class="spinner"></div>
			<p>Generating preview...</p>
		</div>
	{:else if error}
		<div class="error-container">
			<i class="fa-solid fa-exclamation-triangle"></i>
			<p>{error}</p>

			{#if sequenceBeats.length === 0}
				<div class="help-text">
					Create a sequence to see a preview of how it will look when exported.
				</div>
			{:else}
				<div class="help-text">
					Try refreshing the page or creating a new sequence. If the problem persists, check the
					browser console for more details.
				</div>
				<button class="retry-button" onclick={updatePreview}>
					<i class="fa-solid fa-sync"></i> Retry
				</button>
			{/if}
		</div>
	{:else if previewImage}
		<img src={previewImage} alt="Sequence preview" class="preview-image" />
	{:else}
		<div class="placeholder-container">
			<i class="fa-solid fa-image"></i>
			<p>Preview will appear here</p>
		</div>
	{/if}
</div>

<style>
	.preview-panel {
		background: linear-gradient(135deg, #1f1f24, #2a2a30);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 8px;
		display: flex;
		align-items: center;
		justify-content: center;
		overflow: hidden;
		min-height: 200px; /* Reduced minimum height */
		width: 100%;
		position: relative;
		box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.2);
		padding: 0; /* No padding to maximize space */
	}

	.preview-image {
		width: 100%; /* Fill the entire container width */
		height: auto; /* Let height adjust based on aspect ratio */
		max-height: none; /* No maximum height constraint */
		object-fit: contain; /* Maintain aspect ratio while filling container */
		object-position: center; /* Center the image */
		border-radius: 0; /* No border radius to maximize space */
		box-shadow: none; /* Remove shadow to maximize space */
		margin: 0; /* No margins to maximize space */
		display: block; /* Ensure proper display */
	}

	.loading-container,
	.error-container,
	.placeholder-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 2rem;
		text-align: center;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
		min-height: 200px; /* Ensure a minimum height for these containers */
		width: 100%;
	}

	.spinner {
		width: 40px;
		height: 40px;
		border: 4px solid rgba(255, 255, 255, 0.1);
		border-left-color: #167bf4;
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin-bottom: 1rem;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	.error-container i,
	.placeholder-container i {
		font-size: 3rem;
		margin-bottom: 1rem;
		opacity: 0.5;
	}

	.error-container {
		color: #ff6b6b;
	}

	.error-container i {
		color: #ff6b6b;
	}

	.help-text {
		margin-top: 1rem;
		font-size: 0.9rem;
		color: rgba(255, 255, 255, 0.5);
		max-width: 300px;
		line-height: 1.4;
	}

	.retry-button {
		margin-top: 1.5rem;
		background: linear-gradient(to bottom, #3a3a43, #2a2a2e);
		color: var(--color-text-primary, white);
		border: 2px solid var(--tkc-border-color, #3c3c41);
		border-radius: 8px;
		padding: 0.5rem 1rem;
		font-weight: bold;
		display: flex;
		align-items: center;
		gap: 0.5rem;
		transition: all 0.2s ease;
		cursor: pointer;
		box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
	}

	.retry-button:hover {
		background: linear-gradient(to bottom, #454550, #323238);
		transform: translateY(-2px);
		box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
	}

	.retry-button:active {
		transform: translateY(0);
		background: linear-gradient(to bottom, #2a2a30, #1e1e22);
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
	}
</style>
