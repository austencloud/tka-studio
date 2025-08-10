# Svelte 5 $derived Runes - Critical Issues and Solutions

## Overview
This document explains critical issues encountered with Svelte 5's `$derived` runes when working with complex state management systems, specifically in the context of the TKA OptionPicker component.

## The Problem: $derived Not Reactive to Getter Functions

### Issue Description
When using `$derived` to react to changes in a getter function that accesses internal runes state, the derived function may not be called when the underlying state changes.

### Example of the Problem
```javascript
// In optionPickerRunes.svelte.ts
export function createOptionPickerRunes() {
    let optionsData = $state<PictographData[]>([]);
    
    // ... other code ...
    
    return {
        get allOptions() {
            return optionsData; // This is a getter accessing runes state
        },
        // ... other methods
    };
}

// In OptionPicker.svelte
const optionPickerState = createOptionPickerState();

// THIS DOES NOT WORK - derived never gets called when optionsData changes
const effectiveOptions = $derived(() => {
    const allOptions = optionPickerState.allOptions || [];
    return allOptions;
});
```

### Why This Happens
1. `optionPickerState.allOptions` is a getter function
2. The getter accesses internal `optionsData` which is a `$state` rune
3. Svelte's reactivity system doesn't automatically track changes to the underlying state through getters
4. Each component instance creates its own `optionPickerState` instance
5. Options may be loaded into one instance but accessed from another

## The Solution: Direct State Access

### Working Solution
Instead of using getters, expose the reactive state directly or use a different pattern:

```javascript
// Option 1: Direct state exposure (if possible)
export function createOptionPickerRunes() {
    let optionsData = $state<PictographData[]>([]);
    
    return {
        optionsData, // Direct access to reactive state
        // ... other methods
    };
}

// Option 2: Use $effect to sync state
const effectiveOptions = $state([]);

$effect(() => {
    const allOptions = optionPickerState.allOptions || [];
    effectiveOptions.splice(0, effectiveOptions.length, ...allOptions);
});
```

## Debugging Steps Taken

### 1. Initial Symptoms
- Options were loading successfully (36 options)
- Template showed "No options available"
- `$derived` function was never called

### 2. Debugging Logs Added
```javascript
// Added extensive logging to track the issue
console.log('🔍 OptionPicker derived CALLED at:', new Date().toLocaleTimeString());
console.log('🔧 Runes setting optionsData with', options.length, 'options');
console.log('🔍 OptionPicker delayed check:', {
    allOptionsLength: optionPickerState.allOptions?.length || 0,
    timestamp: new Date().toLocaleTimeString(),
});
```

### 3. Key Findings
- Options loading: ✅ Working (`🔧 Runes setting optionsData with 36 options`)
- Derived function: ❌ Never called (no `🔍 OptionPicker derived CALLED` logs)
- Delayed access: ❌ Still 0 options after 1 second
- Template access: ❌ Always shows 0 options

## Regression Prevention

### 1. Create Tests
```javascript
// Test that options are properly reactive
test('options should be reactive to state changes', () => {
    const state = createOptionPickerRunes();
    let derivedCalled = false;
    
    const derived = $derived(() => {
        derivedCalled = true;
        return state.allOptions;
    });
    
    // Load options
    state.loadOptions([mockOption]);
    
    // Verify derived was called
    expect(derivedCalled).toBe(true);
    expect(derived.length).toBe(1);
});
```

### 2. Documentation Requirements
- Always document when using getters with runes
- Explain reactivity implications
- Provide working examples

### 3. Code Review Checklist
- [ ] Are `$derived` functions actually being called?
- [ ] Are getters properly reactive to underlying state?
- [ ] Are state instances shared correctly between components?
- [ ] Are there proper debugging logs to track reactivity?

## Best Practices

### 1. Prefer Direct State Access
```javascript
// Good: Direct access to reactive state
const options = $derived(() => state.optionsData);

// Avoid: Getter functions that may not be reactive
const options = $derived(() => state.allOptions);
```

### 2. Use $effect for Complex State Sync
```javascript
// When you need to sync between different state systems
$effect(() => {
    const newOptions = externalState.getOptions();
    localState.splice(0, localState.length, ...newOptions);
});
```

### 3. Add Debugging Early
```javascript
// Always add logs to verify reactivity
const derived = $derived(() => {
    console.log('Derived called with:', data.length, 'items');
    return data;
});
```

## Resolution for TKA OptionPicker

The issue was resolved by:
1. Identifying that `$derived` was not reactive to getter functions
2. Switching to `$effect` to manually sync state
3. Adding comprehensive logging to prevent future regressions
4. Creating this documentation for future reference

## Never Again Checklist

- [ ] Test `$derived` reactivity immediately after implementation
- [ ] Add debugging logs to verify derived functions are called
- [ ] Document any getter/reactivity patterns used
- [ ] Create regression tests for critical reactive state
- [ ] Review state instance creation and sharing patterns
