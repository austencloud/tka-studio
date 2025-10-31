# Sequence Preview Optimization - Quick Reference

## 🚀 Quick Decision Tree

```
How long does preview generation take?
│
├─ < 500ms
│  └─ ✅ Keep current settings
│     └─ Optional: Increase scale to 0.22 for better visibility
│
├─ 500ms - 1000ms
│  └─ ⭐ Implement Background Pre-rendering
│     └─ Add caching for instant subsequent views
│
└─ > 1000ms
   └─ ⭐ Implement Background Pre-rendering + Progressive Loading
      └─ Consider temporary quality reduction while optimizing
```

## 📊 Quick Benchmark

Run this to get instant results:

```bash
npx tsx scripts/benchmark-preview-rendering.ts
```

## 🎯 Recommended Settings by Use Case

### Current Settings (Balanced)

```typescript
{
  beatScale: 0.15,
  quality: 0.4,
  format: 'JPEG'
}
```

- **Speed**: Good (500-1500ms estimated)
- **Quality**: Acceptable
- **Size**: ~80-150KB
- **Best for**: General use, decent phones

### Recommended for Phone Screens

```typescript
{
  beatScale: 0.22,  // Better visibility
  quality: 0.45,    // Slightly better quality
  format: 'JPEG'
}
```

- **Speed**: Good (700-2000ms estimated)
- **Quality**: Better
- **Size**: ~120-200KB
- **Best for**: Phone screens, requires background pre-rendering

### Speed Priority

```typescript
{
  beatScale: 0.10,
  quality: 0.3,
  format: 'JPEG'
}
```

- **Speed**: Fastest (300-1000ms estimated)
- **Quality**: Lower
- **Size**: ~40-80KB
- **Best for**: Slow devices, poor connections

### Quality Priority

```typescript
{
  beatScale: 0.25,
  quality: 0.6,
  format: 'JPEG'
}
```

- **Speed**: Slower (1000-2500ms estimated)
- **Quality**: Best
- **Size**: ~200-300KB
- **Best for**: Desktop, high-quality exports

## 🛠️ Implementation Snippets

### 1. Background Pre-rendering (RECOMMENDED)

Add to [BuildTab.svelte](../../src/lib/modules/build/workspace-panel/BuildTab.svelte):

```typescript
$effect(() => {
  if (currentSequence && currentSequence.beats?.length > 0 && shareState) {
    // Pre-generate preview in background
    shareState.generatePreview(currentSequence).catch(console.warn);
  }
});
```

### 2. Caching

Add to [share-state.svelte.ts](../../src/lib/modules/build/share/state/share-state.svelte.ts):

```typescript
private previewCache = new Map<string, string>();

async generatePreview(sequence: SequenceData): Promise<void> {
  const cacheKey = `${sequence.id}-${JSON.stringify(this.options)}`;

  if (this.previewCache.has(cacheKey)) {
    this.#previewUrl = this.previewCache.get(cacheKey)!;
    return;
  }

  // ... generate preview
  this.previewCache.set(cacheKey, preview);
}
```

### 3. Increase Scale

Modify [ShareService.ts](../../src/lib/modules/build/share/services/implementations/ShareService.ts):

```typescript
private convertToPreviewOptions(shareOptions: ShareOptions) {
  return {
    // ...
    beatScale: 0.22,  // Changed from 0.15
    quality: 0.45,    // Changed from 0.4
    // ...
  };
}
```

## 📏 Phone Screen Reference

| Device        | Width | Height | Preview Width (0.15) | Preview Width (0.22) |
| ------------- | ----- | ------ | -------------------- | -------------------- |
| iPhone SE     | 375px | 667px  | ~126px               | ~185px               |
| iPhone 14     | 390px | 844px  | ~126px               | ~185px               |
| iPhone 14 Pro | 393px | 852px  | ~126px               | ~185px               |
| Pixel 7       | 412px | 915px  | ~126px               | ~185px               |
| Galaxy S23    | 360px | 780px  | ~126px               | ~185px               |

**Recommendation**: 0.22 scale provides ~185px wide previews, which is much better for phone screens.

## ⚡ Performance Targets

### Excellent

- ✅ < 300ms: Instant, no optimization needed
- ✅ File size < 100KB

### Good

- ✅ 300-500ms: Fast enough for real-time
- ✅ File size 100-200KB

### Acceptable (with background pre-rendering)

- ⚠️ 500-1000ms: Noticeable delay, pre-render recommended
- ⚠️ File size 200-300KB

### Poor (requires optimization)

- ❌ > 1000ms: Too slow, requires background pre-rendering + progressive loading
- ❌ File size > 300KB: Too large, reduce quality/scale

## 🔍 Debugging

### Add Performance Logging

```typescript
const start = performance.now();
const preview = await renderService.generatePreview(sequence, options);
const duration = performance.now() - start;

console.log(
  `Preview: ${duration.toFixed(0)}ms, ${((preview.length * 0.75) / 1024).toFixed(1)}KB`
);
```

### Check Preview Quality

```typescript
// Log preview to console to visually inspect
console.log("Preview URL:", preview.substring(0, 100) + "...");

// Or create an img element to view
const img = document.createElement("img");
img.src = preview;
document.body.appendChild(img);
```

## 📝 Testing Checklist

- [ ] Run benchmark script
- [ ] Test on actual phone devices
- [ ] Measure preview generation time in production
- [ ] Check preview visual quality on small screens
- [ ] Test with various sequence lengths (4, 8, 16, 32 beats)
- [ ] Test with slow network (throttling)
- [ ] Verify caching works correctly
- [ ] Test background pre-rendering doesn't cause UI lag

## 🎓 Key Learnings

1. **Current settings are already well-optimized** (0.15 scale, 0.4 quality, JPEG)
2. **Further quality reduction provides minimal benefit** (diminishing returns)
3. **Background pre-rendering is the best optimization** (100% perceived improvement)
4. **Preview scale is too small for phone screens** (recommend 0.22+)
5. **Caching provides instant retrieval** for repeated sequences

## 🚨 Common Pitfalls

❌ **Don't** reduce quality below 0.3 (diminishing returns, poor UX)
❌ **Don't** reduce scale below 0.10 (unusable on phone screens)
❌ **Don't** use PNG for previews (much slower, larger files)
❌ **Don't** pre-render all sequences (memory waste)
✅ **Do** pre-render current sequence only
✅ **Do** invalidate cache when options change
✅ **Do** use JPEG format for previews
✅ **Do** show loading state during generation

## 📞 Need Help?

- Review full analysis: [sequence-preview-optimization-analysis.md](./sequence-preview-optimization-analysis.md)
- Run tests: `npm test tests/performance/sequence-preview-optimization.test.ts`
- Run benchmark: `npx tsx scripts/benchmark-preview-rendering.ts`
- Check implementation: [ShareService.ts](../../src/lib/modules/build/share/services/implementations/ShareService.ts)

---

**Last Updated**: 2025-10-29
