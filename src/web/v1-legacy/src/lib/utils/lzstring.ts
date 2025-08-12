/**
 * LZString Utility Module
 * 
 * This module provides a centralized way to access the LZString library
 * with proper error handling and performance optimizations.
 */

import { browser } from '$app/environment';
import { logger } from '$lib/core/logging';

// Type definition for LZString
interface LZStringInterface {
  compressToBase64: (input: string) => string;
  decompressFromBase64: (input: string) => string | null;
  compressToUTF16: (input: string) => string;
  decompressFromUTF16: (input: string) => string | null;
  compressToUint8Array: (input: string) => Uint8Array;
  decompressFromUint8Array: (input: Uint8Array) => string | null;
  compressToEncodedURIComponent: (input: string) => string;
  decompressFromEncodedURIComponent: (input: string) => string | null;
  compress: (input: string) => string;
  decompress: (input: string) => string | null;
}

// Static import for better performance and reliability
// This will be tree-shaken if not used
let lzStringModule: LZStringInterface | null = null;

// Flag to track if we've already attempted to load the module
let hasAttemptedLoad = false;

// Flag to track if we've logged the error
let hasLoggedError = false;

/**
 * Initialize the LZString module
 * This is called automatically when needed, but can be called explicitly
 * to preload the module
 */
export async function initLZString(): Promise<void> {
  // Only attempt to load in browser environment
  if (!browser) return;

  // Only attempt to load once
  if (hasAttemptedLoad) return;
  
  hasAttemptedLoad = true;

  try {
    // Import the module
    const module = await import('lz-string');
    lzStringModule = module.default;
    logger.debug('LZString module loaded successfully');
  } catch (error) {
    if (!hasLoggedError) {
      logger.error('Failed to load LZString module', {
        error: error instanceof Error ? error : new Error(String(error))
      });
      hasLoggedError = true;
    }
  }
}

/**
 * Get the LZString module
 * This will attempt to load the module if it hasn't been loaded yet
 * 
 * @returns The LZString module or null if not available
 */
export async function getLZString(): Promise<LZStringInterface | null> {
  if (!browser) return null;
  
  // If we haven't loaded the module yet, try to load it
  if (!lzStringModule && !hasAttemptedLoad) {
    await initLZString();
  }
  
  return lzStringModule;
}

/**
 * Compress a string using LZString
 * 
 * @param input The string to compress
 * @returns The compressed string or the original if compression failed
 */
export async function compressString(input: string): Promise<string> {
  if (!browser || !input) return input;
  
  const lzString = await getLZString();
  if (!lzString) return input;
  
  try {
    const compressed = lzString.compressToEncodedURIComponent(input);
    if (compressed && compressed.length < input.length) {
      return compressed;
    }
  } catch (error) {
    logger.warn('LZString compression failed, using uncompressed format', {
      error: error instanceof Error ? error : new Error(String(error))
    });
  }
  
  return input;
}

/**
 * Decompress a string using LZString
 * 
 * @param input The string to decompress
 * @returns The decompressed string or the original if decompression failed
 */
export async function decompressString(input: string): Promise<string> {
  if (!browser || !input) return input;
  
  const lzString = await getLZString();
  if (!lzString) return input;
  
  try {
    // Try to decompress
    const decompressed = lzString.decompressFromEncodedURIComponent(input);
    if (decompressed) {
      return decompressed;
    }
  } catch (error) {
    logger.warn('LZString decompression failed, using original format', {
      error: error instanceof Error ? error : new Error(String(error))
    });
  }
  
  return input;
}

// Initialize the module immediately in browser environments
// This helps ensure it's ready when needed
if (browser) {
  // Use setTimeout to defer the initialization until after critical resources are loaded
  setTimeout(() => {
    initLZString().catch(() => {
      // Error is already logged in initLZString
    });
  }, 1000);
}
