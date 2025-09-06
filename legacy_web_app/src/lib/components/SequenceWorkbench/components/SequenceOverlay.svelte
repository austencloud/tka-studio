<script lang="ts">
	import { fade, scale } from 'svelte/transition';
	import {
		sequenceOverlayStore,
		closeSequenceOverlay
	} from '$lib/state/sequenceOverlay/sequenceOverlayState';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import { browser } from '$app/environment';

	// Props
	const { title = null, children = $bindable() } = $props<{
		title?: string | null;
		children?: () => any;
		sequenceName?: string;
	}>();

	// Use the store with Svelte 5 runes
	const isOpen = $derived($sequenceOverlayStore.isOpen);

	// Truncate title to 8 characters if it's longer
	const MAX_CHARS = 8;
	const displayTitle = $derived(
		title && title.length > MAX_CHARS ? title.substring(0, MAX_CHARS) + '...' : title
	);

	// Handle close action
	function handleClose() {
		// Provide haptic feedback when closing the sequence overlay
		if (browser && hapticFeedbackService.isAvailable()) {
			hapticFeedbackService.trigger('selection');
		}

		closeSequenceOverlay();
	}

	// Handle escape key press on the window
	function handleWindowKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape' && isOpen) {
			handleClose();
		}
	}

	// Handle background click - this is the main function to close when clicking on blank areas
	function handleBackgroundClick() {
		console.log('Background clicked, closing overlay');
		handleClose();
	}

	// Prevent clicks on the content from closing the overlay
	function handleContentClick(event: MouseEvent) {
		// Stop propagation to prevent the click from reaching the background
		event.stopPropagation();
	}

	// Focus the content element when the overlay opens
	function handleOverlayOpen() {
		// Use document.querySelector to find the content element
		const contentElement = document.querySelector('.sequence-content') as HTMLDivElement | null;
		if (contentElement) {
			setTimeout(() => {
				contentElement.focus();
			}, 50);
		}
	}
</script>

<svelte:window onkeydown={handleWindowKeydown} />

{#if isOpen}
	<!-- The overlay wrapper - this is what receives the background click -->
	<div
		class="sequence-overlay-wrapper"
		transition:fade={{ duration: 200 }}
		onintroend={handleOverlayOpen}
	>
		<!-- Clickable background button - this is accessible and clickable -->
		<button
			class="background-button"
			onclick={handleBackgroundClick}
			aria-label="Close sequence overlay"
		></button>

		<!-- The actual content container -->
		<div
			class="sequence-content"
			transition:scale={{ duration: 200, start: 0.95 }}
			onclick={handleContentClick}
			onkeydown={() => {}}
			role="dialog"
			aria-modal="true"
			aria-labelledby={title ? 'sequence-title' : undefined}
			tabindex="-1"
		>
			{#if title}
				<div class="sequence-header">
					<h2 id="sequence-title">{displayTitle}</h2>
				</div>
			{/if}

			<button
				class="close-button"
				onclick={handleClose}
				aria-label="Close sequence overlay"
				title="Close sequence overlay"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					width="30"
					height="30"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				>
					<line x1="18" y1="6" x2="6" y2="18" />
					<line x1="6" y1="6" x2="18" y2="18" />
				</svg>
			</button>

			<!-- Content area with render function -->
			<div class="sequence-body">
				<!-- Wrap content in a div to prevent clicks from closing the overlay -->
				<div class="content-wrapper">
					{@render children?.()}
				</div>
			</div>
		</div>
	</div>
{/if}

<style>
	/* Wrapper for the entire overlay */
	.sequence-overlay-wrapper {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 9999;
		box-sizing: border-box;
		/* Apply safe area insets */
		padding: var(--safe-inset-top, 0px) var(--safe-inset-right, 0px) var(--safe-inset-bottom, 0px)
			var(--safe-inset-left, 0px);
	}

	/* Background button that covers the entire screen */
	.background-button {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.9);
		backdrop-filter: blur(3px);
		border: none;
		padding: 0;
		margin: 0;
		cursor: pointer;
		z-index: 1;
	}

	/* The actual content container */
	.sequence-content {
		position: relative;
		width: 100%;
		height: 100%;
		max-width: 100vw; /* Increased from 95vw to use more space */
		max-height: 100vh;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		background-color: transparent; /* Make it transparent */
		border-radius: 8px;
		box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
		z-index: 2; /* Above the background button */
		outline: none;
		/* Ensure content respects safe area insets */
		box-sizing: border-box;
	}

	@media (orientation: landscape) and (max-height: 600px) {
		.sequence-content {
			max-height: 100vh;
			max-width: 100vw; /* Increased from 90vw to use more space */
		}
	}

	.sequence-header {
		display: flex;
		justify-content: center;
		align-items: center;
		padding: 0.5rem 1rem;
		min-height: 40px;
		flex-shrink: 0;
		background-color: rgba(0, 0, 0, 0.5);
	}

	.sequence-header h2 {
		margin: 0;
		font-size: 1.25rem;
		color: #e0e0e0;
		font-weight: 600;
	}

	.sequence-body {
		flex: 1;
		display: flex;
		justify-content: center;
		align-items: center;
		overflow: hidden;
		padding: 0;
		box-sizing: border-box;
		width: 100%;
		position: relative;
		/* Ensure the body takes up all available space */
		min-height: 0; /* Important for flex children */
	}

	/* Wrapper for the slot content */

	@media (orientation: landscape) and (max-height: 600px) {
		.sequence-header {
			min-height: 30px;
			padding: 0.25rem 0.5rem;
		}
		.sequence-header h2 {
			font-size: 1rem;
		}
	}

	.close-button {
		position: absolute;
		top: max(15px, var(--safe-inset-top, 15px));
		right: max(15px, var(--safe-inset-right, 15px));
		background-color: rgba(255, 255, 255, 0.3);
		border: 2px solid rgba(255, 255, 255, 0.5);
		border-radius: 50%;
		width: 50px;
		height: 50px;
		display: flex;
		justify-content: center;
		align-items: center;
		cursor: pointer;
		color: white;
		z-index: 1001;
		transition:
			background-color 0.2s,
			transform 0.2s,
			box-shadow 0.2s;
		box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
	}

	@media (orientation: landscape) and (max-height: 600px) {
		.close-button {
			top: max(8px, var(--safe-inset-top, 8px));
			right: max(8px, var(--safe-inset-right, 8px));
			width: 40px;
			height: 40px;
		}
	}

	.close-button:hover {
		background-color: rgba(255, 255, 255, 0.5);
		transform: scale(1.1);
		box-shadow: 0 0 15px rgba(0, 0, 0, 0.7);
	}

	.close-button:active {
		transform: scale(0.95);
		background-color: rgba(255, 255, 255, 0.4);
	}
</style>
