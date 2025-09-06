<script lang="ts">
	import { onMount } from 'svelte';
	import type { GridData } from '$lib/components/objects/Grid/GridData';

	export let gridData: GridData | null = null;
	export let visible: boolean = true;
	export let showLabels: boolean = true;

	let gridPoints: {
		key: string;
		x: number;
		y: number;
		color: string;
	}[] = [];

	$: if (gridData && visible) {
		generateGridPoints();
	}

	function generateGridPoints() {
		if (!gridData) return;

		const newGridPoints: typeof gridPoints = [];

		// Process normal hand points
		if (gridData.allHandPointsNormal) {
			Object.entries(gridData.allHandPointsNormal).forEach(([key, point]) => {
				if (point && point.coordinates) {
					newGridPoints.push({
						key,
						x: point.coordinates.x,
						y: point.coordinates.y,
						color: 'blue'
					});
				}
			});
		}

		// Process normal layer2 points
		if (gridData.allLayer2PointsNormal) {
			Object.entries(gridData.allLayer2PointsNormal).forEach(([key, point]) => {
				if (point && point.coordinates) {
					newGridPoints.push({
						key,
						x: point.coordinates.x,
						y: point.coordinates.y,
						color: 'green'
					});
				}
			});
		}

		// Add center point
		if (gridData.centerPoint && gridData.centerPoint.coordinates) {
			newGridPoints.push({
				key: 'centerPoint',
				x: gridData.centerPoint.coordinates.x,
				y: gridData.centerPoint.coordinates.y,
				color: 'red'
			});
		}

		gridPoints = newGridPoints;
	}

	onMount(() => {
		if (gridData) {
			generateGridPoints();
		}
	});
</script>

{#if visible && gridPoints.length > 0}
	<g class="grid-debug-overlay">
		{#each gridPoints as point}
			<circle cx={point.x} cy={point.y} r="5" fill={point.color} stroke="white" stroke-width="1" />

			{#if showLabels}
				<text
					x={point.x + 10}
					y={point.y}
					font-size="8"
					fill="white"
					stroke="black"
					stroke-width="0.5"
					paint-order="stroke"
				>
					{point.key.replace(/_/g, ' ')}
				</text>
			{/if}
		{/each}
	</g>
{/if}
