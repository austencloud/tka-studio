<script lang="ts">
	import { resolve } from '$services/bootstrap';
	import type { ServiceContainer } from '$services/di/ServiceContainer';
	import type {
		IApplicationInitializationService,
		IDeviceDetectionService,
		ISequenceService,
		ISettingsService,
	} from '$services/interfaces';
	import { getContext, onMount } from 'svelte';
	// Import runes-based state
	import {
		getActiveTab,
		getInitializationError,
		getInitializationProgress,
		getIsInitialized,
		getShowSettings,
		hideSettingsDialog,
		setInitializationError,
		setInitializationProgress,
		setInitializationState,
		showSettingsDialog,
		switchTab,
		updateSettings,
	} from '$lib/state/appState.svelte';

	import { loadSequences } from '$lib/stores/sequenceActions';

	// Import components
	import ErrorScreen from './ErrorScreen.svelte';
	import LoadingScreen from './LoadingScreen.svelte';
	import MainInterface from './MainInterface.svelte';
	import SettingsDialog from './SettingsDialog.svelte';

	// Get DI container from context
	const getContainer = getContext<() => ServiceContainer | null>('di-container');

	// Services - resolved lazily
	let initService: IApplicationInitializationService | null = $state(null);
	let settingsService: ISettingsService | null = $state(null);
	let sequenceService: ISequenceService | null = $state(null);
	let deviceService: IDeviceDetectionService | null = $state(null);

	// Resolve services when container is available
	$effect(() => {
		const container = getContainer?.();
		if (container && !initService) {
			try {
				initService = resolve('IApplicationInitializationService');
				settingsService = resolve('ISettingsService');
				sequenceService = resolve('ISequenceService');
				deviceService = resolve('IDeviceDetectionService');
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
		while (
			(!initService || !settingsService || !sequenceService || !deviceService) &&
			attempts < 10
		) {
			await new Promise((resolve) => setTimeout(resolve, 100));
			attempts++;
		}

		if (!initService || !settingsService || !sequenceService || !deviceService) {
			setInitializationError('Failed to resolve required services');
			return;
		}

		try {
			setInitializationState(false, true, null, 0);

			// Step 1: Initialize application services
			setInitializationProgress(20);
			await initService.initialize();

			// Step 2: Load settings
			setInitializationProgress(40);
			await settingsService.loadSettings();
			updateSettings(settingsService.currentSettings);

			// Step 3: Initialize device detection
			setInitializationProgress(50);
			// Device service auto-initializes in constructor, just ensure it's working
			const capabilities = deviceService.getCapabilities();
			console.log('📱 Device capabilities detected:', capabilities);

			// Step 4: Load initial data
			setInitializationProgress(70);
			await loadSequences(sequenceService);

			// Step 6: Complete initialization
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
						switchTab('browse');
						break;
					case '3':
						event.preventDefault();
						switchTab('write');
						break;
					case '4':
						event.preventDefault();
						switchTab('learn');
						break;
					case '5':
						event.preventDefault();
						switchTab('sequence_card');
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
		<LoadingScreen progress={getInitializationProgress()} message="Initializing TKA..." />
	{:else}
		<MainInterface />

		{#if getShowSettings()}
			<SettingsDialog />
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
</style>
