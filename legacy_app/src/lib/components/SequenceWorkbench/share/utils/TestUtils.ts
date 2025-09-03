/**
 * Test utilities for sequence sharing
 */
import type { BeatData } from '$lib/state/stores/sequence/SequenceContainer';
import { generateShareableUrl } from './UrlUtils';
import { decodeSequenceCompact } from './SequenceDecoder';

/**
 * Test utility for verifying URL parameter encoding/decoding
 * This function is exposed for testing purposes only
 * @param beats The sequence beats to test
 * @returns Test results with encoded URL and decoded beats
 */
export function testSequenceUrlEncoding(beats: BeatData[]): {
    success: boolean;
    originalBeats: BeatData[];
    encodedUrl: string;
    decodedBeats: BeatData[];
    encodedLength: number;
    compressedLength: number;
    compressionRatio: number;
} {
    try {
        // Generate a shareable URL
        const url = generateShareableUrl(beats, 'Test Sequence');

        // Extract the encoded sequence from the URL
        const urlObj = new URL(url);
        const encodedSequence = urlObj.searchParams.get('seq') || '';

        // Decode the sequence
        const decodedBeats = decodeSequenceCompact(encodedSequence);

        // Calculate compression stats
        const originalLength = JSON.stringify(beats).length;
        const compressedLength = encodedSequence.length;
        const compressionRatio = compressedLength / originalLength;

        return {
            success: true,
            originalBeats: beats,
            encodedUrl: url,
            decodedBeats,
            encodedLength: originalLength,
            compressedLength,
            compressionRatio
        };
    } catch (error) {
        console.error('Error in testSequenceUrlEncoding:', error);
        return {
            success: false,
            originalBeats: beats,
            encodedUrl: '',
            decodedBeats: [],
            encodedLength: 0,
            compressedLength: 0,
            compressionRatio: 0
        };
    }
}
