/**
 * Main Application - Root component for TKA V2 Modern
 * 
 * Coordinates application initialization and provides the main interface.
 * Uses pure Svelte 5 runes for state management.
 */

<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import type { ServiceContainer } from '@tka/shared/di/core/ServiceContainer';
	import {
		IApplicationInitializationService,
		ISettingsService,
		ISequenceService
	} from '$services/interfaces';

	// Import runes-based state
	import {
		getIsInitialized,
		getIsInitializing,
		getInitializationError,
		getInitializationProgress,
		getActiveTab,
		getShowSettings,
		setInitializationState,
		setInitializationProgress,
		setInitializationError,
		updateSettings,
		switchTab,
		showSettingsDialog,
		hideSettingsDialog
	} from '$stores/appState.svelte';

	import { loadSequences } from '$stores/sequenceActions';

	// Import components
	import LoadingScreen from './LoadingScreen.svelte';
	import ErrorScreen from './ErrorScreen.svelte';
	import MainInterface from './MainInterface.svelte';
	import SettingsDialog from './SettingsDialog.svelte';

	// Get DI container from context
	const getContainer = getContext<() => ServiceContainer | null>('di-container');

	// Services - resolved lazily
	let initService: IApplicationInitializationService | null = $state(null);
	let settingsService: ISettingsService | null = $state(null);
	let sequenceService: ISequenceService | null = $state(null);

	// Resolve services when container is available
	$effect(() => {
		const container = getContainer?.();
		if (container && !initService) {
			try {
				initService = container.resolve(IApplicationInitializationService);
				settingsService = container.resolve(ISettingsService);
				sequenceService = container.resolve(ISequenceService);
				console.log('✅ Services resolved successfully');
			} catch (error) {
				console.error('Failed to resolve services:', error);
				setInitializationError(`Service resolution failed: ${error}`);
			}
		}
	});

	// Initialize application
	onMount(async () => {
		const container = getContainer?.();
		if (!container) {
			setInitializationError('No DI container available');
			return;
		}

		// Wait for services to be resolved
		let attempts = 0;
		while ((!initService || !settingsService || !sequenceService) && attempts < 10) {
			await new Promise(resolve => setTimeout(resolve, 100));
			attempts++;
		}

		if (!initService || !settingsService || !sequenceService) {
			setInitializationError('Failed to resolve required services');
			return;
		}

		try {
			setInitializationState(false, true, null, 0);

			// Step 1: Initialize application services
			setInitializationProgress(25);
			await initService.initialize();

			// Step 2: Load settings
			setInitializationProgress(50);
			await settingsService.loadSettings();
			updateSettings(settingsService.currentSettings);

			// Step 3: Load initial data
			setInitializationProgress(75);
			await loadSequences(sequenceService);

			// Step 4: Complete initialization
			setInitializationProgress(100);
			setInitializationState(true, false, null, 100);

			console.log('✅ TKA V2 Modern initialized successfully');
		} catch (error) {
			console.error('❌ Application initialization failed:', error);
			setInitializationError(
				error instanceof Error ? error.message : 'Unknown initialization error'
			);
		}
	});

	// Handle keyboard shortcuts
	$effect(() => {
		function handleKeydown(event: KeyboardEvent) {
			// Settings dialog toggle (Ctrl/Cmd + ,)
			if ((event.ctrlKey || event.metaKey) && event.key === ',') {
				event.preventDefault();
				if (getShowSettings()) {
					hideSettingsDialog();
				} else {
					showSettingsDialog();
				}
			}

			// Tab navigation (Ctrl/Cmd + 1-4)
			if (event.ctrlKey || event.metaKey) {
				switch (event.key) {
					case '1':
						event.preventDefault();
						switchTab('construct');
						break;
					case '2':
						event.preventDefault();
						switchTab('generate');
						break;
					case '3':
						event.preventDefault();
						switchTab('browse');
						break;
					case '4':
						event.preventDefault();
						switchTab('learn');
						break;
				}
			}
		}

		document.addEventListener('keydown', handleKeydown);
		return () => document.removeEventListener('keydown', handleKeydown);
	});
</script>

<!-- Provide DI container to children -->
<div class="tka-app" data-theme={getActiveTab()} data-testid="main-application">
	{#if getInitializationError()}
		<ErrorScreen
			error={getInitializationError() || 'Unknown error'}
			onRetry={() => window.location.reload()}
		/>
	{:else if !getIsInitialized()}
		<LoadingScreen
			progress={getInitializationProgress()}
			message="Initializing TKA..."
		/>
	{:else}
		<MainInterface />

		{#if getShowSettings()}
			<SettingsDialog
				{settingsService}
				onClose={hideSettingsDialog}
			/>
		{/if}
	{/if}
</div>

<style>
	.tka-app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
		width: 100%;
		position: relative;
		overflow: hidden;
	}

	/* Theme-specific styles */
	.tka-app[data-theme="construct"] {
		/* Construct tab specific styles */
	}

	.tka-app[data-theme="generate"] {
		/* Generate tab specific styles */
	}

	.tka-app[data-theme="browse"] {
		/* Browse tab specific styles */
	}

	.tka-app[data-theme="learn"] {
		/* Learn tab specific styles */
	}
</style>
