import { browser } from '$app/environment';
import { registerSW } from 'virtual:pwa-register';

// This conditional is important for SSR
if (browser) {
	// Register service worker using vite-plugin-pwa
	const updateSW = registerSW({
		onNeedRefresh() {
			// Show a prompt to the user asking if they want to refresh
			console.log('New content available, click on reload button to update.');
		},
		onOfflineReady() {
			// Notify the user that the app is ready for offline use
			console.log('App ready to work offline');
		}
	});

	// Add event listeners for installation/updates
	window.addEventListener('beforeinstallprompt', (event) => {
		// Prevent the mini-infobar from appearing on mobile
		event.preventDefault();
		// Store the event for later use
		// You could add a UI element here to show "Install this app" button
		console.log('App can be installed, saved event');
		window.deferredPrompt = event;
	});

	// When the app is successfully installed
	window.addEventListener('appinstalled', () => {
		console.log('Application was successfully installed');
		window.deferredPrompt = null;
	});
}
