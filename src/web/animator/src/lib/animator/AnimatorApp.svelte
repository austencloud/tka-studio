<script lang="ts">
	import type { SequenceData, PropState, DictionaryItem } from './types/core.js';

	// Import new layout components
	import AppHeader from './components/layout/AppHeader.svelte';
	import AppLayout from './components/layout/AppLayout.svelte';
	import WelcomeSection from './components/sections/WelcomeSection.svelte';
	import StickyAnimationViewer from './components/layout/StickyAnimationViewer.svelte';

	// Import existing subcomponents
	import ThumbnailBrowser from './components/browser/ThumbnailBrowser.svelte';
	import AnimatorCanvas from './components/canvas/AnimatorCanvas.svelte';

	import AnimatorMessage from './components/ui/AnimatorMessage.svelte';
	import SequenceControlPanel from './components/controls/SequenceControlPanel.svelte';
	import SequenceReadyState from './components/controls/SequenceReadyState.svelte';
	import BeatViewer from './components/animation/BeatViewer.svelte';

	// Import new extracted components
	import AnimationController from './components/animation/AnimationController.svelte';
	import ThemeManager from './components/theme/ThemeManager.svelte';
	import SidebarManager from './components/layout/SidebarManager.svelte';
	import SidebarControls from './components/layout/SidebarControls.svelte';
	
	// Import hardcoded sequences for testing
	import { EXAMPLE_SEQUENCES } from './core/services/hardcoded-dictionary.js';

	// Import global styles
	import './styles/global.css';
	
	// Add type import for DictionaryItem

	// Import utilities (these are used in the functions but not currently imported)
	// Note: These functions are now handled by AnimationController, so we'll remove their usage

	// State variables using Svelte 5 runes
	let sequenceData = $state<SequenceData | null>(null);
	let blueProp = $state<PropState>({ centerPathAngle: 0, staffRotationAngle: 0, x: 0, y: 0 });
	let redProp = $state<PropState>({ centerPathAngle: 0, staffRotationAngle: 0, x: 0, y: 0 });
	let canvasWidth = $state(500);
	let canvasHeight = $state(500);

	// Message state
	let errorMessage = $state('');
	let successMessage = $state('');

	// UI state
	let selectedItem = $state<DictionaryItem | null>(null);
	let isDarkMode = $state(false);

	// Sticky animation viewer state
	let isAnimationSticky = $state(false);

	// Component references
	let animationController: AnimationController | undefined = $state();
	let themeManager: ThemeManager | undefined = $state();
	let sidebarManager: SidebarManager | undefined = $state();

	// Sidebar state - default to 50% of viewport width
	let sidebarWidth = $state(typeof window !== 'undefined' ? window.innerWidth * 0.5 : 600);
	let isResizing = $state(false);

	// Animation Controller event handlers
	function handleAnimationError(message: string): void {
		errorMessage = message;
		successMessage = '';
	}

	function handleAnimationSuccess(message: string): void {
		successMessage = message;
		errorMessage = '';
	}

	// Handle sequence selection from thumbnail browser
	function handleSequenceSelected(data: SequenceData, item: DictionaryItem): void {
		selectedItem = item;
		sequenceData = data;

		// Auto-play the animation after sequence is loaded
		setTimeout(() => {
			animationController?.playSequence();
		}, 100);
	}

	// Theme management
	function toggleTheme(): void {
		themeManager?.toggle();
	}

	function toggleStickyAnimation(): void {
		isAnimationSticky = !isAnimationSticky;
	}

	function closeStickyAnimation(): void {
		isAnimationSticky = false;
	}

	// Sidebar resize handling
	function handleResizeStart(e: MouseEvent): void {
		sidebarManager?.startResize(e);
	}

	// Sidebar preset handlers
	function handleSetSidebar50(): void {
		sidebarManager?.setSidebar50();
	}

	function handleSetSidebar75(): void {
		sidebarManager?.setSidebar75();
	}

	function handleSetSidebar25(): void {
		sidebarManager?.setSidebar25();
	}

	// Beat viewer functionality
	function handleBeatSelect(beatIndex: number): void {
		if (animationController) {
			// Stop current animation
			animationController.resetAnimation();

			// Set to specific beat (beatIndex is 0-based, but we need to account for metadata)
			// The AnimationController expects beat numbers starting from 0
			// We'll need to modify the AnimationController to support jumping to specific beats
			jumpToBeat(beatIndex);
		}
	}

	function jumpToBeat(beatNumber: number): void {
		if (animationController && sequenceData) {
			animationController.jumpToBeat(beatNumber);
		}
	}
	
	// Quick test functions to load hardcoded sequences
	function loadTestSequence(sequenceName: string): void {
		const testSequence = EXAMPLE_SEQUENCES[sequenceName];
		if (testSequence) {
			sequenceData = testSequence;
			selectedItem = {
				id: sequenceName,
				name: sequenceName,
				filePath: '',
				metadata: testSequence[0],
				sequenceData: testSequence,
				thumbnailUrl: '',
				versions: ['v1']
			};
			
			// Auto-play after loading
			setTimeout(() => {
				animationController?.playSequence();
			}, 100);
		}
	}
</script>

<!-- Theme Manager (invisible component) -->
<ThemeManager bind:this={themeManager} bind:isDarkMode />

<!-- Sidebar Manager (invisible component) -->
<SidebarManager bind:this={sidebarManager} bind:sidebarWidth bind:isResizing />

<!-- Animation Controller (invisible - just for state management) -->
<AnimationController
	bind:this={animationController}
	bind:sequenceData
	bind:blueProp
	bind:redProp
	onError={handleAnimationError}
	onSuccess={handleAnimationSuccess}
	renderControls={false}
/>

<div class="animator-app">
	<AppHeader {isDarkMode} onThemeToggle={toggleTheme} />

	<AppLayout {sidebarWidth} {isResizing} onResizeStart={handleResizeStart}>
		{#snippet sidebar()}
			<div class="sidebar-header">
				<h2>Sequence Library</h2>
			</div>

			<div class="sidebar-content">
				<ThumbnailBrowser onSequenceSelected={handleSequenceSelected} />
			</div>

			<SidebarControls
				onSetSidebar50={handleSetSidebar50}
				onSetSidebar75={handleSetSidebar75}
				onSetSidebar25={handleSetSidebar25}
			/>
		{/snippet}

		<AnimatorMessage errorMsg={errorMessage} successMsg={successMessage} />

		{#if sequenceData}
			<div class="animator-section">
				{#if selectedItem}
					<div class="sequence-info">
						<h3>{selectedItem.name}</h3>
						{#if selectedItem.metadata.author}
							<p>by {selectedItem.metadata.author}</p>
						{/if}
					</div>
				{/if}

				<StickyAnimationViewer
					isSticky={isAnimationSticky}
					onToggleSticky={toggleStickyAnimation}
					onCloseSticky={closeStickyAnimation}
				>
					<AnimatorCanvas {blueProp} {redProp} width={canvasWidth} height={canvasHeight} />
				</StickyAnimationViewer>

				<!-- Sequence Controls directly below the animation -->
				{#if animationController}
					{@const animState = animationController.getAnimationState()}

					{#if sequenceData && !animState.isPlaying && animState.currentBeat === 0}
						<!-- Show ready state when sequence is loaded but not playing -->
						<SequenceReadyState
							sequenceWord={animState.sequenceWord}
							sequenceAuthor={animState.sequenceAuthor}
							totalSteps={animState.totalBeats}
							onPlay={() => animationController?.togglePlayPause()}
						/>
					{:else if sequenceData}
						<!-- Show full control panel during playback -->
						<SequenceControlPanel
							isPlaying={animState.isPlaying}
							speed={animState.speed}
							currentBeat={animState.currentBeat}
							totalBeats={animState.totalBeats}
							onPlayPause={() => animationController?.togglePlayPause()}
							onReset={() => animationController?.resetAnimation()}
							onSpeedChange={(value) => animationController?.changeSpeed(value)}
						/>
					{/if}
				{/if}

				<!-- Beat Viewer for individual beat inspection -->
				<BeatViewer {sequenceData} onBeatSelect={handleBeatSelect} />
			</div>
		{:else}
			<WelcomeSection />
			
			<!-- Quick test buttons for debugging -->
			<div class="test-section">
				<h3>Quick Test Sequences</h3>
				<div class="test-buttons">
					<button 
						class="test-button" 
						onclick={() => loadTestSequence('ALFBBLFA')}
					>
						Load ALFBBLFA
					</button>
					<button 
						class="test-button" 
						onclick={() => loadTestSequence('ABC')}
					>
						Load ABC
					</button>
					<button 
						class="test-button" 
						onclick={() => loadTestSequence('BA')}
					>
						Load BA
					</button>
				</div>
				<p class="test-note">
					These buttons load hardcoded sequences to test the animation engine.
				</p>
			</div>
		{/if}
	</AppLayout>
</div>

<style>
	/* Component-specific styles only */

	/* Sidebar styles that are used in this component */
	.sidebar-header {
		padding: 1.5rem 1.5rem 1rem;
		border-bottom: 1px solid var(--color-border);
		display: flex;
		justify-content: space-between;
		align-items: center;
		flex-shrink: 0;
	}

	.sidebar-header h2 {
		margin: 0;
		font-size: 1.25rem;
		font-weight: 600;
		color: var(--color-text-primary);
	}

	.sidebar-content {
		flex: 1;
		overflow-y: auto;
		display: flex;
		flex-direction: column;
		min-height: 0;
	}

	.animator-section {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1.5rem;
		gap: 1rem; /* Reduced gap for more compact layout */
		width: 100%;
		box-sizing: border-box;
		overflow-y: auto;
	}

	.sequence-info {
		text-align: center;
		padding: 0.75rem;
		background: var(--color-surface);
		border-radius: 8px;
		border: 1px solid var(--color-border);
		transition: all 0.3s ease;
	}

	.sequence-info h3 {
		margin: 0 0 0.5rem;
		font-size: 1.25rem;
		color: var(--color-text-primary);
	}

	.sequence-info p {
		margin: 0;
		color: var(--color-text-secondary);
		font-style: italic;
	}

	/* Mobile responsive adjustments */
	/* Test section styles */
	.test-section {
	padding: 2rem;
	text-align: center;
	background: var(--color-surface);
			border-radius: 8px;
	border: 1px solid var(--color-border);
	margin: 1rem;
	}
		
	.test-section h3 {
	margin: 0 0 1rem;
	color: var(--color-text-primary);
	}
		
	.test-buttons {
	display: flex;
	gap: 1rem;
	justify-content: center;
	 flex-wrap: wrap;
			margin-bottom: 1rem;
		}
		
		.test-button {
			padding: 0.75rem 1.5rem;
			background: #3b82f6;
			color: white;
			border: none;
			border-radius: 6px;
			cursor: pointer;
			font-weight: 500;
			transition: background 0.2s ease;
		}
		
		.test-button:hover {
			background: #2563eb;
		}
		
		.test-note {
			margin: 0;
			color: var(--color-text-secondary);
			font-size: 0.875rem;
			font-style: italic;
		}

		@media (max-width: 768px) {
			.sidebar-header {
				padding: 0.75rem 1rem;
				min-height: auto;
			}

			.sidebar-header h2 {
				font-size: 1rem;
			}

			.sidebar-content {
				flex: 1;
				overflow: hidden;
			}

			.animator-section {
				padding: 1rem;
				gap: 1rem;
			}
			
			.test-buttons {
				flex-direction: column;
				align-items: center;
			}
		}
</style>
