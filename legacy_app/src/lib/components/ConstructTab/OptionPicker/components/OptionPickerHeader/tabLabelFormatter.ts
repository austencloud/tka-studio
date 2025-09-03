// src/lib/components/ConstructTab/OptionPicker/components/OptionPickerHeader/tabLabelFormatter.ts
import type { TabLabelMappings } from './types';

// Mappings for tab labels
export const tabLabelMappings: TabLabelMappings = {
  long: {
    Type1: 'Type 1',
    Type2: 'Type 2',
    Type3: 'Type 3',
    Type4: 'Type 4',
    Type5: 'Type 5',
    Type6: 'Type 6',
    'Unknown Type': 'Unknown',
    alpha: 'Alpha',
    beta: 'Beta',
    gamma: 'Gamma',
    Continuous: 'Continuous',
    'One Reversal': 'One Reversal',
    'Two Reversals': 'Two Reversals'
  },
  short: {
    Type1: '1',
    Type2: '2',
    Type3: '3',
    Type4: '4',
    Type5: '5',
    Type6: '6',
    'Unknown Type': '?',
    alpha: 'α',
    beta: 'β',
    gamma: 'Γ',
    Continuous: 'Cont.',
    'One Reversal': '1 Rev.',
    'Two Reversals': '2 Rev.'
  }
};

/**
 * Formats a tab name using the long format
 * @param key The tab key to format
 * @returns The formatted tab name
 */
export function formatTabName(key: string): string {
  if (!key) return '';
  return (
    tabLabelMappings.long[key] ||
    key
      .replace(/([A-Z])/g, ' $1')
      .trim()
      .replace(/^\w/, (c) => c.toUpperCase())
  );
}

/**
 * Formats a tab name using the short format
 * @param key The tab key to format
 * @returns The formatted tab name
 */
export function formatShortTabName(key: string): string {
  if (!key) return '';
  return tabLabelMappings.short[key] || formatTabName(key);
}
