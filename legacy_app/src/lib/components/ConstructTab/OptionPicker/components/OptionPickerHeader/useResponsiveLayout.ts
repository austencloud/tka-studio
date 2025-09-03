// src/lib/components/ConstructTab/OptionPicker/components/OptionPickerHeader/useResponsiveLayout.ts
import { writable, get } from 'svelte/store';
import type { LayoutContext } from '../../layoutContext';
import { onMount, onDestroy } from 'svelte';

/**
 * Hook to manage responsive layout state
 * @param layoutContext The layout context from the parent component
 * @returns An object containing responsive layout state and functions
 */
export function useResponsiveLayout(layoutContext: LayoutContext | null) {
	// Local state as Svelte stores
	const isMobileDevice = writable(false);
	const useShortLabels = writable(false);
	const tabsContainerRef = writable<HTMLDivElement | null>(null);
	const isScrollable = writable(false);
	const compactMode = writable(false);
	const showScrollIndicator = writable(false);

	let currentTabsContainerRef: HTMLDivElement | null = null;
	const unsubscribetabsContainerRef = tabsContainerRef.subscribe((value) => {
		currentTabsContainerRef = value;
	});

	// Function to check if tabs are overflowing
	function checkTabsOverflow() {
		if (!currentTabsContainerRef) return;

		const { scrollWidth, clientWidth } = currentTabsContainerRef;
		const newIsScrollable = scrollWidth > clientWidth;
		isScrollable.set(newIsScrollable);

		const isNearlyOverflowing = scrollWidth > clientWidth - 20;

		if ((newIsScrollable || isNearlyOverflowing) && !get(compactMode)) {
			compactMode.set(true);
			// Force a re-check after a short delay to see if compact mode fixed the overflow
			setTimeout(() => {
				if (currentTabsContainerRef) {
					const { scrollWidth, clientWidth } = currentTabsContainerRef;
					isScrollable.set(scrollWidth > clientWidth);
					showScrollIndicator.set(get(isScrollable));
				}
			}, 50);
		}
		showScrollIndicator.set(newIsScrollable);
	}

	onMount(() => {
		const contextValue = layoutContext;

		const updateMobileState = () => {
			let mobile = false;
			if (contextValue && typeof contextValue === 'object' && 'isMobile' in contextValue) {
				mobile = Boolean(contextValue.isMobile);
			} else {
				mobile = window.innerWidth <= 640;
			}
			isMobileDevice.set(mobile);
			if (mobile) {
				compactMode.set(true);
			}
		};

		updateMobileState(); // Initial check

		const handleResize = () => {
			updateMobileState();
			if (currentTabsContainerRef) {
				checkTabsOverflow();
			}
		};

		window.addEventListener('resize', handleResize);

		// Determine when to use short labels
		const unsubscribeIsMobileDevice = isMobileDevice.subscribe((value) => {
			useShortLabels.set(value || get(compactMode));
		});
		const unsubscribeCompactMode = compactMode.subscribe((value) => {
			useShortLabels.set(get(isMobileDevice) || value);
		});

		// Check if tabs are scrollable when tabsContainerRef changes or on mount
		const unsubscribeTabsRefForOverflow = tabsContainerRef.subscribe((ref) => {
			if (ref) {
				checkTabsOverflow();
				// Add resize observer to check for overflow
				const resizeObserver = new ResizeObserver(() => {
					checkTabsOverflow();
				});
				resizeObserver.observe(ref);
				// Cleanup observer on new ref or unmount
				return () => {
					resizeObserver.disconnect();
				};
			}
		});

		return () => {
			window.removeEventListener('resize', handleResize);
			unsubscribeIsMobileDevice();
			unsubscribeCompactMode();
			unsubscribetabsContainerRef();
			unsubscribeTabsRefForOverflow();
		};
	});

	// Handle scroll events to update scroll indicator
	function handleScroll() {
		if (!currentTabsContainerRef) return;
		const { scrollLeft, scrollWidth, clientWidth } = currentTabsContainerRef;
		showScrollIndicator.set(scrollLeft + clientWidth < scrollWidth - 10);
	}

	return {
		isMobileDevice,
		useShortLabels,
		tabsContainerRef,
		isScrollable,
		compactMode,
		showScrollIndicator,
		handleScroll,
		checkTabsOverflow
	};
}
