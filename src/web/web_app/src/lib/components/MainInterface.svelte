<script lang="ts">
	// Import app mode state management
	import { getAppMode, isLandingMode, isAppMode, getLandingBackground } from '$lib/state/appModeState.svelte';
	
	// Import app state management functions
	import {
		getActiveTab,
		getSettings,
		getShowSettings,
		isTabActive,
		switchTab,
	} from '$lib/state/appState.svelte';
	
	// Import transition utilities
	import { foldTransition } from '$lib/utils/foldTransition';
	import { fade } from '$lib/utils/simpleFade';
	
	// Import Svelte routing
	import { page } from '$app/stores';
	
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
	
	// Import components - Landing Interface
	import Home from './landing/Home.svelte';
	import About from './landing/About.svelte';
	import Contact from './landing/Contact.svelte';
	import Links from './landing/Links.svelte';

	// Reactive state for template using proper derived
	let appMode = $derived(getAppMode());
	let activeTab = $derived(getActiveTab());
	let showSettings = $derived(getShowSettings());
	let settings = $derived(getSettings());
	let landingBackground = $derived(getLandingBackground());

	// Current route information
	let currentRoute = $derived($page.route.id);

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
	] as const;

	function handleTabSelect(tabId: string) {
		switchTab(tabId as 'construct' | 'browse' | 'sequence_card' | 'write' | 'learn');
	}

	function handleBackgroundChange(background: string) {
		console.log('🌌 Background changed to:', background);
	}

	// Determine which landing component to show based on route
	function getLandingComponent() {
		switch (currentRoute) {
			case '/about':
				return About;
			case '/contact':
				return Contact;
			case '/links':
				return Links;
			case '/':
			default:
				return Home;
		}
	}
</script>

<BackgroundProvider>
	<div class="main-interface" data-mode={appMode}>
		<!-- Background Canvas - adapts to mode -->
		{#if isLandingMode()}
			<!-- Landing backgrounds -->
			{#if landingBackground === 'nightSky'}
				<BackgroundCanvas backgroundType="nightSky" quality="high" />
			{:else if landingBackground === 'deepOcean'}
				<BackgroundCanvas backgroundType="deepOcean" quality="high" />
			{:else if landingBackground === 'snowfall'}
				<BackgroundCanvas backgroundType="snowfall" quality="high" />
			{/if}
		{:else if isAppMode() && settings.backgroundEnabled}
			<!-- App backgrounds -->
			<BackgroundCanvas
				backgroundType={settings.backgroundType === 'auroraBorealis' ||
				settings.backgroundType === 'starfield'
					? 'aurora'
					: settings.backgroundType || 'aurora'}
				quality={settings.backgroundQuality || 'medium'}
				onReady={() =>
					console.log(
						`🌌 App background ready: ${settings.backgroundType} at ${settings.backgroundQuality} quality`
					)}
			/>
		{/if}

		<!-- Navigation - unified for both modes -->
		<NavigationBar 
			tabs={isAppMode() ? appTabs : []} 
			activeTab={isAppMode() ? activeTab : ''} 
			onTabSelect={handleTabSelect}
			onBackgroundChange={handleBackgroundChange}
		/>

		<!-- Main Content Area -->
		<main class="content-area">
			{#if isLandingMode()}
				<!-- Landing Page Content with Routing -->
				<div class="landing-content" in:foldTransition={{ direction: 'fold-in', duration: 400 }}>
					{#key currentRoute}
						<div class="landing-page" in:fade={{ duration: 300, delay: 100 }} out:fade={{ duration: 200 }}>
							<svelte:component this={getLandingComponent()} />
						</div>
					{/key}
				</div>
			{:else if isAppMode()}
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
						{/if}
					</div>
				{/key}
			{/if}
		</main>
	</div>
</BackgroundProvider>

<!-- Settings Dialog - only in app mode -->
{#if isAppMode() && showSettings}
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
	}

	.main-interface[data-mode="landing"] {
		/* Landing mode specific styling */
		background: transparent;
	}

	.main-interface[data-mode="app"] {
		/* App mode specific styling */
		background: transparent;
	}

	.content-area {
		flex: 1;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		position: relative;
	}

	.landing-content {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		overflow-y: auto;
		overflow-x: hidden;
		width: 100%;
		height: 100%;
		/* Landing specific scrolling */
		scroll-behavior: smooth;
	}

	.landing-page {
		position: relative;
		width: 100%;
		min-height: 100%;
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

	/* Landing mode specific styles */
	.main-interface[data-mode="landing"] .content-area {
		/* Allow scrolling in landing mode */
		overflow: visible;
	}

	.main-interface[data-mode="landing"] .landing-content {
		position: relative;
		overflow: visible;
		height: auto;
		min-height: 100%;
	}

	/* App mode specific styles */
	.main-interface[data-mode="app"] .content-area {
		/* Fixed height in app mode */
		overflow: hidden;
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.main-interface {
			height: 100vh;
			height: 100dvh; /* Dynamic viewport height for mobile */
		}

		.landing-content {
			/* Better mobile scrolling */
			-webkit-overflow-scrolling: touch;
		}
	}

	/* Disable animations when user prefers reduced motion */
	@media (prefers-reduced-motion: reduce) {
		.main-interface,
		.landing-content,
		.landing-page,
		.tab-content {
			transition: none !important;
			animation: none !important;
		}
	}

	/* High contrast mode */
	@media (prefers-contrast: high) {
		.main-interface[data-mode="landing"] {
			border: 2px solid white;
		}

		.main-interface[data-mode="app"] {
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

		.landing-content,
		.tab-content {
			position: relative;
			overflow: visible;
			height: auto;
		}
	}
</style>
