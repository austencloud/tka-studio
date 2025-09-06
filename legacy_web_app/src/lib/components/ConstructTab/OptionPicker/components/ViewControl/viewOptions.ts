import type { ViewOption } from './types';

// Enhanced view options with better icons and descriptions
export const viewOptions: readonly ViewOption[] = [
    {
        value: 'all',
        label: 'All',
        icon: '✨',
        isSortMethod: false,
        description: 'Show all valid options'
    },
    {
        value: 'type',
        label: 'Type',
        icon: '📁',
        isSortMethod: true,
        description: 'Group options by type'
    },
    {
        value: 'endPosition',
        label: 'End',
        icon: '🏁',
        isSortMethod: true,
        description: 'Group by ending position'
    },
    {
        value: 'reversals',
        label: 'Reversals',
        icon: '🔄',
        isSortMethod: true,
        description: 'Group by reversals'
    }
];
