<script lang="ts">
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import Pictograph from '$lib/components/Pictograph/Pictograph.svelte';
	import { sequenceContainer } from '$lib/state/stores/sequence/SequenceContainer';
	import { selectedStartPos } from '$lib/stores/sequence/selectionStore';
	import type { PictographData } from '$lib/types/PictographData';
	import { autoAdjustLayout } from '../BeatFrame/beatFrameHelpers';

	// Props
	const { title = $bindable('') } = $props<{
		title?: string;
	}>();

	// Local state
	let gridRef: HTMLDivElement;
	let viewportWidth = $state(window.innerWidth);
	let viewportHeight = $state(window.innerHeight);
	let startPosition = $state<PictographData | null>(null);
	let rows = $state(1);
	let cols = $state(1);
	let cellSize = $state(120);
	let gridScale = $state(1);
	let rotationMessage = $state<string | null>(null);
	let showRotationIndicator = $state(false);

	// Get the beats from the sequence container
	const beats = $derived(sequenceContainer.state.beats);
	const beatCount = $derived(beats.length);

	// Initialize viewport dimensions and start position
	onMount(() => {
		// Initialize viewport dimensions
		viewportWidth = window.innerWidth;
		viewportHeight = window.innerHeight;

		// Get the start position from the store
		const unsubscribe = selectedStartPos.subscribe((newStartPos) => {
			if (newStartPos) {
				startPosition = JSON.parse(JSON.stringify(newStartPos));
			}
		});

		// Immediately unsubscribe to prevent further updates
		unsubscribe();

		// Add window resize and orientation change listeners
		const handleResize = () => {
			viewportWidth = window.innerWidth;
			viewportHeight = window.innerHeight;
			updateLayout();
		};

		// Listen for screen orientation changes (mobile-specific)
		let orientationChangeHandler: EventListener | null = null;
		if (typeof window !== 'undefined' && window.screen && window.screen.orientation) {
			orientationChangeHandler = () => {
				viewportWidth = window.innerWidth;
				viewportHeight = window.innerHeight;
				updateLayout();
			};
			window.screen.orientation.addEventListener('change', orientationChangeHandler);
		}

		window.addEventListener('resize', handleResize);
		window.addEventListener('orientationchange', handleResize);

		// Initial layout calculation
		updateLayout();

		return () => {
			window.removeEventListener('resize', handleResize);
			window.removeEventListener('orientationchange', handleResize);

			if (orientationChangeHandler && window.screen && window.screen.orientation) {
				window.screen.orientation.removeEventListener('change', orientationChangeHandler);
			}
		};
	});

	// Calculate optimal layout based on sequence data and viewport dimensions
	function updateLayout() {
		// Determine if we have a start position
		const hasStartPosition = !!startPosition;

		// Calculate rows and columns based on beat count
		const [baseRows, baseCols] = autoAdjustLayout(beatCount);

		// Special case: If we have only a start position with no beats, use a 1x1 grid
		if (hasStartPosition && beatCount === 0) {
			rows = 1;
			cols = 1;
		}
		// Adjust layout for start position if needed for sequences with beats
		else if (hasStartPosition) {
			// Add one column for the start position
			cols = baseCols + 1;

			// Calculate how many rows we need when beats are arranged in columns 2 and onwards
			const beatsPerRow = baseCols;
			rows = Math.ceil(beatCount / beatsPerRow);
		} else {
			rows = baseRows;
			cols = baseCols;
		}

		// Determine device orientation
		let deviceOrientation: 'landscape' | 'portrait' = 'landscape';

		// Check for screen orientation API first (more reliable on mobile)
		if (typeof window !== 'undefined' && window.screen && window.screen.orientation) {
			const orientation = window.screen.orientation.type;
			if (orientation.includes('portrait')) {
				deviceOrientation = 'portrait';
			} else if (orientation.includes('landscape')) {
				deviceOrientation = 'landscape';
			}
		} else {
			// Fallback to comparing dimensions
			deviceOrientation = viewportWidth > viewportHeight ? 'landscape' : 'portrait';
		}

		// Get safe area insets from CSS variables
		const safeInsetTop = parseFloat(
			getComputedStyle(document.documentElement).getPropertyValue('--safe-inset-top') || '0px'
		);
		const safeInsetRight = parseFloat(
			getComputedStyle(document.documentElement).getPropertyValue('--safe-inset-right') || '0px'
		);
		const safeInsetBottom = parseFloat(
			getComputedStyle(document.documentElement).getPropertyValue('--safe-inset-bottom') || '0px'
		);
		const safeInsetLeft = parseFloat(
			getComputedStyle(document.documentElement).getPropertyValue('--safe-inset-left') || '0px'
		);

		// Calculate available space (95% of viewport width, 90% of viewport height) accounting for safe area insets
		const availableWidth = (viewportWidth - safeInsetLeft - safeInsetRight) * 0.95;
		const availableHeight = (viewportHeight - safeInsetTop - safeInsetBottom) * 0.9; // Leave room for header/footer

		// Calculate optimal cell size
		const maxCellWidth = availableWidth / cols;
		const maxCellHeight = availableHeight / rows;
		cellSize = Math.min(maxCellWidth, maxCellHeight);

		// Calculate grid dimensions
		const gridWidth = cellSize * cols;
		const gridHeight = cellSize * rows;

		// No rotation - natural orientation is maintained

		// Calculate scale factor to ensure content fits within viewport
		// No rotation, use original dimensions
		// Ensure dimensions don't exceed viewport
		if (gridWidth > availableWidth || gridHeight > availableHeight) {
			const scaleX = availableWidth / gridWidth;
			const scaleY = availableHeight / gridHeight;
			gridScale = Math.min(scaleX, scaleY) * 0.98; // Add small safety margin
		} else {
			gridScale = 1;
		}

		// Check for mobile devices with unusual aspect ratios
		const isMobile =
			typeof window !== 'undefined' && ('ontouchstart' in window || navigator.maxTouchPoints > 0);

		const isNarrowScreen =
			typeof window !== 'undefined' && viewportWidth < 500 && viewportHeight > 700;

		// Still provide rotation guidance for better viewing experience
		// but don't actually rotate the content
		const isLandscapeContent = cols > rows;
		const isPortraitDevice = deviceOrientation === 'portrait';

		// Show rotation indicator when content orientation doesn't match device orientation
		if (isLandscapeContent && isPortraitDevice) {
			rotationMessage = 'Rotate to landscape for optimal view';
			showRotationIndicator = true;
		} else if (!isLandscapeContent && !isPortraitDevice) {
			rotationMessage = 'Rotate to portrait for optimal view';
			showRotationIndicator = true;
		} else {
			rotationMessage = null;
			showRotationIndicator = false;
		}

		// Force rotation indicator on narrow mobile screens when content is landscape
		if (isMobile && isNarrowScreen && isLandscapeContent && isPortraitDevice) {
			rotationMessage = 'Rotate to landscape for optimal view';
			showRotationIndicator = true;
		}

		// Apply the layout to the grid
		if (gridRef) {
			// Set grid template
			gridRef.style.gridTemplateRows = `repeat(${rows}, ${cellSize}px)`;
			gridRef.style.gridTemplateColumns = `repeat(${cols}, ${cellSize}px)`;

			// Set transform for scaling only, no rotation
			gridRef.style.transform = `translate(-50%, -50%) scale(${gridScale})`;

			// Set CSS variables for use in styles
			gridRef.style.setProperty('--cell-size', `${cellSize}px`);
			gridRef.style.setProperty('--rows', `${rows}`);
			gridRef.style.setProperty('--cols', `${cols}`);
		}
	}

	// Get the position of a beat in the grid
	function getBeatPosition(index: number): { row: number; col: number } {
		const hasStartPosition = !!startPosition;

		// Special case: If we have only a start position with no beats (1x1 grid)
		if (hasStartPosition && beatCount === 0) {
			// In this case, there are no beats to position, but we'll return a default
			return { row: 0, col: 1 };
		} else if (hasStartPosition) {
			// When there's a start position, we need to adjust the layout
			// Beats should be arranged in columns 2 and onwards
			const beatsPerRow = cols - 1; // One less column for beats since column 1 is reserved
			const row = Math.floor(index / beatsPerRow);
			const col = (index % beatsPerRow) + 2; // +2 because column 1 is reserved for start position
			return { row, col };
		} else {
			// Standard layout without start position - use all columns
			const row = Math.floor(index / cols);
			const col = (index % cols) + 1; // +1 for 1-based column index
			return { row, col };
		}
	}
</script>

<div class="fullscreen-overlay-container fullscreen-beat-container" data-beat-count={beatCount}>
	<!-- Rotation indicator -->
	{#if showRotationIndicator}
		<div class="rotation-indicator" transition:fade={{ duration: 300 }}>
			<div class="rotation-message">
				<svg class="rotation-icon" viewBox="0 0 24 24" width="20" height="20">
					<path
						d="M7.11 8.53L5.7 7.11C4.8 8.27 4.24 9.61 4.07 11h2.02c.14-.87.49-1.72 1.02-2.47zM6.09 13H4.07c.17 1.39.72 2.73 1.62 3.89l1.41-1.42c-.52-.75-.87-1.59-1.01-2.47zm1.01 5.32c1.16.9 2.51 1.44 3.9 1.61V17.9c-.87-.15-1.71-.49-2.46-1.03L7.1 18.32zM13 4.07V1L8.45 5.55 13 10V6.09c2.84.48 5 2.94 5 5.91s-2.16 5.43-5 5.91v2.02c3.95-.49 7-3.85 7-7.93s-3.05-7.44-7-7.93z"
					/>
				</svg>
				<span>{rotationMessage}</span>
			</div>
		</div>
	{/if}

	<!-- Sequence grid -->
	<div class="sequence-grid" bind:this={gridRef}>
		<!-- Start position (if available) -->
		{#if startPosition}
			<div class="grid-item start-position">
				<div class="pictograph-container">
					<Pictograph pictographData={startPosition} isStartPosition={true} />
				</div>
			</div>
		{/if}

		<!-- Regular beats -->
		{#each beats as beat, index}
			{@const position = getBeatPosition(index)}
			<div class="grid-item" style="grid-column: {position.col}; grid-row: {position.row + 1};">
				<div class="pictograph-container">
					<Pictograph
						pictographData={{
							letter: beat.metadata?.letter || null,
							startPos: beat.metadata?.startPos || null,
							endPos: beat.metadata?.endPos || null,
							gridMode: (beat.metadata?.gridMode || 'diamond') as any,
							redPropData: beat.redPropData || null,
							bluePropData: beat.bluePropData || null,
							redMotionData: beat.redMotionData || null,
							blueMotionData: beat.blueMotionData || null,
							redArrowData: beat.redArrowData || null,
							blueArrowData: beat.blueArrowData || null,
							grid: (beat.metadata?.grid || '') as string
						} as any}
						beatNumber={index + 1}
					/>
				</div>
			</div>
		{/each}
	</div>
</div>

<style>
	/* Fullscreen overlay container */

	/* Sequence grid */
	.sequence-grid {
		display: grid;
		gap: 0;
		position: absolute;
		transform-origin: center center;
		box-sizing: border-box;
	}

	/* Grid items */
	.grid-item {
		position: relative;
		width: 100%;
		height: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
		overflow: hidden;
	}

	/* Special styling for start position - only in top-left cell */
	.grid-item.start-position {
		grid-column: 1;
		grid-row: 1;
		width: var(--cell-size, 100%);
		height: var(--cell-size, 100%);
	}

	/* Pictograph container */
	.pictograph-container {
		width: 100%;
		height: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
		padding: 0;
		box-sizing: border-box;
	}

	/* Style for pictograph components */
	:global(.pictograph-container .pictograph) {
		width: 100%;
		height: 100%;
		max-width: 100%;
		max-height: 100%;
		border: none;
	}

	/* Rotation indicator */
	.rotation-indicator {
		position: absolute;
		bottom: max(16px, var(--safe-inset-bottom, 16px));
		left: 0;
		right: 0;
		z-index: 10;
		display: flex;
		justify-content: center;
		pointer-events: none;
		transition: opacity 0.3s ease-out;
	}

	.rotation-message {
		background-color: rgba(0, 0, 0, 0.5);
		color: white;
		padding: 8px 12px;
		border-radius: 16px;
		display: flex;
		align-items: center;
		gap: 6px;
		font-size: 12px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
		animation: pulse 3s infinite;
		backdrop-filter: blur(2px);
		max-width: 90%;
	}

	.rotation-icon {
		fill: white;
		animation: rotate 3s infinite;
		opacity: 0.9;
	}

	@keyframes pulse {
		0% {
			opacity: 0.7;
		}
		50% {
			opacity: 0.9;
		}
		100% {
			opacity: 0.7;
		}
	}

	@keyframes rotate {
		0% {
			transform: rotate(0deg);
		}
		20% {
			transform: rotate(45deg);
		}
		40% {
			transform: rotate(45deg);
		}
		60% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(0deg);
		}
	}

	/* Mobile-specific styles */
	@media (max-width: 480px) {
		.rotation-message {
			font-size: 10px;
			padding: 6px 10px;
			border-radius: 12px;
		}
	}

	/* Special handling for tall/narrow screens like Z Fold */
	@media (max-width: 400px) and (min-height: 800px) {
		.rotation-indicator {
			display: flex !important;
			opacity: 1 !important;
		}
	}
</style>
