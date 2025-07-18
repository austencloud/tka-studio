# Sequence Card Tab: UI/UX Design Preservation Guide

## Visual Design Philosophy

The legacy sequence card tab has a sophisticated, modern design with:

- **Dark theme** with gradient backgrounds and glass-morphism effects
- **Clean typography** with careful font sizing and spacing
- **Smooth animations** and hover effects
- **Intuitive navigation** with clear visual hierarchy
- **Professional polish** with rounded corners and subtle shadows

## Detailed Component Design Specifications

### 1. Header Component Design

#### Visual Characteristics:

```python
HEADER_STYLING = {
    'background': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #34495e, stop:1 #2c3e50)',
    'border_radius': '10px',
    'border': '1px solid #4a5568',
    'padding': '20px 15px',
    'spacing': '8px'
}

HEADER_TITLE = {
    'text': 'Sequence Card Manager',
    'font_size': '18px',
    'font_weight': 'bold',
    'color': '#ffffff',
    'letter_spacing': '0.5px',
    'alignment': 'center'
}

HEADER_DESCRIPTION = {
    'text': 'Select a sequence length to view cards',
    'font_size': '13px',
    'font_style': 'italic',
    'color': '#bdc3c7',
    'alignment': 'center'
}

HEADER_BUTTONS = {
    'background': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3498db, stop:1 #2980b9)',
    'hover_background': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5dade2, stop:1 #3498db)',
    'pressed_background': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2980b9, stop:1 #1f618d)',
    'color': 'white',
    'border': '1px solid #5dade2',
    'border_radius': '6px',
    'padding': '8px 16px',
    'font_weight': '600',
    'font_size': '12px',
    'min_width': '100px',
    'cursor': 'pointing_hand'
}

PROGRESS_BAR = {
    'height': '12px',
    'border_radius': '6px',
    'background': 'rgba(0, 0, 0, 0.15)',
    'chunk_background': '#3498db',
    'text_color': 'rgba(255, 255, 255, 0.9)',
    'text_font_size': '10px',
    'text_font_weight': 'bold'
}
```

#### Layout Structure:

```
┌─────────────────────────────────────────┐
│              Header Component            │ ← Fixed height ~120px
├─────────────────────────────────────────┤
│         Sequence Card Manager           │ ← Title (18px, bold, white)
│    Select a sequence length to view...  │ ← Description (13px, italic, gray)
│                                         │
│  [Progress Bar - Hidden by default]     │ ← Only visible during loading
│                                         │
│ [Export] [Refresh] [Regenerate Images]  │ ← Action buttons (centered)
└─────────────────────────────────────────┘
```

### 2. Navigation Sidebar Design

#### Visual Characteristics:

```python
SIDEBAR_STYLING = {
    'width': '200px',  # Fixed width
    'background': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(71, 85, 105, 0.4), stop:1 rgba(51, 65, 85, 0.6))',
    'border_radius': '12px',
    'border': '1px solid rgba(100, 116, 139, 0.3)',
    'padding': '10px'
}

SIDEBAR_HEADER = {
    'background': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(71, 85, 105, 0.5), stop:1 rgba(51, 65, 85, 0.7))',
    'border_radius': '10px',
    'border': '1px solid rgba(100, 116, 139, 0.4)',
    'title_color': '#f8fafc',
    'title_font_size': '16px',
    'title_font_weight': 'bold',
    'title_letter_spacing': '0.5px',
    'subtitle_color': '#cbd5e1',
    'subtitle_font_size': '12px',
    'subtitle_font_style': 'italic'
}

LENGTH_BUTTON_UNSELECTED = {
    'background': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(71, 85, 105, 0.3), stop:1 rgba(51, 65, 85, 0.5))',
    'border': '1px solid rgba(100, 116, 139, 0.4)',
    'border_radius': '10px',
    'margin': '3px'
}

LENGTH_BUTTON_HOVER = {
    'background': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(100, 116, 139, 0.4), stop:1 rgba(71, 85, 105, 0.6))',
    'border': '1px solid rgba(148, 163, 184, 0.5)'
}

LENGTH_BUTTON_SELECTED = {
    'background': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3b82f6, stop:1 #2563eb)',
    'border': '1px solid #60a5fa',
    'border_radius': '10px',
    'margin': '3px'
}

COLUMN_SELECTOR = {
    'dropdown_height': '32px',
    'dropdown_background': 'rgba(71, 85, 105, 0.6)',
    'dropdown_border': '1px solid rgba(100, 116, 139, 0.5)',
    'dropdown_border_radius': '8px',
    'label_font_size': 'responsive 11-13px',
    'label_font_weight': 'medium',
    'label_color': '#f8fafc'
}
```

#### Layout Structure:

```
┌─────────────┐
│   Sidebar   │ ← Fixed width 200px, full height
├─────────────┤
│   HEADER    │ ← Title + subtitle
├─────────────┤
│  Length     │ ← Scrollable area
│  Options:   │
│  [ All ]    │ ← Always at top
│  [ 2 ]      │
│  [ 3 ]      │
│  [ 4 ]      │
│  [ 5 ]      │
│  [ 6 ]      │
│  [ 8 ]      │
│  [ 10 ]     │
│  [ 12 ]     │
│  [ 16 ]     │ ← Default selection
├─────────────┤
│ Preview     │ ← Bottom section
│ Columns:    │
│ [Dropdown]  │ ← 2,3,4,5,6 options
└─────────────┘
```

### 3. Content Display Area Design

#### Visual Characteristics:

```python
CONTENT_AREA_STYLING = {
    'background': 'transparent',
    'border': 'none',
    'scroll_bar_width': '8px',
    'scroll_bar_background': 'rgba(0,0,0,0.1)',
    'scroll_bar_handle': 'rgba(0,0,0,0.3)',
    'scroll_bar_handle_hover': 'rgba(0,0,0,0.5)',
    'scroll_bar_border_radius': '4px'
}

SEQUENCE_CARD_PAGE = {
    'background': 'white',
    'border': '1px solid #ddd',
    'border_radius': '8px',
    'spacing': '10px',
    'margin': '10px',
    'shadow': 'subtle drop shadow'
}

GRID_LAYOUT = {
    'columns_per_row': 'user_configurable (2-6)',
    'page_spacing': '20px',
    'responsive_scaling': True,
    'maintain_aspect_ratio': True
}
```

#### Layout Structure:

```
┌──────────────────────────────────────────────┐
│              Content Display Area             │
├──────────────────────────────────────────────┤
│  ┌────────┐ ┌────────┐ ┌────────┐           │ ← Multiple pages per row
│  │ Page 1 │ │ Page 2 │ │ Page 3 │           │   (2-6 columns configurable)
│  │        │ │        │ │        │           │
│  │ [Grid] │ │ [Grid] │ │ [Grid] │           │ ← Each page contains grid
│  │        │ │        │ │        │           │   of sequence card images
│  └────────┘ └────────┘ └────────┘           │
│                                              │
│  ┌────────┐ ┌────────┐ ┌────────┐           │
│  │ Page 4 │ │ Page 5 │ │ Page 6 │           │
│  │        │ │        │ │        │           │
│  │ [Grid] │ │ [Grid] │ │ [Grid] │           │
│  │        │ │        │ │        │           │
│  └────────┘ └────────┘ └────────┘           │
│                                              │
│              [Scrollable content]            │
└──────────────────────────────────────────────┘
```

## Modern Implementation with Visual Preservation

### Component Mapping Strategy

```python
# Modern Architecture -> Legacy Visual Design Mapping

class ModernSequenceCardView(QWidget):
    """Main container preserving exact legacy layout"""

    def __init__(self):
        super().__init__()
        self._preserve_legacy_layout()
        self._apply_legacy_styling()

    def _preserve_legacy_layout(self):
        # Exact same layout structure as legacy
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        # Header component - exact styling preserved
        self.header = ModernHeaderComponent(self)
        self.main_layout.addWidget(self.header)

        # Content layout - exact same structure
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(15)

        # Sidebar - exact same width and styling
        self.sidebar = ModernNavigationComponent(self)
        self.sidebar.setFixedWidth(200)
        self.sidebar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        # Content area - exact same scroll behavior
        self.content_area = ModernContentComponent(self)

        self.content_layout.addWidget(self.sidebar, 0)
        self.content_layout.addWidget(self.content_area.scroll_area, 1)
        self.main_layout.addLayout(self.content_layout, 1)


class ModernHeaderComponent(QFrame):
    """Preserves exact header styling and behavior"""

    def __init__(self, parent):
        super().__init__(parent)
        self._apply_exact_legacy_styling()
        self._create_exact_legacy_layout()

    def _apply_exact_legacy_styling(self):
        # Copy exact CSS from legacy header
        self.setObjectName("sequenceCardHeader")
        self.setStyleSheet("""
            #sequenceCardHeader {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #34495e, stop:1 #2c3e50);
                border-radius: 10px;
                border: 1px solid #4a5568;
            }
        """)

    def _create_exact_legacy_layout(self):
        # Exact same layout logic as legacy
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(8)

        self.title_label = self._create_title()
        self.description_label = self._create_description()
        self.progress_container = self._create_progress()
        self.button_layout = self._create_buttons()

        # Exact same order and structure
        layout.addWidget(self.title_label)
        layout.addWidget(self.description_label)
        layout.addWidget(self.progress_container)
        layout.addLayout(self.button_layout)


class ModernNavigationComponent(QWidget):
    """Preserves exact sidebar styling and interactions"""

    def __init__(self, parent):
        super().__init__(parent)
        self._apply_exact_legacy_styling()
        self._create_exact_legacy_components()

    def _apply_exact_legacy_styling(self):
        # Import exact styling from SidebarStyler
        from legacy.components.navigation.sidebar_styler import SidebarStyler
        SidebarStyler.apply_modern_styling(self)

    def _create_exact_legacy_components(self):
        # Exact same component structure
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(12)

        # Same header
        self.header = self._create_sidebar_header()
        main_layout.addWidget(self.header)

        # Same length selection area
        self.length_scroll_area = self._create_length_scroll_area()
        main_layout.addWidget(self.length_scroll_area, 1)

        # Same column selector
        self.column_selector = self._create_column_selector()
        main_layout.addWidget(self.column_selector)
```

### Style Preservation Strategy

#### 1. Direct CSS Import

```python
# Import exact stylesheets from legacy components
from legacy.components.navigation.sidebar_styler import SidebarStyler
from legacy.components.styles import HEADER_STYLES, BUTTON_STYLES

class ModernComponent(QWidget):
    def __init__(self):
        super().__init__()
        # Apply exact legacy styling
        SidebarStyler.apply_modern_styling(self)
        self.setStyleSheet(HEADER_STYLES)
```

#### 2. Color Palette Preservation

```python
LEGACY_COLOR_PALETTE = {
    # Header colors
    'header_gradient_start': '#34495e',
    'header_gradient_end': '#2c3e50',
    'header_border': '#4a5568',
    'header_title': '#ffffff',
    'header_description': '#bdc3c7',

    # Button colors
    'button_gradient_start': '#3498db',
    'button_gradient_end': '#2980b9',
    'button_hover_start': '#5dade2',
    'button_hover_end': '#3498db',
    'button_border': '#5dade2',

    # Sidebar colors
    'sidebar_background_start': 'rgba(71, 85, 105, 0.4)',
    'sidebar_background_end': 'rgba(51, 65, 85, 0.6)',
    'sidebar_border': 'rgba(100, 116, 139, 0.3)',

    # Selection colors
    'selection_gradient_start': '#3b82f6',
    'selection_gradient_end': '#2563eb',
    'selection_border': '#60a5fa',

    # Progress bar
    'progress_background': 'rgba(0, 0, 0, 0.15)',
    'progress_chunk': '#3498db'
}
```

#### 3. Animation and Interaction Preservation

```python
class ModernComponentWithAnimations(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_hover_animations()
        self._setup_selection_animations()
        self._setup_loading_animations()

    def _setup_hover_animations(self):
        # Preserve exact hover effects from legacy
        self.setStyleSheet("""
            QFrame:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(100, 116, 139, 0.4),
                    stop:1 rgba(71, 85, 105, 0.6));
                border: 1px solid rgba(148, 163, 184, 0.5);
            }
        """)

    def enterEvent(self, event):
        # Preserve exact hover behavior
        super().enterEvent(event)
        # Add any custom hover logic here

    def leaveEvent(self, event):
        # Preserve exact leave behavior
        super().leaveEvent(event)
```

### Responsive Design Preservation

#### Font Scaling Logic

```python
def calculate_responsive_font_size(widget_width: int, base_size: int, min_size: int, max_size: int) -> int:
    """Preserve exact font scaling logic from legacy"""
    # Direct port of legacy calculation
    calculated_size = min(max(base_size, int(widget_width / 15)), max_size)
    return max(calculated_size, min_size)

class ResponsiveComponent(QWidget):
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Preserve exact resize behavior
        new_width = event.size().width()

        # Update font sizes using legacy logic
        for label in self.findChildren(QLabel):
            current_font = label.font()
            new_size = calculate_responsive_font_size(new_width, 12, 10, 14)
            current_font.setPointSize(new_size)
            label.setFont(current_font)
```

### Visual Regression Testing Setup

#### Screenshot Comparison Framework

```python
import pytest
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication

class VisualRegressionTest:
    def __init__(self):
        self.reference_images_path = "tests/visual_regression/reference/"
        self.tolerance = 0.95  # 95% similarity required

    def capture_component_screenshot(self, component, name: str) -> QPixmap:
        """Capture screenshot of component for comparison"""
        pixmap = component.grab()
        pixmap.save(f"tests/visual_regression/current/{name}.png")
        return pixmap

    def compare_with_legacy(self, component, component_name: str) -> bool:
        """Compare modern component with legacy reference"""
        current_pixmap = self.capture_component_screenshot(component, component_name)
        reference_path = f"{self.reference_images_path}{component_name}.png"

        # Implement pixel comparison logic
        similarity = self._calculate_similarity(current_pixmap, reference_path)
        return similarity >= self.tolerance

@pytest.fixture
def visual_tester():
    return VisualRegressionTest()

def test_header_visual_parity(qtbot, visual_tester):
    """Test that modern header looks identical to legacy"""
    header = ModernHeaderComponent(None)
    qtbot.addWidget(header)

    # Ensure component is fully rendered
    qtbot.waitExposed(header)
    QApplication.processEvents()

    # Compare with legacy reference
    assert visual_tester.compare_with_legacy(header, "header_component")

def test_sidebar_visual_parity(qtbot, visual_tester):
    """Test that modern sidebar looks identical to legacy"""
    sidebar = ModernNavigationComponent(None)
    qtbot.addWidget(sidebar)

    qtbot.waitExposed(sidebar)
    QApplication.processEvents()

    assert visual_tester.compare_with_legacy(sidebar, "navigation_sidebar")
```

### User Experience Preservation Checklist

#### Interaction Patterns

- [ ] **Click Response**: Exact same button press/release visual feedback
- [ ] **Hover Effects**: Identical color transitions and timing
- [ ] **Selection Behavior**: Same visual feedback for selected items
- [ ] **Scrolling**: Identical scroll bar appearance and behavior
- [ ] **Keyboard Navigation**: Same tab order and key bindings
- [ ] **Loading States**: Identical progress bar animations and messages

#### Layout Behavior

- [ ] **Window Resizing**: Same responsive scaling behavior
- [ ] **Component Proportions**: Exact same relative sizing
- [ ] **Spacing and Margins**: Pixel-perfect recreation
- [ ] **Font Rendering**: Identical text appearance and scaling
- [ ] **Image Display**: Same scaling and quality settings
- [ ] **Grid Layout**: Identical organization and spacing

#### Performance Feel

- [ ] **Startup Time**: Match or exceed legacy loading speed
- [ ] **Interaction Responsiveness**: <50ms response time maintained
- [ ] **Smooth Scrolling**: No lag or stuttering
- [ ] **Memory Usage**: No performance degradation
- [ ] **Animation Fluidity**: Smooth transitions preserved

## Implementation Priority

### Phase 1: Visual Foundation (Week 1)

1. Set up exact color palette and style constants
2. Create base component classes with legacy styling
3. Implement responsive font calculation logic
4. Set up visual regression testing framework

### Phase 2: Component Recreation (Week 2-3)

1. Recreate header component with pixel-perfect styling
2. Recreate navigation sidebar with exact interactions
3. Recreate content display area with same scroll behavior
4. Implement hover and selection animations

### Phase 3: Integration Testing (Week 4)

1. Full visual comparison testing
2. User interaction testing
3. Performance benchmarking
4. Cross-platform visual validation

### Phase 4: Polish and Refinement (Week 5)

1. Address any visual discrepancies
2. Fine-tune animations and transitions
3. Optimize performance while maintaining visual fidelity
4. Final user acceptance testing

This approach ensures that users will experience the exact same beautiful, intuitive interface they're accustomed to, while benefiting from the improved architecture underneath. The key is to treat the visual design as sacred and non-negotiable, while modernizing the code structure invisibly.
