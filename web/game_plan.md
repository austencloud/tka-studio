# TKA Legacy Image Export System - Complete Technical Analysis

## 🏗️ **SYSTEM ARCHITECTURE**

```
ImageExportManager (Main Orchestrator)
├── ImageExportLayoutHandler (Grid Layout Logic)
├── ImageExportBeatFactory (Sequence → Beat Conversion)
├── ImageCreator (Image Composition)
│   ├── BeatDrawer (Beat Rendering)
│   │   └── CombinedGridHandler (Dual Grid Overlay)
│   ├── BeatReversalProcessor (Reversal Symbols)
│   ├── UserInfoDrawer (User Details)
│   ├── WordDrawer (Sequence Name)
│   ├── ImageExportDifficultyLevelDrawer (Difficulty Badge)
│   ├── HeightDeterminer (Layout Calculations)
│   └── FontMarginHelper (Typography Scaling)
└── ImageSaver (File Operations)
```

## 🎯 **MAIN ORCHESTRATOR: ImageExportManager**

**Primary Responsibilities:**

- Coordinate entire export pipeline
- Manage settings and configuration
- Handle sequence validation and preprocessing
- Orchestrate component initialization

**Key Properties:**

- `include_start_pos: bool` - Whether to include start position in export
- `last_save_directory: str` - Remember last save location
- `beat_frame` - Reference to the source beat frame
- `main_widget` - Application context reference

**Core Export Flow:**

1. **Validation Phase**: Check sequence validity and settings
2. **Options Assembly**: Gather all export settings into options dict
3. **Image Generation**: Call `ImageCreator.create_sequence_image()`
4. **File Saving**: Use `ImageSaver.save_image()`
5. **User Feedback**: Show success/failure messages

**Critical Logic - Sequence Validation:**

```python
# Empty sequence handling
has_beats = len(sequence) >= 3
if not has_beats and not include_start_pos:
    show_error("Sequence empty and start position disabled")
    return
elif not has_beats and include_start_pos:
    show_message("Exporting only start position")

# Options assembly
options = {
    "user_name": settings_manager.users.get_current_user(),
    "export_date": datetime.now().strftime("%m-%d-%Y"),
    **settings_manager.image_export.get_all_image_export_options()
}
```

---

## 📐 **LAYOUT SYSTEM: ImageExportLayoutHandler**

**Core Responsibility:** Calculate optimal grid layouts that match the beat frame's current layout

**Layout Strategy:**

- **Primary**: Use beat frame's layout manager for consistency
- **Fallback**: Predefined layout tables for various beat counts
- **Adaptive**: Adjust for start position inclusion

**Layout Tables:**

### With Start Position (columns, rows):

```
Beats 0-4:  Single row layouts (1-5 columns)
Beats 5-8:  Two-row layouts (3-5 columns)
Beats 9-16: 3-4 row layouts (3-5 columns)
Beats 17+:  5+ row layouts (5+ columns)
```

### Without Start Position:

```
Similar patterns but optimized for beat-only layouts
Tends toward more square/rectangular arrangements
```

**Key Methods:**

- `get_current_beat_frame_layout()` - Sync with beat frame
- `calculate_layout()` - Main layout determination
- `calculate_layout_with_start()` - Include start position
- `calculate_layout_without_start()` - Exclude start position

---

## 🏭 **BEAT FACTORY: ImageExportBeatFactory**

**Purpose:** Convert raw sequence JSON data into renderable `LegacyBeatView` objects

**Process Flow:**

1. **Temporary Beat Frame Creation**: Create isolated beat frame for processing
2. **Beat Data Processing**: Filter placeholders, process durations
3. **Beat View Creation**: Convert each beat data to `LegacyBeatView`
4. **Beat Assembly**: Apply beat numbers and pictograph data

**Key Processing Logic:**

```python
def process_sequence_to_beats(self, sequence: list[dict]) -> list[LegacyBeatView]:
    filled_beats = []
    current_beatNumber = 1

    for beat_data in sequence[2:]:  # Skip metadata entries
        if beat_data.get("is_placeholder"):
            continue

        duration = beat_data.get("duration", 1)
        beat_view = self.create_beat_view_from_data(beat_data, current_beatNumber, temp_beat_frame)
        filled_beats.append(beat_view)
        current_beatNumber += duration

    return filled_beats
```

**Beat View Creation Process:**

1. Create new `LegacyBeatView` instance
2. Create associated `Beat` object
3. Apply pictograph data to beat state
4. Update beat with pictograph information
5. Set beat number and return configured view

---

## 🎨 **IMAGE COMPOSITION: ImageCreator**

**Central Role:** Main image composition and rendering coordinator

**Key Properties:**

- `BASE_MARGIN = 50` - Base spacing constant
- `beat_size` - Size of individual beat squares
- `beat_scale = 1` - Scaling factor for different export sizes

**Main Creation Pipeline:**

```python
def create_sequence_image(self, sequence, options, dictionary=False, fullscreen_preview=False):
    # 1. Process sequence to beats
    filled_beats = self._process_sequence(sequence)

    # 2. Update options for context
    options = self._update_options(options, len(filled_beats))

    # 3. Handle reversal symbols
    if options["add_reversal_symbols"]:
        self.reversal_processor.process_reversals(sequence, filled_beats)

    # 4. Calculate layout dimensions
    column_count, row_count = self.layout_manager.calculate_layout(...)

    # 5. Determine additional heights for text
    additional_height_top, additional_height_bottom = self._determine_additional_heights(...)

    # 6. Create base image
    image = self._create_image(column_count, row_count, additional_height_top + additional_height_bottom)

    # 7. Draw beats onto image
    self.beat_drawer.draw_beats(image, filled_beats, column_count, row_count, ...)

    # 8. Add additional information
    if not fullscreen_preview and not dictionary:
        self._draw_additional_info(image, filled_beats, options, len(filled_beats))

    return image
```

**Visibility Settings Application:**
The system applies visibility settings to control which elements appear:

```python
def _apply_visibility_settings(self, beats: list[LegacyBeatView]) -> None:
    visibility_settings = self.export_manager.settings_manager.visibility
    red_visible = visibility_settings.get_motion_visibility("red")
    blue_visible = visibility_settings.get_motion_visibility("blue")

    for beat_view in beats:
        # Apply to props and arrows
        red_prop = beat_view.beat.elements.props.get("red")
        blue_prop = beat_view.beat.elements.props.get("blue")
        if red_prop: red_prop.setVisible(red_visible)
        if blue_prop: blue_prop.setVisible(blue_visible)
```

---

## 🖌️ **BEAT RENDERING: BeatDrawer**

**Purpose:** Render individual beats onto the image canvas

**Core Rendering Logic:**

```python
def draw_beats(self, image, filled_beats, column_count, row_count, include_start_pos, additional_height_top, add_beatNumbers):
    beat_size = int(self.beat_frame.start_pos_view.beat.width() * self.image_creator.beat_scale)
    painter = QPainter(image)
    beatNumber = 0

    # Handle start position
    if include_start_pos:
        start_pos_pixmap = self._grab_pixmap(self.beat_frame.start_pos_view, beat_size, beat_size, use_combined_grids)
        painter.drawPixmap(0, additional_height_top, start_pos_pixmap)
        start_col = 1
    else:
        start_col = 0

    # Draw each beat in grid layout
    for row in range(row_count + 1):
        for col in range(start_col, column_count):
            if beatNumber < len(filled_beats):
                beat_view = filled_beats[beatNumber]
                beat_pixmap = self._grab_pixmap(beat_view, beat_size, beat_size, use_combined_grids)
                target_x = col * beat_size
                target_y = row * beat_size + additional_height_top
                painter.drawPixmap(target_x, target_y, beat_pixmap)
                beatNumber += 1
```

**Pixmap Grabbing:**

- **Standard Mode**: Direct beat view capture and scaling
- **Combined Grid Mode**: Overlay both diamond and box grids

---

## 🔄 **COMBINED GRID SYSTEM: CombinedGridHandler**

**Purpose:** Overlay both diamond and box grids simultaneously for enhanced visualization

**Process:**

1. **Base Capture**: Grab normal beat pixmap
2. **Grid Detection**: Determine current grid mode
3. **Overlay Addition**: Add the opposite grid with transparency
4. **Composition**: Combine both grids into final pixmap

**Implementation:**

```python
def process_beat_for_combined_grids(self, beat_view: "LegacyBeatView", beat_size: int) -> QPixmap:
    # Grab normal beat
    normal_pixmap = beat_view.beat.grabber.grab().scaled(beat_size, beat_size, ...)

    # Create composite image
    combined_image = QImage(normal_pixmap.width(), normal_pixmap.height(), QImage.Format.Format_ARGB32)
    combined_image.fill(Qt.GlobalColor.transparent)

    painter = QPainter(combined_image)
    painter.drawPixmap(0, 0, normal_pixmap)

    # Add opposite grid
    current_grid_mode = beat_view.beat.state.gridMode
    if current_grid_mode == DIAMOND:
        self._draw_grid_with_transparency(painter, self.box_grid_path, beat_size)
    elif current_grid_mode == BOX:
        self._draw_grid_with_transparency(painter, self.diamond_grid_path, beat_size)

    return QPixmap.fromImage(combined_image)
```

---

## ↩️ **REVERSAL PROCESSING: BeatReversalProcessor**

**Purpose:** Detect and mark reversal symbols on beats that reverse motion direction

**Detection Process:**

```python
def process_reversals(sequence: list[dict], filled_beats: list["LegacyBeatView"]) -> None:
    sequence_so_far = []

    for i, (beat_data, beat_view) in enumerate(zip(sequence[2:], filled_beats)):
        # Filter out placeholders and start positions
        filtered_sequence_so_far = [
            beat for beat in sequence_so_far
            if not beat.get(SEQUENCE_START_POSITION) and not beat.get("is_placeholder", False)
        ]

        # Detect reversals
        reversal_info = ReversalDetector.detect_reversal(filtered_sequence_so_far, beat_data)

        # Apply reversal state to pictograph
        pictograph = beat_view.beat
        pictograph.state.blueReversal = reversal_info.get("blueReversal", False)
        pictograph.state.redReversal = reversal_info.get("redReversal", False)
        pictograph.elements.reversal_glyph.update_reversal_symbols()

        # Update visual representation
        beat_view.update()
        beat_view.repaint()

        sequence_so_far.append(beat_data)
```

---

## 📏 **LAYOUT CALCULATIONS: HeightDeterminer**

**Purpose:** Calculate additional height needed for text elements based on beat count

**Height Strategy:**

```python
def determine_additional_heights(options: dict, num_filled_beats: int, beat_scale: float) -> tuple[int, int]:
    if num_filled_beats == 0:
        additional_height_top = 0
        additional_height_bottom = 55 if options.get("add_user_info", False) else 0
    elif num_filled_beats == 1:
        additional_height_top = 150 if options.get("add_word", False) else 0
        additional_height_bottom = 55 if options.get("add_user_info", False) else 0
    elif num_filled_beats == 2:
        additional_height_top = 200 if options.get("add_word", False) else 0
        additional_height_bottom = 75 if options.get("add_user_info", False) else 0
    else:
        additional_height_top = 300 if options.get("add_word", False) else 0
        additional_height_bottom = 150 if options.get("add_user_info", False) else 0

    return int(additional_height_top * beat_scale), int(additional_height_bottom * beat_scale)
```

**Scaling Strategy:**

- **Empty sequences**: Minimal height
- **1-2 beats**: Moderate spacing
- **3+ beats**: Full spacing for text clarity
- **Scale factor**: Applied to all measurements

---

## ✏️ **TEXT RENDERING SYSTEMS**

### **WordDrawer - Sequence Name Rendering**

**Purpose:** Render the sequence name at the top of the image

**Features:**

- **Custom Kerning**: Adjustable letter spacing
- **Auto-scaling**: Font size adjusts to fit image width
- **Vertical Centering**: Text centered in top margin space

**Implementation:**

```python
def draw_word(self, image, word, num_filled_beats, additional_height_top):
    # Font and margin scaling
    font, margin = FontMarginHelper.adjust_font_and_margin(self.base_font, num_filled_beats, base_margin, beat_scale)

    # Auto-fit to image width
    while text_width + 2 * margin > image.width() - (image.width() // 4):
        font_size = font.pointSize() - 1
        if font_size <= 10: break
        font = QFont(font.family(), font_size, font.weight(), font.italic())

    # Custom kerning for each letter
    x = (image.width() - text_width - self.kerning * (len(text) - 1)) // 2
    for letter in text:
        painter.drawText(x, y, letter)
        x += metrics.horizontalAdvance(letter) + self.kerning
```

### **UserInfoDrawer - User Details**

**Purpose:** Render user information at the bottom of the image

**Elements:**

- **Left**: User name (bold italic)
- **Center**: Notes/attribution text
- **Right**: Export date

**Layout Strategy:**

```python
def draw_user_info(self, image, options, num_filled_beats):
    # Calculate text widths for positioning
    export_date_width = self._get_text_width(font_italic, export_date)
    notes_width = self._get_text_width(font_italic, notes)

    # Position elements
    self._draw_text(painter, image, user_name, font_bold_italic, margin, "bottom-left")
    self._draw_text(painter, image, notes, font_italic, margin, "bottom-center", notes_width)
    self._draw_text(painter, image, export_date, font_italic, margin, "bottom-right", export_date_width)
```

### **ImageExportDifficultyLevelDrawer - Difficulty Badge**

**Purpose:** Render circular difficulty level indicator

**Features:**

- **Gradient Backgrounds**: Different colors per difficulty level
- **Circular Shape**: Ellipse with border
- **Centered Text**: Difficulty number in center

**Difficulty Gradients:**

- **Level 1**: Light gray (simple)
- **Level 2**: Medium gray (moderate)
- **Level 3**: Gold gradients (advanced)
- **Level 4**: Purple gradients (expert)
- **Level 5**: Red gradients (master)

---

## 🔤 **TYPOGRAPHY SYSTEM: FontMarginHelper**

**Purpose:** Scale fonts and margins based on beat count and scale factor

**Scaling Rules:**

```python
def adjust_font_and_margin(base_font, num_filled_beats, base_margin, beat_scale):
    base_font_size = max(1, base_font.pointSize())

    if num_filled_beats <= 1:
        font_size = max(1, int(base_font_size / 2.3))
        margin = max(1, base_margin // 3)
    elif num_filled_beats == 2:
        font_size = max(1, int(base_font_size / 1.5))
        margin = max(1, base_margin // 2)
    else:
        font_size = base_font_size
        margin = base_margin

    scaled_font_size = max(1, int(font_size * beat_scale))
    return adjusted_font, max(1, int(margin * beat_scale))
```

**Strategy:**

- **Few beats**: Smaller fonts and margins
- **Many beats**: Full-size typography
- **Safety bounds**: Minimum size of 1 to prevent crashes

---

## 💾 **FILE OPERATIONS: ImageSaver**

**Purpose:** Handle file saving with intelligent naming and directory management

**Saving Strategy:**

1. **Filename Generation**: Use sequence word + version number
2. **Directory Logic**:
   - Use last save directory if enabled and exists
   - Fall back to organized word folders in Photos
3. **Version Management**: Auto-increment version numbers
4. **User Feedback**: Show save status and open file location

**Core Save Logic:**

```python
def save_image(self, sequence_image: QImage):
    word = self.beat_frame.get.current_word()

    # Handle empty sequences
    if word == "":
        if include_start_pos:
            word = "startPosition"
        else:
            show_error("Must build sequence to save")
            return

    # Directory determination
    if use_last_directory and last_directory_exists:
        base_path = last_directory
    else:
        base_path = get_my_photos_path(f"{word}")
        os.makedirs(base_path, exist_ok=True)

    # Version management
    version_number = 1
    file_path = os.path.join(base_path, f"{word}_v{version_number}.png")
    while os.path.exists(file_path):
        version_number += 1
        file_path = os.path.join(base_path, f"{word}_v{version_number}.png")

    # Save with dialog
    file_name, _ = QFileDialog.getSaveFileName(self.beat_frame, "Save Image", file_path, "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")

    if file_name and sequence_image.save(file_name, "PNG", 100):
        settings_manager.image_export.set_last_save_directory(os.path.dirname(file_name))
        show_success(f"Image saved as {os.path.basename(file_name)}")
        os.startfile(file_name)  # Open file location
```

---

## ⚙️ **CONFIGURATION & SETTINGS**

The system relies heavily on configurable settings:

**Export Options:**

- `include_start_position`: Show start position beat
- `add_beatNumbers`: Show beat numbers
- `add_reversal_symbols`: Show reversal indicators
- `add_user_info`: Show user details at bottom
- `add_word`: Show sequence name at top
- `add_difficulty_level`: Show difficulty badge
- `combined_grids`: Overlay both grid types
- `use_last_save_directory`: Remember save location

**Visibility Settings:**

- `red_motion_visibility`: Show/hide red elements
- `blue_motion_visibility`: Show/hide blue elements

**User Settings:**

- `current_user`: User name for attribution
- `last_save_directory`: Remember save location

---

## 🔧 **KEY TECHNICAL PATTERNS**

### **Dependency Injection Pattern**

Each component receives its dependencies through constructor injection:

```python
class ImageExportManager:
    def __init__(self, beat_frame, beat_frame_class):
        self.layout_handler = ImageExportLayoutHandler(self)
        self.beat_factory = ImageExportBeatFactory(self, beat_frame_class)
        self.image_creator = ImageCreator(self)
        self.image_saver = ImageSaver(self)
```

### **Settings Management Pattern**

Centralized settings access through manager:

```python
settings_manager = AppContext.settings_manager()
options = settings_manager.image_export.get_all_image_export_options()
user_name = settings_manager.users.get_current_user()
```

### **Template Method Pattern**

`ImageCreator.create_sequence_image()` follows a template method pattern with fixed steps but customizable details.

### **Strategy Pattern**

Different layout strategies based on beat count and start position inclusion.

### **Builder Pattern**

`ImageExportBeatFactory` builds complex beat view objects step by step.

---

## 📊 **PERFORMANCE CONSIDERATIONS**

**Memory Management:**

- Temporary beat frames are created for processing
- Large images use efficient Qt pixmap operations
- Painters are properly disposed after use

**Rendering Optimizations:**

- Beat pixmaps are cached during grab operations
- Combined grid rendering uses efficient overlay techniques
- Font metrics are calculated once per text element

**File I/O:**

- Maximum quality PNG export (quality 100)
- Efficient directory checking and creation
- Version number incrementation to avoid overwrites

---

## 🚨 **ERROR HANDLING PATTERNS**

**Graceful Degradation:**

- Empty sequences can still export start position
- Missing settings fall back to defaults
- Font scaling has minimum bounds to prevent crashes

**User Feedback:**

- Clear error messages for invalid states
- Success notifications with file details
- Progress indication through indicator labels

**Validation:**

- Sequence type checking before processing
- Directory existence verification
- File write permission handling

---

## 🔄 **INTEGRATION POINTS**

**Beat Frame Integration:**

- Uses beat frame's layout manager for consistency
- Accesses current word and sequence data
- Applies beat frame's visibility settings

**Settings System Integration:**

- Reads all export preferences
- Maintains save directory preferences
- Respects user visibility choices

**Application Context:**

- Uses main widget for user feedback
- Accesses JSON manager for sequence data
- Integrates with sequence level evaluator

This system represents a sophisticated image export pipeline with excellent separation of concerns, comprehensive configuration options, and robust error handling. The architecture would translate well to a modern web-based implementation using the patterns outlined in your SvelteKit development guidelines.

# TKA Image Export System - Web Implementation Game Plan

## 🎯 **MISSION OBJECTIVE**

Port the sophisticated Python/Qt image export system to modern web technologies while maintaining **pixel-perfect compatibility** with the desktop version's sizing, layout, and rendering logic.

---

## 📋 **CURRENT STATE ANALYSIS**

### ✅ **What's Already Built**

- **Export UI Framework**: `ExportPanel.svelte`, `ExportPreviewCard.svelte`, `ExportSettingsCard.svelte`
- **Domain Models**: `SequenceData`, `BeatData`, `PictographData` with TypeScript interfaces
- **SVG Rendering**: `Pictograph.svelte` component with grid, props, arrows, and text
- **Service Architecture**: DI container with established registration patterns
- **Canvas Experience**: Multiple canvas components (`AnimatorCanvas`, `BackgroundCanvas`)
- **File Utils**: `file-download.ts` utility for browser downloads

### ❌ **What's Missing (Our Target)**

- **Image Generation Engine**: Canvas-based image composition system
- **Layout Calculation**: Grid layout algorithms matching desktop precisely
- **Beat Rendering**: Convert SVG pictographs to canvas for export
- **Text Rendering**: Typography system with exact font scaling
- **Service Layer**: Business logic services following your architecture
- **Settings Integration**: Export options persistence and management

---

## 🏗️ **ARCHITECTURE MAPPING: Python/Qt → SvelteKit**

| **Desktop Component**      | **Web Equivalent**            | **Technology**          |
| -------------------------- | ----------------------------- | ----------------------- |
| `ImageExportManager`       | `ImageExportService`          | TypeScript Service      |
| `ImageCreator`             | `ImageCompositionService`     | Canvas 2D API           |
| `BeatDrawer`               | `BeatRenderingService`        | SVG → Canvas conversion |
| `ImageExportLayoutHandler` | `LayoutCalculationService`    | Pure algorithms         |
| `UserInfoDrawer`           | `TextRenderingService`        | Canvas text rendering   |
| `WordDrawer`               | `TextRenderingService`        | Typography with kerning |
| `ImageSaver`               | `FileExportService`           | HTML5 download API      |
| `CombinedGridHandler`      | `GridOverlayService`          | Canvas compositing      |
| `BeatReversalProcessor`    | `ReversalDetectionService`    | Business logic          |
| `HeightDeterminer`         | `DimensionCalculationService` | Math utilities          |

---

## 📐 **EXACT SIZE COMPATIBILITY STRATEGY**

### **Desktop Reference Measurements**

- **Base Beat Size**: Desktop uses `self.beat_frame.start_pos_view.beat.width()` (typically 144px)
- **Base Margin**: 50px constant across all text elements
- **Scale Factor**: `beat_scale = 1` (can be adjusted for different export sizes)
- **Grid Layout**: Hardcoded tables for specific beat counts with/without start position

### **Web Implementation**

```typescript
// Match desktop constants exactly
const BASE_BEAT_SIZE = 144; // Match desktop beat.width()
const BASE_MARGIN = 50; // Match desktop BASE_MARGIN
const DEFAULT_SCALE = 1; // Match desktop beat_scale

// Layout tables must match desktop precisely
const LAYOUT_WITH_START = {
  0: [1, 1],
  1: [2, 1],
  2: [3, 1],
  3: [4, 1],
  4: [5, 1],
  5: [4, 2],
  6: [4, 2],
  7: [5, 2],
  8: [5, 2],
  9: [4, 3],
  // ... exact copy of desktop layout tables
};
```

---

## 🎯 **IMPLEMENTATION PHASES**

## **PHASE 1: Core Service Architecture** ⭐ _Start Here_

### **1.1 Service Interfaces**

```typescript
// File: src/lib/services/interfaces/image-export-interfaces.ts
interface IImageExportService {
  exportSequenceImage(
    sequence: SequenceData,
    options: ExportOptions
  ): Promise<Blob>;
  generatePreview(
    sequence: SequenceData,
    options: ExportOptions
  ): Promise<string>;
}

interface ILayoutCalculationService {
  calculateLayout(
    beatCount: number,
    includeStartPosition: boolean
  ): [number, number];
  calculateImageDimensions(
    layout: [number, number],
    additionalHeight: number
  ): [number, number];
}

interface IBeatRenderingService {
  renderBeatToCanvas(
    beatData: BeatData,
    size: number,
    options: RenderOptions
  ): Promise<HTMLCanvasElement>;
  renderStartPositionToCanvas(
    sequence: SequenceData,
    size: number
  ): Promise<HTMLCanvasElement>;
}

interface ITextRenderingService {
  renderWordText(
    canvas: HTMLCanvasElement,
    word: string,
    options: TextOptions
  ): void;
  renderUserInfo(
    canvas: HTMLCanvasElement,
    userInfo: UserInfo,
    options: TextOptions
  ): void;
  renderDifficultyBadge(
    canvas: HTMLCanvasElement,
    level: number,
    position: [number, number]
  ): void;
}

interface IImageCompositionService {
  composeSequenceImage(
    beats: HTMLCanvasElement[],
    layout: LayoutData,
    options: CompositionOptions
  ): Promise<HTMLCanvasElement>;
}
```

### **1.2 Service Registration**

```typescript
// File: src/lib/services/di/registration/image-export-services.ts
export async function registerImageExportServices(
  container: ServiceContainer
): Promise<void> {
  // Register in dependency order
  container.registerSingletonClass(ILayoutCalculationServiceInterface);
  container.registerSingletonClass(ITextRenderingServiceInterface);
  container.registerSingletonClass(IDimensionCalculationServiceInterface);

  // Register with dependencies
  container.registerFactory(IBeatRenderingServiceInterface, () => {
    const pictographService = container.resolve(IPictographServiceInterface);
    return new BeatRenderingService(pictographService);
  });

  container.registerFactory(IImageCompositionServiceInterface, () => {
    const layoutService = container.resolve(ILayoutCalculationServiceInterface);
    const textService = container.resolve(ITextRenderingServiceInterface);
    return new ImageCompositionService(layoutService, textService);
  });

  container.registerFactory(IImageExportServiceInterface, () => {
    const beatRenderer = container.resolve(IBeatRenderingServiceInterface);
    const composer = container.resolve(IImageCompositionServiceInterface);
    const fileService = container.resolve(IFileExportServiceInterface);
    return new ImageExportService(beatRenderer, composer, fileService);
  });
}
```

---

## **PHASE 2: Layout & Dimension Services**

### **2.1 Layout Calculation Service**

```typescript
// File: src/lib/services/implementations/LayoutCalculationService.ts
export class LayoutCalculationService implements ILayoutCalculationService {
  // EXACT copy of desktop layout tables
  private readonly LAYOUT_WITH_START_POSITION = {
    0: [1, 1],
    1: [2, 1],
    2: [3, 1],
    3: [4, 1],
    4: [5, 1],
    5: [4, 2],
    6: [4, 2],
    7: [5, 2],
    8: [5, 2],
    9: [4, 3],
    // ... complete desktop table
  };

  private readonly LAYOUT_WITHOUT_START_POSITION = {
    0: [1, 1],
    1: [1, 1],
    2: [2, 1],
    3: [3, 1],
    4: [4, 1],
    5: [3, 2],
    6: [3, 2],
    7: [4, 2],
    8: [4, 2],
    9: [3, 3],
    // ... complete desktop table
  };

  calculateLayout(
    beatCount: number,
    includeStartPosition: boolean
  ): [number, number] {
    const layoutTable = includeStartPosition
      ? this.LAYOUT_WITH_START_POSITION
      : this.LAYOUT_WITHOUT_START_POSITION;

    return layoutTable[beatCount] || this.getFallbackLayout(beatCount);
  }

  calculateImageDimensions(
    layout: [number, number],
    additionalHeight: number,
    beatScale: number = 1
  ): [number, number] {
    const [columns, rows] = layout;
    const beatSize = BASE_BEAT_SIZE * beatScale;

    return [columns * beatSize, rows * beatSize + additionalHeight];
  }
}
```

### **2.2 Dimension Calculation Service**

```typescript
// File: src/lib/services/implementations/DimensionCalculationService.ts
export class DimensionCalculationService {
  // Match desktop HeightDeterminer exactly
  determineAdditionalHeights(
    options: ExportOptions,
    beatCount: number,
    beatScale: number
  ): [number, number] {
    if (beatCount === 0) {
      return [0, options.addUserInfo ? 55 * beatScale : 0];
    } else if (beatCount === 1) {
      return [
        options.addWord ? 150 * beatScale : 0,
        options.addUserInfo ? 55 * beatScale : 0,
      ];
    } else if (beatCount === 2) {
      return [
        options.addWord ? 200 * beatScale : 0,
        options.addUserInfo ? 75 * beatScale : 0,
      ];
    } else {
      return [
        options.addWord ? 300 * beatScale : 0,
        options.addUserInfo ? 150 * beatScale : 0,
      ];
    }
  }
}
```

---

## **PHASE 3: Beat Rendering Engine**

### **3.1 SVG to Canvas Conversion**

```typescript
// File: src/lib/services/implementations/BeatRenderingService.ts
export class BeatRenderingService implements IBeatRenderingService {
  async renderBeatToCanvas(
    beatData: BeatData,
    size: number,
    options: RenderOptions
  ): Promise<HTMLCanvasElement> {
    // Strategy: Render SVG Pictograph component to canvas

    // 1. Create temporary SVG container
    const svgContainer = document.createElement("div");
    svgContainer.style.position = "absolute";
    svgContainer.style.left = "-9999px";
    svgContainer.style.width = `${size}px`;
    svgContainer.style.height = `${size}px`;
    document.body.appendChild(svgContainer);

    try {
      // 2. Create Pictograph component instance
      const pictographComponent = new Pictograph({
        target: svgContainer,
        props: {
          beatData,
          width: size,
          height: size,
          beatNumber: options.addBeatNumbers ? beatData.beatNumber : null,
        },
      });

      // 3. Wait for component to render completely
      await new Promise((resolve) => setTimeout(resolve, 100));

      // 4. Extract SVG and convert to canvas
      const svgElement = svgContainer.querySelector("svg");
      if (!svgElement) throw new Error("SVG not found");

      const canvas = await this.svgToCanvas(svgElement, size, size);

      // 5. Apply visibility settings (match desktop logic)
      if (!options.redVisible || !options.blueVisible) {
        this.applyVisibilityFilters(canvas, options);
      }

      return canvas;
    } finally {
      document.body.removeChild(svgContainer);
    }
  }

  private async svgToCanvas(
    svgElement: SVGElement,
    width: number,
    height: number
  ): Promise<HTMLCanvasElement> {
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d")!;
    canvas.width = width;
    canvas.height = height;

    // Convert SVG to data URL
    const svgData = new XMLSerializer().serializeToString(svgElement);
    const img = new Image();

    return new Promise((resolve, reject) => {
      img.onload = () => {
        ctx.fillStyle = "white";
        ctx.fillRect(0, 0, width, height);
        ctx.drawImage(img, 0, 0, width, height);
        resolve(canvas);
      };
      img.onerror = reject;
      img.src = `data:image/svg+xml;base64,${btoa(svgData)}`;
    });
  }
}
```

### **3.2 Combined Grid Handler**

```typescript
// File: src/lib/services/implementations/GridOverlayService.ts
export class GridOverlayService {
  applyCombinedGrids(
    canvas: HTMLCanvasElement,
    currentGridMode: string
  ): HTMLCanvasElement {
    // Match desktop CombinedGridHandler logic
    const ctx = canvas.getContext("2d")!;
    const overlayCanvas = document.createElement("canvas");
    overlayCanvas.width = canvas.width;
    overlayCanvas.height = canvas.height;
    const overlayCtx = overlayCanvas.getContext("2d")!;

    // Draw original canvas
    overlayCtx.drawImage(canvas, 0, 0);

    // Add opposite grid with full opacity (desktop uses 100% opacity)
    const oppositeGrid =
      currentGridMode === GridMode.DIAMOND ? GridMode.BOX : GridMode.DIAMOND;
    this.drawGrid(overlayCtx, oppositeGrid, canvas.width, canvas.height);

    return overlayCanvas;
  }
}
```

---

## **PHASE 4: Text Rendering System**

### **4.1 Typography Engine**

```typescript
// File: src/lib/services/implementations/TextRenderingService.ts
export class TextRenderingService implements ITextRenderingService {
  renderWordText(
    canvas: HTMLCanvasElement,
    word: string,
    options: TextOptions
  ): void {
    const ctx = canvas.getContext("2d")!;

    // Match desktop font settings exactly
    let fontSize = 175 * options.beatScale;
    let font = `${fontSize}px Georgia`;
    ctx.font = font;

    // Auto-scale to fit width (match desktop logic)
    let textWidth = ctx.measureText(word).width;
    const maxWidth = canvas.width - canvas.width / 4;

    while (textWidth + 2 * options.margin > maxWidth && fontSize > 10) {
      fontSize--;
      font = `${fontSize}px Georgia`;
      ctx.font = font;
      textWidth = ctx.measureText(word).width;
    }

    // Apply custom kerning (match desktop implementation)
    const kerning = 20 * options.beatScale;
    const totalWidth = textWidth + kerning * (word.length - 1);
    let x = (canvas.width - totalWidth) / 2;
    const y = options.additionalHeightTop / 2 + fontSize / 2;

    ctx.fillStyle = "black";
    ctx.textBaseline = "middle";

    // Draw each letter with custom kerning
    for (const letter of word) {
      ctx.fillText(letter, x, y);
      x += ctx.measureText(letter).width + kerning;
    }
  }

  renderUserInfo(
    canvas: HTMLCanvasElement,
    userInfo: UserInfo,
    options: TextOptions
  ): void {
    // Match desktop UserInfoDrawer layout exactly
    const ctx = canvas.getContext("2d")!;
    const margin = options.margin;
    const bottomY = canvas.height - margin;

    // Left: User name (bold italic)
    ctx.font = `bold italic ${50 * options.beatScale}px Georgia`;
    ctx.fillStyle = "black";
    ctx.textAlign = "left";
    ctx.fillText(userInfo.userName, margin, bottomY);

    // Center: Notes
    ctx.font = `italic ${50 * options.beatScale}px Georgia`;
    ctx.textAlign = "center";
    ctx.fillText(
      userInfo.notes || "Created using The Kinetic Alphabet",
      canvas.width / 2,
      bottomY
    );

    // Right: Export date
    ctx.textAlign = "right";
    const formattedDate = this.formatExportDate(userInfo.exportDate);
    ctx.fillText(formattedDate, canvas.width - margin, bottomY);
  }
}
```

### **4.2 Difficulty Badge Renderer**

```typescript
// File: src/lib/services/implementations/DifficultyBadgeService.ts
export class DifficultyBadgeService {
  renderDifficultyBadge(
    canvas: HTMLCanvasElement,
    level: number,
    additionalHeightTop: number
  ): void {
    const ctx = canvas.getContext("2d")!;

    // Match desktop badge sizing and positioning
    const shapeSize = additionalHeightTop * 0.75;
    const inset = additionalHeightTop / 8;

    // Create gradient matching desktop exactly
    const gradient = this.createDifficultyGradient(ctx, level, shapeSize);

    // Draw circle with border
    ctx.beginPath();
    ctx.arc(
      inset + shapeSize / 2,
      inset + shapeSize / 2,
      shapeSize / 2,
      0,
      2 * Math.PI
    );
    ctx.fillStyle = gradient;
    ctx.fill();
    ctx.strokeStyle = "black";
    ctx.lineWidth = Math.max(1, shapeSize / 50);
    ctx.stroke();

    // Draw level number
    const fontSize = shapeSize / 1.75;
    ctx.font = `bold ${fontSize}px Georgia`;
    ctx.fillStyle = "black";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    const yOffset = level === 3 ? -25 : -15; // Match desktop positioning
    ctx.fillText(
      level.toString(),
      inset + shapeSize / 2,
      inset + shapeSize / 2 + yOffset
    );
  }
}
```

---

## **PHASE 5: Image Composition Engine**

### **5.1 Main Composition Service**

```typescript
// File: src/lib/services/implementations/ImageCompositionService.ts
export class ImageCompositionService implements IImageCompositionService {
  async composeSequenceImage(
    sequence: SequenceData,
    options: ExportOptions
  ): Promise<HTMLCanvasElement> {
    // 1. Calculate layout (match desktop exactly)
    const beatCount = sequence.beats.length;
    const layout = this.layoutService.calculateLayout(
      beatCount,
      options.includeStartPosition
    );
    const [additionalTop, additionalBottom] =
      this.dimensionService.determineAdditionalHeights(
        options,
        beatCount,
        options.beatScale
      );

    // 2. Create main canvas
    const [width, height] = this.layoutService.calculateImageDimensions(
      layout,
      additionalTop + additionalBottom,
      options.beatScale
    );
    const mainCanvas = document.createElement("canvas");
    mainCanvas.width = width;
    mainCanvas.height = height;
    const ctx = mainCanvas.getContext("2d")!;

    // 3. Fill white background
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, width, height);

    // 4. Render start position if enabled
    let startCol = 0;
    if (options.includeStartPosition) {
      const startPosCanvas =
        await this.beatRenderer.renderStartPositionToCanvas(
          sequence,
          options.beatSize
        );
      ctx.drawImage(startPosCanvas, 0, additionalTop);
      startCol = 1;
    }

    // 5. Render beats in grid layout (match desktop positioning exactly)
    const [columns, rows] = layout;
    let beatIndex = 0;

    for (let row = 0; row < rows; row++) {
      for (let col = startCol; col < columns; col++) {
        if (beatIndex < sequence.beats.length) {
          const beatCanvas = await this.beatRenderer.renderBeatToCanvas(
            sequence.beats[beatIndex],
            options.beatSize,
            options
          );

          const x = col * options.beatSize;
          const y = row * options.beatSize + additionalTop;
          ctx.drawImage(beatCanvas, x, y);
          beatIndex++;
        }
      }
    }

    // 6. Add text overlays
    if (options.addWord && sequence.word) {
      this.textRenderer.renderWordText(mainCanvas, sequence.word, {
        margin: BASE_MARGIN * options.beatScale,
        beatScale: options.beatScale,
        additionalHeightTop: additionalTop,
      });
    }

    if (options.addUserInfo) {
      this.textRenderer.renderUserInfo(
        mainCanvas,
        {
          userName: options.userName,
          notes: options.notes,
          exportDate: options.exportDate,
        },
        {
          margin: BASE_MARGIN * options.beatScale,
          beatScale: options.beatScale,
        }
      );
    }

    if (options.addDifficultyLevel && sequence.level) {
      this.difficultyRenderer.renderDifficultyBadge(
        mainCanvas,
        sequence.level,
        additionalTop
      );
    }

    return mainCanvas;
  }
}
```

---

## **PHASE 6: Export Service & File Operations**

### **6.1 File Export Service**

```typescript
// File: src/lib/services/implementations/FileExportService.ts
export class FileExportService implements IFileExportService {
  async exportSequenceImage(
    canvas: HTMLCanvasElement,
    filename: string,
    format: "PNG" | "JPEG" = "PNG",
    quality: number = 1.0
  ): Promise<void> {
    // Convert canvas to blob with maximum quality (match desktop quality 100)
    const blob = await new Promise<Blob>((resolve) => {
      canvas.toBlob(
        (blob) => {
          resolve(blob!);
        },
        `image/${format.toLowerCase()}`,
        quality
      );
    });

    // Use existing file-download utility
    const { downloadFile } = await import("$lib/utils/file-download");
    await downloadFile(blob, filename);
  }

  generateVersionedFilename(word: string, format: string): string {
    // Match desktop versioning logic
    const timestamp = new Date().toISOString().slice(0, 10).replace(/-/g, "");
    return `${word || "sequence"}_v1_${timestamp}.${format.toLowerCase()}`;
  }
}
```

### **6.2 Main Export Service**

```typescript
// File: src/lib/services/implementations/ImageExportService.ts
export class ImageExportService implements IImageExportService {
  constructor(
    private beatRenderer: IBeatRenderingService,
    private composer: IImageCompositionService,
    private fileService: IFileExportService,
    private settingsService: ISettingsService
  ) {}

  async exportSequenceImage(
    sequence: SequenceData,
    options: Partial<ExportOptions> = {}
  ): Promise<Blob> {
    // 1. Merge with default options (match desktop defaults)
    const fullOptions = this.mergeWithDefaults(options);

    // 2. Validate sequence
    this.validateSequence(sequence, fullOptions);

    // 3. Compose image
    const canvas = await this.composer.composeSequenceImage(
      sequence,
      fullOptions
    );

    // 4. Convert to blob
    return new Promise((resolve) => {
      canvas.toBlob((blob) => resolve(blob!), "image/png", 1.0);
    });
  }

  async generatePreview(
    sequence: SequenceData,
    options: Partial<ExportOptions> = {}
  ): Promise<string> {
    const fullOptions = { ...this.mergeWithDefaults(options), beatScale: 0.5 }; // Smaller for preview
    const canvas = await this.composer.composeSequenceImage(
      sequence,
      fullOptions
    );
    return canvas.toDataURL();
  }

  private mergeWithDefaults(options: Partial<ExportOptions>): ExportOptions {
    return {
      // Match desktop defaults exactly
      includeStartPosition: true,
      addBeatNumbers: true,
      addReversalSymbols: true,
      addUserInfo: true,
      addWord: true,
      combinedGrids: false,
      beatScale: 1,
      beatSize: BASE_BEAT_SIZE,
      margin: BASE_MARGIN,
      redVisible: true,
      blueVisible: true,
      userName: this.settingsService.getCurrentUser(),
      exportDate: new Date().toLocaleDateString(),
      notes: "Created using The Kinetic Alphabet",
      ...options,
    };
  }
}
```

---

## **PHASE 7: Reactive State Layer**

### **7.1 Image Export State**

```typescript
// File: src/lib/state/image-export-state.svelte.ts
export function createImageExportState(exportService: IImageExportService) {
  // Export options state
  let exportOptions = $state<ExportOptions>({
    includeStartPosition: true,
    addBeatNumbers: true,
    addReversalSymbols: true,
    addUserInfo: true,
    addWord: true,
    combinedGrids: false,
    beatScale: 1,
    redVisible: true,
    blueVisible: true,
    // ... all options
  });

  // Preview state
  let previewImageUrl = $state<string | null>(null);
  let isGeneratingPreview = $state(false);
  let previewError = $state<string | null>(null);

  // Export state
  let isExporting = $state(false);
  let exportError = $state<string | null>(null);
  let lastExportedFile = $state<string | null>(null);

  // Derived state for validation
  let canExport = $derived(() => {
    return !isExporting && !isGeneratingPreview;
  });

  // Actions
  async function updateOptions(newOptions: Partial<ExportOptions>) {
    exportOptions = { ...exportOptions, ...newOptions };
    await generatePreview(); // Auto-update preview
  }

  async function generatePreview(sequence?: SequenceData) {
    if (!sequence) return;

    isGeneratingPreview = true;
    previewError = null;

    try {
      previewImageUrl = await exportService.generatePreview(
        sequence,
        exportOptions
      );
    } catch (error) {
      previewError =
        error instanceof Error ? error.message : "Preview generation failed";
      previewImageUrl = null;
    } finally {
      isGeneratingPreview = false;
    }
  }

  async function exportSequence(sequence: SequenceData) {
    isExporting = true;
    exportError = null;

    try {
      const blob = await exportService.exportSequenceImage(
        sequence,
        exportOptions
      );

      // Generate filename and download
      const filename = `${sequence.word || "sequence"}_v1.png`;
      const { downloadFile } = await import("$lib/utils/file-download");
      await downloadFile(blob, filename);

      lastExportedFile = filename;
    } catch (error) {
      exportError = error instanceof Error ? error.message : "Export failed";
    } finally {
      isExporting = false;
    }
  }

  return {
    // State
    get exportOptions() {
      return exportOptions;
    },
    get previewImageUrl() {
      return previewImageUrl;
    },
    get isGeneratingPreview() {
      return isGeneratingPreview;
    },
    get previewError() {
      return previewError;
    },
    get isExporting() {
      return isExporting;
    },
    get exportError() {
      return exportError;
    },
    get lastExportedFile() {
      return lastExportedFile;
    },
    get canExport() {
      return canExport;
    },

    // Actions
    updateOptions,
    generatePreview,
    exportSequence,
  };
}
```

---

## **PHASE 8: Updated UI Components**

### **8.1 Enhanced Export Preview**

```typescript
// File: src/lib/components/export/ExportPreviewCard.svelte (Updated)
<script lang="ts">
  import { resolve } from '$lib/services/bootstrap';
  import { createImageExportState } from '$lib/state/image-export-state.svelte';

  interface Props {
    currentSequence: SequenceData | null;
    exportSettings: ExportOptions;
  }

  let { currentSequence, exportSettings }: Props = $props();

  // Get export service and create state
  const exportService = resolve('IImageExportService');
  const exportState = createImageExportState(exportService);

  // Sync settings with state
  $effect(() => {
    exportState.updateOptions(exportSettings);
  });

  // Generate preview when sequence changes
  $effect(() => {
    if (currentSequence) {
      exportState.generatePreview(currentSequence);
    }
  });
</script>

<div class="export-preview-card">
  <!-- Real preview using generated image -->
  {#if exportState.previewImageUrl}
    <img src={exportState.previewImageUrl} alt="Export preview" class="preview-image" />
  {:else if exportState.isGeneratingPreview}
    <div class="preview-loading">Generating preview...</div>
  {:else if exportState.previewError}
    <div class="preview-error">{exportState.previewError}</div>
  {:else}
    <div class="preview-placeholder">No sequence to preview</div>
  {/if}
</div>
```

### **8.2 Enhanced Export Actions**

```typescript
// File: src/lib/components/export/ExportActionsCard.svelte (Updated)
<script lang="ts">
  import { resolve } from '$lib/services/bootstrap';
  import { createImageExportState } from '$lib/state/image-export-state.svelte';

  interface Props {
    currentSequence: SequenceData | null;
    exportSettings: ExportOptions;
  }

  let { currentSequence, exportSettings }: Props = $props();

  const exportService = resolve('IImageExportService');
  const exportState = createImageExportState(exportService);

  async function handleExportCurrent() {
    if (!currentSequence) return;

    // Update state with current settings
    await exportState.updateOptions(exportSettings);

    // Export sequence
    await exportState.exportSequence(currentSequence);
  }
</script>

<div class="export-actions-card">
  <button
    onclick={handleExportCurrent}
    disabled={!exportState.canExport || !currentSequence}
    class="export-button"
  >
    {#if exportState.isExporting}
      Exporting...
    {:else}
      Export Current Sequence
    {/if}
  </button>

  {#if exportState.exportError}
    <div class="error-message">{exportState.exportError}</div>
  {/if}

  {#if exportState.lastExportedFile}
    <div class="success-message">Exported: {exportState.lastExportedFile}</div>
  {/if}
</div>
```

---

## **PHASE 9: Testing & Validation**

### **9.1 Visual Regression Tests**

```typescript
// File: src/lib/services/__tests__/image-export-visual.test.ts
import { describe, it, expect } from "vitest";
import { ImageExportService } from "../implementations/ImageExportService";
import { createTestSequence } from "../test-helpers";

describe("Visual Export Compatibility", () => {
  it("should match desktop layout for 4-beat sequence", async () => {
    const sequence = createTestSequence(4);
    const exportService = new ImageExportService();

    const canvas = await exportService.composeSequenceImage(sequence, {
      includeStartPosition: true,
      addBeatNumbers: true,
      beatScale: 1,
    });

    // Verify dimensions match desktop calculation
    expect(canvas.width).toBe(5 * 144); // 5 columns * 144px beat size
    expect(canvas.height).toBe(1 * 144 + 300 + 150); // 1 row + top + bottom margin
  });

  it("should match desktop font scaling for single beat", async () => {
    const sequence = createTestSequence(1);
    // Test font scaling logic matches desktop FontMarginHelper
  });
});
```

### **9.2 Size Compatibility Tests**

```typescript
// File: src/lib/services/__tests__/layout-compatibility.test.ts
describe("Desktop Layout Compatibility", () => {
  const testCases = [
    { beats: 0, startPosition: true, expected: [1, 1] },
    { beats: 1, startPosition: true, expected: [2, 1] },
    { beats: 4, startPosition: true, expected: [5, 1] },
    { beats: 5, startPosition: true, expected: [4, 2] },
    { beats: 9, startPosition: true, expected: [4, 3] },
    // ... test all desktop layout combinations
  ];

  testCases.forEach(({ beats, startPosition, expected }) => {
    it(`should calculate ${beats} beats with startPosition=${startPosition} as ${expected}`, () => {
      const layoutService = new LayoutCalculationService();
      const result = layoutService.calculateLayout(beats, startPosition);
      expect(result).toEqual(expected);
    });
  });
});
```

---

## **PHASE 10: Performance Optimization**

### **10.1 Canvas Pool & Caching**

```typescript
// File: src/lib/services/implementations/CanvasPoolService.ts
export class CanvasPoolService {
  private pool: HTMLCanvasElement[] = [];
  private cache = new Map<string, HTMLCanvasElement>();

  getCanvas(width: number, height: number): HTMLCanvasElement {
    const canvas = this.pool.pop() || document.createElement("canvas");
    canvas.width = width;
    canvas.height = height;
    return canvas;
  }

  releaseCanvas(canvas: HTMLCanvasElement): void {
    // Clear and return to pool
    const ctx = canvas.getContext("2d")!;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    this.pool.push(canvas);
  }

  getCachedBeat(
    beatId: string,
    options: RenderOptions
  ): HTMLCanvasElement | null {
    const key = `${beatId}-${JSON.stringify(options)}`;
    return this.cache.get(key) || null;
  }

  cacheBeat(
    beatId: string,
    options: RenderOptions,
    canvas: HTMLCanvasElement
  ): void {
    const key = `${beatId}-${JSON.stringify(options)}`;
    this.cache.set(key, canvas);
  }
}
```

---

## 📋 **IMPLEMENTATION CHECKLIST**

### **Phase 1: Core Architecture** ⭐ _Priority 1_

- [ ] Create service interfaces (`image-export-interfaces.ts`)
- [ ] Set up DI registration (`image-export-services.ts`)
- [ ] Add to bootstrap (`bootstrap.ts`)
- [ ] Create basic service shells

### **Phase 2: Layout System** ⭐ _Priority 2_

- [ ] `LayoutCalculationService` with exact desktop tables
- [ ] `DimensionCalculationService` matching `HeightDeterminer`
- [ ] Layout compatibility tests
- [ ] Visual dimension verification

### **Phase 3: Beat Rendering** ⭐ _Priority 3_

- [ ] `BeatRenderingService` with SVG→Canvas conversion
- [ ] Start position rendering
- [ ] Visibility filter application
- [ ] Combined grid overlay (`GridOverlayService`)

### **Phase 4: Text System** ⭐ _Priority 4_

- [ ] `TextRenderingService` with exact font matching
- [ ] Custom kerning implementation
- [ ] User info layout (3-column bottom layout)
- [ ] Difficulty badge with gradients

### **Phase 5: Composition** ⭐ _Priority 5_

- [ ] `ImageCompositionService` orchestration
- [ ] Grid positioning algorithm
- [ ] Layer ordering (background → beats → text)
- [ ] Quality settings and output format

### **Phase 6: Export Operations** ⭐ _Priority 6_

- [ ] `FileExportService` with browser download
- [ ] Filename generation and versioning
- [ ] Format options (PNG/JPEG)
- [ ] Error handling and user feedback

### **Phase 7: State Integration** ⭐ _Priority 7_

- [ ] `createImageExportState` runes factory
- [ ] Reactive preview generation
- [ ] Settings persistence integration
- [ ] Export status management

### **Phase 8: UI Updates** ⭐ _Priority 8_

- [ ] Enhanced `ExportPreviewCard` with real preview
- [ ] Updated `ExportActionsCard` with service integration
- [ ] Settings validation and feedback
- [ ] Progress indicators and error states

### **Phase 9: Testing** ⭐ _Priority 9_

- [ ] Visual regression test suite
- [ ] Layout compatibility verification
- [ ] Performance benchmarks
- [ ] Cross-browser compatibility

### **Phase 10: Optimization** ⭐ _Priority 10_

- [ ] Canvas pooling and reuse
- [ ] Beat rendering cache
- [ ] Memory management
- [ ] Bundle size optimization

---

## 🎯 **SUCCESS CRITERIA**

### **Pixel-Perfect Compatibility**

- ✅ Images exported from web app match desktop app exactly in dimensions
- ✅ Layout grids use identical algorithms and measurements
- ✅ Typography renders with same fonts, sizes, and kerning
- ✅ Text positioning matches desktop placement precisely

### **Feature Parity**

- ✅ All desktop export options available in web version
- ✅ Start position inclusion/exclusion works identically
- ✅ Beat numbering, reversal symbols, user info all render correctly
- ✅ Combined grid mode overlays both diamond and box grids
- ✅ Difficulty level badges with correct gradients and positioning

### **Performance & UX**

- ✅ Preview generation under 1 second for typical sequences
- ✅ Full export under 3 seconds for complex sequences
- ✅ Smooth integration with existing UI components
- ✅ Proper error handling and user feedback
- ✅ Canvas memory management prevents browser crashes

### **Architecture Compliance**

- ✅ All business logic in service layer, no logic in components
- ✅ Reactive state uses Svelte 5 runes exclusively
- ✅ Services registered through DI container properly
- ✅ Clean separation between rendering and composition concerns
- ✅ Testable components with proper dependency injection

---

## 🚀 **NEXT STEPS**

1. **Start with Phase 1**: Create the service interfaces and basic shells
2. **Implement Phase 2**: Get layout calculations working with desktop compatibility
3. **Build Phase 3**: Create the beat rendering engine with SVG conversion
4. **Iterate through phases**: Each phase builds on the previous foundation
5. **Test continuously**: Validate against desktop output at each phase

This game plan provides a **complete roadmap** for creating a web-based image export system that maintains perfect compatibility with your desktop application while following your modern SvelteKit architecture patterns. The phased approach ensures steady progress with testable milestones at each step.

Ready to begin? **Phase 1** is your starting point! 🎯
