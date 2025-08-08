<script lang="ts">
	// Import Lucide icons
	import Maximize2 from 'lucide-svelte/icons/maximize-2';
	import Minimize2 from 'lucide-svelte/icons/minimize-2';
	import Sun from 'lucide-svelte/icons/sun';
	import Moon from 'lucide-svelte/icons/moon';

	// Props
	let {
		isDarkMode = false,
		onThemeToggle,
		activeTab = 'animator',
		onTabChange
	}: {
		isDarkMode?: boolean;
		onThemeToggle?: () => void;
		activeTab?: 'animator' | 'constructor';
		onTabChange?: (tab: 'animator' | 'constructor') => void;
	} = $props();

	// Local fullscreen state
	let isFullScreen = $state(false);

	// Full-screen functionality
	function toggleFullScreen(): void {
		if (!document.fullscreenElement) {
			document.documentElement
				.requestFullscreen()
				.then(() => {
					isFullScreen = true;
				})
				.catch((err) => {
					console.warn('Failed to enter fullscreen:', err);
				});
		} else {
			document
				.exitFullscreen()
				.then(() => {
					isFullScreen = false;
				})
				.catch((err) => {
					console.warn('Failed to exit fullscreen:', err);
				});
		}
	}

	// Listen for fullscreen changes (e.g., ESC key)
	$effect(() => {
		function handleFullscreenChange(): void {
			isFullScreen = !!document.fullscreenElement;
		}

		document.addEventListener('fullscreenchange', handleFullscreenChange);
		return () => {
			document.removeEventListener('fullscreenchange', handleFullscreenChange);
		};
	});
</script>

<header class="app-header">
	<div class="header-content">
		<div class="header-branding">
			<div class="header-icon">🎭</div>
			<div class="header-text">
				<h1>TKA Web</h1>
			</div>
		</div>

		<!-- Tab Navigation -->
		<div class="tab-navigation">
			<button
				type="button"
				class="tab-button"
				class:active={activeTab === 'animator'}
				onclick={() => onTabChange?.('animator')}
			>
				🎬 Animator
			</button>
			<button
				type="button"
				class="tab-button"
				class:active={activeTab === 'constructor'}
				onclick={() => onTabChange?.('constructor')}
			>
				⚒️ Constructor
			</button>
		</div>
		<div class="header-controls">
			<!-- Fullscreen Button -->
			<button
				type="button"
				class="header-button fullscreen-button"
				onclick={toggleFullScreen}
				title={isFullScreen ? 'Exit full screen' : 'Enter full screen'}
				aria-label={isFullScreen ? 'Exit full screen' : 'Enter full screen'}
			>
				{#if isFullScreen}
					<Minimize2 size={20} />
				{:else}
					<Maximize2 size={20} />
				{/if}
			</button>

			<!-- Theme Toggle Button -->
			<button
				type="button"
				class="header-button theme-toggle"
				onclick={onThemeToggle}
				title={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
				aria-label={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
			>
				{#if isDarkMode}
					<Sun size={20} />
				{:else}
					<Moon size={20} />
				{/if}
			</button>
		</div>
	</div>
</header>

<style>
	.app-header {
		background: var(--header-gradient);
		border-bottom: none;
		box-shadow: var(--header-shadow);
		padding: 0.75rem 1.5rem;
		flex-shrink: 0;
		transition: all 0.3s ease;
		position: relative;
		z-index: 100;
	}

	.header-content {
		display: flex;
		justify-content: space-between;
		align-items: center;
		max-width: 1400px;
		margin: 0 auto;
	}

	.header-branding {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		min-width: 0;
		flex: 1;
	}

	.header-icon {
		font-size: 1.5rem;
		filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
		flex-shrink: 0;
	}

	.header-text {
		min-width: 0;
		overflow: hidden;
	}

	.header-text h1 {
		margin: 0;
		font-size: 1.25rem;
		font-weight: 700;
		color: white;
		line-height: 1.2;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
		letter-spacing: -0.025em;
	}

	.header-controls {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		flex-shrink: 0;
	}

	.header-button {
		background: rgba(255, 255, 255, 0.15);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 50%;
		width: 40px;
		height: 40px;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		font-size: 1.1rem;
		transition: all 0.2s ease;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
		color: white;
		backdrop-filter: blur(10px);
	}

	.header-button:hover {
		background: rgba(255, 255, 255, 0.25);
		border-color: rgba(255, 255, 255, 0.3);
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
	}

	.header-button:active {
		transform: translateY(0);
	}

	/* Specific button styles */
	.fullscreen-button {
		background: rgba(100, 149, 237, 0.15);
		border-color: rgba(100, 149, 237, 0.3);
	}

	.fullscreen-button:hover {
		background: rgba(100, 149, 237, 0.25);
		border-color: rgba(100, 149, 237, 0.4);
	}

	/* Mobile Layout */
	@media (max-width: 768px) {
		.app-header {
			padding: 0.5rem 1rem;
		}

		.header-branding {
			gap: 0.5rem;
		}

		.header-icon {
			font-size: 1.25rem;
		}

		.header-text h1 {
			font-size: 1.1rem;
		}

		.header-controls {
			gap: 0.25rem;
		}

		.header-button {
			width: 36px;
			height: 36px;
			font-size: 1rem;
		}
	}

	/* Small Mobile Layout */
	@media (max-width: 480px) {
		.header-text h1 {
			font-size: 1rem;
		}

		.header-button {
			width: 32px;
			height: 32px;
			font-size: 0.9rem;
		}
	}
</style>
