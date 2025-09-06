<script lang="ts">
	import TabContent from '../tabs/TabContent.svelte';
	import { onMount } from 'svelte';
	import SettingsContent from '$lib/components/SettingsDialog/SettingsDialog.svelte';
	import { appActions } from '$lib/state/machines/app/app.actions';
	import { useSelector } from '@xstate/svelte';
	import { appService } from '$lib/state/machines/app/app.machine';
	import { fade, fly } from 'svelte/transition';
	import { cubicOut, quintOut } from 'svelte/easing';
	import { uiStore } from '$lib/state/stores/uiStore';

	const isSettingsOpenStore = useSelector(appService, (state) => state.context.isSettingsOpen);
	$: isSettingsDialogOpen = $isSettingsOpenStore;

	let buttonSize = 50;
	let iconSize = 38;

	$: if ($uiStore && $uiStore.windowWidth) {
		buttonSize = Math.max(30, Math.min(50, $uiStore.windowWidth / 12));
		iconSize = buttonSize * 0.75;
	}

	onMount(() => {
		if (typeof window !== 'undefined') {
			buttonSize = Math.max(30, Math.min(50, window.innerWidth / 12));
			iconSize = buttonSize * 0.75;

			// Ensure settings dialog is closed on page load
			if (isSettingsDialogOpen) {
				console.log('Closing settings dialog on page load');
				appActions.closeSettings();
			}

			// Also check localStorage directly to ensure settings dialog state is reset
			try {
				const storageKey = 'xstate-app';
				const storedData = localStorage.getItem(storageKey);

				if (storedData) {
					const parsedData = JSON.parse(storedData);

					// If the stored data includes isSettingsOpen, ensure it's set to false
					if (parsedData && parsedData.context && parsedData.context.isSettingsOpen === true) {
						console.log('Resetting persisted settings dialog state on page load');
						parsedData.context.isSettingsOpen = false;
						localStorage.setItem(storageKey, JSON.stringify(parsedData));
					}
				}
			} catch (error) {
				console.error('Error resetting settings dialog state:', error);
			}
		}
		appActions.changeTab(0);
	});

	function handleToggleSettings() {
		if (isSettingsDialogOpen) {
			appActions.closeSettings();
		} else {
			appActions.openSettings();
		}
	}

	function handleBackdropKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape' || event.key === 'Enter' || event.key === ' ') {
			appActions.closeSettings();
		}
	}
</script>

<div class="content">
	<div class="mainContent">
		<TabContent />
	</div>

	{#if isSettingsDialogOpen}
		<div
			class="settingsBackdrop"
			transition:fade={{ duration: 300, easing: cubicOut }}
			on:click={() => appActions.closeSettings()}
			on:keydown={handleBackdropKeydown}
			role="button"
			tabindex="0"
			aria-label="Close settings"
		></div>
		<div
			class="settingsContent"
			in:fly={{ y: 20, duration: 400, delay: 100, easing: quintOut }}
			out:fade={{ duration: 200, easing: cubicOut }}
		>
			<SettingsContent onClose={() => appActions.closeSettings()} />
		</div>
	{/if}
</div>

<style>
	.content {
		display: flex;
		flex-direction: column;
		flex: 1;
		min-height: 0;
		z-index: 1;
		width: 100%;
		position: relative;
	}

	.mainContent {
		display: flex;
		flex: 1;
		overflow: hidden;
		position: relative;
		z-index: 0;
		width: 100%;
		opacity: 1;
	}
	.settingsBackdrop {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: rgba(0, 0, 0, 0.5);
		backdrop-filter: blur(4px);
		z-index: 9;
		cursor: pointer;
	}

	.settingsContent {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: 90%;
		max-width: 800px;
		max-height: 90vh;
		border-radius: 12px;
		box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
		z-index: 10;
		overflow: hidden;
	}
</style>
