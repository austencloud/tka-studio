/**
 * Utilities for sharing sequences and generating shareable URLs
 * Main export file that re-exports all functionality from specialized modules
 */

// Re-export types
export type { ShareData } from './types';
export type { SequenceRenderResult } from './ImageUtils';
export type { ShareOptions } from './ShareHandler';
export type { DownloadOptions } from './DownloadHandler';
export type { SequenceRenderOptions } from './SequenceRenderer';

// Re-export functions from specialized modules
export {
	// Sequence encoding/decoding
	encodeSequenceCompact,
	extractStartPositionData,
	encodeStartPosition,
	encodeOrientation,
	encodePosition,
	encodeMotion,
	compressString
} from './SequenceEncoder';

export {
	// Sequence decoding
	decodeSequenceCompact,
	decodeStartPosition,
	decodeOrientation,
	decodePosition,
	inferPositionFromLocations,
	decodeMotion,
	inferMotionType,
	inferOrientations,
	inferPosition,
	inferEndPosition,
	createStartPositionBeat,
	createBeatFromMotions
} from './SequenceDecoder';

export {
	// Web Share API utilities
	isWebShareSupported,
	isFileShareSupported,
	isMobileDevice,
	shareSequence as shareSequenceWithWebShareApi,
	shareSequenceWithImage
} from './WebShareApi';

export {
	// Clipboard operations
	copyToClipboard,
	copyImageToClipboard
} from './ClipboardUtils';

export {
	// URL utilities
	generateShareableUrl,
	checkForSequenceInUrl
} from './UrlUtils';

export {
	// Image utilities
	dataURLtoBlob,
	createFileFromDataURL
} from './ImageUtils';

export {
	// Test utilities
	testSequenceUrlEncoding
} from './TestUtils';

export {
	// Element finder utilities
	findBeatFrameElement,
	listenForBeatFrameElement
} from './ElementFinder';

export {
	// Sequence renderer utilities
	renderSequence
} from './SequenceRenderer';

export {
	// Share handler utilities
	shareSequence
} from './ShareHandler';

export {
	// Download handler utilities
	downloadSequenceImage
} from './DownloadHandler';
