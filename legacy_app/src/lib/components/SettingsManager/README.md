# SettingsManager Component

## Purpose

The SettingsManager component is a specialized component designed to handle lifecycle events for application settings in a Svelte 5 application using runes. It solves a specific problem with Svelte 5's lifecycle methods:

**Problem**: In Svelte 5 with runes, lifecycle methods like `onMount` can only be used within Svelte component files (`.svelte`), not in `.svelte.ts` files that are meant for state management.

**Solution**: This component provides a proper component context for initializing settings and handling lifecycle events like loading from localStorage on mount and saving to localStorage before the application unloads.

## Usage

The SettingsManager component is designed to be included once at the application root level. It's currently included in the `ServiceProvider.svelte` component, which ensures it's loaded when the application starts.

```svelte
<!-- In ServiceProvider.svelte -->
<SettingsManager />
<slot></slot>
```

## How It Works

1. **Initialization**: When the component mounts, it calls `loadImageExportSettings()` to load settings from localStorage.

2. **Cleanup**: It sets up an event listener for the `beforeunload` event to save settings when the user closes the application.

3. **Lifecycle Management**: It properly handles component lifecycle events using Svelte's `onMount` and `onDestroy` hooks.

## Benefits

- Provides a proper component context for lifecycle methods
- Ensures settings are loaded when the application starts
- Ensures settings are saved when the application closes
- Prevents the "lifecycle_outside_component" error that occurs when using lifecycle methods outside of a component context

## Implementation Details

The component is invisible in the UI (using `display: none`) and only serves to manage the settings lifecycle.

```svelte
<!-- This is an invisible component that just manages settings lifecycle -->
<div style="display: none;" aria-hidden="true">
	<!-- Status for debugging -->
	{#if initialized}
		<!-- Settings manager initialized -->
	{/if}
</div>
```

## Related Files

- `src/lib/state/image-export-settings.svelte.ts`: Contains the settings state and functions for loading/saving settings
- `src/lib/providers/ServiceProvider.svelte`: Includes the SettingsManager component

## Common Issues and Solutions

### structuredClone Error with Svelte 5 Runes

When using Svelte 5 runes, you might encounter this error:

```
Uncaught DataCloneError: Failed to execute 'structuredClone' on 'Window': #<Object> could not be cloned.
```

This happens because `structuredClone()` cannot properly clone Svelte 5's reactive state objects. When you use `$state` in Svelte 5, it creates a special proxy object that can't be directly cloned using `structuredClone()`.

**Solution**: Instead of using `structuredClone()` on reactive state objects, create a plain object copy by manually copying each property:

```typescript
// Instead of this:
const copy = structuredClone(reactiveObject);

// Do this:
const copy = {
	property1: reactiveObject.property1,
	property2: reactiveObject.property2
	// ...and so on
};
```

This approach is used in the `getImageExportSettings()` and `saveImageExportSettings()` functions.
