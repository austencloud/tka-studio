<script lang="ts">
	import { onMount } from 'svelte';
	import NavButton from './NavButton.svelte';
	import { scale } from 'svelte/transition';
	import { elasticOut } from 'svelte/easing';
	import { useSelector } from '@xstate/svelte';
	import { appService } from '$lib/state/machines/app/app.machine';
	import { uiStore } from '$lib/state/stores/uiStore';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import { browser } from '$app/environment';

	// Props using Svelte 5 runes
	const { onChangeBackground = () => {}, onSettingsClick = () => {} } = $props<{
		onChangeBackground?: (background: string) => void;
		onSettingsClick?: () => void;
	}>();

	// Get state from the app state machine
	const currentTabStore = useSelector(appService, (state) => state.context.currentTab);
	const previousTabStore = useSelector(appService, (state) => state.context.previousTab);

	// Use $derived instead of $: reactive declarations
	const activeTab = $derived($currentTabStore as number);
	const previousTab = $derived($previousTabStore as number);

	// Get device information from the UI store
	const isMobileDevice = $derived($uiStore.isMobile);
	const isPortraitMode = $derived(
		!$uiStore.isDesktop && $uiStore.windowHeight > $uiStore.windowWidth
	);

	// State with runes
	let lastClickTime = $state(0);

	const tabNames = ['Construct', 'Generate', 'Browse', 'Learn', 'Write'];
	// Replace emojis with Font Awesome icons for a more professional look
	const tabIcons = [
		'fa-solid fa-hammer',
		'fa-solid fa-robot',
		'fa-solid fa-magnifying-glass',
		'fa-solid fa-brain',
		'fa-solid fa-pen-nib'
	];

	// Determine if text should be shown based on device/orientation
	const showButtonText = $derived(!isMobileDevice && !isPortraitMode);

	function handleTabClick(index: number) {
		if (index === activeTab) return;

		const now = Date.now();
		if (now - lastClickTime < 50) return; // Debounce rapid clicks
		lastClickTime = now;

		// Provide haptic feedback for tab navigation
		if (browser && hapticFeedbackService.isAvailable()) {
			hapticFeedbackService.trigger('navigation');
		}

		// Update the app state machine
		appService.send({ type: 'CHANGE_TAB', tab: index });
	}

	// Update device/orientation state if UI store is not available
	const updateModes = () => {
		if (typeof window !== 'undefined') {
			uiStore.updateWindowDimensions(window.innerWidth, window.innerHeight);
		}
	};

	onMount(() => {
		updateModes();
	});
</script>

<div class="nav-widget">
	{#each tabNames as name, index}
		<div class="button-wrapper" class:active={index === activeTab}>
			{#key `tab-${index}-${activeTab === index}-${showButtonText}`}
				<NavButton
					isActive={index === activeTab}
					onClick={() => handleTabClick(index)}
					{index}
					previousIndex={previousTab}
					showText={showButtonText}
				>
					{#if showButtonText}
						<div
							class="button-content landscape"
							in:scale={{ duration: 400, delay: 50, easing: elasticOut }}
						>
							<span class="text">{name}</span>
							<i class="{tabIcons[index]} icon"></i>
						</div>
					{:else}
						<div
							class="button-content portrait"
							in:scale={{ duration: 400, delay: 50, easing: elasticOut }}
						>
							<i class="{tabIcons[index]} icon-only"></i>
						</div>
					{/if}
				</NavButton>
			{/key}

			{#if index === activeTab}
				<div
					class="active-tab-indicator"
					class:round={!showButtonText}
					in:scale={{ duration: 300, delay: 200, start: 0.5 }}
				></div>
			{/if}
		</div>
	{/each}
</div>

<style>
	.nav-widget {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 1rem; /* Increased gap for better spacing */
		position: relative;
		overflow: visible;
		padding: 6px 0;
		width: 100%; /* Take up available space */
		margin: 0 auto; /* Center horizontally */
		max-width: 600px; /* Limit width to ensure proper centering */
	}

	.button-wrapper {
		position: relative;
		display: flex;
		flex-direction: column;
		align-items: center;
		background: transparent;
		padding-bottom: 8px; /* Space for indicator */
	}

	/* Content alignment within the button slot */
	.button-content {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100%;
	}

	.button-content.landscape {
		gap: 0.5rem;
	}

	.text {
		font-weight: 500;
		letter-spacing: 0.02em;
	}

	.icon {
		font-size: 0.9em;
		color: rgba(255, 255, 255, 0.9);
	}

	.icon-only {
		font-size: 1.2em;
		line-height: 1;
	}

	/* Tab indicator */
	.active-tab-indicator {
		position: absolute;
		bottom: -2px;
		left: 50%;
		transform: translateX(-50%);
		width: 70%;
		max-width: 40px;
		height: 3px;
		background: linear-gradient(to right, #6c9ce9, #1e3c72);
		border-radius: 10px;
		box-shadow: 0 0 8px rgba(108, 156, 233, 0.7);
		transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
	}

	.active-tab-indicator.round {
		width: 40%;
		max-width: 20px;
		height: 4px;
		bottom: 0px;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.nav-widget {
			gap: 0.5rem;
		}

		.menu-button {
			margin-left: 5px;
		}

		.settings-button-container {
			margin-right: 5px;
		}
	}
</style>
