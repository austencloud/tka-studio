# Sequence State Management

## Migration Notice

The sequence state management has been migrated to a new architecture using a container-based approach. The files in this directory are being maintained for backward compatibility but are deprecated and will be removed in a future version.

## New Implementation

The new implementation can be found in:

- `src/lib/state/stores/sequence/sequenceAdapter.ts` - Adapter between the modern container and legacy store API
- `src/lib/state/stores/sequence/modernSequenceContainer.ts` - Modern container implementation
- `src/lib/state/machines/sequenceMachine/modernSequenceMachine.ts` - State machine for sequence operations
- `src/lib/state/machines/sequenceMachine/modernActions.ts` - Actions for the sequence state machine

## Migration Plan

1. Replace imports from the deprecated files with imports from the new implementation:
   - Replace `import { beatsStore } from '$lib/stores/sequence/beatsStore'` with `import { sequenceStore } from '$lib/state/stores/sequence/sequenceAdapter'`
   - Replace `import { isSequenceEmpty } from '$lib/stores/sequence/sequenceStateStore'` with a derived store from sequenceStore
   - Replace `import { sequenceActions } from '$lib/stores/sequence/sequenceActions'` with `import { sequenceActions } from '$lib/state/machines/sequenceMachine'`

2. Update method calls:
   - Replace `beatsStore.set(beats)` with `sequenceStore.setSequence(beats)`
   - Replace `beatsStore.update(updater)` with appropriate sequenceStore methods

3. Once all components have been migrated, the deprecated files can be removed.
