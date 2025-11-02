<script lang="ts">
	import { onMount, setContext, getContext } from 'svelte';
	import { writable, derived, type Readable } from 'svelte/store';
	import { get } from 'svelte/store';
	import { beatsStore } from '$lib/stores/sequence/beatsStore';
	import { uiState, filteredOptionsStore, groupedOptionsStore, actions } from './store';
	// Ensure layoutUtils imports are correct
	import { getResponsiveLayout, getEnhancedDeviceType } from './utils/layoutUtils';
	import { getContainerAspect, getDeviceType, BREAKPOINTS } from './config'; // getDeviceType might be unused if getEnhancedDeviceType handles all cases
	import { LAYOUT_CONTEXT_KEY, type LayoutContextValue } from './layoutContext';
	import OptionPickerHeader from './components/OptionPickerHeader.svelte';
	import OptionDisplayArea from './components/OptionDisplayArea.svelte';
	import { resize } from './actions/resize';
	import type { ViewModeDetail } from './components/ViewControl.svelte';
	import LayoutDebugger from './utils/debugger/LayoutDebugger.svelte';
	import sequenceDataService, { type SequenceBeat } from '$lib/services/SequenceDataService';
	import type { PictographData } from '$lib/types/PictographData';
	import type { TKAPosition } from '$lib/types/TKAPosition';
	import type { MotionData } from '$lib/components/objects/Motion/MotionData';
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

	// --- State Stores ---
	const windowWidth = writable(
		typeof window !== 'undefined' ? window.innerWidth : BREAKPOINTS.desktop
	);
	const windowHeight = writable(typeof window !== 'undefined' ? window.innerHeight : 768);
	const containerWidth = writable(0);
	const containerHeight = writable(0);
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
	// Determine which options to display based on the selected tab
	$: optionsToDisplay =
		$selectedTab === 'all'
			? filteredOptions // Show all (filtered/sorted) options if 'all' is selected
			: ($selectedTab && groupedOptions && groupedOptions[$selectedTab]) || []; // Show options for the specific category tab
	$: panelKey = $selectedTab || 'none'; // Key for transitions based on the selected tab
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
			const {
				deviceType: enhancedDeviceType,
				isFoldable,
				foldableInfo
			} = getEnhancedDeviceType(
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

	// Update container dimensions when the container resizes
	function handleContainerResize(width: number, height: number) {
		containerWidth.set(width);
		containerHeight.set(height);
	}

	// Handle changes from the ViewControl (Show All / Group By...)
	function handleViewChange(event: CustomEvent<ViewModeDetail>) {
		const detail = event.detail;
		if (detail.mode === 'all') {
			// Switch to 'Show All' view
			selectedTab.set('all');
			const currentSortMethod = get(uiState).sortMethod;
			// Persist 'all' as the last selection for this sort method
			actions.setLastSelectedTabForSort(currentSortMethod, 'all');
			// Optionally reset sort method if needed when showing all
			// if (currentSortMethod !== 'type') {
			// 	actions.setSortMethod('type');
			// }
		} else if (detail.mode === 'group') {
			// Switch to a grouped view (by Type, EndPos, etc.)
			const newSortMethod = detail.method;
			actions.setSortMethod(newSortMethod); // Update the sorting method in the store

			// Determine which category tab to select within the new grouping
			const lastSelectedForNewMethod = get(uiState).lastSelectedTab[newSortMethod];
			const currentGroupsForNewMethod = get(groupedOptionsStore); // Re-get groups based on new sort method
			const availableKeysForNewMethod = currentGroupsForNewMethod
				? Object.keys(currentGroupsForNewMethod)
				: [];

			let nextTabToSelect: string | null = null; // Default to null, meaning no specific tab initially

			if (
				lastSelectedForNewMethod &&
				availableKeysForNewMethod.includes(lastSelectedForNewMethod)
			) {
				// If there was a previously selected tab for this sort method, use it
				nextTabToSelect = lastSelectedForNewMethod;
			} else if (availableKeysForNewMethod.length > 0) {
				// Otherwise, select the first available category tab
				nextTabToSelect = availableKeysForNewMethod[0];
			} else {
				// If no categories exist for this grouping, maybe default back to 'all'? Or handle empty state.
				// For now, setting to null might be okay if the display area handles it.
				// Let's try setting back to 'all' if no sub-tabs exist
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
	function handleSectionSelect(event: CustomEvent<string>) {
		const newSection = event.detail;
		selectedTab.set(newSection);
		// Save this tab selection preference for the current sort method
		actions.setLastSelectedTabForSort(get(uiState).sortMethod, newSection);
	}

	// Update window dimensions on resize
	function updateWindowSize() {
		windowWidth.set(window.innerWidth);
		windowHeight.set(window.innerHeight);
	}

	// --- onMount: Load options based on sequence ---
	onMount(() => {
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
				console.log('Loaded options from sequence data:', pictographData);
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

		document.addEventListener('sequence-updated', handleSequenceUpdate);

		// Also keep current beatsStore subscription for backward compatibility
		// This way it works with both our new event and the original beat updates
		const unsubscribeBeats = beatsStore.subscribe((beats) => {
			if (beats && beats.length > 0) {
				const sequence = beats.map((beat) => beat.pictographData);
				actions.loadOptions(sequence);
			}
		});

		// --- Cleanup ---
		return () => {
			window.removeEventListener('resize', updateWindowSize);
			document.removeEventListener('sequence-updated', handleSequenceUpdate);
			unsubscribeBeats();
		};
	});
</script>

<div class="option-picker" class:mobile={context.isMobile} class:portrait={context.isPortrait}>
	<OptionPickerHeader
		selectedTab={$selectedTab}
		categoryKeys={actualCategoryKeys}
		{showTabs}
		on:viewChange={handleViewChange}
		on:tabSelect={handleSectionSelect}
	/>

	<div class="options-container" use:resize={handleContainerResize}>
		<OptionDisplayArea
			{isLoading}
			selectedTab={$selectedTab}
			{optionsToDisplay}
			hasCategories={actualCategoryKeys.length > 0}
		/>
	</div>

	<LayoutDebugger />
</div>

<style>
	.option-picker {
		display: flex;
		flex-direction: column;
		width: 100%;
		height: 100%;
		padding: clamp(10px, 2vw, 15px);
		box-sizing: border-box;
		overflow: hidden;
		position: relative;
		background-color: transparent; /* Or your desired background */
	}
	.option-picker.mobile {
		padding: clamp(8px, 1.5vw, 12px);
	}
	.options-container {
		flex: 1; /* Takes remaining vertical space */
		display: flex; /* Needed for children */
		position: relative; /* For absolute positioning of children like messages */
		border: 1px solid #e5e7eb; /* Example border */
		border-radius: 8px;
		background-color: transparent; /* Or your desired background */
		min-height: 0; /* Crucial for flex child sizing */
		overflow: hidden; /* Contains children, prevents double scrollbars */
	}
	/* Optional: Constrain max width on large screens */
	@media (min-width: 1400px) {
		.option-picker {
			max-width: 1400px;
			margin: 0 auto;
		}
	}
</style>
