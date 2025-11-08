# Clear Sequence Animation Test Plan

## Test Scenarios

### Scenario 1: Clear sequence with beats

**Setup**: Create sequence with start position + 3 beats
**Expected behavior**:

1. Beats fade out together (300ms)
2. Layout shifts (workspace/tool panel fade out) - should happen AFTER beats fade
3. Welcome screen and creation method selector fade in
4. Total smooth transition ~600-700ms

**Current issues**:

- ❌ Option picker fades at same time as beats (confusing)
- ❌ Layout shift might be happening too early

### Scenario 2: Clear sequence with start position only

**Setup**: Select start position, no beats
**Expected behavior**:

1. Start position fades out (300ms)
2. Layout shifts (workspace/tool panel fade out)
3. Welcome screen and creation method selector fade in
4. NO popping or sudden replacements All right can you go ahead and test it

**Current issues**:

- ❌ Start position pops away and gets replaced with empty placeholder
- ❌ Not smooth

### Scenario 3: Clear from welcome screen (undo after clear)

**Setup**: Clear sequence, then undo
**Expected behavior**:

1. Creation method selector fades out
2. Workspace fades in with beats
3. Smooth restoration

## Root Causes

1. **Multiple animation systems**:
   - Beat clearing animation (`isClearing` CSS)
   - Layout transition (`hasSelectedCreationMethod` triggers fade in/out)
   - Component mount/unmount transitions
   - Start position picker show/hide

2. **Timing conflicts**:
   - Setting `hasSelectedCreationMethod = false` immediately
   - Calling `setShowStartPositionPicker(true)` too early (causes pop)
   - Clearing data before animations complete

## Solution

**SIMULTANEOUS animation approach**:

1. Start beat clearing animation (300ms) - beats fade
2. Immediately trigger layout shift (0ms delay) - workspace/tool panel fade out (300ms)
3. BOTH animations run in parallel
4. Wait for BOTH to complete (300ms)
5. ONLY THEN clear data and reset UI state

This ensures:

- Beats and layout fade together (cohesive, not confusing)
- No early state changes that cause components to remount
- No popping or sudden replacements
- All data clearing happens AFTER animations complete
