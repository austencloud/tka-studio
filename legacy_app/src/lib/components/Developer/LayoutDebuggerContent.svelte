<!--
  Layout Debugger Content Component

  A simplified layout debugger that displays layout information.
-->
<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';

	// State
	const deviceInfo = writable({
		width: 0,
		height: 0,
		pixelRatio: 1,
		orientation: 'landscape',
		userAgent: '',
		deviceType: 'desktop'
	});

	// Update device info
	function updateDeviceInfo() {
		const width = window.innerWidth;
		const height = window.innerHeight;
		const pixelRatio = window.devicePixelRatio || 1;
		const orientation = width > height ? 'landscape' : 'portrait';
		const userAgent = navigator.userAgent;

		// Determine device type
		let deviceType = 'desktop';
		if (/Mobi|Android/i.test(userAgent)) {
			deviceType = width < 768 ? 'mobile' : 'tablet';
		} else if (width < 768) {
			deviceType = 'tablet';
		}

		deviceInfo.set({
			width,
			height,
			pixelRatio,
			orientation,
			userAgent,
			deviceType
		});
	}

	// Initialize on mount
	onMount(() => {
		updateDeviceInfo();

		// Update on resize
		const resizeHandler = () => {
			updateDeviceInfo();
		};

		window.addEventListener('resize', resizeHandler);

		return () => {
			window.removeEventListener('resize', resizeHandler);
		};
	});

	// Format user agent
	function formatUserAgent(ua: string): string {
		if (ua.length > 100) {
			return ua.substring(0, 100) + '...';
		}
		return ua;
	}
</script>

<div class="layout-debugger">
	<div class="section">
		<h3>Device Information</h3>
		<div class="info-grid">
			<div class="info-label">Device Type:</div>
			<div class="info-value">
				{$deviceInfo.deviceType}
				{$deviceInfo.deviceType === 'mobile'
					? '📱'
					: $deviceInfo.deviceType === 'tablet'
						? '📟'
						: '💻'}
			</div>

			<div class="info-label">Orientation:</div>
			<div class="info-value">
				{$deviceInfo.orientation}
				{$deviceInfo.orientation === 'portrait' ? '📸' : '🌄'}
			</div>

			<div class="info-label">Dimensions:</div>
			<div class="info-value">
				{$deviceInfo.width}×{$deviceInfo.height}px (Aspect: {(
					$deviceInfo.width / $deviceInfo.height
				).toFixed(2)})
			</div>

			<div class="info-label">Pixel Ratio:</div>
			<div class="info-value">{$deviceInfo.pixelRatio}</div>

			<div class="info-label">User Agent:</div>
			<div class="info-value user-agent">{formatUserAgent($deviceInfo.userAgent)}</div>
		</div>
	</div>

	<div class="section">
		<h3>Layout Visualization</h3>
		<div class="layout-visualization">
			<div
				class="device-frame"
				style="
          width: {Math.min(400, $deviceInfo.width / 4)}px;
          height: {Math.min(400, $deviceInfo.height / 4)}px;
          aspect-ratio: {$deviceInfo.width / $deviceInfo.height};
        "
			>
				<div class="screen">
					<div class="header"></div>
					<div class="content">
						<div class="sidebar"></div>
						<div class="main"></div>
					</div>
					<div class="footer"></div>
				</div>
			</div>
		</div>
	</div>

	<div class="section">
		<h3>Responsive Breakpoints</h3>
		<div class="breakpoints">
			<div class="breakpoint" class:active={$deviceInfo.width < 576}>
				<span class="name">XS</span>
				<span class="range">&lt; 576px</span>
			</div>
			<div class="breakpoint" class:active={$deviceInfo.width >= 576 && $deviceInfo.width < 768}>
				<span class="name">SM</span>
				<span class="range">≥ 576px</span>
			</div>
			<div class="breakpoint" class:active={$deviceInfo.width >= 768 && $deviceInfo.width < 992}>
				<span class="name">MD</span>
				<span class="range">≥ 768px</span>
			</div>
			<div class="breakpoint" class:active={$deviceInfo.width >= 992 && $deviceInfo.width < 1200}>
				<span class="name">LG</span>
				<span class="range">≥ 992px</span>
			</div>
			<div class="breakpoint" class:active={$deviceInfo.width >= 1200}>
				<span class="name">XL</span>
				<span class="range">≥ 1200px</span>
			</div>
		</div>
	</div>
</div>

<style>
	.layout-debugger {
		display: flex;
		flex-direction: column;
		gap: 20px;
		padding: 16px;
		height: 100%;
		overflow: auto;
		color: #e0e0e0;
		font-family:
			system-ui,
			-apple-system,
			sans-serif;
		box-sizing: border-box;
	}

	.section {
		background-color: #2a2a2a;
		border-radius: 8px;
		padding: 16px;
		border: 1px solid #444;
	}

	h3 {
		margin-top: 0;
		margin-bottom: 16px;
		font-size: 16px;
		color: #4da6ff;
		border-bottom: 1px solid #444;
		padding-bottom: 8px;
	}

	.info-grid {
		display: grid;
		grid-template-columns: 120px 1fr;
		gap: 8px 16px;
	}

	.info-label {
		font-weight: bold;
		color: #aaa;
	}

	.info-value {
		color: #e0e0e0;
	}

	.user-agent {
		word-break: break-all;
	}

	.layout-visualization {
		display: flex;
		justify-content: center;
		padding: 16px;
	}

	.device-frame {
		border: 2px solid #666;
		border-radius: 8px;
		overflow: hidden;
		background-color: #111;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
	}

	.screen {
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
	}

	.header {
		height: 10%;
		background-color: #4da6ff;
		opacity: 0.7;
	}

	.content {
		flex: 1;
		display: flex;
	}

	.sidebar {
		width: 20%;
		background-color: #9c27b0;
		opacity: 0.7;
	}

	.main {
		flex: 1;
		background-color: #4caf50;
		opacity: 0.7;
	}

	.footer {
		height: 8%;
		background-color: #ff9800;
		opacity: 0.7;
	}

	.breakpoints {
		display: flex;
		justify-content: space-between;
		gap: 8px;
	}

	.breakpoint {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 12px 8px;
		background-color: #333;
		border-radius: 4px;
		border: 1px solid #555;
		opacity: 0.6;
		transition: all 0.2s ease;
	}

	.breakpoint.active {
		background-color: #4da6ff;
		color: #fff;
		opacity: 1;
		transform: scale(1.05);
		border-color: #4da6ff;
		box-shadow: 0 0 10px rgba(77, 166, 255, 0.5);
	}

	.breakpoint .name {
		font-weight: bold;
		font-size: 16px;
	}

	.breakpoint .range {
		font-size: 12px;
		margin-top: 4px;
	}
</style>
