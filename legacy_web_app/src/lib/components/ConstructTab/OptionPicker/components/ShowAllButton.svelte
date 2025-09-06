<script lang="ts">
	import { createEventDispatcher, getContext } from 'svelte';
	// Removed: fly, quintOut
	import { LAYOUT_CONTEXT_KEY, type LayoutContext } from '../layoutContext';

	// --- Props ---
	export let showAllActive: boolean = false;

	// --- Context ---
	// Keep context if needed for internal styling (e.g., mobile class for padding/font)
	const layoutContext = getContext<LayoutContext>(LAYOUT_CONTEXT_KEY);
	$: isMobileDevice = $layoutContext.isMobile;

	// --- Computed ---
	$: buttonState = {
		text: showAllActive ? 'Filters Off' : 'Show All',
		icon: showAllActive ? '👁️' : '✨',
		ariaLabel: showAllActive ? 'Enable filters and sorting' : 'Show all options without filtering'
	};

	// --- Events ---
	const dispatch = createEventDispatcher<{ toggle: void }>();
	const handleToggle = () => dispatch('toggle');
</script>

<button
	class="show-all-button"
	class:mobile={isMobileDevice}
	class:active={showAllActive}
	on:click={handleToggle}
	aria-pressed={showAllActive}
	aria-label={buttonState.ariaLabel}
	data-testid="show-all-button"
	>
	<span class="icon" aria-hidden="true">{buttonState.icon}</span>
	<span class="text">{buttonState.text}</span>
</button>

<style>
	.show-all-button {
		display: flex;
		align-items: center;
		gap: clamp(4px, 1vw, 6px);
		background-color: #ffffff;
		border: 1px solid #e2e8f0;
		border-radius: 6px;
		padding: clamp(5px, 1.2vw, 8px) clamp(8px, 1.8vw, 12px);
		font-size: clamp(0.75rem, 2vw, 0.9rem);
		font-weight: 500;
		color: #374151;
		cursor: pointer;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
		transition:
			background-color 0.2s ease,
			border-color 0.2s ease,
			color 0.2s ease,
			box-shadow 0.2s ease,
			transform 0.1s ease;
		white-space: nowrap;
	}
	.show-all-button .icon {
		font-size: 1.2em;
		line-height: 1;
	}
	.show-all-button:hover {
		background-color: #f9fafb;
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
	}
	.show-all-button.active {
		background-color: #e0f2fe;
		border-color: #7dd3fc;
		color: #0c4a6e;
	}
	.show-all-button.active:hover {
		background-color: #bae6fd;
	}
	.show-all-button:active {
		box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
		transform: scale(0.98);
	}
	.show-all-button:focus-visible {
		outline: 2px solid #4299e1;
		outline-offset: 1px;
	}
	/* Style adjustments for mobile if needed */
	.show-all-button.mobile {
		padding: clamp(4px, 1vw, 6px) clamp(6px, 1.5vw, 10px);
		font-size: clamp(0.7rem, 1.8vw, 0.85rem);
	}
</style>
