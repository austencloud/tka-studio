<script lang="ts">
	/**
	 * Debug Canvas Component
	 * Visual representation of arrow positioning with debug overlays
	 */

	import type { DebugStepData } from './types';
	import type { Point } from '$lib/services/positioning/types';

	interface Props {
		debugData: DebugStepData;
		showCoordinateGrid: boolean;
		showHandPoints: boolean;
		showLayer2Points: boolean;
		showAdjustmentVectors: boolean;
		currentStep: number;
		stepByStepMode: boolean;
	}

	let {
		debugData,
		showCoordinateGrid,
		showHandPoints,
		showLayer2Points,
		showAdjustmentVectors,
		currentStep,
		stepByStepMode
	}: Props = $props();

	let canvasElement: SVGSVGElement;
	const CANVAS_SIZE = 400;
	const CENTER = CANVAS_SIZE / 2;

	// Color scheme for debug visualization
	const COLORS = {
		grid: '#404040',
		handPoints: '#60a5fa',
		layer2Points: '#34d399',
		arrow: { blue: '#3b82f6', red: '#ef4444' },
		adjustment: '#fbbf24',
		final: '#10b981'
	};

	// Convert world coordinates to canvas coordinates
	function worldToCanvas(point: Point): [number, number] {
		return [
			CENTER + point.x,
			CENTER - point.y // Flip Y axis for SVG
		];
	}

	// Render hand points if available
	function renderHandPoints(): string {
		if (!showHandPoints || !debugData.coordinateSystemDebugInfo?.handPoints) {
			return '';
		}

		const points = debugData.coordinateSystemDebugInfo.handPoints;
		return Object.entries(points)
			.map(([location, point]) => {
				const [x, y] = worldToCanvas(point);
				return `<circle cx="${x}" cy="${y}" r="4" fill="${COLORS.handPoints}" opacity="0.8"/>
				        <text x="${x + 8}" y="${y - 8}" fill="${COLORS.handPoints}" font-size="10">${location}</text>`;
			})
			.join('');
	}

	// Render layer 2 points if available
	function renderLayer2Points(): string {
		if (!showLayer2Points || !debugData.coordinateSystemDebugInfo?.layer2Points) {
			return '';
		}

		const points = debugData.coordinateSystemDebugInfo.layer2Points;
		return Object.entries(points)
			.map(([location, point]) => {
				const [x, y] = worldToCanvas(point);
				return `<circle cx="${x}" cy="${y}" r="3" fill="${COLORS.layer2Points}" opacity="0.8"/>
				        <text x="${x + 8}" y="${y + 12}" fill="${COLORS.layer2Points}" font-size="9">${location}</text>`;
			})
			.join('');
	}

	// Render coordinate grid
	function renderCoordinateGrid(): string {
		if (!showCoordinateGrid) return '';

		const gridLines = [];
		const step = 20;
		
		// Vertical lines
		for (let x = step; x < CANVAS_SIZE; x += step) {
			gridLines.push(`<line x1="${x}" y1="0" x2="${x}" y2="${CANVAS_SIZE}" stroke="${COLORS.grid}" stroke-width="0.5" opacity="0.3"/>`);
		}
		
		// Horizontal lines
		for (let y = step; y < CANVAS_SIZE; y += step) {
			gridLines.push(`<line x1="0" y1="${y}" x2="${CANVAS_SIZE}" y2="${y}" stroke="${COLORS.grid}" stroke-width="0.5" opacity="0.3"/>`);
		}
		
		// Center lines
		gridLines.push(`<line x1="${CENTER}" y1="0" x2="${CENTER}" y2="${CANVAS_SIZE}" stroke="${COLORS.grid}" stroke-width="1" opacity="0.6"/>`);
		gridLines.push(`<line x1="0" y1="${CENTER}" x2="${CANVAS_SIZE}" y2="${CENTER}" stroke="${COLORS.grid}" stroke-width="1" opacity="0.6"/>`);
		
		return gridLines.join('');
	}

	// Render adjustment vectors
	function renderAdjustmentVectors(): string {
		if (!showAdjustmentVectors) return '';

		const vectors = [];
		const selectedArrowColor = debugData.arrowData?.color || 'blue';

		// Initial position to default adjustment
		if (debugData.initialPosition && debugData.defaultAdjustment) {
			const [startX, startY] = worldToCanvas(debugData.initialPosition);
			const [endX, endY] = worldToCanvas({
				x: debugData.initialPosition.x + debugData.defaultAdjustment.x,
				y: debugData.initialPosition.y + debugData.defaultAdjustment.y
			});
			
			vectors.push(`<line x1="${startX}" y1="${startY}" x2="${endX}" y2="${endY}" 
			             stroke="${COLORS.adjustment}" stroke-width="2" marker-end="url(#arrowhead)"/>`);
			vectors.push(`<text x="${(startX + endX) / 2}" y="${(startY + endY) / 2 - 8}" 
			             fill="${COLORS.adjustment}" font-size="10">Default Adj</text>`);
		}

		// Special adjustment if different
		if (debugData.specialAdjustment && debugData.defaultAdjustment &&
		    (debugData.specialAdjustment.x !== debugData.defaultAdjustment.x ||
		     debugData.specialAdjustment.y !== debugData.defaultAdjustment.y)) {
			
			const basePos = debugData.initialPosition || { x: 0, y: 0 };
			const [startX, startY] = worldToCanvas({
				x: basePos.x + debugData.defaultAdjustment.x,
				y: basePos.y + debugData.defaultAdjustment.y
			});
			const [endX, endY] = worldToCanvas({
				x: basePos.x + debugData.specialAdjustment.x,
				y: basePos.y + debugData.specialAdjustment.y
			});
			
			vectors.push(`<line x1="${startX}" y1="${startY}" x2="${endX}" y2="${endY}" 
			             stroke="#f59e0b" stroke-width="2" marker-end="url(#arrowhead2)"/>`);
			vectors.push(`<text x="${(startX + endX) / 2}" y="${(startY + endY) / 2 - 8}" 
			             fill="#f59e0b" font-size="10">Special Adj</text>`);
		}

		return vectors.join('');
	}

	// Render arrow at final position
	function renderArrow(): string {
		if (!debugData.finalPosition) return '';

		const selectedArrowColor = debugData.arrowData?.color || 'blue';
		const [x, y] = worldToCanvas(debugData.finalPosition);
		const rotation = debugData.finalRotation || 0;
		
		return `<g transform="translate(${x},${y}) rotate(${rotation})">
		          <path d="M-10,0 L10,0 M5,-5 L10,0 L5,5" 
		                stroke="${COLORS.arrow[selectedArrowColor as keyof typeof COLORS.arrow]}" 
		                stroke-width="3" fill="none" stroke-linecap="round"/>
		          <circle cx="0" cy="0" r="2" fill="${COLORS.arrow[selectedArrowColor as keyof typeof COLORS.arrow]}"/>
		        </g>`;
	}

	// Generate the complete SVG content
	const svgContent = $derived(`
		<defs>
			<marker id="arrowhead" markerWidth="10" markerHeight="7" 
			        refX="9" refY="3.5" orient="auto">
				<polygon points="0 0, 10 3.5, 0 7" fill="${COLORS.adjustment}"/>
			</marker>
			<marker id="arrowhead2" markerWidth="10" markerHeight="7" 
			        refX="9" refY="3.5" orient="auto">
				<polygon points="0 0, 10 3.5, 0 7" fill="#f59e0b"/>
			</marker>
		</defs>
		${renderCoordinateGrid()}
		${renderHandPoints()}
		${renderLayer2Points()}
		${renderAdjustmentVectors()}
		${renderArrow()}
	`);
</script>

<div class="debug-canvas">
	<div class="canvas-header">
		<h3>📊 Visual Debug Canvas</h3>
		{#if stepByStepMode}
			<div class="step-indicator">
				Step {currentStep} of {5}
			</div>
		{/if}
	</div>
	
	<div class="canvas-container">
		<svg 
			bind:this={canvasElement}
			width={CANVAS_SIZE} 
			height={CANVAS_SIZE}
			viewBox={`0 0 ${CANVAS_SIZE} ${CANVAS_SIZE}`}
			class="debug-svg"
		>
			{@html svgContent}
		</svg>
	</div>

	<div class="canvas-info">
		{#if debugData.finalPosition}
			<div class="position-info">
				<strong>Final Position:</strong> 
				({debugData.finalPosition.x.toFixed(2)}, {debugData.finalPosition.y.toFixed(2)})
			</div>
		{/if}
		{#if debugData.finalRotation !== undefined}
			<div class="rotation-info">
				<strong>Rotation:</strong> {debugData.finalRotation.toFixed(1)}°
			</div>
		{/if}
		{#if debugData.errors.length > 0}
			<div class="error-count">
				<strong>Errors:</strong> {debugData.errors.length}
			</div>
		{/if}
	</div>
</div>

<style>
	.debug-canvas {
		display: flex;
		flex-direction: column;
		height: 100%;
		align-items: center;
		justify-content: center;
		gap: 16px;
	}

	.canvas-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		width: 100%;
		padding: 0 16px;
	}

	.canvas-header h3 {
		margin: 0;
		color: #fbbf24;
		font-size: 1.1rem;
	}

	.step-indicator {
		background: rgba(251, 191, 36, 0.2);
		border: 1px solid rgba(251, 191, 36, 0.4);
		border-radius: 12px;
		padding: 4px 12px;
		font-size: 0.85rem;
		color: #fbbf24;
		font-weight: 600;
	}

	.canvas-container {
		background: rgba(0, 0, 0, 0.3);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 8px;
		padding: 16px;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.debug-svg {
		background: rgba(255, 255, 255, 0.05);
		border-radius: 4px;
	}

	.canvas-info {
		display: flex;
		flex-direction: column;
		gap: 8px;
		padding: 12px;
		background: rgba(255, 255, 255, 0.05);
		border-radius: 6px;
		min-width: 200px;
		text-align: center;
	}

	.canvas-info div {
		color: #c7d2fe;
		font-size: 0.9rem;
	}

	.canvas-info strong {
		color: #fbbf24;
	}

	.error-count {
		color: #f87171 !important;
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.canvas-header {
			flex-direction: column;
			gap: 8px;
		}

		.canvas-container {
			padding: 8px;
		}

		.debug-svg {
			width: 280px;
			height: 280px;
		}
	}
</style>
