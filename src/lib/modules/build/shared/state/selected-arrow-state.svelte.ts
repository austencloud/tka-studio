/**
 * Selected Arrow State
 *
 * TEMPORARY STUB for Session B development
 * Session A will replace this with the real implementation
 *
 * Manages the currently selected arrow in the pictograph adjustment editor
 */

import type { MotionData, PictographData } from "$shared";

interface SelectedArrow {
  motionData: MotionData;
  color: string;
  pictographData: PictographData;
}

// CRITICAL FIX: Use plain JavaScript object instead of $state
// This state doesn't need Svelte reactivity - it's just a simple container.
// Using $state at module-level caused issues when DevTools was open during refresh
// because module loading timing changes and $state can't be used outside components.
let _selectedArrow: SelectedArrow | null = null;

export const selectedArrowState = {
  get selectedArrow() {
    return _selectedArrow;
  },

  selectArrow(motionData: MotionData, color: string, pictographData: PictographData) {
    _selectedArrow = { motionData, color, pictographData };
    console.log('[SelectedArrowState STUB] Arrow selected:', color, motionData.motionType);
  },

  clearSelection() {
    _selectedArrow = null;
    console.log('[SelectedArrowState STUB] Selection cleared');
  },

  isSelected(motionData: MotionData, color: string): boolean {
    if (!_selectedArrow) return false;
    return (
      _selectedArrow.color === color &&
      _selectedArrow.motionData.motionType === motionData.motionType &&
      _selectedArrow.motionData.startLocation === motionData.startLocation &&
      _selectedArrow.motionData.endLocation === motionData.endLocation
    );
  }
};
