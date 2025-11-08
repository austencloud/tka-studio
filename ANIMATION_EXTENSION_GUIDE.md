# Animation System Extension Guide

Quick reference for extending animation functionality in TKA Studio.

---

## Quick Start: Adding a New Animation Feature

### 1. Add State to AnimationPanelState

**File:** `C:\_TKA-STUDIO/src/lib/modules/create/animate/state/animation-panel-state.svelte.ts`

```typescript
// Add property
let myNewFeature = $state(false);

// Add getter/setter in return object
get myNewFeature() { return myNewFeature; },
setMyNewFeature: (value: boolean) => {
  myNewFeature = value;
},
```

### 2. Add UI Control to AnimationControls

**File:** `C:\_TKA-STUDIO/src/lib/modules/create/animate/components/AnimationControls.svelte`

```svelte
<script lang="ts">
  let { myNewFeatureValue = false, onMyNewFeatureChange = () => {} } = $props();
</script>

<button onclick={() => onMyNewFeatureChange(!myNewFeatureValue)}>
  My Feature
</button>
```

### 3. Connect in AnimationCoordinator

**File:** `C:\_TKA-STUDIO/src/lib/modules/create/shared/components/coordinators/AnimationCoordinator.svelte`

```svelte
function handleMyNewFeatureChange(value: boolean) {
  animationPanelState.setMyNewFeature(value);
  // Add logic based on feature
}

<AnimationPanel
  myNewFeatureValue={animationPanelState.myNewFeature}
  onMyNewFeatureChange={handleMyNewFeatureChange}
  ...
/>
```

---

## Adding Animation Modes

### Example: Slow-Motion Mode

**1. Create Mode Service**

```typescript
// C:\_TKA-STUDIO/src/lib/modules/create/animate/services/contracts/IAnimationModeService.ts

export interface IAnimationModeService {
  applyMode(
    mode: AnimationMode,
    playbackController: IAnimationPlaybackController
  ): void;
}

export enum AnimationMode {
  NORMAL = "normal",
  SLOWMO = "slowmo",
  REWIND = "rewind",
}
```

**2. Implement Service**

```typescript
// C:\_TKA-STUDIO/src/lib/modules/create/animate/services/implementations/AnimationModeService.ts

@injectable()
export class AnimationModeService implements IAnimationModeService {
  applyMode(
    mode: AnimationMode,
    playbackController: IAnimationPlaybackController
  ): void {
    switch (mode) {
      case AnimationMode.SLOWMO:
        playbackController.setSpeed(0.5); // Half speed
        break;
      case AnimationMode.REWIND:
        // Implement reverse playback
        break;
      case AnimationMode.NORMAL:
      default:
        playbackController.setSpeed(1.0);
    }
  }
}
```

**3. Register in DI Container**

```typescript
// C:\_TKA-STUDIO/src/lib/shared/inversify/container.ts

container
  .bind<IAnimationModeService>(TYPES.IAnimationModeService)
  .to(AnimationModeService)
  .inSingletonScope();
```

**4. Use in Coordinator**

```typescript
// AnimationCoordinator

let selectedMode = $state<AnimationMode>(AnimationMode.NORMAL);

function handleModeChange(mode: AnimationMode) {
  selectedMode = mode;
  animationModeService.applyMode(mode, playbackController);
}
```

---

## Adding Multiple Canvas Panels

### Structure for Split-View Animation

**1. Create Canvas Manager Service**

```typescript
// C:\_TKA-STUDIO/src/lib/modules/create/animate/services/contracts/ICanvasManager.ts

export interface ICanvasManager {
  addCanvas(id: string, purpose: CanvasPurpose): HTMLCanvasElement;
  renderAllCanvases(state: AnimationPanelState): void;
  removeCanvas(id: string): void;
}

export enum CanvasPurpose {
  MAIN = "main",
  SPLIT_LEFT = "split-left",
  SPLIT_RIGHT = "split-right",
  TRAILS = "trails",
  ANALYSIS = "analysis",
}
```

**2. Create Multi-Canvas Component**

```svelte
<!-- C:\_TKA-STUDIO/src/lib/modules/create/animate/components/MultiCanvasRenderer.svelte -->

<script lang="ts">
  import type { CanvasPurpose, ICanvasManager } from '../services/contracts';
  
  let {
    purposes = [CanvasPurpose.MAIN],
    blueProp,
    redProp,
    gridVisible,
    gridMode,
  } = $props();
  
  let canvases = $state<Map<CanvasPurpose, HTMLCanvasElement>>(new Map());
  
  // Create canvas element for each purpose
  $effect(() => {
    purposes.forEach(purpose => {
      if (!canvases.has(purpose)) {
        const canvas = document.createElement('canvas');
        canvases.set(purpose, canvas);
      }
    });
  });
  
  // Render all canvases with different visualizations
  $effect(() => {
    canvases.forEach((canvas, purpose) => {
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      
      switch (purpose) {
        case CanvasPurpose.MAIN:
          // Normal rendering
          canvasRenderer.renderScene(ctx, ...);
          break;
        case CanvasPurpose.SPLIT_LEFT:
          // Render only blue prop
          // TODO
          break;
        case CanvasPurpose.SPLIT_RIGHT:
          // Render only red prop
          // TODO
          break;
        case CanvasPurpose.TRAILS:
          // Render motion trails
          // TODO
          break;
      }
    });
  });
</script>

<div class="canvas-grid" class:multi-canvas={purposes.length > 1}>
  {#each Array.from(canvases.entries()) as [purpose, canvas]}
    <div class="canvas-container" data-purpose={purpose}>
      {canvas}
    </div>
  {/each}
</div>

<style>
  .canvas-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 8px;
  }

  .canvas-grid.multi-canvas {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  }
</style>
```

**3. Add Canvas Selection to AnimationPanel**

```svelte
<script lang="ts">
  let canvasMode = $state<"single" | "split" | "detail">("single");

  const canvasPurposes = $derived(() => {
    switch (canvasMode) {
      case "split":
        return [
          CanvasPurpose.MAIN,
          CanvasPurpose.SPLIT_LEFT,
          CanvasPurpose.SPLIT_RIGHT,
        ];
      case "detail":
        return [CanvasPurpose.MAIN, CanvasPurpose.TRAILS];
      default:
        return [CanvasPurpose.MAIN];
    }
  });
</script>

<div class="animation-panel">
  <div class="canvas-mode-selector">
    <button onclick={() => (canvasMode = "single")}>Single</button>
    <button onclick={() => (canvasMode = "split")}>Split</button>
    <button onclick={() => (canvasMode = "detail")}>Detail</button>
  </div>

  <MultiCanvasRenderer purposes={canvasPurposes()} ... />
</div>
```

---

## Adding Keyframe Editing

### Frame-by-Frame Edit Mode

**1. Create Keyframe State**

```typescript
// C:\_TKA-STUDIO/src/lib/modules/create/animate/state/keyframe-state.svelte.ts

export interface Keyframe {
  beat: number;
  bluePropState: PropState;
  redPropState: PropState;
}

export function createKeyframeState() {
  let keyframes = $state<Keyframe[]>([]);
  let editingKeyframe = $state<number | null>(null);

  return {
    get keyframes() {
      return keyframes;
    },
    get editingKeyframe() {
      return editingKeyframe;
    },

    addKeyframe: (beat: number, blue: PropState, red: PropState) => {
      keyframes.push({ beat, bluePropState: blue, redPropState: red });
      keyframes.sort((a, b) => a.beat - b.beat);
    },

    updateKeyframe: (index: number, newState: Partial<Keyframe>) => {
      keyframes[index] = { ...keyframes[index], ...newState };
    },

    removeKeyframe: (index: number) => {
      keyframes.splice(index, 1);
    },

    setEditingKeyframe: (index: number | null) => {
      editingKeyframe = index;
    },
  };
}
```

**2. Create Keyframe Editor Component**

```svelte
<!-- C:\_TKA-STUDIO/src/lib/modules/create/animate/components/KeyframeEditor.svelte -->

<script lang="ts">
  let {
    keyframes,
    editingKeyframe,
    blueProp,
    redProp,
    onKeyframeSelect,
    onKeyframeDelete,
  } = $props();
</script>

<div class="keyframe-editor">
  <div class="keyframe-timeline">
    {#each keyframes as kf, index}
      <button
        class="keyframe"
        class:editing={editingKeyframe === index}
        onclick={() => onKeyframeSelect(index)}
      >
        Beat {kf.beat}
      </button>
    {/each}
  </div>

  {#if editingKeyframe !== null}
    <div class="keyframe-properties">
      <h3>Edit Keyframe {keyframes[editingKeyframe].beat}</h3>

      <div class="property">
        <label>Blue Center Angle</label>
        <input
          type="range"
          min="0"
          max="360"
          value={(keyframes[editingKeyframe].bluePropState.centerPathAngle *
            180) /
            Math.PI}
        />
      </div>

      <div class="property">
        <label>Red Center Angle</label>
        <input
          type="range"
          min="0"
          max="360"
          value={(keyframes[editingKeyframe].redPropState.centerPathAngle *
            180) /
            Math.PI}
        />
      </div>

      <button onclick={() => onKeyframeDelete(editingKeyframe)}
        >Delete Keyframe</button
      >
    </div>
  {/if}
</div>
```

**3. Integrate into AnimationCoordinator**

```typescript
// AnimationCoordinator

const keyframeState = createKeyframeState();

function handleCaptureKeyframe() {
  const currentBeat = animationPanelState.currentBeat;
  const blueProp = animationPanelState.bluePropState;
  const redProp = animationPanelState.redPropState;

  keyframeState.addKeyframe(currentBeat, blueProp, redProp);
}

function handleApplyKeyframes() {
  // Rebuild sequence with keyframe data
  // Update beat motions based on captured keyframes
}
```

---

## Adding Motion Trail Visualization

### Render Prop Paths

**1. Create Motion Trail Service**

```typescript
// C:\_TKA-STUDIO/src/lib/modules/create/animate/services/contracts/IMotionTrailRenderer.ts

export interface IMotionTrailRenderer {
  renderTrail(
    ctx: CanvasRenderingContext2D,
    canvasSize: number,
    beat1: number,
    beat2: number,
    orchestrator: ISequenceAnimationOrchestrator,
    color: "blue" | "red"
  ): void;
}
```

**2. Implement Renderer**

```typescript
// C:\_TKA-STUDIO/src/lib/modules/create/animate/services/implementations/MotionTrailRenderer.ts

@injectable()
export class MotionTrailRenderer implements IMotionTrailRenderer {
  renderTrail(
    ctx: CanvasRenderingContext2D,
    canvasSize: number,
    beat1: number,
    beat2: number,
    orchestrator: ISequenceAnimationOrchestrator,
    color: "blue" | "red"
  ): void {
    const centerX = canvasSize / 2;
    const centerY = canvasSize / 2;
    const gridScaleFactor = canvasSize / 950;
    const radius = 150 * gridScaleFactor;

    ctx.strokeStyle = color === "blue" ? "#0066ff" : "#ff0033";
    ctx.lineWidth = 2;
    ctx.setLineDash([5, 5]);
    ctx.globalAlpha = 0.5;

    ctx.beginPath();

    // Draw path from beat1 to beat2
    for (let beat = beat1; beat <= beat2; beat += 0.1) {
      orchestrator.calculateState(beat);
      const propState =
        color === "blue"
          ? orchestrator.getBluePropState()
          : orchestrator.getRedPropState();

      const x = centerX + Math.cos(propState.centerPathAngle) * radius;
      const y = centerY + Math.sin(propState.centerPathAngle) * radius;

      if (beat === beat1) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    }

    ctx.stroke();
    ctx.setLineDash([]);
    ctx.globalAlpha = 1.0;
  }
}
```

**3. Add Trail Visualization Button**

```svelte
<!-- AnimationPanel.svelte -->

<script lang="ts">
  let showTrails = $state(false);
</script>

<button onclick={() => (showTrails = !showTrails)}>
  {showTrails ? "Hide" : "Show"} Trails
</button>

{#if showTrails}
  <MotionTrailVisualization
    orchestrator={animationEngine}
    currentBeat={animationPanelState.currentBeat}
  />
{/if}
```

---

## Performance Optimization Tips

### 1. Debounce Canvas Redraws

```typescript
// AnimatorCanvas.svelte

let needsRender = $state(true);
let rafId: number | null = null;

function renderLoop(): void {
  if (!ctx || !imagesLoaded) {
    rafId = null;
    return;
  }

  if (needsRender) {
    render();
    needsRender = false;
  }

  // Only request new frame if render was needed
  if (needsRender) {
    rafId = requestAnimationFrame(renderLoop);
  } else {
    rafId = null;
  }
}

// Only trigger render when props actually change
$effect(() => {
  blueProp;
  redProp;
  needsRender = true; // Mark dirty
  startRenderLoop();
});
```

### 2. Memoize Expensive Calculations

```typescript
// In SequenceAnimationOrchestrator

private beatStateCache = new Map<number, BeatState>();

calculateState(currentBeat: number): void {
  const cacheKey = Math.floor(currentBeat);

  if (this.beatStateCache.has(cacheKey)) {
    // Return cached calculation
    return;
  }

  // Do expensive calculation...
  this.beatStateCache.set(cacheKey, result);
}
```

### 3. Use Lazy Image Loading

```typescript
// AnimatorCanvas.svelte - Load images only when needed

async function loadPropImages() {
  if (imagesLoaded) return; // Skip if already loaded

  try {
    [blueStaffImage, redStaffImage] = await Promise.all([
      svgImageService.convertSvgStringToImage(...),
      svgImageService.convertSvgStringToImage(...),
    ]);

    imagesLoaded = true;
    needsRender = true;
  } catch (err) {
    console.error("Failed to load images:", err);
  }
}
```

---

## Testing Animation Features

### Unit Test Template

```typescript
// C:\_TKA-STUDIO/tests/animate/my-feature.test.ts

import { describe, it, expect, beforeEach } from "vitest";
import { MyFeatureService } from "$create/animate/services/implementations";

describe("MyFeatureService", () => {
  let service: MyFeatureService;

  beforeEach(() => {
    service = new MyFeatureService();
  });

  it("should correctly calculate feature state", () => {
    const result = service.calculateState({
      input: "test-data",
    });

    expect(result).toEqual({
      expected: "output",
    });
  });
});
```

### Integration Test Template

```typescript
// C:\_TKA-STUDIO/tests/animate/animation-integration.test.ts

import { describe, it, expect } from "vitest";
import { render } from "@testing-library/svelte";
import AnimationCoordinator from "$create/shared/components/coordinators/AnimationCoordinator.svelte";

describe("AnimationCoordinator Integration", () => {
  it("should load sequence and start animation", async () => {
    const { container } = render(AnimationCoordinator);

    // Verify initial state
    expect(container.querySelector(".animation-panel")).toBeFalsy();

    // Simulate panel open
    // TODO: Trigger through component

    // Verify animation started
    // TODO: Assert animation state
  });
});
```

---

## Common Extension Patterns

### Pattern 1: Add State → Add UI → Connect in Coordinator

```
AnimationPanelState
    ↓ (add property & setter)
AnimationControls
    ↓ (add button/input)
AnimationCoordinator
    ↓ (add handler & pass props)
AnimationPanel
    ↓ (receive props & forward callbacks)
```

### Pattern 2: Add Service → Register DI → Inject in Coordinator

```
Create Service Interface
    ↓
Implement Service
    ↓
Register in DI Container
    ↓
Inject via Constructor in Coordinator
    ↓
Use in Effect/Handler
```

### Pattern 3: Add Visualization → Create Component → Integrate with Canvas

```
Create Custom Renderer/Component
    ↓
Export from animate/index.ts
    ↓
Import in AnimationCoordinator
    ↓
Add toggle control to AnimationPanel
    ↓
Show/hide conditionally
```

---

## File Organization Best Practices

**Where to put new animation features:**

```
New Animation Mode?
→ services/implementations/MyAnimationModeService.ts
→ services/contracts/IMyAnimationModeService.ts

New Canvas Visualization?
→ components/MyCanvasVisualization.svelte
→ services/implementations/MyRenderer.ts

New Animation State?
→ state/my-state.svelte.ts
→ Compose into AnimationPanelState or create new

New Domain Models?
→ domain/my-models.ts
→ domain/my-constants.ts

New Tests?
→ tests/animate/my-feature.test.ts
```

---

## Related Documentation

- `ARCHITECTURE_ANALYSIS.md` - Complete system architecture
- `ARCHITECTURE_DIAGRAMS.md` - Visual data flows and state machines
- Animation System Source: `C:\_TKA-STUDIO/src/lib/modules/create/animate/`
- Create Module Source: `C:\_TKA-STUDIO/src/lib/modules/create/shared/`

---

**Generated:** 2025-11-05
**Version:** 1.0 - Animation Extension Quick Reference
