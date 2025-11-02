# Deep Ocean Refactor - Root Cause Analysis & Fixes

## Problem Summary
The refactored Deep Ocean background was running at hyper-speed on high refresh rate monitors. After comparing with the working monolith, we found **critical timing differences**.

---

## Root Causes Identified

### 1. **Marine Life Movement - Missing Delta Time Conversion**

#### Fish Movement
**Monolith (✓ Correct):**
```typescript
const deltaSeconds = 0.016 * frameMultiplier;
fish.x += fish.direction * fish.speed * deltaSeconds;
fish.baseY += fish.verticalDrift * deltaSeconds;
```

**Refactored (✗ Wrong):**
```typescript
fish.x += fish.direction * fish.speed * frameMultiplier;
// Missing deltaSeconds conversion!
// verticalDrift is applied to frameMultiplier instead of being added to baseY
fish.y = fish.baseY + ... + fish.verticalDrift * frameMultiplier;
```

**Impact:** Fish move at ~62x faster speed (frameMultiplier ≈ 1.0 vs deltaSeconds ≈ 0.016)

---

#### Jellyfish Movement
**Monolith (✓ Correct):**
```typescript
const deltaSeconds = 0.016 * frameMultiplier;
jelly.x += jelly.horizontalSpeed * deltaSeconds;
jelly.baseY += jelly.verticalSpeed * deltaSeconds;
```

**Refactored (✗ Wrong):**
```typescript
jellyfish.x += jellyfish.horizontalSpeed * frameMultiplier;
jellyfish.y += jellyfish.verticalSpeed * frameMultiplier;
```

**Impact:** Same issue - jellyfish move at ~62x faster speed

---

### 2. **Fish Bobbing Animation - Wrong Approach**

**Monolith (✓ Correct):**
```typescript
fish.animationPhase += fish.bobSpeed * frameMultiplier;
const bob = Math.sin(fish.animationPhase) * fish.bobAmplitude;
fish.y = fish.baseY + bob;
```
- Uses **per-fish phase accumulator** (`fish.animationPhase`)
- Phase increments independently for each fish
- Clean separation of concerns

**Refactored (✗ Wrong):**
```typescript
fish.y = fish.baseY +
  Math.sin(animationTime * fish.bobSpeed + fish.animationPhase) * fish.bobAmplitude;
```
- Uses **global `animationTime`** multiplied by bobSpeed
- Doesn't update `fish.animationPhase` at all
- Mixes timing systems

**Impact:** Animation tied to global time instead of per-object phase

---

### 3. **Jellyfish Wave Animation - Same Issue**

**Monolith (✓ Correct):**
```typescript
jelly.animationPhase += jelly.waveFrequency * frameMultiplier;
jelly.y = jelly.baseY + Math.sin(jelly.animationPhase) * jelly.waveAmplitude;
```

**Refactored (✗ Wrong):**
```typescript
jellyfish.x += ... +
  Math.sin(animationTime * jellyfish.waveFrequency + jellyfish.animationPhase) *
  jellyfish.waveAmplitude * frameMultiplier;
```

**Impact:** Same mixing of global time with per-object animation

---

### 4. **Light Rays - Actually Correct!**

**Both versions use the same approach:**
```typescript
ray.phase += ray.speed * frameMultiplier;
ray.opacity = 0.05 + Math.sin(ray.phase) * 0.05;
```
✓ Light rays were refactored correctly

---

### 5. **Bubble Sway - Correct Formula, Wrong in Refactor**

**Monolith (✓ Correct):**
```typescript
bubble.x += Math.sin(this.animationTime * bubble.sway + bubble.swayOffset) * 0.5 * frameMultiplier;
```

**Refactored (Current - ✓ Fixed):**
```typescript
bubble.x += Math.sin(animationTime * bubble.sway + bubble.swayOffset) * 0.5 * frameMultiplier;
```
✓ We already fixed this one during debugging

---

## Key Insight: Two Valid Animation Patterns

The monolith uses **TWO DIFFERENT patterns** for animation:

### Pattern A: Global Animation Time (for simple periodic effects)
Used for: Bubble sway
```typescript
Math.sin(this.animationTime * property + offset)
```

### Pattern B: Per-Object Phase Accumulator (for complex/independent animations)
Used for: Fish bobbing, jellyfish waves, light rays
```typescript
object.phase += object.speed * frameMultiplier;
Math.sin(object.phase)
```

**The refactor mixed these patterns incorrectly!**

---

## The Fix Strategy

### Required Changes to MarineLifeAnimator.ts:

1. **Add `deltaSeconds` calculation**
   ```typescript
   const deltaSeconds = 0.016 * frameMultiplier;
   ```

2. **Fix fish movement**
   ```typescript
   fish.animationPhase += fish.bobSpeed * frameMultiplier;
   fish.x += fish.direction * fish.speed * deltaSeconds;
   fish.baseY += fish.verticalDrift * deltaSeconds;
   fish.y = fish.baseY + Math.sin(fish.animationPhase) * fish.bobAmplitude;
   ```

3. **Fix jellyfish movement**
   ```typescript
   jelly.animationPhase += jelly.waveFrequency * frameMultiplier;
   jelly.x += jelly.horizontalSpeed * deltaSeconds;
   jelly.baseY += jelly.verticalSpeed * deltaSeconds;
   jelly.y = jelly.baseY + Math.sin(jelly.animationPhase) * jelly.waveAmplitude;
   ```

4. **Remove `animationTime` parameter** from updateMarineLife (not needed anymore)

---

## Why This Matters

The monolith is **intentionally inconsistent** in its approach:
- **Position changes** (x, y, baseY) use `deltaSeconds = 0.016 * frameMultiplier`
- **Phase/rotation changes** use `frameMultiplier` directly
- This creates the right balance of speed vs smoothness

The refactor tried to be "consistent" by always using `animationTime` or `frameMultiplier`, but this broke the carefully tuned timing.

---

## Testing After Fix

1. Check fish swim at reasonable speed (not zooming across screen)
2. Check jellyfish drift slowly upward
3. Check bobbing/waving is smooth and gentle
4. Verify works correctly at 60Hz, 144Hz, 240Hz refresh rates
5. Compare side-by-side with monolith to ensure identical behavior

---

## Next Steps

1. Apply fixes to MarineLifeAnimator.ts
2. Update IMarineLifeAnimator interface (remove animationTime param)
3. Update DeepOceanBackgroundOrchestrator (don't pass animationTime to updateMarineLife)
4. Test thoroughly
5. Switch BackgroundFactory back to using the orchestrator
6. Delete the monolith once confirmed working
