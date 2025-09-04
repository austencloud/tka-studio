/**
 * Panel Management Domain Types
 *
 * Types for browse tab panel management, resizing, and layout.
 * Browse-specific panel state and configuration management.
 */

// ============================================================================
// PANEL MANAGEMENT TYPES
// ============================================================================

export interface BrowsePanelState {
  id: string;
  isVisible: boolean;
  isCollapsed: boolean;
  width: number;
  height?: number;
  position?: { x: number; y: number };
  // Extended properties for TKA panel management
  minWidth: number;
  maxWidth: number;
  defaultWidth: number;
  collapsedWidth: number;
  isResizing: boolean;
}

export interface BrowsePanelConfig {
  id: string;
  title: string;
  defaultWidth: number;
  defaultHeight?: number;
  minWidth: number;
  maxWidth: number;
  minHeight?: number;
  resizable?: boolean;
  collapsible?: boolean;
  collapsedWidth: number;
  persistKey: string;
}

export interface ResizeOperation {
  panelId: string;
  direction: ResizeDirection;
  startPosition: { x: number; y: number };
  startSize: { width: number; height: number };
}

import { ResizeDirection } from "$shared/domain/enums/enums";

export interface SplitterConfig {
  orientation: "horizontal" | "vertical";
  initialPosition: number;
  minPosition: number;
  maxPosition: number;
}
