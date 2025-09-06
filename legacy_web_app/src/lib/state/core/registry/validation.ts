/**
 * Validation utilities for the state registry
 */

/**
 * Validate a machine snapshot to ensure it has the expected structure
 */
export function validateMachineSnapshot(snapshot: any): boolean {
  // Basic structure validation for XState machine snapshots
  return (
    snapshot &&
    typeof snapshot === 'object' &&
    'status' in snapshot &&
    typeof snapshot.status === 'string' &&
    ['active', 'done', 'error', 'stopped'].includes(snapshot.status) &&
    'context' in snapshot &&
    typeof snapshot.context === 'object'
  );
}

/**
 * Validate store data to ensure it's safe to use
 * This can be extended with more specific validation logic as needed
 */
export function validateStoreData<T>(data: any): data is T {
  // Basic validation to check if the data is not undefined or corrupted
  return data !== undefined && data !== null;
}

/**
 * Validate the overall structure of persisted data
 */
export function validatePersistedDataStructure(data: any): boolean {
  return typeof data === 'object' && data !== null;
}
