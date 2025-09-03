import type { SortMethod } from '../../config';

export type ViewModeDetail = { mode: 'all' } | { mode: 'group'; method: SortMethod };

export type ViewOption = {
    value: string;
    label: string;
    icon: string;
    isSortMethod: boolean;
    description: string;
};
