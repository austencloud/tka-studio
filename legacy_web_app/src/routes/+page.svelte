<script lang="ts">
	import { onMount } from '$lib/utils/svelte-lifecycle';
	import { fade } from 'svelte/transition';

	// Components
	import FullScreen from '$lib/AppFullScreen.svelte';
	import MainLayout from '$lib/components/MainWidget/layout/MainLayout.svelte';
	import LoadingOverlay from '$lib/components/MainWidget/loading/LoadingOverlay.svelte';
	import BackgroundCanvas from '$lib/components/Backgrounds/BackgroundCanvas.svelte';
	import BackgroundProvider from '$lib/components/Backgrounds/BackgroundProvider.svelte';
	import FirstTimeSetupDialog from '$lib/components/FirstTimeSetup/FirstTimeSetupDialog.svelte';
	import FirstTimeSetupButton from '$lib/components/FirstTimeSetup/FirstTimeSetupButton.svelte';

	// State Management
	import { appActions } from '$lib/state/machines/app/app.actions';
	import { useSelector } from '@xstate/svelte';
	import { appService } from '$lib/state/machines/app/app.machine';
	import { uiStore } from '$lib/state/stores/uiStore';
	import type { BackgroundType } from '$lib/components/Backgrounds/types/types';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';

	// Performance metrics type is defined in the handler directly

	// Get window dimensions from UI store using $derived
	const windowHeight = $derived($uiStore ? $uiStore.windowHeight + 'px' : '100vh');

	// --- Get State directly from the app service using $derived ---
	const isInitializingAppStore = useSelector(appService, (state) =>
		state.matches('initializingApp')
	);
	const isInitializingApp = $derived($isInitializingAppStore);

	const hasFailedStore = useSelector(appService, (state) => state.matches('initializationFailed'));
	const hasFailed = $derived($hasFailedStore);

	const isReadyStore = useSelector(appService, (state) => state.matches('ready'));
	const isReady = $derived($isReadyStore);

	const currentBackgroundStore = useSelector(appService, (state) => state.context.background);
	const currentBackground = $derived($currentBackgroundStore as BackgroundType);

	const initializationErrorMsgStore = useSelector(
		appService,
		(state) => state.context.initializationError
	);
	const initializationErrorMsg = $derived($initializationErrorMsgStore as string);

	const loadingProgressStore = useSelector(appService, (state) => state.context.loadingProgress);
	const loadingProgress = $derived($loadingProgressStore as number);

	const loadingMessageStore = useSelector(appService, (state) => state.context.loadingMessage);
	const loadingMessage = $derived($loadingMessageStore as string);

	// --- Event Handlers ---
	function handleFullScreenToggle(event: CustomEvent<boolean>) {
		appActions.setFullScreen(event.detail);
		hapticFeedbackService.trigger('success');
	}

	function handleBackgroundChange(event: CustomEvent<string>) {
		const validBackgrounds = ['snowfall', 'nightSky'] as const;
		type ValidBackground = (typeof validBackgrounds)[number];

		if (validBackgrounds.includes(event.detail as any)) {
			appActions.updateBackground(event.detail as ValidBackground);
		}
	}

	function handleBackgroundReady() {
		appActions.backgroundReady();
	}

	function handlePerformanceReport(_metrics: {
		fps: number;
		memory?: { used: number; total: number };
	}) {
		// We're not using the metrics currently, but we need to provide the handler
		// If we want to use them in the future, we can add an action to appActions
		// Example: appActions.updatePerformanceMetrics(_metrics);
	}

	function handleTabChange(event: CustomEvent<number>) {
		appActions.changeTab(event.detail);
	}

	function handleRetry() {
		appActions.retryInitialization();
	}

	// Reference to the first-time setup dialog component
	let firstTimeSetupDialog = $state<{ showDialog: () => void } | null>(null);

	// Function to show the first-time setup dialog
	function showFirstTimeSetupDialog() {
		if (firstTimeSetupDialog) {
			firstTimeSetupDialog.showDialog();
		}
	}

	// --- Lifecycle ---
	onMount(() => {
		// Force the state machine to transition
		setTimeout(() => {
			appActions.backgroundReady();
		}, 500);
	});
</script>

<div id="main-widget" style="height: {windowHeight}" class="main-widget">
	<FullScreen on:toggleFullscreen={handleFullScreenToggle}>
		<div class="background" class:blur-background={isInitializingApp || hasFailed}>
			<BackgroundProvider
				backgroundType={currentBackground || 'snowfall'}
				isLoading={isInitializingApp || hasFailed}
				initialQuality={isInitializingApp || hasFailed ? 'medium' : 'high'}
			>
				<BackgroundCanvas
					appIsLoading={isInitializingApp || hasFailed}
					onReady={handleBackgroundReady}
					onPerformanceReport={handlePerformanceReport}
				/>
			</BackgroundProvider>
		</div>

		{#if isInitializingApp || hasFailed}
			<div class="loading-overlay-wrapper" transition:fade={{ duration: 300 }}>
				<LoadingOverlay
					message={loadingMessage}
					progress={loadingProgress}
					onRetry={handleRetry}
					showInitializationError={hasFailed}
					errorMessage={initializationErrorMsg}
				/>
			</div>
		{/if}

		{#if isReady}
			<div class="main-layout-wrapper" transition:fade={{ duration: 500, delay: 100 }}>
				<MainLayout on:changeBackground={handleBackgroundChange} on:tabChange={handleTabChange} />
			</div>

			<!-- First-time setup dialog -->
			<FirstTimeSetupDialog bind:this={firstTimeSetupDialog} />

			<!-- Setup button - always visible -->
			<FirstTimeSetupButton showDialog={showFirstTimeSetupDialog} />
		{/if}
	</FullScreen>
</div>

<style>
	.main-widget {
		width: 100%;
		height: 100vh;
		position: relative;
		overflow: hidden;
		display: flex;
		flex-direction: column;
	}

	.background {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		z-index: 0;
		transition: filter 0.3s ease-in-out;
	}

	.blur-background {
		filter: blur(5px);
	}

	.loading-overlay-wrapper {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		z-index: 10;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.main-layout-wrapper {
		position: relative;
		z-index: 1;
		flex: 1;
		display: flex;
		flex-direction: column;
		width: 100%;
		height: 100%;
	}
</style>
