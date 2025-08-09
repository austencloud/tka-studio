<!-- Navigation Bar - Tab switching interface with fade system integration -->
<script lang="ts">
	import {
		showSettingsDialog,
		getIsMainTabTransitioning,
		getMainTabTransitionState,
	} from '$stores/appState.svelte';
	import { isFadeEnabled } from '$services/ui/animation';

	interface Props {
		tabs: readonly { id: string; label: string; icon: string }[];
		activeTab: string;
		onTabSelect: (tab: any) => void;
	}

	let { tabs, activeTab, onTabSelect }: Props = $props();

	// Reactive state for transition feedback
	let isTransitioning = $derived(getIsMainTabTransitioning());
	let transitionState = $derived(getMainTabTransitionState());
	let fadeEnabled = $derived(() => {
		try {
			return isFadeEnabled();
		} catch {
			return false;
		}
	});

	// Handle tab click with transition feedback
	async function handleTabClick(tab: { id: string; label: string; icon: string }) {
		if (isTransitioning) {
			console.log('🎭 Tab transition in progress, ignoring click');
			return;
		}

		try {
			await onTabSelect(tab.id as any);
		} catch (error) {
			console.error('Failed to select tab:', error);
		}
	}

	// Check if a specific tab is currently transitioning
	function isTabTransitioning(tabId: string): boolean {
		return (
			isTransitioning &&
			(transitionState.fromTab === tabId || transitionState.toTab === tabId)
		);
	}
</script>

<nav class="navigation-bar glass-surface" class:transitioning={isTransitioning}>
	<div class="nav-brand">
		<h1>TKA</h1>
		<span class="version">v2.0</span>
		{#if fadeEnabled}
			<span class="fade-indicator" title="Fade animations enabled">🎭</span>
		{/if}
	</div>

	<div class="nav-tabs">
		{#each tabs as tab}
			<button
				class="nav-tab"
				class:active={activeTab === tab.id}
				class:transitioning={isTabTransitioning(tab.id)}
				class:disabled={isTransitioning && !isTabTransitioning(tab.id)}
				onclick={() => handleTabClick(tab)}
				disabled={isTransitioning && !isTabTransitioning(tab.id)}
			>
				<span class="tab-icon">{tab.icon}</span>
				<span class="tab-label">{tab.label}</span>
				{#if isTabTransitioning(tab.id)}
					<span class="transition-indicator">⟳</span>
				{/if}
			</button>
		{/each}
	</div>

	<div class="nav-actions">
		<button
			class="nav-action"
			onclick={showSettingsDialog}
			title="Settings (Ctrl+,)"
			aria-label="Open Settings"
		>
			<svg width="20" height="20" viewBox="0 0 24 24" fill="none">
				<circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2" />
				<path
					d="m12 1 2.09.87.87 2.09-2.09.87-.87-2.09L12 1zM12 23l-2.09-.87-.87-2.09 2.09-.87.87 2.09L12 23zM1 12l.87-2.09L3.96 9l.87 2.09L5.7 12l-.87 2.09L3.96 15l-.87-2.09L1 12zM23 12l-.87 2.09L20.04 15l-.87-2.09L18.3 12l.87-2.09L20.04 9l.87 2.09L23 12z"
					stroke="currentColor"
					stroke-width="2"
				/>
			</svg>
		</button>
	</div>
</nav>

<style>
	.navigation-bar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: var(--spacing-md) var(--spacing-lg);
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
		backdrop-filter: var(--glass-backdrop-strong);
	}

	.nav-brand {
		display: flex;
		align-items: center;
		gap: var(--spacing-sm);
	}

	.nav-brand h1 {
		font-size: var(--font-size-xl);
		font-weight: 700;
		background: var(--gradient-primary);
		background-clip: text;
		-webkit-background-clip: text;
		color: transparent;
		margin: 0;
	}

	.version {
		font-size: var(--font-size-xs);
		color: var(--muted-foreground);
		background: rgba(255, 255, 255, 0.1);
		padding: 2px 6px;
		border-radius: 4px;
	}

	.nav-tabs {
		display: flex;
		gap: var(--spacing-sm);
	}

	.nav-tab {
		display: flex;
		align-items: center;
		gap: var(--spacing-sm);
		padding: var(--spacing-sm) var(--spacing-md);
		background: transparent;
		border: none;
		border-radius: 8px;
		color: var(--muted-foreground);
		cursor: pointer;
		transition: all var(--transition-fast);
		font-size: var(--font-size-sm);
		font-weight: 500;
	}

	.nav-tab:hover {
		background: rgba(255, 255, 255, 0.05);
		color: var(--foreground);
	}

	.nav-tab.active {
		background: rgba(99, 102, 241, 0.2);
		color: var(--primary-light);
		border: 1px solid rgba(99, 102, 241, 0.3);
	}

	.tab-icon {
		font-size: 16px;
	}

	.tab-label {
		font-weight: 500;
	}

	.nav-actions {
		display: flex;
		gap: var(--spacing-sm);
	}

	.nav-action {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 40px;
		height: 40px;
		background: transparent;
		border: none;
		border-radius: 8px;
		color: var(--muted-foreground);
		cursor: pointer;
		transition: all var(--transition-fast);
	}

	.nav-action:hover {
		background: rgba(255, 255, 255, 0.1);
		color: var(--foreground);
	}

	/* Fade system integration */
	.fade-indicator {
		font-size: 10px;
		opacity: 0.6;
		margin-left: 4px;
	}

	.navigation-bar.transitioning {
		pointer-events: none;
	}

	.navigation-bar.transitioning .nav-tabs {
		opacity: 0.8;
	}

	.nav-tab.transitioning {
		pointer-events: auto;
		position: relative;
		overflow: hidden;
	}

	.nav-tab.transitioning::after {
		content: '';
		position: absolute;
		top: 0;
		left: -100%;
		width: 100%;
		height: 100%;
		background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
		animation: shimmer 1s infinite;
	}

	.nav-tab.disabled {
		opacity: 0.5;
		cursor: not-allowed;
		pointer-events: none;
	}

	.transition-indicator {
		font-size: 12px;
		animation: spin 1s linear infinite;
		margin-left: 4px;
	}

	@keyframes shimmer {
		0% {
			left: -100%;
		}
		100% {
			left: 100%;
		}
	}

	@keyframes spin {
		from {
			transform: rotate(0deg);
		}
		to {
			transform: rotate(360deg);
		}
	}
	@media (max-width: 768px) {
		.navigation-bar {
			padding: var(--spacing-sm) var(--spacing-md);
		}

		.nav-tabs {
			gap: var(--spacing-xs);
		}

		.nav-tab {
			padding: var(--spacing-xs) var(--spacing-sm);
			font-size: var(--font-size-xs);
		}

		.tab-label {
			display: none;
		}

		.tab-icon {
			font-size: 18px;
		}

		.nav-brand h1 {
			font-size: var(--font-size-lg);
		}
	}
</style>
