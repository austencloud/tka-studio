<script lang="ts">
	import { onMount, setContext } from 'svelte';
	import { writable, derived, type Readable } from 'svelte/store';
	import { get } from 'svelte/store';
	import { uiState, filteredOptionsStore, groupedOptionsStore, actions } from './store';
	// Ensure layoutUtils imports are correct
	import { getResponsiveLayout, getEnhancedDeviceType } from './utils/layoutUtils';
	import { getContainerAspect, BREAKPOINTS } from './config';
	import { LAYOUT_CONTEXT_KEY, type LayoutContextValue } from './layoutContext';
	import OptionDisplayArea from './components/OptionDisplayArea.svelte';
	import { resize } from './actions/resize';
	import type { ViewModeDetail } from './components/ViewControl/types';
	import sequenceDataService, { type SequenceBeat } from '$lib/services/SequenceDataService';
	import type { PictographData } from '$lib/types/PictographData';
	import type { TKAPosition } from '$lib/types/TKAPosition';
	import type { MotionData } from '$lib/components/objects/Motion/MotionData';
	import { sequenceStore } from '$lib/state/stores/sequenceStore';
	import type {
		Color,
		MotionType,
		Orientation,
		PropRotDir,
		Loc,
		TKATurns,
		VTGTiming,
		VTGDir
	} from '$lib/types/Types';
	// Import the loading state store
	import transitionLoading from '$lib/state/stores/ui/transitionLoadingStore';
	import OptionPickerHeader from './components/OptionPickerHeader';

	// --- State Stores ---
	// Use sensible defaults for window dimensions
	const windowWidth = writable(
		typeof window !== 'undefined' ? window.innerWidth : BREAKPOINTS.desktop
	);
	const windowHeight = writable(typeof window !== 'undefined' ? window.innerHeight : 768);

	// Initialize container dimensions with fallback values to avoid invalid dimensions
	// This helps prevent the "getResponsiveLayout called with invalid dimensions" error
	const containerWidth = writable(
		typeof window !== 'undefined' ? Math.max(300, window.innerWidth * 0.8) : BREAKPOINTS.desktop
	);
	const containerHeight = writable(
		typeof window !== 'undefined' ? Math.max(200, window.innerHeight * 0.6) : 768
	);
	const selectedTab = writable<string | null>(null); // Tracks the currently selected category tab ('all' or specific key)

	// --- Type Safety Helpers ---
	/**
	 * Safely cast a string to a TKAPosition
	 * Returns null if the value isn't a valid TKAPosition
	 */
	function safeAsTKAPosition(value: string | undefined): TKAPosition | null {
		// This regex validates alpha1-8, beta1-8, gamma1-16
		const validPattern = /^(alpha[1-8]|beta[1-8]|gamma([1-9]|1[0-6]))$/;

		if (!value || !validPattern.test(value)) {
			return null;
		}

		return value as TKAPosition;
	}

	/**
	 * Check if a string is a valid MotionType
	 */
	function isValidMotionType(value: string): value is MotionType {
		return ['anti', 'pro', 'static', 'dash', 'float'].includes(value);
	}

	/**
	 * Check if a string is a valid Orientation
	 */
	function isValidOrientation(value: string): value is Orientation {
		return ['in', 'out', 'clock', 'counter'].includes(value);
	}

	/**
	 * Check if a string is a valid PropRotDir
	 */
	function isValidPropRotDir(value: string): value is PropRotDir {
		return ['cw', 'ccw', 'no_rot'].includes(value);
	}

	/**
	 * Check if a string is a valid Loc
	 */
	function isValidLoc(value: string): value is Loc {
		return ['n', 's', 'e', 'w', 'ne', 'se', 'sw', 'nw'].includes(value);
	}

	/**
	 * Safely convert a value to TKATurns
	 */
	function safeAsTKATurns(value: number | string | undefined): TKATurns {
		if (value === 'fl') return 'fl';
		const num = typeof value === 'number' ? value : parseFloat(value || '0');

		if ([0, 0.5, 1, 1.5, 2, 2.5, 3].includes(num)) {
			return num as TKATurns;
		}
		return 0;
	}

	/**
	 * Safely convert a SequenceBeat to a PictographData
	 */
	function sequenceBeatToPictographData(beat: SequenceBeat): PictographData {
		// Create a motion data object with proper type casting
		const createMotionData = (attrs: any): MotionData | null => {
			if (!attrs) return null;

			return {
				id: `motion-${Math.random().toString(36).substring(2, 11)}`,
				motionType: isValidMotionType(attrs.motion_type) ? attrs.motion_type : 'static',
				startOri: isValidOrientation(attrs.start_ori) ? attrs.start_ori : 'in',
				endOri: isValidOrientation(attrs.end_ori || attrs.start_ori)
					? attrs.end_ori || attrs.start_ori
					: 'in',
				propRotDir: isValidPropRotDir(attrs.prop_rot_dir) ? attrs.prop_rot_dir : 'no_rot',
				startLoc: isValidLoc(attrs.start_loc) ? attrs.start_loc : 's',
				endLoc: isValidLoc(attrs.end_loc) ? attrs.end_loc : 's',
				turns: safeAsTKATurns(attrs.turns),
				color: 'blue' as Color, // Will be overridden below
				leadState: null,
				prefloatMotionType: null,
				prefloatPropRotDir: null
			};
		};

		// Create blue and red motion data
		const blueMotionData = createMotionData(beat.blue_attributes);
		const redMotionData = createMotionData(beat.red_attributes);

		// Set colors
		if (blueMotionData) blueMotionData.color = 'blue';
		if (redMotionData) redMotionData.color = 'red';

		// Create and return the PictographData
		return {
			letter: null, // Not using this for options
			startPos: safeAsTKAPosition(beat.start_pos),
			endPos: safeAsTKAPosition(beat.end_pos),
			timing: (beat.timing as VTGTiming) || null,
			direction: (beat.direction as VTGDir) || null,
			gridMode: 'diamond',
			gridData: null,
			blueMotionData,
			redMotionData,
			redPropData: null,
			bluePropData: null,
			redArrowData: null,
			blueArrowData: null,
			grid: 'diamond'
		};
	}

	// --- Reactive UI State & Data ---
	$: isLoading = $uiState.isLoading;
	$: groupedOptions = $groupedOptionsStore; // Options grouped by the current sort method's criteria
	$: filteredOptions = $filteredOptionsStore; // Options after filtering (if any) and sorting
	$: actualCategoryKeys = groupedOptions ? Object.keys(groupedOptions) : []; // Available category keys based on current grouping

	// Clear the loading state when options are loaded
	$: if (!isLoading && filteredOptions.length > 0) {
		// Clear the transition loading state
		transitionLoading.end();
	}
	// Determine which options to display based on the selected tab
	$: optionsToDisplay =
		$selectedTab === 'all'
			? filteredOptions // Show all (filtered/sorted) options if 'all' is selected
			: ($selectedTab && groupedOptions && groupedOptions[$selectedTab]) || []; // Show options for the specific category tab
	// Key for transitions based on the selected tab
	// This is used in the template for keyed each blocks
	$: showTabs = $selectedTab !== 'all'; // Flag to determine if category tabs should be shown in the header

	// --- Derived Layout Context ---
	// This derived store calculates layout values based on various inputs
	const layoutContextValue: Readable<LayoutContextValue> = derived(
		[
			windowWidth,
			windowHeight,
			containerWidth,
			containerHeight,
			uiState,
			filteredOptionsStore, // Need filtered options count for layout
			groupedOptionsStore, // Need grouped options for layout when tab is selected
			selectedTab
		],
		([
			$windowWidth,
			$windowHeight,
			$containerWidth,
			$containerHeight,
			$ui,
			$filteredOptions,
			$groupedOptions,
			$selectedTab
		]) => {
			// 1. Get enhanced device info using container width (more reliable for component layout)
			const { deviceType: enhancedDeviceType, foldableInfo } = getEnhancedDeviceType(
				$containerWidth > 0 ? $containerWidth : $windowWidth,
				$windowWidth < BREAKPOINTS.tablet
			);

			// 2. Determine isMobile/isTablet BASED ON the final enhancedDeviceType
			const isMobile = enhancedDeviceType === 'smallMobile' || enhancedDeviceType === 'mobile';
			const isTablet = enhancedDeviceType === 'tablet';

			// 3. Determine portrait/aspect based on container dimensions
			const isPortrait = $containerHeight > $containerWidth;
			const currentContainerAspect = getContainerAspect($containerWidth, $containerHeight);

			// 4. Calculate the count of items currently being displayed for layout purposes
			const optionsCount =
				$selectedTab && $selectedTab !== 'all' && $groupedOptions && $groupedOptions[$selectedTab]
					? $groupedOptions[$selectedTab].length // Count for the specific selected tab
					: $filteredOptions.length; // Count for the 'all' view

			// 5. Get the responsive layout configuration, passing foldableInfo
			const currentLayoutConfig = getResponsiveLayout(
				optionsCount,
				$containerHeight,
				$containerWidth,
				isMobile,
				isPortrait,
				foldableInfo // Pass the full foldable info object
			);

			// 6. Return the complete context object
			return {
				deviceType: enhancedDeviceType,
				isMobile: isMobile,
				isTablet: isTablet,
				isPortrait: isPortrait,
				containerWidth: $containerWidth,
				containerHeight: $containerHeight,
				ht: $containerHeight, // Add missing 'ht' property
				containerAspect: currentContainerAspect,
				layoutConfig: currentLayoutConfig,
				foldableInfo: foldableInfo // IMPORTANT: Pass the full foldable info object
			};
		}
	);

	// --- Set Context ---
	// Make the derived layout context available to child components
	setContext<Readable<LayoutContextValue>>(LAYOUT_CONTEXT_KEY, layoutContextValue);

	// --- Reactive Access to Context (Optional) ---
	// You can reactively access the context value if needed directly in this component's logic/template
	$: context = $layoutContextValue;

	// --- Event Handlers ---

	// Debounced function to update container dimensions when the container resizes
	const debouncedHandleContainerResize = (() => {
		let timeoutId: ReturnType<typeof setTimeout> | null = null;

		return (width: number, height: number) => {
			if (timeoutId !== null) {
				clearTimeout(timeoutId);
			}

			timeoutId = setTimeout(() => {
				// Ensure we never set invalid dimensions (0 or negative values)
				// This prevents the "getResponsiveLayout called with invalid dimensions" error
				if (width > 0 && height > 0) {
					containerWidth.set(width);
					containerHeight.set(height);
				} else {
					// If we get invalid dimensions, use fallback values based on window size
					// This can happen during initial render or when container is hidden
					if (width <= 0) {
						const fallbackWidth =
							typeof window !== 'undefined'
								? Math.max(300, window.innerWidth * 0.8)
								: BREAKPOINTS.desktop;
						containerWidth.set(fallbackWidth);
					}

					if (height <= 0) {
						const fallbackHeight =
							typeof window !== 'undefined' ? Math.max(200, window.innerHeight * 0.6) : 768;
						containerHeight.set(fallbackHeight);
					}
				}
				timeoutId = null;
			}, 100);
		};
	})();

	// Handle changes from the ViewControl (Show All / Group By...)
	function handleViewChange(event: CustomEvent<ViewModeDetail>) {
		const detail = event.detail;
		if (detail.mode === 'all') {
			// Switch to 'Show All' view
			selectedTab.set('all');
			const currentSortMethod = get(uiState).sortMethod;
			// Persist 'all' as the last selection for this sort method
			actions.setLastSelectedTabForSort(currentSortMethod, 'all');

			// Important: When showing all, we don't change the sort method
			// This ensures we keep the current sort method but just show all options
			console.log('Showing all options while maintaining sort method:', currentSortMethod);

			// Dispatch an event to notify the ViewControl to update its icon
			// Only force update if we're coming from a different view
			if (typeof document !== 'undefined') {
				const viewUpdateEvent = new CustomEvent('update-view-control', {
					detail: {
						mode: 'all',
						forceUpdate: true // Force update only when explicitly showing all
					},
					bubbles: true
				});
				document.dispatchEvent(viewUpdateEvent);
			}
		} else if (detail.mode === 'group') {
			// Switch to a grouped view (by Type, EndPos, etc.)
			const newSortMethod = detail.method;
			actions.setSortMethod(newSortMethod); // Update the sorting method in the store

			// Determine which category tab to select within the new grouping
			const uiStateValue = get(uiState);
			const lastSelectedForNewMethod =
				uiStateValue.lastSelectedTab[newSortMethod as keyof typeof uiStateValue.lastSelectedTab];
			const currentGroupsForNewMethod = get(groupedOptionsStore); // Re-get groups based on new sort method
			const availableKeysForNewMethod = currentGroupsForNewMethod
				? Object.keys(currentGroupsForNewMethod)
				: [];

			let nextTabToSelect: string | null = null; // Default to null, meaning no specific tab initially

			if (
				lastSelectedForNewMethod &&
				lastSelectedForNewMethod !== 'all' &&
				availableKeysForNewMethod.includes(lastSelectedForNewMethod)
			) {
				// If there was a previously selected tab for this sort method, use it
				nextTabToSelect = lastSelectedForNewMethod;
			} else if (availableKeysForNewMethod.length > 0) {
				// Otherwise, select the first available category tab
				nextTabToSelect = availableKeysForNewMethod[0];
			} else {
				// If no categories exist for this grouping, default back to 'all'
				nextTabToSelect = 'all';
			}

			selectedTab.set(nextTabToSelect);

			// Update the last selected tab preference if it changed
			if (lastSelectedForNewMethod !== nextTabToSelect) {
				actions.setLastSelectedTabForSort(newSortMethod, nextTabToSelect);
			}
		}
	}

	// Handle clicks on specific category tabs (Type1, Type2, etc.)
	function handleSubTabSelect(event: CustomEvent<string>) {
		const newSubTab = event.detail;
		selectedTab.set(newSubTab);
		// Save this tab selection preference for the current sort method
		actions.setLastSelectedTabForSort(get(uiState).sortMethod, newSubTab);
	}

	// Update window dimensions on resize
	function updateWindowSize() {
		windowWidth.set(window.innerWidth);
		windowHeight.set(window.innerHeight);
	}

	// --- onMount: Load options based on sequence ---
	onMount(() => {
		// Set up event listeners for tab selection and view changes
		const optionPickerElement = document.querySelector('.option-picker');
		if (optionPickerElement) {
			// Listen for tabSelect events
			optionPickerElement.addEventListener('tabSelect', (event) => {
				if (event instanceof CustomEvent) {
					console.log('OptionPicker received tabSelect event:', event.detail);
					handleSubTabSelect(event as CustomEvent<string>);
				}
			});

			// Listen for both viewChange and optionPickerViewChange events
			optionPickerElement.addEventListener('viewChange', (event) => {
				if (event instanceof CustomEvent) {
					console.log('OptionPicker received viewChange event:', event.detail);
					handleViewChange(event as CustomEvent<ViewModeDetail>);
				}
			});

			// Add listener for the new event name to avoid infinite recursion
			optionPickerElement.addEventListener('optionPickerViewChange', (event) => {
				if (event instanceof CustomEvent) {
					console.log('OptionPicker received optionPickerViewChange event:', event.detail);
					handleViewChange(event as CustomEvent<ViewModeDetail>);
				}
			});
		}

		// --- Initialization Logic ---
		const savedState = get(uiState);
		const savedSortMethod = savedState.sortMethod;
		const lastSelectedTabsMap = savedState.lastSelectedTab;
		const preferredTabForSavedMethod = lastSelectedTabsMap[savedSortMethod];

		// Function to load options from sequence data
		const loadOptionsFromSequence = async () => {
			// Get current sequence data
			const fullSequence = sequenceDataService.getCurrentSequence();

			// Find the start position beat (beat 0)
			const startPosBeat = fullSequence.find(
				(beat) =>
					beat && typeof beat === 'object' && 'beat' in beat && (beat as SequenceBeat).beat === 0
			) as SequenceBeat | undefined;

			if (startPosBeat) {
				// Convert to PictographData with proper typing
				const pictographData = sequenceBeatToPictographData(startPosBeat);

				// Load options based on the pictograph data
				actions.loadOptions([pictographData]);
			} else {
				// No start position found, load empty options
				actions.loadOptions([]);
				console.log('No start position found in sequence data');
			}
		};

		// Initial load
		loadOptionsFromSequence();

		// Set up the tab selection
		setTimeout(() => {
			const currentGroups = get(groupedOptionsStore);
			const availableKeys = currentGroups ? Object.keys(currentGroups) : [];

			let initialTabToSet: string | null = 'all';
			if (preferredTabForSavedMethod) {
				if (preferredTabForSavedMethod === 'all') {
					initialTabToSet = 'all';
				} else if (availableKeys.includes(preferredTabForSavedMethod)) {
					initialTabToSet = preferredTabForSavedMethod;
				} else if (availableKeys.length > 0) {
					initialTabToSet = availableKeys[0];
				}
			} else if (availableKeys.length > 0) {
				initialTabToSet = availableKeys[0];
			}

			selectedTab.set(initialTabToSet);

			if (preferredTabForSavedMethod !== initialTabToSet) {
				actions.setLastSelectedTabForSort(savedSortMethod, initialTabToSet);
			}
		}, 0);

		// --- Event Listeners & Subscriptions ---
		window.addEventListener('resize', updateWindowSize);
		updateWindowSize();

		// Listen for sequence-updated events
		const handleSequenceUpdate = () => {
			loadOptionsFromSequence();
		};

		// Listen for refresh-options events (used when preserving start position after beat removal)
		const handleRefreshOptions = (event: CustomEvent) => {
			console.log('OptionPicker received refresh-options event:', event.detail);
			if (event.detail?.startPosition) {
				// Load options based on the provided start position
				actions.loadOptions([event.detail.startPosition]);
			} else {
				// Fallback to loading from sequence data
				loadOptionsFromSequence();
			}
		};

		document.addEventListener('sequence-updated', handleSequenceUpdate);
		document.addEventListener('refresh-options', handleRefreshOptions as EventListener);

		// Subscribe to the sequenceStore for updates
		const unsubscribeSequence = sequenceStore.subscribe((state) => {
			if (state && state.beats && state.beats.length > 0) {
				// Convert StoreBeatData to PictographData format
				const sequence = state.beats.map((beat) => {
					return {
						letter: beat.metadata?.letter || null,
						startPos: beat.metadata?.startPos || null,
						endPos: beat.metadata?.endPos || null,
						redPropData: beat.redPropData,
						bluePropData: beat.bluePropData,
						// Convert motion data from the store format
						redMotionData: beat.redMotionData || null,
						blueMotionData: beat.blueMotionData || null
					} as PictographData;
				});
				actions.loadOptions(sequence);
			}
		});

		// --- Cleanup ---
		return () => {
			window.removeEventListener('resize', updateWindowSize);
			document.removeEventListener('sequence-updated', handleSequenceUpdate);
			document.removeEventListener('refresh-options', handleRefreshOptions as EventListener);
			unsubscribeSequence();

			// Remove custom event listeners
			const optionPickerElement = document.querySelector('.option-picker');
			if (optionPickerElement) {
				optionPickerElement.removeEventListener('tabSelect', (event) => {
					if (event instanceof CustomEvent) {
						handleSubTabSelect(event as CustomEvent<string>);
					}
				});

				optionPickerElement.removeEventListener('viewChange', (event) => {
					if (event instanceof CustomEvent) {
						handleViewChange(event as CustomEvent<ViewModeDetail>);
					}
				});

				// Also remove the new event listener
				optionPickerElement.removeEventListener('optionPickerViewChange', (event) => {
					if (event instanceof CustomEvent) {
						handleViewChange(event as CustomEvent<ViewModeDetail>);
					}
				});
			}
		};
	});
</script>

<div class="option-picker" class:mobile={context.isMobile} class:portrait={context.isPortrait}>
	<OptionPickerHeader selectedTab={$selectedTab} categoryKeys={actualCategoryKeys} {showTabs} />

	<div class="options-container" use:resize={debouncedHandleContainerResize}>
		<OptionDisplayArea
			{isLoading}
			selectedTab={$selectedTab}
			{optionsToDisplay}
			hasCategories={actualCategoryKeys.length > 0}
		/>
	</div>
</div>

<style>
	.option-picker {
		display: flex;
		flex-direction: column;
		width: 100%;
		height: 100%;
		box-sizing: border-box;
		overflow: hidden;
		position: relative;
		background-color: transparent; /* Or your desired background */
		justify-content: center; /* Center content vertically */
	}

	.options-container {
		flex: 1; /* Takes remaining vertical space */
		display: flex; /* Needed for children */
		position: relative; /* For absolute positioning of children like messages */
		border-radius: 8px;
		background-color: transparent; /* Or your desired background */
		min-height: 0; /* Crucial for flex child sizing */
		overflow: hidden; /* Contains children, prevents double scrollbars */
		justify-content: center; /* Center content vertically */
	}
	/* Optional: Constrain max width on large screens */
	@media (min-width: 1400px) {
		.option-picker {
			max-width: 1400px;
			margin: 0 auto;
		}
	}
</style>
