// Share utils stub
export function isWebShareSupported() {
  return typeof navigator !== 'undefined' && 'share' in navigator;
}