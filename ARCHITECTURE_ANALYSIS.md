# TKA Studio - Comprehensive Architecture Analysis

## Executive Summary

TKA Studio is a Svelte 5-based web application for creating, exploring, and learning TKA (Tablao Kinetic Art) pictograph sequences. The architecture emphasizes:

- **Modular Composition**: Seven main modules (Create, Explore, Collect, Learn, Admin, Write, Word-Card) with clear separation of concerns
- **Service-Oriented Design**: Heavy use of dependency injection (Inversify) with contract-based interfaces
- **Reactive State Management**: Svelte 5 runes ($state, $derived, $effect) for fine-grained reactivity
- **Layered Architecture**: Presentation → Coordinator → Service → Domain layers
- **Animation-First Approach**: Dedicated animation system with playback, rendering, and GIF export

---

## 1. CURRENT ANIMATOR IMPLEMENTATION

### 1.1 Architecture Overview

The animator is a **drawer-based sheet panel** (not a modal) that slides up from the bottom of the screen. It's tightly integrated with the Create module's sequence display system.

**Key Files:**

- Presentation: `C:\_TKA-STUDIO/src/lib/modules/create/animate/components/AnimationPanel.svelte`
- Coordinator: `C:\_TKA-STUDIO/src/lib/modules/create/shared/components/coordinators/AnimationCoordinator.svelte`
- Canvas Renderer: `C:\_TKA-STUDIO/src/lib/modules/create/animate/components/AnimatorCanvas.svelte`

### 1.2 How It Currently Animates Sequences

**Data Flow:**

```
AnimationCoordinator (orchestration)
  ↓
AnimationPanelState (reactive state)
  ↓
AnimationPlaybackController (playback control)
  ├→ SequenceAnimationOrchestrator (beat calculation)
  ├→ AnimationLoopService (timing/frame loop)
  └→ CanvasRenderer (rendering)
      ├→ SVGGenerator (prop SVG generation)
      └→ AnimatorCanvas (HTML canvas)
```

**Step-by-Step Flow:**

1. **Panel Opens**: User clicks "Play" button → AnimationCoordinator sets `panelState.isAnimationPanelOpen = true`
2. **Sequence Loading**: `AnimationCoordinator` loads the current sequence via `loadSequenceForAnimation()`
3. **Playback Initialization**: `AnimationPlaybackController.initialize()` sets up:
   - SequenceAnimationOrchestrator with domain data
   - AnimationPanelState with beat count and metadata
   - Checks if sequence is "seamlessly loopable" via SequenceLoopabilityChecker
4. **Animation Playback**:
   - User can toggle play/pause via controls
   - `AnimationLoopService` provides frame-by-frame delta time (requestAnimationFrame-based)
   - `AnimationPlaybackController.onAnimationUpdate()` calculates current beat (with speed multiplier)
   - `SequenceAnimationOrchestrator.calculateState()` interpolates prop positions
5. **Canvas Rendering**:
   - `CanvasRenderer.renderScene()` draws: grid → blue prop → red prop
   - Props are rendered using transformed SVG images
   - Canvas updates via reactive `needsRender` flag in `AnimatorCanvas`

### 1.3 Workspace Dependencies

**What it depends on from the workspace:**

```typescript
// From CreateModuleState
- sequenceState.currentSequence: SequenceData
  └─ beats: BeatData[]
  └─ startPosition: BeatData (optional)
  └─ gridMode: GridMode

// From AnimationPanelState (local coordinator state)
- currentBeat: number (0 to totalBeats)
- isPlaying: boolean
- speed: number (0.25 to 2.0)
- shouldLoop: boolean
- bluePropState: PropState
- redPropState: PropState
```

**No mutable dependencies** - the animator reads the sequence once on load, then only modifies its own animation state.

### 1.4 How It's Triggered/Opened

**Trigger Points:**

1. **Play Button**: `ButtonPanel.svelte` → `CreateModule.handlePlayAnimation()` → `handlers.handlePlayAnimation(panelState)`
2. **Handler**: Sets `panelState.isAnimationPanelOpen = true`
3. **Coordinator Effect**: `AnimationCoordinator` watches `panelState.isAnimationPanelOpen`:
   - When true: Loads sequence and auto-starts animation
   - When false: Disposes playback controller

**State Location:** `panelState.isAnimationPanelOpen` (PanelCoordinationState)

---

## 2. NAVIGATION STRUCTURE

### 2.1 Module System

**Primary Modules** (isMain: true):

- `create` - Construct, Generate, Guided modes for building sequences
- `explore` - Browse, discover sequences from the community
- `learn` - Study concepts, practice drills, read flipbooks
- `collect` - Personal gallery, achievements, challenges

**Secondary Modules**:

- `admin` - System management (hidden from non-admins)

**Legacy Modules** (not in use):

- `write`, `word-card` - Archived

**Navigation State:**

```typescript
// File: C:\_TKA-STUDIO/src/lib/shared/navigation/state/navigation-state.svelte.ts
navigationState.currentModule: ModuleId  // 'create', 'explore', 'learn', 'collect', 'admin'
navigationState.activeTab: string         // Tab within current module ('construct', 'generate', 'guided', etc.)
navigationState.lastTabByModule: Map     // Remember last active tab per module
```

### 2.2 Create Module Tabs

**Three Creation Methods** (mutually exclusive):

| Tab      | ID          | Purpose                                               | Icon       |
| -------- | ----------- | ----------------------------------------------------- | ---------- |
| Guided   | `guided`    | Build sequences one hand at a time (6 simple choices) | compass    |
| Standard | `construct` | Create step-by-step with all options                  | hammer     |
| Generate | `generate`  | Auto-create sequences with AI                         | magic wand |

**Persistence:**

- Last selected tab saved to `localStorage` as `tka-current-create-mode`
- Session flag tracks creation method selection via `CreationMethodPersistenceService`

### 2.3 Navigation Routing

**Architecture:**

- **Not file-based routing** - uses manual navigation state management
- **SvelteKit routes** are mostly placeholders for pages (Create, Explore, Learn, Collect, Admin)
- **Within-module navigation** is state-based (not URL-based)

**How Tab Switching Works:**

```typescript
// User clicks "Generate" tab
navigationState.setActiveTab('generate')
  ↓
CreateModule watches activeTab (via effect in CreateModuleEffectCoordinator)
  ↓
setactiveToolPanel('generate') called on CreateModuleState
  ↓
UI switches to GenerateTabContent component
```

**Effect Coordination** (CreateModuleEffectCoordinator):

- Syncs `navigationState.activeTab` with `CreateModuleState.activeSection`
- Prevents circular updates via `isNavigatingBack` and `isUpdatingFromToggle` flags
- Tracks navigation history for back button support

### 2.4 Submodule Organization

#### Create Module Structure

```
create/
├── animate/           # Animation playback system
│   ├── components/    # AnimationPanel, AnimatorCanvas
│   ├── services/      # PlaybackController, SequenceAnimationOrchestrator
│   ├── domain/        # Animation models, math constants
│   └── state/         # AnimationPanelState
├── construct/         # Standard beat-by-beat building
│   ├── option-picker/ # Select pictographs for beats
│   ├── sequential-builder/ # Guided mode builder
│   └── start-position-picker/ # Select starting position
├── generate/          # AI-powered sequence generation
├── shared/            # CreateModule composition root + coordinators
│   ├── components/    # CreateModule.svelte, coordinators
│   ├── services/      # CreateModuleHandlers, SequenceService, etc.
│   └── state/         # CreateModuleState, SequenceState
└── workspace-panel/   # Workspace display
    ├── sequence-display/ # BeatGrid, SequenceDisplay
    └── shared/        # ButtonPanel, action sheets
```

#### Explore Module Structure

```
explore/
├── display/           # Sequence browsing and display
│   ├── components/    # ExploreGrid, ExploreThumbnail
├── collections/       # Curated collections/playlists
├── filtering/         # Search and filter UI
├── navigation/        # Module navigation
└── spotlight/         # Featured sequences
```

#### Collect Module Structure

```
collect/
├── components/
│   ├── GallerySection.svelte     # My saved sequences
│   ├── AchievementsSection.svelte # Progress & unlocks
│   └── ChallengesSection.svelte    # Quests & daily challenges
```

---

## 3. SEQUENCE REFLECTOR / TRANSFORMATION SYSTEM

### 3.1 Overview

There is **no component called "SequenceReflector"**, but there is a **SequenceTransformationService** that handles sequence transformations.

**File:** `C:\_TKA-STUDIO/src/lib/modules/create/shared/services/implementations/SequenceTransformationService.ts`

### 3.2 How It Works

The `SequenceTransformationService` provides pure transformation functions that create new sequences without mutating the original:

**Available Operations:**

1. **Mirror Sequence** - Flip horizontally
   - Maps all positions using `VERTICAL_MIRROR_POSITION_MAP`
   - Maps all locations (flips east/west) using `VERTICAL_MIRROR_LOCATION_MAP`
   - Reverses rotation directions (clockwise ↔ counter-clockwise)

2. **Rotate Sequence** - 90° clockwise
   - Maps positions using `QUARTER_POSITION_MAP_CW`
   - Maps locations using `LOCATION_MAP_CLOCKWISE`
   - Toggles grid mode (DIAMOND ↔ BOX)

3. **Swap Colors** - Blue ↔ Red
   - Swaps entire motion data between colors
   - Swaps reversal states
   - Updates positions based on swapped locations

4. **Reverse Beat Order** - Reverse sequence direction
5. **Duplicate Sequence** - Clone with new IDs

### 3.3 Data Structures

**Transformation Maps** (constants in `C:\_TKA-STUDIO/src/lib/modules/create/generate/circular/domain/constants`):

```typescript
VERTICAL_MIRROR_POSITION_MAP: Map<GridPosition, GridPosition>;
VERTICAL_MIRROR_LOCATION_MAP: Map<GridLocation, GridLocation>;
QUARTER_POSITION_MAP_CW: Map<GridPosition, GridPosition>;
LOCATION_MAP_CLOCKWISE: Map<GridLocation, GridLocation>;
SWAPPED_POSITION_MAP: Map<GridPosition, GridPosition>;
```

### 3.4 Integration Points

**SequenceActionsCoordinator** handles user interactions:

- File: `C:\_TKA-STUDIO/src/lib/modules/create/shared/components/coordinators/SequenceActionsCoordinator.svelte`
- Coordinator receives transformation requests from SequenceActionsSheet
- Calls `transformationService.mirrorSequence()`, `.rotateSequence()`, etc.
- Updates `CreateModuleState.sequenceState.setCurrentSequence()` with result
- Changes are persisted automatically via debounced save

---

## 4. CANVAS/RENDERING ARCHITECTURE

### 4.1 Canvas Rendering Pipeline

**Components:**

1. **AnimatorCanvas.svelte** - Canvas host and image loading
   - Manages canvas element and 2D context
   - Loads SVG images asynchronously
   - Orchestrates render loop via requestAnimationFrame
   - Implements container query-based responsive sizing

2. **CanvasRenderer Service** - Low-level rendering
   - Pure rendering logic (no state mutation)
   - `renderScene()` - draws grid, props to canvas
   - `renderLetterToCanvas()` - overlays glyph during GIF export
   - Uses exact positioning from standalone_animator.html

3. **SVGGenerator Service** - Prop SVG generation
   - `generateBluePropSvg()` - creates blue prop SVG
   - `generateRedPropSvg()` - creates red prop SVG
   - `generateGridSvg()` - creates grid SVG
   - Respects current prop type (staff, ...)

**Rendering Pipeline:**

```
PropState (centerPathAngle, staffRotationAngle, x?, y?)
  ↓
CanvasRenderer.renderScene()
  ├─ drawGrid() → Grid SVG image at (0,0)
  ├─ drawStaff() → Blue prop rotated/positioned
  └─ drawStaff() → Red prop rotated/positioned
```

### 4.2 PropState Model

```typescript
interface PropState {
  centerPathAngle: number; // Radians, position on circle
  staffRotationAngle: number; // Radians, rotation of prop itself
  x?: number; // Optional: Cartesian x (dash motions)
  y?: number; // Optional: Cartesian y (dash motions)
}
```

**Coordinate Systems:**

- **Polar**: centerPathAngle positions prop on circle (8 main positions)
- **Cartesian**: x,y used only for dash motions (straight-line movements)
- **Rotation**: staffRotationAngle independent of position

### 4.3 Pictograph Display on Canvas

**Letter Overlay System:**

```typescript
// During animation, currentLetter is derived from:
if (currentBeat === 0 && !isPlaying)
  → sequence.startPosition.letter
else if (currentBeat > 0 && beats exist)
  → beats[floor(currentBeat)].letter
```

- Letters are fetched from `getLetterImagePath(letter)`
- Rendered to canvas via `CanvasRenderer.renderLetterToCanvas()`
- Positioned in bottom-left corner (x=50, y=800 in 950px viewBox)

### 4.4 Multiple Canvas Support

**Current State:**

- Only **one canvas** in AnimatorCanvas
- No split-view or multi-canvas rendering yet

**Extensibility:**

- Canvas size is responsive via CSS container queries
- Could render multiple prop types simultaneously with additional canvas elements
- GIF export already uses canvas.toDataURL() → could generate multiple GIFs

---

## 5. SEQUENCE DATA FLOW

### 5.1 Data Model

**SequenceData** (immutable):

```typescript
interface SequenceData {
  id: string;
  name: string;
  word: string;
  beats: readonly BeatData[];
  startPosition?: BeatData;
  gridMode?: GridMode;
  propType?: PropType;
  isFavorite: boolean;
  isCircular: boolean;
  tags: readonly string[];
  metadata: Record<string, unknown>;
}
```

**BeatData** (one per beat):

```typescript
interface BeatData {
  beatNumber: number;
  duration: number;
  startPosition?: GridPosition;
  endPosition?: GridPosition;
  letter?: Letter;
  motions: Record<MotionColor, MotionData>;
  blueReversal: boolean;
  redReversal: boolean;
  isBlank: boolean;
  pictographData?: PictographData;
}
```

### 5.2 Sequence Storage and Passing

**Storage Locations:**

1. **Working Sequence** (in-memory during session):
   - Stored in `CreateModuleState.sequenceState.currentSequence`
   - Reactively bound to all child components
   - Auto-persists every 500ms via debounced save

2. **Persisted Sequence** (IndexedDB/localStorage):
   - Managed by `SequencePersistenceService`
   - Restored on app load via `initializeWithPersistence()`
   - Saves via `saveCurrentState(activeBuildSection)`

3. **Selected Sequence** (Explore module):
   - Loaded on-demand from database
   - Read-only for browsing/playing
   - Can be copied/exported to Create module

### 5.3 Workspace Sequence vs. Saved Sequences

**Workspace Sequence** (current working):

- Lives in `CreateModuleState.sequenceState.currentSequence`
- Modified by beat operations, transformations
- Persisted incrementally (debounced)
- Only **one** active workspace sequence at a time

**Saved Sequences** (history/library):

- Stored separately in persistence layer
- Listed in Explore module
- Can be loaded into workspace
- Users can manage multiple saved versions

### 5.4 Collections/Explore Access

**How Explore Accesses Sequences:**

```
ExploreGrid (displays thumbnails)
  ↓
ExploreThumbnail (individual card)
  ↓
SequenceDisplayPanel (preview on click)
  ↓
ISequenceService.getSequence(id) - loads full sequence data
```

**No Direct Coupling:**

- Explore doesn't know about Create module state
- Uses service layer to load sequences
- Displays are read-only (no editing)

**Collections** (curated playlists):

- Reference multiple sequences
- Managed in separate collection storage
- Can be filtered/browsed independently

---

## 6. BEAT GRID AND WORKSPACE

### 6.1 Beat Grid Component

**File:** `C:\_TKA-STUDIO/src/lib/modules/create/workspace-panel/sequence-display/components/BeatGrid.svelte`

**Responsibilities:**

- Displays sequence as grid of BeatCell components
- Manages visual selection, multi-select, animation states
- Handles user interactions (click, long-press, keyboard)
- Renders start position placeholder at beginning

**Props:**

```typescript
beats: BeatData[]
startPosition?: BeatData
selectedBeatNumber?: number | null
practiceBeatNumber?: number | null
removingBeatIndex?: number
removingBeatIndices?: Set<number>
isClearing?: boolean
isMultiSelectMode?: boolean
selectedBeatNumbers?: Set<number>
onBeatClick, onStartClick, onBeatDelete, onBeatLongPress
```

### 6.2 Workspace State

**Workspace Panel** orchestrates:

- SequenceDisplay (beat grid + word label)
- SelectionToolbar (multi-select mode controls)
- Multi-select mode state management

**Non-Modal Integration:**

- Workspace is **always visible** (not a modal)
- Animator slides up on top of it
- No focus-trapping or backdrop interaction blocking

### 6.3 Beat Grid Coupling

**Tight Coupling to Create Module:**

- BeatGrid tightly depends on SequenceState
- Changes to selection immediately propagate
- No abstraction layer between grid and state

**Animation States:**

- `animatingBeatNumber` - highlights current beat during playback
- `removingBeatIndex` - fade-out animation when deleting
- `isClearing` - full grid fade during sequence clear

**Multi-Select Mode:**

- Entered via long-press on beat
- Selection toolbar appears below grid
- Can batch-edit multiple beats
- Can cancel to exit mode

---

## 7. KEY ARCHITECTURAL PATTERNS

### 7.1 Composition Root Pattern

**CreateModule.svelte** is the composition root:

- Resolves all services via DI container
- Provides CreateModuleContext to descendants
- Coordinates all effects via CreateModuleEffectCoordinator
- Orchestrates panel coordination (edit, share, animation, etc.)

### 7.2 Coordinator Pattern

**Coordinators** manage cross-cutting concerns:

- `AnimationCoordinator` - animation panel lifecycle
- `EditCoordinator` - edit slide panel
- `ShareCoordinator` - share dialog
- `SequenceActionsCoordinator` - transform actions
- `ConfirmationDialogCoordinator` - confirmations
- `CAPCoordinator` - generate CAP mode

**Pattern:**

```svelte
<!-- Coordinator uses context to access state/services -->
<script>
  const ctx = getCreateModuleContext();
  // ... handle business logic
</script>

<!-- Presentation component receives props only -->
<PresentationComponent {prop1} {prop2} {onEvent} />
```

### 7.3 State Orchestrator Pattern

**SequenceStateOrchestrator** composes multiple sub-states:

- CoreState (sequences, current sequence)
- SelectionState (beat selection, start position)
- ArrowState (animation arrows)
- AnimationState (removal animations)

**Unified Public API** delegates to sub-states internally.

### 7.4 Service Layer Architecture

**Three-Layer Model:**

1. **Presentation Layer** - Svelte components
   - No business logic
   - Reactive data via props
   - Events to parent

2. **Coordinator Layer** - Service resolution, effect management
   - Resolves services from DI
   - Manages component lifecycle
   - Delegates to services

3. **Service Layer** - Application logic
   - DI-injectable via Inversify
   - Contract-based interfaces
   - Pure functions, no mutations

4. **Domain Layer** - Business rules
   - Pure data transformations
   - Math calculations
   - No side effects

---

## 8. KEY SERVICES

### Animation Services

| Service                          | Purpose                         | File                               |
| -------------------------------- | ------------------------------- | ---------------------------------- |
| `IAnimationPlaybackController`   | Orchestrate playback lifecycle  | `AnimationPlaybackController.ts`   |
| `ISequenceAnimationOrchestrator` | Calculate animation frame state | `SequenceAnimationOrchestrator.ts` |
| `IAnimationLoopService`          | RAF-based frame timing          | `AnimationLoopService.ts`          |
| `ICanvasRenderer`                | Low-level canvas drawing        | `CanvasRenderer.ts`                |
| `ISVGGenerator`                  | Generate prop/grid SVGs         | `SVGGenerator.ts`                  |
| `ISequenceLoopabilityChecker`    | Detect seamless looping         | `SequenceLoopabilityChecker.ts`    |

### Sequence Services

| Service                          | Purpose                                |
| -------------------------------- | -------------------------------------- |
| `ISequenceService`               | CRUD operations, service layer         |
| `ISequencePersistenceService`    | IndexedDB storage/retrieval            |
| `ISequenceTransformationService` | Mirror, rotate, swap, reverse          |
| `ISequenceValidationService`     | Validate beat data                     |
| `ISequenceStatisticsService`     | Calculate stats (duration, complexity) |
| `ISequenceAnalysisService`       | Analyze motion patterns                |

### Create Module Services

| Service                              | Purpose                     |
| ------------------------------------ | --------------------------- |
| `ICreateModuleHandlers`              | Event handler delegation    |
| `ICreateModuleInitializationService` | Bootstrap composition root  |
| `ICreateModuleEffectCoordinator`     | Manage all reactive effects |
| `IResponsiveLayoutService`           | Detect layout mode changes  |
| `INavigationSyncService`             | Sync navigation state       |

---

## 9. DATA PERSISTENCE ARCHITECTURE

### 9.1 Storage Layers

```
User Interactions
  ↓
Svelte State ($state runes)
  ↓
(Debounced 500ms)
  ↓
SequencePersistenceService
  ↓
IndexedDB / localStorage
```

### 9.2 Persistence Flow

**Save:**

1. User makes change (add beat, edit start position, etc.)
2. State updated in SequenceState
3. `saveSequenceDataOnly()` queued via debounce
4. Service saves to `IPersistenceService`
5. Persisted to browser storage

**Load:**

1. App initializes
2. `CreateModule.onMount()` → `CreateModuleInitializationService.initialize()`
3. Calls `sequenceState.initializeWithPersistence()`
4. Loads from storage via persistence service
5. Restores working sequence

**Undo/Redo:**

- Managed by `IUndoService`
- Snapshots captured before destructive operations
- Stored separately from main sequence persistence

---

## 10. EXTENDING ANIMATION FUNCTIONALITY - RECOMMENDATIONS

### 10.1 Current Limitations

1. **Single Canvas Only** - No multi-canvas rendering
2. **Fixed Canvas Position** - Always drawer at bottom
3. **Limited Animation Parameters** - Speed, loop, start/stop only
4. **No Branching Paths** - Always linear playback
5. **No Frame-by-Frame Editing** - Animation is read-only
6. **No Keyframe Control** - Can't pause on specific beats mid-beat
7. **No Layer Visualization** - Only shows final prop positions
8. **No Motion Trails** - No path visualization

### 10.2 Architectural Extension Points

**To add new animation features:**

1. **New Animation Modes** - Add to AnimationPanelState:

   ```typescript
   enum AnimationMode {
     NORMAL = "normal",
     SLOWMO = "slowmo",
     REWIND = "rewind",
     FRAME_BY_FRAME = "frame-by-frame",
   }
   ```

2. **Multiple Canvas Panels** - Extend AnimationCoordinator:

   ```typescript
   // Add canvas slots for:
   // - Full animation
   // - Split-screen (left/right props)
   // - Top-down view
   // - Trail visualization
   ```

3. **Playback Presets** - Extend AnimationPlaybackController:

   ```typescript
   interface PlaybackPreset {
     speed: number;
     startBeat: number;
     endBeat: number;
     loop: boolean;
   }
   ```

4. **Motion Visualization** - Extend CanvasRenderer:

   ```typescript
   renderMotionTrail(ctx, beat1, beat2);
   renderVelocityVector(ctx, beat);
   renderAccelerationArrows(ctx, beat);
   ```

5. **Keyframe Editing** - New coordinator:
   ```typescript
   AnimationKeyframeEditor
   - Select beat ranges
   - Adjust individual prop angles
   - Live preview changes
   - Save as preset
   ```

### 10.3 Recommended New Components

**File Structure for Animation Enhancements:**

```
animate/
├── components/
│   ├── AnimationPanel.svelte (existing)
│   ├── AnimationModeSelector.svelte (NEW)
│   ├── AnimationPresetManager.svelte (NEW)
│   ├── MotionTrailVisualization.svelte (NEW)
│   ├── AnimationTimeline.svelte (NEW)
│   └── KeyframeEditor.svelte (NEW)
├── services/
│   ├── AnimationPlaybackController.ts (existing)
│   ├── AnimationPresetService.ts (NEW)
│   ├── MotionTrailRenderer.ts (NEW)
│   └── KeyframeService.ts (NEW)
├── domain/
│   ├── animation-models.ts (existing)
│   ├── playback-presets.ts (NEW)
│   └── motion-trail-models.ts (NEW)
└── state/
    ├── animation-panel-state.svelte.ts (existing)
    ├── animation-mode-state.svelte.ts (NEW)
    └── keyframe-state.svelte.ts (NEW)
```

### 10.4 Integration Strategy

**For adding multi-canvas support:**

```typescript
// AnimationCoordinator changes
canvases: {
  main: AnimatorCanvas,
  splitLeft: AnimatorCanvas (optional),
  splitRight: AnimatorCanvas (optional),
  trails: MotionTrailVisualization (optional)
}

// Each canvas subscribes to same playback state:
// - currentBeat (shared)
// - bluePropState (shared)
// - redPropState (shared)
// - animationMode (shared)
```

**For frame-by-frame editing:**

```typescript
// New service interface
interface IAnimationKeyframeService {
  captureKeyframe(beat: number): Keyframe;
  modifyKeyframe(beat: number, changes: Partial<PropState>): void;
  interpolateKeyframes(beat1: number, beat2: number): PropState[];
  validateKeyframes(): ValidationResult;
}
```

---

## 11. DEPENDENCY INJECTION CONFIGURATION

**DI Container Setup:**

- File: `C:\_TKA-STUDIO/src/lib/shared/inversify/container.ts`
- Framework: Inversify (TypeScript IoC)

**Key Registrations:**

```typescript
// Animation services
container
  .bind<IAnimationPlaybackController>(TYPES.IAnimationPlaybackController)
  .to(AnimationPlaybackController)
  .inTransientScope();

container
  .bind<ISequenceAnimationOrchestrator>(TYPES.ISequenceAnimationOrchestrator)
  .to(SequenceAnimationOrchestrator)
  .inTransientScope();

// Sequence services
container
  .bind<ISequenceService>(TYPES.ISequenceService)
  .to(SequenceService)
  .inSingletonScope();

container
  .bind<ISequencePersistenceService>(TYPES.ISequencePersistenceService)
  .to(SequencePersistenceService)
  .inSingletonScope();

// Create module services
container
  .bind<ICreateModuleInitializationService>(
    TYPES.ICreateModuleInitializationService
  )
  .to(CreateModuleInitializationService)
  .inTransientScope();
```

---

## 12. EFFECT COORDINATION SYSTEM

**CreateModuleEffectCoordinator** manages all reactive effects:

1. **Navigation Sync** - Sync activeTab ↔ activeSection
2. **Layout Management** - Detect side-by-side vs stacked layout
3. **Auto-Edit Panel** - Open edit panel on beat selection
4. **Single-Beat Mode** - Focus mode for individual beat editing
5. **PWA Engagement** - Track user engagement for PWA
6. **Current Word Display** - Update word label during animation
7. **Panel Height Tracking** - Track tool/button panel heights

**Why Centralized:**

- Prevents circular effect dependencies
- Makes effect interactions visible and testable
- Reduces debugging complexity for cross-cutting concerns

---

## 13. CRITICAL FILES FOR ANIMATION EXTENSION

**Must Understand:**

1. `AnimationCoordinator.svelte` - Main entry point
2. `AnimationPlaybackController.ts` - Playback logic
3. `SequenceAnimationOrchestrator.ts` - Beat calculation
4. `CanvasRenderer.ts` - Low-level rendering
5. `AnimationPanelState.svelte.ts` - State management
6. `CreateModuleState.svelte.ts` - Workspace integration
7. `SequenceTransformationService.ts` - Animation modifiers

**Supporting Files:**

1. `animation-panel-state.svelte.ts` - Local animator state
2. `math-constants.ts` - Angle/location mappings
3. `SVGGenerator.ts` - Prop SVG creation
4. `SequenceLoopabilityChecker.ts` - Loop detection
5. `GifExportOrchestrator.ts` - GIF rendering pipeline

---

## 14. BROWSER STORAGE & SESSION MANAGEMENT

**What's Persisted:**

```typescript
// Animation panel
ANIMATION_LOOP_STATE_KEY: boolean // loop preference

// Navigation
tka-current-create-mode: string        // Last active create tab
tka-current-learn-mode: string         // Last active learn tab
tka-current-module: string             // Last active module
tka-active-tab: string                 // Current tab
tka-module-last-tabs: Map<string>      // Per-module tab memory

// Session
tka-creation-method-selected: boolean  // Did user pick create method this session
```

**IndexedDB** (via SequencePersistenceService):

- Current working sequence
- Persisted undo history
- User preferences (settings)

---

## 15. TESTING CONSIDERATIONS

**Key Test Areas for Animation Enhancements:**

1. **Playback State Management**
   - Speed changes mid-animation
   - Loop toggle at end position
   - Seek to arbitrary beat

2. **Frame Interpolation**
   - Accuracy of prop position calculation
   - Continuity between beats
   - Angle normalization (0-360)

3. **Canvas Rendering**
   - SVG loading and conversion to images
   - Proper scaling and positioning
   - Transform accuracy

4. **Performance**
   - 60 FPS maintenance during playback
   - Memory usage of large sequences
   - GIF export performance

5. **Integration**
   - Panel open/close transitions
   - Workspace sequence updates
   - Effect coordination

---

## Summary Table: Animation System Architecture

| Component                     | Type      | Location                  | Responsibility                  |
| ----------------------------- | --------- | ------------------------- | ------------------------------- |
| AnimationCoordinator          | Component | coordinators/             | Orchestration, state management |
| AnimationPanel                | Component | components/               | Presentation (read-only props)  |
| AnimatorCanvas                | Component | components/               | Canvas rendering, image loading |
| AnimationPlaybackController   | Service   | services/implementations/ | Playback lifecycle              |
| SequenceAnimationOrchestrator | Service   | services/implementations/ | Beat state calculation          |
| AnimationLoopService          | Service   | services/implementations/ | Frame timing via RAF            |
| CanvasRenderer                | Service   | services/implementations/ | Low-level canvas drawing        |
| SVGGenerator                  | Service   | services/implementations/ | SVG prop generation             |
| AnimationPanelState           | Factory   | state/                    | Reactive local state            |
| GifExportOrchestrator         | Service   | services/implementations/ | GIF encoding                    |

This architecture is highly extensible through:

- **Service injection** - Add new services without modifying existing code
- **State factories** - New state machines via createXxxState() pattern
- **Coordinator pattern** - New features via new coordinators
- **Context provision** - New context providers for child components

---

**Generated:** 2025-11-05
**Architecture Version:** 1.0
**Last Updated:** Animation system and navigation structure comprehensive
