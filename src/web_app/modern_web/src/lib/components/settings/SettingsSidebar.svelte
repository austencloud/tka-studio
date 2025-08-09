<!-- SettingsSidebar.svelte - Improved contrast navigation sidebar -->
<script lang="ts">
	interface Tab {
		id: string;
		label: string;
		icon: string;
	}

	interface Props {
		tabs: Tab[];
		activeTab: string;
		onTabSelect: (tabId: string) => void;
	}

	let { tabs, activeTab, onTabSelect }: Props = $props();

	function handleTabClick(tabId: string) {
		onTabSelect(tabId);
	}
</script>

<aside class="settings-sidebar">
	<nav class="sidebar-nav">
		{#each tabs as tab}
			<button
				class="sidebar-item"
				class:active={activeTab === tab.id}
				onclick={() => handleTabClick(tab.id)}
			>
				<span class="sidebar-icon">{tab.icon}</span>
				<span class="sidebar-label">{tab.label}</span>
			</button>
		{/each}
	</nav>
</aside>

<style>
	.settings-sidebar {
		width: 200px;
		background: rgba(255, 255, 255, 0.08);
		border-right: 1px solid rgba(255, 255, 255, 0.2);
		overflow-y: auto;
	}

	.sidebar-nav {
		padding: var(--spacing-md);
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.sidebar-item {
		display: flex;
		align-items: center;
		gap: var(--spacing-sm);
		padding: var(--spacing-md);
		background: transparent;
		border: none;
		border-radius: 8px;
		color: rgba(255, 255, 255, 0.8);
		cursor: pointer;
		transition: all var(--transition-fast);
		text-align: left;
		width: 100%;
		font-size: var(--font-size-sm);
		font-weight: 500;
	}

	.sidebar-item:hover {
		background: rgba(255, 255, 255, 0.1);
		color: #ffffff;
	}

	.sidebar-item.active {
		background: rgba(99, 102, 241, 0.3);
		color: #ffffff;
		border: 1px solid rgba(99, 102, 241, 0.5);
	}

	.sidebar-icon {
		font-size: 16px;
		width: 20px;
		text-align: center;
	}

	/* Mobile responsive */
	@media (max-width: 768px) {
		.settings-sidebar {
			width: 100%;
			border-right: none;
			border-bottom: 1px solid rgba(255, 255, 255, 0.2);
		}

		.sidebar-nav {
			flex-direction: row;
			overflow-x: auto;
			padding: var(--spacing-sm);
		}

		.sidebar-item {
			flex-shrink: 0;
			min-width: 100px;
		}
	}
</style>
