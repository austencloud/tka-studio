<script lang="ts">
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import { sequenceOverlayStore } from '$lib/state/sequenceOverlay/sequenceOverlayState';
	import { browser } from '$app/environment';

	// Create a function to show the first-time setup dialog
	const { showDialog } = $props<{
		showDialog: () => void;
	}>();

	// Track if the sequence overlay is open
	let isOverlayOpen = $state(false);

	// Subscribe to the sequence overlay store
	$effect(() => {
		if (browser) {
			const unsubscribe = sequenceOverlayStore.subscribe((state) => {
				isOverlayOpen = state.isOpen;
			});

			return unsubscribe;
		}
	});

	// Detect if we're on desktop and in landscape mode
	let isDesktopLandscape = $state(false);

	// Update the device detection on mount and resize
	$effect(() => {
		if (browser) {
			const updateDeviceDetection = () => {
				const isLandscape = window.innerWidth > window.innerHeight;
				const isDesktop = window.innerWidth >= 768; // Common breakpoint for desktop
				isDesktopLandscape = isDesktop && isLandscape;
			};

			// Initial check
			updateDeviceDetection();

			// Add resize listener
			window.addEventListener('resize', updateDeviceDetection);

			return () => {
				window.removeEventListener('resize', updateDeviceDetection);
			};
		}
	});

	// Handle click with haptic feedback
	function handleClick() {
		// Provide haptic feedback when opening the setup dialog
		if (browser && hapticFeedbackService.isAvailable()) {
			hapticFeedbackService.trigger('selection');
		}

		// Call the original showDialog function
		showDialog();
	}
</script>

{#if !isOverlayOpen}
	<button
		class="setup-button"
		class:desktop-landscape={isDesktopLandscape}
		onclick={handleClick}
		title="Show First-Time Setup Dialog"
		aria-label="Show First-Time Setup Dialog"
	>
		<svg
			xmlns="http://www.w3.org/2000/svg"
			width="16"
			height="16"
			viewBox="0 0 24 24"
			fill="none"
			stroke="currentColor"
			stroke-width="2"
			stroke-linecap="round"
			stroke-linejoin="round"
		>
			<path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"></path>
			<path d="M12 16v-4"></path>
			<path d="M12 8h.01"></path>
		</svg>
	</button>
{/if}

<style>
	.setup-button {
		background: #1e293b;
		color: white;
		border: 1px solid #334155;
		border-radius: 50%;
		width: 36px;
		height: 36px;
		padding: 0;
		cursor: pointer;
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
		display: flex;
		align-items: center;
		justify-content: center;
		opacity: 0.8;
		transition: all 0.2s ease;
		position: fixed;
		bottom: 10px; /* Default position for mobile */
		left: 10px;
		z-index: 9999;
	}

	.setup-button:hover {
		opacity: 1;
		background: #334155;
		box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3);
		transform: scale(1.05);
	}

	/* Desktop landscape positioning - near the Clear Sequence button */
	.setup-button.desktop-landscape {
		bottom: 10px; /* Same level as Clear Sequence button */
		left: 65px; /* Position to the right of the Clear Sequence button */
	}

	/* Adjust position on larger screens (non-landscape) */
	@media (min-width: 768px) and (orientation: portrait) {
		.setup-button {
			bottom: 70px; /* Moved higher to avoid overlap with other buttons */
			left: 15px;
		}
	}

	/* Ensure proper positioning on mobile devices */
	@media (max-width: 480px) {
		.setup-button {
			bottom: 10px;
			left: 10px;
		}
	}
</style>
