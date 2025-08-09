<script lang="ts">
	// Import simplified state
	import {
		getActiveTab,
		isTabActive,
		switchTab,
		getShowSettings,
		getSettings,
		getIsTransitioning
	} from '$stores/appState.svelte';

	// Import simple fade system
	import { fade, slideInFade, conditionalTransition } from '$utils/simpleFade';

	// Reactive state for template
	let activeTab = $derived(getActiveTab());
	let showSettings = $derived(getShowSettings());
	let settings = $derived(getSettings());
	let isTransitioning = $derived(getIsTransitioning());

	// Import tab components
	import ConstructTab from './tabs/ConstructTab.svelte';
	import BrowseTab from './tabs/BrowseTab.svelte';
	import WriteTab from './tabs/WriteTab.svelte';
	import LearnTab from './tabs/LearnTab.svelte';
	import SequenceCardTab from './tabs/SequenceCardTab.svelte';
	import NavigationBar from './navigation/NavigationBar.svelte';
	import SettingsDialog from './SettingsDialog.svelte';
	import BackgroundProvider from './backgrounds/BackgroundProvider.svelte';
	import BackgroundCanvas from './backgrounds/BackgroundCanvas.svelte';

	// Simple transition functions that respect animation settings
	const tabIn = conditionalTransition((node: Element) => slideInFade(node, { 
		duration: 300, 
		direction: 'right' 
	}));
	
	const tabOut = conditionalTransition((node: Element) => fade(node, { 
		duration: 250 
	}));

	// Tab configuration
	const tabs = [
		{ id: 'construct', label: 'Construct', icon: '🔧' },
		{ id: 'browse', label: 'Browse', icon: '🔍' },
		{ id: 'sequence_card', label: 'Sequence Card', icon: '🎴' },
		{ id: 'write', label: 'Write', icon: '✍️' },
		{ id: 'learn', label: 'Learn', icon: '🧠' },
	] as const;
</script>

<BackgroundProvider>
	<div class="main-interface">
		<!-- Background Canvas -->
		{#if settings.backgroundEnabled}
			<BackgroundCanvas
				backgroundType={settings.backgroundType || 'aurora'}
				quality={settings.backgroundQuality || 'medium'}
				onReady={() =>
					console.log(
						`🌌 Background ready: ${settings.backgroundType} at ${settings.backgroundQuality} quality`
					)}
			/>
		{/if}

		<NavigationBar {tabs} {activeTab} onTabSelect={switchTab} />

		<main class="content-area">
			<!-- Simple tab content with reliable transitions -->
			{#key activeTab}
				<div class="tab-content" in:tabIn out:tabOut>
					{#if isTabActive('construct')}
						<ConstructTab />
					{:else if isTabActive('browse')}
						<BrowseTab />
					{:else if isTabActive('sequence_card')}
						<SequenceCardTab />
					{:else if isTabActive('write')}
						<WriteTab />
					{:else if isTabActive('learn')}
						<LearnTab />
					{/if}
				</div>
			{/key}

			<!-- Simple transition indicator -->
			{#if isTransitioning}
				<div class="transition-indicator">
					Switching to {activeTab}...
				</div>
			{/if}
		</main>
	</div>
</BackgroundProvider>

<!-- Settings Dialog -->
{#if showSettings}
	<SettingsDialog />
{/if}

<style>
	.main-interface {
		display: flex;
		flex-direction: column;
		height: 100vh;
		width: 100%;
		overflow: hidden;
		position: relative;
	}

	.content-area {
		flex: 1;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		position: relative;
	}

	.tab-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		width: 100%;
		height: 100%;
	}

	.transition-indicator {
		position: absolute;
		top: 20px;
		left: 50%;
		transform: translateX(-50%);
		background: rgba(0, 123, 255, 0.9);
		color: white;
		padding: 8px 16px;
		border-radius: 20px;
		font-size: 14px;
		z-index: 1000;
		pointer-events: none;
	}

	/* Disable animations when user prefers reduced motion */
	@media (prefers-reduced-motion: reduce) {
		* {
			transition: none !important;
			animation: none !important;
		}
	}
</style>
