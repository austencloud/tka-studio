<!-- src/lib/components/ConstructTab/OptionPicker/components/OptionPickerHeader/TabsContainer.svelte -->
<script lang="ts">
	import { get, type Writable } from 'svelte/store';
	import TabButton from './TabButton.svelte';
	import ScrollIndicator from './ScrollIndicator.svelte';
	import { fade } from 'svelte/transition';

	// Props
	const props = $props<{
		selectedTab: string | null;
		categoryKeys: string[];
		isScrollable: boolean;
		showScrollIndicator: boolean;
		useShortLabels: boolean;
		isMobileDevice: boolean; // Keep if used directly for styling/logic within TabsContainer
		compactMode: boolean; // Keep if used directly for styling/logic
		tabsContainerRefStore?: Writable<HTMLDivElement | null>; // Expects the store itself
		onScroll?: () => void; // Event handler for scroll
	}>();

	// Local state for the DOM element and scroll position
	let actualTabsContainerElement = $state<HTMLDivElement | null>(null);
	let scrollPosition = $state(0);
	let maxScroll = $state(0);
	let showTooltip = $state(false);

	// Show tooltip after a delay
	setTimeout(() => {
		showTooltip = true;
		// Hide tooltip after 5 seconds
		setTimeout(() => {
			showTooltip = false;
		}, 5000);
	}, 1000);

	$effect(() => {
		if (props.tabsContainerRefStore) {
			props.tabsContainerRefStore.set(actualTabsContainerElement);
		}
		// Optional: Cleanup when the element is unmounted or store changes
		// This might be more robustly handled by the hook's onDestroy if the hook manages the lifecycle
		return () => {
			if (
				props.tabsContainerRefStore &&
				actualTabsContainerElement &&
				get(props.tabsContainerRefStore) === actualTabsContainerElement
			) {
				// If the hook doesn't clear it on its own destroy, uncommenting this might be useful.
				// props.tabsContainerRefStore.set(null);
			}
		};
	});

	// Forward scroll event if onScroll prop is provided and update scroll position
	function handleScroll() {
		if (props.onScroll) {
			props.onScroll();
		}

		if (actualTabsContainerElement) {
			scrollPosition = actualTabsContainerElement.scrollLeft;
			maxScroll = actualTabsContainerElement.scrollWidth - actualTabsContainerElement.clientWidth;
		}
	}

	// Update maxScroll when the component mounts or when tabs change
	$effect(() => {
		if (actualTabsContainerElement) {
			maxScroll = actualTabsContainerElement.scrollWidth - actualTabsContainerElement.clientWidth;
		}
	});
</script>

{#if props.categoryKeys && props.categoryKeys.length > 0}
	<div class="tabs-wrapper">
		<!-- Left scroll indicator -->
		{#if props.isScrollable && scrollPosition > 20}
			<div class="scroll-hint left" transition:fade={{ duration: 200 }}>
				<div class="scroll-arrow">←</div>
				<div class="scroll-hint-text">More</div>
			</div>
		{/if}

		<div
			class="tabs"
			role="tablist"
			bind:this={actualTabsContainerElement}
			class:scrollable={props.isScrollable}
			onscroll={handleScroll}
		>
			<div class="tabs-inner-container">
				{#each props.categoryKeys as categoryKey, index (categoryKey)}
					<TabButton
						{categoryKey}
						isActive={props.selectedTab === categoryKey}
						isFirstTab={index === 0}
						isLastTab={index === props.categoryKeys.length - 1}
						useShortLabels={props.useShortLabels}
						tabFlexBasis={`${100 / props.categoryKeys.length}%`}
						{index}
						totalTabs={props.categoryKeys.length}
					/>
				{/each}
			</div>

			<!-- Tooltip to indicate more options in other tabs -->
			{#if showTooltip && props.categoryKeys.length > 1}
				<div class="tabs-tooltip" transition:fade={{ duration: 300 }}>
					<div class="tooltip-content">
						Explore {props.categoryKeys.length} categories
					</div>
				</div>
			{/if}
		</div>

		<!-- Right scroll indicator -->
		{#if props.isScrollable && scrollPosition < maxScroll - 20}
			<div class="scroll-hint right" transition:fade={{ duration: 200 }}>
				<div class="scroll-arrow">→</div>
				<div class="scroll-hint-text">More</div>
			</div>
		{/if}
	</div>

	{#if props.showScrollIndicator}
		<ScrollIndicator show={props.isScrollable} />
	{/if}
{:else}
	<!-- Placeholder when tabs are shown but empty -->
	<div class="tabs-placeholder">
		<span class="no-categories-message">No sub-categories</span>
	</div>
{/if}

<style>
	/* Wrapper for tabs and scroll indicators */
	.tabs-wrapper {
		display: flex;
		position: relative;
		width: 100%;
		align-items: center;
		margin-bottom: 4px;
	}

	.tabs {
		display: flex;
		justify-content: flex-start;
		flex-wrap: nowrap; /* Prevent tabs from wrapping to a new line */
		padding: 0;
		margin: 0;
		flex-grow: 1; /* Allow tabs container to grow */
		flex-shrink: 1;
		flex-basis: 0;
		min-width: 50px;
		overflow-x: auto; /* Enable horizontal scrolling */
		scrollbar-width: thin; /* For Firefox */
		scrollbar-color: rgba(255, 255, 255, 0.3) transparent; /* For Firefox */
		-ms-overflow-style: none; /* Hide scrollbar in IE and Edge */
		position: relative; /* For scroll indicator positioning */
		padding-bottom: 4px; /* Space for scrollbar */
		/* Add padding to prevent border clipping */
		padding-top: 2px;
		padding-left: 2px;
		padding-right: 2px;
		width: 100%; /* Ensure .tabs itself takes full available width from parent */
		scroll-behavior: smooth; /* Smooth scrolling for better UX */
		transition: all 0.3s ease; /* Smooth transitions */
	}

	.tabs-inner-container {
		display: flex; /* Make this a flex container */
		width: 100%; /* Make it take the full width of .tabs */
		min-width: max-content; /* Ensure it's wide enough for all tabs if not scrollable */
		gap: 4px;
		padding: 0 4px;
		/* Ensure inner container doesn't clip borders */
		margin: 0 -2px; /* Compensate for tabs padding */
		position: relative; /* For tooltip positioning */
	}

	/* Hide scrollbar in Webkit browsers by default */
	.tabs::-webkit-scrollbar {
		height: 4px;
		background: transparent;
	}

	.tabs::-webkit-scrollbar-thumb {
		background-color: rgba(255, 255, 255, 0.3);
		border-radius: 4px;
	}

	/* Show scrollbar on hover for better UX */
	.tabs:hover::-webkit-scrollbar {
		height: 6px;
	}

	/* Scrollable class for visual indication */
	.tabs.scrollable {
		padding-right: 20px; /* Space for scroll indicator */
		mask-image: linear-gradient(to right, transparent, black 10px, black 90%, transparent);
		-webkit-mask-image: linear-gradient(to right, transparent, black 10px, black 90%, transparent);
	}

	/* Scroll hint indicators */
	.scroll-hint {
		position: absolute;
		top: 50%;
		transform: translateY(-50%);
		background: rgba(15, 23, 42, 0.8);
		border: 1px solid rgba(148, 163, 184, 0.3);
		border-radius: 8px;
		padding: 4px 8px;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		z-index: 10;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
		pointer-events: none; /* Don't block clicks */
		color: #e2e8f0;
	}

	.scroll-hint.left {
		left: 0;
	}

	.scroll-hint.right {
		right: 0;
	}

	.scroll-arrow {
		font-size: 1.2rem;
		font-weight: bold;
		color: #38bdf8;
		margin-bottom: 2px;
	}

	.scroll-hint-text {
		font-size: 0.7rem;
		opacity: 0.8;
	}

	/* Tooltip for category exploration */
	.tabs-tooltip {
		position: absolute;
		top: -40px;
		left: 50%;
		transform: translateX(-50%);
		background: rgba(15, 23, 42, 0.9);
		border: 1px solid #38bdf8;
		border-radius: 8px;
		padding: 6px 12px;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
		z-index: 20;
		pointer-events: none;
	}

	.tooltip-content {
		color: #f8fafc;
		font-size: 0.85rem;
		white-space: nowrap;
	}

	.tooltip-content::after {
		content: '';
		position: absolute;
		bottom: -8px;
		left: 50%;
		transform: translateX(-50%);
		border-left: 8px solid transparent;
		border-right: 8px solid transparent;
		border-top: 8px solid rgba(15, 23, 42, 0.9);
	}

	/* Placeholder used only for "No sub-categories" message */
	.tabs-placeholder {
		display: flex;
		justify-content: flex-start; /* Align message left */
		align-items: center;
		flex-grow: 1;
		flex-shrink: 1;
		flex-basis: 0;
		min-width: 50px;
		min-height: 30px; /* Ensure it has some height */
	}

	.no-categories-message {
		color: #94a3b8;
		font-style: italic;
		padding: clamp(0.4rem, 1vw, 0.6rem) clamp(0.8rem, 1.5vw, 1.2rem);
		white-space: nowrap;
		/* text-align: center; Removed, placeholder is justify-content: flex-start */
	}

	/* Mobile styles */
	@media (max-width: 640px) {
		.tabs-placeholder {
			justify-content: flex-start; /* Ensure "No sub-categories" aligns left */
		}

		.no-categories-message {
			font-size: 0.9rem;
			padding: 0.4rem 0.6rem;
		}

		/* Reduce gap between tabs */
		.tabs-inner-container {
			gap: 2px;
		}

		/* Adjust tooltip position */
		.tabs-tooltip {
			top: -35px;
			padding: 4px 8px;
		}

		.tooltip-content {
			font-size: 0.75rem;
		}
	}

	/* Very small screens */
	@media (max-width: 480px) {
		/* Further reduce gap between tabs */
		.tabs-inner-container {
			gap: 1px;
		}

		/* Hide scroll hint text on very small screens */
		.scroll-hint-text {
			display: none;
		}

		.scroll-hint {
			padding: 2px 4px;
		}
	}
</style>
