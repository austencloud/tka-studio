<!-- src/lib/components/SettingsDialog/ImageExportTab/ImageExportPreviewPanel.svelte -->
<script lang="ts">
	import { browser } from '$app/environment';
	import { sequenceContainer } from '$lib/state/stores/sequence/SequenceContainer';
	import { useContainer } from '$lib/state/core/svelte5-integration.svelte';
	import type { ImageExportSettings } from '$lib/state/image-export-settings.svelte';

	// Import components
	import PreviewStateManager from './PreviewStateManager.svelte';
	import PreviewRenderer from './PreviewRenderer.svelte';

	// Props
	const { settings } = $props<{
		settings: ImageExportSettings;
	}>();

	// Use the sequence container
	const sequence = useContainer(sequenceContainer);

	// Get the current sequence data
	const sequenceBeats = $derived(sequence.beats || []);

	// Get the start position from localStorage
	let startPosition = $state<any>(null);

	// References to child components
	let stateManager: PreviewStateManager;
	let renderer: PreviewRenderer;

	// Load start position from localStorage
	$effect(() => {
		if (browser) {
			try {
				const savedStartPos = localStorage.getItem('start_position');
				if (savedStartPos) {
					startPosition = JSON.parse(savedStartPos);
				}
			} catch (error) {
				console.error('Failed to load start position from localStorage:', error);
			}
		}
	});

	// Function to update the preview
	function updatePreview() {
		if (browser && renderer) {
			renderer.updatePreview();
		}
	}
</script>

<div class="preview-container">
	<!-- State Manager (invisible component) -->
	<PreviewStateManager bind:this={stateManager} {settings} onUpdatePreview={updatePreview} />

	<!-- Renderer (visible component) -->
	<PreviewRenderer
		bind:this={renderer}
		{settings}
		{sequenceBeats}
		{startPosition}
		sequenceTitle={sequence.metadata?.name || 'Sequence'}
		difficultyLevel={sequence.metadata?.difficulty || 1}
	/>
</div>

<style>
	.preview-container {
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
	}
</style>
