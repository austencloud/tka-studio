/**
 * Hybrid Dictionary Service
 * 
 * Temporary service to get the animator running while we implement Phase 2.
 * This will be replaced with proper web app integration in later phases.
 */

import type { DictionaryItem, DictionaryIndex, SequenceData } from '../../types/core.js';

export class HybridDictionaryService {
  private static instance: HybridDictionaryService | null = null;
  private index: DictionaryIndex | null = null;
  private items: DictionaryItem[] = [];

  private constructor() {
    // Private constructor for singleton
  }

  static getInstance(): HybridDictionaryService {
    if (!HybridDictionaryService.instance) {
      HybridDictionaryService.instance = new HybridDictionaryService();
    }
    return HybridDictionaryService.instance;
  }

  async getIndex(): Promise<DictionaryIndex> {
    if (this.index) {
      return this.index;
    }

    // For now, create a minimal index with sample data
    // In Phase 2, this will be replaced with web app integration
    this.index = {
      items: await this.loadSampleItems(),
      categories: ['Sample', 'Test'],
      totalCount: 2,
      lastUpdated: new Date()
    };

    return this.index;
  }

  async searchItems(query: string, category?: string): Promise<DictionaryItem[]> {
    const index = await this.getIndex();
    let results = index.items;

    // Filter by category if specified
    if (category && category !== 'All') {
      results = results.filter(item => 
        item.metadata.author === category || 
        item.name.includes(category)
      );
    }

    // Filter by search query
    if (query.trim()) {
      const lowerQuery = query.toLowerCase();
      results = results.filter(item =>
        item.name.toLowerCase().includes(lowerQuery) ||
        item.metadata.word?.toLowerCase().includes(lowerQuery) ||
        item.metadata.author?.toLowerCase().includes(lowerQuery)
      );
    }

    return results;
  }

  private async loadSampleItems(): Promise<DictionaryItem[]> {
    // Create sample sequence data for testing
    const sampleSequence1: SequenceData = [
      {
        id: 'sample-1',
        word: 'ABC',
        author: 'Sample Author',
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
      }
    ];

    const sampleSequence2: SequenceData = [
      {
        id: 'sample-2',
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

    return [
      {
        id: 'sample-1',
        name: 'Sample Sequence ABC',
        filePath: '/sample/abc.json',
        metadata: sampleSequence1[0],
        sequenceData: sampleSequence1,
        thumbnailUrl: '/static/sample-thumbnail-1.png',
        versions: ['1.0']
      },
      {
        id: 'sample-2',
        name: 'Test Sequence XYZ',
        filePath: '/sample/xyz.json',
        metadata: sampleSequence2[0],
        sequenceData: sampleSequence2,
        thumbnailUrl: '/static/sample-thumbnail-2.png',
        versions: ['1.0']
      }
    ];
  }
}
