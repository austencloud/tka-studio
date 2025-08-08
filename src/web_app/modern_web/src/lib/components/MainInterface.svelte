/**
 * Main Interface - Core application interface
 * 
 * The main interface that houses all application functionality.
 * Uses pure Svelte 5 runes for state management.
 */

<script lang="ts">
	// Import runes-based state
	import { getActiveTab, isTabActive, switchTab } from '$stores/appState.svelte';

	// Reactive state for template
	let activeTab = $derived(getActiveTab());

	// Import tab components (will be created)
	import ConstructTab from './tabs/ConstructTab.svelte';
	import GenerateTab from './tabs/GenerateTab.svelte';
	import BrowseTab from './tabs/BrowseTab.svelte';
	import LearnTab from './tabs/LearnTab.svelte';
	import NavigationBar from './navigation/NavigationBar.svelte';

	// Tab configuration
	const tabs = [
		{ id: 'construct', label: 'Construct', icon: '🏗️' },
		{ id: 'generate', label: 'Generate', icon: '✨' },
		{ id: 'browse', label: 'Browse', icon: '📚' },
		{ id: 'learn', label: 'Learn', icon: '🎓' }
	] as const;
</script>

<div class="main-interface">
	<NavigationBar {tabs} {activeTab} onTabSelect={switchTab} />
	
	<main class="content-area">
		{#if isTabActive('construct')}
			<ConstructTab />
		{:else if isTabActive('generate')}
			<GenerateTab />
		{:else if isTabActive('browse')}
			<BrowseTab />
		{:else if isTabActive('learn')}
			<LearnTab />
		{/if}
	</main>
</div>

<style>
	.main-interface {
		display: flex;
		flex-direction: column;
		height: 100vh;
		width: 100%;
		overflow: hidden;
	}

	.content-area {
		flex: 1;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		position: relative;
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.main-interface {
			height: 100vh;
			height: 100dvh; /* Dynamic viewport height for mobile */
		}
	}
</style>
