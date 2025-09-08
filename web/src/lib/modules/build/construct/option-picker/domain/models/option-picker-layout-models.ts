/**
 * Layout Domain Types
 *
 * Core types for layout calculations, device detection, and responsive design
 */

// ============================================================================
// DEVICE AND VIEWPORT TYPES
// ============================================================================

import type {
  ContainerAspect,
} from "$shared";
import type { DeviceType } from "../../../../../../shared/device/domain/enums/device-enums";

// ============================================================================
// CONFIGURATION TYPES
// ============================================================================



export interface LayoutTemplate {
  cols: number;
  class: string;
}

export interface TwoItemsLayoutTemplate {
  horizontal: LayoutTemplate;
  vertical: LayoutTemplate;
}

export interface ResponsiveLayoutTemplates {
  singleItem: LayoutTemplate;
  twoItems: TwoItemsLayoutTemplate;
  fewItems: {
    portraitDevice: LayoutTemplate;
    landscapeDevice: LayoutTemplate;
  };
  mediumItems: {
    portraitDevice: LayoutTemplate;
    landscapeDevice: LayoutTemplate;
  };
  manyItems: {
    portraitDevice: LayoutTemplate;
    landscapeDevice: LayoutTemplate;
  };
}




export interface OptionPickerGridConfig {
  columns: number;
  gap: string;
  itemSize: number;
  gridClass: string;
  aspectClass: string;
  scaleFactor: number;
}

export interface OptionPickerLayoutCalculationParams {
  count: number;
  containerWidth: number;
  containerHeight: number;
  windowWidth?: number;
  windowHeight?: number;
  isMobileUserAgent?: boolean;
}

export interface OptionPickerLayoutCalculationResult {
  optionsPerRow: number;
  optionSize: number;
  gridGap: string;
  gridColumns: string;
  gridClass: string;
  aspectClass: string;
  scaleFactor: number;
  deviceType: DeviceType;
  containerAspect: ContainerAspect;
  layoutCategory: LayoutCategory;
  canFitHorizontally: boolean;
  optimalSize: number;
  isMobile: boolean;
  isTablet: boolean;
  isPortrait: boolean;
  debugInfo?: {
    userAgent: string;
    dimensions: { width: number; height: number };
    matchedSpecs?: string[];
  };
}

export interface ResponsiveLayoutConfig {
  gridColumns: string;
  optionSize: string;
  gridGap: string;
  gridClass: string;
  aspectClass: string;
  scaleFactor: number;
}

// Generic layout calculation types
export interface LayoutCalculationParams {
  containerWidth: number;
  containerHeight: number;
  itemCount: number;
  targetColumns?: number;
  deviceType?: DeviceType;
}

export interface LayoutCalculationResult {
  columns: number;
  rows: number;
  itemSize: number;
  gap: string;
  gridClass: string;
  aspectClass: string;
  scaleFactor: number;
}


export interface OptionPickerLayoutDimensions {
  width: number;
  height: number;
}



export interface OptionPickerLayoutResult {
  optionsPerRow: number;
  optionSize: number;
  gridGap: string;
  gridColumns: string;
  gridClass: string;
  aspectClass: string;
  scaleFactor: number;
  deviceType: DeviceType;
  containerAspect: ContainerAspect;
  isMobile: boolean;
  isTablet: boolean;
  isPortrait: boolean;
  layoutConfig: ResponsiveLayoutConfig;
}

export enum ReversalFilter {
  ALL = "all",
  CONTINUOUS = "continuous",
  ONE_REVERSAL = "oneReversal",
  TWO_REVERSALS = "twoReversals",
}

export enum LayoutCategory {
  SINGLE_ITEM = "singleItem",
  TWO_ITEMS = "twoItems",
  FEW_ITEMS = "fewItems",
  MEDIUM_ITEMS = "mediumItems",
  MANY_ITEMS = "manyItems",
}
