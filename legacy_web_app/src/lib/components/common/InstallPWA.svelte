<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { browser } from '$app/environment';

	export let buttonText = 'Install App';
	export let showInstallPrompt = false;

	const canInstall = writable(false);

	// Standard event handlers from pwa.ts
	onMount(() => {
		if (!browser) return;

		// Check if the app can be installed
		window.addEventListener('beforeinstallprompt', (e) => {
			e.preventDefault();
			window.deferredPrompt = e;
			canInstall.set(true);
		});

		// Update state when app is installed
		window.addEventListener('appinstalled', () => {
			window.deferredPrompt = null;
			canInstall.set(false);
		});
	});

	// Handle install button click
	function promptInstall() {
		if (!browser || !window.deferredPrompt) return;

		const promptEvent = window.deferredPrompt;
		promptEvent.prompt();

		promptEvent.userChoice.then((choice: { outcome: 'accepted' | 'dismissed' }) => {
			if (choice.outcome === 'accepted') {
				console.log('User accepted the install prompt');
			} else {
				console.log('User dismissed the install prompt');
			}
			window.deferredPrompt = null;
			canInstall.set(false);
		});
	}
</script>

{#if showInstallPrompt && $canInstall}
	<button class="install-button" on:click={promptInstall} aria-label="Install application">
		<span class="install-icon">📱</span>
		<span class="install-text">{buttonText}</span>
	</button>
{/if}

<style>
	.install-button {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 8px;
		padding: 8px 16px;
		background-color: #1e3c72;
		color: white;
		border: none;
		border-radius: 8px;
		cursor: pointer;
		font-weight: 500;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
		transition:
			background-color 0.2s,
			transform 0.1s;
	}

	.install-button:hover {
		background-color: #2a52be;
		transform: translateY(-1px);
	}

	.install-button:active {
		transform: translateY(1px);
	}

	.install-icon {
		font-size: 1.2em;
	}
</style>
