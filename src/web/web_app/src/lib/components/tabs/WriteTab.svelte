<!-- Write Tab - Act creation and editing with pixel-perfect desktop replica -->
<script lang="ts">
	import ActBrowser from '$lib/components/write/ActBrowser.svelte';
	import ActSheet from '$lib/components/write/ActSheet.svelte';
	import MusicPlayer from '$lib/components/write/MusicPlayer.svelte';
	import WriteToolbar from '$lib/components/write/WriteToolbar.svelte';
	import {
		createDefaultMusicPlayerState,
		createEmptyAct,
		type ActData,
		type ActThumbnailInfo,
		type MusicPlayerState,
	} from '$lib/types/write';

	// State management using runes

	let currentAct = $state<ActData | null>(null);
	let availableActs = $state<ActThumbnailInfo[]>([]);
	let isLoading = $state<boolean>(false);
	let hasUnsavedChanges = $state<boolean>(false);
	let musicPlayerState = $state<MusicPlayerState>(createDefaultMusicPlayerState());

	// Layout state
	let browserWidth = $state(300); // Default browser width
	let isDragging = $state(false);

	// Initialize with sample data
	$effect(() => {
		// TODO: Load actual acts from storage/API
		availableActs = [
			{
				id: '1',
				name: 'Sample Act 1',
				description: 'A sample act for demonstration',
				filePath: '/acts/sample1.json',
				sequenceCount: 3,
				hasMusic: true,
				lastModified: new Date(Date.now() - 86400000), // 1 day ago
			},
			{
				id: '2',
				name: 'Sample Act 2',
				description: 'Another sample act',
				filePath: '/acts/sample2.json',
				sequenceCount: 1,
				hasMusic: false,
				lastModified: new Date(Date.now() - 172800000), // 2 days ago
			},
		];
	});

	// Toolbar handlers
	function handleNewActRequested() {
		currentAct = createEmptyAct();
		hasUnsavedChanges = true;
		console.log('Creating new act');
	}

	function handleSaveRequested() {
		if (!currentAct) return;
		// TODO: Implement actual save logic
		hasUnsavedChanges = false;
		console.log('Saving act:', currentAct.name);
	}

	function handleSaveAsRequested() {
		if (!currentAct) return;
		// TODO: Implement save as dialog
		console.log('Save as requested for act:', currentAct.name);
	}

	// Act browser handlers
	function handleActSelected(filePath: string) {
		// TODO: Load actual act from file
		const actInfo = availableActs.find((act) => act.filePath === filePath);
		if (actInfo) {
			currentAct = {
				id: actInfo.id,
				name: actInfo.name,
				description: actInfo.description,
				sequences: [], // TODO: Load actual sequences
				metadata: {
					created: new Date(),
					modified: actInfo.lastModified,
				},
				filePath: actInfo.filePath,
			};
			hasUnsavedChanges = false;
			console.log('Loading act:', actInfo.name);
		}
	}

	function handleActBrowserRefresh() {
		isLoading = true;
		// TODO: Refresh acts from storage
		setTimeout(() => {
			isLoading = false;
			console.log('Refreshed act browser');
		}, 1000);
	}

	// Act sheet handlers
	function handleActInfoChanged(name: string, description: string) {
		if (!currentAct) return;
		currentAct.name = name;
		currentAct.description = description;
		hasUnsavedChanges = true;
	}

	function handleMusicLoadRequested() {
		// TODO: Implement music file selection
		console.log('Music load requested');
	}

	function handleSequenceClicked(position: number) {
		// TODO: Open sequence in construct tab
		console.log('Sequence clicked:', position);
	}

	function handleSequenceRemoveRequested(position: number) {
		if (!currentAct) return;
		currentAct.sequences.splice(position, 1);
		hasUnsavedChanges = true;
		console.log('Sequence removed:', position);
	}

	// Music player handlers
	function handlePlayRequested() {
		musicPlayerState.isPlaying = true;
		musicPlayerState.isPaused = false;
		console.log('Play requested');
	}

	function handlePauseRequested() {
		musicPlayerState.isPlaying = false;
		musicPlayerState.isPaused = true;
		console.log('Pause requested');
	}

	function handleStopRequested() {
		musicPlayerState.isPlaying = false;
		musicPlayerState.isPaused = false;
		musicPlayerState.currentTime = 0;
		console.log('Stop requested');
	}

	function handleSeekRequested(position: number) {
		musicPlayerState.currentTime = position;
		console.log('Seek requested:', position);
	}

	// Splitter handlers
	function handleSplitterMouseDown(event: MouseEvent) {
		isDragging = true;
		event.preventDefault();

		const handleMouseMove = (e: MouseEvent) => {
			if (!isDragging) return;
			const newWidth = Math.max(200, Math.min(500, e.clientX));
			browserWidth = newWidth;
		};

		const handleMouseUp = () => {
			isDragging = false;
			document.removeEventListener('mousemove', handleMouseMove);
			document.removeEventListener('mouseup', handleMouseUp);
		};

		document.addEventListener('mousemove', handleMouseMove);
		document.addEventListener('mouseup', handleMouseUp);
	}

	// Keyboard support for splitter
	function handleSplitterKeyDown(event: KeyboardEvent) {
		const step = 10;
		switch (event.key) {
			case 'ArrowLeft':
				event.preventDefault();
				browserWidth = Math.max(200, browserWidth - step);
				break;
			case 'ArrowRight':
				event.preventDefault();
				browserWidth = Math.min(500, browserWidth + step);
				break;
		}
	}
</script>

<div class="write-tab">
	<!-- Toolbar -->
	<div class="toolbar-section">
		<WriteToolbar
			{hasUnsavedChanges}
			disabled={isLoading}
			onNewActRequested={handleNewActRequested}
			onSaveRequested={handleSaveRequested}
			onSaveAsRequested={handleSaveAsRequested}
		/>
	</div>

	<!-- Main content area with horizontal layout -->
	<div class="main-content">
		<!-- Act Browser -->
		<div class="browser-section" style="width: {browserWidth}px;">
			<ActBrowser
				acts={availableActs}
				{isLoading}
				onActSelected={handleActSelected}
				onRefresh={handleActBrowserRefresh}
			/>
		</div>

		<!-- Splitter -->
		<button
			class="splitter"
			class:dragging={isDragging}
			onmousedown={handleSplitterMouseDown}
			onkeydown={handleSplitterKeyDown}
			aria-label="Resize panels"
			type="button"
		></button>

		<!-- Right panel with act sheet and music player -->
		<div class="right-panel">
			<!-- Act Sheet -->
			<div class="sheet-section">
				<ActSheet
					act={currentAct}
					disabled={isLoading}
					onActInfoChanged={handleActInfoChanged}
					onMusicLoadRequested={handleMusicLoadRequested}
					onSequenceClicked={handleSequenceClicked}
					onSequenceRemoveRequested={handleSequenceRemoveRequested}
				/>
			</div>

			<!-- Music Player -->
			<div class="player-section">
				<MusicPlayer
					playerState={musicPlayerState}
					disabled={isLoading}
					onPlayRequested={handlePlayRequested}
					onPauseRequested={handlePauseRequested}
					onStopRequested={handleStopRequested}
					onSeekRequested={handleSeekRequested}
				/>
			</div>
		</div>
	</div>
</div>

<style>
	.write-tab {
		display: flex;
		flex-direction: column;
		width: 100%;
		height: 100%;
		background: transparent;
		overflow: hidden;
	}

	.toolbar-section {
		flex-shrink: 0;
		padding: var(--spacing-sm);
	}

	.main-content {
		flex: 1;
		display: flex;
		min-height: 0;
		gap: 0;
		padding: 0 var(--spacing-sm) var(--spacing-sm) var(--spacing-sm);
	}

	.browser-section {
		flex-shrink: 0;
		min-width: 200px;
		max-width: 500px;
	}

	.splitter {
		width: 4px;
		background: rgba(80, 80, 100, 0.4);
		cursor: col-resize;
		transition: background-color var(--transition-fast);
		flex-shrink: 0;
	}

	.splitter:hover,
	.splitter.dragging {
		background: rgba(120, 150, 200, 0.8);
	}

	.right-panel {
		flex: 1;
		display: flex;
		flex-direction: column;
		gap: var(--spacing-sm);
		min-width: 0;
	}

	.sheet-section {
		flex: 1;
		min-height: 0;
	}

	.player-section {
		flex-shrink: 0;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.main-content {
			flex-direction: column;
			gap: var(--spacing-sm);
		}

		.browser-section {
			width: 100% !important;
			max-height: 200px;
			overflow-y: auto;
		}

		.splitter {
			display: none;
		}

		.right-panel {
			gap: var(--spacing-xs);
		}
	}

	@media (max-width: 480px) {
		.toolbar-section {
			padding: var(--spacing-xs);
		}

		.main-content {
			padding: 0 var(--spacing-xs) var(--spacing-xs) var(--spacing-xs);
		}

		.browser-section {
			max-height: 150px;
		}
	}

	/* Prevent text selection during drag */
	.splitter.dragging {
		user-select: none;
	}
</style>
