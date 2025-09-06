# Svelte 5 Runes TypeScript Integration

This directory contains TypeScript declarations and utilities to help with Svelte 5 runes integration.

## Overview

Svelte 5 introduces a new reactivity system based on "runes" (`$state`, `$derived`, `$effect`, etc.). These runes can sometimes cause TypeScript errors like:

- "Block-scoped variable '$state' used before its declaration"
- "Implicitly has type 'any' because it does not have a type annotation"
- "Untyped function calls may not accept type arguments"

This directory provides solutions to these issues.

## Files

- `svelte-runes.d.ts`: TypeScript declarations for Svelte 5 runes

## How to Use

### 1. Proper TypeScript Configuration

Make sure your `tsconfig.json` has the following settings:

```json
{
  "compilerOptions": {
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "target": "ES2022",
    "useDefineForClassFields": true
  }
}
```

### 2. Typing Rune Variables

When using runes, use the following patterns to avoid TypeScript errors:

```typescript
// For primitive values
let count = $state(0);

// For nullable values
let data = $state(null as MyType | null);

// For complex types
let items = $state([] as MyItem[]);
let map = $state({} as Record<string, string>);

// For derived values
const doubled = $derived(count * 2);

// For effects
$effect(() => {
  console.log(`Count is now ${count}`);
});
```

### 3. Common Pitfalls

- **Don't use `const` with `$state`**: Using `const` will prevent reassignment, which is often needed with reactive state.
- **Don't use type parameters with runes**: Instead of `$state<MyType>(null)`, use `$state(null as MyType)`.
- **Be careful with destructuring**: When you destructure a reactive object, the destructured values are not reactive.

## Troubleshooting

If you're still seeing TypeScript errors:

1. Make sure your `svelte.config.js` has `vitePreprocess({ script: true })` to enable TypeScript processing.
2. Check that the `svelte-runes.d.ts` file is being included in your TypeScript compilation.
3. Try restarting your TypeScript server in your IDE.

## References

- [Svelte 5 Documentation](https://svelte.dev/docs/svelte/runes)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
