<script lang="ts">
	import NavWidget from './NavWidget/NavWidget.svelte';
	import SettingsButton from './SettingsButton/SettingsButton.svelte';
	import InstallPWA from '../common/InstallPWA.svelte';
	import { fade, fly } from 'svelte/transition';
	import { cubicInOut, quintOut } from 'svelte/easing';
	import { appActions } from '$lib/state/machines/app/app.actions';
	import { uiStore } from '$lib/state/stores/uiStore';

	// Props using Svelte 5 runes
	const { onChangeBackground = () => {}, onOpenSettings = () => {} } = $props<{
		onChangeBackground?: (background: string) => void;
		onOpenSettings?: () => void;
	}>();

	// Use state rune for nav visibility
	let isNavVisible = $state(true);

	// Use state for menu height with animation handled in CSS
	let menuHeight = $state(60);

	// Get device information from the UI store
	const isMobileDevice = $derived($uiStore.isMobile);
	const isPortraitMode = $derived(
		!$uiStore.isDesktop && $uiStore.windowHeight > $uiStore.windowWidth
	);

	function handleSettingsClick() {
		appActions.openSettings();
		onOpenSettings();
	}

	function handleBackgroundChange(background: string) {
		onChangeBackground(background);
	}

	function toggleNav() {
		// Update the menu height based on visibility
		menuHeight = isNavVisible ? 0 : isMobileDevice ? 50 : 60;
		isNavVisible = !isNavVisible;
	}
</script>

<div class="menu-wrapper" style="--menu-height: {menuHeight}px;">
	<!-- Fixed Navigation Controls - Always visible -->
	<div class="fixed-nav-controls">
		<!-- Hamburger button on the left -->
		<button class="hamburger-button" onclick={toggleNav} aria-label="Menu">
			<i class="fa-solid fa-bars"></i>
		</button>
	</div>

	<header class="menu-bar-container">
		<!-- Menu Bar Content -->
		{#if isNavVisible}
			<div class="menu-bar-backdrop" transition:fade={{ duration: 400, easing: cubicInOut }}></div>
			<div
				class="menu-bar"
				in:fly={{ y: -20, duration: 500, delay: 100, easing: quintOut }}
				out:fade={{ duration: 200 }}
			>
				<!-- Left spacer section to balance the right section -->
				<div class="menu-section left-section">
					<!-- Empty spacer with same width as right section -->
					<div class="left-spacer"></div>
				</div>

				<!-- Center section with navigation -->
				<div class="menu-section center-section">
					<div class="nav-widget-wrapper">
						<NavWidget
							onChangeBackground={handleBackgroundChange}
							onSettingsClick={handleSettingsClick}
						/>
					</div>
				</div>

				<!-- Right section with install button and settings button -->
				<div class="menu-section right-section">
					<div class="menu-buttons-container">
						<div class="settings-button-container">
							<SettingsButton onClick={handleSettingsClick} />
						</div>
						<div class="pwa-install-container" in:fade={{ duration: 400, delay: 300 }}>
							<InstallPWA
								showInstallPrompt={true}
								buttonText={isMobileDevice || isPortraitMode ? '' : 'Install App'}
							/>
						</div>
					</div>
				</div>
			</div>
		{/if}
	</header>
</div>

<style>
	.menu-wrapper {
		position: relative;
		width: 100%;
		height: var(--menu-height);
		transition: height 0.4s cubic-bezier(0.16, 1, 0.3, 1);
		overflow: hidden;
	}

	.menu-bar-container {
		position: relative;
		width: 100%;
	}

	.menu-bar-backdrop {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		height: 60px;
		background-color: rgba(0, 0, 0, 0.4);
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		border-bottom: 1px solid rgba(255, 255, 255, 0.12);
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
		z-index: 1;
	}

	.menu-bar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 8px 0; /* Removed horizontal padding */
		position: relative;
		height: 60px;
		z-index: 1;
		width: 100%; /* Ensure full width */
	}

	/* Fixed Navigation Controls */
	.fixed-nav-controls {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 10px;
		z-index: 10; /* Reduced z-index to not block navigation buttons */
		width: 100%;
		pointer-events: none; /* Make the container transparent to clicks */
	}

	/* But make the buttons themselves clickable */
	.hamburger-button {
		pointer-events: auto;
	}

	.hamburger-button {
		background: rgba(0, 0, 0, 0.3);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 12px;
		color: rgba(255, 255, 255, 0.9);
		width: 40px;
		height: 40px;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition: all 0.3s ease;
	}

	.hamburger-button:hover {
		background: rgba(30, 60, 114, 0.4);
		border-color: rgba(108, 156, 233, 0.3);
		color: #6c9ce9;
		transform: translateY(-2px);
	}

	.menu-section {
		display: flex;
		align-items: center;
	}

	.left-section {
		flex: 1;
		justify-content: flex-start;
	}

	.center-section {
		flex: 2;
		justify-content: center;
	}

	.right-section {
		flex: 1;
		justify-content: flex-end;
	}

	.left-spacer {
		width: 100%;
		height: 100%;
	}

	.nav-widget-wrapper {
		position: relative;
		display: flex;
		justify-content: center;
		width: 100%;
		max-width: 100vw; /* Ensure it doesn't exceed viewport width */
	}

	.pwa-install-container {
		margin-left: auto;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.menu-bar-backdrop {
			height: 50px;
		}

		.menu-bar {
			padding: 6px 0; /* Removed horizontal padding */
			height: 50px;
		}

		.fixed-nav-controls {
			padding: 6px;
		}

		.hamburger-button {
			width: 36px;
			height: 36px;
			height: 36px;
		}
	}
</style>
