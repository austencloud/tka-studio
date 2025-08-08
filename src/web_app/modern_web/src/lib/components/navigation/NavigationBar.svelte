<!-- Navigation Bar - Tab switching interface -->
<script lang="ts">
	import { showSettingsDialog } from '$stores/appState.svelte';

	interface Props {
		tabs: readonly { id: string; label: string; icon: string }[];
		activeTab: string;
		onTabSelect: (tab: any) => void;
	}

	let { tabs, activeTab, onTabSelect }: Props = $props();

	// Handle tab click
	function handleTabClick(tab: { id: string; label: string; icon: string }) {
		onTabSelect(tab.id as any);
	}
</script>

<nav class="navigation-bar glass-surface">
	<div class="nav-brand">
		<h1>TKA</h1>
		<span class="version">v2.0</span>
	</div>

	<div class="nav-tabs">
		{#each tabs as tab}
			<button 
				class="nav-tab" 
				class:active={activeTab === tab.id}
				onclick={() => handleTabClick(tab)}
			>
				<span class="tab-icon">{tab.icon}</span>
				<span class="tab-label">{tab.label}</span>
			</button>
		{/each}
	</div>

	<div class="nav-actions">
		<button class="nav-action" onclick={showSettingsDialog} title="Settings (Ctrl+,)" aria-label="Open Settings">
			<svg width="20" height="20" viewBox="0 0 24 24" fill="none">
				<circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
				<path d="m12 1 2.09.87.87 2.09-2.09.87-.87-2.09L12 1zM12 23l-2.09-.87-.87-2.09 2.09-.87.87 2.09L12 23zM1 12l.87-2.09L3.96 9l.87 2.09L5.7 12l-.87 2.09L3.96 15l-.87-2.09L1 12zM23 12l-.87 2.09L20.04 15l-.87-2.09L18.3 12l.87-2.09L20.04 9l.87 2.09L23 12z" stroke="currentColor" stroke-width="2"/>
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

	/* Mobile responsive */
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
