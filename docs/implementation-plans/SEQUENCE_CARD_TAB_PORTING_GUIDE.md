# Sequence Card Tab: Legacy to Modern Architecture Porting Guide

## Executive Summary

This document provides a comprehensive roadmap for porting the legacy sequence card tab to the modern architecture. The legacy system is a sophisticated 2000+ line codebase with complex image caching, dynamic layouts, and export capabilities. We'll break this down into 5 iterative phases with testing protocols to ensure parity.

## Legacy Architecture Analysis

### Core Components Overview

#### 1. Main Controller (`SequenceCardTab` - 216 lines)

**Purpose**: Entry point and lifecycle coordinator
**Key Responsibilities**:

- Qt event handling (showEvent, resizeEvent, closeEvent)
- Component initialization and coordination
- Loading state management
- Settings persistence integration

**Critical Methods**:

- `_on_length_selected()`: Triggers sequence filtering and loading
- `load_sequences()`: Main sequence loading orchestrator
- `regenerate_all_images()`: Batch image regeneration
- `refresh_layout_after_resize()`: Dynamic layout recalculation

#### 2. Display Orchestration System

**SequenceDisplayManager** (502 lines) - **Most Complex Component**

- **State Management**: Loading states, cancellation, progress tracking
- **Cache Coordination**: Multi-level LRU caching with performance metrics
- **Batch Processing**: Processes sequences in chunks with memory management
- **Layout Calculation**: Dynamic grid sizing based on sequence length
- **Performance Monitoring**: Cache hit/miss ratios, memory usage tracking

**Supporting Components**:

- `ImageProcessor`: Multi-level caching (raw images → scaled images → UI labels)
- `SequenceLoader`: File system interface with metadata extraction
- `LayoutCalculator`: Dynamic grid calculations (sequence length → grid dimensions)
- `PageRenderer`: UI page creation with scaling and layout management
- `ScrollView`: Multi-column scrolling container

#### 3. Navigation & Controls (`SequenceCardNavSidebar` - 115 lines)

- Length selection (2, 3, 4, 5, 6, 8, 10, 12, 16, all)
- Column count selection (1-4 columns)
- Preview layout coordination
- Settings persistence

#### 4. Export System

**SequenceCardImageExporter** (524 lines) - **Second Most Complex**

- Dictionary scanning and sequence enumeration
- TempBeatFrame integration for sequence rendering
- Batch processing with memory management
- PNG compression and metadata embedding
- Progress tracking and cancellation support

#### 5. Settings & Resource Management

- **SequenceCardSettingsHandler**: Settings persistence wrapper
- **SequenceCardResourceManager**: Memory monitoring, file change detection
- **Cache Management**: Multi-level caching with size limits and TTL

### Data Flow Architecture

```
Dictionary Files → SequenceLoader → SequenceDisplayManager → ImageProcessor → PageRenderer → UI
     ↓                                       ↓                        ↓
Settings ←→ SettingsHandler           Cache Manager              Export System
     ↓                                       ↓                        ↓
Navigation Sidebar ←→ Layout Calculator ←→ ScrollView         File System
```

### Key Dependencies

- `MetaDataExtractor`: PNG metadata (sequence length, tags, favorites)
- `TempBeatFrame`: Sequence rendering engine
- `ImageExportManager`: High-quality image export
- `Path helpers`: File system navigation utilities
- Qt widgets and layouts for UI rendering

## Modern Architecture Service Mapping

### Phase 1: Core Data Services (Foundation)

**Target**: Establish data layer without UI dependencies

#### New Services to Create:

1. **`SequenceCardDataService`** ← `SequenceLoader`
   - File system scanning
   - Metadata extraction
   - Sequence filtering by length
   - Data validation

2. **`SequenceCardCacheService`** ← `ImageProcessor` caching logic
   - Raw image caching
   - Scaled image caching
   - Cache performance metrics
   - Memory management

3. **`SequenceCardSettingsService`** ← `SequenceCardSettingsHandler`
   - Column count persistence
   - Last length persistence
   - Cache configuration
   - Export settings

#### Testing Protocol Phase 1:

- **Unit Tests**: Each service in isolation
- **Integration Tests**: Service interaction without UI
- **Performance Tests**: Cache hit rates, memory usage
- **Data Validation**: Sequence loading accuracy vs legacy

### Phase 2: Layout & Display Logic (Business Logic)

**Target**: Extract layout calculations and display logic

#### New Services to Create:

4. **`SequenceCardLayoutService`** ← `LayoutCalculator`
   - Grid dimension calculations
   - Scale factor computations
   - Page size optimization
   - Responsive layout logic

5. **`SequenceCardDisplayService`** ← `SequenceDisplayManager` (business logic only)
   - Display state management
   - Batch processing coordination
   - Loading state tracking
   - Error handling

#### Testing Protocol Phase 2:

- **Layout Tests**: Grid calculations match legacy exactly
- **Display Logic Tests**: State transitions, batch processing
- **Performance Tests**: Display performance vs legacy
- **Cross-Device Tests**: Different screen sizes/resolutions

### Phase 3: Export Services (Complex Business Logic)

**Target**: Extract export functionality into clean services

#### New Services to Create:

6. **`SequenceCardExportService`** ← `SequenceCardImageExporter`
   - Dictionary scanning
   - Batch export processing
   - Progress tracking
   - Error handling

7. **`SequenceCardRenderingService`** ← TempBeatFrame integration
   - Sequence rendering coordination
   - Quality settings management
   - Metadata embedding

#### Testing Protocol Phase 3:

- **Export Tests**: Pixel-perfect comparison with legacy exports
- **Performance Tests**: Export speed and memory usage
- **Metadata Tests**: PNG metadata preservation
- **Batch Tests**: Large dataset export reliability

### Phase 4: Presentation Layer (Qt-Specific UI)

**Target**: Create modern UI components with clean service integration

#### New Components to Create:

8. **`SequenceCardView`** ← Main UI container
9. **`SequenceCardNavigationComponent`** ← Sidebar
10. **`SequenceCardDisplayComponent`** ← Content area
11. **`SequenceCardHeaderComponent`** ← Header with controls

#### Adapters to Create:

- **`SequenceCardQtAdapter`**: Qt signals ↔ Service calls
- **`SequenceCardImageAdapter`**: QPixmap ↔ Service data
- **`SequenceCardLayoutAdapter`**: Qt layouts ↔ Layout service

#### Testing Protocol Phase 4:

- **UI Tests**: Visual parity with legacy
- **Interaction Tests**: Click handling, keyboard navigation
- **Responsive Tests**: Window resizing, column changes
- **Performance Tests**: UI responsiveness vs legacy

### Phase 5: Integration & Optimization

**Target**: Full integration with performance optimization

#### Final Integration:

- Service dependency injection
- Error handling standardization
- Performance monitoring
- Memory leak prevention

#### Testing Protocol Phase 5:

- **End-to-End Tests**: Complete user workflows
- **Performance Tests**: Memory usage, loading times
- **Stress Tests**: Large datasets, rapid interactions
- **Regression Tests**: All legacy functionality preserved

## Detailed Service Specifications

### 1. SequenceCardDataService

```typescript
interface SequenceCardDataService {
  // Core data loading
  getAllSequences(basePath: string): Promise<SequenceData[]>;
  getSequencesByLength(
    sequences: SequenceData[],
    length: number
  ): SequenceData[];

  // Metadata operations
  extractMetadata(imagePath: string): SequenceMetadata;
  validateSequenceData(data: SequenceData): ValidationResult;

  // File system monitoring
  watchDirectoryChanges(
    path: string,
    callback: (changes: FileChange[]) => void
  ): void;
  getDirectoryModificationTime(path: string): Date;
}

interface SequenceData {
  path: string;
  word: string;
  length: number;
  metadata: SequenceMetadata;
  thumbnailPath?: string;
  highResPath?: string;
}

interface SequenceMetadata {
  sequenceLength: number;
  sequence: string;
  tags: string[];
  isFavorite: boolean;
  dateCreated: Date;
  dateModified: Date;
}
```

### 2. SequenceCardCacheService

```typescript
interface SequenceCardCacheService {
  // Raw image caching
  getRawImage(path: string): Promise<ImageData | null>;
  setRawImage(path: string, data: ImageData): void;

  // Scaled image caching
  getScaledImage(path: string, scale: number): Promise<ImageData | null>;
  setScaledImage(path: string, scale: number, data: ImageData): void;

  // Cache management
  clearCache(): void;
  getCacheStats(): CacheStats;
  optimizeCache(): void;

  // Memory management
  getMemoryUsage(): MemoryStats;
  enforceMemoryLimits(): void;
}

interface CacheStats {
  rawCacheHits: number;
  rawCacheMisses: number;
  scaledCacheHits: number;
  scaledCacheMisses: number;
  totalMemoryUsage: number;
  cacheSize: number;
}
```

### 3. SequenceCardLayoutService

```typescript
interface SequenceCardLayoutService {
  // Grid calculations
  calculateOptimalGridDimensions(sequenceLength: number): GridDimensions;
  calculatePageSize(availableWidth: number, columnCount: number): PageSize;
  calculateScaleFactor(originalSize: Size, targetSize: Size): number;

  // Layout optimization
  optimizeLayoutForColumnCount(columnCount: number): LayoutConfig;
  calculateImagePositions(
    gridSize: GridDimensions,
    imageCount: number
  ): Position[];

  // Responsive calculations
  recalculateLayoutForResize(newSize: Size): LayoutUpdate;
}

interface GridDimensions {
  columns: number;
  rows: number;
  totalPositions: number;
}

interface LayoutConfig {
  pageSize: Size;
  scaleFactor: number;
  spacing: number;
  margins: Margins;
}
```

### 4. SequenceCardDisplayService

```typescript
interface SequenceCardDisplayService {
  // Display coordination
  displaySequences(length: number, columnCount: number): Promise<DisplayResult>;
  refreshDisplay(): Promise<void>;
  cancelCurrentOperation(): void;

  // State management
  getDisplayState(): DisplayState;
  setLoadingState(isLoading: boolean): void;
  updateProgress(current: number, total: number): void;

  // Batch processing
  processBatch(
    sequences: SequenceData[],
    batchSize: number
  ): AsyncIterable<BatchResult>;
  getBatchProgress(): BatchProgress;
}

interface DisplayState {
  isLoading: boolean;
  currentLength: number;
  totalSequences: number;
  processedSequences: number;
  cacheHitRatio: number;
}
```

### 5. SequenceCardExportService

```typescript
interface SequenceCardExportService {
  // Export operations
  exportAllPages(): Promise<ExportResult>;
  exportSequenceRange(
    startIndex: number,
    endIndex: number
  ): Promise<ExportResult>;
  regenerateAllImages(): Promise<RegenerationResult>;

  // Progress tracking
  getExportProgress(): ExportProgress;
  cancelExport(): void;

  // Quality settings
  setExportQuality(settings: ExportQualitySettings): void;
  getExportQuality(): ExportQualitySettings;
}

interface ExportQualitySettings {
  pngCompression: number; // 0-9
  highQuality: boolean;
  dpi: number;
  colorDepth: number;
}
```

## Testing Protocols

### Unit Testing Strategy

#### Phase 1 - Data Services

```typescript
describe("SequenceCardDataService", () => {
  test("getAllSequences should return valid sequence data", async () => {
    // Test data loading accuracy
    // Compare with legacy output
    // Validate metadata extraction
  });

  test("getSequencesByLength should filter correctly", () => {
    // Test all length values (2,3,4,5,6,8,10,12,16)
    // Ensure exact match with legacy filtering
  });

  test("extractMetadata should handle all PNG types", () => {
    // Test metadata extraction parity
    // Handle missing metadata gracefully
  });
});
```

#### Phase 2 - Layout Services

```typescript
describe("SequenceCardLayoutService", () => {
  test("calculateOptimalGridDimensions should match legacy", () => {
    // Test grid mapping: length → (cols, rows)
    // Verify exact legacy parity
    const legacyMappings = {
      2: [3, 2],
      3: [3, 2],
      4: [10, 2],
      5: [2, 3],
      6: [2, 3],
      8: [5, 2],
      10: [4, 3],
      12: [4, 3],
      16: [3, 2],
    };
  });

  test("calculatePageSize should handle responsive layout", () => {
    // Test different screen sizes
    // Verify column count scaling
  });
});
```

### Integration Testing Strategy

#### Cross-Service Integration

```typescript
describe("Service Integration", () => {
  test("data → cache → display pipeline", async () => {
    // Load sequences through data service
    // Verify caching behavior
    // Test display coordination
  });

  test("settings persistence across services", () => {
    // Change settings in one service
    // Verify propagation to dependent services
  });
});
```

### Performance Testing Strategy

#### Memory Usage Testing

```typescript
describe("Performance Tests", () => {
  test("memory usage within limits", async () => {
    // Load large datasets
    // Monitor memory consumption
    // Verify garbage collection
    expect(memoryUsage).toBeLessThan(MEMORY_LIMIT);
  });

  test("cache performance matches legacy", async () => {
    // Compare cache hit rates
    // Measure loading times
    // Verify image quality
  });
});
```

### Visual Regression Testing

#### Pixel-Perfect Comparison

```typescript
describe("Visual Regression", () => {
  test("sequence card layout matches legacy", async () => {
    // Generate screenshots
    // Compare with legacy screenshots
    // Verify pixel-perfect match
  });

  test("export quality matches legacy", async () => {
    // Export same sequences
    // Compare file sizes and quality
    // Verify metadata preservation
  });
});
```

## Common Pitfalls & Prevention

### 1. **Cache Synchronization Issues**

**Problem**: Cache inconsistency between services
**Prevention**:

- Single source of truth for cache state
- Event-driven cache invalidation
- Atomic cache operations

### 2. **Memory Leaks in Image Processing**

**Problem**: QPixmap/PIL objects not properly disposed
**Prevention**:

- Explicit resource disposal
- Memory monitoring
- Weak references where appropriate

### 3. **Layout Calculation Precision**

**Problem**: Floating-point rounding differences
**Prevention**:

- Use integer calculations where possible
- Consistent rounding strategies
- Regression tests with exact values

### 4. **Qt Signal/Slot Timing**

**Problem**: Race conditions in UI updates
**Prevention**:

- Proper signal ordering
- State validation before updates
- Debouncing for rapid events

### 5. **Settings Migration**

**Problem**: Legacy settings format incompatibility
**Prevention**:

- Migration utilities
- Backward compatibility layer
- Default value handling

### 6. **File System Path Handling**

**Problem**: Path separator differences, encoding issues
**Prevention**:

- Use Path objects consistently
- UTF-8 encoding everywhere
- Cross-platform testing

### 7. **Batch Processing Interruption**

**Problem**: Incomplete state after cancellation
**Prevention**:

- Atomic batch operations
- Proper cleanup on cancellation
- State restoration mechanisms

### 8. **Export Quality Regression**

**Problem**: Different compression/quality settings
**Prevention**:

- Exact setting replication
- Binary comparison tests
- Quality metrics validation

## Implementation Timeline

### Week 1-2: Phase 1 (Data Services)

- Implement SequenceCardDataService
- Implement SequenceCardCacheService
- Implement SequenceCardSettingsService
- Unit tests and data validation

### Week 3-4: Phase 2 (Layout Services)

- Implement SequenceCardLayoutService
- Implement SequenceCardDisplayService
- Layout calculation tests
- Performance benchmarking

### Week 5-6: Phase 3 (Export Services)

- Implement SequenceCardExportService
- Implement SequenceCardRenderingService
- Export quality validation
- Batch processing tests

### Week 7-8: Phase 4 (Presentation Layer)

- Implement modern UI components
- Implement Qt adapters
- Visual regression testing
- User interaction testing

### Week 9-10: Phase 5 (Integration)

- Full integration testing
- Performance optimization
- Bug fixing and polish
- Documentation completion

## Success Criteria

### Functional Parity

- [ ] All sequence lengths display correctly
- [ ] Column count changes work seamlessly
- [ ] Export functionality produces identical results
- [ ] Settings persistence works across sessions
- [ ] Performance matches or exceeds legacy

### Code Quality

- [ ] Clean service separation
- [ ] Comprehensive test coverage (>90%)
- [ ] No memory leaks
- [ ] Proper error handling
- [ ] Clear documentation

### Performance Benchmarks

- [ ] Sequence loading: <2 seconds for 1000+ sequences
- [ ] Memory usage: <500MB for typical operations
- [ ] Cache hit rate: >80% for repeated operations
- [ ] Export speed: Match legacy ±10%
- [ ] UI responsiveness: <100ms for interactions

This guide provides the foundation for a successful, iterative port of the sequence card tab while maintaining full compatibility and improving the architecture for future maintenance and enhancement.
