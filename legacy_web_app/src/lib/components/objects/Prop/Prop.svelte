<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { parsePropSvg } from '../../SvgManager/PropSvgParser';
	import SvgManager from '../../SvgManager/SvgManager';
	import type { PropData } from './PropData';
	import type { PropSvgData } from '../../SvgManager/PropSvgData';
	import PropRotAngleManager from './PropRotAngleManager';
	import { sequenceStore } from '$lib/state/stores/sequenceStore';
	import { derived } from 'svelte/store';

	// Props - we support both direct propData and store-based approach
	export let propData: PropData | undefined = undefined;
	export let beatId: string | undefined = undefined;
	export let color: 'red' | 'blue' | undefined = undefined;
	// Animation duration is passed from parent but not used directly in this component
	export const animationDuration = 200;

	// Component state
	let svgData: PropSvgData | null = null;
	let isLoaded = false;
	let loadTimeout: ReturnType<typeof setTimeout>;
	let rotAngle = 0;

	// Services
	const dispatch = createEventDispatcher();
	const svgManager = new SvgManager();

	// Get prop data from the sequence store if beatId and color are provided
	const propDataFromStore = derived(sequenceStore, ($sequenceStore) => {
		if (!beatId || !color) return null;

		const beat = $sequenceStore.beats.find((b) => b.id === beatId);
		if (!beat) return null;

		return color === 'red' ? beat.redPropData : beat.bluePropData;
	});

	// Use either the prop data from store or the directly provided prop data
	$: effectivePropData = $propDataFromStore || propData;

	// Reactive statement to compute rotation angle
	$: {
		// Ensure we have both loc and ori, and the SVG is loaded
		if (effectivePropData) {
			// Always try to calculate, even if loc or ori might be undefined
			try {
				const rotAngleManager = new PropRotAngleManager({
					loc: effectivePropData.loc,
					ori: effectivePropData.ori
				});

				// Update rotAngle even if loc or ori are potentially undefined
				rotAngle = rotAngleManager.getRotationAngle();

				// Update the rotation angle in the prop data
				if (propData) {
					propData.rotAngle = rotAngle;
				}

				// If using store data and we need to update it, we would do it here
				// This would require implementing an update function that uses sequenceStore.updateBeat
			} catch (error) {
				console.warn('Error calculating rotation angle:', error);
			}
		}
	}

	onMount(() => {
		if (effectivePropData?.propType) {
			loadSvg();
		} else {
			isLoaded = true;
			dispatch('loaded', { error: true });
		}

		return () => {
			clearTimeout(loadTimeout);
		};
	});

	async function loadSvg() {
		try {
			// Safety check
			if (!effectivePropData) {
				throw new Error('No prop data available');
			}

			loadTimeout = setTimeout(() => {
				if (!isLoaded) {
					isLoaded = true;
					dispatch('loaded', { timeout: true });
				}
			}, 10);

			const svgText = await svgManager.getPropSvg(
				effectivePropData.propType,
				effectivePropData.color
			);
			const { viewBox, center } = parsePropSvg(svgText, effectivePropData.color);

			svgData = {
				imageSrc: `data:image/svg+xml;base64,${btoa(svgText)}`,
				viewBox,
				center
			};

			// Update the center in the prop data if it's directly provided
			if (propData) {
				propData.svgCenter = center;
			}

			clearTimeout(loadTimeout);
			isLoaded = true;
			dispatch('loaded');
		} catch (error: any) {
			console.error('Error loading prop SVG:', error);

			// Fallback SVG for error state
			svgData = {
				imageSrc:
					'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iI2ZmZiIgLz48dGV4dCB4PSIyMCIgeT0iNTAiIGZpbGw9IiNmMDAiPkVycm9yPC90ZXh0Pjwvc3ZnPg==',
				viewBox: { width: 100, height: 100 },
				center: { x: 50, y: 50 }
			};

			clearTimeout(loadTimeout);
			isLoaded = true;
			dispatch('loaded', { error: true });
			dispatch('error', { message: (error as Error)?.message || 'Unknown error' });
		}
	}

	function handleImageLoad() {
		dispatch('imageLoaded');
	}
	function handleImageError() {
		dispatch('error', { message: 'Image failed to load' });
	}
</script>

<!-- No nested transforms - just directly place everything with proper attributes -->
{#if svgData && isLoaded && effectivePropData}
	<g>
		<image
			href={svgData.imageSrc}
			transform="
				translate({effectivePropData.coords.x}, {effectivePropData.coords.y})
				rotate({rotAngle})
				translate({-svgData.center.x}, {-svgData.center.y})
			"
			width={svgData.viewBox.width}
			height={svgData.viewBox.height}
			preserveAspectRatio="xMidYMid meet"
			on:load={handleImageLoad}
			on:error={handleImageError}
		/>
	</g>
{/if}
