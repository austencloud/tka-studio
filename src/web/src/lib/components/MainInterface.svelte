<script lang="ts">
	// Import app state management functions
	import {
		getActiveTab,
		getSettings,
		getShowSettings,
		isTabActive,
		switchTab,
	} from '$lib/state/appState.svelte';
	
	// Import transition utilities
	import { fade } from '$lib/utils/simpleFade';
	
	// Import components - App Interface
	import BackgroundCanvas from './backgrounds/BackgroundCanvas.svelte';
	import BackgroundProvider from './backgrounds/BackgroundProvider.svelte';
	import NavigationBar from './navigation/NavigationBar.svelte';
	import SettingsDialog from './SettingsDialog.svelte';
	import BrowseTab from './tabs/BrowseTab.svelte';
	import ConstructTab from './tabs/ConstructTab.svelte';
	import LearnTab from './tabs/LearnTab.svelte';
	import SequenceCardTab from './tabs/SequenceCardTab.svelte';
	import WriteTab from './tabs/WriteTab.svelte';
	import AboutTab from './tabs/AboutTab.svelte';
	import MotionTesterTab from './tabs/MotionTesterTab.svelte';
	import ArrowDebugTab from './tabs/ArrowDebugTab.svelte';

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

	// App tab configuration
	const appTabs = [
		{ id: 'construct', label: 'Construct', icon: '🔧' },
		{ id: 'browse', label: 'Browse', icon: '🔍' },
		{ id: 'sequence_card', label: 'Sequence Card', icon: '🎴' },
		{ id: 'write', label: 'Write', icon: '✍️' },
		{ id: 'learn', label: 'Learn', icon: '🧠' },
		{ id: 'motion-tester', label: 'Motion Tester', icon: '🎯' },
		{ id: 'arrow-debug', label: 'Arrow Debug', icon: '🏹' },
		{ id: 'about', label: 'About', icon: 'ℹ️' },
	] as const;

	function handleTabSelect(tabId: string) {
		switchTab(tabId as 'construct' | 'browse' | 'sequence_card' | 'write' | 'learn' | 'about' | 'motion-tester' | 'arrow-debug');
	}

	function handleBackgroundChange(background: string) {
		// Background change handled
	}
</script>

<BackgroundProvider>
<div class="main-interface">
<!-- Background Canvas -->
{#if settings.backgroundEnabled}
<BackgroundCanvas
 backgroundType={settings.backgroundType === 'auroraBorealis' ||
settings.backgroundType === 'starfield'
  ? 'aurora'
 : settings.backgroundType || 'aurora'}
 quality={settings.backgroundQuality || 'medium'}
/>
{/if}

<!-- Navigation Bar -->
<NavigationBar 
tabs={appTabs} 
activeTab={activeTab} 
onTabSelect={handleTabSelect}
onBackgroundChange={handleBackgroundChange}
/>

<!-- Main Content Area -->
		<main class="content-area">
 <!-- App Content with reliable transitions -->
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
{:else if isTabActive('motion-tester')}
	<MotionTesterTab />
{:else if isTabActive('arrow-debug')}
	<ArrowDebugTab />
{:else if isTabActive('about')}
<AboutTab />
{/if}
</div>
{/key}
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
		transition: all 0.3s ease;
		background: transparent;
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

	/* Responsive design */
	@media (max-width: 768px) {
		.main-interface {
			height: 100vh;
			height: 100dvh; /* Dynamic viewport height for mobile */
		}
	}

	/* Disable animations when user prefers reduced motion */
	@media (prefers-reduced-motion: reduce) {
		.main-interface,
		.tab-content {
			transition: none !important;
			animation: none !important;
		}
	}

	/* High contrast mode */
	@media (prefers-contrast: high) {
		.main-interface {
			border: 2px solid #667eea;
		}
	}

	/* Print styles */
	@media print {
		.main-interface {
			height: auto;
			overflow: visible;
		}

		.content-area {
			overflow: visible;
			height: auto;
		}

		.tab-content {
			position: relative;
			overflow: visible;
			height: auto;
		}
	}
</style>
