<!-- src/lib/components/SequenceWorkbench/ToolsPanel/ToolsPanel.svelte -->
<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { fly } from 'svelte/transition';
	import type { ButtonDefinition } from '../ButtonPanel/types';

	// Props
	export let buttons: ButtonDefinition[] = [];
	export let activeMode: 'construct' | 'generate' | null = null;

	// Create event dispatcher
	const dispatch = createEventDispatcher<{
		action: { id: string };
	}>();

	// Handle button click directly
	function handleToolClick(id: string) {
		// Add a small vibration for tactile feedback on mobile devices
		if (navigator.vibrate) {
			navigator.vibrate(30);
		}

		// Log the action for debugging
		console.log(`ToolsPanel: Dispatching action for button ${id}`);

		// Dispatch the action event to the parent component ONLY
		// This prevents the circular reference that was causing infinite recursion
		dispatch('action', { id });
	}

	// Close tools panel
	function handleClose() {
		// Create and dispatch a custom event
		const event = new CustomEvent('close-tools-panel', {
			bubbles: true,
			composed: true
		});
		document.dispatchEvent(event);
	}

	// Organize buttons in logical groups with improved categorization
	const modeButtons = buttons.filter((b) => ['constructMode', 'generateMode'].includes(b.id));
	const sharingButtons = buttons.filter((b) => ['viewFullScreen', 'saveImage'].includes(b.id));
	const manipulationButtons = buttons.filter((b) =>
		['mirrorSequence', 'swapColors', 'rotateSequence'].includes(b.id)
	);
	const dictionaryButtons = buttons.filter((b) => ['addToDictionary'].includes(b.id));
	const destructiveButtons = buttons.filter((b) => ['deleteBeat', 'clearSequence'].includes(b.id));

	// Combine all buttons in a logical order
	const orderedButtons = [
		...modeButtons,
		...sharingButtons,
		...manipulationButtons,
		...dictionaryButtons,
		...destructiveButtons
	];

	let gridContainer: HTMLDivElement;

	// Debounce function to prevent too many layout updates
	function debounce<T extends (...args: any[]) => any>(
		func: T,
		wait: number
	): (...args: Parameters<T>) => void {
		let timeout: ReturnType<typeof setTimeout> | undefined;
		return function executedFunction(...args: Parameters<T>): void {
			const later = () => {
				clearTimeout(timeout);
				func(...args);
			};
			clearTimeout(timeout);
			timeout = setTimeout(later, wait);
		};
	}

	// Modern grid layout function with better calculations
	function updateGridLayout() {
		if (!gridContainer) return;

		const containerWidth = gridContainer.clientWidth;
		const containerHeight = gridContainer.clientHeight;
		const buttonCount = orderedButtons.length;

		// Determine gap and padding based on container size
		const gap = containerWidth < 480 ? 6 : containerWidth < 768 ? 8 : 12;
		const padding = containerWidth < 480 ? 4 : containerWidth < 768 ? 6 : 8;

		// Set these values as CSS variables
		gridContainer.style.setProperty('--grid-gap', `${gap}px`);
		gridContainer.style.setProperty('--grid-padding', `${padding}px`);

		// Calculate available space
		const availableWidth = containerWidth - padding * 2;
		const availableHeight = containerHeight - padding * 2;

		// Calculate the minimum number of columns needed based on button count
		// We need to ensure all buttons fit without overlapping
		const minButtonSize = 70; // Absolute minimum size for a button
		const maxButtonsPerRow = Math.floor(availableWidth / minButtonSize);

		// Calculate minimum columns needed to fit all buttons
		const minColumnsNeeded = Math.ceil(buttonCount / Math.floor(availableHeight / minButtonSize));

		// Calculate ideal columns based on container width and minimum button size
		// (This calculation is used for reference but not directly applied)

		// Determine final column count based on container dimensions and button count
		let columns;

		// For very small screens
		if (containerWidth < 320) {
			columns = Math.min(2, buttonCount);
		}
		// For mobile screens (target 3x3 layout if possible)
		else if (containerWidth < 600) {
			columns = Math.min(3, buttonCount, maxButtonsPerRow);
		}
		// For medium screens
		else if (containerWidth < 900) {
			columns = Math.min(4, buttonCount, maxButtonsPerRow);
		}
		// For large screens
		else {
			columns = Math.min(5, buttonCount, maxButtonsPerRow);
		}

		// Ensure we have at least the minimum columns needed
		columns = Math.max(columns, minColumnsNeeded);

		// Calculate rows needed based on final column count
		const rows = Math.ceil(buttonCount / columns);

		// Calculate available space per button, accounting for gaps
		// Subtract the total gap space from available dimensions
		const availableWidthForButtons = availableWidth - gap * (columns - 1);
		const availableHeightForButtons = availableHeight - gap * (rows - 1);

		// Calculate maximum button dimensions that would fit
		const maxButtonWidth = availableWidthForButtons / columns;
		const maxButtonHeight = availableHeightForButtons / rows;

		// Use the smaller dimension to ensure buttons fit and remain square
		// Floor the value to avoid fractional pixels
		let buttonSize = Math.floor(Math.min(maxButtonWidth, maxButtonHeight));

		// Set reasonable limits
		const minSize = 44; // Minimum touch target size for accessibility
		const maxSize = containerWidth < 600 ? 90 : 160; // Limit size based on screen

		// Ensure button size is within limits
		buttonSize = Math.max(minSize, Math.min(buttonSize, maxSize));

		// Set CSS variables for the grid
		gridContainer.style.setProperty('--button-size', `${buttonSize}px`);
		gridContainer.style.setProperty('--columns', `${columns}`);

		// Calculate and set icon and text sizes based on button size
		const iconSize = Math.max(18, Math.min(32, Math.floor(buttonSize * 0.4)));
		const titleSize = Math.max(9, Math.min(14, Math.floor(buttonSize * 0.15)));

		gridContainer.style.setProperty('--icon-size', `${iconSize}px`);
		gridContainer.style.setProperty('--title-size', `${titleSize}px`);

		// Set a flag for small screens to adjust layout
		const isSmallScreen = containerWidth < 480;
		gridContainer.classList.toggle('small-screen', isSmallScreen);

		// Set a flag for portrait/landscape orientation
		const isPortrait = containerWidth < containerHeight;
		gridContainer.classList.toggle('portrait', isPortrait);
		gridContainer.classList.toggle('landscape', !isPortrait);
	}

	// Create debounced version for better performance
	const debouncedUpdateLayout = debounce(updateGridLayout, 100);

	onMount(() => {
		// Initial layout calculation
		updateGridLayout();

		// Create a ResizeObserver with the debounced update function
		const resizeObserver = new ResizeObserver(() => {
			debouncedUpdateLayout();
		});

		// Observe the grid container for size changes
		if (gridContainer) {
			resizeObserver.observe(gridContainer);
		}

		// Also observe the parent container if possible
		const parentContainer = gridContainer?.parentElement;
		if (parentContainer) {
			resizeObserver.observe(parentContainer);
		}

		// Clean up on component destruction
		return () => {
			resizeObserver.disconnect();
		};
	});
</script>

<div class="tools-panel" transition:fly={{ y: 20, duration: 300 }}>
	<div class="tools-header">
		<h2>Tools</h2>
		<button class="close-button" on:click={handleClose} aria-label="Close tools panel"> ✕ </button>
	</div>

	<div class="tools-content">
		<div class="tools-grid" bind:this={gridContainer}>
			{#each orderedButtons as button}
				<button
					class="tool-button {button.id.includes('delete') || button.id.includes('clear')
						? 'destructive'
						: ''} {(button.id === 'constructMode' && activeMode === 'construct') ||
					(button.id === 'generateMode' && activeMode === 'generate')
						? 'active-mode'
						: ''}"
					on:click={() => handleToolClick(button.id)}
					style="--button-color: {button.color}"
					title={button.title}
					aria-label={button.title}
				>
					<i class="fa-solid {button.id === 'saveImage' ? 'fa-share-nodes' : button.icon}"></i>
					<span class="button-title">{button.title}</span>
				</button>
			{/each}
		</div>
	</div>
</div>

<style>
	.tools-panel {
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
		background: rgba(248, 249, 250, 0.2); /* Very subtle background */
		border-radius: 12px;
		box-shadow:
			0 4px 16px rgba(0, 0, 0, 0.1),
			0 0 0 1px rgba(255, 255, 255, 0.05);
		overflow: hidden;
		position: relative;
		flex: 1;
		backdrop-filter: blur(5px); /* Enhanced blur effect for the entire panel */
		-webkit-backdrop-filter: blur(5px);
	}

	.tools-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 12px 16px;
		background: linear-gradient(135deg, rgba(106, 17, 203, 0.9), rgba(37, 117, 252, 0.9));
		color: white;
		backdrop-filter: blur(8px); /* Enhanced blur effect for the header */
		-webkit-backdrop-filter: blur(8px);
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	}

	.tools-header h2 {
		margin: 0;
		font-size: 1.2rem;
		font-weight: 600;
		letter-spacing: 0.5px;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
	}

	.close-button {
		background: rgba(255, 255, 255, 0.2);
		border: none;
		border-radius: 50%;
		width: 32px;
		height: 32px;
		display: flex;
		justify-content: center;
		align-items: center;
		cursor: pointer;
		color: white;
		font-weight: bold;
		transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275); /* Bouncy animation */
		font-size: 14px;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
	}

	.close-button:hover {
		background: rgba(255, 255, 255, 0.4);
		transform: scale(1.1);
	}

	.close-button:active {
		transform: scale(0.95);
	}

	.tools-content {
		flex: 1;
		padding: 8px;
		display: flex;
		flex-direction: column;
		overflow: auto; /* Allow scrolling if needed */
		background: transparent; /* Ensure content background is also transparent */
	}

	.tools-grid {
		display: grid;
		/* Modern approach using auto-fill and minmax for truly responsive layouts */
		grid-template-columns: repeat(var(--columns, 3), 1fr);
		gap: var(--grid-gap, 12px);
		justify-content: center;
		align-content: center; /* Center content vertically */
		width: 100%;
		height: 100%;
		padding: var(--grid-padding, 8px);
		box-sizing: border-box;
		/* Added to ensure it fills the container properly */
		flex: 1;
		min-height: 0;
		/* Allow overflow in case of extreme sizing issues, but hide scrollbars */
		overflow: auto;
		scrollbar-width: none; /* Firefox */
		-ms-overflow-style: none; /* IE and Edge */
	}

	/* Hide scrollbar for Chrome, Safari and Opera */
	.tools-grid::-webkit-scrollbar {
		display: none;
	}

	.tool-button {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		width: 100%; /* Fill the grid cell width */
		aspect-ratio: 1 / 1; /* Keep buttons square */
		border: 1px solid rgba(238, 238, 238, 0.7);
		background: rgba(248, 249, 250, 0.8); /* Semi-transparent background */
		border-radius: 8px;
		cursor: pointer;
		transition: all 0.2s ease;
		color: #333;
		padding: var(--button-padding, 6px);
		box-sizing: border-box;
		position: relative;
		backdrop-filter: blur(2px); /* Add a slight blur effect */
		/* Ensure minimum touch target size for accessibility */
		min-width: 44px;
		min-height: 44px;
		/* Prevent text from overflowing */
		overflow: hidden;
		/* Ensure content scales properly */
		font-size: calc(var(--button-size, 80px) * 0.12);
	}

	/* Special styling for mode buttons */
	.tool-button[title='Construct'],
	.tool-button[title='Generate'] {
		background: rgba(255, 255, 255, 0.9);
		border-width: 2px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	}

	/* Active mode styling */
	.tool-button.active-mode {
		background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(240, 240, 255, 0.95));
		border-color: var(--button-color, #4361ee);
		box-shadow:
			0 0 0 2px rgba(67, 97, 238, 0.3),
			0 4px 12px rgba(0, 0, 0, 0.15);
		transform: translateY(-2px);
	}

	.tool-button:hover {
		background: rgba(255, 255, 255, 0.9);
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
		border-color: var(--button-color, #555);
		transform: translateY(-2px);
	}

	.tool-button:active {
		transform: scale(0.95);
	}

	.tool-button i {
		font-size: var(--icon-size, 24px);
		color: var(--button-color, #555);
		margin-bottom: 6px;
		/* Use modern fluid typography */
		font-size: clamp(18px, calc(var(--button-size, 80px) * 0.3), 32px);
	}

	.button-title {
		font-size: var(--title-size, 11px);
		text-align: center;
		line-height: 1.2;
		max-width: 100%;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		/* Use modern fluid typography */
		font-size: clamp(9px, calc(var(--button-size, 80px) * 0.12), 14px);
		/* Add padding to prevent text from touching edges */
		padding: 0 2px;
	}

	.destructive {
		background-color: rgba(255, 245, 245, 0.8);
		border-color: rgba(255, 224, 224, 0.7);
	}

	.destructive:hover {
		background-color: rgba(255, 240, 240, 0.9);
	}

	/* Modern container-based responsive design */
	/* Small screens and mobile devices */
	@media (max-width: 480px) {
		.tools-panel {
			border-radius: 6px; /* Smaller border radius */
		}

		.tools-header {
			padding: 8px 10px; /* Smaller padding */
		}

		.tools-header h2 {
			font-size: 1rem; /* Smaller font size */
		}
	}

	/* Medium screens */
	@media (min-width: 481px) and (max-width: 768px) {
		.tools-panel {
			border-radius: 8px;
		}
	}

	/* Large screens */
	@media (min-width: 769px) {
		.tools-grid {
			/* Allow more space between buttons on larger screens */
			gap: var(--grid-gap, 12px);
		}
	}

	/* Extra large screens */
	@media (min-width: 1200px) {
		.tools-grid {
			gap: var(--grid-gap, 16px);
		}
	}

	/* Handle portrait vs landscape orientation */
	@media (orientation: portrait) and (max-width: 768px) {
		.tools-grid {
			/* Optimize for vertical space in portrait mode */
			align-content: start;
		}
	}

	/* Handle high-density displays */
	@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
		.tool-button {
			/* Sharper borders on high-DPI screens */
			border-width: 0.5px;
		}
	}
</style>
