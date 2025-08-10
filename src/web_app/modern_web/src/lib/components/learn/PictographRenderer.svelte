<!--
	Pictograph Renderer Component

	Renders pictograph data as visual representations.
	Handles different pictograph formats and grid modes.
-->

<script lang="ts">
	import type { PictographData } from '$domain/PictographData';

	// Props
	export let pictographData: PictographData;
	export let size: 'small' | 'medium' | 'large' = 'medium';
	export let showDetails = false;

	// Reactive statements
	$: gridSize = getGridSize(size);
	$: positions = getPositions(pictographData);

	// Methods
	function getGridSize(size: string): number {
		switch (size) {
			case 'small':
				return 80;
			case 'medium':
				return 120;
			case 'large':
				return 160;
			default:
				return 120;
		}
	}

	function getPositions(data: PictographData) {
		if (!data) return { start: null, end: null };

		return {
			start: parsePosition(data.start_pos || ''),
			end: parsePosition(data.end_pos || ''),
		};
	}

	function parsePosition(pos: string) {
		if (!pos) return null;

		const positionMap: Record<string, { x: number; y: number }> = {
			n: { x: 0.5, y: 0 },
			ne: { x: 1, y: 0 },
			e: { x: 1, y: 0.5 },
			se: { x: 1, y: 1 },
			s: { x: 0.5, y: 1 },
			sw: { x: 0, y: 1 },
			w: { x: 0, y: 0.5 },
			nw: { x: 0, y: 0 },
		};

		return positionMap[pos.toLowerCase()] || { x: 0.5, y: 0.5 };
	}

	function getPositionStyle(position: { x: number; y: number } | null, _isStart = true) {
		if (!position) return '';

		const x = position.x * gridSize;
		const y = position.y * gridSize;

		return `left: ${x}px; top: ${y}px;`;
	}

	function getLineStyle() {
		if (!positions.start || !positions.end) return '';

		const startX = positions.start.x * gridSize;
		const startY = positions.start.y * gridSize;
		const endX = positions.end.x * gridSize;
		const endY = positions.end.y * gridSize;

		const deltaX = endX - startX;
		const deltaY = endY - startY;
		const length = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
		const angle = Math.atan2(deltaY, deltaX) * (180 / Math.PI);

		return `
			left: ${startX}px;
			top: ${startY}px;
			width: ${length}px;
			transform: rotate(${angle}deg);
			transform-origin: 0 50%;
		`;
	}
</script>

<div class="pictograph-renderer" style="width: {gridSize}px; height: {gridSize}px;">
	<!-- Grid Background -->
	<div class="grid-background">
		{#if pictographData?.grid_mode === 'diamond'}
			<svg width={gridSize} height={gridSize} class="grid-svg">
				<!-- Diamond grid lines -->
				<path
					d="M {gridSize / 2} 0 L {gridSize} {gridSize / 2} L {gridSize /
						2} {gridSize} L 0 {gridSize / 2} Z"
					fill="none"
					stroke="rgba(255, 255, 255, 0.2)"
					stroke-width="1"
				/>
				<!-- Center cross -->
				<line
					x1={gridSize / 2}
					y1="0"
					x2={gridSize / 2}
					y2={gridSize}
					stroke="rgba(255, 255, 255, 0.1)"
					stroke-width="1"
				/>
				<line
					x1="0"
					y1={gridSize / 2}
					x2={gridSize}
					y2={gridSize / 2}
					stroke="rgba(255, 255, 255, 0.1)"
					stroke-width="1"
				/>
			</svg>
		{:else}
			<!-- Square grid -->
			<svg width={gridSize} height={gridSize} class="grid-svg">
				<!-- Grid lines -->
				<defs>
					<pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
						<path
							d="M 20 0 L 0 0 0 20"
							fill="none"
							stroke="rgba(255, 255, 255, 0.1)"
							stroke-width="1"
						/>
					</pattern>
				</defs>
				<rect width="100%" height="100%" fill="url(#grid)" />
				<rect
					width="100%"
					height="100%"
					fill="none"
					stroke="rgba(255, 255, 255, 0.2)"
					stroke-width="2"
				/>
			</svg>
		{/if}
	</div>

	<!-- Pictograph Content -->
	<div class="pictograph-content">
		<!-- Start Position -->
		{#if positions.start}
			<div
				class="position-marker start-position"
				style={getPositionStyle(positions.start, true)}
			>
				<div class="marker-dot"></div>
				<div class="marker-label">Start</div>
			</div>
		{/if}

		<!-- End Position -->
		{#if positions.end}
			<div
				class="position-marker end-position"
				style={getPositionStyle(positions.end, false)}
			>
				<div class="marker-dot"></div>
				<div class="marker-label">End</div>
			</div>
		{/if}

		<!-- Connection Line -->
		{#if positions.start && positions.end}
			<div class="connection-line" style={getLineStyle()}></div>
		{/if}

		<!-- Letter Display -->
		{#if pictographData?.letter}
			<div class="letter-overlay">
				{pictographData.letter}
			</div>
		{/if}
	</div>

	<!-- Details Panel -->
	{#if showDetails && pictographData}
		<div class="details-panel">
			<div class="detail-item">
				<span class="label">Letter:</span>
				<span class="value">{pictographData.letter}</span>
			</div>
			<div class="detail-item">
				<span class="label">Start:</span>
				<span class="value">{pictographData.start_pos}</span>
			</div>
			<div class="detail-item">
				<span class="label">End:</span>
				<span class="value">{pictographData.end_pos}</span>
			</div>
			<div class="detail-item">
				<span class="label">Grid:</span>
				<span class="value">{pictographData.grid_mode}</span>
			</div>
		</div>
	{/if}
</div>

<style>
	.pictograph-renderer {
		position: relative;
		display: inline-block;
		background: rgba(255, 255, 255, 0.05);
		border-radius: 8px;
		border: 1px solid rgba(255, 255, 255, 0.1);
		overflow: hidden;
	}

	.grid-background {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
	}

	.grid-svg {
		width: 100%;
		height: 100%;
	}

	.pictograph-content {
		position: relative;
		width: 100%;
		height: 100%;
	}

	.position-marker {
		position: absolute;
		transform: translate(-50%, -50%);
		z-index: 2;
	}

	.marker-dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		margin: 0 auto 2px;
	}

	.start-position .marker-dot {
		background: #4ade80;
		box-shadow: 0 0 8px rgba(74, 222, 128, 0.6);
	}

	.end-position .marker-dot {
		background: #f87171;
		box-shadow: 0 0 8px rgba(248, 113, 113, 0.6);
	}

	.marker-label {
		font-size: 10px;
		color: #ffffff;
		text-align: center;
		font-weight: 500;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8);
	}

	.connection-line {
		position: absolute;
		height: 2px;
		background: linear-gradient(90deg, #4ade80 0%, #f87171 100%);
		z-index: 1;
		box-shadow: 0 0 4px rgba(255, 255, 255, 0.3);
	}

	.letter-overlay {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		font-size: 1.5rem;
		font-weight: bold;
		color: #ffffff;
		text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
		z-index: 3;
		background: rgba(0, 0, 0, 0.3);
		padding: 4px 8px;
		border-radius: 4px;
		backdrop-filter: blur(4px);
	}

	.details-panel {
		position: absolute;
		bottom: -60px;
		left: 0;
		right: 0;
		background: rgba(0, 0, 0, 0.8);
		padding: 8px;
		border-radius: 4px;
		font-size: 12px;
		color: #ffffff;
		backdrop-filter: blur(8px);
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.detail-item {
		display: flex;
		justify-content: space-between;
		margin-bottom: 2px;
	}

	.detail-item:last-child {
		margin-bottom: 0;
	}

	.label {
		color: #94a3b8;
		font-weight: 500;
	}

	.value {
		color: #ffffff;
		font-weight: 600;
	}

	/* Size Variations */
	:global(.pictograph-renderer.small) {
		.letter-overlay {
			font-size: 1rem;
		}

		.marker-dot {
			width: 6px;
			height: 6px;
		}

		.marker-label {
			font-size: 8px;
		}
	}

	:global(.pictograph-renderer.large) {
		.letter-overlay {
			font-size: 2rem;
		}

		.marker-dot {
			width: 10px;
			height: 10px;
		}

		.marker-label {
			font-size: 12px;
		}
	}
</style>
