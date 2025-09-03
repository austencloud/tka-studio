<script lang="ts">
	import { useResponsiveLayout } from '$lib/composables/useResponsiveLayout';
	import { onMount, onDestroy, getContext } from 'svelte';
	import { useResizeObserver } from '$lib/composables/useResizeObserver';
	import { browser } from '$app/environment';
	import { BEAT_FRAME_CONTEXT_KEY, type ElementContext } from './context/ElementContext';

	import { handleButtonAction } from './ButtonPanel/ButtonPanelLogic';
	import {
		calculateWorkbenchIsPortrait,
		calculateButtonSizeFactor
	} from './utils/SequenceLayoutCalculator';
	import { useSequenceMetadata } from './utils/SequenceMetadataManager';
	import { openSequenceOverlay } from '$lib/state/sequenceOverlay/sequenceOverlayState';

	import type { ActionEventDetail } from './ButtonPanel/types';
	import { sequenceActions } from '$lib/state/machines/sequenceMachine';
	import { appActions } from '$lib/state/machines/app/app.actions';
	import { sequenceContainer } from '$lib/state/stores/sequence/SequenceContainer';

	import SequenceContent from './content/SequenceContent.svelte';
	import SequenceOverlay from './components/SequenceOverlay.svelte';
	import SequenceOverlayContent from './overlay/SequenceOverlayContent.svelte';
	import DeleteButton from './DeleteButton.svelte';
	import DeleteModal from './DeleteModal.svelte';
	import SequenceOverlayButton from './SequenceOverlayButton.svelte';
	import RemoveBeatButton from './RemoveBeatButton.svelte';
	import ClearSequenceButton from './ClearSequenceButton.svelte';
	// Explicitly import ShareButton with a console log to verify it's being imported
	import ShareButton from './share/ShareButton.svelte';
	import SettingsButton from '$lib/components/MenuBar/SettingsButton/SettingsButton.svelte';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';

	// Log to verify ShareButton is imported
	console.log('SequenceWidget: ShareButton imported:', ShareButton);

	const { size, resizeObserver } = useResizeObserver();
	const { dimensions } = useResponsiveLayout();

	let activeMode = $state<'construct' | 'generate'>('construct');

	// We're using the shared context key from ElementContext.ts

	// Create a reactive state for the beat frame element
	let beatFrameElement = $state<HTMLElement | null>(null);
	let fallbackElement = $state<HTMLElement | null>(null);

	// Try to get the element from context
	const beatFrameContext = getContext<ElementContext>(BEAT_FRAME_CONTEXT_KEY);

	// Set up an effect to update our local reference from context if available
	$effect(() => {
		if (beatFrameContext) {
			const contextElement = beatFrameContext.getElement();
			if (contextElement) {
				beatFrameElement = contextElement;
			}
		}
	});

	// Update when beatFrameElement changes
	$effect(() => {
		// If we have a valid element, store it in localStorage for persistence across hot reloads
		if (beatFrameElement && browser) {
			try {
				// We can't store the element directly, but we can mark that we have it
				localStorage.setItem('beatFrameElementAvailable', 'true');

				// Also store in global variables for maximum compatibility
				(window as any).__beatFrameElementRef = beatFrameElement;
				(window as any).__pendingBeatFrameElement = beatFrameElement;
			} catch (error) {
				console.error('SequenceWidget: Error storing beatFrameElement availability:', error);
			}
		}
	});

	// Listen for the custom event as a fallback mechanism
	onMount(() => {
		if (browser) {
			// Check if we have a global fallback reference
			if ((window as any).__beatFrameElementRef) {
				fallbackElement = (window as any).__beatFrameElementRef;

				// If we don't have a primary element yet, use the fallback
				if (!beatFrameElement) {
					beatFrameElement = fallbackElement;
				}
			}

			// Listen for the custom event
			const handleBeatFrameElementAvailable = (event: CustomEvent) => {
				if (event.detail && event.detail.element) {
					fallbackElement = event.detail.element;

					// If we don't have a primary element yet, use the fallback
					if (!beatFrameElement) {
						beatFrameElement = fallbackElement;
					}
				}
			};

			document.addEventListener(
				'beatframe-element-available',
				handleBeatFrameElementAvailable as EventListener
			);

			// Set up a MutationObserver to detect when the BeatFrame element is added to the DOM
			const observer = new MutationObserver(() => {
				if (!beatFrameElement) {
					// Try to find the BeatFrame element in the DOM
					const beatFrameElements = document.querySelectorAll('.beat-frame-container');
					if (beatFrameElements.length > 0) {
						fallbackElement = beatFrameElements[0] as HTMLElement;

						// If we don't have a primary element yet, use the fallback
						if (!beatFrameElement) {
							beatFrameElement = fallbackElement;
						}
					}
				}
			});

			// Start observing the document body for DOM changes
			observer.observe(document.body, {
				childList: true,
				subtree: true
			});

			return () => {
				// Clean up the event listener and observer when the component is destroyed
				document.removeEventListener(
					'beatframe-element-available',
					handleBeatFrameElementAvailable as EventListener
				);
				observer.disconnect();
			};
		}
	});
	let isDeleteModalOpen = $state(false);
	let isInDeletionMode = $state(false);
	let deletionModeTooltip = $state<HTMLElement | null>(null);
	let deleteButtonRect = $state<DOMRect | null>(null);

	// Emit the full sequence widget dimensions whenever they change
	$effect(() => {
		if ($size && $size.width > 0 && $size.height > 0) {
			const event = new CustomEvent('sequence-widget-dimensions', {
				bubbles: true,
				detail: {
					width: $size.width,
					height: $size.height
				}
			});
			document.dispatchEvent(event);
		}
	});

	const workbenchIsPortrait = $derived(
		calculateWorkbenchIsPortrait($dimensions.width, $size.height)
	);

	const buttonSizeFactor = $derived(
		calculateButtonSizeFactor($dimensions.width, $dimensions.height)
	);

	let sequenceName = $state('');

	$effect(() => {
		const { unsubscribe } = useSequenceMetadata((metadata) => {
			sequenceName = metadata.name;
		});
		return unsubscribe;
	});

	// Check if there's a selected beat
	// Use $state and a direct subscription for immediate reactivity
	let hasSelectedBeat = $state(false);

	// Create a more reactive subscription to the selection state
	// This ensures immediate UI updates when selection changes
	$effect(() => {
		// Create a direct subscription to the sequenceContainer
		const unsubscribe = sequenceContainer.subscribe((state) => {
			// Update the hasSelectedBeat state immediately when selection changes
			hasSelectedBeat = state.selectedBeatIds.length > 0;
		});

		// Clean up the subscription when the component is destroyed or the effect is re-run
		return unsubscribe;
	});

	function handleButtonActionWrapper(event: CustomEvent<ActionEventDetail>) {
		handleButtonAction({
			id: event.detail.id,
			activeMode,
			setActiveMode: (mode) => {
				activeMode = mode;
			},
			openFullScreen: openSequenceOverlay
		});
	}

	// Remove selected beat and following beats
	function handleRemoveBeat() {
		const selectedBeatIds = sequenceContainer.state.selectedBeatIds;

		// Check if the start position is selected
		const isStartPositionSelected = selectedBeatIds.includes('start-position');

		if (isStartPositionSelected) {
			// If start position is selected, clear the entire sequence
			// Trigger haptic feedback for deletion
			if (browser) {
				hapticFeedbackService.trigger('error');
			}

			// Clear the entire sequence including start position
			handleClearSequence();

			// Ensure the selection is cleared
			sequenceContainer.clearSelection();
		} else if (selectedBeatIds.length > 0) {
			// Pass the beatId directly to the action
			sequenceActions.removeBeatAndFollowing(selectedBeatIds[0]);

			// Trigger haptic feedback for deletion
			if (browser) {
				hapticFeedbackService.trigger('warning');
			}

			// Clear the selection after removing the beat
			sequenceContainer.clearSelection();
		} else {
			console.warn('No beat selected to remove');
		}
	}

	function handleClearSequence() {
		const event = new CustomEvent<ActionEventDetail>('action', {
			detail: { id: 'clearSequence' }
		});
		hapticFeedbackService.trigger('error');

		handleButtonActionWrapper(event);
	}

	function handleSettingsClick() {
		appActions.openSettings();
	}

	function handleDeleteButtonClick(buttonRect: DOMRect) {
		// Store the button rect
		deleteButtonRect = buttonRect;

		// Open the delete modal
		isDeleteModalOpen = true;
	}

	function handleCloseModal() {
		isDeleteModalOpen = false;
	}

	function enterDeletionMode() {
		isInDeletionMode = true;

		// Close the modal
		isDeleteModalOpen = false;

		// Change cursor to indicate deletion mode with an improved X cursor
		if (beatFrameElement) {
			beatFrameElement.style.cursor =
				"url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23ff5555' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='10' fill='rgba(255,85,85,0.2)'/%3E%3Cline x1='15' y1='9' x2='9' y2='15'%3E%3C/line%3E%3Cline x1='9' y1='9' x2='15' y2='15'%3E%3C/line%3E%3C/svg%3E\") 12 12, no-drop";
		}

		// Show tooltip
		showDeletionModeTooltip();

		// Add event listener to exit deletion mode when clicking outside the beat frame
		document.addEventListener('click', handleDocumentClick);
		document.addEventListener('keydown', handleEscapeKey);
	}

	function exitDeletionMode() {
		isInDeletionMode = false;

		// Reset cursor
		if (beatFrameElement) {
			beatFrameElement.style.cursor = '';
		}

		// Hide tooltip
		hideDeletionModeTooltip();

		// Remove event listeners
		document.removeEventListener('click', handleDocumentClick);
		document.removeEventListener('keydown', handleEscapeKey);
	}

	function showDeletionModeTooltip() {
		// Create tooltip element if it doesn't exist
		if (!deletionModeTooltip) {
			deletionModeTooltip = document.createElement('div');
			deletionModeTooltip.className = 'deletion-mode-tooltip';
			deletionModeTooltip.textContent = 'Click a beat to delete';

			// Position the tooltip relative to the BeatFrame
			if (beatFrameElement) {
				// Append to the BeatFrame container instead of body for proper positioning
				beatFrameElement.appendChild(deletionModeTooltip);
			} else {
				// Fallback to body if BeatFrame element is not available
				document.body.appendChild(deletionModeTooltip);
			}
		}

		// Show tooltip
		if (deletionModeTooltip) {
			deletionModeTooltip.style.display = 'flex';

			// Update position on window resize
			window.addEventListener('resize', updateTooltipPosition);
			// Initial position update
			updateTooltipPosition();
		}
	}

	function updateTooltipPosition() {
		if (deletionModeTooltip && beatFrameElement) {
			// If the tooltip is appended to the body, we need to calculate absolute position
			if (deletionModeTooltip.parentElement === document.body) {
				const beatFrameRect = beatFrameElement.getBoundingClientRect();
				deletionModeTooltip.style.position = 'fixed';
				deletionModeTooltip.style.top = `${beatFrameRect.top - 8}px`;
				deletionModeTooltip.style.left = `${beatFrameRect.left + beatFrameRect.width / 2}px`;
				deletionModeTooltip.style.transform = 'translate(-50%, -100%)';
			}
			// Otherwise, it's already positioned correctly with CSS
		}
	}

	function hideDeletionModeTooltip() {
		if (deletionModeTooltip) {
			deletionModeTooltip.style.display = 'none';
			// Remove resize event listener
			window.removeEventListener('resize', updateTooltipPosition);
		}
	}

	function handleDocumentClick(event: MouseEvent) {
		// Exit deletion mode if clicking outside the beat frame
		if (beatFrameElement && !beatFrameElement.contains(event.target as Node)) {
			exitDeletionMode();
		}
	}

	function handleEscapeKey(event: KeyboardEvent) {
		if (event.key === 'Escape') {
			exitDeletionMode();
		}
	}

	// Handle beat selection during deletion mode
	function handleBeatSelected(event: CustomEvent<{ beatId: string }>) {
		if (isInDeletionMode) {
			// Get the selected beat ID
			const beatId = event.detail.beatId;
			if (beatId) {
				// Pass the beatId directly to the action
				sequenceActions.removeBeatAndFollowing(beatId);

				// Exit deletion mode
				exitDeletionMode();
			}
		}
	}

	let buttonActionListener: (event: CustomEvent) => void;

	onMount(() => {
		buttonActionListener = (event: CustomEvent) => {
			if (event.detail && event.detail.id) {
				handleButtonActionWrapper(event);
			}
		};
		document.addEventListener('action', buttonActionListener as EventListener);
		document.addEventListener('beat-selected', handleBeatSelected as EventListener);
	});

	onDestroy(() => {
		if (buttonActionListener) {
			document.removeEventListener('action', buttonActionListener as EventListener);
		}
		document.removeEventListener('beat-selected', handleBeatSelected as EventListener);
		document.removeEventListener('click', handleDocumentClick);
		document.removeEventListener('keydown', handleEscapeKey);
		window.removeEventListener('resize', updateTooltipPosition);

		// Clean up tooltip
		if (deletionModeTooltip && deletionModeTooltip.parentNode) {
			deletionModeTooltip.parentNode.removeChild(deletionModeTooltip);
			deletionModeTooltip = null;
		}
	});
</script>

{#key null}
	<div class="sequence-widget" use:resizeObserver>
		<div
			class="main-layout"
			class:portrait={workbenchIsPortrait}
			style="--container-width: {$dimensions.width}px;
			   --container-height: {$dimensions.height}px;
			   --button-size-factor: {buttonSizeFactor};"
		>
			<div class="left-vbox">
				<SequenceContent
					containerHeight={$size.height}
					containerWidth={$dimensions.width}
					onBeatSelected={(beatId) => {
						// Create a custom event to match the expected format
						const customEvent = new CustomEvent<{ beatId: string }>('beatselected', {
							detail: { beatId }
						});
						handleBeatSelected(customEvent);
					}}
				/>
			</div>

			<SettingsButton onClick={handleSettingsClick} />
			<DeleteButton onClick={handleDeleteButtonClick} />
			<ClearSequenceButton />
			<SequenceOverlayButton />
			<!-- Ensure ShareButton is rendered with proper props -->
			<ShareButton />

			{#if hasSelectedBeat}
				<RemoveBeatButton onRemoveBeat={handleRemoveBeat} />
			{/if}
		</div>

		<SequenceOverlay title={sequenceName}>
			<SequenceOverlayContent title={sequenceName} />
		</SequenceOverlay>

		<DeleteModal
			isOpen={isDeleteModalOpen}
			{hasSelectedBeat}
			buttonRect={deleteButtonRect}
			on:clearSequence={() => handleClearSequence()}
			on:removeBeat={() => handleRemoveBeat()}
			on:enterDeletionMode={() => enterDeletionMode()}
			on:close={() => handleCloseModal()}
		/>

		{#if isInDeletionMode}
			<div class="deletion-mode-overlay" aria-hidden="true"></div>
		{/if}
	</div>
{/key}

<style>
	.sequence-widget {
		display: flex;
		flex-direction: column;
		height: 100%;
		flex: 1;
	}

	.main-layout {
		display: flex;
		flex-direction: row;
		height: 100%;
		width: 100%;
		overflow: hidden;
		justify-content: space-between;
		position: relative;
	}

	.main-layout.portrait {
		flex-direction: column;
		justify-content: flex-start;
	}

	.left-vbox {
		display: flex;
		flex-direction: column;
		height: 100%;
		width: 100%;
		min-height: 0;
		flex: 1;
		overflow: hidden;
		transition: all 0.3s ease-out;
	}

	.main-layout {
		transition: flex-direction 0.3s ease-out;
	}

	/* Deletion mode styles */
	.deletion-mode-overlay {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		pointer-events: none;
		border: 2px solid rgba(255, 85, 85, 0.7);
		border-radius: 8px;
		box-shadow: 0 0 10px rgba(255, 85, 85, 0.3);
		animation: pulse 2s infinite;
		z-index: 30;
	}

	@keyframes pulse {
		0% {
			box-shadow: 0 0 0 0 rgba(255, 85, 85, 0.4);
			border-color: rgba(255, 85, 85, 0.7);
		}
		50% {
			box-shadow: 0 0 8px 0 rgba(255, 85, 85, 0.5);
			border-color: rgba(255, 85, 85, 0.9);
		}
		100% {
			box-shadow: 0 0 0 0 rgba(255, 85, 85, 0.4);
			border-color: rgba(255, 85, 85, 0.7);
		}
	}

	:global(.deletion-mode-tooltip) {
		position: absolute;
		top: 0;
		left: 50%;
		transform: translate(-50%, -100%) translateY(-8px);
		background-color: rgba(255, 85, 85, 0.7);
		color: white;
		padding: 4px 8px;
		border-radius: 4px;
		font-size: 12px;
		font-weight: 400;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
		z-index: 90; /* Lower than popup menu (100) but higher than most UI elements */
		pointer-events: none;
		white-space: nowrap;
		border: 1px solid rgba(255, 60, 60, 0.8);
		height: 24px;
		display: flex;
		align-items: center;
		justify-content: center;
		animation: tooltipFadeIn 0.25s ease-out;
	}

	/* Add a small arrow pointing down */
	:global(.deletion-mode-tooltip::after) {
		content: '';
		position: absolute;
		top: 100%;
		left: 50%;
		margin-left: -5px;
		border-width: 5px;
		border-style: solid;
		border-color: rgba(255, 85, 85, 0.7) transparent transparent transparent;
	}

	@keyframes tooltipFadeIn {
		from {
			opacity: 0;
			transform: translate(-50%, -100%) translateY(-16px);
		}
		to {
			opacity: 1;
			transform: translate(-50%, -100%) translateY(-8px);
		}
	}
</style>
