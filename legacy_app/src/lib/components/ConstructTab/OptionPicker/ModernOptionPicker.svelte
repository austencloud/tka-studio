<script lang="ts">
	import { onMount, setContext } from 'svelte';
	import { LAYOUT_CONTEXT_KEY } from './layoutContext';
	import OptionDisplayArea from './components/OptionDisplayArea.svelte';
	import { resize } from './actions/resize';
	import type { ViewModeDetail } from './components/ViewControl/types';
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
	import OptionPickerHeader from './components/OptionPickerHeader';
	import { BREAKPOINTS, getContainerAspect } from './config';
	import { getResponsiveLayout, getEnhancedDeviceType } from './utils/layoutUtils';
	import { optionPickerContainer } from '$lib/state/stores/optionPicker/optionPickerContainer';

	// --- State using Svelte 5 runes ---
	// Window dimensions with sensible defaults
	let windowWidth = $state(typeof window !== 'undefined' ? window.innerWidth : BREAKPOINTS.desktop);
	let windowHeight = $state(typeof window !== 'undefined' ? window.innerHeight : 768);

	// Container dimensions with fallback values
	let containerWidth = $state(
		typeof window !== 'undefined' ? Math.max(300, window.innerWidth * 0.8) : BREAKPOINTS.desktop
	);
	let containerHeight = $state(
		typeof window !== 'undefined' ? Math.max(200, window.innerHeight * 0.6) : 768
	);

	// Create a reactive layout context
	let layoutContext = $state({
		deviceType: 'desktop',
		isMobile: false,
		isTablet: false,
		isPortrait: false,
		containerWidth: 0, // Will be updated in the effect
		containerHeight: 0, // Will be updated in the effect
		ht: 0, // Will be updated in the effect
		containerAspect: 'square',
		layoutConfig: {
			gridColumns: 'repeat(auto-fit, minmax(100px, 1fr))',
			optionSize: '100px',
			gridGap: '8px',
			gridClass: '',
			aspectClass: '',
			scaleFactor: 1.0
		},
		foldableInfo: {
			isFoldable: false,
			isUnfolded: false,
			foldableType: 'unknown',
			confidence: 0,
			detectionMethod: 'none'
		}
	});

	// Update the layout context with the current container dimensions
	$effect(() => {
		layoutContext.containerWidth = containerWidth;
		layoutContext.containerHeight = containerHeight;
		layoutContext.ht = containerHeight;
	});

	// Update the layout context when dimensions change
	$effect(() => {
		// 1. Get enhanced device info using container width
		const { deviceType: enhancedDeviceType, foldableInfo } = getEnhancedDeviceType(
			containerWidth > 0 ? containerWidth : windowWidth,
			windowWidth < BREAKPOINTS.tablet
		);

		// 2. Determine isMobile/isTablet based on the device type
		const isMobile = enhancedDeviceType === 'smallMobile' || enhancedDeviceType === 'mobile';
		const isTablet = enhancedDeviceType === 'tablet';

		// 3. Determine portrait/aspect based on container dimensions
		const isPortrait = containerHeight > containerWidth;
		const currentContainerAspect = getContainerAspect(containerWidth, containerHeight);

		// 4. Calculate the count of items currently being displayed
		const selectedTab = optionPickerContainer.state.selectedTab;
		const optionsCount =
			selectedTab && selectedTab !== 'all' && groupedOptions[selectedTab]
				? groupedOptions[selectedTab].length // Count for the specific selected tab
				: filteredOptions.length; // Count for the 'all' view

		// 5. Get the responsive layout configuration
		const currentLayoutConfig = getResponsiveLayout(
			optionsCount,
			containerHeight,
			containerWidth,
			isMobile,
			isPortrait,
			foldableInfo
		);

		// 6. Update the context object
		layoutContext = {
			deviceType: enhancedDeviceType,
			isMobile,
			isTablet,
			isPortrait,
			containerWidth,
			containerHeight,
			ht: containerHeight,
			containerAspect: currentContainerAspect,
			layoutConfig: currentLayoutConfig,
			foldableInfo: {
				isFoldable: foldableInfo.isFoldable || false,
				isUnfolded: foldableInfo.isUnfolded || false,
				foldableType: foldableInfo.foldableType || 'unknown',
				confidence: foldableInfo.confidence || 0,
				detectionMethod: foldableInfo.detectionMethod || 'none'
			}
		};
	});

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

	// --- Derived values using Svelte 5 runes ---
	const isLoading = $derived(optionPickerContainer.state.isLoading);
	const showTabs = $derived(optionPickerContainer.state.selectedTab !== 'all');
	const context = $derived(layoutContext);

	// Create a simple array for the options to display
	let optionsToDisplay = $state<PictographData[]>([]);
	let groupedOptions = $state<Record<string, PictographData[]>>({});
	let filteredOptions = $state<PictographData[]>([]);
	let actualCategoryKeys = $state<string[]>([]);

	// Update options when the container state changes
	$effect(() => {
		// Get the current options from the container
		const options = [...optionPickerContainer.state.options];

		// Apply sorting based on the current sort method
		const sortMethod = optionPickerContainer.state.sortMethod;

		// Group options by the appropriate key based on sort method
		groupedOptions = {};
		options.forEach((option) => {
			let groupKey = 'unknown';

			// Determine the group key based on the sort method
			if (sortMethod === 'type') {
				groupKey = option.letter || 'unknown';
			} else if (sortMethod === 'endPosition') {
				groupKey = option.endPos || 'unknown';
			} else if (sortMethod === 'reversals') {
				// Handle reversals sorting
				groupKey =
					option.redMotionData?.motionType === 'anti' ||
					option.blueMotionData?.motionType === 'anti'
						? 'reversal'
						: 'continuous';
			} else {
				groupKey = 'all';
			}

			if (!groupedOptions[groupKey]) {
				groupedOptions[groupKey] = [];
			}

			groupedOptions[groupKey].push(option);
		});

		// Update the filtered options (all options, sorted)
		filteredOptions = options;

		// Update the category keys
		actualCategoryKeys = Object.keys(groupedOptions);

		// Update the options to display based on the selected tab
		const selectedTab = optionPickerContainer.state.selectedTab;
		if (selectedTab === 'all') {
			optionsToDisplay = filteredOptions;
		} else if (selectedTab && groupedOptions[selectedTab]) {
			optionsToDisplay = groupedOptions[selectedTab];
		} else {
			optionsToDisplay = [];
		}
	});

	// --- Set Context ---
	// Make the layout context available to child components
	$effect(() => {
		setContext(LAYOUT_CONTEXT_KEY, layoutContext);
	});

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
				if (width > 0 && height > 0) {
					containerWidth = width;
					containerHeight = height;
				} else {
					// If we get invalid dimensions, use fallback values based on window size
					if (width <= 0) {
						containerWidth =
							typeof window !== 'undefined'
								? Math.max(300, window.innerWidth * 0.8)
								: BREAKPOINTS.desktop;
					}

					if (height <= 0) {
						containerHeight =
							typeof window !== 'undefined' ? Math.max(200, window.innerHeight * 0.6) : 768;
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
			optionPickerContainer.setSelectedTab('all');
			optionPickerContainer.setLastSelectedTabForSort(
				optionPickerContainer.state.sortMethod,
				'all'
			);
		} else if (detail.mode === 'group') {
			// Switch to a grouped view (by Type, EndPos, etc.)
			const newSortMethod = detail.method;
			optionPickerContainer.setSortMethod(newSortMethod);

			// Determine which category tab to select within the new grouping
			const lastSelectedForNewMethod = optionPickerContainer.state.lastSelectedTab[newSortMethod];
			const availableKeysForNewMethod = actualCategoryKeys;

			let nextTabToSelect: string | null = null;

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
				// If no categories exist for this grouping, default back to 'all'
				nextTabToSelect = 'all';
			}

			optionPickerContainer.setSelectedTab(nextTabToSelect);
			optionPickerContainer.setLastSelectedTabForSort(newSortMethod, nextTabToSelect);
		}
	}

	// Handle clicks on specific category tabs (Type1, Type2, etc.)
	function handleSubTabSelect(event: CustomEvent<string>) {
		const newSubTab = event.detail;
		optionPickerContainer.setSelectedTab(newSubTab);
		optionPickerContainer.setLastSelectedTabForSort(
			optionPickerContainer.state.sortMethod,
			newSubTab
		);
	}

	// Update window dimensions on resize
	function updateWindowSize() {
		windowWidth = window.innerWidth;
		windowHeight = window.innerHeight;
	}

	// --- onMount: Load options based on sequence ---
	onMount(() => {
		// Set up event listeners for tab selection and view changes
		const optionPickerElement = document.querySelector('.option-picker');
		if (optionPickerElement) {
			// Listen for tabSelect events
			optionPickerElement.addEventListener('tabSelect', (event) => {
				if (event instanceof CustomEvent) {
					handleSubTabSelect(event as CustomEvent<string>);
				}
			});

			// Listen for viewChange events
			optionPickerElement.addEventListener('viewChange', (event) => {
				if (event instanceof CustomEvent) {
					handleViewChange(event as CustomEvent<ViewModeDetail>);
				}
			});

			// Add listener for the new event name to avoid infinite recursion
			optionPickerElement.addEventListener('optionPickerViewChange', (event) => {
				if (event instanceof CustomEvent) {
					handleViewChange(event as CustomEvent<ViewModeDetail>);
				}
			});
		}

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
				optionPickerContainer.loadOptions([pictographData]);
			} else {
				// No start position found, load empty options
				optionPickerContainer.loadOptions([]);
				console.log('No start position found in sequence data');
			}
		};

		// Initial load
		loadOptionsFromSequence();

		// --- Event Listeners & Subscriptions ---
		window.addEventListener('resize', updateWindowSize);
		updateWindowSize();

		// Listen for sequence-updated events
		const handleSequenceUpdate = () => {
			loadOptionsFromSequence();
		};

		// Listen for refresh-options events (used when preserving start position after beat removal)
		const handleRefreshOptions = (event: CustomEvent) => {
			if (event.detail?.startPosition) {
				// Load options based on the provided start position
				optionPickerContainer.loadOptions([event.detail.startPosition]);
			} else {
				// Fallback to loading from sequence data
				loadOptionsFromSequence();
			}
		};

		document.addEventListener('sequence-updated', handleSequenceUpdate);
		document.addEventListener('refresh-options', handleRefreshOptions as EventListener);

		// --- Cleanup ---
		return () => {
			window.removeEventListener('resize', updateWindowSize);
			document.removeEventListener('sequence-updated', handleSequenceUpdate);
			document.removeEventListener('refresh-options', handleRefreshOptions as EventListener);

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
	<OptionPickerHeader
		selectedTab={optionPickerContainer.state.selectedTab}
		categoryKeys={actualCategoryKeys}
		{showTabs}
	/>

	<div class="options-container" use:resize={debouncedHandleContainerResize}>
		<OptionDisplayArea
			{isLoading}
			selectedTab={optionPickerContainer.state.selectedTab}
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
