<script lang="ts">
	import Pictograph from '$lib/components/Pictograph/Pictograph.svelte';
	import { onMount } from 'svelte';
	import type { PictographData } from '$lib/types/PictographData.js';
	import LoadingSpinner from '$lib/components/MainWidget/loading/LoadingSpinner.svelte';
	import { selectedStartPos } from '$lib/stores/sequence/selectionStore';
	import pictographDataStore from '$lib/stores/pictograph/pictographStore';
	import { pictographContainer } from '$lib/state/stores/pictograph/pictographContainer';
	import startPositionService from '$lib/services/StartPositionService';
	import { isSequenceEmpty } from '$lib/state/machines/sequenceMachine/persistence';
	import { browser } from '$app/environment';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import LoadingOverlay from './LoadingOverlay.svelte';
	import transitionLoading, {
		transitionLoadingStore
	} from '$lib/state/stores/ui/transitionLoadingStore';

	let gridMode = 'diamond';
	let startPositionPictographs: PictographData[] = [];
	let filteredDataAvailable = false;
	let dataInitializationChecked = false;
	let isLoading = true;
	let loadingError = false;
	let isTransitioning = false; // Local state for the loading overlay

	// Subscribe to the global loading state
	$effect(() => {
		const unsubscribe = transitionLoadingStore.subscribe((value) => {
			isTransitioning = value;
		});

		return unsubscribe;
	});

	let initialDataTimeout: number | null = null;

	const unsubscribe = pictographDataStore.subscribe((data) => {
		if (!browser) return;

		if (data && data.length > 0) {
			dataInitializationChecked = true;

			const pictographData = data as PictographData[];
			const defaultStartPosKeys =
				gridMode === 'diamond'
					? ['alpha1_alpha1', 'beta5_beta5', 'gamma11_gamma11']
					: ['alpha2_alpha2', 'beta4_beta4', 'gamma12_gamma12'];

			const filteredPictographs = pictographData.filter(
				(entry) =>
					entry.redMotionData &&
					entry.blueMotionData &&
					defaultStartPosKeys.includes(`${entry.startPos}_${entry.endPos}`)
			);

			startPositionPictographs = filteredPictographs;
			filteredDataAvailable = filteredPictographs.length > 0;

			isLoading = false;
			if (initialDataTimeout) clearTimeout(initialDataTimeout);
		} else if (dataInitializationChecked) {
			startPositionPictographs = [];
			filteredDataAvailable = false;
			isLoading = false;
		}
	});

	function handleStartPosClick(event: CustomEvent) {
		if (event.detail?.immediate) {
			isLoading = true;
			dataInitializationChecked = false;
			loadingError = false;
		}
		hapticFeedbackService.trigger('selection');
	}

	onMount(() => {
		document.addEventListener('start-position-click', handleStartPosClick as EventListener);

		initialDataTimeout = window.setTimeout(() => {
			if (isLoading && !dataInitializationChecked) {
				isLoading = false;
				loadingError = true;
			}
		}, 5000);

		return () => {
			unsubscribe();
			document.removeEventListener('start-position-click', handleStartPosClick as EventListener);
			if (initialDataTimeout) {
				clearTimeout(initialDataTimeout);
			}
		};
	});

	function safeCopyPictographData(data: PictographData): PictographData {
		const safeCopy: PictographData = {
			letter: data.letter,
			startPos: data.startPos,
			endPos: data.endPos,
			timing: data.timing,
			direction: data.direction,
			gridMode: data.gridMode,
			grid: data.grid,

			redMotionData: data.redMotionData
				? {
						id: data.redMotionData.id,
						handRotDir: data.redMotionData.handRotDir,
						color: data.redMotionData.color,
						leadState: data.redMotionData.leadState,
						motionType: data.redMotionData.motionType,
						startLoc: data.redMotionData.startLoc,
						endLoc: data.redMotionData.endLoc,
						startOri: data.redMotionData.startOri,
						endOri: data.redMotionData.endOri,
						propRotDir: data.redMotionData.propRotDir,
						turns: data.redMotionData.turns,
						prefloatMotionType: data.redMotionData.prefloatMotionType,
						prefloatPropRotDir: data.redMotionData.prefloatPropRotDir
					}
				: null,

			blueMotionData: data.blueMotionData
				? {
						id: data.blueMotionData.id,
						handRotDir: data.blueMotionData.handRotDir,
						color: data.blueMotionData.color,
						leadState: data.blueMotionData.leadState,
						motionType: data.blueMotionData.motionType,
						startLoc: data.blueMotionData.startLoc,
						endLoc: data.blueMotionData.endLoc,
						startOri: data.blueMotionData.startOri,
						endOri: data.blueMotionData.endOri,
						propRotDir: data.blueMotionData.propRotDir,
						turns: data.blueMotionData.turns,
						prefloatMotionType: data.blueMotionData.prefloatMotionType,
						prefloatPropRotDir: data.blueMotionData.prefloatPropRotDir
					}
				: null,

			redPropData: null,
			bluePropData: null,
			redArrowData: null,
			blueArrowData: null,
			gridData: null,

			motions: [],
			redMotion: null,
			blueMotion: null,
			props: []
		};

		return safeCopy;
	}

	const handleSelect = async (startPosPictograph: PictographData) => {
		try {
			// Immediately show loading state
			isTransitioning = true;
			transitionLoading.start();

			// Provide haptic feedback when selecting a start position
			if (browser) {
				hapticFeedbackService.trigger('selection');
			}

			await startPositionService.addStartPosition(startPosPictograph);

			const startPosCopy = safeCopyPictographData(startPosPictograph);

			startPosCopy.isStartPosition = true;

			if (startPosCopy.redMotionData) {
				startPosCopy.redMotionData.motionType = 'static';
				startPosCopy.redMotionData.endLoc = startPosCopy.redMotionData.startLoc;
				startPosCopy.redMotionData.endOri = startPosCopy.redMotionData.startOri;
				startPosCopy.redMotionData.turns = 0;
			}

			if (startPosCopy.blueMotionData) {
				startPosCopy.blueMotionData.motionType = 'static';
				startPosCopy.blueMotionData.endLoc = startPosCopy.blueMotionData.startLoc;
				startPosCopy.blueMotionData.endOri = startPosCopy.blueMotionData.startOri;
				startPosCopy.blueMotionData.turns = 0;
			}

			selectedStartPos.set(startPosCopy);

			pictographContainer.setData(startPosCopy);

			isSequenceEmpty.set(false);

			try {
				localStorage.setItem('start_position', JSON.stringify(startPosCopy));
			} catch (error) {
				console.error('Failed to save start position to localStorage:', error);
			}

			if (browser) {
				const customEvent = new CustomEvent('start-position-selected', {
					detail: {
						startPosition: startPosCopy,
						isTransitioning: true
					},
					bubbles: true
				});

				document.dispatchEvent(customEvent);

				// Provide success haptic feedback when the start position is successfully set
				hapticFeedbackService.trigger('success');

				// Note: We don't reset the loading state here because we want it to persist
				// during the transition to the OptionPicker. The OptionPicker will reset it
				// when it's done loading.
			}
		} catch (error) {
			console.error('Error adding start position:', error);
		}
	};
</script>

<div class="start-pos-picker">
	{#if isLoading}
		<div class="loading-container">
			<LoadingSpinner size="large" />
			<p class="loading-text">Loading Start Positions...</p>
		</div>
	{:else if loadingError}
		<div class="error-container">
			<p>Unable to load start positions. Please try refreshing the page.</p>
			<button
				on:click={() => {
					if (browser) window.location.reload();
				}}>Refresh</button
			>
		</div>
	{:else if !filteredDataAvailable}
		<div class="error-container">
			<p>No valid start positions found for the current configuration.</p>
		</div>
	{:else}
		<div class="pictograph-row">
			{#each startPositionPictographs as pictograph (pictograph.letter + '_' + pictograph.startPos + '_' + pictograph.endPos)}
				<div
					class="pictograph-container"
					role="button"
					tabindex="0"
					on:click={() => {
						handleSelect(pictograph);
					}}
					on:keydown={(e) => {
						if (e.key === 'Enter' || e.key === ' ') {
							e.preventDefault();
							handleSelect(pictograph);
						}
					}}
				>
					<Pictograph pictographData={pictograph} showLoadingIndicator={false} debug={true} />
				</div>
			{/each}
		</div>
	{/if}

	<!-- Loading overlay that appears during transition -->
	<LoadingOverlay visible={isTransitioning} message="Loading options..." transitionDuration={200} />
</div>

<style>
	.start-pos-picker {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		height: 100%;
		width: 100%;
		min-height: 300px;
		padding: 20px 0;
		position: relative; /* Required for absolute positioning of the loading overlay */
	}

	.loading-container {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		height: 100%;
		width: 100%;
		flex: 1;
	}

	.loading-text {
		margin-top: 20px;
		font-size: 1.2rem;
		color: #555;
		animation: pulse 1.5s infinite ease-in-out;
	}

	@keyframes pulse {
		0% {
			opacity: 0.6;
		}
		50% {
			opacity: 1;
		}
		100% {
			opacity: 0.6;
		}
	}

	.error-container {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		height: 100%;
		width: 100%;
		background-color: rgba(255, 220, 220, 0.7);
		padding: 20px;
		border-radius: 10px;
		flex: 1;
	}

	.pictograph-row {
		display: flex;
		flex-direction: row;
		justify-content: space-around;
		align-items: center;
		width: 90%;
		gap: 3%;
		margin: auto;
		flex: 0 0 auto;
		padding: 2rem 0;
	}

	.pictograph-container {
		width: 25%;
		aspect-ratio: 1 / 1;
		height: auto;
		position: relative;
		cursor: pointer;
		transition: transform 0.2s ease-in-out;
	}

	.pictograph-container:hover {
		transform: scale(1.05);
	}
</style>
