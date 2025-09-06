<!-- src/lib/components/SequenceWorkbench/RightPanel/TransitionWrapper.svelte -->
<script lang="ts">
	import { fly } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { onMount } from 'svelte';

	// Props using Svelte 5 runes
	const props = $props<{
		isSequenceEmpty: boolean;
		transitionDuration?: number;
	}>();

	// Set default values
	$effect(() => {
		if (props.transitionDuration === undefined) props.transitionDuration = 400;
	});

	// State using Svelte 5 runes
	let previousState = $state(props.isSequenceEmpty);
	let isTransitioning = $state(false);
	let showStartPosPicker = $state(props.isSequenceEmpty);
	let showOptionPicker = $state(!props.isSequenceEmpty);
	let containerHeight = $state(0);
	let startPosPickerHeight = $state(0);
	let optionPickerHeight = $state(0);
	let startPosPickerElement = $state<HTMLElement | null>(null);
	let optionPickerElement = $state<HTMLElement | null>(null);
	let containerElement = $state<HTMLElement | null>(null);
	let isMounted = $state(false);

	onMount(() => {
		isMounted = true;

		// Initialize both components
		showStartPosPicker = true;
		showOptionPicker = true;

		// Initialize heights after a short delay to ensure DOM is ready
		setTimeout(() => {
			preInitializeComponents();
			updateHeights();

			// Hide the component that shouldn't be visible initially
			if (props.isSequenceEmpty) {
				showOptionPicker = false;
			} else {
				showStartPosPicker = false;
			}
		}, 50);
	});

	// Update container height when component dimensions change
	function updateHeights() {
		if (!isMounted) return;

		// Check if we're in fullscreen mode by looking at the document.fullscreenElement
		const isFullScreen = !!document.fullscreenElement;

		// For the start position picker, we want to use the full height of the container
		// This ensures the start position picker is centered vertically
		if (containerElement) {
			// In fullscreen mode, use the viewport height
			if (isFullScreen) {
				startPosPickerHeight = window.innerHeight;
			} else {
				const containerParentHeight = containerElement.parentElement?.clientHeight || 0;
				if (containerParentHeight > 0) {
					startPosPickerHeight = containerParentHeight;
				} else {
					// Fallback to scrollHeight if parent height is not available
					if (startPosPickerElement) {
						startPosPickerHeight = startPosPickerElement.scrollHeight;
					}
				}
			}
		}

		// For the option picker, we need to ensure it has enough height
		if (optionPickerElement) {
			// In fullscreen mode, use the viewport height
			if (isFullScreen) {
				optionPickerHeight = window.innerHeight;
			} else {
				// Use the greater of the content height or the container parent height
				const contentHeight = optionPickerElement.scrollHeight;
				const containerParentHeight = containerElement?.parentElement?.clientHeight || 0;
				optionPickerHeight = Math.max(contentHeight, containerParentHeight);
			}
		}

		// Set container height to the height of the visible component
		const newHeight = props.isSequenceEmpty ? startPosPickerHeight : optionPickerHeight;

		// Only update if height has changed
		if (newHeight !== containerHeight && newHeight > 0) {
			containerHeight = newHeight;

			// Update container style with animation
			if (containerElement) {
				// In fullscreen mode, use 100% height instead of fixed pixel value
				if (isFullScreen) {
					containerElement.style.height = '100%';
				} else {
					containerElement.style.height = `${containerHeight}px`;
				}
			}
		}
	}

	// Add a resize observer to update heights when content changes
	onMount(() => {
		const resizeObserver = new ResizeObserver(() => {
			updateHeights();
		});

		if (startPosPickerElement) {
			resizeObserver.observe(startPosPickerElement);
		}

		if (optionPickerElement) {
			resizeObserver.observe(optionPickerElement);
		}

		// Add fullscreen change event listener
		const handleFullscreenChange = () => {
			// Update heights when entering or exiting fullscreen mode
			updateHeights();

			// Force a window resize event to ensure all components update
			window.dispatchEvent(new Event('resize'));
		};

		// Add event listeners for all browser variants
		document.addEventListener('fullscreenchange', handleFullscreenChange);
		document.addEventListener('webkitfullscreenchange', handleFullscreenChange);
		document.addEventListener('mozfullscreenchange', handleFullscreenChange);
		document.addEventListener('MSFullscreenChange', handleFullscreenChange);

		return () => {
			resizeObserver.disconnect();

			// Remove fullscreen event listeners
			document.removeEventListener('fullscreenchange', handleFullscreenChange);
			document.removeEventListener('webkitfullscreenchange', handleFullscreenChange);
			document.removeEventListener('mozfullscreenchange', handleFullscreenChange);
			document.removeEventListener('MSFullscreenChange', handleFullscreenChange);
		};
	});

	// Watch for changes in isSequenceEmpty and handle transitions
	$effect(() => {
		if (isMounted && previousState !== props.isSequenceEmpty) {
			handleTransition();
			previousState = props.isSequenceEmpty;
		}
	});

	// Pre-initialize both components to ensure proper layout
	function preInitializeComponents() {
		// For the start position picker, we want to use the full height of the container
		if (containerElement) {
			const containerParentHeight = containerElement.parentElement?.clientHeight || 0;
			if (containerParentHeight > 0) {
				startPosPickerHeight = containerParentHeight;
			} else if (startPosPickerElement) {
				startPosPickerHeight = startPosPickerElement.scrollHeight;
			}
		}

		// For the option picker, we need to ensure it's properly sized before transition
		if (containerElement && !optionPickerHeight) {
			// Use the container's parent height as a starting point
			const containerParentHeight = containerElement.parentElement?.clientHeight || 0;
			if (containerParentHeight > 0) {
				optionPickerHeight = containerParentHeight;
			}
		}
	}

	// Handle the transition between components
	function handleTransition() {
		if (isTransitioning) return;
		isTransitioning = true;

		// Ensure both components are properly initialized
		preInitializeComponents();

		// Measure both components before transition
		if (startPosPickerElement) {
			startPosPickerHeight = startPosPickerElement.scrollHeight || startPosPickerHeight;
		}
		if (optionPickerElement) {
			optionPickerHeight = optionPickerElement.scrollHeight || optionPickerHeight;
		}

		// Preserve the current height during transition
		if (containerElement) {
			containerElement.style.height = `${containerHeight}px`;

			// Animate to the new height
			setTimeout(() => {
				const newHeight = props.isSequenceEmpty ? startPosPickerHeight : optionPickerHeight;
				if (containerElement) {
					containerElement.style.height = `${newHeight}px`;
					containerHeight = newHeight;
				}
			}, 50); // Small delay to ensure DOM is ready
		}

		// If transitioning to StartPosPicker
		if (props.isSequenceEmpty) {
			// Show StartPosPicker immediately to ensure animation plays
			showStartPosPicker = true;

			// Force a reflow to ensure the animation triggers properly
			if (startPosPickerElement) {
				void startPosPickerElement.offsetHeight;
			}

			// Hide OptionPicker after transition completes
			setTimeout(() => {
				showOptionPicker = false;
				isTransitioning = false;
			}, props.transitionDuration + 50); // Add a small buffer to ensure animation completes
		}
		// If transitioning to OptionPicker
		else {
			// Show OptionPicker immediately to ensure animation plays
			showOptionPicker = true;

			// Force a reflow to ensure the animation triggers properly
			if (optionPickerElement) {
				void optionPickerElement.offsetHeight;
			}

			// Hide StartPosPicker after transition completes
			setTimeout(() => {
				showStartPosPicker = false;
				isTransitioning = false;
			}, props.transitionDuration + 50); // Add a small buffer to ensure animation completes
		}
	}

	// Transition parameters

	// Different fly parameters for entering and exiting
	const flyInParams = $derived({
		duration: props.transitionDuration,
		easing: cubicInOut,
		y: 30,
		opacity: 0
	});

	const flyOutParams = $derived({
		duration: props.transitionDuration * 0.8,
		easing: cubicInOut,
		y: -20,
		opacity: 0
	});
</script>

<div class="transition-container" bind:this={containerElement}>
	{#if showStartPosPicker}
		<!-- svelte-ignore slot_element_deprecated -->
		<div
			class="component-wrapper start-pos-wrapper"
			class:active={props.isSequenceEmpty}
			bind:this={startPosPickerElement}
			in:fly={flyInParams}
			out:fly={flyOutParams}
		>
			<slot name="startPosPicker" />
		</div>
	{/if}

	{#if showOptionPicker}
		<!-- svelte-ignore slot_element_deprecated -->
		<div
			class="component-wrapper option-picker-wrapper"
			class:active={!props.isSequenceEmpty}
			bind:this={optionPickerElement}
			in:fly={flyInParams}
			out:fly={flyOutParams}
		>
			<slot name="optionPicker" />
		</div>
	{/if}
</div>

<style>
	.transition-container {
		position: relative;
		width: 100%;
		height: 100%;
		overflow: hidden;
		transition: height 0.4s cubic-bezier(0.4, 0, 0.2, 1);
		will-change: height;
		display: flex;
		flex-direction: column;
		flex: 1;
		min-height: 0; /* Crucial for proper flex behavior */
	}

	.component-wrapper {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%; /* Fill the entire height */
		opacity: 0;
		transform: translateY(20px);
		transition:
			opacity 0.4s cubic-bezier(0.4, 0, 0.2, 1),
			transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
		will-change: opacity, transform;
		pointer-events: none;
		display: flex;
		flex-direction: column;
		justify-content: center; /* Center content vertically */
		align-items: center; /* Center content horizontally */
		flex: 1;
		min-height: 0; /* Crucial for proper flex behavior */
		overflow: auto; /* Allow scrolling if content overflows */
	}

	.component-wrapper.active {
		opacity: 1;
		transform: translateY(0);
		pointer-events: all;
	}

	/* Ensure both components are properly centered from the start */
	.component-wrapper > :global(*) {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		width: 100%;
		height: 100%;
		flex: 1;
		min-height: 0; /* Crucial for proper flex behavior */
		overflow: auto; /* Allow scrolling if content overflows */
	}

	/* Ensure the start position picker has proper styling */
	.start-pos-wrapper {
		z-index: 2;
	}

	/* Ensure the option picker has proper styling */
	.option-picker-wrapper {
		z-index: 1;
	}
</style>
