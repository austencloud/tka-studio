<script lang="ts">
	import { onMount } from 'svelte';
	import { getContainer } from '$lib/core/di/ContainerProvider';
	import { setServiceContainer } from '$lib/core/di/serviceContext';
	import { registerServices } from '$lib/core/di/registerServices';
	import { initializeStateManagement } from '$lib/state';
	import { browser } from '$app/environment';
	import SettingsManager from '$lib/components/SettingsManager/SettingsManager.svelte';

	// State tracking
	let isStateInitialized = false;
	let isInitializing = false;

	/**
	 * Initialize the state management system
	 * This function ensures we only initialize once
	 */
	async function initializeState() {
		// Guard against multiple initializations
		if (isStateInitialized || isInitializing || !browser) return;

		isInitializing = true;

		try {
			// Initialize dependency injection
			const container = getContainer();
			registerServices(container);
			setServiceContainer(container);

			// Explicitly import the state machines to ensure proper registration order
			// We need to await these imports to ensure they're fully loaded
			await import('$lib/state/machines/app/app.machine');
			await import('$lib/state/machines/sequenceMachine');

			// Import the sequence container to ensure it's available
			const { sequenceContainer } = await import('$lib/state/stores/sequence/SequenceContainer');

			// Explicitly try to load sequence from localStorage
			try {
				sequenceContainer.loadFromLocalStorage();
			} catch (error) {
				console.error('ServiceProvider: Error loading sequence from localStorage:', error);
			}

			// Now initialize state management
			initializeStateManagement();
			isStateInitialized = true;
		} catch (error) {
			console.error('Error initializing state management:', error);
		} finally {
			isInitializing = false;
		}
	}

	// Start initialization in the script section for SSR compatibility
	if (browser) {
		initializeState();
	}

	// Also try in onMount as a fallback
	onMount(() => {
		if (!isStateInitialized && browser) {
			initializeState();
		}
	});
</script>

{#if isStateInitialized || !browser}
	<!-- Include the SettingsManager component to handle settings lifecycle -->
	<SettingsManager />
	<slot></slot>
{:else}
	<div class="loading">Initializing application...</div>
{/if}

<style>
	.loading {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
		width: 100vw;
		background-color: rgb(11, 29, 42);
		color: white;
		font-size: 1.5rem;
	}
</style>
