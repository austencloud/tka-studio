/**
 * Act model - represents a choreography act with sequences, beats, cues, and timestamps
 */

export interface Beat {
  beat_number?: number;
  pictograph_data?: any;
  step_label?: string;
  is_filled?: boolean;
}

export interface Sequence {
  sequence_start_marker: boolean;
  cue: string;
  timestamp: string;
  beats: Beat[];
  sequence_length?: number;
}

export interface Act {
  title: string;
  prop_type: string;
  sequences: Sequence[];
}

/**
 * Creates a default empty act structure
 */
export function createEmptyAct(rows: number = 24, columns: number = 8): Act {
  const sequences: Sequence[] = [];

  for (let row = 0; row < rows; row++) {
    const sequence: Sequence = {
      sequence_start_marker: row === 0,
      cue: "",
      timestamp: "",
      beats: Array(columns).fill(null).map(() => ({
        step_label: "",
        is_filled: false
      }))
    };
    sequences.push(sequence);
  }

  return {
    title: "Act",
    prop_type: "Staff",
    sequences
  };
}
