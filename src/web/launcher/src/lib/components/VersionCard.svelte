<script lang="ts">
	import type { Version, PerformanceMetrics } from '../types/launcher.types.js';
	import { launcherState } from '../stores/launcher.svelte.js';
	import { spring, tweened } from 'svelte/motion';
	import { cubicOut, backOut } from 'svelte/easing';
	import {
		Play,
		Square,
		RotateCcw,
		ExternalLink,
		CheckCircle2,
		AlertCircle,
		Clock,
		Zap,
		Monitor,
		Package,
		Rocket,
		Activity,
		Cpu,
		HardDrive,
		Wifi,
		WifiOff
	} from 'lucide-svelte';

	interface Props {
		version: Version;
		metrics?: PerformanceMetrics;
		isSelected?: boolean;
		compact?: boolean;
		touchOptimized?: boolean;
	}

	let {
		version,
		metrics,
		isSelected = false,
		compact = false,
		touchOptimized = false
	}: Props = $props();

	// Advanced reactive state with better performance
	let isStarting = $state(false);
	let isStopping = $state(false);
	let isHovered = $state(false);
	let isFocused = $state(false);
	let cardElement: HTMLElement;
	let announceElement: HTMLElement;
	let lastAnnouncedStatus = $state(version.status);

	// Advanced animation stores with spring physics
	const cardScale = spring(1, { stiffness: 0.3, damping: 0.8 });
	const cardElevation = spring(0, { stiffness: 0.4, damping: 0.7 });
	const progressBar = tweened(0, { duration: 1200, easing: cubicOut });
	const glowIntensity = spring(0, { stiffness: 0.2, damping: 0.6 });
	const pulseScale = spring(1, { stiffness: 0.15, damping: 0.4 });

	// Gesture support for mobile
	let touchStartY = 0;
	let touchStartX = 0;
	let isDragging = $state(false);

	// Enhanced status configuration with better semantics
	const statusConfig = {
		available: {
			icon: CheckCircle2,
			class: 'status-available',
			text: 'Available',
			ariaLabel: 'Available for launch',
			color: 'electric-blue',
			priority: 'polite' as const
		},
		running: {
			icon: Zap,
			class: 'status-running',
			text: 'Running',
			ariaLabel: 'Currently running',
			color: 'neon-green',
			priority: 'polite' as const
		},
		starting: {
			icon: Clock,
			class: 'status-starting',
			text: 'Starting...',
			ariaLabel: 'Starting up, please wait',
			color: 'neon-orange',
			priority: 'assertive' as const
		},
		stopping: {
			icon: Clock,
			class: 'status-stopping',
			text: 'Stopping...',
			ariaLabel: 'Shutting down, please wait',
			color: 'neon-orange',
			priority: 'assertive' as const
		},
		stopped: {
			icon: CheckCircle2,
			class: 'status-available',
			text: 'Stopped',
			ariaLabel: 'Stopped and ready to start',
			color: 'electric-blue',
			priority: 'polite' as const
		},
		error: {
			icon: AlertCircle,
			class: 'status-error',
			text: 'Error',
			ariaLabel: 'Error occurred, retry available',
			color: 'red-500',
			priority: 'assertive' as const
		},
		'not-found': {
			icon: Package,
			class: 'status-not-found',
			text: 'Not Found',
			ariaLabel: 'Version files not found',
			color: 'slate-500',
			priority: 'polite' as const
		},
		'manual-start-required': {
			icon: AlertCircle,
			class: 'status-warning',
			text: 'Manual Start Required',
			ariaLabel: 'Manual start required, automated launch unavailable',
			color: 'neon-orange',
			priority: 'polite' as const
		}
	};

	// Enhanced derived state with better performance
	const currentStatus = $derived(statusConfig[version.status]);
	const serverInfo = $derived(launcherState.runningServers.get(version.id));
	const IconComponent = $derived(currentStatus.icon);
	const isInteractive = $derived(version.status !== 'not-found');
	const hasNetworkConnection = $derived(navigator.onLine);

	// Advanced performance calculations with caching
	const performanceScore = $derived(() => {
		if (!metrics) return 85;
		const fpsScore = Math.min(((metrics.fps || 60) / 60) * 100, 100);
		const memoryScore = Math.max(
			100 - ((metrics.memory?.used || 50) / (metrics.memory?.total || 100)) * 100,
			0
		);
		const loadTimeScore = Math.max(100 - (metrics.loadTime || 1000) / 50, 0);
		return Math.round((fpsScore + memoryScore + loadTimeScore) / 3);
	});

	// Real-time connection status
	const connectionStatus = $derived(() => {
		if (!hasNetworkConnection) return 'offline';
		if (version.status === 'running' && serverInfo) return 'connected';
		return 'disconnected';
	});

	// Advanced keyboard shortcuts with context awareness
	const keyboardShortcuts = $derived(() => ({
		Enter: 'Launch or open application',
		Space: 'Toggle selection',
		r: 'Restart (when running)',
		s: 'Stop (when running)',
		o: 'Open in browser (when running)',
		Escape: 'Clear selection'
	}));

	// Effects for animations and announcements
	$effect(() => {
		// Announce status changes to screen readers
		if (version.status !== lastAnnouncedStatus) {
			const announcement = `${version.name} status changed to ${currentStatus.text}`;
			announceStatusChange(announcement, currentStatus.priority);
			lastAnnouncedStatus = version.status;
		}
	});

	$effect(() => {
		// Update progress bar based on performance
		progressBar.set(performanceScore());
	});

	$effect(() => {
		// Handle hover and focus animations
		const targetScale = isHovered || isFocused ? 1.02 : 1;
		const targetElevation = isHovered || isFocused ? 12 : 0;
		const targetGlow = isHovered || isFocused ? 1 : 0;

		cardScale.set(targetScale);
		cardElevation.set(targetElevation);
		glowIntensity.set(targetGlow);
	});

	$effect(() => {
		// Pulse animation for running status
		if (version.status === 'running') {
			const interval = setInterval(() => {
				pulseScale.set(1.05);
				setTimeout(() => pulseScale.set(1), 600);
			}, 2000);
			return () => clearInterval(interval);
		}
	});

	// Enhanced interaction handlers with better UX
	async function handleStart() {
		if (isStarting || version.status === 'running') return;

		isStarting = true;
		announceAction('Starting application');

		try {
			await launcherState.startVersion(version.id);
			announceAction(`${version.name} started successfully`);
		} catch (error) {
			const message = error instanceof Error ? error.message : 'Unknown error';
			announceAction(`Failed to start ${version.name}: ${message}`, 'assertive');
		} finally {
			isStarting = false;
		}
	}

	async function handleStop() {
		if (isStopping || version.status !== 'running') return;

		isStopping = true;
		announceAction('Stopping application');

		try {
			await launcherState.stopVersion(version.id);
			announceAction(`${version.name} stopped successfully`);
		} catch (error) {
			const message = error instanceof Error ? error.message : 'Unknown error';
			announceAction(`Failed to stop ${version.name}: ${message}`, 'assertive');
		} finally {
			isStopping = false;
		}
	}

	async function handleRestart() {
		if (version.status !== 'running') return;

		announceAction('Restarting application');

		try {
			await launcherState.restartVersion(version.id);
			announceAction(`${version.name} restarted successfully`);
		} catch (error) {
			const message = error instanceof Error ? error.message : 'Unknown error';
			announceAction(`Failed to restart ${version.name}: ${message}`, 'assertive');
		}
	}

	function handleSelect() {
		if (!isInteractive) return;

		launcherState.toggleVersionSelection(version.id);
		const action = isSelected ? 'deselected' : 'selected';
		announceAction(`${version.name} ${action}`);
	}

	async function openInBrowser() {
		try {
			await launcherState.openApp(version.id);
			announceAction(`Opening ${version.name} in browser`);
		} catch (error) {
			announceAction(`Failed to open ${version.name}`, 'assertive');
			if (serverInfo) {
				window.open(serverInfo.url, '_blank');
			}
		}
	}

	// Enhanced keyboard navigation with comprehensive shortcuts
	function handleKeydown(event: KeyboardEvent) {
		if (!isInteractive) return;

		// Prevent default for handled keys
		const handledKeys = ['Enter', ' ', 'r', 's', 'o', 'Escape'];
		if (handledKeys.includes(event.key)) {
			event.preventDefault();
		}

		switch (event.key) {
			case 'Enter':
				if (version.status === 'available') {
					handleStart();
				} else if (version.status === 'running') {
					openInBrowser();
				}
				break;
			case ' ':
				handleSelect();
				break;
			case 'r':
				if (version.status === 'running') {
					handleRestart();
				}
				break;
			case 's':
				if (version.status === 'running') {
					handleStop();
				}
				break;
			case 'o':
				if (version.status === 'running') {
					openInBrowser();
				}
				break;
			case 'Escape':
				if (isSelected) {
					handleSelect();
				}
				cardElement?.blur();
				break;
		}
	}

	// Touch gesture support for mobile
	function handleTouchStart(event: TouchEvent) {
		if (!touchOptimized) return;

		const touch = event.touches[0];
		touchStartX = touch.clientX;
		touchStartY = touch.clientY;
		isDragging = false;
	}

	function handleTouchMove(event: TouchEvent) {
		if (!touchOptimized) return;

		const touch = event.touches[0];
		const deltaX = Math.abs(touch.clientX - touchStartX);
		const deltaY = Math.abs(touch.clientY - touchStartY);

		if (deltaX > 10 || deltaY > 10) {
			isDragging = true;
		}
	}

	function handleTouchEnd(event: TouchEvent) {
		if (!touchOptimized || isDragging) return;

		// Treat as click if not dragging
		if (version.status === 'available') {
			handleStart();
		} else if (version.status === 'running') {
			openInBrowser();
		}
	}

	// Accessibility announcements
	function announceStatusChange(message: string, priority: 'polite' | 'assertive' = 'polite') {
		if (announceElement) {
			announceElement.setAttribute('aria-live', priority);
			announceElement.textContent = message;

			// Clear after announcement
			setTimeout(() => {
				announceElement.textContent = '';
			}, 1000);
		}
	}

	function announceAction(message: string, priority: 'polite' | 'assertive' = 'polite') {
		announceStatusChange(message, priority);
	}

	// Enhanced formatting functions
	function formatUptime(startTime: Date): string {
		const now = new Date();
		const diff = now.getTime() - startTime.getTime();
		const minutes = Math.floor(diff / 60000);
		const hours = Math.floor(minutes / 60);
		const days = Math.floor(hours / 24);

		if (days > 0) {
			return `${days}d ${hours % 24}h`;
		} else if (hours > 0) {
			return `${hours}h ${minutes % 60}m`;
		}
		return `${minutes}m`;
	}

	function formatMemory(bytes: number): string {
		const units = ['B', 'KB', 'MB', 'GB'];
		let value = bytes;
		let unitIndex = 0;

		while (value >= 1024 && unitIndex < units.length - 1) {
			value /= 1024;
			unitIndex++;
		}

		return `${value.toFixed(1)}${units[unitIndex]}`;
	}

	// Focus management
	function handleFocus() {
		isFocused = true;
	}

	function handleBlur() {
		isFocused = false;
	}

	function handleMouseEnter() {
		isHovered = true;
	}

	function handleMouseLeave() {
		isHovered = false;
	}
</script>

<!-- Screen reader announcements -->
<div bind:this={announceElement} class="sr-only" aria-live="polite" aria-atomic="true"></div>

<div
	bind:this={cardElement}
	class="version-card glass-card group"
	class:selected={isSelected}
	class:compact
	class:touch-optimized={touchOptimized}
	class:opacity-75={version.status === 'not-found'}
	class:animate-pulse={version.status === 'starting' || version.status === 'stopping'}
	style:transform="scale({$cardScale}) translateY({-$cardElevation}px)"
	style:box-shadow="var(--shadow-glass), 0 {$cardElevation}px {$cardElevation * 2}px rgba(0, 212,
	255, {$glowIntensity * 0.3})"
	role="button"
	tabindex={isInteractive ? 0 : -1}
	aria-labelledby="version-{version.id}-title"
	aria-describedby="version-{version.id}-description version-{version.id}-status"
	aria-pressed={isSelected}
	aria-disabled={!isInteractive}
	onkeydown={handleKeydown}
	onfocus={handleFocus}
	onblur={handleBlur}
	onmouseenter={handleMouseEnter}
	onmouseleave={handleMouseLeave}
	ontouchstart={handleTouchStart}
	ontouchmove={handleTouchMove}
	ontouchend={handleTouchEnd}
>
	<!-- Skip link for keyboard navigation -->
	{#if isFocused}
		<div class="skip-link">
			<button
				onclick={() =>
					(cardElement.querySelector('.action-section button') as HTMLElement)?.focus()}
			>
				Skip to actions
			</button>
		</div>
	{/if}

	<!-- Enhanced status indicator with network awareness -->
	<div class="status-indicator-wrapper absolute right-4 top-4">
		<div class="status-indicator {currentStatus.class}" aria-hidden="true">
			<div class="status-dot" style:transform="scale({$pulseScale})"></div>
			{#if version.status === 'running'}
				<div class="pulse-ring"></div>
			{/if}
		</div>

		<!-- Network status indicator -->
		<div class="network-indicator" title="Network connection: {connectionStatus()}">
			{#if connectionStatus() === 'connected'}
				<Wifi size={12} class="text-neon-green" />
			{:else if connectionStatus() === 'offline'}
				<WifiOff size={12} class="text-red-500" />
			{:else}
				<div class="h-3 w-3 rounded-full bg-slate-500"></div>
			{/if}
		</div>
	</div>

	<!-- Enhanced header with better semantics -->
	<header class="version-header mb-4">
		<div class="flex items-start justify-between">
			<div class="flex-1">
				<h3 id="version-{version.id}-title" class="version-title mb-2 text-xl font-bold">
					{version.name}
				</h3>

				<p
					id="version-{version.id}-description"
					class="version-description mb-3 text-sm text-slate-400"
				>
					{version.description}
				</p>

				<!-- Enhanced status badge with better accessibility -->
				<div
					id="version-{version.id}-status"
					class="status-badge inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-semibold"
					role="status"
					aria-label={currentStatus.ariaLabel}
				>
					<IconComponent size={12} aria-hidden="true" />
					<span>{currentStatus.text}</span>
				</div>
			</div>

			<!-- Enhanced selection checkbox with better accessibility -->
			{#if isInteractive && (version.status === 'available' || version.status === 'running')}
				<label class="version-checkbox" aria-label="Select {version.name} for comparison">
					<input
						type="checkbox"
						checked={isSelected}
						onchange={handleSelect}
						disabled={!isInteractive}
						aria-describedby="version-{version.id}-title"
					/>
					<div class="checkbox-custom" aria-hidden="true"></div>
				</label>
			{/if}
		</div>
	</header>

	<!-- Tech Stack with better responsive design -->
	{#if version.techStack && version.techStack.length > 0 && !compact}
		<section class="tech-stack mb-4 flex flex-wrap gap-2" aria-label="Technology stack">
			{#each version.techStack as tech}
				<span class="tech-tag" role="img" aria-label="Technology: {tech}">{tech}</span>
			{/each}
		</section>
	{/if}

	<!-- Enhanced performance metrics with real-time updates -->
	{#if version.status === 'running'}
		<section class="metrics-section mb-4" aria-label="Performance metrics">
			<!-- Advanced performance score with better visualization -->
			<div class="performance-bar mb-3">
				<div class="mb-1 flex items-center justify-between">
					<span class="text-xs uppercase tracking-wide text-slate-400">Performance</span>
					<span
						class="text-electric-blue font-mono text-xs"
						aria-label="Performance score: {performanceScore()} percent"
					>
						{performanceScore()}%
					</span>
				</div>
				<div
					class="progress-track"
					role="progressbar"
					aria-valuenow={performanceScore()}
					aria-valuemin="0"
					aria-valuemax="100"
				>
					<div class="progress-fill" style="width: {$progressBar}%"></div>
				</div>
			</div>

			<!-- Enhanced metrics grid with better data visualization -->
			<div class="grid grid-cols-2 gap-3">
				{#if serverInfo}
					<div class="server-panel glass-card">
						<div class="flex items-center justify-between">
							<div>
								<div class="text-neon-green text-xs font-semibold">
									PORT {serverInfo.port}
								</div>
								<div
									class="text-xs text-slate-400"
									title="Uptime: {formatUptime(serverInfo.startTime)}"
								>
									Up {formatUptime(serverInfo.startTime)}
								</div>
							</div>
							<button
								onclick={openInBrowser}
								class="btn-icon"
								title="Open {version.name} in browser"
								aria-label="Open {version.name} in browser"
							>
								<ExternalLink size={12} aria-hidden="true" />
							</button>
						</div>
					</div>
				{/if}

				{#if metrics}
					<div class="metrics-panel glass-card">
						<div class="grid grid-cols-2 gap-1 text-xs">
							<div class="metric-item" title="Frames per second: {metrics.fps || 'N/A'}">
								<span class="text-slate-400" aria-label="FPS">
									<Activity size={10} class="inline" aria-hidden="true" />
									FPS
								</span>
								<span class="text-electric-blue font-mono">{metrics.fps || 'N/A'}</span>
							</div>
							<div
								class="metric-item"
								title="Memory usage: {metrics.memory
									? formatMemory(metrics.memory.used * 1024 * 1024)
									: 'N/A'}"
							>
								<span class="text-slate-400" aria-label="Memory">
									<HardDrive size={10} class="inline" aria-hidden="true" />
									MEM
								</span>
								<span class="text-neon-green font-mono">
									{metrics.memory ? `${metrics.memory.used}MB` : 'N/A'}
								</span>
							</div>
						</div>
					</div>
				{/if}
			</div>
		</section>
	{/if}

	<!-- Enhanced action section with better keyboard support -->
	<section class="action-section" aria-label="Version actions">
		{#if version.status === 'available'}
			<button
				onclick={handleStart}
				disabled={isStarting}
				class="launch-button btn-electric"
				aria-describedby="launch-{version.id}-description"
			>
				{#if isStarting}
					<Clock size={16} class="animate-spin" aria-hidden="true" />
					Starting...
				{:else}
					<Rocket size={16} aria-hidden="true" />
					Launch
				{/if}
			</button>
			<div id="launch-{version.id}-description" class="sr-only">
				Press Enter or click to launch {version.name}
			</div>
		{:else if version.status === 'running'}
			<div class="flex gap-2" role="group" aria-label="Running version controls">
				<button
					onclick={handleRestart}
					class="btn-glass flex-1"
					title="Restart {version.name} (Press R)"
					aria-label="Restart {version.name}"
				>
					<RotateCcw size={14} aria-hidden="true" />
					{compact ? '' : 'Restart'}
				</button>
				<button
					onclick={handleStop}
					disabled={isStopping}
					class="btn-glass"
					title="Stop {version.name} (Press S)"
					aria-label="Stop {version.name}"
				>
					{#if isStopping}
						<Clock size={14} class="animate-spin" aria-hidden="true" />
					{:else}
						<Square size={14} aria-hidden="true" />
					{/if}
				</button>
			</div>
		{:else if version.status === 'not-found'}
			<div class="not-found-panel" role="alert" aria-label="Version not found">
				<Package size={24} class="mx-auto mb-2 text-slate-500" aria-hidden="true" />
				<div class="text-center text-xs text-slate-500">Version Not Found</div>
			</div>
		{:else if version.status === 'error'}
			<button
				onclick={handleStart}
				class="launch-button bg-neon-orange"
				aria-label="Retry launching {version.name}"
			>
				<RotateCcw size={16} aria-hidden="true" />
				Retry
			</button>
		{/if}
	</section>

	<!-- Features section with better accessibility -->
	{#if version.features && version.features.length > 0 && !compact}
		<details class="features-section mt-4">
			<summary class="features-summary" aria-label="Show {version.features.length} features">
				Features ({version.features.length})
			</summary>
			<ul class="features-list mt-2 space-y-1" role="list">
				{#each version.features as feature}
					<li class="feature-item" role="listitem">
						<CheckCircle2 size={10} class="text-neon-green flex-shrink-0" aria-hidden="true" />
						{feature}
					</li>
				{/each}
			</ul>
		</details>
	{/if}

	<!-- Keyboard shortcuts hint (visible on focus) -->
	{#if isFocused && isInteractive}
		<div class="keyboard-hints" role="region" aria-label="Keyboard shortcuts">
			<div class="mt-2 rounded bg-black/20 p-2 text-xs text-slate-400">
				<div class="mb-1 font-semibold">Shortcuts:</div>
				{#each Object.entries(keyboardShortcuts()) as [key, description]}
					<div class="flex justify-between">
						<kbd class="rounded bg-slate-700 px-1 text-xs">{key}</kbd>
						<span class="text-xs">{description}</span>
					</div>
				{/each}
			</div>
		</div>
	{/if}
</div>

<style>
	/* Enhanced base styles with better performance */
	.version-card {
		padding: 1.5rem;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		position: relative;
		min-height: 280px;
		border-radius: 1rem;
		backdrop-filter: blur(20px);
		will-change: transform, box-shadow;
		contain: layout style paint;
	}

	.version-card.compact {
		min-height: 200px;
		padding: 1rem;
	}

	.version-card.touch-optimized {
		min-height: 320px;
		padding: 1.75rem;
	}

	.version-card:focus-visible {
		outline: 2px solid var(--electric-blue);
		outline-offset: 2px;
	}

	.version-card.selected {
		border-color: var(--electric-blue);
		background: rgba(0, 212, 255, 0.1);
	}

	/* Enhanced typography with better contrast */
	.version-title {
		background: linear-gradient(135deg, var(--electric-blue) 0%, var(--cyber-blue) 100%);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
		line-height: 1.2;
	}

	/* Advanced status indicators */
	.status-indicator-wrapper {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		align-items: center;
	}

	.status-indicator {
		width: 16px;
		height: 16px;
		position: relative;
	}

	.status-dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		position: relative;
		transition: all 0.3s ease-out;
	}

	.status-running .status-dot {
		background: var(--neon-green);
		box-shadow: 0 0 10px var(--neon-green);
	}

	.status-available .status-dot {
		background: var(--electric-blue);
		box-shadow: 0 0 8px var(--electric-blue);
	}

	.status-error .status-dot {
		background: #ef4444;
		box-shadow: 0 0 8px #ef4444;
	}

	.pulse-ring {
		position: absolute;
		top: -4px;
		left: -4px;
		right: -4px;
		bottom: -4px;
		border: 2px solid var(--neon-green);
		border-radius: 50%;
		animation: pulse-ring 2s ease-in-out infinite;
		opacity: 0.7;
	}

	@keyframes pulse-ring {
		0% {
			transform: scale(0.8);
			opacity: 1;
		}
		100% {
			transform: scale(1.4);
			opacity: 0;
		}
	}

	/* Network indicator */
	.network-indicator {
		width: 16px;
		height: 16px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	/* Enhanced status badge */
	.status-badge {
		background: rgba(255, 255, 255, 0.1);
		border-color: var(--border-primary);
		color: var(--text-secondary);
		transition: all 0.2s ease-out;
	}

	.status-badge.status-running {
		background: rgba(16, 185, 129, 0.2);
		border-color: var(--neon-green);
		color: var(--neon-green);
	}

	/* Enhanced tech tags with better spacing */
	.tech-tag {
		padding: 0.25rem 0.5rem;
		background: rgba(0, 212, 255, 0.2);
		color: var(--electric-blue);
		border: 1px solid var(--electric-blue);
		border-radius: 0.375rem;
		font-size: 0.6875rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		transition: all 0.2s ease-out;
	}

	.tech-tag:hover {
		background: rgba(0, 212, 255, 0.3);
		transform: translateY(-1px);
	}

	/* Enhanced progress indicators */
	.progress-track {
		height: 6px;
		background: rgba(30, 41, 59, 0.5);
		border-radius: 3px;
		overflow: hidden;
		position: relative;
	}

	.progress-fill {
		height: 100%;
		background: linear-gradient(90deg, var(--neon-green) 0%, var(--electric-blue) 100%);
		transition: width 1.2s cubic-bezier(0.4, 0, 0.2, 1);
		border-radius: 3px;
		position: relative;
	}

	.progress-fill::after {
		content: '';
		position: absolute;
		top: 0;
		left: -100%;
		width: 100%;
		height: 100%;
		background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
		animation: progress-shimmer 2s infinite;
	}

	@keyframes progress-shimmer {
		0% {
			left: -100%;
		}
		100% {
			left: 100%;
		}
	}

	/* Enhanced panels */
	.server-panel,
	.metrics-panel {
		padding: 0.75rem;
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		backdrop-filter: blur(10px);
		transition: all 0.2s ease-out;
	}

	.server-panel:hover,
	.metrics-panel:hover {
		background: rgba(255, 255, 255, 0.08);
		border-color: rgba(255, 255, 255, 0.2);
	}

	.metric-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 0.25rem;
	}

	/* Enhanced buttons with better touch targets */
	.launch-button {
		width: 100%;
		padding: 0.875rem 1.5rem;
		border-radius: 0.75rem;
		font-weight: 600;
		border: none;
		cursor: pointer;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.5rem;
		background: var(--gradient-electric);
		color: white;
		box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
		position: relative;
		overflow: hidden;
	}

	.touch-optimized .launch-button {
		padding: 1rem 1.5rem;
		min-height: 48px;
	}

	.launch-button:hover:not(:disabled) {
		transform: translateY(-2px);
		box-shadow: 0 8px 25px rgba(0, 212, 255, 0.4);
		filter: brightness(1.1);
	}

	.launch-button:active:not(:disabled) {
		transform: translateY(0);
	}

	.launch-button:disabled {
		opacity: 0.7;
		cursor: not-allowed;
	}

	.launch-button::before {
		content: '';
		position: absolute;
		top: 0;
		left: -100%;
		width: 100%;
		height: 100%;
		background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
		transition: left 0.5s ease-out;
	}

	.launch-button:hover::before {
		left: 100%;
	}

	/* Enhanced glass buttons */
	.btn-glass {
		padding: 0.5rem 1rem;
		background: var(--gradient-glass);
		color: var(--text-primary);
		border: 1px solid var(--border-primary);
		border-radius: 0.5rem;
		backdrop-filter: blur(10px);
		cursor: pointer;
		transition: all 0.2s ease-out;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.5rem;
		font-size: 0.875rem;
		min-height: 36px;
	}

	.touch-optimized .btn-glass {
		min-height: 44px;
		padding: 0.75rem 1rem;
	}

	.btn-glass:hover:not(:disabled) {
		background: rgba(255, 255, 255, 0.15);
		border-color: var(--border-secondary);
		transform: translateY(-1px);
	}

	.btn-glass:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.btn-icon {
		padding: 0.375rem;
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 0.375rem;
		color: var(--electric-blue);
		cursor: pointer;
		transition: all 0.2s ease-out;
		min-width: 28px;
		min-height: 28px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.touch-optimized .btn-icon {
		min-width: 40px;
		min-height: 40px;
		padding: 0.5rem;
	}

	.btn-icon:hover {
		background: rgba(255, 255, 255, 0.2);
		transform: scale(1.05);
	}

	.btn-icon:focus-visible {
		outline: 2px solid var(--electric-blue);
		outline-offset: 2px;
	}

	/* Enhanced checkbox with better accessibility */
	.version-checkbox {
		position: relative;
		cursor: pointer;
		min-width: 20px;
		min-height: 20px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.touch-optimized .version-checkbox {
		min-width: 32px;
		min-height: 32px;
	}

	.version-checkbox input {
		opacity: 0;
		position: absolute;
		width: 100%;
		height: 100%;
		margin: 0;
		cursor: pointer;
	}

	.checkbox-custom {
		width: 18px;
		height: 18px;
		border: 2px solid var(--border-primary);
		border-radius: 0.25rem;
		background: transparent;
		transition: all 0.2s ease-out;
		position: relative;
	}

	.touch-optimized .checkbox-custom {
		width: 24px;
		height: 24px;
	}

	.version-checkbox input:checked + .checkbox-custom {
		background: var(--gradient-electric);
		border-color: var(--electric-blue);
	}

	.version-checkbox input:focus + .checkbox-custom {
		outline: 2px solid var(--electric-blue);
		outline-offset: 2px;
	}

	.checkbox-custom::after {
		content: '';
		position: absolute;
		top: 1px;
		left: 4px;
		width: 6px;
		height: 10px;
		border: solid white;
		border-width: 0 2px 2px 0;
		transform: rotate(45deg);
		opacity: 0;
		transition: opacity 0.2s ease-out;
	}

	.touch-optimized .checkbox-custom::after {
		top: 2px;
		left: 6px;
		width: 8px;
		height: 12px;
	}

	.version-checkbox input:checked + .checkbox-custom::after {
		opacity: 1;
	}

	/* Enhanced features section */
	.features-section {
		border-top: 1px solid rgba(255, 255, 255, 0.1);
		padding-top: 1rem;
	}

	.features-summary {
		font-size: 0.875rem;
		font-weight: 500;
		color: var(--text-secondary);
		cursor: pointer;
		transition: color 0.2s ease-out;
		padding: 0.25rem 0;
	}

	.features-summary:hover {
		color: var(--electric-blue);
	}

	.features-summary:focus-visible {
		outline: 2px solid var(--electric-blue);
		outline-offset: 2px;
		border-radius: 0.25rem;
	}

	.feature-item {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		font-size: 0.875rem;
		color: var(--text-tertiary);
		padding: 0.125rem 0;
	}

	/* Not found panel */
	.not-found-panel {
		padding: 1.5rem 1rem;
		text-align: center;
		background: rgba(100, 116, 139, 0.1);
		border: 1px solid rgba(100, 116, 139, 0.3);
		border-radius: 0.75rem;
	}

	/* Skip link for accessibility */
	.skip-link {
		position: absolute;
		top: -2rem;
		left: 0.5rem;
		z-index: 1000;
	}

	.skip-link button {
		background: var(--electric-blue);
		color: white;
		padding: 0.5rem 1rem;
		border: none;
		border-radius: 0.25rem;
		font-size: 0.875rem;
		cursor: pointer;
	}

	/* Keyboard hints */
	.keyboard-hints {
		position: absolute;
		bottom: 100%;
		left: 0;
		right: 0;
		z-index: 100;
		margin-bottom: 0.5rem;
	}

	.keyboard-hints kbd {
		font-family: inherit;
		font-size: 0.75rem;
	}

	/* Screen reader only content */
	.sr-only {
		position: absolute;
		width: 1px;
		height: 1px;
		padding: 0;
		margin: -1px;
		overflow: hidden;
		clip: rect(0, 0, 0, 0);
		white-space: nowrap;
		border: 0;
	}

	/* Reduced motion support */
	@media (prefers-reduced-motion: reduce) {
		.version-card,
		.launch-button,
		.btn-glass,
		.btn-icon,
		.progress-fill,
		.status-dot,
		.pulse-ring {
			transition: none;
			animation: none;
		}

		.version-card:hover {
			transform: none;
		}
	}

	/* High contrast mode support */
	@media (prefers-contrast: high) {
		.version-card {
			border: 2px solid;
		}

		.status-dot {
			border: 2px solid currentColor;
		}

		.tech-tag {
			border-width: 2px;
		}
	}

	/* Dark mode optimizations */
	@media (prefers-color-scheme: dark) {
		.version-card {
			background: rgba(0, 0, 0, 0.3);
		}

		.server-panel,
		.metrics-panel {
			background: rgba(0, 0, 0, 0.2);
		}
	}

	/* Container queries for responsive design */
	@container (max-width: 280px) {
		.tech-stack {
			display: none;
		}

		.metrics-section .grid {
			grid-template-columns: 1fr;
		}
	}

	@container (max-width: 320px) {
		.version-card {
			padding: 1rem;
		}

		.btn-glass span {
			display: none;
		}
	}
</style>
