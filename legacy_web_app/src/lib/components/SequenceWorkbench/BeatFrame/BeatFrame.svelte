<script lang="ts">
	import { onMount } from 'svelte';
	import { useResizeObserver } from '$lib/composables/useResizeObserver';
	import { defaultPictographData } from '$lib/components/Pictograph/utils/defaultPictographData';
	import { autoAdjustLayout, calculateCellSize } from './beatFrameHelpers';
	import { selectedStartPos } from '$lib/stores/sequence/selectionStore';
	import type { PictographData } from '$lib/types/PictographData';
	import type { BeatData as LegacyBeatData } from './BeatData';
	import { browser } from '$app/environment';
	import { layoutStore } from '$lib/stores/layout/layoutStore';
	import { createEventDispatcher, setContext } from 'svelte';

	// Import the sequence container and integration utilities
	import { sequenceContainer } from '$lib/state/stores/sequence/SequenceContainer';
	import { useContainer } from '$lib/state/core/svelte5-integration.svelte';
	import type { BeatFrameLayoutOptions } from '$lib/types/BeatFrameLayoutOptions'; // Added import
	import { BEAT_FRAME_CONTEXT_KEY } from '../context/ElementContext';

	// Helper function for safe logging of reactive state
	function safeLog(message: string, data: any) {
		if (import.meta.env.DEV) {
			// Use $state.snapshot to avoid Svelte 5 proxy warnings
			console.log(message, data instanceof Object ? $state.snapshot(data) : data);
		}
	}

	// Components
	import StartPosBeat from './StartPosBeat.svelte';
	import AnimatedBeat from './AnimatedBeat.svelte';
	import ReversalGlyph from './ReversalGlyph.svelte';
	import EmptyStartPosLabel from './EmptyStartPosLabel.svelte';
	import { isSequenceEmpty } from '$lib/state/machines/sequenceMachine/persistence';

	// Create event dispatcher for natural height changes and beat selection
	const dispatch = createEventDispatcher<{
		naturalheightchange: { height: number };
		beatselected: { beatId: string };
	}>();

	// Use Svelte 5 runes for reactive state
	const { size: sizeStore, resizeObserver } = useResizeObserver({
		width: browser ? window.innerWidth : 800,
		height: browser ? window.innerHeight : 600
	});

	// Convert the size store to a reactive value
	const size = $derived({
		width: $sizeStore?.width || 0,
		height: $sizeStore?.height || 0
	});

	// Use the sequence container with Svelte 5 runes
	const sequence = useContainer(sequenceContainer);

	// Props using Svelte 5 runes
	const {
		isScrollable = $bindable(false),
		layoutOverride = $bindable(null),
		elementReceiver = $bindable<(element: HTMLElement | null) => void>(() => {}), // Define with $bindable and default
		fullScreenMode = $bindable(false) // Add fullScreenMode prop
	} = $props<{
		isScrollable?: boolean;
		layoutOverride?: BeatFrameLayoutOptions | null;
		elementReceiver?: (element: HTMLElement | null) => void;
		fullScreenMode?: boolean; // Add to type definition
	}>();

	// We're using the shared context key from ElementContext.ts

	// Local state
	let startPosition = $state<PictographData | null>(null);
	let beatRows = $state(1);
	let beatCols = $state(1);
	let prevRows = $state(1);
	let prevCols = $state(1);
	let cellSize = $state(100);
	let naturalGridHeight = $state(0);

	// Derived values
	const beats = $derived(convertContainerBeatsToLegacyFormat(sequence.beats));
	const selectedBeatIds = $derived(sequence.selectedBeatIds);
	const selectedBeatIndex = $derived(
		selectedBeatIds.length > 0 ? beats.findIndex((beat) => beat.id === selectedBeatIds[0]) : -1
	);
	const beatCount = $derived(beats.length);

	// We don't need to track layout orientation locally
	// as it's already managed by the layoutStore

	// Subscribe to isSequenceEmpty store
	let sequenceIsEmpty = $state(true);
	$effect(() => {
		const unsubscribe = isSequenceEmpty.subscribe((value) => {
			sequenceIsEmpty = value;
		});

		return () => {
			unsubscribe();
		};
	});

	// Create start position beat data
	const startPosBeatData = $derived({
		beatNumber: 0,
		filled: !!startPosition,
		pictographData: startPosition || defaultPictographData
	});

	// Convert container beats to legacy BeatData format
	function convertContainerBeatsToLegacyFormat(containerBeats: any[]): LegacyBeatData[] {
		return containerBeats.map((beat) => {
			// Create a proper pictographData object from the container beat data
			const pictographData = {
				letter: beat.metadata?.letter || null,
				startPos: beat.metadata?.startPos || null,
				endPos: beat.metadata?.endPos || null,
				gridMode: beat.metadata?.gridMode || 'diamond',
				redPropData: beat.redPropData || null,
				bluePropData: beat.bluePropData || null,
				redMotionData: beat.redMotionData || null,
				blueMotionData: beat.blueMotionData || null,
				redArrowData: beat.redArrowData || null,
				blueArrowData: beat.blueArrowData || null,
				grid: beat.metadata?.grid || ''
			};

			return {
				id: beat.id,
				beatNumber: beat.number,
				filled: true, // Assume filled if it exists in the container
				pictographData,
				duration: 1, // Default duration
				metadata: beat.metadata
			} as LegacyBeatData;
		});
	}

	// Get the initial value from the selectedStartPos store
	onMount(() => {
		// One-time subscription to get the initial value
		const unsubscribe = selectedStartPos.subscribe((newStartPos) => {
			if (newStartPos && !startPosition) {
				// Create a deep copy to avoid reference issues
				startPosition = JSON.parse(JSON.stringify(newStartPos));
				// Log using our safe logging helper (only in dev mode)
				safeLog('BeatFrame: Initialized startPosition with:', startPosition);
			}
		});

		// Immediately unsubscribe to prevent further updates
		unsubscribe();
	});

	// Calculate layout based on beat count
	$effect(() => {
		// Always ensure at least one row for the start position beat
		[beatRows, beatCols] = autoAdjustLayout(Math.max(1, beatCount));

		// Check if the layout has changed
		if (beatRows !== prevRows || beatCols !== prevCols) {
			// Log layout changes
			safeLog(`Layout changed`, { from: `${prevRows}x${prevCols}`, to: `${beatRows}x${beatCols}` });

			// Update the layout store
			layoutStore.updateLayout(beatRows, beatCols, beatCount);

			// Update previous values
			prevRows = beatRows;
			prevCols = beatCols;

			// Dispatch a custom event for layout changes
			const event = new CustomEvent('layout-changed', {
				bubbles: true,
				detail: {
					rows: beatRows,
					cols: beatCols,
					beatCount,
					previousLayout: { rows: prevRows, cols: prevCols }
				}
			});
			document.dispatchEvent(event);

			// Check for overflow after layout changes
			// Delay to ensure DOM is updated
			setTimeout(checkForOverflow, 100);
		}
	});

	// Track the full sequence widget dimensions
	let sequenceWidgetWidth = $state(0);
	let sequenceWidgetHeight = $state(0);

	// Track container reference
	let beatFrameContainerRef: HTMLElement;

	// Listen for sequence widget dimensions
	let sequenceWidgetDimensionsListener: (event: CustomEvent) => void;

	// Calculate natural grid height
	$effect(() => {
		const gridElement = beatFrameContainerRef?.querySelector('.beat-frame');
		if (gridElement) {
			naturalGridHeight = gridElement.scrollHeight; // Use scrollHeight for the most accurate content height

			// Log natural height in dev mode
			safeLog('Natural grid height calculated', {
				naturalGridHeight,
				beatRows,
				cellSize,
				element: 'scrollHeight'
			});
		} else {
			// Fallback calculation if element not ready
			naturalGridHeight = beatRows * cellSize + 20; // Add padding-bottom (20px) of the .beat-frame

			// Log fallback calculation in dev mode
			safeLog('Natural grid height calculated (fallback)', {
				naturalGridHeight,
				beatRows,
				cellSize,
				element: 'fallback calculation'
			});
		}
	});

	// Dispatch natural height change event
	$effect(() => {
		if (naturalGridHeight > 0 && beatFrameContainerRef) {
			// Dispatch the event using Svelte's event dispatcher
			dispatch('naturalheightchange', { height: naturalGridHeight });

			// Log event dispatch in dev mode
			safeLog('Dispatched naturalheightchange event', {
				height: naturalGridHeight
			});
		}
	});

	// Create a reactive state for the element reference
	let beatFrameElementState = $state<HTMLElement | null>(null);

	// This effect ensures the element reference is passed to the parent component
	// whenever the container element or the elementReceiver function changes
	$effect(() => {
		if (beatFrameContainerRef) {
			console.log('BeatFrame: Container element available');

			// Update our reactive state
			beatFrameElementState = beatFrameContainerRef;

			// Set the context for other components to access
			setContext(BEAT_FRAME_CONTEXT_KEY, {
				getElement: () => beatFrameElementState
			});

			// Store the element in global variables for fallback mechanisms
			if (browser) {
				// Store in both variables for maximum compatibility
				(window as any).__beatFrameElementRef = beatFrameContainerRef;
				(window as any).__pendingBeatFrameElement = beatFrameContainerRef;
				console.log('BeatFrame: Element stored in global fallback variables');
			}

			// Make sure elementReceiver is a function before calling it
			if (typeof elementReceiver === 'function') {
				try {
					// Call the receiver function
					elementReceiver(beatFrameContainerRef);
					console.log('BeatFrame: Element passed to receiver:', beatFrameContainerRef);
				} catch (error) {
					console.error('BeatFrame: Error calling elementReceiver:', error);
				}
			} else {
				console.error('BeatFrame: elementReceiver is not a function:', elementReceiver);
			}

			// Dispatch a custom event as a reliable fallback mechanism
			if (browser) {
				const event = new CustomEvent('beatframe-element-available', {
					bubbles: true,
					detail: { element: beatFrameContainerRef }
				});
				document.dispatchEvent(event);
				console.log('BeatFrame: Dispatched beatframe-element-available event');
			}
		} else {
			console.log('BeatFrame: Container element not yet available');
			beatFrameElementState = null;
		}
	});

	// Add a MutationObserver to ensure the element is passed even after DOM changes
	onMount(() => {
		if (browser) {
			// Track last update time to debounce frequent updates
			let lastUpdateTime = 0;
			const debounceInterval = 500; // Only update once every 500ms
			let lastElementRef: HTMLElement | null = null;

			// Set up a MutationObserver to detect when the element is added to the DOM
			const observer = new MutationObserver((_mutations) => {
				// Skip if container ref doesn't exist
				if (!beatFrameContainerRef) return;

				// Skip if element hasn't changed
				if (lastElementRef === beatFrameContainerRef) return;

				// Implement debouncing to prevent rapid consecutive calls
				const now = Date.now();
				if (now - lastUpdateTime < debounceInterval) return;

				// Update tracking variables
				lastUpdateTime = now;
				lastElementRef = beatFrameContainerRef;

				// Only log in development mode
				if (import.meta.env.DEV) {
					safeLog('BeatFrame: DOM mutation detected, updating element reference', {});
				}

				// Update our reactive state
				beatFrameElementState = beatFrameContainerRef;

				// Store in global variables for maximum compatibility
				(window as any).__beatFrameElementRef = beatFrameContainerRef;
				(window as any).__pendingBeatFrameElement = beatFrameContainerRef;

				// Make sure elementReceiver is a function before calling it
				if (typeof elementReceiver === 'function') {
					try {
						// Call the receiver function
						elementReceiver(beatFrameContainerRef);
					} catch (error) {
						console.error('BeatFrame: Error calling elementReceiver after DOM mutation:', error);
					}
				}

				// Dispatch a custom event as a reliable fallback mechanism
				const event = new CustomEvent('beatframe-element-available', {
					bubbles: true,
					detail: { element: beatFrameContainerRef }
				});
				document.dispatchEvent(event);
			});

			// Start observing only the parent container of the beat frame
			// This is more targeted than observing the entire document body
			if (beatFrameContainerRef && beatFrameContainerRef.parentElement) {
				observer.observe(beatFrameContainerRef.parentElement, {
					childList: true,
					subtree: false // Only watch direct children
				});
			} else {
				// Fallback to a more limited observation of document.body
				observer.observe(document.body, {
					childList: true,
					subtree: false // Limit depth to reduce overhead
				});
			}

			return () => {
				// Clean up the observer when the component is destroyed
				observer.disconnect();
			};
		}
	});

	onMount(() => {
		// Create a listener for the sequence-widget-dimensions event
		sequenceWidgetDimensionsListener = (event: CustomEvent) => {
			if (event.detail && event.detail.width && event.detail.height) {
				sequenceWidgetWidth = event.detail.width;
				sequenceWidgetHeight = event.detail.height;
			}
		};

		// Add the event listener
		document.addEventListener(
			'sequence-widget-dimensions',
			sequenceWidgetDimensionsListener as EventListener
		);

		return () => {
			// Remove the event listener when the component is destroyed
			document.removeEventListener(
				'sequence-widget-dimensions',
				sequenceWidgetDimensionsListener as EventListener
			);
		};
	});

	// Calculate cell size based on the full sequence widget dimensions
	$effect(() => {
		// Only calculate if we have valid dimensions
		if (sequenceWidgetWidth > 0 && sequenceWidgetHeight > 0) {
			// Use the full sequence widget height instead of the beat frame's height
			cellSize = calculateCellSize(
				beatCount,
				sequenceWidgetWidth,
				sequenceWidgetHeight,
				beatRows,
				beatCols + 1, // Add 1 for start position column
				0 // No gap
			);
		} else {
			// Fallback to using the beat frame's dimensions if sequence widget dimensions aren't available
			cellSize = calculateCellSize(
				beatCount,
				size.width,
				size.height,
				beatRows,
				beatCols + 1, // Add 1 for start position column
				0 // No gap
			);
		}

		// Check for overflow after cell size is calculated
		// This needs to be delayed to ensure DOM is updated
		setTimeout(checkForOverflow, 50);
	});

	// Function to check if content overflows container - for debugging only
	function checkForOverflow() {
		if (!beatFrameContainerRef) return;

		const container = beatFrameContainerRef;
		const beatFrame = container.querySelector('.beat-frame');

		if (!beatFrame) return;

		// Check if content is larger than container
		const containerHeight = container.clientHeight;
		const contentHeight = beatFrame.clientHeight;
		const containerWidth = container.clientWidth;
		const contentWidth = beatFrame.clientWidth;

		// Add a small buffer to prevent flickering at the boundary
		const buffer = 10; // 10px buffer

		// Calculate overflow - check both height and width
		const heightOverflow = contentHeight > containerHeight + buffer;
		const widthOverflow = contentWidth > containerWidth + buffer;

		// Log overflow state in dev mode
		safeLog('Overflow check', {
			containerHeight,
			contentHeight,
			containerWidth,
			contentWidth,
			heightOverflow,
			widthOverflow,
			isScrollable: isScrollable, // Corrected: Use destructured prop
			beatRows,
			beatCols,
			beatCount
		});
	}

	// Initialize dev tools and set up event listeners
	onMount(() => {
		// Initialize dev tools updater

		// Listen for the custom event when a start position is selected
		const handleStartPosSelected = (event: CustomEvent) => {
			if (event.detail?.startPosition) {
				// Log the received start position (only in dev mode)
				safeLog(
					'BeatFrame: Received start-position-selected event with data:',
					event.detail.startPosition
				);

				// Create a deep copy to avoid reference issues
				const newStartPos = JSON.parse(JSON.stringify(event.detail.startPosition));

				// Update the local state
				startPosition = newStartPos;

				// Update the store (but don't subscribe to its changes to avoid loops)
				selectedStartPos.set(newStartPos);
			}
		};

		document.addEventListener('start-position-selected', handleStartPosSelected as EventListener);

		// Check for overflow after component is mounted
		// Delay to ensure DOM is fully rendered
		setTimeout(checkForOverflow, 200);

		// Add window resize listener to check for overflow on window resize
		const handleResize = () => {
			setTimeout(checkForOverflow, 100);
		};
		window.addEventListener('resize', handleResize);

		// Set up an interval to periodically update dev tools
		const intervalId = setInterval(() => {}, 1000);

		return () => {
			document.removeEventListener(
				'start-position-selected',
				handleStartPosSelected as EventListener
			);
			window.removeEventListener('resize', handleResize);
			clearInterval(intervalId);
		};
	});

	// Event handlers
	function handleStartPosBeatClick() {
		// Deselect current beat - clear all selections

		// Dispatch a custom event to trigger the start position selector
		// Create a deep copy of startPosition to avoid reference issues
		const startPosCopy = startPosition ? JSON.parse(JSON.stringify(startPosition)) : null;

		const event = new CustomEvent('select-start-pos', {
			bubbles: true,
			detail: { currentStartPos: startPosCopy }
		});
		document.dispatchEvent(event);
	}

	function handleBeatClick(beatIndex: number) {
		// Get the beat ID from the index
		if (beatIndex >= 0 && beatIndex < beats.length) {
			const beat = beats[beatIndex];
			const beatId = beat.id;

			// Log detailed information about the beat being selected
			safeLog('Selecting beat', {
				index: beatIndex,
				beatNumber: beat.beatNumber,
				id: beatId,
				gridLayout: `${beatRows}x${beatCols}`,
				position: {
					row: Math.floor(beatIndex / beatCols) + 1,
					col: (beatIndex % beatCols) + 1
				},
				motionTypes: {
					red: beat.pictographData?.redMotionData?.motionType || 'none',
					blue: beat.pictographData?.blueMotionData?.motionType || 'none'
				}
			});

			if (beatId) {
				// Select the beat in the container
				sequenceContainer.selectBeat(beatId);

				// Dispatch a custom event for the beat selection
				// This will be used by the deletion mode
				dispatch('beatselected', { beatId });

				// Also dispatch a global event for components that aren't direct parents
				const event = new CustomEvent('beat-selected', {
					bubbles: true,
					detail: { beatId }
				});
				document.dispatchEvent(event);
			}
		}
	}

	// Public methods that can be called from parent components
	export function addBeat(beatData: LegacyBeatData) {
		// Ensure the beat has an ID
		const beatWithId = beatData.id ? beatData : { ...beatData, id: crypto.randomUUID() };

		// Convert from legacy BeatData to container BeatData format
		const containerBeat = {
			id: beatWithId.id || crypto.randomUUID(), // Ensure ID is never undefined
			number: beatWithId.beatNumber,
			redPropData: beatWithId.pictographData.redPropData,
			bluePropData: beatWithId.pictographData.bluePropData,
			redMotionData: beatWithId.pictographData.redMotionData,
			blueMotionData: beatWithId.pictographData.blueMotionData,
			redArrowData: beatWithId.pictographData.redArrowData,
			blueArrowData: beatWithId.pictographData.blueArrowData,
			metadata: {
				...beatWithId.metadata,
				letter: beatWithId.pictographData.letter,
				startPos: beatWithId.pictographData.startPos,
				endPos: beatWithId.pictographData.endPos,
				gridMode: beatWithId.pictographData.gridMode
			}
		};

		// Add the beat to the sequence container
		sequenceContainer.addBeat(containerBeat as any); // Use type assertion to bypass TypeScript error
	}

	// Add a method to clear beats (could be called from parent)
	export function clearBeats() {
		// Use the sequence container to clear the sequence
		sequenceContainer.setSequence([]);
	}

	// Add a test method to verify persistence
	export function testPersistence() {
		// Log the current state
		console.log('Current sequence state:', {
			beats: sequence.beats.length,
			startPosition: startPosition ? 'set' : 'not set'
		});

		// Check localStorage
		if (browser) {
			const savedSequence = localStorage.getItem('sequence');
			const startPosData = localStorage.getItem('start_position');
			const backupData = localStorage.getItem('sequence_backup');

			console.log('localStorage state:', {
				sequence: savedSequence ? 'found' : 'not found',
				startPosition: startPosData ? 'found' : 'not found',
				backup: backupData ? 'found' : 'not found'
			});

			if (savedSequence) {
				try {
					const parsed = JSON.parse(savedSequence);
					console.log('Saved sequence contains:', {
						beats: parsed.beats?.length || 0,
						metadata: parsed.metadata ? 'present' : 'missing'
					});
				} catch (e) {
					console.error('Error parsing saved sequence:', e);
				}
			}
		}

		// Force a save
		sequenceContainer.saveToLocalStorage();
		console.log('Forced save to localStorage');

		return {
			success: true,
			message: 'Persistence test complete. Check console for details.'
		};
	}
</script>

<div
	use:resizeObserver
	class="beat-frame-container"
	class:scrollable-active={isScrollable}
	class:fullscreen-mode={fullScreenMode}
	bind:this={beatFrameContainerRef}
>
	<div
		class="beat-frame"
		style="--total-rows: {beatRows}; --total-cols: {beatCount === 0
			? 1
			: beatCols + 1}; --cell-size: {cellSize}px;"
	>
		{#each Array(beatRows) as _, rowIndex}
			{#if rowIndex === 0}
				<div class="beat-container start-position" style="grid-row: 1; grid-column: 1;">
					{#if sequenceIsEmpty}
						<EmptyStartPosLabel onClick={handleStartPosBeatClick} />
					{:else}
						<StartPosBeat beatData={startPosBeatData} onClick={handleStartPosBeatClick} />
					{/if}
				</div>
			{/if}

			{#each Array(beatCols) as _, colIndex}
				{#if rowIndex * beatCols + colIndex < beats.length}
					{@const beatIndex = rowIndex * beatCols + colIndex}
					{@const beat = beats[beatIndex]}

					{#key beat.id}
						<div
							class="beat-container"
							class:selected={selectedBeatIndex === beatIndex}
							style="grid-row: {rowIndex + 1}; grid-column: {colIndex + (beatCount === 0 ? 1 : 2)};"
						>
							<AnimatedBeat
								{beat}
								onClick={() => handleBeatClick(beatIndex)}
								isSelected={selectedBeatIndex === beatIndex}
							/>

							{#if beat.metadata?.blueReversal || beat.metadata?.redReversal}
								<div class="reversal-indicator">
									<ReversalGlyph
										blueReversal={beat.metadata?.blueReversal || false}
										redReversal={beat.metadata?.redReversal || false}
									/>
								</div>
							{/if}
						</div>
					{/key}
				{/if}
			{/each}
		{/each}
	</div>
</div>

<style>
	.beat-frame-container {
		width: 100%;
		/* height will be 'auto' by default, or '100%' when scrollable */
		height: auto;
		display: flex;
		justify-content: center;
		align-items: center; /* Default alignment */
		position: relative;
		transition: all 0.3s ease-out;
		overflow: visible; /* Default */
		/* Add margin auto to help with vertical centering */
		margin: auto;
	}

	/* Apply scrolling only when needed */
	.beat-frame-container.scrollable-active {
		height: 100%; /* Fill the constrained height from SequenceWidget */
		overflow-y: auto !important;
		overflow-x: hidden;
		scrollbar-width: thin; /* For Firefox */
		scrollbar-color: rgba(0, 0, 0, 0.3) transparent; /* For Firefox */
		align-items: flex-start !important; /* Pin to top when scrolling */
		padding-right: 8px; /* Space for scrollbar */
		/* Remove auto margins in scroll mode */
		margin: 0;
	}

	/* Webkit scrollbar styling */
	.beat-frame-container.scrollable-active::-webkit-scrollbar {
		width: 8px;
		height: 8px;
	}

	.beat-frame-container.scrollable-active::-webkit-scrollbar-track {
		background: transparent;
	}

	.beat-frame-container.scrollable-active::-webkit-scrollbar-thumb {
		background-color: rgba(0, 0, 0, 0.3);
		border-radius: 4px;
	}

	/* Apply different alignment for scrollable containers */
	.beat-frame-container.scrollable-active {
		/* Align to top when scrolling is needed */
		align-items: flex-start;
		justify-content: center;
		/* Add padding to ensure content isn't cut off */
		padding: 10px 0;
	}

	.beat-frame {
		display: grid;
		grid-template-columns: repeat(var(--total-cols), var(--cell-size));
		grid-template-rows: repeat(var(--total-rows), var(--cell-size));
		gap: 0; /* No gap between cells */
		justify-content: center;
		align-content: center; /* Center by default for short sequences */
		width: fit-content;
		height: fit-content; /* Default for non-scrolling */
		margin: auto; /* Default for centering */
		transition: all 0.3s ease-out;
		/* Add padding that respects safe area insets */
		padding: 0 calc(var(--safe-inset-right, 0px)) calc(20px + var(--safe-inset-bottom, 0px))
			calc(var(--safe-inset-left, 0px));
		transform-origin: center center;
	}

	/* Only apply scrolling styles when parent is scrollable */
	.beat-frame-container.scrollable-active .beat-frame {
		margin-top: 0;
		margin-bottom: 0; /* Remove auto margins */
		align-content: flex-start; /* Align grid items to the top */
	}

	/* For short sequences in non-scrollable containers, maintain centering */
	.beat-frame-container:not(.scrollable-active) .beat-frame {
		margin: auto; /* Center when content fits */
	}

	/* Fullscreen mode styles */
	.beat-frame-container.fullscreen-mode {
		height: 100%;
		width: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
		overflow: visible;
		margin: 0;
		padding: 20px;
		box-sizing: border-box;
	}

	.beat-frame-container.fullscreen-mode .beat-frame {
		transform: scale(1.2); /* Make the beat frame larger in fullscreen mode */
		margin: auto;
	}

	.beat-container {
		position: relative;
		width: var(--adjusted-cell-size, var(--cell-size));
		height: var(--adjusted-cell-size, var(--cell-size));
		display: flex;
		justify-content: center;
		align-items: center;
		background-color: transparent;
		/* Add transition for smooth size changes */
		transition:
			width 0.3s ease,
			height 0.3s ease;
		/* Ensure content is properly centered */
		box-sizing: border-box;
		/* Prevent overflow */
		overflow: hidden;
	}

	/* Specific styling for start position when it's the only beat */
	.beat-container.start-position:only-child {
		justify-self: center;
		align-self: center;
	}

	.reversal-indicator {
		position: absolute;
		bottom: 5px;
		right: 5px;
		z-index: 2;
	}
</style>
