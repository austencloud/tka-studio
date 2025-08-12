<!-- Unified Layout - Handles both Landing and App modes -->
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
	
	// Import app mode state
	import { getAppMode, isLandingMode, isAppMode } from '$lib/state/appModeState.svelte';
	
	// Import runes-based state
	import {
		getActiveTab,
		getInitializationError,
		getInitializationProgress,
		getIsInitialized,
		getShowSettings,
		hideSettingsDialog,
		restoreApplicationState,
		setInitializationError,
		setInitializationProgress,
		setInitializationState,
		showSettingsDialog,
		switchTab,
		updateSettings,
	} from '$lib/state/appState.svelte';

	import { loadSequences } from '$lib/stores/sequenceActions';

	// Import components
	import ErrorScreen from '$components/ErrorScreen.svelte';
	import LoadingScreen from '$components/LoadingScreen.svelte';
	import MainInterface from '$components/MainInterface.svelte';
	import SettingsDialog from '$components/SettingsDialog.svelte';

	// Get DI container from context
	const getContainer = getContext<() => ServiceContainer | null>('di-container');

	// Services - resolved lazily
	let initService: IApplicationInitializationService | null = $state(null);
	let settingsService: ISettingsService | null = $state(null);
	let sequenceService: ISequenceService | null = $state(null);
	let deviceService: IDeviceDetectionService | null = $state(null);

	// App mode state
	let appMode = $derived(getAppMode());
	let isInitialized = $derived(getIsInitialized());
	let initializationError = $derived(getInitializationError());
	let initializationProgress = $derived(getInitializationProgress());

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
			const capabilities = deviceService.getCapabilities();
			console.log('📱 Device capabilities detected:', capabilities);

			// Step 4: Load initial data (only in app mode)
			if (isAppMode()) {
				setInitializationProgress(70);
				await loadSequences(sequenceService);
			} else {
				setInitializationProgress(70);
			}

			// Step 5: Restore application state (tab memory)
			setInitializationProgress(85);
			await restoreApplicationState();

			// Step 6: Complete initialization
			setInitializationProgress(100);
			setInitializationState(true, false, null, 100);

			console.log(`✅ TKA V2 Unified initialized successfully (${appMode} mode)`);
		} catch (error) {
			console.error('❌ Application initialization failed:', error);
			setInitializationError(
				error instanceof Error ? error.message : 'Unknown initialization error'
			);
		}
	});

	// Handle keyboard shortcuts (only in app mode)
	$effect(() => {
		if (!isAppMode()) return;

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

			// Tab navigation (Ctrl/Cmd + 1-5)
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
						switchTab('sequence_card');
						break;
					case '4':
						event.preventDefault();
						switchTab('write');
						break;
					case '5':
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

<svelte:head>
	<title>{isLandingMode() ? 'The Kinetic Alphabet - Flow Arts Choreography Toolbox' : 'TKA Constructor - The Kinetic Alphabet'}</title>
	<meta name="description" content="The Kinetic Alphabet is a revolutionary flow arts choreography toolbox for poi, staff, fans, and other flow arts. Create, learn, and share movement sequences." />
</svelte:head>

<!-- Unified Application Container -->
<div class="tka-unified-app" data-mode={appMode} data-testid="unified-application">
	{#if initializationError}
		<ErrorScreen
			error={initializationError}
			onRetry={() => window.location.reload()}
		/>
	{:else if !isInitialized}
		<LoadingScreen 
			progress={initializationProgress} 
			message={isLandingMode() ? "Loading TKA..." : "Initializing Constructor..."}
		/>
	{:else}
		<!-- Main Interface handles both landing and app modes -->
		<MainInterface />

		<!-- Settings dialog only in app mode -->
		{#if isAppMode() && getShowSettings()}
			<SettingsDialog />
		{/if}
	{/if}
</div>

<style>
	.tka-unified-app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
		width: 100%;
		position: relative;
		overflow: hidden;
		transition: all 0.3s ease;
	}

	.tka-unified-app[data-mode="landing"] {
		/* Landing mode styles */
		background: transparent;
		overflow: visible; /* Allow scrolling for landing pages */
	}

	.tka-unified-app[data-mode="app"] {
		/* App mode styles */
		background: transparent;
		overflow: hidden; /* Fixed height for app interface */
	}

	/* Global typography for landing mode */
	.tka-unified-app[data-mode="landing"] {
		--text-color: rgba(255, 255, 255, 0.95);
		--text-secondary: rgba(255, 255, 255, 0.8);
		--text-muted: rgba(255, 255, 255, 0.6);
	}

	/* Global typography for app mode */
	.tka-unified-app[data-mode="app"] {
		--text-color: rgba(255, 255, 255, 0.95);
		--muted-foreground: rgba(255, 255, 255, 0.7);
		--foreground: rgba(255, 255, 255, 0.95);
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.tka-unified-app[data-mode="landing"] {
			/* Better mobile scrolling for landing */
			-webkit-overflow-scrolling: touch;
		}

		.tka-unified-app[data-mode="app"] {
			/* Dynamic viewport height for mobile app */
			min-height: 100dvh;
		}
	}

	/* Reduced motion support */
	@media (prefers-reduced-motion: reduce) {
		.tka-unified-app {
			transition: none;
		}
	}

	/* High contrast mode */
	@media (prefers-contrast: high) {
		.tka-unified-app[data-mode="landing"] {
			--text-color: white;
			--text-secondary: rgba(255, 255, 255, 0.9);
		}

		.tka-unified-app[data-mode="app"] {
			--text-color: white;
			--foreground: white;
		}
	}

	/* Print styles */
	@media print {
		.tka-unified-app {
			min-height: auto;
			overflow: visible;
		}
	}
</style>
