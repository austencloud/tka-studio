# Sequence Card Tab - Web Implementation

This directory contains the complete web implementation of the Sequence Card tab, cloning the functionality and styling from the desktop modern app.

## Overview

The Sequence Card tab provides a visual interface for managing and viewing sequence cards, similar to the desktop modern app implementation.

## Components

### Main Components

- **`SequenceCardTab.svelte`** - Main tab component that orchestrates the entire sequence card interface
- **`SequenceCardHeader.svelte`** - Header component with title, progress tracking, and action buttons
- **`SequenceCardNavigation.svelte`** - Sidebar navigation with length selection and column count controls
- **`SequenceCardContent.svelte`** - Main content area displaying sequence cards in a responsive grid
- **`SequenceCard.svelte`** - Individual sequence card component with preview and metadata

### Features Implemented

#### Header Component

- **Title and Description**: "Sequence Card Manager" with dynamic status messages
- **Progress Bar**: Shows loading/export/regeneration progress
- **Action Buttons**: Export All, Refresh, and Regenerate Images functionality
- **Status Management**: Tracks loading, exporting, and regenerating states

#### Navigation Component

- **Length Selection**: Buttons for All, 2, 3, 4, 5, 6, 8, 10, 12, 16 beats (matching desktop exactly)
- **Active State**: Visual indication of selected length
- **Column Selector**: Dropdown to choose 2-6 preview columns
- **Responsive Design**: Adapts layout for mobile devices

#### Content Component

- **Grid Layout**: Responsive grid that adjusts based on column count selection
- **Progressive Loading**: Simulates desktop app's progressive loading behavior
- **Empty States**: Shows appropriate messages when no sequences are available
- **Scroll Position**: Preserves scroll position when switching between lengths

#### Individual Cards

- **Visual Preview**: Color-coded preview with beat visualization
- **Metadata Display**: Shows beats, difficulty, grid mode, and author
- **Action Buttons**: Export and view details functionality
- **Loading States**: Progressive loading simulation with spinners
- **Hover Effects**: Enhanced interactivity matching desktop styling

## Styling

### Design System

- **Dark Theme**: Matches desktop app's dark gradient theme
- **Color Palette**: Uses CSS custom properties for theming
- **Typography**: Consistent font sizes and weights
- **Spacing**: Uses design system spacing variables

### Visual Elements

- **Gradients**: Linear gradients matching desktop (#34495e to #2c3e50 for headers)
- **Border Radius**: Consistent rounded corners (10-12px)
- **Shadows**: Subtle drop shadows for depth
- **Hover States**: Transform and shadow effects on interactive elements

### Responsive Behavior

- **Mobile Layout**: Stacks navigation and content vertically
- **Tablet Layout**: Adjusts grid columns and button sizes
- **Desktop Layout**: Full two-panel layout with sidebar

## State Management

### Props and Events

- **Length Selection**: Communicates selected length via custom events
- **Column Count**: Tracks and updates grid layout
- **Loading States**: Manages multiple loading states (sequences, export, regeneration)
- **Progress Tracking**: Real-time progress updates for long operations

### Data Flow

1. Main tab component coordinates all child components
2. Navigation emits length/column changes
3. Content component filters and displays sequences
4. Individual cards handle their own loading states

## Integration

### Dependencies

- **Svelte 5**: Uses modern runes-based reactivity
- **Type Safety**: Full TypeScript integration
- **Event System**: Custom event dispatching for component communication

### Services Integration

- **Sequence Store**: Integrates with existing sequence state management
- **Export Services**: Ready for actual export service integration
- **Settings**: Column count and other preferences can be persisted

## Usage

```svelte
<script>
	import SequenceCardTab from './tabs/SequenceCardTab.svelte';
</script>

<SequenceCardTab />
```

The component is fully self-contained and handles all internal state management.

## Future Enhancements

### Planned Features

- **Actual Image Generation**: Replace placeholders with real sequence visualizations
- **Export Implementation**: Connect to actual export services
- **Drag & Drop**: Card reordering and organization
- **Search & Filter**: Advanced filtering options
- **Batch Operations**: Select multiple cards for operations

### Performance Optimizations

- **Virtual Scrolling**: For large sequence collections
- **Image Caching**: Efficient image loading and caching
- **Lazy Loading**: Load cards only when visible

## Files Created

```
/tabs/
├── SequenceCardTab.svelte              # Main tab component
└── sequence_card/
    ├── SequenceCardHeader.svelte       # Header with actions
    ├── SequenceCardNavigation.svelte   # Sidebar navigation
    ├── SequenceCardContent.svelte      # Grid content area
    └── SequenceCard.svelte            # Individual card
```

All components follow modern Svelte 5 patterns with runes-based reactivity and maintain full type safety throughout.
