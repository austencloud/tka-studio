// Sequence persistence utilities
export function isSequenceEmpty(sequence) {
  if (!sequence) return true;
  if (!sequence.beats) return true;
  return sequence.beats.length === 0;
}

export function saveSequence(sequence) {
  if (typeof localStorage !== 'undefined') {
    localStorage.setItem('tka_current_sequence', JSON.stringify(sequence));
  }
}

export function loadSequence() {
  if (typeof localStorage !== 'undefined') {
    const saved = localStorage.getItem('tka_current_sequence');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch (e) {
        console.warn('Failed to parse saved sequence:', e);
      }
    }
  }
  return null;
}

export function clearSavedSequence() {
  if (typeof localStorage !== 'undefined') {
    localStorage.removeItem('tka_current_sequence');
  }
}
