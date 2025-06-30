# TKA Option Picker Performance Fix
# Remove sequential loading, make options appear immediately

# 1. MAIN FIX: Update OptionPickerDisplayManager._batch_update_beat_display()

def _batch_update_beat_display(self, beat_options: List[BeatData]) -> None:
    """FIXED: True batch update with no sequential delays"""
    from domain.models.letter_type_classifier import LetterTypeClassifier

    # Step 1: Clear all sections in one pass (keep this)
    for section in self._sections.values():
        section.clear_pictographs_pool_style()

    # Step 2: Pre-categorize beats by letter type (keep this) 
    beats_by_type = {}
    for i, beat in enumerate(beat_options):
        if i >= self.pool_manager.get_pool_size():
            break
        if beat.letter:
            letter_type = LetterTypeClassifier.get_letter_type(beat.letter)
            if letter_type in self._sections:
                if letter_type not in beats_by_type:
                    beats_by_type[letter_type] = []
                beats_by_type[letter_type].append((i, beat))

    # Step 3: FIXED - True batch update with no intermediate sizing
    for letter_type, beat_list in beats_by_type.items():
        target_section = self._sections[letter_type]
        
        # BATCH ALL FRAME PREPARATIONS FIRST
        prepared_frames = []
        for pool_index, beat in beat_list:
            frame = self.pool_manager.get_pictograph_from_pool(pool_index)
            if frame:
                # Update frame data without triggering layout
                frame.update_beat_data(beat)
                frame.setParent(target_section.section_pictograph_container)
                prepared_frames.append(frame)
        
        # BATCH ADD ALL FRAMES TO SECTION AT ONCE
        target_section.add_multiple_pictographs_from_pool(prepared_frames)

# 2. NEW METHOD: Add to OptionPickerSection class
def add_multiple_pictographs_from_pool(self, pictograph_frames):
    """BATCH add multiple pictographs without intermediate updates"""
    # Defer sizing until all frames are added
    self.layout_manager.defer_sizing_updates()
    
    try:
        for frame in pictograph_frames:
            # Add without triggering size updates
            self.section_pictograph_container.add_pictograph(frame)
        
        # Single size update at the end
        self.layout_manager.update_size_once()
        
    finally:
        self.layout_manager.resume_sizing_updates()

# 3. UPDATE: SectionLayoutManager to support deferred updates
class SectionLayoutManager:
    def __init__(self, section_widget):
        self.section = section_widget
        self._sizing_deferred = False  # ADD THIS
        # ... existing code ...
    
    def defer_sizing_updates(self):
        """Defer sizing updates for batch operations"""
        self._sizing_deferred = True
    
    def resume_sizing_updates(self):
        """Resume sizing updates"""
        self._sizing_deferred = False
    
    def update_size_once(self):
        """Force a single size update"""
        if not self._sizing_deferred:
            self._update_size()
    
    def add_pictograph_from_pool(self, pictograph_frame):
        """MODIFIED: Skip sizing if deferred"""
        if not self._sizing_deferred:
            self._ensure_container_ready()
        
        self.section.section_pictograph_container.sync_width_with_section()
        self.section.section_pictograph_container.add_pictograph(pictograph_frame)
        
        if not self._sizing_deferred:
            self._update_size()

# 4. REMOVE: ProcessEvents calls in _ensure_container_ready
def _ensure_container_ready(self):
    """FIXED: Remove forced event processing"""
    if self.section.parent():
        widget = self.section.parent()
        while widget:
            if (
                hasattr(widget, "__class__")
                and "ModernOptionPickerWidget" in widget.__class__.__name__
            ):
                widget.updateGeometry()
                # REMOVED: QApplication.processEvents()  ← THIS WAS CAUSING DELAYS
                break
            elif (
                hasattr(widget, "layout")
                and widget.layout()
                and widget.layout().__class__.__name__ == "QVBoxLayout"
                and widget.width() > 500
            ):
                widget.updateGeometry()
                # REMOVED: QApplication.processEvents()  ← THIS WAS CAUSING DELAYS
                break
            widget = widget.parent()
