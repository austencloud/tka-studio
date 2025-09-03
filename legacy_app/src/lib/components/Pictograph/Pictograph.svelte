<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { get } from 'svelte/store';
	import { popIn } from '$lib/transitions/popIn';
	import type { PictographData } from '$lib/types/PictographData';
	import type { PropData } from '../objects/Prop/PropData';
	import type { ArrowData } from '../objects/Arrow/ArrowData';
	import type { GridData } from '../objects/Grid/GridData';
	import Grid from '../objects/Grid/Grid.svelte';
	import Prop from '../objects/Prop/Prop.svelte';
	import Arrow from '../objects/Arrow/Arrow.svelte';
	import TKAGlyph from '../objects/Glyphs/TKAGlyph/TKAGlyph.svelte';
	import SvgManager from '../SvgManager/SvgManager';
	import type { Color, MotionType, Orientation, TKATurns } from '$lib/types/Types';
	import { PictographService } from './PictographService';
	import PictographError from './components/PictographError.svelte';
	import PictographDebug from './components/PictographDebug.svelte';
	import InitializingSpinner from './components/InitializingSpinner.svelte';
	import LoadingProgress from './components/LoadingProgress.svelte';
	import BeatLabel from './components/BeatLabel.svelte';
	import PictographWrapper from './components/PictographWrapper.svelte';
	import PictographSVG from './components/PictographSVG.svelte';
	// Import utility functions
	import { defaultPictographData } from './utils/defaultPictographData';
	import type { PictographDataSnapshot } from './utils/dataComparison';
	import {
		handlePictographError,
		handlePictographComponentError,
		type ErrorHandlerContext,
		type ComponentErrorContext,
		type FallbackDataContext
	} from './handlers/PictographErrorHandler';

	import { createAndPositionComponents as createAndPositionComponentsUtil } from './utils/componentPositioning';
	import {
		shouldShowBeatLabel,
		shouldShowDebugInfo,
		shouldShowLoadingIndicator,
		shouldShowMotionComponents
	} from './utils/PictographRenderUtils';
	import {
		handleGridLoaded as handleGridLoadedUtil,
		handleComponentLoaded as handleComponentLoadedUtil,
		checkLoadingComplete as checkLoadingCompleteUtil,
		hasRequiredMotionData as hasRequiredMotionDataUtil,
		type LoadingManagerContext
	} from './managers/PictographLoadingManager';

	// Import state management functions
	import {
		createPictographDataStore,
		initializePictographService,
		checkForDataChanges as checkForDataChangesUtil,
		updateComponentsFromData as updateComponentsFromDataUtil,
		setupPictographDataSubscription
	} from './managers/PictographStateManager';

	// Import lifecycle management functions
	import {
		initializePictograph,
		createCleanupFunction,
		createInitializationContext
	} from './managers/PictographLifecycle';

	// Props
	export let pictographData: PictographData | undefined = undefined;
	export let onClick: (() => void) | undefined = undefined;
	export let debug = false;
	export let animationDuration = 200; // Animation duration for transitions
	export let showLoadingIndicator = true;
	export let beatNumber: number | null = null;
	export let isStartPosition = false;

	// Create a local pictograph data store
	const pictographDataStore = createPictographDataStore(pictographData);

	// Reactively update the pictographDataStore when the pictographData changes.
	// Since pictographData is already a new object when the beat itself is updated
	// (due to the mapping in BeatFrameState), a direct assignment is sufficient and safer
	// than JSON.parse(JSON.stringify()), which can corrupt complex data.
	$: if (pictographData) {
		pictographDataStore.set(pictographData);
	}

	// Component state
	let state = 'initializing';
	let errorMessage: string | null = null;
	let gridData: GridData | null = null;
	let redPropData: PropData | null = null;
	let bluePropData: PropData | null = null;
	let redArrowData: ArrowData | null = null;
	let blueArrowData: ArrowData | null = null;
	let loadedComponents = new Set<string>();
	let requiredComponents = ['grid'];
	let totalComponentsToLoad = 1;
	let componentsLoaded = 0;
	let renderCount = 0;
	let loadProgress = 0;
	let service: PictographService | null = null;
	let lastDataSnapshot: PictographDataSnapshot | null = null;

	// Define the PictographEvents interface for proper typing
	interface PictographEvents {
		loaded: { error?: boolean };
		error: { message: string; component?: string };
		dataUpdated: { data: PictographData };
	}

	// Event dispatcher with proper typing
	const dispatch = createEventDispatcher<PictographEvents>();

	// Create a wrapper function for dispatch to use in contexts that expect a simpler function signature
	function dispatchWrapper(event: string, detail?: any): void {
		if (event === 'error' && detail?.message) {
			dispatch('error', { message: detail.message, component: detail.component });
		} else if (event === 'loaded') {
			dispatch('loaded', detail || {});
		} else if (event === 'dataUpdated' && detail?.data) {
			dispatch('dataUpdated', { data: detail.data });
		}
	}

	onMount(() => {
		// Make sure we have data to work with
		if (!pictographData && !get(pictographDataStore)) {
			// If no data is available, use default data
			pictographDataStore.set(defaultPictographData);
			return;
		}

		// Create a writable store for the service
		const serviceStore = {
			set: (value: PictographService | null) => {
				service = value;
			},
			update: (updater: (value: PictographService | null) => PictographService | null) => {
				service = updater(service);
			},
			subscribe: () => {
				return () => {};
			}
		};

		// Create a writable store for the state
		const stateStore = {
			set: (value: string) => {
				state = value;
			},
			update: (updater: (value: string) => string) => {
				state = updater(state);
			},
			subscribe: () => {
				return () => {};
			}
		};

		// Create a writable store for the lastDataSnapshot
		const lastDataSnapshotStore = {
			set: (value: PictographDataSnapshot | null) => {
				lastDataSnapshot = value;
			},
			update: (
				updater: (value: PictographDataSnapshot | null) => PictographDataSnapshot | null
			) => {
				lastDataSnapshot = updater(lastDataSnapshot);
			},
			subscribe: () => {
				return () => {};
			}
		};

		// Create initialization context
		const context = createInitializationContext(
			pictographDataStore,
			serviceStore,
			stateStore,
			lastDataSnapshotStore,
			initializePictographService,
			handleError
		);

		// Initialize the pictograph
		initializePictograph(context, debug);

		// Return cleanup function
		return createCleanupFunction(loadedComponents, subscription.unsubscribe);
	});

	// Create subscription for the pictographDataStore
	let subscription = { unsubscribe: () => {} };

	// Initialize subscription in onMount to ensure proper order
	onMount(() => {
		// Set up subscription to the pictographDataStore
		subscription = setupPictographDataSubscription(
			pictographDataStore,
			service,
			lastDataSnapshot,
			updateComponentsFromData,
			dispatchWrapper,
			debug,
			checkForDataChangesUtil
		);
	});

	// Function to update components when pictographData changes
	function updateComponentsFromData() {
		try {
			const result = updateComponentsFromDataUtil(
				pictographDataStore,
				service,
				state,
				errorMessage,
				gridData,
				createAndPositionComponents,
				requiredComponents,
				loadedComponents,
				hasRequiredMotionDataUtil
			);

			// Update local state
			state = result.state;
			errorMessage = result.errorMessage;
			if (result.renderCount > 0) {
				renderCount += result.renderCount;
			}
		} catch (error) {
			handleError('data update', error);
		}
	}

	// Create loading manager context
	function getLoadingManagerContext(): LoadingManagerContext {
		return {
			state: {
				set: (value: string) => {
					state = value;
				}
			},
			loadedComponents,
			requiredComponents,
			componentsLoaded,
			totalComponentsToLoad,
			dispatch: dispatchWrapper,
			pictographData: get(pictographDataStore)
		};
	}

	// Wrapper for handleGridLoadedUtil to maintain local state
	function handleGridLoaded(data: GridData) {
		try {
			// Update local state
			gridData = data;

			// Call the utility function
			handleGridLoadedUtil(data, getLoadingManagerContext(), {
				createAndPositionComponents
			});
		} catch (error) {
			handleError('grid loading', error);
		}
	}

	/**
	 * Helper function to detect mobile devices
	 */
	function isMobile(): boolean {
		return (
			typeof window !== 'undefined' &&
			(window.innerWidth <= 768 ||
				/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent))
		);
	}

	/**
	 * Preload arrow SVGs in parallel for better performance
	 */
	async function preloadArrowSvgs() {
		if (!service || !get(pictographDataStore)) return;

		const data = get(pictographDataStore);
		const arrowConfigs: Array<{
			motionType: MotionType;
			startOri: Orientation;
			turns: TKATurns;
			color: Color;
		}> = [];

		// Add red arrow config if exists
		if (data.redArrowData) {
			arrowConfigs.push({
				motionType: data.redArrowData.motionType,
				startOri: data.redArrowData.startOri,
				turns: data.redArrowData.turns,
				color: data.redArrowData.color
			});
		}

		// Add blue arrow config if exists
		if (data.blueArrowData) {
			arrowConfigs.push({
				motionType: data.blueArrowData.motionType,
				startOri: data.blueArrowData.startOri,
				turns: data.blueArrowData.turns,
				color: data.blueArrowData.color
			});
		}

		// Preload SVGs if we have any configs
		if (arrowConfigs.length > 0 && service) {
			try {
				// Create a new SvgManager instance for preloading
				const svgManager = new SvgManager();
				await svgManager.preloadArrowSvgs(arrowConfigs);
			} catch (error) {
				// Silently handle preloading errors
				if (import.meta.env.DEV) {
					console.warn('Arrow SVG preloading error:', error);
				}
			}
		}
	}

	// Wrapper for createAndPositionComponentsUtil to maintain local state
	function createAndPositionComponents() {
		try {
			// Make sure we have data to work with
			if (!get(pictographDataStore) || !service) return;

			// Create state context
			const stateContext = {
				requiredComponents,
				totalComponentsToLoad
			};

			// Call the utility function
			const result = createAndPositionComponentsUtil(
				get(pictographDataStore),
				service,
				gridData,
				stateContext
			);

			// Update local state
			requiredComponents = stateContext.requiredComponents;
			totalComponentsToLoad = stateContext.totalComponentsToLoad;
			redPropData = result.redPropData;
			bluePropData = result.bluePropData;
			redArrowData = result.redArrowData;
			blueArrowData = result.blueArrowData;

			// Preload arrow SVGs in parallel
			preloadArrowSvgs();
		} catch (error) {
			handleError('component creation', error);
		}
	}

	// Wrapper for handleComponentLoadedUtil to maintain local state
	function handleComponentLoaded(component: string) {
		// Call the utility function
		handleComponentLoadedUtil(component, getLoadingManagerContext());

		// Update local state
		componentsLoaded = getLoadingManagerContext().componentsLoaded;

		// Check if loading is complete
		checkLoadingComplete();
	}

	// Wrapper for checkLoadingCompleteUtil to maintain local state
	function checkLoadingComplete() {
		// Call the utility function
		checkLoadingCompleteUtil(getLoadingManagerContext());

		// Update render count
		renderCount++;
	}

	// Create component error handler context
	function getComponentErrorContext(): ComponentErrorContext {
		return {
			loadedComponents,
			componentsLoaded,
			totalComponentsToLoad,
			dispatch: dispatchWrapper,
			checkLoadingComplete
		};
	}

	// Create fallback data context
	function getFallbackDataContext(): FallbackDataContext {
		return {
			redPropData,
			bluePropData,
			redArrowData,
			blueArrowData
		};
	}

	// Handle component errors
	function handleComponentError(component: string, error: any) {
		handlePictographComponentError(
			component,
			error,
			getComponentErrorContext(),
			getFallbackDataContext()
		);
	}

	// Create error handler context
	function getErrorHandlerContext(): ErrorHandlerContext {
		return {
			pictographDataStore,
			dispatch: dispatchWrapper,
			state: {
				set: (value: string) => {
					state = value;
				}
			},
			errorMessage: {
				set: (value: string | null) => {
					errorMessage = value;
				}
			},
			componentsLoaded,
			totalComponentsToLoad
		};
	}

	// Handle general errors
	function handleError(source: string, error: any) {
		handlePictographError(source, error, getErrorHandlerContext());
	}

	// Using imported utility functions
</script>

<PictographWrapper {pictographDataStore} {onClick} {state}>
	<PictographSVG {pictographDataStore} {state} {errorMessage}>
		{#if state === 'initializing'}
			{#if shouldShowLoadingIndicator(state, showLoadingIndicator)}
				<InitializingSpinner {animationDuration} />
			{/if}
		{:else if state === 'error'}
			<PictographError {errorMessage} {animationDuration} />
		{:else}
			<Grid
				gridMode={get(pictographDataStore)?.gridMode}
				onPointsReady={handleGridLoaded}
				onError={(message) => handleComponentError('grid', message)}
				{debug}
			/>

			{#if shouldShowBeatLabel(beatNumber, isStartPosition)}
				<BeatLabel
					text={isStartPosition ? 'Start' : beatNumber?.toString() || ''}
					position="top-left"
					{animationDuration}
				/>
			{/if}

			{#if shouldShowMotionComponents(state)}
				<!-- Wrap all motion components in a single animated container for unified animation -->
				<g
					in:popIn={{
						duration: animationDuration,
						start: 0.85, // More pronounced scale effect (from 0.85 to 1.0)
						opacity: 0.2 // Start with slight visibility for smoother appearance
					}}
					style="transform-origin: center center;"
				>
					{#if get(pictographDataStore)?.letter}
						<TKAGlyph
							letter={get(pictographDataStore)?.letter}
							turnsTuple="(s, 0, 0)"
							x={50}
							y={800}
						/>
					{/if}

					{#each [{ color: 'red', propData: redPropData, arrowData: redArrowData }, { color: 'blue', propData: bluePropData, arrowData: blueArrowData }] as { color, propData, arrowData } (color)}
						{#if propData}
							<Prop
								{propData}
								on:loaded={() => handleComponentLoaded(`${color}Prop`)}
								on:error={(e) => handleComponentError(`${color}Prop`, e.detail.message)}
							/>
						{/if}

						{#if arrowData}
							<Arrow
								{arrowData}
								loadTimeoutMs={isMobile() ? 2000 : 1000}
								pictographService={service}
								on:loaded={() => handleComponentLoaded(`${color}Arrow`)}
								on:error={(e) => handleComponentError(`${color}Arrow`, e.detail.message)}
							/>
						{/if}
					{/each}
				</g>
			{/if}
		{/if}
	</PictographSVG>

	{#if state === 'loading' && shouldShowLoadingIndicator(state, showLoadingIndicator)}
		<LoadingProgress {loadProgress} showText={true} />
	{/if}

	{#if shouldShowDebugInfo(debug)}
		<PictographDebug
			{state}
			{componentsLoaded}
			totalComponents={totalComponentsToLoad}
			{renderCount}
		/>
	{/if}
</PictographWrapper>
