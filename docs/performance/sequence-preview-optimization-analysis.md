# Sequence Preview Rendering Optimization Analysis

## Executive Summary

This document analyzes the performance of sequence preview rendering for the share panel and provides recommendations for optimization, specifically targeting phone screens.

### Current Implementation

**Location**: Share button → Share panel → Preview generation

**Current Settings** (in [ShareService.ts](../../src/lib/modules/build/share/services/implementations/ShareService.ts:130-166)):

- `beatScale`: 0.15 (15% of full size)
- `quality`: 0.4 (40% JPEG quality)
- `format`: 'JPEG' (fastest encoding)

### Key Question

> "Should we pre-render in the background, or optimize further?"

## Architecture Overview

### Rendering Pipeline

```
User clicks Share Button
  ↓
SharePanel opens
  ↓
shareState.generatePreview(sequence) is called
  ↓
ShareService.generatePreview()
  ↓
SequenceRenderService.generatePreview()
  ↓
ImageCompositionService.composeSequenceImage()
  ↓
For each beat (17 times for 16-beat sequence):
  ├─ renderPictographToSVG() - Generate SVG string
  ├─ svgStringToImage() - Convert SVG to Image via Blob URL
  └─ ctx.drawImage() - Draw to canvas
  ↓
ImageFormatConverterService.canvasToDataURL()
  ↓
Return data URL to UI
```

### Performance Bottlenecks

1. **SVG Generation** (CPU-intensive)
   - Each beat requires complex SVG rendering
   - 16 beats + 1 start position = 17 SVG generations per sequence

2. **Image Loading** (Async overhead)
   - Each SVG → Blob URL → Image load is asynchronous
   - 17 sequential async operations

3. **Canvas Drawing** (Moderate)
   - Drawing 17 images onto canvas
   - Relatively fast, but adds up

4. **Format Conversion** (Minimal for JPEG)
   - JPEG encoding is fast at low quality
   - PNG would be much slower

## Performance Test Results

### Test Setup

- **Test Sequence**: 16-beat circular sequence (provided in request)
- **Platform**: Browser (Chrome/Edge)
- **Metrics**: Render time (ms), Data URL size (KB)

### Expected Results

Based on the current architecture and typical browser performance:

| Configuration                    | Expected Time  | Expected Size | Use Case                       |
| -------------------------------- | -------------- | ------------- | ------------------------------ |
| **Current (0.15, 0.4, JPEG)**    | **500-1500ms** | **80-150KB**  | **Optimal balance**            |
| Lower Scale (0.12, 0.4, JPEG)    | 400-1200ms     | 60-120KB      | Faster, slightly lower quality |
| Lower Quality (0.15, 0.3, JPEG)  | 450-1400ms     | 60-120KB      | Smaller file, similar speed    |
| Aggressive (0.10, 0.3, JPEG)     | 300-1000ms     | 40-80KB       | Fast, noticeably lower quality |
| Ultra Low (0.08, 0.2, JPEG)      | 250-800ms      | 30-60KB       | Fastest, very low quality      |
| PNG Format (0.15, 0.4, PNG)      | 600-2000ms     | 200-400KB     | Slower, larger, lossless       |
| WebP Format (0.15, 0.4, WebP)    | 500-1500ms     | 60-120KB      | Similar to JPEG                |
| Higher Quality (0.20, 0.6, JPEG) | 800-2000ms     | 150-250KB     | Better quality, slower         |

### Phone Screen Suitability

For phone screens (375-412px wide):

- **Optimal preview size**: 300-400px wide
- **Current 0.15 beatScale**: ~21px per beat (144px base × 0.15)
- **16-beat sequence**: ~6 columns × 3 rows = ~126px × 63px preview
- **With title**: ~126px × ~100px total

**Conclusion**: Current scale is extremely small for phone screens. Consider increasing to 0.20-0.25 for better visibility.

## Optimization Strategies

### Option 1: Background Pre-rendering ⭐ RECOMMENDED

**Implementation**: Generate preview in background when sequence is opened, before user clicks share button.

**Pros**:

- Preview appears instantly when share panel opens
- No user-perceived delay
- Can use higher quality settings without UX impact

**Cons**:

- Uses CPU/memory proactively
- Wasted work if user doesn't share
- Need to regenerate if options change

**Implementation**:

```typescript
// In BuildTab or Workspace Panel
$effect(() => {
  if (currentSequence && currentSequence.beats?.length > 0) {
    // Start generating preview in background
    shareState.generatePreview(currentSequence);
  }
});
```

**When to use**:

- If preview generation takes > 500ms
- If share feature is used frequently
- If you want to use higher quality settings

### Option 2: Further Quality Optimization

**Implementation**: Reduce quality/scale further to speed up rendering.

**Recommended Settings**:

```typescript
{
  beatScale: 0.12,  // Slightly smaller (20% faster)
  quality: 0.3,     // Lower quality (30% smaller file)
  format: 'JPEG'    // Keep JPEG for speed
}
```

**Pros**:

- Faster rendering (20-30% improvement)
- Smaller file size (30-40% smaller)
- No architectural changes needed

**Cons**:

- Lower visual quality
- May be too small for phone screens
- Diminishing returns

**When to use**:

- If preview generation takes < 500ms already
- If file size is a concern
- If quality is less important than speed

### Option 3: Progressive Loading

**Implementation**: Show a placeholder immediately, then load full preview.

**Approach**:

1. Show loading skeleton/placeholder instantly
2. Generate preview in background
3. Fade in preview when ready

**Pros**:

- Instant feedback to user
- Perceived performance improvement
- Can use higher quality without UX impact

**Cons**:

- More complex UI logic
- Still uses background CPU
- Two-step loading process

**When to use**:

- If preview generation takes > 1000ms
- If instant feedback is critical
- If you want to maintain high quality

### Option 4: Caching

**Implementation**: Cache generated previews in memory or localStorage.

**Approach**:

```typescript
const previewCache = new Map<string, string>();

async generatePreview(sequence: SequenceData): Promise<string> {
  const cacheKey = `${sequence.id}-${JSON.stringify(options)}`;

  if (previewCache.has(cacheKey)) {
    return previewCache.get(cacheKey)!;
  }

  const preview = await renderService.generatePreview(sequence, options);
  previewCache.set(cacheKey, preview);

  return preview;
}
```

**Pros**:

- Instant retrieval for repeated sequences
- No re-rendering needed
- Works well with background pre-rendering

**Cons**:

- Memory usage
- Need cache invalidation strategy
- Only helps for repeated views

**When to use**:

- If users frequently re-share the same sequences
- In combination with other strategies
- If memory is not a concern

### Option 5: Increase Scale for Phone Screens

**Implementation**: Use larger beatScale specifically for mobile previews.

**Recommended Settings**:

```typescript
{
  beatScale: 0.20-0.25,  // Better visibility on phone
  quality: 0.4-0.5,      // Slightly better quality
  format: 'JPEG'         // Keep JPEG for speed
}
```

**Pros**:

- Better visibility on small screens
- More professional appearance
- Still reasonably fast

**Cons**:

- Slower rendering (30-50% slower)
- Larger file size (50-100% larger)
- May still need background pre-rendering

**When to use**:

- If current previews are too small
- If quality is important
- In combination with background pre-rendering

## Recommendations

### Immediate Actions

1. **Run the benchmark** to get actual performance metrics:

   ```bash
   # Option 1: Run the test suite
   npm test tests/performance/sequence-preview-optimization.test.ts

   # Option 2: Run the standalone benchmark
   npx tsx scripts/benchmark-preview-rendering.ts
   ```

2. **Measure current preview generation time** in production:
   - Add performance timing to ShareService.generatePreview()
   - Log metrics to console or analytics
   - Identify actual bottlenecks

3. **Evaluate user experience**:
   - Test on actual phone devices
   - Check if preview quality is acceptable
   - Measure time from click to preview visible

### Recommended Strategy (Based on Expected Performance)

**If preview generation < 500ms**:

- ✅ Keep current settings
- ✅ Consider increasing beatScale to 0.20 for better visibility
- ✅ Add caching for frequently shared sequences

**If preview generation 500-1000ms**:

- ⭐ Implement **Background Pre-rendering** (Option 1)
- ✅ Increase beatScale to 0.20-0.25 for better quality
- ✅ Add caching for instant subsequent views

**If preview generation > 1000ms**:

- ⭐ Implement **Background Pre-rendering** (Option 1)
- ⭐ Implement **Progressive Loading** (Option 3)
- ⚠️ Consider reducing quality/scale temporarily
- 🔍 Investigate rendering pipeline for optimization opportunities

### Implementation Priority

1. **HIGH**: Run benchmarks to measure actual performance
2. **HIGH**: Implement background pre-rendering if > 500ms
3. **MEDIUM**: Add preview caching
4. **MEDIUM**: Increase beatScale to 0.20-0.25 for phone screens
5. **LOW**: Implement progressive loading if > 1000ms
6. **LOW**: Further optimize quality/scale settings

## Code Changes

### 1. Background Pre-rendering

**File**: [src/lib/modules/build/workspace-panel/BuildTab.svelte](../../src/lib/modules/build/workspace-panel/BuildTab.svelte)

```typescript
// Add this effect to pre-generate preview
$effect(() => {
  if (currentSequence && currentSequence.beats?.length > 0 && shareState) {
    // Pre-generate preview in background (non-blocking)
    shareState.generatePreview(currentSequence).catch((err) => {
      console.warn("Preview pre-generation failed:", err);
    });
  }
});
```

### 2. Caching

**File**: [src/lib/modules/build/share/state/share-state.svelte.ts](../../src/lib/modules/build/share/state/share-state.svelte.ts)

```typescript
class ShareStateImpl implements ShareState {
  // Add cache
  private previewCache = new Map<string, string>();

  async generatePreview(sequence: SequenceData): Promise<void> {
    // Generate cache key
    const cacheKey = `${sequence.id}-${JSON.stringify(this.options)}`;

    // Check cache first
    if (this.previewCache.has(cacheKey)) {
      this.#previewUrl = this.previewCache.get(cacheKey)!;
      return;
    }

    this.#isGeneratingPreview = true;
    this.#previewError = null;

    try {
      const preview = await this.shareService.generatePreview(
        sequence,
        this.options
      );

      // Cache result
      this.previewCache.set(cacheKey, preview);

      this.#previewUrl = preview;
    } catch (error) {
      // ... error handling
    }
  }

  // Clear cache when options change
  updateOptions(newOptions: Partial<ShareOptions>): void {
    this.#options = { ...this.#options, ...newOptions };
    this.previewCache.clear(); // Invalidate cache
  }
}
```

### 3. Increase Scale for Phone Screens

**File**: [src/lib/modules/build/share/services/implementations/ShareService.ts](../../src/lib/modules/build/share/services/implementations/ShareService.ts:130-166)

```typescript
private convertToPreviewOptions(shareOptions: ShareOptions) {
  return {
    // ... other options

    // Increase scale for better phone screen visibility
    beatScale: 0.22, // Increased from 0.15 (47% larger)

    // Slightly better quality for improved clarity
    quality: 0.45, // Increased from 0.4

    // ... other options
  };
}
```

## Monitoring

Add performance monitoring to track improvements:

```typescript
// In ShareService.generatePreview()
const startTime = performance.now();

const preview = await this.renderService.generatePreview(
  sequence,
  renderOptions
);

const endTime = performance.now();
const duration = endTime - startTime;

// Log or send to analytics
console.log(`Preview generated in ${duration.toFixed(0)}ms`);

// Optional: Track in analytics
analytics.track("preview_generated", {
  duration_ms: duration,
  beatCount: sequence.beats.length,
  beatScale: renderOptions.beatScale,
  quality: renderOptions.quality,
  format: renderOptions.format,
});
```

## Testing

Run the provided tests to validate optimizations:

```bash
# Full test suite
npm test tests/performance/sequence-preview-optimization.test.ts

# Standalone benchmark
npx tsx scripts/benchmark-preview-rendering.ts
```

## Expected Improvements

| Strategy                 | Speed Improvement        | Quality Impact      | Implementation Effort |
| ------------------------ | ------------------------ | ------------------- | --------------------- |
| Background Pre-rendering | 100% (instant UX)        | None                | Low                   |
| Caching                  | 100% (instant retrieval) | None                | Low                   |
| Lower Scale (0.12)       | 20-30%                   | Slight decrease     | Minimal               |
| Lower Quality (0.3)      | 5-10%                    | Moderate decrease   | Minimal               |
| Aggressive (0.10, 0.3)   | 40-50%                   | Noticeable decrease | Minimal               |
| Progressive Loading      | 100% (perceived)         | None                | Medium                |

## Conclusion

**Recommended Approach**: Implement **Background Pre-rendering** + **Caching** + **Increased Scale (0.22)**

This combination provides:

- ✅ Instant preview display (background pre-rendering)
- ✅ Instant subsequent views (caching)
- ✅ Better quality for phone screens (increased scale)
- ✅ Minimal code changes (low effort)
- ✅ No user-perceived performance impact

The current quality settings (0.4 JPEG) are already well-optimized. Further reducing quality would provide minimal speed benefits while noticeably degrading visual quality. The best optimization is to move rendering off the critical path via background pre-rendering.

## Next Steps

1. Run benchmarks to validate assumptions
2. Implement background pre-rendering
3. Add preview caching
4. Increase beatScale to 0.22 for better phone visibility
5. Monitor performance in production
6. Iterate based on real-world metrics

---

**Created**: 2025-10-29
**Last Updated**: 2025-10-29
**Status**: Recommendations Pending Testing
