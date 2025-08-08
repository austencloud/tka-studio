<script lang="ts">
	import { resizeManager } from '../../utils/performance/resize-manager.js';
	// import { thumbnailViewportManager } from '../../utils/performance/viewport.js'; // Not used currently

	// Props
	let {
		enabled = false
	}: {
		enabled?: boolean;
	} = $props();

	// State
	let stats = $state({
		totalRegistered: 0,
		visibleCount: 0,
		isResizing: false
	});

	let updateInterval: ReturnType<typeof setInterval> | null = null;

	// Update stats periodically when enabled
	$effect(() => {
		if (enabled) {
			updateStats();
			updateInterval = setInterval(updateStats, 100); // Update every 100ms
		} else {
			if (updateInterval) {
				clearInterval(updateInterval);
				updateInterval = null;
			}
		}

		return () => {
			if (updateInterval) {
				clearInterval(updateInterval);
			}
		};
	});

	function updateStats(): void {
		stats = resizeManager.getStats();
	}

	function getPerformanceColor(): string {
		const ratio = stats.visibleCount / Math.max(stats.totalRegistered, 1);
		if (ratio < 0.3) return '#22c55e'; // Green - good performance
		if (ratio < 0.6) return '#f59e0b'; // Yellow - moderate
		return '#ef4444'; // Red - many elements processing
	}
</script>

{#if enabled}
	<div class="performance-monitor">
		<div class="monitor-header">
			<span class="monitor-title">📊 Performance</span>
			<div
				class="status-indicator"
				class:resizing={stats.isResizing}
				style:background-color={getPerformanceColor()}
			></div>
		</div>

		<div class="monitor-stats">
			<div class="stat-item">
				<span class="stat-label">Total:</span>
				<span class="stat-value">{stats.totalRegistered}</span>
			</div>
			<div class="stat-item">
				<span class="stat-label">Visible:</span>
				<span class="stat-value">{stats.visibleCount}</span>
			</div>
			<div class="stat-item">
				<span class="stat-label">Status:</span>
				<span class="stat-value" class:resizing={stats.isResizing}>
					{stats.isResizing ? 'Resizing' : 'Idle'}
				</span>
			</div>
		</div>
	</div>
{/if}

<style>
	.performance-monitor {
		position: fixed;
		top: 80px;
		right: 16px;
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 8px;
		padding: 12px;
		font-size: 0.75rem;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
		z-index: 1000;
		min-width: 140px;
		backdrop-filter: blur(8px);
	}

	.monitor-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 8px;
	}

	.monitor-title {
		font-weight: 600;
		color: var(--color-text-primary);
	}

	.status-indicator {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		transition: all 0.3s ease;
	}

	.status-indicator.resizing {
		animation: pulse 1s infinite;
	}

	@keyframes pulse {
		0%,
		100% {
			opacity: 1;
			transform: scale(1);
		}
		50% {
			opacity: 0.7;
			transform: scale(1.2);
		}
	}

	.monitor-stats {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.stat-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.stat-label {
		color: var(--color-text-secondary);
	}

	.stat-value {
		color: var(--color-text-primary);
		font-weight: 500;
	}

	.stat-value.resizing {
		color: var(--color-primary);
		font-weight: 600;
	}

	/* Hide on mobile */
	@media (max-width: 768px) {
		.performance-monitor {
			display: none;
		}
	}
</style>
