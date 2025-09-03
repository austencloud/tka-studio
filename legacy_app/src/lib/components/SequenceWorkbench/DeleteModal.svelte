<!-- src/lib/components/SequenceWorkbench/DeleteModal.svelte -->
<script lang="ts">
	import { fade, scale } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import { createEventDispatcher } from 'svelte';

	// Props
	const { isOpen = false, hasSelectedBeat = false, buttonRect = null } = $props();

	// Event dispatcher
	const dispatch = createEventDispatcher<{
		clearSequence: void;
		removeBeat: void;
		enterDeletionMode: void;
		close: void;
	}>();

	function handleClearSequence() {
		dispatch('clearSequence');
		close();
	}

	function handleRemoveBeat() {
		if (hasSelectedBeat) {
			dispatch('removeBeat');
			close();
		} else {
			dispatch('enterDeletionMode');
			close();
		}
	}

	function close() {
		dispatch('close');
	}

	function handleBackdropClick(event: MouseEvent) {
		if (event.target === event.currentTarget) {
			close();
		}
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape') {
			close();
		}
	}

	// Calculate popup position and properties
	let popupPosition = $state({
		left: 0,
		position: '',
		arrowOffset: 0,
		positionAbove: true
	});

	// Update popup position when buttonRect changes
	$effect(() => {
		if (!buttonRect) return;

		// Get viewport dimensions
		const viewportHeight = window.innerHeight;
		const viewportWidth = window.innerWidth;

		// Modal dimensions (approximate)
		const modalWidth = 280;
		const modalHeight = 220; // Approximate height

		// Calculate the center point of the button
		const buttonCenterX = buttonRect.left + buttonRect.width / 2;
		const buttonTop = buttonRect.top;

		// Determine if there's enough space above the button
		const positionAbove = buttonTop > modalHeight + 20;

		// Calculate left position, ensuring the modal stays within viewport
		let left = Math.max(
			modalWidth / 2 + 10, // Left edge + padding
			Math.min(
				buttonCenterX,
				viewportWidth - modalWidth / 2 - 10 // Right edge - half modal width - padding
			)
		);

		// Calculate top or bottom position based on whether we're showing above or below
		let position = positionAbove
			? `bottom: ${viewportHeight - buttonTop + 12}px;` // Position above with gap
			: `top: ${buttonTop + buttonRect.height + 12}px;`; // Position below with gap

		// Calculate the arrow position (relative to the modal center)
		const arrowOffset = buttonCenterX - left;

		// Update the state
		popupPosition = {
			left,
			position,
			arrowOffset,
			positionAbove
		};
	});

	// Compute the style string
	const popupStyle = $derived(
		buttonRect
			? `left: ${popupPosition.left}px; ${popupPosition.position} --arrow-offset: ${popupPosition.arrowOffset}px; --position-above: ${popupPosition.positionAbove ? '1' : '0'};`
			: ''
	);
</script>

<svelte:window onkeydown={handleKeydown} />

{#if isOpen}
	<div
		class="popup-backdrop"
		onclick={handleBackdropClick}
		onkeydown={handleKeydown}
		role="dialog"
		aria-modal="true"
		aria-labelledby="delete-popup-title"
		tabindex="-1"
		transition:fade={{ duration: 200 }}
	>
		<!-- Positioned popup that animates from the delete button -->
		<div
			class="popup-container"
			style={popupStyle}
			data-testid="delete-popup-container"
			in:scale={{
				duration: 300,
				delay: 50,
				opacity: 0,
				start: 0.8,
				easing: quintOut
			}}
			style:transform="translateX(-50%)"
			style:transform-origin={`calc(50% + var(--arrow-offset)) ${popupPosition.positionAbove ? '100%' : '0%'}`}
		>
			<div class="popup-content">
				<div class="option-buttons">
					<button class="option-button remove-beat" onclick={handleRemoveBeat}>
						<div class="option-icon">
							<i class="fa-solid fa-trash"></i>
						</div>
						<div class="option-text">
							<span class="option-title">Remove Selected Beat</span>
							<span class="option-description">
								{hasSelectedBeat
									? 'Delete the currently selected beat'
									: 'Click a beat to delete it'}
							</span>
						</div>
					</button>

					<button class="option-button clear-sequence" onclick={handleClearSequence}>
						<div class="option-icon">
							<i class="fa-solid fa-eraser"></i>
						</div>
						<div class="option-text">
							<span class="option-title">Clear Entire Sequence</span>
							<span class="option-description">Remove all beats and reset start position</span>
						</div>
					</button>
				</div>

				<div class="popup-footer">
					<button class="cancel-button" onclick={close}>Cancel</button>
				</div>
			</div>
		</div>
	</div>
{/if}

<style>
	.popup-backdrop {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.3);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 100;
		pointer-events: all;
		cursor: default;
	}

	.popup-container {
		position: fixed;
		transform: translateX(-50%); /* Center horizontally relative to button */
		background-color: var(--tkc-button-panel-background, #2a2a2e);
		border-radius: 8px;
		box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
		width: 280px;
		max-width: 90vw;
		max-height: calc(100vh - 100px);
		display: flex;
		flex-direction: column;
		overflow: hidden;
		z-index: 101;
		margin-bottom: 12px; /* Space between button and popup */
	}

	.popup-content {
		padding: 1rem;
		overflow-y: auto;
		color: #e0e0e0;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.option-buttons {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.option-button {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 0.75rem;
		border-radius: 6px;
		border: 1px solid rgba(255, 255, 255, 0.1);
		background-color: rgba(255, 255, 255, 0.05);
		cursor: pointer;
		transition: all 0.2s ease;
		text-align: left;
		color: inherit;
	}

	.option-button:hover {
		background-color: rgba(255, 255, 255, 0.1);
		transform: translateY(-2px) scale(1.02);
		filter: brightness(1.1);
	}

	.option-button:active {
		transform: translateY(0) scale(0.98);
	}

	.option-button.remove-beat {
		border-left: 3px solid #ff9e00;
	}

	.option-button.clear-sequence {
		border-left: 3px solid #ff5555;
	}

	.option-icon {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 36px;
		height: 36px;
		border-radius: 50%;
		background-color: rgba(255, 255, 255, 0.1);
		flex-shrink: 0;
	}

	.option-button.remove-beat .option-icon {
		color: #ff9e00;
	}

	.option-button.clear-sequence .option-icon {
		color: #ff5555;
	}

	.option-text {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.option-title {
		font-weight: 600;
		font-size: 0.95rem;
	}

	.option-description {
		font-size: 0.8rem;
		color: rgba(255, 255, 255, 0.7);
	}

	.popup-footer {
		display: flex;
		justify-content: flex-end;
		padding-top: 0.5rem;
		border-top: 1px solid rgba(255, 255, 255, 0.1);
	}

	.cancel-button {
		padding: 0.5rem 0.75rem;
		border-radius: 4px;
		background-color: rgba(255, 255, 255, 0.1);
		color: #e0e0e0;
		border: none;
		cursor: pointer;
		transition: all 0.2s ease;
		font-size: 0.85rem;
	}

	.cancel-button:hover {
		background-color: rgba(255, 255, 255, 0.2);
		transform: translateY(-1px);
	}

	/* Add a small arrow pointing to the button */
	.popup-container::after {
		content: '';
		position: absolute;
		left: calc(50% + var(--arrow-offset, 0px));
		transform: translateX(-50%);
		width: 16px;
		height: 16px;
		background-color: var(--tkc-button-panel-background, #2a2a2e);
		border: 1px solid rgba(255, 255, 255, 0.1);
		transform: translateX(-50%) rotate(45deg);
		z-index: -1;

		/* Position based on whether the modal is above or below the button */
		bottom: calc(var(--position-above, 1) * -8px);
		top: calc((1 - var(--position-above, 1)) * -8px);

		/* Set the correct border sides based on position */
		border-top: calc((1 - var(--position-above, 1)) * 1px) solid rgba(255, 255, 255, 0.1);
		border-left: calc((1 - var(--position-above, 1)) * 1px) solid rgba(255, 255, 255, 0.1);
		border-bottom: calc(var(--position-above, 1) * 1px) solid rgba(255, 255, 255, 0.1);
		border-right: calc(var(--position-above, 1) * 1px) solid rgba(255, 255, 255, 0.1);
	}

	/* Add a subtle glow effect to connect the button and modal */
	.popup-container::before {
		content: '';
		position: absolute;
		left: calc(50% + var(--arrow-offset, 0px));
		width: 30px;
		height: 30px;
		border-radius: 50%;
		background: radial-gradient(circle, rgba(108, 156, 233, 0.2) 0%, rgba(108, 156, 233, 0) 70%);
		transform: translateX(-50%);

		/* Position based on whether the modal is above or below the button */
		bottom: calc(var(--position-above, 1) * -15px);
		top: calc((1 - var(--position-above, 1)) * -15px);
		z-index: -2;
		pointer-events: none;
	}

	/* Responsive adjustments */
	@media (max-width: 480px) {
		.popup-container {
			width: 240px;
		}

		.option-icon {
			width: 32px;
			height: 32px;
		}

		.option-title {
			font-size: 0.9rem;
		}

		.option-description {
			font-size: 0.75rem;
		}
	}
</style>
