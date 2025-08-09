<script lang="ts">
	// Import runes-based state
	import {
		getActiveTab,
		isTabActive,
		switchTab,
		getShowSettings,
		getIsMainTabTransitioning,
		getMainTabTransitionState,
	} from '$stores/appState.svelte';

	// Import fade transitions
	import { enhancedFade, fluidTransition, getTabTransitionKey } from '$services/ui/animation';

	// Reactive state for template
	let activeTab = $derived(getActiveTab());
	let showSettings = $derived(getShowSettings());
	let settings = $derived(getSettings());
	let isTransitioning = $derived(getIsMainTabTransitioning());
	let transitionState = $derived(getMainTabTransitionState());

	// Simple background integration - let BackgroundCanvas handle the settings directly

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
	import { getSettings } from '$stores/appState.svelte';

	// Create transition functions for tabs
	function createTabTransition(tabId: string) {
		return fluidTransition(node, {
			duration: 350,
			effects: ['fade', 'slide'],
			slideDirection: 'right',
			distance: 30,
			opacity: { start: 0, end: 1 },
		});
	}

	// Tab-specific transition configurations - simplified to fix compilation issues
	const tabInTransition = (node: Element) => ({
		duration: 350,
		css: (t: number) => `opacity: ${t}`,
	});

	const tabOutTransition = (node: Element) => ({
		duration: 250,
		css: (t: number) => `opacity: ${1 - t}`,
	});

	// Tab configuration - UPDATED to include Sequence Card tab matching desktop app exactly
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
		<!-- Background Canvas - positioned behind everything -->
		{#if settings.backgroundEnabled}
			<BackgroundCanvas
				backgroundType={settings.backgroundType || 'aurora'}
				quality={settings.backgroundQuality || 'medium'}
				onReady={() =>
					console.log(
						`🌌 Main app background ready: ${settings.backgroundType} at ${settings.backgroundQuality} quality`
					)}
			/>
		{:else}
			<!-- Debug: Show when background is disabled -->
			<div
				style="position: absolute; top: 10px; right: 10px; background: rgba(255,0,0,0.5); color: white; padding: 4px; font-size: 12px; z-index: 1000;"
			>
				Background Disabled
			</div>
		{/if}

		<NavigationBar {tabs} {activeTab} onTabSelect={switchTab} />

		<main class="content-area">
			<!-- Main tab content with fade transitions -->
			{#if isTabActive('construct')}
				<div class="tab-content" data-tab="construct" in:tabInTransition out:tabOutTransition>
					<ConstructTab />
				</div>
			{:else if isTabActive('browse')}
				<div class="tab-content" data-tab="browse" in:tabInTransition out:tabOutTransition>
					<BrowseTab />
				</div>
			{:else if isTabActive('sequence_card')}
				<div class="tab-content" data-tab="sequence_card" in:tabInTransition out:tabOutTransition>
					<SequenceCardTab />
				</div>
			{:else if isTabActive('write')}
				<div class="tab-content" data-tab="write" in:tabInTransition out:tabOutTransition>
					<WriteTab />
				</div>
			{:else if isTabActive('learn')}
				<div class="tab-content" data-tab="learn" in:tabInTransition out:tabOutTransition>
					<LearnTab />
				</div>
			{/if}

			<!-- Debug transition state (remove in production) -->
			{#if isTransitioning}
				<div class="transition-debug">
					🎭 Transitioning: {transitionState.fromTab} → {transitionState.toTab}
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
		z-index: 1;
	}

	.content-area {
		flex: 1;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		position: relative;
	}

	/* Tab content styling for transitions */
	.tab-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		position: relative;
		height: 100%;
		width: 100%;
	}

	/* Debug transition indicator */
	.transition-debug {
		position: absolute;
		top: 10px;
		left: 50%;
		transform: translateX(-50%);
		background: rgba(255, 215, 0, 0.9);
		color: #000;
		padding: 8px 16px;
		border-radius: 20px;
		font-size: 14px;
		font-weight: 600;
		z-index: 9999;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
		pointer-events: none;
	}

	/* Tab content styling */

	/* Responsive design */
	@media (max-width: 768px) {
		.main-interface {
			height: 100vh;
			height: 100dvh; /* Dynamic viewport height for mobile */
		}

		/* Mobile responsive adjustments */
	}
</style>
