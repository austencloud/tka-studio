# 🚨 ESSENTIAL AI READING - READ THIS FIRST! 🚨

**⚠️ CRITICAL: Every AI agent working on this codebase MUST read this documentation before making any changes to Svelte 5 components! ⚠️**

This directory contains essential documentation that prevents common AI mistakes when working with Svelte 5 runes and modern web development patterns.

## 📚 Required Reading

1. **[SVELTE_5_RUNES_GUIDE.md](./SVELTE_5_RUNES_GUIDE.md)** - Complete guide to Svelte 5 runes syntax and common pitfalls
2. **[DERIVED_RUNE_TROUBLESHOOTING.md](./DERIVED_RUNE_TROUBLESHOOTING.md)** - Specific troubleshooting for `$derived` rune issues

## 🎯 Why This Matters

AI agents consistently make the same mistakes with Svelte 5 runes, particularly:
- Using incorrect `$derived` syntax
- Not understanding the difference between `$derived()` and `$derived.by()`
- Expecting `$derived` to work like Svelte 4 reactive statements
- Missing reactivity configuration requirements

## 🔥 Common Failure Patterns

**WRONG:**
```javascript
const organizedPictographs = $derived(() => {
    console.log('This will never execute');
    return someComputation();
});
```

**RIGHT:**
```javascript
const organizedPictographs = $derived(() => someComputation());
// OR for complex logic:
const organizedPictographs = $derived.by(() => {
    console.log('This will execute');
    return someComputation();
});
```

## 📖 Reading Order

1. Read the Svelte 5 runes guide completely
2. Understand the derived rune troubleshooting guide
3. Only then proceed with component modifications

**Failure to read this documentation will result in repeated debugging cycles and wasted time.**