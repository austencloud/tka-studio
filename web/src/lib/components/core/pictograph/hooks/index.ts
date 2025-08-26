/**
 * Pictograph Hooks - Logical separation of concerns
 *
 * These hooks break down the Pictograph component into focused,
 * easy-to-understand pieces:
 *
 * - usePictographData: Data transformation and derivation
 * - useComponentLoading: Component loading state management
 * - useArrowPositioning: Arrow positioning coordination
 */

export { usePictographData } from "./usePictographData";
export { useComponentLoading } from "./useComponentLoading";
export { useArrowPositioning } from "./useArrowPositioning";

export type {
  PictographDataProps,
  PictographDataState,
} from "./usePictographData";
export type {
  ComponentLoadingProps,
  ComponentLoadingState,
} from "./useComponentLoading";
export type { ArrowPositioningProps } from "./useArrowPositioning";
