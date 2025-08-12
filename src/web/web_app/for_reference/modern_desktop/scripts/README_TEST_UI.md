# Image Export Test UI

A comprehensive GUI tool for testing and validating the modern image export system with real-time rendering and interactive controls.

## Features

### 🎯 **Real-Time Rendering**

- **Auto-render on changes**: Automatically updates the image when you modify settings
- **Threaded rendering**: Non-blocking UI with progress indicators
- **Instant feedback**: See changes immediately as you adjust options

### 📋 **Preset Sequences**

- **Single Beat**: Simple 1-beat sequence for basic testing
- **Simple 2-Beat**: Basic 2-beat back-and-forth pattern
- **Simple 4-Beat**: Complete 4-beat sequence with position changes
- **Complex 8-Beat**: Advanced 8-beat sequence with varied motions
- **Custom**: Edit your own JSON sequence data

### ⚙️ **Export Options**

- **Add Word**: Include word text in the export
- **Add User Info**: Include user name and date
- **Add Difficulty**: Include difficulty level indicator
- **Add Beat Numbers**: Show beat numbers on pictographs
- **Add Reversals**: Show reversal symbols
- **Include Start Position**: Add start position pictograph
- **User Name**: Customizable user name
- **Notes**: Custom notes for the export

### 🖼️ **Image Display**

- **Scalable preview**: Automatically scales images to fit display
- **Image information**: Shows actual and display dimensions
- **Save functionality**: Export images to PNG files
- **High-quality rendering**: Uses the same engine as production exports

## Quick Start

### Launch the UI

```bash
# Simple launcher
python scripts/launch_test_ui.py

# Or run directly
python scripts/image_export_test_ui.py
```

### Basic Usage

1. **Select a preset sequence** from the dropdown
2. **Modify export options** using the checkboxes
3. **Change the word** in the text field
4. **Watch the image update** automatically (if auto-render is enabled)
5. **Click "Save Image"** to export the result

### Custom Sequences

1. Select **"Custom"** from the sequence dropdown
2. Edit the **JSON sequence data** in the text editor
3. The image will **auto-update** as you type (with a 500ms delay)
4. **Invalid JSON** will show an error in the status bar

## Interface Layout

```
┌─────────────────────────────────────────────────────────────┐
│ Image Export Test UI                                        │
├─────────────────┬───────────────────────────────────────────┤
│ Controls Panel  │ Image Display Panel                       │
│                 │                                           │
│ ┌─────────────┐ │ ┌─────────────────────────────────────┐   │
│ │ Sequence    │ │ │ Image Info: 399×716px               │   │
│ │ Settings    │ │ │ Display: 400×600px (0.67x scale)    │   │
│ └─────────────┘ │ └─────────────────────────────────────┘   │
│                 │                                           │
│ ┌─────────────┐ │ ┌─────────────────────────────────────┐   │
│ │ Export      │ │ │                                     │   │
│ │ Options     │ │ │        Rendered Image               │   │
│ └─────────────┘ │ │                                     │   │
│                 │ │                                     │   │
│ [Render Now]    │ │                                     │   │
│ [Save Image]    │ │                                     │   │
│                 │ └─────────────────────────────────────┘   │
│ ☑ Auto-render  │                                           │
└─────────────────┴───────────────────────────────────────────┤
│ Status: Image rendered successfully                         │
└─────────────────────────────────────────────────────────────┘
```

## Sequence JSON Format

The UI accepts sequence data in this JSON format:

```json
[
	{
		"beat": "1",
		"red_attributes": {
			"start_loc": "n",
			"end_loc": "s",
			"motion_type": "pro",
			"turns": 0
		},
		"blue_attributes": {
			"start_loc": "s",
			"end_loc": "n",
			"motion_type": "pro",
			"turns": 0
		},
		"start_position": "alpha",
		"end_position": "alpha"
	}
]
```

### Field Descriptions

- **beat**: Beat number (string)
- **red_attributes/blue_attributes**: Motion properties for each prop
  - **start_loc/end_loc**: Location codes (`n`, `s`, `e`, `w`)
  - **motion_type**: Motion type (`pro`, `anti`)
  - **turns**: Number of turns (integer)
- **start_position/end_position**: Position names (`alpha`, `beta`, `gamma`)

## Testing Scenarios

### Font Sizing Validation

1. Test **different sequence lengths** (1, 2, 4, 8 beats)
2. Compare **image dimensions** with legacy exports
3. Verify **font scaling** based on beat count
4. Check **text positioning** and alignment

### Export Options Testing

1. **Toggle each option** individually to see effects
2. Test **combinations** of options
3. Verify **user info** appears correctly
4. Check **beat numbering** accuracy

### Performance Testing

1. **Rapid option changes** with auto-render enabled
2. **Large sequences** (8+ beats)
3. **Custom sequence editing** with live updates
4. **Multiple renders** in succession

## Troubleshooting

### Common Issues

**UI doesn't launch**

- Check Python environment and dependencies
- Ensure PyQt6 is installed
- Run from the correct directory

**Images don't render**

- Check the status bar for error messages
- Verify sequence JSON is valid
- Look for service initialization errors

**Auto-render not working**

- Check if "Auto-render on changes" is enabled
- Try manual render with "Render Now" button
- Check for JSON syntax errors

**Save fails**

- Ensure you have write permissions
- Check available disk space
- Try a different file location

### Debug Information

- **Status bar**: Shows current operation status and errors
- **Image info**: Displays actual image dimensions
- **Console output**: Check terminal for detailed error messages

## Advanced Usage

### Custom Testing

1. **Create test sequences** using the JSON editor
2. **Save frequently used sequences** as presets
3. **Compare outputs** with legacy system
4. **Batch testing** with different configurations

### Integration Testing

1. **Test with real sequence data** from the application
2. **Validate against legacy exports** for pixel-perfect matching
3. **Performance benchmarking** with various sequence sizes
4. **Error handling** with malformed data

## Files

- **`image_export_test_ui.py`**: Main UI application
- **`launch_test_ui.py`**: Simple launcher script
- **`README_TEST_UI.md`**: This documentation

## Dependencies

- PyQt6 (GUI framework)
- Modern image export services
- Dependency injection container
- Image export interfaces

The UI automatically initializes all required services and provides error messages if anything is missing.
