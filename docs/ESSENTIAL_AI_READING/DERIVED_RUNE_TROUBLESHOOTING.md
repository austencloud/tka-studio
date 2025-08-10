# `$derived` Rune Troubleshooting Guide

## 🚨 The #1 Problem: Wrong Syntax

**The most common mistake is using `$derived(() => { ... })` when you should use `$derived.by(() => { ... })`**

## 🔍 Symptoms

- `$derived` function never executes
- Console.log statements inside `$derived` don't appear
- Reactive values don't update
- No error messages (fails silently)

## 🎯 Root Cause

`$derived()` expects a **value or simple expression**, not a function that returns a value.

## ✅ Correct Usage Patterns

### Pattern 1: Simple Expressions
```javascript
// ✅ CORRECT - Direct value/expression
let doubled = $derived(count * 2);
let isEven = $derived(count % 2 === 0);
let fullName = $derived(firstName + ' ' + lastName);
let filteredItems = $derived(items.filter(item => item.active));
```

### Pattern 2: Complex Logic with `$derived.by()`
```javascript
// ✅ CORRECT - Complex logic needs $derived.by()
let organizedData = $derived.by(() => {
    console.log('This will execute!');
    
    if (items.length === 0) {
        return { empty: true };
    }
    
    const grouped = {};
    for (const item of items) {
        if (!grouped[item.category]) {
            grouped[item.category] = [];
        }
        grouped[item.category].push(item);
    }
    
    return grouped;
});
```

## ❌ Common Wrong Patterns

### Wrong Pattern 1: Function in `$derived()`
```javascript
// ❌ WRONG - This creates a function, not a derived value
let result = $derived(() => {
    console.log('This will NEVER execute');
    return computation();
});

// The variable `result` now contains a function, not the computed value!
```

### Wrong Pattern 2: Expecting Svelte 4 Behavior
```javascript
// ❌ WRONG - Svelte 4 syntax
$: result = computation();

// ✅ CORRECT - Svelte 5 equivalent
let result = $derived(computation());
```

## 🔧 Quick Fix Checklist

1. **Are you using complex logic?** → Use `$derived.by(() => { ... })`
2. **Are you using console.log?** → Use `$derived.by(() => { ... })`
3. **Do you have if/else statements?** → Use `$derived.by(() => { ... })`
4. **Do you have multiple lines?** → Use `$derived.by(() => { ... })`
5. **Is it a simple expression?** → Use `$derived(expression)`

## 🐛 Debugging Steps

### Step 1: Check if the derived is executing
```javascript
// Add this to test if your derived is working
let testDerived = $derived.by(() => {
    console.log('🔍 Derived is executing with:', yourVariable);
    return yourVariable;
});
```

### Step 2: Verify runes mode
- Check VS Code status bar for "Runes" mode
- Ensure `runes: true` in svelte.config.js

### Step 3: Check dependencies
```javascript
// Make sure your dependencies are reactive ($state)
let items = $state([]); // ✅ Reactive
let items = []; // ❌ Not reactive in Svelte 5
```

## 📝 Real-World Examples

### Example 1: Organizing Data
```javascript
// ❌ WRONG
const organized = $derived(() => {
    const result = {};
    for (const item of items) {
        // Complex logic here
    }
    return result;
});

// ✅ CORRECT
const organized = $derived.by(() => {
    const result = {};
    for (const item of items) {
        // Complex logic here
    }
    return result;
});
```

### Example 2: Filtering with Logging
```javascript
// ❌ WRONG
const filtered = $derived(() => {
    console.log('Filtering items:', items.length);
    return items.filter(item => item.active);
});

// ✅ CORRECT
const filtered = $derived.by(() => {
    console.log('Filtering items:', items.length);
    return items.filter(item => item.active);
});
```

## 🎯 Memory Aid

**If you need `{` and `}` braces, use `$derived.by()`**
**If it's a single expression, use `$derived()`**

## 🔄 Migration Pattern

```javascript
// Old Svelte 4 pattern
$: {
    console.log('Items changed');
    result = processItems(items);
}

// New Svelte 5 pattern
let result = $derived.by(() => {
    console.log('Items changed');
    return processItems(items);
});
```