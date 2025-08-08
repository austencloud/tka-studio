// LZ String compression utilities
export function compressString(str) {
  return btoa(str); // Simple base64 encoding as placeholder
}

export function decompressString(compressed) {
  try {
    return atob(compressed); // Simple base64 decoding as placeholder
  } catch {
    return '';
  }
}