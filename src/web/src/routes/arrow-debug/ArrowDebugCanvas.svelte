<script lang="ts">
	import type { ArrowDebugState } from './state/arrow-debug-state.svelte';

	interface Props {
		state: ArrowDebugState;
	}

	let { state }: Props = $props();

	// Canvas dimensions and scaling
	const CANVAS_SIZE = 600;
	const SCENE_SIZE = 950;
	const SCALE = CANVAS_SIZE / SCENE_SIZE;

	// Colors
	const COLORS = {
		grid: '#374151',
		gridMajor: '#4b5563',
		handPoint: '#60a5fa',
		layer2Point: '#34d399',
		center: '#fbbf24',
		arrow: {
			blue: '#60a5fa',
			red: '#f87171'
		},
		vector: {
			initial: '#a78bfa',
			adjustment: '#34d399',
			final: '#fbbf24'
		},
		text: '#e5e7eb'
	};

	// Canvas reference
	let canvas: HTMLCanvasElement;
	let ctx: CanvasRenderingContext2D;

	// Reactive drawing
	$effect(() => {
		if (canvas) {
			ctx = canvas.getContext('2d')!;
			drawCanvas();
		}
	});

	function drawCanvas() {
		if (!ctx) return;

		// Clear canvas
		ctx.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
		
		// Draw coordinate grid
		if (state.showCoordinateGrid) {
			drawCoordinateGrid();
		}

		// Draw coordinate points
		if (state.currentDebugData.coordinateSystemDebugInfo) {
			if (state.showHandPoints) {
				drawHandPoints();
			}
			if (state.showLayer2Points) {
				drawLayer2Points();
			}
			drawSceneCenter();
		}

		// Draw positioning visualization based on current step
		drawPositioningVisualization();
	}

	function drawCoordinateGrid() {
		ctx.strokeStyle = COLORS.grid;
		ctx.lineWidth = 0.5;

		// Grid lines every 50 pixels in scene coordinates
		const gridSpacing = 50 * SCALE;
		
		for (let i = 0; i <= CANVAS_SIZE; i += gridSpacing) {
			// Vertical lines
			ctx.beginPath();
			ctx.moveTo(i, 0);
			ctx.lineTo(i, CANVAS_SIZE);
			ctx.stroke();
			
			// Horizontal lines
			ctx.beginPath();
			ctx.moveTo(0, i);
			ctx.lineTo(CANVAS_SIZE, i);
			ctx.stroke();
		}

		// Major grid lines (center lines)
		ctx.strokeStyle = COLORS.gridMajor;
		ctx.lineWidth = 1;
		
		const centerLine = CANVAS_SIZE / 2;
		
		// Center vertical line
		ctx.beginPath();
		ctx.moveTo(centerLine, 0);
		ctx.lineTo(centerLine, CANVAS_SIZE);
		ctx.stroke();
		
		// Center horizontal line
		ctx.beginPath();
		ctx.moveTo(0, centerLine);
		ctx.lineTo(CANVAS_SIZE, centerLine);
		ctx.stroke();

		// Add coordinate labels
		drawCoordinateLabels();
	}

	function drawCoordinateLabels() {
		ctx.fillStyle = COLORS.text;
		ctx.font = '10px monospace';
		ctx.textAlign = 'center';

		// Draw some key coordinate labels
		const labelPoints = [
			{ x: 0, y: 0, label: '(0,0)' },
			{ x: SCENE_SIZE / 2, y: SCENE_SIZE / 2, label: '(475,475)' },
			{ x: SCENE_SIZE, y: SCENE_SIZE, label: `(${SCENE_SIZE},${SCENE_SIZE})` }
		];

		labelPoints.forEach(point => {
			const canvasX = point.x * SCALE;
			const canvasY = point.y * SCALE;
			ctx.fillText(point.label, canvasX, canvasY - 5);
		});
	}

	function drawHandPoints() {
		if (!state.currentDebugData.coordinateSystemDebugInfo) return;

		const handPoints = state.currentDebugData.coordinateSystemDebugInfo.handPoints;
		
		ctx.fillStyle = COLORS.handPoint;
		ctx.strokeStyle = COLORS.handPoint;
		ctx.lineWidth = 2;

		Object.entries(handPoints).forEach(([location, point]) => {
			const canvasX = point.x * SCALE;
			const canvasY = point.y * SCALE;

			// Draw point
			ctx.beginPath();
			ctx.arc(canvasX, canvasY, 4, 0, 2 * Math.PI);
			ctx.fill();

			// Draw label
			ctx.fillStyle = COLORS.text;
			ctx.font = '10px monospace';
			ctx.textAlign = 'center';
			ctx.fillText(`H-${location}`, canvasX, canvasY - 8);
			ctx.fillStyle = COLORS.handPoint;
		});
	}

	function drawLayer2Points() {
		if (!state.currentDebugData.coordinateSystemDebugInfo) return;

		const layer2Points = state.currentDebugData.coordinateSystemDebugInfo.layer2Points;
		
		ctx.fillStyle = COLORS.layer2Point;
		ctx.strokeStyle = COLORS.layer2Point;
		ctx.lineWidth = 2;

		Object.entries(layer2Points).forEach(([location, point]) => {
			const canvasX = point.x * SCALE;
			const canvasY = point.y * SCALE;

			// Draw point as diamond
			ctx.beginPath();
			ctx.moveTo(canvasX, canvasY - 5);
			ctx.lineTo(canvasX + 5, canvasY);
			ctx.lineTo(canvasX, canvasY + 5);
			ctx.lineTo(canvasX - 5, canvasY);
			ctx.closePath();
			ctx.fill();

			// Draw label
			ctx.fillStyle = COLORS.text;
			ctx.font = '10px monospace';
			ctx.textAlign = 'center';
			ctx.fillText(`L2-${location}`, canvasX, canvasY + 15);
			ctx.fillStyle = COLORS.layer2Point;
		});
	}

	function drawSceneCenter() {
		if (!state.currentDebugData.coordinateSystemDebugInfo) return;

		const center = state.currentDebugData.coordinateSystemDebugInfo.sceneCenter;
		const canvasX = center.x * SCALE;
		const canvasY = center.y * SCALE;

		// Draw center point
		ctx.fillStyle = COLORS.center;
		ctx.strokeStyle = COLORS.center;
		ctx.lineWidth = 3;

		ctx.beginPath();
		ctx.arc(canvasX, canvasY, 6, 0, 2 * Math.PI);
		ctx.fill();

		// Draw crosshairs
		ctx.beginPath();
		ctx.moveTo(canvasX - 10, canvasY);
		ctx.lineTo(canvasX + 10, canvasY);
		ctx.moveTo(canvasX, canvasY - 10);
		ctx.lineTo(canvasX, canvasY + 10);
		ctx.stroke();

		// Draw label
		ctx.fillStyle = COLORS.text;
		ctx.font = '12px monospace';
		ctx.textAlign = 'center';
		ctx.fillText('CENTER', canvasX, canvasY + 25);
	}

	function drawPositioningVisualization() {
		const debugData = state.currentDebugData;
		
		// Only draw if we have the necessary data
		if (!debugData.initialPosition) return;

		const currentStep = state.stepByStepMode ? state.currentStep : 5;
		const arrowColor = state.selectedArrowColor;

		// Step 1-2: Show initial position
		if (currentStep >= 1) {
			drawInitialPosition(debugData.initialPosition);
		}

		// Step 3-4: Show adjustments
		if (currentStep >= 3 && state.showAdjustmentVectors) {
			if (debugData.defaultAdjustment) {
				drawAdjustmentVector(
					debugData.initialPosition,
					debugData.defaultAdjustment,
					'default',
					'Default Adjustment'
				);
			}

			if (currentStep >= 4 && debugData.specialAdjustment) {
				drawAdjustmentVector(
					debugData.initialPosition,
					debugData.specialAdjustment,
					'special',
					'Special Adjustment'
				);
			}

			if (debugData.tupleProcessedAdjustment) {
				drawAdjustmentVector(
					debugData.initialPosition,
					debugData.tupleProcessedAdjustment,
					'total',
					'Total Adjustment'
				);
			}
		}

		// Step 5: Show final position
		if (currentStep >= 5 && debugData.finalPosition) {
			drawFinalPosition(debugData.finalPosition, debugData.finalRotation, arrowColor);
		}

		// Draw step info overlay
		drawStepInfo();
	}

	function drawInitialPosition(position: any) {
		const canvasX = position.x * SCALE;
		const canvasY = position.y * SCALE;

		ctx.fillStyle = COLORS.vector.initial;
		ctx.strokeStyle = COLORS.vector.initial;
		ctx.lineWidth = 2;

		// Draw initial position marker
		ctx.beginPath();
		ctx.arc(canvasX, canvasY, 8, 0, 2 * Math.PI);
		ctx.stroke();

		// Draw inner dot
		ctx.beginPath();
		ctx.arc(canvasX, canvasY, 3, 0, 2 * Math.PI);
		ctx.fill();

		// Label
		ctx.fillStyle = COLORS.text;
		ctx.font = '11px monospace';
		ctx.textAlign = 'center';
		ctx.fillText('INITIAL', canvasX, canvasY - 15);
		ctx.fillText(`(${position.x.toFixed(1)}, ${position.y.toFixed(1)})`, canvasX, canvasY + 25);
	}

	function drawAdjustmentVector(from: any, adjustment: any, type: string, label: string) {
		const fromX = from.x * SCALE;
		const fromY = from.y * SCALE;
		const adjX = adjustment.x * SCALE;
		const adjY = adjustment.y * SCALE;

		let color = COLORS.vector.adjustment;
		if (type === 'total') color = COLORS.vector.final;

		ctx.strokeStyle = color;
		ctx.fillStyle = color;
		ctx.lineWidth = type === 'total' ? 3 : 2;

		// Draw vector arrow
		if (Math.abs(adjX) > 1 || Math.abs(adjY) > 1) {
			drawArrow(fromX, fromY, fromX + adjX, fromY + adjY, color);

			// Label the vector
			ctx.fillStyle = COLORS.text;
			ctx.font = '9px monospace';
			ctx.textAlign = 'center';
			const labelX = fromX + adjX / 2;
			const labelY = fromY + adjY / 2;
			ctx.fillText(label, labelX, labelY - 5);
			ctx.fillText(`(${adjustment.x.toFixed(1)}, ${adjustment.y.toFixed(1)})`, labelX, labelY + 10);
		}
	}

	function drawFinalPosition(position: any, rotation: number, color: string) {
		const canvasX = position.x * SCALE;
		const canvasY = position.y * SCALE;

		// Draw final arrow
		const arrowColor = color === 'blue' ? COLORS.arrow.blue : COLORS.arrow.red;
		drawArrow(canvasX, canvasY, canvasX + 30, canvasY, arrowColor, true);

		// Apply rotation visualization
		if (rotation !== 0) {
			ctx.save();
			ctx.translate(canvasX, canvasY);
			ctx.rotate((rotation * Math.PI) / 180);
			
			// Draw rotation indicator
			ctx.strokeStyle = COLORS.text;
			ctx.lineWidth = 1;
			ctx.setLineDash([2, 2]);
			ctx.beginPath();
			ctx.arc(0, 0, 20, 0, (rotation * Math.PI) / 180);
			ctx.stroke();
			ctx.setLineDash([]);
			
			ctx.restore();
		}

		// Label
		ctx.fillStyle = COLORS.text;
		ctx.font = '12px monospace';
		ctx.textAlign = 'center';
		ctx.fillText('FINAL', canvasX, canvasY - 25);
		ctx.fillText(`(${position.x.toFixed(1)}, ${position.y.toFixed(1)})`, canvasX, canvasY + 40);
		if (rotation !== 0) {
			ctx.fillText(`${rotation.toFixed(1)}°`, canvasX, canvasY + 55);
		}
	}

	function drawArrow(fromX: number, fromY: number, toX: number, toY: number, color: string, isArrowHead = false) {
		ctx.strokeStyle = color;
		ctx.fillStyle = color;
		ctx.lineWidth = 2;

		// Draw line
		ctx.beginPath();
		ctx.moveTo(fromX, fromY);
		ctx.lineTo(toX, toY);
		ctx.stroke();

		// Draw arrowhead
		const angle = Math.atan2(toY - fromY, toX - fromX);
		const headLength = isArrowHead ? 12 : 8;
		
		ctx.beginPath();
		ctx.moveTo(toX, toY);
		ctx.lineTo(
			toX - headLength * Math.cos(angle - Math.PI / 6),
			toY - headLength * Math.sin(angle - Math.PI / 6)
		);
		ctx.moveTo(toX, toY);
		ctx.lineTo(
			toX - headLength * Math.cos(angle + Math.PI / 6),
			toY - headLength * Math.sin(angle + Math.PI / 6)
		);
		ctx.stroke();
	}

	function drawStepInfo() {
		if (!state.stepByStepMode) return;

		const stepNames = [
			'Input Data Loaded',
			'Location Calculated', 
			'Initial Position Set',
			'Default Adjustment Applied',
			'Special Adjustment Applied',
			'Final Position Calculated'
		];

		// Draw step info box
		ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
		ctx.fillRect(10, 10, 200, 60);
		
		ctx.strokeStyle = COLORS.vector.final;
		ctx.lineWidth = 1;
		ctx.strokeRect(10, 10, 200, 60);

		// Draw step text
		ctx.fillStyle = COLORS.text;
		ctx.font = '12px monospace';
		ctx.textAlign = 'left';
		ctx.fillText(`Step ${state.currentStep + 1}/${state.maxSteps + 1}`, 20, 30);
		ctx.fillText(stepNames[state.currentStep] || 'Complete', 20, 50);
	}

	function handleCanvasClick(event: MouseEvent) {
		const rect = canvas.getBoundingClientRect();
		const canvasX = event.clientX - rect.left;
		const canvasY = event.clientY - rect.top;
		
		// Convert to scene coordinates
		const sceneX = canvasX / SCALE;
		const sceneY = canvasY / SCALE;
		
		console.log(`Clicked at scene coordinates: (${sceneX.toFixed(1)}, ${sceneY.toFixed(1)})`);
	}
</script>

<div class="canvas-container">
	<h2>🎯 Visual Arrow Positioning</h2>
	
	<div class="canvas-wrapper">
		<canvas
			bind:this={canvas}
			width={CANVAS_SIZE}
			height={CANVAS_SIZE}
			onclick={handleCanvasClick}
		></canvas>
		
		{#if state.isCalculating}
			<div class="loading-overlay">
				<div class="spinner"></div>
				<p>Calculating positioning...</p>
			</div>
		{/if}
	</div>

	<!-- Legend -->
	<div class="legend">
		<h3>📖 Legend</h3>
		<div class="legend-grid">
			{#if state.showCoordinateGrid}
				<div class="legend-item">
					<div class="legend-color" style="background: {COLORS.grid}"></div>
					<span>Coordinate Grid</span>
				</div>
			{/if}
			
			{#if state.showHandPoints}
				<div class="legend-item">
					<div class="legend-symbol hand-point"></div>
					<span>Hand Points (Static/Dash)</span>
				</div>
			{/if}
			
			{#if state.showLayer2Points}
				<div class="legend-item">
					<div class="legend-symbol layer2-point"></div>
					<span>Layer2 Points (Pro/Anti/Float)</span>
				</div>
			{/if}
			
			<div class="legend-item">
				<div class="legend-symbol center-point"></div>
				<span>Scene Center (475, 475)</span>
			</div>
			
			{#if state.showAdjustmentVectors}
				<div class="legend-item">
					<div class="legend-color" style="background: {COLORS.vector.adjustment}"></div>
					<span>Adjustment Vectors</span>
				</div>
			{/if}
			
			<div class="legend-item">
				<div class="legend-color" style="background: {COLORS.arrow[state.selectedArrowColor]}"></div>
				<span>{state.selectedArrowColor} Arrow</span>
			</div>
		</div>
	</div>

	<!-- Current coordinates display -->
	{#if state.currentDebugData.finalPosition}
		<div class="coordinates-display">
			<h4>📍 Current Arrow Position</h4>
			<div class="coord-item">
				<span class="coord-label">Scene Position:</span>
				<span class="coord-value">
					({state.currentDebugData.finalPosition.x.toFixed(2)}, {state.currentDebugData.finalPosition.y.toFixed(2)})
				</span>
			</div>
			<div class="coord-item">
				<span class="coord-label">Canvas Position:</span>
				<span class="coord-value">
					({(state.currentDebugData.finalPosition.x * SCALE).toFixed(2)}, {(state.currentDebugData.finalPosition.y * SCALE).toFixed(2)})
				</span>
			</div>
			<div class="coord-item">
				<span class="coord-label">Rotation:</span>
				<span class="coord-value">{state.currentDebugData.finalRotation.toFixed(2)}°</span>
			</div>
		</div>
	{/if}
</div>

<style>
	.canvas-container {
		display: flex;
		flex-direction: column;
		gap: 20px;
		height: 100%;
		align-items: center;
	}

	h2 {
		margin: 0 0 20px 0;
		color: #fbbf24;
		font-size: 1.3rem;
		text-align: center;
	}

	.canvas-wrapper {
		position: relative;
		border: 2px solid rgba(255, 255, 255, 0.2);
		border-radius: 8px;
		overflow: hidden;
		background: #000;
	}

	canvas {
		display: block;
		cursor: crosshair;
	}

	.loading-overlay {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(0, 0, 0, 0.8);
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		color: white;
	}

	.spinner {
		width: 40px;
		height: 40px;
		border: 4px solid rgba(251, 191, 36, 0.3);
		border-top: 4px solid #fbbf24;
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin-bottom: 15px;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}

	.legend {
		background: rgba(0, 0, 0, 0.2);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 8px;
		padding: 15px;
		width: 100%;
		max-width: 600px;
	}

	.legend h3 {
		margin: 0 0 12px 0;
		color: #fde047;
		font-size: 1rem;
		border-bottom: 1px solid rgba(253, 224, 71, 0.2);
		padding-bottom: 8px;
	}

	.legend-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: 8px;
	}

	.legend-item {
		display: flex;
		align-items: center;
		gap: 8px;
		font-size: 0.85rem;
		color: #e5e7eb;
	}

	.legend-color {
		width: 16px;
		height: 16px;
		border-radius: 2px;
		border: 1px solid rgba(255, 255, 255, 0.3);
	}

	.legend-symbol {
		width: 16px;
		height: 16px;
		border: 1px solid rgba(255, 255, 255, 0.3);
	}

	.legend-symbol.hand-point {
		background: #60a5fa;
		border-radius: 50%;
	}

	.legend-symbol.layer2-point {
		background: #34d399;
		transform: rotate(45deg);
	}

	.legend-symbol.center-point {
		background: #fbbf24;
		border-radius: 50%;
		position: relative;
	}

	.legend-symbol.center-point::before,
	.legend-symbol.center-point::after {
		content: '';
		position: absolute;
		background: #000;
	}

	.legend-symbol.center-point::before {
		top: 7px;
		left: 2px;
		right: 2px;
		height: 2px;
	}

	.legend-symbol.center-point::after {
		left: 7px;
		top: 2px;
		bottom: 2px;
		width: 2px;
	}

	.coordinates-display {
		background: rgba(0, 0, 0, 0.3);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 8px;
		padding: 15px;
		width: 100%;
		max-width: 600px;
	}

	.coordinates-display h4 {
		margin: 0 0 10px 0;
		color: #fbbf24;
		font-size: 0.9rem;
		border-bottom: 1px solid rgba(251, 191, 36, 0.2);
		padding-bottom: 6px;
	}

	.coord-item {
		display: flex;
		justify-content: space-between;
		margin-bottom: 6px;
		font-size: 0.85rem;
	}

	.coord-label {
		color: #c7d2fe;
	}

	.coord-value {
		color: #fbbf24;
		font-family: 'Courier New', monospace;
		font-weight: 600;
	}
</style>
