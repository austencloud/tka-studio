<!-- src/lib/components/SettingsManager/SettingsManager.svelte -->
<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';
	import {
		loadImageExportSettings,
		saveImageExportSettings
	} from '$lib/state/image-export-settings.svelte';

	// Flag to track initialization
	let initialized = $state(false);

	// Initialize settings when component mounts
	onMount(() => {
		if (!browser) return;

		// Load settings from localStorage
		loadImageExportSettings();

		// Add event listener to save settings before unload
		window.addEventListener('beforeunload', saveImageExportSettings);

		// Mark as initialized
		initialized = true;
	});

	// Clean up event listeners when component is destroyed
	onDestroy(() => {
		if (!browser) return;

		// Remove event listener
		window.removeEventListener('beforeunload', saveImageExportSettings);
	});
</script>

<!-- This is an invisible component that just manages settings lifecycle -->
<div style="display: none;" aria-hidden="true">
	<!-- Status for debugging -->
	{#if initialized}
		<!-- Settings manager initialized -->
	{/if}
</div>
