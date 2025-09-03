<script lang="ts">
	import { sequenceStore } from '$lib/state/stores/sequence/sequenceAdapter';
	import { writable, get } from 'svelte/store';
	import { fade, fly } from 'svelte/transition'; // Import transitions
	import { cubicOut } from 'svelte/easing'; // Import easing

	let visible = false;
	let jsonText = '';
	const error = writable(''); // For formatting/parsing errors

	// State for copy button feedback
	type CopyStatus = 'idle' | 'copying' | 'copied' | 'error';
	let copyStatus = writable<CopyStatus>('idle');
	let copyError = writable<string | null>(null); // Specific error for copy action

	// Timeout ID for resetting copy status
	let copyTimeoutId: ReturnType<typeof setTimeout> | null = null;

	// --- Formatting Functions (remain the same) ---
	function formatBeatForExport(beat: any) {
		const createAttributes = (motionData: any) => {
			if (!motionData) return undefined;
			const attributes = {
				start_loc: motionData.startLoc,
				end_loc: motionData.endLoc,
				start_ori: motionData.startOri,
				end_ori: motionData.endOri,
				prop_rot_dir: motionData.propRotDir,
				turns: motionData.turns,
				motion_type: motionData.motionType
			};
			Object.keys(attributes).forEach(
				(key) =>
					attributes[key as keyof typeof attributes] === undefined &&
					delete attributes[key as keyof typeof attributes]
			);
			return Object.keys(attributes).length > 0 ? attributes : undefined;
		};
		const formatted = {
			beat: beat.beatNumber,
			letter: beat.pictographData?.letter ?? undefined,
			sequence_start_position:
				beat.beatNumber === 0 ? beat.pictographData?.startPos?.replace(/\d+/g, '') : undefined,
			end_pos: beat.pictographData?.endPos,
			timing: beat.pictographData?.timing,
			direction: beat.pictographData?.direction,
			blue_attributes: createAttributes(beat.pictographData?.blueMotionData),
			red_attributes: createAttributes(beat.pictographData?.redMotionData)
		};
		Object.keys(formatted).forEach(
			(key) =>
				(formatted as Record<string, any>)[key] === undefined &&
				delete (formatted as Record<string, any>)[key]
		);
		return formatted;
	}
	// Modify your formatSequence function to read from sequenceDataService
	function formatSequence() {
		// This would show the actual JSON data instead of beatsStore
		return sequenceDataService.getCurrentSequence();
	}

	// --- UI Interaction ---
	function toggleInspector() {
		visible = !visible;
		if (visible) {
			try {
				jsonText = JSON.stringify(formatSequence(), null, 2);
				error.set(''); // Clear formatting errors
				copyError.set(null); // Clear copy errors
				copyStatus.set('idle'); // Reset copy button state
			} catch (e) {
				error.set('Error formatting sequence: ' + (e as Error).message);
				jsonText = 'Error generating JSON.';
			}
		} else {
			// Clear timeout if closing the panel
			if (copyTimeoutId) clearTimeout(copyTimeoutId);
		}
	}

	// REMOVED: handleSave function is no longer needed

	/** Handles copying the JSON text to the clipboard */
	async function handleCopy() {
		// Clear previous timeout and errors
		if (copyTimeoutId) clearTimeout(copyTimeoutId);
		copyError.set(null);
		copyStatus.set('copying'); // Indicate copying process start

		if (!navigator.clipboard) {
			copyError.set('Clipboard API not available in this context.');
			copyStatus.set('error');
			console.error('Clipboard API not available.');
			resetCopyStatusAfterDelay();
			return;
		}

		try {
			await navigator.clipboard.writeText(jsonText);
			copyStatus.set('copied'); // Set status to copied on success
		} catch (err) {
			copyError.set('Failed to copy JSON.'); // Set specific copy error
			copyStatus.set('error'); // Set status to error on failure
			console.error('Failed to copy text: ', err);
		} finally {
			resetCopyStatusAfterDelay(); // Reset status back to idle after delay
		}
	}

	/** Resets the copy button status to 'idle' after a delay */
	function resetCopyStatusAfterDelay(delay = 2000) {
		copyTimeoutId = setTimeout(() => {
			copyStatus.set('idle');
			copyError.set(null); // Clear copy error when resetting
			copyTimeoutId = null;
		}, delay);
	}

	function closeInspector() {
		visible = false;
		// Clear timeout if closing the panel
		if (copyTimeoutId) clearTimeout(copyTimeoutId);
	}

	// Cleanup timeout on component destroy
	import { onDestroy } from 'svelte';
	import sequenceDataService from '$lib/services/SequenceDataService';
	onDestroy(() => {
		if (copyTimeoutId) clearTimeout(copyTimeoutId);
	});
</script>

<button
	class="dev-tab-button"
	on:click={toggleInspector}
	aria-label="Toggle Sequence JSON Inspector"
	title="Toggle Sequence JSON Inspector"
>
	<span aria-hidden="true">🧪</span>
</button>

{#if visible}
	<div class="json-flyout" transition:fade={{ duration: 200 }}>
		<div class="header">
			<h3>Sequence Inspector</h3>
			<button
				class="close-button"
				on:click={closeInspector}
				aria-label="Close Inspector"
				title="Close"
			>
				<span aria-hidden="true">✖</span>
			</button>
		</div>

		<textarea
			bind:value={jsonText}
			placeholder="Sequence JSON will appear here..."
			spellcheck="false"
			readonly={$copyStatus === 'copying'}
		></textarea>

		<div class="actions">
			{#if $error}
				<p class="error-message formatting-error">{$error}</p>
			{/if}
			{#if $copyError && $copyStatus === 'error'}
				<p class="error-message copy-error">{$copyError}</p>
			{/if}

			<button
				class="copy-button"
				class:copying={$copyStatus === 'copying'}
				class:copied={$copyStatus === 'copied'}
				class:error={$copyStatus === 'error'}
				on:click={handleCopy}
				disabled={$copyStatus !== 'idle'}
				aria-live="polite"
			>
				{#if $copyStatus === 'idle'}
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="16"
						height="16"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
						><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path
							d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"
						></path></svg
					>
					<span>Copy JSON</span>
				{:else if $copyStatus === 'copying'}
					<span>Copying...</span>
				{:else if $copyStatus === 'copied'}
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="16"
						height="16"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="3"
						stroke-linecap="round"
						stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg
					>
					<span>Copied!</span>
				{:else if $copyStatus === 'error'}
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="16"
						height="16"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
						><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"
						></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg
					>
					<span>Error</span>
				{/if}
			</button>
		</div>
	</div>
{/if}

<style>
	/* --- Toggle Button Styles (remain the same) --- */

	.dev-tab-button {
		position: absolute;
		left: 10px; /* Align with the dialog's left edge */
		top: calc(50% - 36px); /* Position near the top of the dialog */
		z-index: 1100;
		background-color: rgba(58, 123, 213, 0.8);
		color: white;
		border: none;
		width: 36px;
		height: 36px;
		padding: 0;
		border-radius: 50%;
		cursor: pointer;
		font-size: 1.2rem;
		line-height: 36px;
		text-align: center;
		box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
		transition:
			background-color 0.2s ease,
			transform 0.2s ease;
		backdrop-filter: blur(2px);
	}
	.dev-tab-button:hover {
		background-color: rgba(78, 143, 233, 0.9);
		transform: scale(1.1);
	}
	.dev-tab-button:active {
		transform: scale(1.05);
	}
	/* --- Flyout Panel Styles (remain the same) --- */
	.json-flyout {
		position: absolute;
		top: 50%; /* Position halfway down the window */
		left: 10px; /* Keep it on the left */
		transform: translateY(-50%); /* Center it vertically */
		width: clamp(300px, 40vw, 500px);
		height: clamp(300px, 60vh, 600px);
		background-color: #2a2a2e;
		color: #e0e0e0;
		border: 1px solid #444;
		border-radius: 8px;
		padding: 1rem;
		z-index: 1090;
		box-shadow: 0 5px 15px rgba(0, 0, 0, 0.4);
		display: flex;
		flex-direction: column;
		overflow: hidden;
	}
	.json-flyout .header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 12px;
		flex-shrink: 0;
	}
	.json-flyout .header h3 {
		margin: 0;
		font-size: 1.1rem;
		font-weight: 600;
		color: #ffffff;
	}
	.json-flyout .close-button {
		background: transparent;
		border: none;
		color: #a0a0a0;
		font-size: 1.3rem;
		cursor: pointer;
		padding: 2px;
		line-height: 1;
		transition: color 0.2s ease;
	}
	.json-flyout .close-button:hover {
		color: #ffffff;
	}

	/* --- Textarea Styles (remain the same) --- */
	textarea {
		flex: 1;
		width: 100%;
		background-color: #1e1e1e;
		color: #d4d4d4;
		border: 1px solid #3c3c3c;
		border-radius: 4px;
		padding: 10px;
		font-family: 'Fira Code', 'Consolas', 'Monaco', monospace;
		font-size: 0.9rem;
		line-height: 1.5;
		resize: none;
		margin-bottom: 12px;
		box-sizing: border-box;
		overflow-y: auto;
	}
	textarea:focus {
		outline: none;
		border-color: #3a7bd5;
		box-shadow: 0 0 0 2px rgba(58, 123, 213, 0.3);
	}

	/* --- Actions Area --- */
	.json-flyout .actions {
		display: flex;
		/* Change justification to push content to the right */
		justify-content: flex-end;
		align-items: center;
		flex-shrink: 0;
		flex-wrap: wrap; /* Allow wrapping */
		gap: 10px; /* Space between items if they wrap */
	}

	/* --- Copy Button --- */
	.copy-button {
		/* Base styles */
		display: inline-flex; /* Align icon and text */
		align-items: center;
		gap: 6px; /* Space between icon and text */
		background-color: #4a4a50; /* Neutral dark background */
		color: #e0e0e0;
		border: 1px solid #666;
		padding: 8px 14px; /* Adjusted padding */
		border-radius: 6px; /* Slightly more rounded */
		cursor: pointer;
		font-weight: 500;
		font-size: 0.9rem;
		transition: all 0.2s ease-out; /* Smooth transitions */
		overflow: hidden; /* Hide overflowing content during animations */
		position: relative; /* For potential pseudo-elements */
	}

	.copy-button svg {
		/* Style for icons */
		width: 16px;
		height: 16px;
		flex-shrink: 0; /* Prevent icon shrinking */
	}

	.copy-button:not(:disabled):hover {
		background-color: #5a5a60;
		border-color: #888;
		transform: translateY(-1px); /* Subtle lift */
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
	}

	.copy-button:disabled {
		cursor: default;
		opacity: 0.7;
	}

	/* Copying state - subtle indication */
	.copy-button.copying {
		background-color: #5a5a60;
		/* You could add a subtle loading indicator or animation here */
	}

	/* Copied state - success indication */
	.copy-button.copied {
		background-color: #28a745; /* Green for success */
		border-color: #28a745;
		color: white;
		animation: pulse-success 0.5s ease-out;
	}

	/* Error state */
	.copy-button.error {
		background-color: #dc3545; /* Red for error */
		border-color: #dc3545;
		color: white;
		animation: shake-error 0.5s ease-out;
	}

	/* Animations */
	@keyframes pulse-success {
		0% {
			transform: scale(1);
		}
		50% {
			transform: scale(1.05);
		}
		100% {
			transform: scale(1);
		}
	}

	@keyframes shake-error {
		0%,
		100% {
			transform: translateX(0);
		}
		25% {
			transform: translateX(-3px);
		}
		50% {
			transform: translateX(3px);
		}
		75% {
			transform: translateX(-3px);
		}
	}

	/* --- Error Message(s) --- */
	.error-message {
		color: #ff6b6b;
		font-size: 0.85rem;
		margin: 0;
		text-align: right;
		/* Let it take space but don't force it to grow excessively */
		flex-basis: auto;
		/* Order it before the button if needed */
		order: -1; /* Place error messages before the button */
	}

	/* --- Scrollbar Styles (remain the same) --- */
	textarea::-webkit-scrollbar {
		width: 8px;
	}
	textarea::-webkit-scrollbar-track {
		background: #2a2a2e;
		border-radius: 4px;
	}
	textarea::-webkit-scrollbar-thumb {
		background-color: #555;
		border-radius: 4px;
		border: 2px solid #2a2a2e;
	}
	textarea::-webkit-scrollbar-thumb:hover {
		background-color: #777;
	}
</style>
