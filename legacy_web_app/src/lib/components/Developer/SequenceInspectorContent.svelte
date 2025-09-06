<!--
  Sequence Inspector Content Component

  This component displays the current sequence data in JSON format.
  It's designed to be embedded in the DeveloperTools panel.
-->
<script lang="ts">
	import { writable } from 'svelte/store';
	import sequenceDataService from '$lib/services/SequenceDataService';
	import { onDestroy } from 'svelte';

	// State
	let jsonText = '';
	const error = writable(''); // For formatting/parsing errors

	// State for copy button feedback
	type CopyStatus = 'idle' | 'copying' | 'copied' | 'error';
	let copyStatus = writable<CopyStatus>('idle');
	let copyError = writable<string | null>(null); // Specific error for copy action

	// Timeout ID for resetting copy status
	let copyTimeoutId: ReturnType<typeof setTimeout> | null = null;

	// --- Formatting Functions ---
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

	// Format sequence data
	function formatSequence() {
		return sequenceDataService.getCurrentSequence();
	}

	// Initialize JSON text
	function initializeJsonText() {
		try {
			jsonText = JSON.stringify(formatSequence(), null, 2);
			error.set(''); // Clear formatting errors
			copyError.set(null); // Clear copy errors
			copyStatus.set('idle'); // Reset copy button state
		} catch (e) {
			error.set('Error formatting sequence: ' + (e as Error).message);
			jsonText = 'Error generating JSON.';
		}
	}

	// Initialize on mount
	initializeJsonText();

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

	// Cleanup timeout on component destroy
	onDestroy(() => {
		if (copyTimeoutId) clearTimeout(copyTimeoutId);
	});

	// Refresh button handler
	function handleRefresh() {
		initializeJsonText();
	}
</script>

<div class="sequence-inspector">
	<div class="actions">
		<button on:click={handleRefresh} class="refresh-button">
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
			>
				<path
					d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"
				/>
			</svg>
			<span>Refresh</span>
		</button>
		<div class="spacer"></div>
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
				>
					<rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
					<path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
				</svg>
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
					stroke-linejoin="round"
				>
					<polyline points="20 6 9 17 4 12"></polyline>
				</svg>
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
				>
					<circle cx="12" cy="12" r="10"></circle>
					<line x1="12" y1="8" x2="12" y2="12"></line>
					<line x1="12" y1="16" x2="12.01" y2="16"></line>
				</svg>
				<span>Error</span>
			{/if}
		</button>
	</div>

	{#if $error}
		<p class="error-message">{$error}</p>
	{/if}

	{#if $copyError && $copyStatus === 'error'}
		<p class="error-message">{$copyError}</p>
	{/if}

	<textarea
		bind:value={jsonText}
		placeholder="Sequence JSON will appear here..."
		spellcheck="false"
		readonly={$copyStatus === 'copying'}
	></textarea>
</div>

<style>
	.sequence-inspector {
		display: flex;
		flex-direction: column;
		height: 100%;
		color: #e0e0e0;
		font-family:
			system-ui,
			-apple-system,
			sans-serif;
	}

	.actions {
		display: flex;
		align-items: center;
		margin-bottom: 12px;
	}

	.spacer {
		flex: 1;
	}

	.refresh-button,
	.copy-button {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		background-color: #2a2a2a;
		color: #e0e0e0;
		border: 1px solid #444;
		padding: 6px 12px;
		border-radius: 4px;
		cursor: pointer;
		font-size: 14px;
		transition: all 0.2s ease;
	}

	.refresh-button:hover,
	.copy-button:hover {
		background-color: #333;
	}

	.copy-button.copying {
		background-color: #333;
		cursor: wait;
	}

	.copy-button.copied {
		background-color: #28a745;
		color: white;
		border-color: #28a745;
	}

	.copy-button.error {
		background-color: #dc3545;
		color: white;
		border-color: #dc3545;
	}

	.error-message {
		color: #ff6b6b;
		margin: 0 0 12px 0;
		font-size: 14px;
		background-color: rgba(220, 53, 69, 0.2);
		padding: 8px;
		border-radius: 4px;
		border-left: 3px solid #dc3545;
	}

	textarea {
		flex: 1;
		width: 100%;
		padding: 12px;
		border: 1px solid #444;
		border-radius: 4px;
		font-family: monospace;
		font-size: 14px;
		line-height: 1.5;
		resize: none;
		background-color: #2a2a2a;
		color: #e0e0e0;
	}

	textarea:focus {
		outline: none;
		border-color: #4da6ff;
		box-shadow: 0 0 0 2px rgba(77, 166, 255, 0.2);
	}
</style>
