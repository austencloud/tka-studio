<script lang="ts">
	import { createEventDispatcher, onMount } from 'svelte';

	let isFull = false;
	let fsContainer: HTMLDivElement | null = null;
	let fullscreenSupport = false;
	let exitFullscreen: () => Promise<void> = async () => {
		console.warn('Exit fullscreen not supported');
	}; // Default fallback
	let requestFullscreen: () => Promise<void> = async () => {
		console.warn('Request fullscreen not supported on element');
	}; // Default fallback

	const dispatch = createEventDispatcher<{ toggleFullscreen: boolean }>();

	onMount(() => {
		// --- Fullscreen API Detection Logic ---
		const doc = document as Document & {
			webkitFullscreenEnabled?: boolean;
			mozFullScreenEnabled?: boolean;
			msFullscreenEnabled?: boolean;
			mozCancelFullScreen?: () => Promise<void>; // Standard returns Promise
			webkitExitFullscreen?: () => Promise<void>;
			msExitFullscreen?: () => Promise<void>;
		};

		fullscreenSupport = !!(
			document.fullscreenEnabled ||
			doc.webkitFullscreenEnabled ||
			doc.mozFullScreenEnabled ||
			doc.msFullscreenEnabled
		);
		// console.log('FullScreen onMount. Support:', fullscreenSupport);

		// Assign the correct exit function, ensuring it's called on document
		const exitFn =
			document.exitFullscreen ||
			doc.mozCancelFullScreen ||
			doc.webkitExitFullscreen ||
			doc.msExitFullscreen;

		if (exitFn) {
			// Bind the function to the document context
			exitFullscreen = exitFn.bind(document);
		}

		// Assign the correct request function
		requestFullscreen = async () => {
			if (!fsContainer) return;
			const el = fsContainer as HTMLElement & {
				mozRequestFullScreen?: () => Promise<void>; // Standard returns Promise
				webkitRequestFullscreen?: () => Promise<void>;
				msRequestFullscreen?: () => Promise<void>;
			};
			const reqFn =
				el.requestFullscreen ||
				el.mozRequestFullScreen ||
				el.webkitRequestFullscreen ||
				el.msRequestFullscreen;

			if (reqFn) {
				try {
					// Bind the function to the element context and call it
					await reqFn.call(el);
				} catch (err) {
					console.error('Error requesting fullscreen:', err);
				}
			} else {
				console.warn('Request fullscreen not supported on element');
			}
		};
		// --- End Fullscreen API Logic ---

		// --- Fullscreen Change Listener ---
		// Optional: Listen for changes triggered by Escape key etc.
		const handleFsChange = () => {
			const fullscreenElement =
				document.fullscreenElement ||
				(doc as any).webkitFullscreenElement ||
				(doc as any).mozFullScreenElement ||
				(doc as any).msFullscreenElement;
			const currentlyFull = !!fullscreenElement;
			if (isFull !== currentlyFull) {
				isFull = currentlyFull;
				dispatch('toggleFullscreen', isFull);
				// console.log("Fullscreen state changed externally:", isFull);
			}
		};

		document.addEventListener('fullscreenchange', handleFsChange);
		document.addEventListener('webkitfullscreenchange', handleFsChange);
		document.addEventListener('mozfullscreenchange', handleFsChange);
		document.addEventListener('MSFullscreenChange', handleFsChange);

		// Cleanup listener on component destroy
		return () => {
			document.removeEventListener('fullscreenchange', handleFsChange);
			document.removeEventListener('webkitfullscreenchange', handleFsChange);
			document.removeEventListener('mozfullscreenchange', handleFsChange);
			document.removeEventListener('MSFullscreenChange', handleFsChange);
		};
	});

	async function fsToggle() {
		if (!fullscreenSupport) return;

		// Store current state before attempting change
		const enteringFullscreen = !isFull;

		try {
			if (isFull) {
				await exitFullscreen(); // Call the bound function
				// Update state only if exit succeeded (or no error)
				// Note: Event listener above might handle this, but explicit update can be safer
				isFull = false;
			} else {
				await requestFullscreen(); // Call the bound function
				// Update state only if request succeeded (or no error)
				// Note: Event listener above might handle this
				isFull = true;
			}
			// Dispatch state change regardless of listener (more immediate feedback)
			dispatch('toggleFullscreen', isFull);
			// Trigger resize after state change seems complete
			setTimeout(() => window.dispatchEvent(new Event('resize')), 50);
		} catch (err) {
			console.error(`Error ${enteringFullscreen ? 'entering' : 'exiting'} fullscreen:`, err);
			// Optional: Revert state if the operation failed?
			// isFull = !enteringFullscreen;
			// dispatch('toggleFullscreen', isFull);
		}
	}
</script>

<div class="fullscreen-container {isFull ? 'isFull' : ''}" bind:this={fsContainer}>
	<slot {isFull} />

	{#if fullscreenSupport}
		<button
			class="app-fullscreen-btn"
			on:click={fsToggle}
			aria-label={isFull ? 'Exit browser fullscreen' : 'Enter browser fullscreen'}
		>
			<i class="fa-solid {isFull ? 'fa-compress-arrows-alt' : 'fa-expand-arrows-alt'} fs-icon"></i>
		</button>
	{/if}
</div>

<style>
	.fullscreen-container {
		position: relative;
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
		flex: 1;
		overflow: hidden;
	}

	.app-fullscreen-btn {
		/* Base sizes for dynamic scaling - match Sequence Widget buttons */
		--base-size: 45px; /* Base size of the button */
		--base-icon-size: 19px; /* Base size of the icon */
		--base-margin: 10px; /* Base margin from corner */

		z-index: 9999;
		position: absolute;
		right: var(--base-margin);
		bottom: var(--base-margin);

		width: var(--base-size);
		height: var(--base-size);
		min-width: 38px;
		min-height: 38px;

		background-color: var(--tkc-button-panel-background, #2a2a2e);
		color: var(
			--tkc-icon-color-app-fullscreen,
			#8338ec
		); /* Purple icon color to distinguish from sequence overlay */

		border: none;
		border-radius: 50%;
		display: flex;
		justify-content: center;
		align-items: center;
		cursor: pointer;
		padding: 0;

		box-shadow:
			0 3px 6px rgba(0, 0, 0, 0.16),
			0 3px 6px rgba(0, 0, 0, 0.23);

		transition:
			transform 0.2s ease-out,
			background-color 0.2s ease-out,
			box-shadow 0.2s ease-out;

		overflow: hidden;
	}

	/* Style icon directly if needed */
	.app-fullscreen-btn i.fs-icon {
		font-size: var(--base-icon-size);
		line-height: 1; /* Ensure proper vertical alignment */
	}

	.app-fullscreen-btn:hover {
		background-color: var(--tkc-button-panel-background-hover, #3c3c41);
		transform: translateY(-2px) scale(1.05);
		box-shadow:
			0 6px 12px rgba(0, 0, 0, 0.2),
			0 4px 8px rgba(0, 0, 0, 0.26);
	}

	.app-fullscreen-btn:active {
		transform: translateY(0px) scale(1);
		background-color: var(--tkc-button-panel-background-active, #1e1e21);
		box-shadow:
			0 1px 3px rgba(0, 0, 0, 0.12),
			0 1px 2px rgba(0, 0, 0, 0.24);
	}
</style>
