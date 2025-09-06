<script lang="ts">
	// Import necessary modules and types
	import type { ButtonDefinition, ActionEventDetail, LayoutOrientation } from '../types'; // Import LayoutOrientation
	import { getButtonAnimationDelayValue } from '../utils/animations';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import { browser } from '$app/environment';

	// Props using Svelte 5 runes
	const props = $props<{
		button: ButtonDefinition;
		buttonSize: number;
		index: number; // Index for stagger animation delay
		isAnimatingOut?: boolean;
		layout?: LayoutOrientation;
		onClick?: (detail: ActionEventDetail) => void;
	}>();

	// Set default values
	$effect(() => {
		if (props.isAnimatingOut === undefined) props.isAnimatingOut = false;
		if (props.layout === undefined) props.layout = 'horizontal';
	});

	// Extract props for easier access using $derived
	const button = $derived(props.button);
	const buttonSize = $derived(props.buttonSize);
	const index = $derived(props.index);
	const isAnimatingOut = $derived(props.isAnimatingOut || false);
	const layout = $derived(props.layout || 'horizontal');

	// Handle click event
	function handleClick() {
		// Provide appropriate haptic feedback based on button type
		if (browser) {
			// Use different haptic patterns based on button action
			if (button.id === 'clearSequence' || button.id === 'deleteBeat') {
				// Warning feedback for destructive actions
				hapticFeedbackService.trigger('warning');
			} else if (button.id === 'saveImage' || button.id === 'viewFullScreen') {
				// Success feedback for sharing/viewing actions
				hapticFeedbackService.trigger('success');
			} else {
				// Default selection feedback for other actions
				hapticFeedbackService.trigger('selection');
			}
		}

		// Call the onClick handler if provided
		if (props.onClick) {
			props.onClick({ id: button.id });
		}
	}

	// Reactive calculation for animation delay CSS variable
	const animationDelay = $derived(getButtonAnimationDelayValue(index));

	// Reactive calculation for icon size based on button size
	const iconSize = $derived(buttonSize * 0.5); // Icon takes up half the button size
</script>

<div
	class="button-container"
	class:animating-out={isAnimatingOut}
	class:vertical={layout === 'vertical'}
	style="--button-index: {index}; width: {buttonSize}px; height: {buttonSize}px; --animation-delay: {animationDelay};"
	role="listitem"
>
	<button
		class="modern-button ripple"
		onclick={handleClick}
		title={button.title}
		aria-label={button.title}
		disabled={button.disabled || false}
		style="--button-color: {button.color || '#555'};"
		data-mdb-ripple="true"
		data-mdb-ripple-color="light"
	>
		<i class="fa-solid {button.icon}" style="font-size: {iconSize}px;" aria-hidden="true"></i>
	</button>
</div>

<style>
	.button-container {
		display: flex; /* Use flex to center button */
		justify-content: center;
		align-items: center;
		position: relative; /* Needed for z-index hover effect */
		z-index: 0;
		transition: transform 0.2s ease-in-out;
		/* Apply default (horizontal fly-in) animation using the shorthand property */
		/* Ensure ease timing function is included if desired */
		animation: flyInHorizontal 0.5s var(--animation-delay) backwards ease;
		flex-shrink: 0; /* Prevent shrinking */
		min-width: 50px; /* Ensure minimum width */
		min-height: 50px; /* Ensure minimum height */
	}

	/* --- Reverted to overriding specific properties --- */

	/* Apply horizontal fly-out animation */
	.button-container.animating-out {
		animation-name: flyOutHorizontal;
		animation-duration: 0.4s;
		animation-fill-mode: forwards;
		/* Inherits delay and timing function from base */
	}

	/* Apply vertical fly-in animation */
	.button-container.vertical {
		animation-name: flyInVertical;
		/* Inherits duration, delay, fill-mode, timing function from base */
		/* Ensure base animation has desired properties (like backwards fill mode) */
	}

	/* Apply vertical fly-out animation */
	.button-container.vertical.animating-out {
		animation-name: flyOutVertical;
		animation-duration: 0.4s;
		animation-fill-mode: forwards;
		/* Inherits delay and timing function from base */
	}

	/* Hover effect: scale up and bring to front */
	.button-container:hover {
		z-index: 1;
		transform: scale(1.1);
	}

	/* Button styles (remain the same) */
	.modern-button {
		width: 100%;
		height: 100%;
		border-radius: 50%; /* Circular buttons */
		display: flex;
		justify-content: center;
		align-items: center;
		background-color: white;
		border: 2px solid var(--button-color);
		color: var(--button-color);
		cursor: pointer;
		transition: all 0.2s ease-in-out;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
		position: relative; /* Needed for ripple */
		overflow: hidden; /* Contain ripple effect */
	}

	.modern-button:hover {
		background-color: var(--button-color);
		color: white;
		transform: translateY(-2px); /* Slight lift effect */
		box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
	}

	.modern-button:active {
		transform: translateY(1px); /* Press down effect */
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
	}

	/* Disabled state (remains the same) */
	.modern-button[disabled] {
		opacity: 0.5;
		cursor: not-allowed;
		background-color: #eee;
		border-color: #ccc;
		color: #999;
		box-shadow: none;
		transform: none;
	}
	.modern-button[disabled]:hover {
		transform: none;
		box-shadow: none;
	}

	/* --- Keyframe Animations (remain the same) --- */

	@keyframes flyInHorizontal {
		from {
			opacity: 0;
			transform: translateX(100px);
		}
		to {
			opacity: 1;
			transform: translateX(0);
		}
	}
	@keyframes flyOutHorizontal {
		from {
			opacity: 1;
			transform: translateX(0);
		}
		to {
			opacity: 0;
			transform: translateX(100px);
		}
	}
	@keyframes flyInVertical {
		from {
			opacity: 0;
			transform: translateY(100px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
	@keyframes flyOutVertical {
		from {
			opacity: 1;
			transform: translateY(0);
		}
		to {
			opacity: 0;
			transform: translateY(100px);
		}
	}
</style>
