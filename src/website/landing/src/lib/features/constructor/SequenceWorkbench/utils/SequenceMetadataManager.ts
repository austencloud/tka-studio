import { sequenceStore } from '../../state/stores/sequenceStore.js';

/**
 * Interface for sequence metadata
 */
export interface SequenceMetadata {
    name: string;
    difficulty: number;
}

/**
 * Interface for the sequence metadata manager return value
 */
export interface SequenceMetadataManagerResult {
    metadata: SequenceMetadata;
    unsubscribe: () => void;
}

/**
 * Manages sequence metadata by subscribing to the sequence store
 * @param onUpdate Callback function to update metadata values
 * @returns Object with metadata and unsubscribe function
 */
export function useSequenceMetadata(
    onUpdate: (metadata: SequenceMetadata) => void
): SequenceMetadataManagerResult {
    // Initialize metadata with default values
    const metadata: SequenceMetadata = {
        name: '',
        difficulty: 0
    };

    // Subscribe to the sequence store for metadata updates
    const unsubscribe = sequenceStore.subscribe((store) => {
        metadata.name = store.metadata.name;
        metadata.difficulty = store.metadata.difficulty;

        // Call the update callback with the new metadata
        onUpdate(metadata);
    });

    return {
        metadata,
        unsubscribe
    };
}
