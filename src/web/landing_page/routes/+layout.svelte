<script lang="ts">
	import { page } from '$app/stores';

	// Import global styles
	import '$lib/styles/global.css';
	import '$lib/styles/variables.css';
	import '$lib/styles/themes.css';

	// Import runes-based components
	import NavBar from '$lib/components/landing/NavBar.svelte';

	// Pure runes state management
	let currentTheme = $state('dark');
	let currentBackground = $state('deepOcean');
	let isLoading = $state(false);

	// Computed values using $derived
	let isAppMode = $derived($page.url.pathname.startsWith('/app'));
	let isAnimatorMode = $derived($page.url.pathname.startsWith('/animator'));
	let isLandingMode = $derived(!isAppMode && !isAnimatorMode);
	let currentPage = $derived((() => {
		const path = $page.url.pathname;
		if (path === '/') return 'home';
		if (path.startsWith('/app')) return 'app';
		if (path.startsWith('/animator')) return 'animator';
		if (path.startsWith('/about')) return 'about';
		return 'home';
	})());

	// Initialize theme and background using $effect
	$effect(() => {
		// Initialize theme from localStorage
		const savedTheme = localStorage.getItem('tka-theme') || 'dark';
		currentTheme = savedTheme;
		document.documentElement.setAttribute('data-theme', savedTheme);
	});

	$effect(() => {
		// Initialize background from localStorage
		const savedBackground = localStorage.getItem('tka-background') || 'deepOcean';
		currentBackground = savedBackground;
		document.documentElement.style.setProperty('--current-background', savedBackground);
	});
</script>

<svelte:head>
	<title>{
		isAppMode ? 'Constructor - TKA' :
		isAnimatorMode ? 'Animator - TKA' :
		'The Kinetic Alphabet'
	}</title>
</svelte:head>

<div class="app-container" data-theme={currentTheme}>
	<!-- Navigation - only show on non-app pages or app landing -->
	{#if isLandingMode || $page.url.pathname === '/app'}
		<NavBar {currentPage} />
	{/if}

	<!-- Main Content -->
	<main class="main-content" class:app-mode={isAppMode} class:full-screen={isAppMode && $page.url.pathname !== '/app'}>
		{#if isLoading}
			<div class="loading-overlay">
				<div class="loading-spinner"></div>
				<p>Loading...</p>
			</div>
		{:else}
			<slot />
		{/if}
	</main>
</div>

<style>
	.app-container {
		min-height: 100vh;
		position: relative;
		font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
		background: var(--background-color);
		color: var(--text-color);
		transition: background-color var(--transition-normal), color var(--transition-normal);
	}

	.main-content {
		position: relative;
		z-index: 1;
		min-height: 100vh;
		transition: all 0.3s ease;
	}

	.main-content.app-mode {
		padding-top: 0;
	}

	.main-content.full-screen {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		z-index: 10;
	}

	/* Landing mode has normal padding for nav */
	.main-content:not(.app-mode) {
		padding-top: 80px; /* Account for fixed navigation */
	}

	.loading-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.7);
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		z-index: 1000;
		backdrop-filter: blur(4px);
	}

	.loading-spinner {
		width: 40px;
		height: 40px;
		border: 4px solid rgba(255, 255, 255, 0.3);
		border-top: 4px solid var(--primary-color);
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin-bottom: var(--spacing-md);
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}

	@media (max-width: 768px) {
		.main-content:not(.app-mode) {
			padding-top: 120px; /* Account for mobile nav height */
		}
	}
</style>
