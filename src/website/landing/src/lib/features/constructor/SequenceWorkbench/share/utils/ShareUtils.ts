/**
 * Utilities for sharing sequences and generating shareable URLs
 * Main export file that re-exports all functionality from specialized modules
 */

// Re-export types
export type { ShareData } from './types.js';
export type { SequenceRenderResult } from './ImageUtils.js';
export type { ShareOptions } from './ShareHandler.js';
export type { DownloadOptions } from './DownloadHandler.js';
export type { SequenceRenderOptions } from './SequenceRenderer.js';

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
} from './SequenceEncoder.js';

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
} from './SequenceDecoder.js';

export {
	// Web Share API utilities
	isWebShareSupported,
	isFileShareSupported,
	isMobileDevice,
	shareSequence as shareSequenceWithWebShareApi,
	shareSequenceWithImage
} from './WebShareApi.js';

export {
	// Clipboard operations
	copyToClipboard,
	copyImageToClipboard
} from './ClipboardUtils.js';

export {
	// URL utilities
	generateShareableUrl,
	checkForSequenceInUrl
} from './UrlUtils.js';

export {
	// Image utilities
	dataURLtoBlob,
	createFileFromDataURL
} from './ImageUtils.js';

export {
	// Test utilities
	testSequenceUrlEncoding
} from './TestUtils.js';

export {
	// Element finder utilities
	findBeatFrameElement,
	listenForBeatFrameElement
} from './ElementFinder.js';

export {
	// Sequence renderer utilities
	renderSequence
} from './SequenceRenderer.js';

export {
	// Share handler utilities
	shareSequence
} from './ShareHandler.js';

export {
	// Download handler utilities
	downloadSequenceImage
} from './DownloadHandler.js';
