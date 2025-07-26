# Settings Dialog Components

This directory contains a modern, component-based settings dialog implementation with clear separation of concerns.

## Architecture Overview

The settings dialog has been refactored from a monolithic 700+ line file into focused, reusable components:

### Core Components

#### 📝 `settings_dialog.py` (Main Dialog)

- **Size**: ~350 lines (reduced from 700+)
- **Responsibility**: Dialog coordination, drag functionality, main layout
- **Dependencies**: All other components

#### 🎨 `components/glassmorphism_styles.py`

- **Responsibility**: All CSS styling for glassmorphism design
- **Benefits**: Centralized styling, easy theming, no CSS duplication

#### 📋 `components/settings_header.py`

- **Responsibility**: Title bar with close button
- **Features**: Custom title support, close signal emission

#### 🧭 `components/settings_sidebar.py`

- **Responsibility**: Navigation between settings tabs
- **Features**: Tab selection, programmatic navigation, hover effects

#### 📱 `components/settings_content_area.py`

- **Responsibility**: Tab content container and management
- **Features**: Tab switching, content refresh, widget management

#### 🔘 `components/settings_action_buttons.py`

- **Responsibility**: Bottom action buttons (Reset, Apply, OK)
- **Features**: Signal emission, enable/disable states

#### ✨ `components/settings_animations.py`

- **Responsibility**: Dialog animations (fade in/out)
- **Features**: Smooth transitions, easing curves

#### ⚙️ `components/settings_services.py`

- **Responsibility**: Service initialization and dependency injection
- **Features**: Lazy loading, service factory pattern

## Benefits of Refactoring

### 🔧 **Maintainability**

- Each component has a single responsibility
- Easy to locate and fix issues
- Clear component boundaries

### 🧪 **Testability**

- Components can be tested in isolation
- Mock dependencies easily
- Better unit test coverage

### 🔄 **Reusability**

- Components can be reused in other dialogs
- Glassmorphism styles shared across app
- Header/sidebar patterns replicable

### 📈 **Scalability**

- Easy to add new components
- Simple to extend functionality
- Clear extension points

### 🎯 **Performance**

- Smaller import footprint
- Lazy loading of services
- Better memory management

## Usage

### Basic Usage

```python
from .settings_dialog import SettingsDialog

dialog = SettingsDialog(ui_state_service, parent)
dialog.show()
```

### Component Usage

```python
from .components import SettingsHeader, SettingsSidebar

# Use individual components
header = SettingsHeader("My Settings")
sidebar = SettingsSidebar(["General", "Advanced"])
```

### Styling Customization

```python
from .components import GlassmorphismStyles

# Get base styles and customize
styles = GlassmorphismStyles.get_dialog_styles()
custom_styles = styles + """
    #my_custom_element {
        background: rgba(255, 255, 255, 0.1);
    }
"""
```

## Migration from Legacy

The refactored dialog maintains **100% backward compatibility**:

- Same public API
- Same signals and slots
- Same properties and methods
- Drop-in replacement

## File Structure

```
settings/
├── settings_dialog.py              # Main dialog (350 lines)
├── coordinator.py                  # Settings coordination
├── components/                     # Reusable components
│   ├── __init__.py                # Component exports
│   ├── glassmorphism_styles.py    # CSS styling
│   ├── settings_header.py         # Title bar
│   ├── settings_sidebar.py        # Navigation
│   ├── settings_content_area.py   # Content container
│   ├── settings_action_buttons.py # Action buttons
│   ├── settings_animations.py     # Animations
│   ├── settings_services.py       # Service factory
│   ├── setting_card.py           # Individual setting card
│   ├── toggle.py                 # Toggle component
│   └── combo_box.py              # Dropdown component
└── tabs/                          # Settings tab content
    ├── general_tab.py
    ├── prop_type_tab.py
    ├── visibility_tab.py
    ├── beat_layout_tab.py
    ├── image_export_tab.py
    ├── background_tab.py
    └── codex_exporter_tab.py
```

## Key Features Preserved

✅ **Drag functionality** - Click and drag to move dialog  
✅ **Glassmorphism design** - Translucent, modern appearance  
✅ **Component architecture** - Reusable UI elements  
✅ **Settings coordination** - Centralized state management  
✅ **Smooth animations** - Fade effects and transitions  
✅ **All settings tabs** - Complete functionality preserved  
✅ **Backward compatibility** - Drop-in replacement

This refactoring represents a significant improvement in code organization while maintaining all existing functionality and visual design.
