/**
 * Responsive Layout Service Implementation
 *
 * Manages all responsive layout logic for two-panel construction interfaces.
 * Determines optimal panel arrangement based on device context.
 *
 * Domain: Create module - Sequence Construction Interface
 */

import type { IDeviceDetector, IViewportService } from "$shared";
import { TYPES } from "$shared";
import { inject, injectable } from "inversify";
import type { IResponsiveLayoutService } from "../contracts/IResponsiveLayoutService";

@injectable()
export class ResponsiveLayoutService implements IResponsiveLayoutService {
  private layoutChangeCallbacks: Set<() => void> = new Set();
  private viewportUnsubscribe: (() => void) | null = null;

  constructor(
    @inject(TYPES.IDeviceDetector) private deviceDetector: IDeviceDetector,
    @inject(TYPES.IViewportService) private viewportService: IViewportService
  ) {}

  initialize(): void {
    // Subscribe to viewport changes and notify listeners
    this.viewportUnsubscribe = this.viewportService.onViewportChange(() => {
      this.notifyLayoutChange();
    });
  }

  dispose(): void {
    if (this.viewportUnsubscribe) {
      this.viewportUnsubscribe();
      this.viewportUnsubscribe = null;
    }
    this.layoutChangeCallbacks.clear();
  }

  getViewportWidth(): number {
    return this.viewportService.width;
  }

  getViewportHeight(): number {
    return this.viewportService.height;
  }

  getNavigationLayout(): "top" | "left" {
    const layout = this.deviceDetector.getNavigationLayoutImmediate();
    // Filter out 'bottom' if present, default to 'top'
    return layout === "left" ? "left" : "top";
  }

  shouldUseSideBySideLayout(): boolean {
    const isDesktop = this.isDesktop();
    const isLandscapeMobile = this.isLandscapeMobile();
    const hasWideViewport = this.hasWideViewport();
    const isLikelyZFold = this.isLikelyZFoldUnfolded();
    const aspectRatio = this.getAspectRatio();
    const isSignificantlyLandscape = aspectRatio >= 1.15;

    // Use side-by-side layout for CreateModule panels when:
    // 1. Desktop with sufficient width for workspace + tool panel
    // 2. Landscape mobile (phone sideways optimizes horizontal space)
    // 3. Z Fold unfolded (wide screen perfect for panel arrangement)
    // 4. Significantly landscape orientation (sequence viewing benefits)
    return (
      (isDesktop && hasWideViewport) ||
      isLandscapeMobile ||
      isLikelyZFold ||
      isSignificantlyLandscape
    );
  }

  isMobilePortrait(): boolean {
    // Mobile portrait is the inverse of side-by-side layout
    // When NOT using side-by-side, we're in mobile portrait stacked layout
    return !this.shouldUseSideBySideLayout();
  }

  isDesktop(): boolean {
    return this.deviceDetector.isDesktop();
  }

  isLandscapeMobile(): boolean {
    return this.deviceDetector.isLandscapeMobile();
  }

  hasWideViewport(): boolean {
    // Standard desktop breakpoint
    return this.getViewportWidth() >= 1024;
  }

  getAspectRatio(): number {
    const width = this.getViewportWidth();
    const height = this.getViewportHeight();
    return height > 0 ? width / height : 1;
  }

  isLikelyZFoldUnfolded(): boolean {
    const width = this.getViewportWidth();
    const aspectRatio = this.getAspectRatio();

    // Z Fold specific: More flexible detection that accounts for browser UI
    return (
      width >= 700 &&
      width <= 950 && // Wider range to account for browser UI
      aspectRatio >= 1.1 &&
      aspectRatio <= 1.4 // Broader aspect ratio range
    );
  }

  onLayoutChange(callback: () => void): () => void {
    this.layoutChangeCallbacks.add(callback);

    // Return unsubscribe function
    return () => {
      this.layoutChangeCallbacks.delete(callback);
    };
  }

  private notifyLayoutChange(): void {
    this.layoutChangeCallbacks.forEach((callback) => callback());
  }
}
