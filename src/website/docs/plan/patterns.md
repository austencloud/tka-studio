# 🎨 Modern Patterns & Best Practices

## 🔄 **1. Pure Svelte 5 Runes State Management**

### State Classes with Runes

```typescript
// No more writables - Pure runes approach
class FeatureState {
  // Reactive state
  items = $state<Item[]>([]);
  selectedId = $state<string | null>(null);

  // Computed values
  selectedItem = $derived(
    this.items.find((item) => item.id === this.selectedId) ?? null,
  );

  // Effects
  constructor() {
    $effect(() => {
      // Auto-save when items change
      if (this.items.length > 0) {
        this.saveToStorage();
      }
    });
  }

  // Actions
  addItem = (item: Item) => {
    this.items.push(item);
  };

  selectItem = (id: string) => {
    this.selectedId = id;
  };
}

export const featureState = new FeatureState();
```

### Migration from Legacy Stores

```typescript
// OLD - Legacy writable stores (ELIMINATE)
import { writable, derived } from "svelte/store";
export const items = writable([]);
export const selectedId = writable(null);

// NEW - Pure runes approach
class ItemState {
  items = $state<Item[]>([]);
  selectedId = $state<string | null>(null);
  selectedItem = $derived(
    this.items.find((item) => item.id === this.selectedId),
  );
}
```

---

## 🧩 **2. Component Architecture**

### Modern Component with Runes

```svelte
<!-- V2 Component Pattern -->
<script lang="ts">
  import { featureState } from '../state/feature.svelte.ts'

  interface Props {
    title: string
    onAction?: (item: Item) => void
  }

  let { title, onAction }: Props = $props()

  // Local state
  let isEditing = $state(false)
  let editValue = $state('')

  // Derived state
  let hasItems = $derived(featureState.items.length > 0)

  // Effects
  $effect(() => {
    console.log('Items changed:', featureState.items.length)
  })

  function handleEdit() {
    isEditing = true
    editValue = featureState.selectedItem?.name ?? ''
  }
</script>

<div class="modern-component">
  <h2>{title}</h2>
  {#if hasItems}
    <!-- Component content -->
  {:else}
    <EmptyState />
  {/if}
</div>
```

### Component Organization

```
ui/
├── layout/           # App structure
│   ├── AppShell.svelte
│   ├── MainLayout.svelte
│   └── PanelSystem.svelte
├── workspace/        # Core editing UI
│   ├── Canvas.svelte
│   ├── Timeline.svelte
│   └── Toolbox.svelte
├── backgrounds/      # Animation systems
│   ├── SnowfallCanvas.svelte
│   └── BackgroundEngine.svelte
└── common/          # Reusable components
    ├── Button.svelte
    ├── Modal.svelte
    └── Loading.svelte
```

---

## 🔒 **3. Type Safety**

### Strict TypeScript Interfaces

```typescript
// Comprehensive type definitions
export interface Pictograph {
  readonly id: string;
  readonly type: PictographType;
  readonly position: Point2D;
  readonly rotation: number;
  readonly scale: number;
  readonly metadata: PictographMetadata;
}

export type PictographType = "person" | "arrow" | "formation" | "prop";

export interface Point2D {
  readonly x: number;
  readonly y: number;
}

export interface PictographMetadata {
  readonly createdAt: Date;
  readonly updatedAt: Date;
  readonly version: string;
  readonly tags: readonly string[];
}
```

### State Type Safety

```typescript
// Type-safe state management
class WorkspaceState {
  pictographs = $state<Pictograph[]>([]);
  selectedIds = $state<Set<string>>(new Set());

  // Type-safe actions
  addPictograph = (pictograph: Pictograph): void => {
    this.pictographs.push(pictograph);
  };

  selectPictograph = (id: string): void => {
    this.selectedIds.add(id);
  };

  // Type-safe computed values
  selectedPictographs = $derived(
    this.pictographs.filter((p) => this.selectedIds.has(p.id)),
  );
}
```

---

## ⚡ **4. Performance Optimization**

### Canvas Rendering with RAF

```typescript
// High-performance canvas rendering
class CanvasRenderer {
  private animationId: number | null = null;
  private lastFrameTime = 0;

  canvas = $state<HTMLCanvasElement | null>(null);
  ctx = $state<CanvasRenderingContext2D | null>(null);
  fps = $state(60);

  render = (currentTime: number) => {
    if (!this.ctx) return;

    // Calculate delta time
    const deltaTime = currentTime - this.lastFrameTime;
    this.lastFrameTime = currentTime;

    // Update FPS
    this.fps = Math.round(1000 / deltaTime);

    // Clear and render
    this.ctx.clearRect(0, 0, this.canvas!.width, this.canvas!.height);
    this.drawPictographs();
    this.drawGrid();

    // Continue animation loop
    this.animationId = requestAnimationFrame(this.render);
  };

  startAnimation = () => {
    if (!this.animationId) {
      this.animationId = requestAnimationFrame(this.render);
    }
  };

  stopAnimation = () => {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  };

  // Clean up resources
  destroy = () => {
    this.stopAnimation();
    this.ctx = null;
    this.canvas = null;
  };
}
```

### Memory Management

```typescript
// Efficient resource management
class ResourceManager {
  private resources = new Map<string, Resource>();

  load = async (id: string, url: string): Promise<Resource> => {
    if (this.resources.has(id)) {
      return this.resources.get(id)!;
    }

    const resource = await this.loadResource(url);
    this.resources.set(id, resource);
    return resource;
  };

  cleanup = () => {
    for (const [id, resource] of this.resources) {
      resource.dispose();
    }
    this.resources.clear();
  };
}
```

---

## 🧪 **5. Testing Patterns**

### Component Testing

```typescript
// Modern component testing
import { render, screen } from "@testing-library/svelte";
import { expect, test } from "vitest";
import Canvas from "./Canvas.svelte";

test("renders canvas with correct dimensions", () => {
  render(Canvas, {
    props: {
      width: 800,
      height: 600,
    },
  });

  const canvas = screen.getByRole("img");
  expect(canvas).toHaveAttribute("width", "800");
  expect(canvas).toHaveAttribute("height", "600");
});
```

### State Testing

```typescript
// State class testing
import { expect, test } from "vitest";
import { PictographEngine } from "./engine.svelte.ts";

test("creates pictograph with correct properties", () => {
  const engine = new PictographEngine();

  engine.create("person");

  expect(engine.pictographs).toHaveLength(1);
  expect(engine.pictographs[0].type).toBe("person");
  expect(engine.pictographs[0].id).toBeDefined();
});
```

---

## 📦 **6. Modern Dependencies**

### Minimal, Focused Dependencies

```json
{
  "dependencies": {
    "lucide-svelte": "^0.486.0",
    "motion": "^11.0.0",
    "tailwindcss": "^3.4.17"
  },
  "devDependencies": {
    "@sveltejs/kit": "^2.16.1",
    "@sveltejs/vite-plugin-svelte": "^5.0.3",
    "svelte": "^5.0.0",
    "typescript": "^5.8.3",
    "vite": "^6.0.0",
    "vitest": "^3.1.1",
    "@playwright/test": "^1.52.0"
  }
}
```

### Eliminated Dependencies

```json
// REMOVED - Heavy, conflicting dependencies
{
  "xstate": "REMOVED - Complex state management",
  "redux": "REMOVED - React pattern in Svelte",
  "react-redux": "REMOVED - Wrong framework",
  "@reduxjs/toolkit": "REMOVED - Unnecessary complexity"
}
```

---

## 🔧 **7. Development Workflow**

### Hot Development Experience

```typescript
// Vite configuration for optimal DX
export default {
  plugins: [sveltekit()],
  server: {
    hmr: true,
    port: 5174,
  },
  optimizeDeps: {
    include: ["lucide-svelte"],
  },
};
```

### Code Quality Tools

```json
// TypeScript strict configuration
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noImplicitReturns": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

---

## 🎯 **8. Error Handling**

### Comprehensive Error Boundaries

```svelte
<!-- ErrorBoundary.svelte -->
<script lang="ts">
  interface Props {
    children: Snippet
    fallback?: Snippet<[Error]>
  }

  let { children, fallback }: Props = $props()
  let error = $state<Error | null>(null)

  function handleError(e: Error) {
    error = e
    console.error('Component error:', e)
  }
</script>

{#if error}
  {#if fallback}
    {@render fallback(error)}
  {:else}
    <div class="error-fallback">
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
    </div>
  {/if}
{:else}
  {@render children()}
{/if}
```

### Graceful Degradation

```typescript
// Resilient feature detection
class FeatureDetector {
  static hasWebGL = (): boolean => {
    try {
      const canvas = document.createElement("canvas");
      return !!(
        canvas.getContext("webgl") || canvas.getContext("experimental-webgl")
      );
    } catch {
      return false;
    }
  };

  static hasOffscreenCanvas = (): boolean => {
    return typeof OffscreenCanvas !== "undefined";
  };
}
```

_Last updated: June 11, 2025_
