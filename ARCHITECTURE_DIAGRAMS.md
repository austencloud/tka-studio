# TKA Studio - Architecture Diagrams & Data Flow

## 1. Application Module Structure

```
TKA Studio App
│
├── Create Module (Build sequences)
│   ├── Guided Tab (Sequential one-hand builder)
│   ├── Construct Tab (Beat-by-beat builder)
│   ├── Generate Tab (AI-powered generator)
│   └── Animator Sheet (Playback & visualization)
│
├── Explore Module (Discover sequences)
│   ├── Sequences Tab (Browse all)
│   ├── Collections Tab (Curated playlists)
│   └── Users Tab (Creator profiles)
│
├── Learn Module (Study & practice)
│   ├── Concepts Tab (Progressive lessons)
│   ├── Drills Tab (Flash card quizzes)
│   └── Read Tab (PDF flipbook)
│
├── Collect Module (My library)
│   ├── Gallery Section (My sequences)
│   ├── Achievements Section (Unlocks & progress)
│   └── Challenges Section (Daily quests)
│
└── Admin Module (System management)
    ├── Challenges (Manage daily challenges)
    ├── Analytics (View metrics)
    └── Users (Manage accounts)
```

---

## 2. Animation System Data Flow

```
User Action (Click Play Button)
    │
    ▼
ButtonPanel.svelte
    │ onPlayAnimation()
    ▼
CreateModule.handlePlayAnimation()
    │
    ├─► panelState.openAnimationPanel()
    │
    └─► AnimationCoordinator (watches panelState.isAnimationPanelOpen)
         │
         ├─ [Effect] Panel opens
         │    │
         │    ├─► sequenceService.getSequence(currentSequence)
         │    │
         │    └─► playbackController.initialize(sequence, panelState)
         │         │
         │         ├─► animationEngine.initializeWithDomainData(sequence)
         │         │    │
         │         │    ├─ Extract beats: sequence.beats[]
         │         │    ├─ Set totalBeats
         │         │    └─ Extract metadata: word, author
         │         │
         │         └─► loopabilityChecker.isSeamlesslyLoopable(sequence)
         │              │
         │              └─► Determine loop behavior
         │
         ├─ [Effect] Auto-start animation
         │    │
         │    └─► playbackController.togglePlayback()
         │         │
         │         └─► loopService.start(onAnimationUpdate, speed)
         │
         └─ AnimationPanel (presentation component)
              │
              ├─ Canvas: <AnimatorCanvas>
              │  │
              │  ├─ Load SVG images (blue, red, grid, letter)
              │  │
              │  └─ Render loop:
              │     │
              │     ├─ requestAnimationFrame
              │     │
              │     └─ canvasRenderer.renderScene(ctx, ...)
              │
              └─ Controls: <AnimationControls>
                 │
                 ├─ Speed slider → playbackController.setSpeed()
                 │
                 └─ Export button → gifExportOrchestrator


Animation Frame Update Loop
│
├─ AnimationLoopService.onFrame(deltaTime)
│   │
│   └─► AnimationPlaybackController.onAnimationUpdate(deltaTime)
│        │
│        ├─ Calculate newBeat = currentBeat + (deltaTime * speed)
│        │
│        ├─► animationEngine.calculateState(newBeat)
│        │    │
│        │    ├─ beatCalculator.calculateBeatState(newBeat, beats, totalBeats)
│        │    │   │
│        │    │   └─ Returns: currentBeatIndex, beatProgress (0.0-1.0)
│        │    │
│        │    └─ propInterpolator.interpolatePropAngles(currentBeat, progress)
│        │         │
│        │         ├─ startAngles = beats[currentBeatIndex].startAngles
│        │         ├─ endAngles = beats[currentBeatIndex].endAngles
│        │         │
│        │         └─ Interpolate: angle = lerp(start, end, progress)
│        │
│        └─► animationStateService.updatePropStates(interpolatedAngles)
│             │
│             └─► panelState.setPropStates(blueProp, redProp)
│
└─► CanvasRenderer.renderScene(ctx, canvasSize, props, images)
    │
    ├─ Clear canvas (white background)
    │
    ├─ Draw grid image
    │
    ├─ Draw blue prop:
    │  │ x = centerX + cos(blueProp.centerPathAngle) * radius
    │  │ y = centerY + sin(blueProp.centerPathAngle) * radius
    │  │
    │  └─ Rotate by blueProp.staffRotationAngle
    │
    ├─ Draw red prop (same calculations)
    │
    └─ [During GIF export] Draw letter glyph overlay
```

---

## 3. State Management Architecture

```
CreateModuleState (Composition Root)
│
├─ SequenceState (Orchestrator)
│  │
│  ├─ CoreState
│  │  ├─ currentSequence: SequenceData
│  │  ├─ sequences: SequenceData[]
│  │  ├─ isLoading: boolean
│  │  └─ error: string | null
│  │
│  ├─ SelectionState
│  │  ├─ selectedBeatNumber: number | null
│  │  ├─ selectedStartPosition: PictographData | null
│  │  ├─ hasStartPosition: boolean
│  │  ├─ selectedBeatNumbers: Set<number> (multi-select)
│  │  └─ isMultiSelectMode: boolean
│  │
│  ├─ ArrowState
│  │  ├─ arrowPositions: Map<string, ArrowPosition>
│  │  ├─ arrowPositioningInProgress: boolean
│  │  └─ arrowPositioningError: string | null
│  │
│  └─ AnimationState
│     ├─ removingBeatIndex: number | null
│     ├─ removingBeatIndices: Set<number>
│     └─ isClearing: boolean
│
├─ AnimationPanelState (Local to animator)
│  ├─ currentBeat: number
│  ├─ isPlaying: boolean
│  ├─ speed: number
│  ├─ shouldLoop: boolean
│  ├─ totalBeats: number
│  ├─ bluePropState: PropState
│  ├─ redPropState: PropState
│  ├─ loading: boolean
│  ├─ error: string | null
│  └─ sequenceData: SequenceData | null
│
├─ NavigationState (Global)
│  ├─ currentModule: ModuleId
│  ├─ activeTab: string
│  ├─ currentCreateMode: string
│  ├─ currentLearnMode: string
│  └─ lastTabByModule: Map<ModuleId, string>
│
├─ PanelCoordinationState
│  ├─ isAnimationPanelOpen: boolean
│  ├─ isEditPanelOpen: boolean
│  ├─ isSharePanelOpen: boolean
│  ├─ isSequenceActionsSheetOpen: boolean
│  ├─ combinedPanelHeight: number (tool + button panels)
│  └─ practiceBeatIndex: number | null
│
└─ UndoService (Global singleton)
   ├─ undoHistory: UndoEntry[]
   ├─ redoStack: UndoEntry[]
   └─ onChange: () => void (notify listeners)


Data Persistence Flow
│
User Changes
  │
  ├─► sequenceState.setCurrentSequence(newSequence)
  │
  ├─► [Debounce 500ms]
  │
  └─► sequenceState.saveSequenceDataOnly()
       │
       └─► SequencePersistenceService
            │
            ├─► IndexedDB: save(sequenceData)
            │
            └─► localStorage: save(activeTab, animation preferences)


On App Initialize
│
└─► CreateModule.onMount()
     │
     ├─► InitializationService.initialize()
     │
     ├─► sequenceState.initializeWithPersistence()
     │   │
     │   └─► SequencePersistenceService.loadCurrentState()
     │        │
     │        └─► [Restore sequence from IndexedDB]
     │
     ├─► navigationState reads from localStorage
     │
     └─► animationPanelState reads loop preference
```

---

## 4. Create Module Component Tree

```
CreateModule (Composition Root)
│ [Resolves DI, provides context, coordinates effects]
│
├─ CreationWelcomeScreen [SHOWN: empty workspace, no method selected]
│  │ [Gradient background, method selector buttons]
│  │
│  └─ CreationWelcomeCue
│     ├─ orientation: 'horizontal' | 'vertical' [based on layout]
│     └─ mood: 'default' | 'redo' | 'returning' | 'fresh'
│
├─ CreationWorkspaceArea [SHOWN: has sequence or method selected]
│  │
│  ├─ HandPathSettingsView [SHOWN ONLY: gestural mode pre-start]
│  │
│  └─ WorkspacePanel
│     │
│     ├─ SequenceDisplay
│     │  │
│     │  ├─ BeatGrid
│     │  │  │
│     │  │  ├─ BeatCell [for each beat]
│     │  │  │  │ [Shows pictograph thumbnail]
│     │  │  │  │ [Highlights on selection/animation]
│     │  │  │  │ [Fade-out animation on delete]
│     │  │  │  │
│     │  │  │  └─ Pictograph.svelte [SVG rendering]
│     │  │  │
│     │  │  └─ EmptyStartPositionPlaceholder [if no start]
│     │  │
│     │  └─ WordLabel [Progressive word building during animation]
│     │
│     ├─ SelectionToolbar [SHOWN: multi-select mode active]
│     │  │ [Selection count, Edit, Cancel buttons]
│     │  │
│     │  └─ Multi-select batch editing
│     │
│     └─ Toast [Validation/error messages]
│
├─ ButtonPanel
│  │
│  ├─ PlayButton → handlePlayAnimation()
│  ├─ ShareButton → handleOpenSharePanel()
│  ├─ SequenceActionsButton → handleOpenSequenceActions()
│  ├─ FilterButton → handleOpenFilterPanel()
│  ├─ ClearButton → handleClearSequence()
│  └─ UndoButton → CreateModuleState.undo()
│
├─ CreationToolPanelSlot
│  │
│  ├─ ConstructTabContent [SHOWN: construct tab]
│  │  │
│  │  ├─ StartPositionPicker
│  │  │  └─ [Grid with selectable positions]
│  │  │
│  │  └─ OptionPicker
│  │     │ [Shows available pictographs for next beat]
│  │     │ [Grouped by motion type]
│  │     │ [Filters based on current selection]
│  │     │
│  │     └─ [Animations on beat add/remove]
│  │
│  ├─ GenerateTabContent [SHOWN: generate tab]
│  │  │
│  │  └─ SequenceGenerator UI
│  │
│  └─ GuidedTabContent [SHOWN: guided tab]
│     │
│     └─ SequentialBuilder
│        │ [One-hand sequential flow]
│        │ [6 simple choices per hand]
│        │ [Step-by-step guidance]
│        │
│        └─ [Emits guidedModeHeaderText updates]
│
└─ Coordinators [Modals/Sheets below workspace]
   │
   ├─ EditCoordinator → EditSlidePanel
   │  │ [Slide panel from right with edit UI]
   │  │ [Edit start position or beat]
   │  │ [Auto-opens on beat selection]
   │  │
   │  └─ [Closes on blur or save]
   │
   ├─ ShareCoordinator → ShareDialog
   │  │ [Modal: export, share, save options]
   │  │
   │  └─ [Opens from share button]
   │
   ├─ AnimationCoordinator → AnimationPanel
   │  │ [Drawer sheet from bottom]
   │  │ [Full-screen animator with canvas]
   │  │ [Speed control, export GIF]
   │  │
   │  └─ [Opens from play button]
   │
   ├─ SequenceActionsCoordinator → SequenceActionsSheet
   │  │ [Drawer sheet from bottom]
   │  │ [Transformation actions: Mirror, Rotate, Color Swap]
   │  │ [Copy JSON for debugging]
   │  │
   │  └─ [Opens from sequence actions button]
   │
   ├─ CAPCoordinator
   │  │ [Generate CAP (Context-Aware Pictograph) mode]
   │  │
   │  └─ [Specialized generation flow]
   │
   └─ ConfirmationDialogCoordinator
      │ [Modals for critical actions]
      │ - Switch to Guided (clears sequence)
      │ - Exit Guided (abandon progress)
      │ - Clear sequence
      │
      └─ [Yes/No confirmations]
```

---

## 5. Animation Playback State Machine

```
IDLE
  │
  ├─ [Click Play Button]
  │  │
  │  ├─ panelState.openAnimationPanel()
  │  │
  │  └─► LOADING
  │      │
  │      ├─ [Load sequence data]
  │      ├─ [Load SVG images]
  │      ├─ [Initialize animation engine]
  │      │
  │      └─► READY
  │          │
  │          ├─ [currentBeat = 0]
  │          ├─ [isPlaying = false]
  │          │
  │          ├─ [Auto-start animation after delay]
  │          │
  │          └─► PLAYING
  │              │
  │              ├─ [RAF loop: onAnimationUpdate(deltaTime)]
  │              ├─ [Calculate currentBeat += (deltaTime * speed)]
  │              ├─ [Update prop angles via engine]
  │              ├─ [Render canvas on prop change]
  │              │
  │              ├─ [Speed change] → PLAYING (with new speed)
  │              │
  │              ├─ [Seek/Jump] → PLAYING (jump to beat)
  │              │
  │              ├─ [Pause] → PAUSED
  │              │  │
  │              │  └─ [Stop RAF loop]
  │              │
  │              └─ [currentBeat >= endBeat]
  │                  │
  │                  ├─ [if shouldLoop]
  │                  │  │
  │                  │  └─ [currentBeat = 0] → PLAYING (restart)
  │                  │
  │                  └─ [if not shouldLoop]
  │                     │
  │                     └─► FINISHED
  │                         │
  │                         └─ [Stop animation]
  │                             [Wait for user action]
  │
  ├─ [Close panel]
  │  │
  │  └─► DISPOSED
  │      │
  │      └─ [Cleanup: stop RAF, dispose engine, clear state]
  │
  └─ [Error loading sequence/images]
     │
     └─► ERROR
         │ [Display error message]
         │
         └─ [Close panel or retry]
```

---

## 6. Sequence Transformation Pipeline

```
Original Sequence
├─ beats: [
│   {blue: {location: 'east'}, red: {location: 'north'}},
│   {blue: {location: 'north'}, red: {location: 'west'}}
│ ]
├─ startPosition: {location: 'center'}
└─ gridMode: DIAMOND

User Action: Mirror Sequence
│
▼
SequenceTransformationService.mirrorSequence(sequence)
│
├─ Apply VERTICAL_MIRROR_LOCATION_MAP to each beat:
│  │ 'east' → 'west'
│  │ 'north' → 'north'
│  │ 'west' → 'east'
│
├─ Reverse rotation directions:
│  │ clockwise → counter-clockwise
│  │ counter-clockwise → clockwise
│  │ no-rotation → no-rotation
│
├─ Mirror start position location
│
└─ gridMode unchanged

Result Sequence (Mirrored)
├─ beats: [
│   {blue: {location: 'west'}, red: {location: 'north'}},
│   {blue: {location: 'north'}, red: {location: 'east'}}
│ ]
├─ startPosition: {location: 'center'} (unchanged)
└─ gridMode: DIAMOND


User Action: Rotate Sequence 90°
│
▼
SequenceTransformationService.rotateSequence(sequence, 90)
│
├─ Apply QUARTER_POSITION_MAP_CW:
│  │ Maps grid positions: north → east, east → south, south → west, west → north
│
├─ Apply LOCATION_MAP_CLOCKWISE:
│  │ Maps grid locations: center → center, north → east, northeast → southeast, etc.
│
├─ Toggle gridMode:
│  │ DIAMOND → BOX
│  │ BOX → DIAMOND
│
└─ [Return new sequence with rotated beats]

Result Sequence (Rotated)
├─ beats: [
│   {blue: {location: 'south'}, red: {location: 'east'}},
│   {blue: {location: 'east'}, red: {location: 'north'}}
│ ]
├─ gridMode: BOX (toggled from DIAMOND)
└─ startPosition: [rotated appropriately]


User Action: Swap Colors (Blue ↔ Red)
│
▼
SequenceTransformationService.swapColors(sequence)
│
├─ For each beat:
│  │
│  ├─ newBeats[i].motions[BLUE] ← oldBeats[i].motions[RED]
│  ├─ newBeats[i].motions[RED] ← oldBeats[i].motions[BLUE]
│  │
│  ├─ Update motion.color property to match new color
│  │
│  ├─ Swap reversal flags:
│  │  │ newBeats[i].blueReversal ← oldBeats[i].redReversal
│  │  │ newBeats[i].redReversal ← oldBeats[i].blueReversal
│  │
│  └─ Apply SWAPPED_POSITION_MAP to positions
│
└─ [Return new sequence with swapped colors]

Result Sequence (Colors Swapped)
├─ beats: [
│   {blue: [old red motion], red: [old blue motion]},
│   ...
│ ]
└─ [All color-dependent properties swapped]


All transformations
├─ Create new SequenceData (immutable)
├─ Preserve metadata (id, name, author)
└─ Update CreateModuleState.sequenceState.setCurrentSequence(newSequence)
   │
   └─ Trigger debounced persistence
```

---

## 7. Navigation & Tab Management

```
MainInterface.svelte (App Shell)
│
├─ TopBar (Module/Tab Navigation)
│  │
│  ├─ Module Selector
│  │  │ [Shows: Create, Explore, Learn, Collect, Admin]
│  │  │
│  │  └─ [Click] → navigationState.setCurrentModule(moduleId)
│  │
│  └─ Tab Selector
│     │ [Shows tabs for current module]
│     │
│     └─ [Click] → navigationState.setActiveTab(tabId)
│        │
│        └─ Effect in CreateModuleEffectCoordinator:
│           └─ Syncs navigationState.activeTab → CreateModuleState.activeSection
│
└─ Content Area (Module Content)
   │
   ├─ CreateModule (if currentModule === 'create')
   │  │
   │  ├─ [activeTab === 'guided']
   │  │  └─ GuidedTabContent
   │  │
   │  ├─ [activeTab === 'construct']
   │  │  └─ ConstructTabContent
   │  │
   │  └─ [activeTab === 'generate']
   │     └─ GenerateTabContent
   │
   ├─ ExploreModule (if currentModule === 'explore')
   │  │
   │  ├─ [activeTab === 'sequences']
   │  │  └─ SequencesBrowse
   │  │
   │  ├─ [activeTab === 'collections']
   │  │  └─ CollectionsBrowse
   │  │
   │  └─ [activeTab === 'users']
   │     └─ UsersBrowse
   │
   ├─ LearnModule (if currentModule === 'learn')
   │
   └─ CollectModule (if currentModule === 'collect')


Navigation State Persistence (localStorage)
│
├─ tka-current-module: 'create' | 'explore' | 'learn' | 'collect' | 'admin'
├─ tka-current-create-mode: 'guided' | 'construct' | 'generate'
├─ tka-current-learn-mode: 'concepts' | 'drills' | 'read'
├─ tka-active-tab: [current active tab id]
└─ tka-module-last-tabs: {
    'create': 'construct',
    'explore': 'sequences',
    'learn': 'concepts',
    'collect': 'gallery'
   }

On App Load
└─ navigationState reads localStorage
   ├─ Restores currentModule
   ├─ Restores activeTab
   └─ Restores per-module last tab memory
```

---

## 8. Service Dependency Graph

```
CreateModule (Composition Root)
│
├─ ICreateModuleInitializationService
│  │
│  ├─► ISequenceService
│  ├─► ISequencePersistenceService
│  ├─► IStartPositionService
│  ├─► ICreateModuleService
│  ├─► ILayoutService
│  ├─► INavigationSyncService
│  └─► IBeatOperationsService
│
├─ ICreateModuleHandlers
│  │
│  ├─► ISequenceService
│  ├─► IBeatOperationsService
│  └─► IShareService
│
├─ ICreateModuleEffectCoordinator
│  │
│  ├─► ILayoutService
│  ├─► INavigationSyncService
│  └─► [Context/State]
│
├─ IAnimationPlaybackController
│  │
│  ├─► ISequenceAnimationOrchestrator
│  ├─► IAnimationLoopService
│  └─► ISequenceLoopabilityChecker
│
├─ ISequenceAnimationOrchestrator
│  │
│  ├─► IAnimationStateManager
│  ├─► IBeatCalculator
│  └─► IPropInterpolator
│
├─ ICanvasRenderer
│  │
│  ├─► ISVGGenerator
│  └─► [Canvas context]
│
├─ IGifExportOrchestrator
│  │
│  ├─► IAnimationPlaybackController
│  ├─► ICanvasRenderer
│  └─► [GIF encoding library]
│
└─ ISequenceTransformationService
   ├─► [Constants: position/location maps]
   └─► [Transformation algorithms]
```

---

## 9. Beat Cell Lifecycle

```
BeatCell Component Props
├─ beat: BeatData
├─ beatNumber: number (1-indexed)
├─ isSelected: boolean
├─ isRemoving: boolean
├─ isPractice: boolean
├─ isMultiSelectMode: boolean
├─ isMultiSelected: boolean
├─ onBeatSelected?: (beatNumber) => void
├─ onBeatDelete?: (beatNumber) => void
└─ onBeatLongPress?: (beatNumber) => void

BeatCell Render States
│
├─ NORMAL STATE
│  │ [Displays pictograph thumbnail]
│  │ [Opaque background]
│  │ [Beat number label]
│  │
│  └─ [Hover] → Slightly elevated shadow
│
├─ SELECTED STATE
│  │ [Highlighted border/background]
│  │ [Visual indication of selection]
│  │
│  └─ [Click elsewhere] → NORMAL STATE
│
├─ REMOVING STATE (fade-out)
│  │ [Triggered by animationState.startRemovingBeats()]
│  │ [CSS fade-out animation (300ms)]
│  │ [Opacity: 1.0 → 0.0]
│  │
│  └─ [Animation ends] → Remove from DOM
│
├─ MULTI-SELECT STATE
│  │ [Checkbox visible]
│  │ [Can toggle multiple beats]
│  │ [Toolbar shows selection count]
│  │
│  └─ [Click cancel] → EXIT MULTI-SELECT
│
├─ PRACTICE STATE
│  │ [Highlighted to show practice beat]
│  │ [User studying this beat]
│  │
│  └─ [User moves on] → NORMAL STATE
│
└─ ANIMATING STATE
   │ [Highlighted during animation playback]
   │ [Shows current beat during sequence play]
   │
   └─ [Animation ends/paused] → NORMAL STATE

User Interactions
│
├─ [Single Click]
│  │ [Not in multi-select mode]
│  │ → onBeatSelected(beatNumber)
│  │   → sequenceState.selectBeat(beatNumber)
│  │   → Opens edit panel (via effect)
│
├─ [Long Press (0.5s)]
│  │ [Enter multi-select mode]
│  │ → onBeatLongPress(beatNumber)
│  │ → sequenceState.enterMultiSelectMode(beatNumber)
│  │ → Show selection toolbar
│
├─ [Keyboard Delete]
│  │ [While selected]
│  │ → onBeatDelete(beatNumber)
│  │ → beatOperationsService.removeBeat(beatIndex)
│  │ → Start remove animation
│  │ → Remove from sequence
│
└─ [Right-Click Menu]
    [Context menu options]
    ├─ Edit
    ├─ Delete
    ├─ Duplicate
    └─ [Color] [Reversal] toggles
```

---

## 10. Effect Coordination Flow

```
CreateModuleEffectCoordinator.setupEffects()
│
├─ EFFECT 1: Navigation Sync
│  │ Watches: navigationState.activeTab, CreateModuleState.activeSection
│  │ Syncs tab changes bidirectionally
│  │ Prevents circular updates via isNavigatingBack & isUpdatingFromToggle
│  │
│  └─ Updates: CreateModuleState.activeSection ↔ navigationState.activeTab
│
├─ EFFECT 2: Layout Management
│  │ Watches: window resize, layout service changes
│  │ Detects: side-by-side vs. stacked layout
│  │ Calls: onLayoutChange(shouldUseSideBySideLayout)
│  │
│  └─ Updates: UI layout from flex-direction: column → row
│
├─ EFFECT 3: Auto-Edit Panel
│  │ Watches: sequenceState.selectedBeatNumber
│  │ When beat selected: Opens EditCoordinator panel
│  │ When selection cleared: Closes panel
│  │
│  └─ Manages: panelState.isEditPanelOpen
│
├─ EFFECT 4: Single-Beat Edit Mode
│  │ Watches: activeSection, constructTabState.singleBeatEditMode
│  │ When single-beat edit triggered: Opens panel for that beat
│  │ Triggers animation highlighting
│  │
│  └─ Manages: panelState.isSingleBeatEditMode
│
├─ EFFECT 5: PWA Engagement
│  │ Watches: User interactions (beat added/removed)
│  │ Tracks: Engagement metrics
│  │ Triggers: PWA install prompts
│  │
│  └─ External: Fire analytics events
│
├─ EFFECT 6: Current Word Display
│  │ Watches: sequenceState.currentSequence.beats
│  │ Calls: onCurrentWordChange(word) to parent
│  │ Updates: Top bar word label
│  │
│  └─ External: Parent component updates header
│
└─ EFFECT 7: Panel Height Tracking
   │ Watches: toolPanelElement, buttonPanelElement sizes
   │ Calculates: combinedPanelHeight
   │ Updates: panelState.combinedPanelHeight
   │
   └─ Manages: Animation panel sizing to not overlap panels
```

---

## 11. GIF Export Pipeline

```
User clicks "Export GIF"
│
▼
AnimationCoordinator.handleExportGif()
│
├─► Find canvas element
│
├─► gifExportOrchestrator.executeExport(
│     canvas,
│     playbackController,
│     animationPanelState,
│     (progress) => { exportProgress = progress }
│   )
│
└─► GifExportOrchestrator
    │
    ├─ Determine GIF duration from animation
    │  │ totalFrames = totalBeats * framesPerBeat
    │  │ frameDelay = 1000 / 60fps
    │
    ├─ Initialize GIF encoder library
    │
    ├─ For each frame:
    │  │
    │  ├─ playbackController.jumpToBeat(currentBeat)
    │  │  │
    │  │  ├─ animationEngine.calculateState(beat)
    │  │  └─ animationStateService.updatePropStates()
    │  │
    │  ├─ canvasRenderer.renderScene(ctx, ...) [renders frame to canvas]
    │  │
    │  ├─ canvasRenderer.renderLetterToCanvas() [overlay letter]
    │  │
    │  ├─ canvas.toDataURL('image/png') [capture frame]
    │  │
    │  ├─ gifEncoder.addFrame(frameData)
    │  │
    │  └─ Update progress: (currentFrame / totalFrames)
    │
    ├─ gifEncoder.render() [encode to GIF binary]
    │
    ├─ Create blob from GIF binary
    │
    ├─ generateFilename(sequence.word, sequence.id)
    │
    └─ Trigger browser download
       │
       ├─ Create <a> element with blob URL
       ├─ Set download attribute to filename
       └─ Programmatically click to download
```

---

## Summary Connections

| Component | Depends On | Updates |
|-----------|-----------|---------|
| AnimationCoordinator | CreateModuleContext | AnimationPanelState |
| AnimationPanel | AnimationPanelState props | onClose, onSpeedChange, onExport |
| AnimatorCanvas | AnimationPanelState | needsRender flag |
| AnimationPlaybackController | SequenceAnimationOrchestrator | AnimationPanelState.currentBeat |
| SequenceAnimationOrchestrator | BeatCalculator, PropInterpolator | AnimationStateService |
| CanvasRenderer | PropState, Images | Canvas pixels |
| CreateModule | services from DI | CreateModuleContext |
| SequenceState | SequenceService | currentSequence, beats |
| BeatGrid | SequenceState | Rerender on sequence/selection change |
| EditCoordinator | SequenceState | Opens/closes panel |
| SequenceActionsCoordinator | SequenceTransformationService | Updates currentSequence |

---

**Generated:** 2025-11-05
**Version:** 1.0 - Complete Architecture Diagrams
