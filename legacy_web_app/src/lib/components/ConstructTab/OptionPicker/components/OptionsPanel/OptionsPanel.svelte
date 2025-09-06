<script lang="ts">
	import { onMount } from 'svelte';
	import type { PictographData } from '$lib/types/PictographData';
	import { scrollActions } from '../../store/scrollStore';
	import { determineGroupKey, getSortedGroupKeys } from '../../services/OptionsService';
	import { resize } from '../../actions/resize';
	import SingleRowRenderer from './SingleRowRenderer.svelte';
	import MultiRowRenderer from './MultiRowRenderer.svelte';


	type LayoutRow = {
		type: 'single' | 'multi';
		groups: Array<{ key: string; options: PictographData[] }>;
	};

	const {
		selectedTab = null,
		options = [],
		transitionKey = 'default'
	} = $props<{
		selectedTab?: string | null;
		options?: PictographData[];
		transitionKey?: string | number;
	}>();

	let panelElement: HTMLElement | undefined = $state(); // Use $state for reactive updates
	let contentIsShort = $state(false); // Use $state for reactive updates
	let layoutRows: LayoutRow[] = $state([]); // Use $state for reactive updates
	let previousTab: string | null = $state(null); // Use $state for reactive updates
	let isReady = $state(false); // Track if component is ready to be shown, use $state

	const MAX_ITEMS_FOR_SMALL_GROUP = 2;

	// Save scroll position when scrolling
	function handleScroll() {
		if (panelElement && selectedTab) {
			scrollActions.savePosition(`tab-${selectedTab}`, panelElement.scrollTop);
		}
	}

	// Restore scroll position after transition
	function restoreScrollPosition() {
		if (panelElement && selectedTab) {
			scrollActions.restorePosition(panelElement, `tab-${selectedTab}`, 50);
		}
	}

	// Track tab changes for scroll position management
	$effect(() => {
		if (selectedTab !== previousTab && previousTab !== null) {
			if (panelElement && previousTab) {
				scrollActions.savePosition(`tab-${previousTab}`, panelElement.scrollTop);
			}
		}
		previousTab = selectedTab;
		setTimeout(() => {
			restoreScrollPosition();
		}, 0);
	});

	// Restore scroll position when component mounts for the initial tab
	onMount(() => {
		setTimeout(() => {
			restoreScrollPosition();
		}, 50);
	});

	$effect(() => {
		const subGroups: Record<string, PictographData[]> = {};
		options.forEach((option: PictographData) => {
			const groupKey = determineGroupKey(option, 'type');
			if (!subGroups[groupKey]) subGroups[groupKey] = [];
			subGroups[groupKey].push(option);
		});

		const currentSortedGroupKeys = getSortedGroupKeys(Object.keys(subGroups), 'type');

		const rows: LayoutRow[] = [];
		let i = 0;
		while (i < currentSortedGroupKeys.length) {
			const currentKey = currentSortedGroupKeys[i];
			const currentOptions = subGroups[currentKey];
			if (!currentOptions || currentOptions.length === 0) {
				i++;
				continue;
			}
			const isCurrentSmall = currentOptions.length <= MAX_ITEMS_FOR_SMALL_GROUP;

			if (isCurrentSmall) {
				const smallGroupSequence = [{ key: currentKey, options: currentOptions }];
				let j = i + 1;
				while (j < currentSortedGroupKeys.length) {
					const nextKey = currentSortedGroupKeys[j];
					const nextOptions = subGroups[nextKey];
					if (
						nextOptions &&
						nextOptions.length > 0 &&
						nextOptions.length <= MAX_ITEMS_FOR_SMALL_GROUP
					) {
						smallGroupSequence.push({ key: nextKey, options: nextOptions });
						j++;
					} else {
						break;
					}
				}
				if (smallGroupSequence.length >= 2) {
					rows.push({ type: 'multi', groups: smallGroupSequence });
					i = j;
				} else {
					rows.push({ type: 'single', groups: smallGroupSequence });
					i++;
				}
			} else {
				rows.push({ type: 'single', groups: [{ key: currentKey, options: currentOptions }] });
				i++;
			}
		}
		layoutRows = rows;
	});

	const debouncedCheckContentHeight = (() => {
		let timeoutId: ReturnType<typeof setTimeout> | null = null;
		let lastCheckTime = 0;
		let lastContentHeight = 0;
		let lastContainerHeight = 0;
		let checkCount = 0;
		const MIN_CHECK_INTERVAL = 300;
		const MAX_CHECKS_PER_CYCLE = 3;

		return () => {
			if (timeoutId !== null) {
				clearTimeout(timeoutId);
				timeoutId = null;
			}

			const now = Date.now();
			if (now - lastCheckTime < MIN_CHECK_INTERVAL) {
				checkCount++;
				if (checkCount > MAX_CHECKS_PER_CYCLE) {
					if (import.meta.env.DEV) console.debug('Too many content height checks, backing off');
					setTimeout(() => {
						checkCount = 0;
					}, 1000);
					return;
				}
				timeoutId = setTimeout(() => {
					debouncedCheckContentHeight();
				}, MIN_CHECK_INTERVAL);
				return;
			}

			if (now - lastCheckTime > 1000) {
				checkCount = 0;
			}

			timeoutId = setTimeout(() => {
				if (!panelElement) return;
				const panelContent = panelElement.querySelector('.panel-content');
				if (!panelContent) return;

				const contentHeight = panelContent.scrollHeight;
				const containerHeight = panelElement.clientHeight;

				if (
					Math.abs(contentHeight - lastContentHeight) < 2 &&
					Math.abs(containerHeight - lastContainerHeight) < 2
				) {
					timeoutId = null;
					return;
				}

				lastCheckTime = Date.now();
				lastContentHeight = contentHeight;
				lastContainerHeight = containerHeight;

				const buffer = 10;
				const fits = contentHeight + buffer <= containerHeight;

				if (fits !== contentIsShort) {
					contentIsShort = fits;

				}
				timeoutId = null;
			}, 100);
		};
	})();

	let previousOptionsLength = -1;
	let previousOptionsKey = '';

	$effect(() => {
		if (!options || !panelElement) return;
		const optionsKey = `${options.length}-${transitionKey}`;

		if (options.length !== previousOptionsLength || optionsKey !== previousOptionsKey) {
			previousOptionsLength = options.length;
			previousOptionsKey = optionsKey;
			setTimeout(() => {
				if (panelElement) {
					debouncedCheckContentHeight();
				}
			}, 150);
		}
	});

	onMount(() => {
		let initialCheckTimeout: ReturnType<typeof setTimeout> | null = setTimeout(() => {
			if (panelElement) {
				debouncedCheckContentHeight();
				setTimeout(() => {
					isReady = true;
				}, 50);
			}
			initialCheckTimeout = null;
		}, 200);

		return () => {
			if (initialCheckTimeout) {
				clearTimeout(initialCheckTimeout);
			}
		};
	});
</script>

<div
	class="options-panel"
	class:ready={isReady}
	bind:this={panelElement}
	use:resize={debouncedCheckContentHeight}
	class:vertically-center={contentIsShort}
	role="tabpanel"
	aria-labelledby="tab-{selectedTab}"
	id="options-panel-{selectedTab}"
	onscroll={handleScroll}
>
	<div class="panel-content">
		{#each layoutRows as row, rowIndex (transitionKey + '-row-' + rowIndex)}
			{#if row.type === 'single'}
				<SingleRowRenderer groups={row.groups} {transitionKey} {rowIndex} />
			{:else if row.type === 'multi'}
				<MultiRowRenderer groups={row.groups} {transitionKey} {rowIndex} />
			{/if}
		{/each}
	</div>
</div>

<style>
	.options-panel {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		overflow-y: auto; /* Allows vertical scrolling */
		overflow-x: hidden; /* Prevents horizontal scrolling */
		box-sizing: border-box;
		display: flex; /* Using flex to help with centering logic */
		flex-direction: column;
		opacity: 0;
		transition: opacity 0.35s ease-out;
		will-change: opacity; /* Optimize for animations */
		transform: translateZ(0); /* Force GPU acceleration */
		backface-visibility: hidden; /* Prevent flickering during animations */
	}

	.options-panel.ready {
		opacity: 1;
	}

	.panel-content {
		width: 100%;
		padding: 0.5rem 0;
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.options-panel.vertically-center {
		justify-content: center;
	}
	.options-panel.vertically-center .panel-content {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
	}

	/* Styles for multi-group-row and multi-group-item have been moved to MultiRowRenderer.svelte */

	.options-panel {
		scrollbar-width: thin;
		scrollbar-color: rgba(100, 116, 139, 0.7) rgba(30, 41, 59, 0.1);
	}

	.options-panel::-webkit-scrollbar {
		width: 10px;
	}

	.options-panel::-webkit-scrollbar-track {
		background: rgba(30, 41, 59, 0.1);
		border-radius: 6px;
		margin: 2px 0;
	}

	.options-panel::-webkit-scrollbar-thumb {
		background-color: rgba(100, 116, 139, 0.7);
		border-radius: 6px;
		border: 2px solid transparent;
		background-clip: padding-box;
	}

	.options-panel::-webkit-scrollbar-thumb:hover {
		background-color: rgba(148, 163, 184, 0.9);
	}
</style>
