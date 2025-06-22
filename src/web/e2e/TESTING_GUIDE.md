# E2E Testing Guide for The Kinetic Constructor

This guide provides best practices for making components testable with Playwright and maintaining reliable E2E tests.

## Adding Test Attributes to Components

To make components easily selectable in tests, add `data-test` attributes:

```svelte
<!-- Good: Component with test attribute -->
<div data-test="pictograph" class="pictograph-wrapper">
  <!-- Component content -->
</div>

<!-- Bad: Component without test attribute -->
<div class="pictograph-wrapper">
  <!-- Component content -->
</div>
```

### Naming Conventions

- Use kebab-case for attribute values
- Include component name and optional identifier
- Be specific but concise

```svelte
<!-- Main components -->
<div data-test="pictograph">...</div>
<div data-test="grid">...</div>

<!-- Components with identifiers -->
<button data-test="generate-button">Generate</button>
<div data-test="sequence-item-1">...</div>

<!-- State-specific elements -->
<div data-test="error-message">...</div>
<div data-state="generating">...</div>
```

## Testing XState Components

For components driven by XState:

1. Add `data-state` attributes that reflect the current state:

```svelte
<div data-state={$sequenceState.value}>
  <!-- Component content -->
</div>
```

2. Add test attributes for specific states:

```svelte
{#if $sequenceState.matches('generating')}
  <div data-test="generating-indicator">Generating...</div>
{/if}
```

3. Expose state transitions for testing:

```svelte
<script>
  // Expose the actor for testing
  if (typeof window !== 'undefined') {
    window.sequenceActor = sequenceActor;
  }
</script>
```

## SVG Testing Best Practices

For SVG components:

1. Add test attributes to SVG elements:

```svelte
<svg data-test="grid-svg" viewBox="0 0 1000 1000">
  <!-- SVG content -->
</svg>
```

2. Add identifiers to important SVG elements:

```svelte
<circle
  data-point-name="center"
  cx="500"
  cy="500"
  r="10"
/>
```

3. Use consistent attribute names for similar elements:

```svelte
<!-- Grid points -->
<circle data-point-name="ne_diamond" />
<circle data-point-name="sw_diamond" />

<!-- Props -->
<g data-prop-type="club" />
<g data-prop-type="hoop" />

<!-- Arrows -->
<path data-motion-type="pro" />
<path data-motion-type="anti" />
```

## Testing State Persistence

For components that persist state:

1. Add test attributes to elements that display persisted state:

```svelte
<h1 data-test="act-title">{actTitle}</h1>
```

2. Add test attributes to elements that modify persisted state:

```svelte
<input data-test="act-title-input" bind:value={actTitle} />
```

## Performance Testing

For performance-sensitive components:

1. Add performance marks in critical code paths:

```javascript
// Start timing
performance.mark("grid-render-start");

// Render the grid
renderGrid();

// End timing
performance.mark("grid-render-end");
performance.measure("grid-render", "grid-render-start", "grid-render-end");
```

2. Expose performance metrics for testing:

```javascript
// In your component
onMount(() => {
  if (typeof window !== "undefined") {
    window.addEventListener("grid-rendered", (e) => {
      const renderTime =
        performance.getEntriesByName("grid-render")[0].duration;
      dispatchEvent(
        new CustomEvent("performance-report", {
          detail: { component: "grid", renderTime },
        }),
      );
    });
  }
});
```

## Debugging Tests

When tests fail:

1. Use `test:e2e:debug` to run tests in debug mode
2. Check screenshots in `test-results/` directory
3. Review the HTML report with `test:e2e:report`
4. Add more specific assertions to identify the issue
