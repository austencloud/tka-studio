/**
 * Tool Operations Domain Models
 *
 * Defines types and interfaces for sequence toolkit operations.
 * These models represent the various operations that can be performed on sequences.
 */

import { ToolOperationType } from "./toolkit-enums";
import type { ToolOperationMetadata } from "./toolkit-models";



export const TOOL_OPERATIONS: Record<ToolOperationType, ToolOperationMetadata> = {
  [ToolOperationType.MIRROR]: {
    type: ToolOperationType.MIRROR,
    name: "Mirror",
    description: "Mirror the sequence horizontally",
    icon: "🪞",
    isDestructive: false,
    requiresConfirmation: false,
    category: "transform",
  },
  [ToolOperationType.ROTATE_CLOCKWISE]: {
    type: ToolOperationType.ROTATE_CLOCKWISE,
    name: "Rotate Clockwise",
    description: "Rotate the sequence clockwise",
    icon: "🔄",
    isDestructive: false,
    requiresConfirmation: false,
    category: "transform",
  },
  [ToolOperationType.ROTATE_COUNTERCLOCKWISE]: {
    type: ToolOperationType.ROTATE_COUNTERCLOCKWISE,
    name: "Rotate Counterclockwise",
    description: "Rotate the sequence counterclockwise",
    icon: "🔄",
    isDestructive: false,
    requiresConfirmation: false,
    category: "transform",
  },
  [ToolOperationType.SWAP_COLORS]: {
    type: ToolOperationType.SWAP_COLORS,
    name: "Swap Colors",
    description: "Swap red and blue colors",
    icon: "🎨",
    isDestructive: false,
    requiresConfirmation: false,
    category: "transform",
  },
  [ToolOperationType.CLEAR]: {
    type: ToolOperationType.CLEAR,
    name: "Clear",
    description: "Clear all beats in the sequence",
    icon: "🧹",
    isDestructive: true,
    requiresConfirmation: true,
    category: "transform",
  },
  [ToolOperationType.DUPLICATE]: {
    type: ToolOperationType.DUPLICATE,
    name: "Duplicate",
    description: "Create a copy of the sequence",
    icon: "📋",
    isDestructive: false,
    requiresConfirmation: false,
    category: "transform",
  },
  [ToolOperationType.DELETE_SEQUENCE]: {
    type: ToolOperationType.DELETE_SEQUENCE,
    name: "Delete Sequence",
    description: "Delete the entire sequence",
    icon: "🗑️",
    isDestructive: true,
    requiresConfirmation: true,
    category: "delete",
  },
  [ToolOperationType.DELETE_BEAT]: {
    type: ToolOperationType.DELETE_BEAT,
    name: "Delete Beat",
    description: "Delete a single beat",
    icon: "❌",
    isDestructive: true,
    requiresConfirmation: false,
    category: "delete",
  },
  [ToolOperationType.DELETE_BEATS]: {
    type: ToolOperationType.DELETE_BEATS,
    name: "Delete Beats",
    description: "Delete multiple beats",
    icon: "❌",
    isDestructive: true,
    requiresConfirmation: true,
    category: "delete",
  },
  [ToolOperationType.DELETE_BEAT_AND_FOLLOWING]: {
    type: ToolOperationType.DELETE_BEAT_AND_FOLLOWING,
    name: "Delete Beat and Following",
    description: "Delete beat and all following beats",
    icon: "❌",
    isDestructive: true,
    requiresConfirmation: true,
    category: "delete",
  },
  [ToolOperationType.CLEAR_BEATS]: {
    type: ToolOperationType.CLEAR_BEATS,
    name: "Clear Beats",
    description: "Clear all beats but keep sequence structure",
    icon: "🧹",
    isDestructive: true,
    requiresConfirmation: true,
    category: "delete",
  },
  [ToolOperationType.EXPORT_JSON]: {
    type: ToolOperationType.EXPORT_JSON,
    name: "Export JSON",
    description: "Export sequence as JSON",
    icon: "📄",
    isDestructive: false,
    requiresConfirmation: false,
    category: "share",
  },
  [ToolOperationType.COPY_JSON]: {
    type: ToolOperationType.COPY_JSON,
    name: "Copy JSON",
    description: "Copy sequence JSON to clipboard",
    icon: "📋",
    isDestructive: false,
    requiresConfirmation: false,
    category: "share",
  },
  [ToolOperationType.ADD_TO_DICTIONARY]: {
    type: ToolOperationType.ADD_TO_DICTIONARY,
    name: "Save",
    description: "Add sequence to Explore",
    icon: "📚",
    isDestructive: false,
    requiresConfirmation: false,
    category: "share",
  },
  [ToolOperationType.EXPORT_FULLSCREEN]: {
    type: ToolOperationType.EXPORT_FULLSCREEN,
    name: "Fullscreen",
    description: "View sequence in fullscreen",
    icon: "🔍",
    isDestructive: false,
    requiresConfirmation: false,
    category: "share",
  },
};
