<script lang="ts">
	// Import state management functions - updated to work with consolidated MainInterface
	import {
		getActiveTab,
		getIsTransitioning,
		getSettings,
		getShowSettings,
		isTabActive,
		switchTab,
	} from '$lib/state/appState.svelte';
	// Import simple fade system
	import { fade } from '$lib/utils/simpleFade';
	// Import tab components
	import BackgroundCanvas from './backgrounds/BackgroundCanvas.svelte';
	import BackgroundProvider from './backgrounds/BackgroundProvider.svelte';
	import NavigationBar from './navigation/NavigationBar.svelte';
	import SettingsDialog from './SettingsDialog.svelte';
	import BrowseTab from './tabs/BrowseTab.svelte';
	import ConstructTab from './tabs/ConstructTab.svelte';
	import LearnTab from './tabs/LearnTab.svelte';
	import SequenceCardTab from './tabs/SequenceCardTab.svelte';
	import WriteTab from './tabs/WriteTab.svelte';

	// Reactive state for template using proper derived
	let activeTab = $derived(getActiveTab());
	let showSettings = $derived(getShowSettings());
	let settings = $derived(getSettings());

	// Simple transition functions that respect animation settings
	const tabOut = (node: Element) => {
		const animationsEnabled = settings.animationsEnabled !== false;
		return fade(node, {
			duration: animationsEnabled ? 250 : 0,
		});
	};

	const tabIn = (node: Element) => {
		const animationsEnabled = settings.animationsEnabled !== false;
		return fade(node, {
			duration: animationsEnabled ? 300 : 0,
			delay: animationsEnabled ? 250 : 0, // Wait for out transition
		});
	};

	let isTransitioning = $derived(getIsTransitioning());

	// Tab configuration
	const tabs = [
		{ id: 'construct', label: 'Construct', icon: '🔧' },
		{ id: 'browse', label: 'Browse', icon: '🔍' },
		{ id: 'sequence_card', label: 'Sequence Card', icon: '🎴' },
		{ id: 'write', label: 'Write', icon: '✍️' },
		{ id: 'learn', label: 'Learn', icon: '🧠' },
	] as const;

	function handleTabSelect(tabId: string) {
		switchTab(tabId);
	}
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

		<NavigationBar {tabs} {activeTab} onTabSelect={handleTabSelect} />

		<main class="content-area">
			<!-- Tab content with reliable transitions -->
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

			<!-- Transition indicator for better UX -->
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
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
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

	/* Responsive design */
	@media (max-width: 768px) {
		.main-interface {
			height: 100vh;
			height: 100dvh; /* Dynamic viewport height for mobile */
		}
	}

	/* Disable animations when user prefers reduced motion */
	@media (prefers-reduced-motion: reduce) {
		* {
			transition: none !important;
			animation: none !important;
		}
	}
</style>
