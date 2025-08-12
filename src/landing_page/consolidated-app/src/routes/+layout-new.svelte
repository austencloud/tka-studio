<script lang="ts">
	import { browser } from '$app/environment';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';

	// Import global styles
	import '$lib/styles/global.css';
	import '$lib/styles/variables.css';
	import '$lib/styles/themes.css';

	// Import unified components
	import Navigation from '$lib/components/navigation/Navigation.svelte';
	import BackgroundProvider from '$lib/components/backgrounds/BackgroundProvider.svelte';
	import ToastManager from '$lib/components/shared/ToastManager.svelte';
	import LoadingOverlay from '$lib/components/shared/LoadingOverlay.svelte';

	// Pure Svelte 5 runes - no stores
	let currentTheme = $state('dark');
	let currentBackground = $state<'deepOcean' | 'snowfall' | 'nightSky'>('deepOcean');
	let isLoading = $state(false);
	let isInitialized = $state(false);

	// Reactive navigation state using $derived
	let isAppMode = $derived(browser && $page.url.pathname.startsWith('/app'));
	let isAnimatorMode = $derived(browser && $page.url.pathname.startsWith('/animator'));
	let isConstructorMode = $derived(browser && $page.url.pathname.startsWith('/constructor'));
	let isLandingMode = $derived(browser && !isAppMode && !isAnimatorMode && !isConstructorMode);

	// Initialize app using $effect instead of onMount
	$effect(() => {
		if (browser && !isInitialized) {
			// Apply theme
			document.documentElement.setAttribute('data-theme', currentTheme);

			// Apply background class
			document.body.className = `background-${currentBackground}`;

			isInitialized = true;
		}
	});

	// Theme synchronization effect
	$effect(() => {
		if (browser && isInitialized) {
			document.documentElement.setAttribute('data-theme', currentTheme);
		}
	});

	// Background synchronization effect
	$effect(() => {
		if (browser && isInitialized) {
			document.body.className = `background-${currentBackground}`;
		}
	});

	// Navigation handler using regular functions instead of event dispatchers
	function handleNavigation(path: string) {
		goto(path);
	}

	// Theme change handler
	function handleThemeChange(theme: string) {
		currentTheme = theme;
	}

	// Background change handler
	function handleBackgroundChange(background: string) {
		if (background === 'deepOcean' || background === 'snowfall' || background === 'nightSky') {
			currentBackground = background;
		}
	}
</script>

<svelte:head>
	<title>The Kinetic Alphabet - Flow Arts Choreography Toolbox</title>
	<meta name="description" content="The Kinetic Alphabet is a revolutionary flow arts choreography toolbox for poi, staff, fans, and other flow arts. Learn, create, and share movement sequences." />
</svelte:head>

<!-- Background System -->
<BackgroundProvider backgroundType={currentBackground}>

	<!-- Navigation -->
	<Navigation
		{currentTheme}
		{currentBackground}
		{isAppMode}
		{isAnimatorMode}
		{isConstructorMode}
		{isLandingMode}
		onNavigate={handleNavigation}
		onThemeChange={handleThemeChange}
		onBackgroundChange={handleBackgroundChange}
	/>

	<!-- Main Content Area -->
	<main class="main-content" class:app-mode={isAppMode} class:landing-mode={isLandingMode}>
		<slot />
	</main>

	<!-- Toast Manager for notifications -->
	<ToastManager />

	<!-- Loading Overlay -->
	{#if isLoading}
		<LoadingOverlay />
	{/if}

</BackgroundProvider>

<style>
	:global(html) {
		height: 100%;
		scroll-behavior: smooth;
	}

	:global(body) {
		height: 100%;
		margin: 0;
		font-family: var(--font-family-sans);
		line-height: 1.6;
		color: var(--text-color);
		background: var(--background-color);
		transition: background-color var(--transition-normal);
	}

	.main-content {
		min-height: calc(100vh - var(--nav-height));
		position: relative;
		z-index: 1;
		transition: padding var(--transition-normal);
	}

	.main-content.landing-mode {
		padding: 0;
	}

	.main-content.app-mode {
		padding: var(--spacing-lg);
		max-width: var(--max-width-app);
		margin: 0 auto;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.main-content.app-mode {
			padding: var(--spacing-md);
		}
	}
</style>
