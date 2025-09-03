<!--
  ShareButton Component

  This component provides a button for sharing and downloading sequence images.
  It uses the enhanced image exporter for reliable rendering.
-->
<script lang="ts">
	import { onMount } from '$lib/utils/svelte-lifecycle';
	import { browser } from '$app/environment';
	import { sequenceContainer } from '$lib/state/stores/sequence/SequenceContainer';
	import { useContainer } from '$lib/state/core/svelte5-integration.svelte';
	import { BEAT_FRAME_CONTEXT_KEY, type ElementContext } from '../context/ElementContext';
	import { getContext } from 'svelte';
	import { showError } from '$lib/components/shared/ToastManager.svelte';
	import {
		findBeatFrameElement,
		listenForBeatFrameElement,
		renderSequence,
		shareSequence,
		downloadSequenceImage,
		isWebShareSupported
	} from './utils/ShareUtils';
	import ShareDropdown from './ShareDropdown.svelte';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import { fade, scale } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	// Track dropdown state
	let isDropdownOpen = $state(false);

	// Track rendering state
	let isRendering = $state(false);

	// Track success indicator state
	let showSuccessIndicator = $state(false);
	let successTimeout: number | null = $state(null);

	// Props
	const { beatFrameElement = null } = $props<{ beatFrameElement?: HTMLElement | null }>();

	// Track element references
	let beatFrameElementState = $state<HTMLElement | null>(beatFrameElement);

	// Update state when prop changes
	$effect(() => {
		if (beatFrameElement) {
			beatFrameElementState = beatFrameElement;
		}
	});

	// Use the sequence container
	const sequence = useContainer(sequenceContainer);

	// Get the current sequence data
	const sequenceBeats = $derived(sequence.beats || []);
	const sequenceName = $derived(generateSequenceName(sequenceBeats));

	// Try to get the element from context
	const beatFrameContext = getContext<ElementContext>(BEAT_FRAME_CONTEXT_KEY);

	// Set up an effect to update our local reference from context if available
	$effect(() => {
		if (beatFrameContext) {
			const contextElement = beatFrameContext.getElement();
			if (contextElement) {
				console.log('ShareButton: Got element from context');
				beatFrameElementState = contextElement;
			}
		}
	});

	// Set up event listener for beatframe-element-available
	onMount(() => {
		// Try to find the element immediately on mount
		if (!beatFrameElementState) {
			const element = findBeatFrameElement(beatFrameContext);
			if (element) {
				beatFrameElementState = element;
			}
		}

		// Set up listener for element availability
		const cleanupListener = listenForBeatFrameElement((element) => {
			beatFrameElementState = element;
		});

		return () => {
			// Clean up listener
			cleanupListener();

			// Clear any pending timeout
			if (successTimeout !== null) {
				clearTimeout(successTimeout);
				successTimeout = null;
			}
		};
	});

	// Generate a sequence name from the beats
	function generateSequenceName(beats: any[]): string {
		if (!beats || beats.length === 0) return 'Sequence';

		// Extract letters from beats
		const letters = beats
			.map((beat) => ((beat.letter || beat.metadata?.letter) as string) || '')
			.filter((letter) => letter.trim() !== '')
			.join('');

		// Return the exact sequence word as displayed in the UI
		// This preserves the original case and format
		return letters || 'Sequence';
	}

	// Toggle dropdown
	function toggleDropdown() {
		// Provide haptic feedback
		if (browser && hapticFeedbackService.isAvailable()) {
			hapticFeedbackService.trigger('selection');
		}

		isDropdownOpen = !isDropdownOpen;
	}

	// Close dropdown
	function closeDropdown() {
		isDropdownOpen = false;
	}

	// Handle share button click
	async function handleShare() {
		if (!browser) return;

		// Provide haptic feedback
		if (hapticFeedbackService.isAvailable()) {
			hapticFeedbackService.trigger('success');
		}

		try {
			// Close dropdown
			closeDropdown();

			// Check if sequence is empty
			if (!sequenceBeats || sequenceBeats.length === 0) {
				showError('No sequence to share');
				return;
			}

			// Check if Web Share API is supported
			if (!isWebShareSupported()) {
				showError("Your device doesn't support sharing");
				return;
			}

			// Set rendering state
			isRendering = true;

			// Render the sequence
			const result = await renderSequence({
				sequenceName,
				sequenceBeats,
				difficultyLevel: sequence.metadata?.difficulty || 1,
				beatFrameElement: beatFrameElementState
			});

			if (!result) {
				showError('Failed to generate image for sharing');
				isRendering = false;
				return;
			}

			// Share the sequence
			await shareSequence({
				sequenceBeats,
				sequenceName,
				imageResult: result
			});

			// Show success indicator
			showSuccessIndicator = true;

			// Clear any existing timeout
			if (successTimeout !== null) {
				clearTimeout(successTimeout);
			}

			// Hide success indicator after 2 seconds
			successTimeout = window.setTimeout(() => {
				showSuccessIndicator = false;
				successTimeout = null;
			}, 2000);

			// Provide haptic feedback for successful share
			hapticFeedbackService.trigger('success');
		} catch (error) {
			showError('Failed to share sequence');
			console.error('Share error:', error);
		} finally {
			isRendering = false;
		}
	}

	// Handle download button click
	async function handleDownload() {
		if (!browser) return;

		// Provide haptic feedback
		if (hapticFeedbackService.isAvailable()) {
			hapticFeedbackService.trigger('success');
		}

		try {
			// Close dropdown
			closeDropdown();

			// Check if sequence is empty
			if (!sequenceBeats || sequenceBeats.length === 0) {
				showError('No sequence to download');
				return;
			}

			// Set rendering state
			isRendering = true;

			console.log('ShareButton: Starting download process');

			// Make one last attempt to find the element if it's not available
			if (!beatFrameElementState) {
				beatFrameElementState = findBeatFrameElement(beatFrameContext);

				if (!beatFrameElementState) {
					showError('Cannot find sequence display. Please try again.');
					isRendering = false;
					return;
				}
			}

			// Render the sequence
			const result = await renderSequence({
				sequenceName,
				sequenceBeats,
				difficultyLevel: sequence.metadata?.difficulty || 1,
				beatFrameElement: beatFrameElementState
			});

			if (!result) {
				showError('Failed to generate image for download');
				isRendering = false;
				return;
			}

			console.log('ShareButton: Starting download process');

			// Download the sequence image
			const downloadResult = await downloadSequenceImage({
				sequenceName,
				imageResult: result
			});

			console.log('ShareButton: Download result:', downloadResult);

			// Only provide success feedback if the download was successful
			// and not cancelled by the user
			if (downloadResult) {
				console.log('ShareButton: Download successful, providing feedback');

				// Provide haptic feedback for successful download
				if (hapticFeedbackService.isAvailable()) {
					hapticFeedbackService.trigger('success');
				}

				// Show success indicator
				showSuccessIndicator = true;

				// Clear any existing timeout
				if (successTimeout !== null) {
					clearTimeout(successTimeout);
				}

				// Hide success indicator after 2 seconds
				successTimeout = window.setTimeout(() => {
					showSuccessIndicator = false;
					successTimeout = null;
				}, 2000);
			} else {
				console.log('ShareButton: Download was cancelled or failed without error');
			}
		} catch (error) {
			// Log the full error for debugging
			console.error(
				'ShareButton: Download error:',
				error instanceof Error
					? {
							name: error.name,
							message: error.message,
							stack: error.stack
						}
					: error
			);

			// Check if this is a cancellation error
			const isCancellation =
				error instanceof Error &&
				(error.message === 'USER_CANCELLED_OPERATION' ||
					error.message.includes('cancelled') ||
					error.message.includes('canceled') ||
					error.message.includes('aborted') ||
					error.name === 'AbortError');

			if (!isCancellation) {
				// Only show error for non-cancellation errors
				showError('Failed to download sequence');
				console.error('ShareButton: Non-cancellation download error:', error);
			} else {
				console.log('ShareButton: User cancelled the download operation');
			}
		} finally {
			isRendering = false;
		}
	}
</script>

<button
	class="share-button"
	onclick={toggleDropdown}
	aria-label="Share sequence"
	class:loading={isRendering}
	class:success={showSuccessIndicator}
>
	<div class="icon-wrapper">
		{#if isRendering}
			<i class="fa-solid fa-spinner fa-spin"></i>
		{:else if showSuccessIndicator}
			<i class="fa-solid fa-check" transition:scale={{ duration: 300, easing: quintOut }}></i>
		{:else}
			<i class="fa-solid fa-share-alt"></i>
		{/if}
	</div>

	{#if showSuccessIndicator}
		<div class="success-pulse" transition:fade={{ duration: 300 }}></div>
	{/if}
</button>

{#if isDropdownOpen}
	<div class="dropdown-container">
		<ShareDropdown onShare={handleShare} onDownload={handleDownload} onClose={closeDropdown} />
	</div>
{/if}

<style>
	/* Global styles to ensure consistent sizing with settings button */
	:global(.sequence-widget > .main-layout > .share-button) {
		position: absolute !important;
		top: calc(var(--button-size-factor, 1) * 10px) !important; /* Exactly match settings button */
		right: calc(
			var(--button-size-factor, 1) * 10px
		) !important; /* Mirror of settings button's left */
		width: calc(
			var(--button-size-factor, 1) * 45px
		) !important; /* Exact same size as settings button */
		height: calc(
			var(--button-size-factor, 1) * 45px
		) !important; /* Exact same size as settings button */
		z-index: 40 !important; /* Consistent with other FABs */
		margin: 0 !important; /* Override any default margin */
		display: flex !important; /* Ensure it's displayed */
		visibility: visible !important; /* Ensure it's visible */
		opacity: 1 !important; /* Ensure it's fully opaque */
	}

	/* Ensure the icon inside scales correctly */
	:global(.sequence-widget > .main-layout > .share-button i) {
		font-size: calc(
			var(--button-size-factor, 1) * 19px
		); /* Exact same icon size as settings button */
	}

	/* Position the dropdown container absolutely to prevent layout shifts */
	:global(.sequence-widget > .main-layout > .dropdown-container) {
		position: absolute !important;
		top: calc(
			var(--button-size-factor, 1) * 10px + var(--button-size-factor, 1) * 45px + 5px
		) !important;
		right: calc(var(--button-size-factor, 1) * 10px) !important;
		z-index: 41 !important; /* Slightly higher than the button */
	}

	.share-button {
		background-color: var(--tkc-button-panel-background, #2a2a2e);
		color: var(--tkc-icon-color-share, #00bcd4); /* Teal icon color, or a theme variable */
		border: none;
		border-radius: 50%; /* Perfectly round */
		width: 100%;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition:
			transform 0.2s ease-out,
			background-color 0.2s ease-out,
			box-shadow 0.2s ease-out,
			color 0.2s ease-out;
		box-shadow:
			0 3px 6px rgba(0, 0, 0, 0.16),
			0 3px 6px rgba(0, 0, 0, 0.23);
		padding: 0;
		pointer-events: auto;
		position: relative;
		overflow: hidden; /* Match settings button */
	}

	/* Success state styling */
	.share-button.success {
		color: #4caf50; /* Green color for success */
		animation: success-pulse 0.5s ease-out;
	}

	/* Success pulse animation */
	@keyframes success-pulse {
		0% {
			transform: scale(1);
			box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7);
		}
		50% {
			transform: scale(1.1);
			box-shadow: 0 0 0 10px rgba(76, 175, 80, 0);
		}
		100% {
			transform: scale(1);
			box-shadow: 0 0 0 0 rgba(76, 175, 80, 0);
		}
	}

	/* Success pulse overlay */
	.success-pulse {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		border-radius: 50%;
		background: radial-gradient(circle, rgba(76, 175, 80, 0.2) 0%, rgba(76, 175, 80, 0) 70%);
		pointer-events: none;
		z-index: -1;
	}

	.share-button:hover {
		background-color: var(--tkc-button-panel-background-hover, #3c3c41);
		transform: translateY(-2px) scale(1.05);
		box-shadow:
			0 6px 12px rgba(0, 0, 0, 0.2),
			0 4px 8px rgba(0, 0, 0, 0.26);
		color: var(--tkc-icon-color-share-hover, #6c9ce9); /* Match settings button hover color */
	}

	.share-button:focus-visible {
		outline: none;
		box-shadow: 0 0 0 2px var(--tkc-focus-ring-color, rgba(108, 156, 233, 0.6));
	}

	.share-button:active {
		transform: translateY(0px) scale(1);
		background-color: var(--tkc-button-panel-background-active, #1e1e21);
		box-shadow:
			0 1px 3px rgba(0, 0, 0, 0.12),
			0 1px 2px rgba(0, 0, 0, 0.24);
	}

	/* Add icon wrapper styles */
	.icon-wrapper {
		background: transparent;
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%; /* Ensure wrapper fills button for icon centering */
		height: 100%;
		color: inherit;
	}

	.icon-wrapper i {
		/* Font size is controlled by the global selector */
		line-height: 1;
		display: block;
		transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
	}

	/* Add a subtle scale effect on hover, similar to settings button */
	.share-button:hover .icon-wrapper i {
		transform: scale(1.1); /* Subtle scale effect */
	}

	/* Style for the dropdown container */
	.dropdown-container {
		position: absolute;
		z-index: 41;
	}
</style>
