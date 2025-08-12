/**
 * Hardcoded Dictionary Service
 * 
 * Provides example sequences for testing the animator while we implement Phase 2.
 * This contains sample sequence data to demonstrate the animation functionality.
 */

import type { SequenceData, DictionaryItem } from '../../types/core.js';

// Example sequence data for testing
const EXAMPLE_SEQUENCE_ABC: SequenceData = [
  {
    id: 'example-abc',
    word: 'ABC',
    author: 'Example Author',
    level: 1,
    grid_mode: 'grid'
  },
  {
    beat: 1,
    letter: 'A',
    blue_attributes: {
      start_loc: 'center',
      end_loc: 'right',
      motion_type: 'pro',
      prop_rot_dir: 'cw',
      turns: 1,
      start_ori: 'in',
      end_ori: 'out'
    },
    red_attributes: {
      start_loc: 'center',
      end_loc: 'left',
      motion_type: 'anti',
      prop_rot_dir: 'ccw',
      turns: 1,
      start_ori: 'in',
      end_ori: 'out'
    }
  },
  {
    beat: 2,
    letter: 'B',
    blue_attributes: {
      start_loc: 'right',
      end_loc: 'center',
      motion_type: 'pro',
      prop_rot_dir: 'no_rot',
      turns: 0,
      start_ori: 'out',
      end_ori: 'in'
    },
    red_attributes: {
      start_loc: 'left',
      end_loc: 'center',
      motion_type: 'anti',
      prop_rot_dir: 'no_rot',
      turns: 0,
      start_ori: 'out',
      end_ori: 'in'
    }
  },
  {
    beat: 3,
    letter: 'C',
    blue_attributes: {
      start_loc: 'center',
      end_loc: 'top',
      motion_type: 'static',
      prop_rot_dir: 'no_rot',
      turns: 0,
      start_ori: 'in',
      end_ori: 'in'
    },
    red_attributes: {
      start_loc: 'center',
      end_loc: 'bottom',
      motion_type: 'static',
      prop_rot_dir: 'no_rot',
      turns: 0,
      start_ori: 'in',
      end_ori: 'in'
    }
  }
];

const EXAMPLE_SEQUENCE_XYZ: SequenceData = [
  {
    id: 'example-xyz',
    word: 'XYZ',
    author: 'Test Author',
    level: 2,
    grid_mode: 'grid'
  },
  {
    beat: 1,
    letter: 'X',
    blue_attributes: {
      start_loc: 'center',
      end_loc: 'top_right',
      motion_type: 'pro',
      prop_rot_dir: 'cw',
      turns: 2,
      start_ori: 'in',
      end_ori: 'out'
    },
    red_attributes: {
      start_loc: 'center',
      end_loc: 'bottom_left',
      motion_type: 'anti',
      prop_rot_dir: 'ccw',
      turns: 2,
      start_ori: 'in',
      end_ori: 'out'
    }
  },
  {
    beat: 2,
    letter: 'Y',
    blue_attributes: {
      start_loc: 'top_right',
      end_loc: 'center',
      motion_type: 'dash',
      prop_rot_dir: 'no_rot',
      turns: 0,
      start_ori: 'out',
      end_ori: 'in'
    },
    red_attributes: {
      start_loc: 'bottom_left',
      end_loc: 'center',
      motion_type: 'dash',
      prop_rot_dir: 'no_rot',
      turns: 0,
      start_ori: 'out',
      end_ori: 'in'
    }
  },
  {
    beat: 3,
    letter: 'Z',
    blue_attributes: {
      start_loc: 'center',
      end_loc: 'left',
      motion_type: 'fl',
      prop_rot_dir: 'cw',
      turns: 'fl' as any,
      start_ori: 'in',
      end_ori: 'clock'
    },
    red_attributes: {
      start_loc: 'center',
      end_loc: 'right',
      motion_type: 'fl',
      prop_rot_dir: 'ccw',
      turns: 'fl' as any,
      start_ori: 'in',
      end_ori: 'counter'
    }
  }
];

// Export example sequences for use in the app
export const EXAMPLE_SEQUENCES: DictionaryItem[] = [
  {
    id: 'example-abc',
    name: 'Example ABC Sequence',
    filePath: '/examples/abc.json',
    metadata: EXAMPLE_SEQUENCE_ABC[0],
    sequenceData: EXAMPLE_SEQUENCE_ABC,
    thumbnailUrl: '/static/example-abc-thumbnail.png',
    versions: ['1.0']
  },
  {
    id: 'example-xyz',
    name: 'Example XYZ Sequence',
    filePath: '/examples/xyz.json',
    metadata: EXAMPLE_SEQUENCE_XYZ[0],
    sequenceData: EXAMPLE_SEQUENCE_XYZ,
    thumbnailUrl: '/static/example-xyz-thumbnail.png',
    versions: ['1.0']
  }
];

// Helper function to get a specific example sequence
export function getExampleSequence(id: string): SequenceData | null {
  const item = EXAMPLE_SEQUENCES.find(seq => seq.id === id);
  return item ? item.sequenceData : null;
}

// Helper function to get all example sequence names
export function getExampleSequenceNames(): string[] {
  return EXAMPLE_SEQUENCES.map(seq => seq.name);
}
