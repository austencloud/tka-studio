<script lang="ts">
	import type { PictographData } from '$lib/types/PictographData';
	import SectionHeader from '../SectionHeader.svelte';
	import OptionGroupGrid from '../OptionGroupGrid.svelte';
	import type { Action } from 'svelte/action';
	import { onMount, onDestroy } from 'svelte'; // Import onMount and onDestroy for cleanup

	// Props
	export let groups: Array<{ key: string; options: PictographData[] }>;
	export let transitionKey: string | number;
	export let rowIndex: number;

	/**
	 * Debounce utility function.
	 * Creates a debounced function that delays invoking the input function until
	 * after 'delay' milliseconds have elapsed since the last time the debounced
	 * function was invoked.
	 */
	function debounce<T extends (...args: any[]) => any>(
		func: T,
		delay: number
	): (...args: Parameters<T>) => void {
		let timeoutId: ReturnType<typeof setTimeout> | null = null;
		return (...args: Parameters<T>) => {
			if (timeoutId !== null) {
				clearTimeout(timeoutId);
			}
			timeoutId = setTimeout(() => {
				func(...args);
				timeoutId = null;
			}, delay);
		};
	}

	// Action to handle multi-group row overflow detection and prevention
	const setupMultiGroupRow: Action<HTMLElement> = (node) => {
		let resizeObserver: ResizeObserver | null = null;
		let debouncedCheckOverflow: () => void;

		// Function to get the minimum width based on screen size
		function getMinGroupWidth(): number {
			// Check if window is defined (for SSR safety, though less critical in action)
			if (typeof window === 'undefined') return 140; // Default if no window
			if (window.innerWidth <= 380) {
				return 80; // Minimum width for very small screens
			} else if (window.innerWidth <= 640) {
				return 100; // Minimum width for small screens
			} else {
				return 140; // Default minimum width
			}
		}

		// Function to get margin and padding values based on screen size
		function getSpacingValues() {
			// Assuming 1rem = 16px for calculations
			const remInPx = 16;
			if (typeof window === 'undefined') {
				// SSR safety
				return {
					margin: 0.25 * remInPx * 2,
					padding: 0.25 * remInPx * 2,
					gap: 0.25 * remInPx
				};
			}
			if (window.innerWidth <= 640) {
				return {
					margin: 0.1 * remInPx * 2,
					padding: 0.1 * remInPx * 2,
					gap: 0.1 * remInPx
				};
			} else {
				return {
					margin: 0.25 * remInPx * 2,
					padding: 0.25 * remInPx * 2,
					gap: 0.25 * remInPx
				};
			}
		}

		// Function to check and handle overflow
		function checkOverflow() {
			if (!node) return; // Ensure node is still available

			const groupItems = node.querySelectorAll<HTMLElement>('.multi-group-item');
			if (groupItems.length < 2) return;

			const containerWidth = node.clientWidth;
			const minGroupWidth = getMinGroupWidth();
			const { margin, padding, gap } = getSpacingValues();
			const itemWidth = minGroupWidth + margin + padding;
			const totalMinWidth = itemWidth * groupItems.length + gap * (groupItems.length - 1);
			const wouldOverflow = totalMinWidth > containerWidth;

			groupItems.forEach((item, index) => {
				// Force new row only on the *last* item if it would overflow
				// and remove from others.
				if (wouldOverflow && index === groupItems.length - 1) {
					item.classList.add('force-new-row');
				} else {
					item.classList.remove('force-new-row');
				}
			});


		}

		// Debounce the checkOverflow function for window resize
		debouncedCheckOverflow = debounce(checkOverflow, 150);

		if (typeof ResizeObserver !== 'undefined') {
			resizeObserver = new ResizeObserver(() => {
				checkOverflow(); // ResizeObserver is usually already optimized
			});
			resizeObserver.observe(node);
		}

		// Listen for window resize events (debounced)
		const handleWindowResize = () => {
			debouncedCheckOverflow();
		};

		if (typeof window !== 'undefined') {
			window.addEventListener('resize', handleWindowResize);
			// Initial check
			setTimeout(checkOverflow, 0);
		}

		return {
			destroy() {
				if (resizeObserver) {
					resizeObserver.disconnect();
				}
				if (typeof window !== 'undefined') {
					window.removeEventListener('resize', handleWindowResize);
				}
			}
		};
	};
</script>

<div class="multi-group-row" use:setupMultiGroupRow>
	{#each groups as group, groupIndex (transitionKey + '-multi-' + group.key)}
		<div class="multi-group-item" data-group-index={groupIndex}>
			<SectionHeader
				groupKey={group.key}
				isFirstHeader={rowIndex === 0 && groupIndex === 0}
				isCompact={true}
			/>
			<OptionGroupGrid options={group.options} key={transitionKey + '-multiopt-' + group.key} />
		</div>
	{/each}
</div>

<style>
	/* Styles moved from OptionsPanel.svelte */
	.multi-group-row {
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		justify-content: space-evenly; /* Distributes space, good for varying item counts */
		align-items: flex-start; /* Align items to the top of the row */
		width: 100%;
		background-color: rgba(0, 0, 0, 0.01); /* Subtle background for the row */
		gap: 0.25rem; /* Consistent gap between items */
	}

	.multi-group-item {
		display: flex;
		flex-direction: column;
		align-items: center; /* Center content (header, grid) within the item */
		min-width: 140px; /* Minimum width before wrapping or shrinking too much */
		flex: 1; /* Allow items to grow and share space */
		margin: 0.25rem; /* Margin around each item */
		padding: 0.25rem; /* Padding inside each item */
		border-radius: 12px; /* Rounded corners for items */
		transition: all 0.2s ease-out;
	}


	@media (max-width: 640px) {
		.multi-group-row {
			gap: 0.1rem;
		}
		.multi-group-item {
			min-width: 100px;
			margin: 0.1rem;
			padding: 0.1rem;
		}
	}

	@media (max-width: 380px) {
		.multi-group-item {
			min-width: 80px; /* Further reduce min-width for very small screens */
		}
	}
</style>
