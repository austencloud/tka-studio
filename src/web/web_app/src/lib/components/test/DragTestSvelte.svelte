<script>
	let leftPanelWidth = 50; // percentage
	let isResizing = false;
	let performanceData = {
		lagEvents: [],
		moveEvents: [],
		lagThreshold: 5
	};

	$: lagCount = performanceData.lagEvents.length;
	$: avgTime = performanceData.moveEvents.length > 0 
		? (performanceData.moveEvents.reduce((sum, e) => sum + e.duration, 0) / performanceData.moveEvents.length).toFixed(2)
		: 0;
	$: worstLag = performanceData.lagEvents.length > 0
		? Math.max(...performanceData.lagEvents.map(e => e.duration)).toFixed(2)
		: 0;

	function handleResizeStart(event) {
		isResizing = true;
		event.preventDefault();

		const startX = event.clientX;
		const startWidth = leftPanelWidth;
		const containerWidth = event.target.closest('.container')?.clientWidth || 1000;

		// Reset performance data for this drag session
		performanceData.lagEvents = [];
		performanceData.moveEvents = [];

		function handleMouseMove(e) {
			if (!isResizing) return;

			const moveStartTime = performance.now();

			const deltaX = e.clientX - startX;
			const deltaPercent = (deltaX / containerWidth) * 100;
			const newWidth = Math.max(15, Math.min(60, startWidth + deltaPercent));

			leftPanelWidth = newWidth;

			const moveEndTime = performance.now();
			const moveDuration = moveEndTime - moveStartTime;

			performanceData.moveEvents.push({
				duration: moveDuration,
				timestamp: moveEndTime
			});

			if (moveDuration > performanceData.lagThreshold) {
				performanceData.lagEvents.push({
					duration: moveDuration,
					timestamp: moveEndTime
				});
			}

			// Trigger reactivity update
			performanceData = performanceData;
		}

		function handleMouseUp() {
			isResizing = false;
			
			console.log('Svelte drag session complete:', {
				totalMoves: performanceData.moveEvents.length,
				lagEvents: performanceData.lagEvents.length,
				avgTime: performanceData.moveEvents.length > 0 
					? (performanceData.moveEvents.reduce((sum, e) => sum + e.duration, 0) / performanceData.moveEvents.length).toFixed(2) + 'ms'
					: '0ms'
			});

			document.removeEventListener('mousemove', handleMouseMove);
			document.removeEventListener('mouseup', handleMouseUp);
		}

		document.addEventListener('mousemove', handleMouseMove);
		document.addEventListener('mouseup', handleMouseUp);
	}
</script>

<div class="performance-info">
	Svelte Drag Performance Monitor<br>
	Lag Events: <span>{lagCount}</span><br>
	Avg Time: <span>{avgTime}ms</span><br>
	Worst Lag: <span>{worstLag}ms</span>
</div>

<div class="container">
	<div class="left-panel" style="width: {leftPanelWidth}%;">
		<div class="panel-content">
			<h3>Left Panel (Svelte)</h3>
			<p>This is the left panel content. Width: {leftPanelWidth.toFixed(1)}%</p>
			<div class="tall-content">
				<p>Tall content to test scrolling...</p>
			</div>
		</div>
	</div>
	
	<button 
		class="splitter" 
		class:dragging={isResizing}
		on:mousedown={handleResizeStart}
		aria-label="Resize panels"
	></button>
	
	<div class="right-panel">
		<div class="panel-content">
			<h3>Right Panel (Svelte)</h3>
			<p>This is the right panel content. It should flex to fill remaining space.</p>
			<div class="tall-content">
				<p>More tall content...</p>
			</div>
		</div>
	</div>
</div>

<style>
	.container {
		display: flex;
		height: 100vh;
		width: 100vw;
	}

	.left-panel {
		background-color: #f0f0f0;
		border-right: 1px solid #ccc;
		overflow: auto;
		transition: width 0.2s ease;
	}

	.splitter {
		width: 4px;
		background-color: #ddd;
		cursor: col-resize;
		user-select: none;
		border: none;
		padding: 0;
		margin: 0;
	}

	.splitter:hover {
		background-color: #bbb;
	}

	.splitter.dragging {
		background-color: #999;
		transition: none;
	}

	.right-panel {
		flex: 1;
		background-color: #fff;
		overflow: auto;
	}

	.panel-content {
		padding: 20px;
	}

	.tall-content {
		height: 2000px;
		background: linear-gradient(to bottom, #f0f0f0, #e0e0e0);
	}

	.performance-info {
		position: fixed;
		top: 10px;
		right: 10px;
		background: rgba(0, 0, 0, 0.8);
		color: white;
		padding: 10px;
		border-radius: 5px;
		font-family: monospace;
		font-size: 12px;
		z-index: 1000;
	}
</style>
